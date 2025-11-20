#!/usr/bin/env python3
import threading
import struct
import time
from typing import Optional

import serial

try:
    import rclpy
    from rclpy.node import Node
    from geometry_msgs.msg import Twist
    from nav_msgs.msg import Odometry
    from std_msgs.msg import String
    from geometry_msgs.msg import TransformStamped
    from tf2_ros import TransformBroadcaster
except Exception:
    # Allow running basic serial tests without ROS2 installed
    rclpy = None
    Node = object  # type: ignore


MSG_START = 0xAA
MSG_END = 0x55
MSG_CMD_VEL = 0x01
MSG_ODOM = 0x02
MSG_STATUS = 0x03


def yaw_to_quat(theta: float):
    import math
    half = theta * 0.5
    return (0.0, 0.0, math.sin(half), math.cos(half))


class ArduinoBridge(Node):
    def __init__(self):
        super().__init__('arduino_bridge')

        # Parameters
        self.declare_parameter('serial_port', 'COM3')
        self.declare_parameter('baudrate', 115200)
        self.declare_parameter('frame_id', 'odom')
        self.declare_parameter('base_frame_id', 'base_link')
        self.declare_parameter('publish_tf', True)

        self.port = self.get_parameter('serial_port').get_parameter_value().string_value
        self.baudrate = self.get_parameter('baudrate').get_parameter_value().integer_value
        self.frame_id = self.get_parameter('frame_id').get_parameter_value().string_value
        self.base_frame_id = self.get_parameter('base_frame_id').get_parameter_value().string_value
        self.publish_tf = self.get_parameter('publish_tf').get_parameter_value().bool_value

        # Publishers / Subscribers
        self.odom_pub = self.create_publisher(Odometry, 'odom', 10)
        self.status_pub = self.create_publisher(String, 'robot_status', 10)
        self.cmd_sub = self.create_subscription(Twist, 'cmd_vel', self._on_cmd_vel, 10)
        self.tf_broadcaster = TransformBroadcaster(self) if self.publish_tf else None

        # Serial
        self._ser: Optional[serial.Serial] = None
        self._tx_lock = threading.Lock()
        self._rx_thread = threading.Thread(target=self._rx_loop, name='serial_rx', daemon=True)
        self._stop_event = threading.Event()

        self._open_serial()
        self._rx_thread.start()

        self.get_logger().info(f"ArduinoBridge started on {self.port} @ {self.baudrate}")

    def destroy_node(self):
        self._stop_event.set()
        if self._rx_thread.is_alive():
            self._rx_thread.join(timeout=1.0)
        if self._ser and self._ser.is_open:
            try:
                self._ser.close()
            except Exception:
                pass
        super().destroy_node()

    # --- Serial helpers ---
    def _open_serial(self):
        try:
            self._ser = serial.Serial(self.port, self.baudrate, timeout=0.1)
        except Exception as e:
            self.get_logger().error(f"Failed to open serial {self.port}: {e}")
            raise

    def _write_frame(self, msg_type: int, payload: bytes):
        if not self._ser:
            return
        frame = bytes([MSG_START, msg_type]) + payload + bytes([MSG_END])
        with self._tx_lock:
            self._ser.write(frame)

    # --- ROS callbacks ---
    def _on_cmd_vel(self, msg: Twist):
        lin = float(msg.linear.x)
        ang = float(msg.angular.z)
        payload = struct.pack('<ff', lin, ang)
        self._write_frame(MSG_CMD_VEL, payload)

    # --- RX loop ---
    def _rx_loop(self):
        buf = bytearray()
        while not self._stop_event.is_set():
            try:
                if not self._ser:
                    time.sleep(0.1)
                    continue
                chunk = self._ser.read(64)
                if not chunk:
                    continue
                buf.extend(chunk)

                # Try to parse frames
                while True:
                    # Find start byte
                    start_idx = buf.find(bytes([MSG_START]))
                    if start_idx < 0:
                        buf.clear()
                        break
                    if start_idx > 0:
                        del buf[:start_idx]

                    if len(buf) < 2:
                        break  # need at least start+type

                    msg_type = buf[1]

                    expected_len = None
                    if msg_type == MSG_ODOM:
                        expected_len = 1 + 1 + 20 + 1  # S + T + 5 floats + E
                    elif msg_type == MSG_STATUS:
                        expected_len = 1 + 1 + 1 + 1   # S + T + 1 byte + E
                    else:
                        # Unknown/partial -> try to find next start
                        # but first check if we have at least minimal frame to skip
                        if len(buf) >= 3:
                            # drop first byte and resync
                            del buf[0]
                            continue
                        else:
                            break

                    if len(buf) < expected_len:
                        break  # wait more

                    frame = bytes(buf[:expected_len])
                    # Validate end
                    if frame[-1] != MSG_END:
                        # Corrupt frame, drop first byte
                        del buf[0]
                        continue

                    # Extract payload
                    payload = frame[2:-1]
                    if msg_type == MSG_ODOM and len(payload) == 20:
                        x, y, th, vx, vth = struct.unpack('<fffff', payload)
                        self._publish_odom(x, y, th, vx, vth)
                    elif msg_type == MSG_STATUS and len(payload) == 1:
                        code = payload[0]
                        txt = 'ESTOP' if code == 0x00 else f'STATUS_{code}'
                        self.status_pub.publish(String(data=txt))

                    # Consume frame
                    del buf[:expected_len]

            except Exception as e:
                try:
                    self.get_logger().warn(f"Serial RX error: {e}")
                except Exception:
                    pass
                time.sleep(0.05)

    # --- Publishers ---
    def _publish_odom(self, x: float, y: float, th: float, vx: float, vth: float):
        now = self.get_clock().now().to_msg()

        odom = Odometry()
        odom.header.stamp = now
        odom.header.frame_id = self.frame_id
        odom.child_frame_id = self.base_frame_id
        odom.pose.pose.position.x = x
        odom.pose.pose.position.y = y
        odom.pose.pose.position.z = 0.0
        qx, qy, qz, qw = yaw_to_quat(th)
        odom.pose.pose.orientation.x = qx
        odom.pose.pose.orientation.y = qy
        odom.pose.pose.orientation.z = qz
        odom.pose.pose.orientation.w = qw
        odom.twist.twist.linear.x = vx
        odom.twist.twist.angular.z = vth

        self.odom_pub.publish(odom)

        if self.tf_broadcaster:
            tf = TransformStamped()
            tf.header.stamp = now
            tf.header.frame_id = self.frame_id
            tf.child_frame_id = self.base_frame_id
            tf.transform.translation.x = x
            tf.transform.translation.y = y
            tf.transform.translation.z = 0.0
            tf.transform.rotation.x = qx
            tf.transform.rotation.y = qy
            tf.transform.rotation.z = qz
            tf.transform.rotation.w = qw
            self.tf_broadcaster.sendTransform(tf)


def main():
    if rclpy is None:
        print('ROS2 not available. This script is meant to run inside a ROS2 package.')
        return
    rclpy.init()
    node = ArduinoBridge()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
