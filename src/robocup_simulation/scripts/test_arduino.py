#!/usr/bin/env python3
import argparse
import struct
import time

import serial

MSG_START = 0xAA
MSG_END = 0x55
MSG_CMD_VEL = 0x01
MSG_ODOM = 0x02
MSG_STATUS = 0x03


def send_cmd(ser: serial.Serial, lin: float, ang: float):
    payload = struct.pack('<ff', float(lin), float(ang))
    frame = bytes([MSG_START, MSG_CMD_VEL]) + payload + bytes([MSG_END])
    ser.write(frame)


def read_frames(ser: serial.Serial, timeout_s: float = 0.0):
    buf = bytearray()
    t0 = time.time()
    while timeout_s <= 0.0 or (time.time() - t0) < timeout_s:
        chunk = ser.read(64)
        if not chunk:
            continue
        buf.extend(chunk)
        while True:
            si = buf.find(bytes([MSG_START]))
            if si < 0:
                buf.clear()
                break
            if si > 0:
                del buf[:si]
            if len(buf) < 2:
                break
            msg_type = buf[1]
            if msg_type == MSG_ODOM:
                needed = 1 + 1 + 20 + 1
            elif msg_type == MSG_STATUS:
                needed = 1 + 1 + 1 + 1
            else:
                del buf[0]
                continue
            if len(buf) < needed:
                break
            frame = bytes(buf[:needed])
            if frame[-1] != MSG_END:
                del buf[0]
                continue
            payload = frame[2:-1]
            if msg_type == MSG_ODOM and len(payload) == 20:
                x, y, th, vx, vth = struct.unpack('<fffff', payload)
                yield ('odom', (x, y, th, vx, vth))
            elif msg_type == MSG_STATUS and len(payload) == 1:
                yield ('status', payload[0])
            del buf[:needed]


def main():
    ap = argparse.ArgumentParser(description='Quick Arduino serial test (no ROS2 needed)')
    ap.add_argument('--port', default='COM3', help='Serial port (Windows: COM3, Linux: /dev/ttyACM0)')
    ap.add_argument('--baud', type=int, default=115200)
    ap.add_argument('--forward', type=float, default=0.2, help='Linear speed (m/s)')
    ap.add_argument('--turn', type=float, default=0.0, help='Angular speed (rad/s)')
    ap.add_argument('--duration', type=float, default=3.0, help='Seconds to drive forward')
    args = ap.parse_args()

    ser = serial.Serial(args.port, args.baud, timeout=0.1)
    print(f'Opened {args.port} @ {args.baud}')

    t_start = time.time()
    try:
        while (time.time() - t_start) < args.duration:
            send_cmd(ser, args.forward, args.turn)
            for kind, data in read_frames(ser, timeout_s=0.05):
                if kind == 'odom':
                    x, y, th, vx, vth = data
                    print(f'ODOM x={x:.3f} y={y:.3f} th={th:.3f} vx={vx:.3f} vth={vth:.3f}')
                elif kind == 'status':
                    print(f'STATUS: {data}')
            time.sleep(0.05)
    finally:
        # Stop
        send_cmd(ser, 0.0, 0.0)
        ser.close()
        print('Stopped and closed serial')


if __name__ == '__main__':
    main()
