#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import String, Float64MultiArray
import matplotlib.pyplot as plt
from matplotlib.widgets import Button, Slider
import numpy as np

class SliderNode(Node):
    def __init__(self):
        super().__init__('slider_node')
        self.pub_chatter = self.create_publisher(String, 'chatter', 10)
        self.pub_data = self.create_publisher(Float64MultiArray, 'data', 10)
        
        self.rb = 0.0
        
        # Setup Matplotlib GUI
        self.fig, self.ax = plt.subplots(figsize=(8, 6))
        plt.subplots_adjust(left=0.25, bottom=0.25)
        
        # Sliders axes
        ax_tx = plt.axes([0.25, 0.8, 0.65, 0.03])
        ax_ty = plt.axes([0.25, 0.7, 0.65, 0.03])
        ax_tz = plt.axes([0.25, 0.6, 0.65, 0.03])
        ax_rx = plt.axes([0.25, 0.5, 0.65, 0.03])
        ax_ry = plt.axes([0.25, 0.4, 0.65, 0.03])
        ax_rz = plt.axes([0.25, 0.3, 0.65, 0.03])
        ax_gr = plt.axes([0.25, 0.2, 0.65, 0.03])
        
        self.tx_slider = Slider(ax_tx, 'X', -1.0, 1.0, valinit=0.0)
        self.ty_slider = Slider(ax_ty, 'Y', 0.0, 2.0, valinit=0.75)
        self.tz_slider = Slider(ax_tz, 'Z', -1.0, 1.0, valinit=0.0)
        self.rx_slider = Slider(ax_rx, 'Rot X', -180.0, 180.0, valinit=90.0)
        self.ry_slider = Slider(ax_ry, 'Rot Y', -180.0, 180.0, valinit=0.0)
        self.rz_slider = Slider(ax_rz, 'Rot Z', -180.0, 180.0, valinit=0.0)
        self.gr_slider = Slider(ax_gr, 'Pince', 0.0, 1.0, valinit=0.0)
        
        # Reboot button
        ax_button = plt.axes([0.45, 0.05, 0.2, 0.075])
        self.button = Button(ax_button, 'Reboot')
        self.button.on_clicked(self.reboot_callback)

        self.timer = self.create_timer(0.1, self.publish_callback)
        self.get_logger().info('SliderNode has been started.')

    def reboot_callback(self, event):
        self.rb = 1.0
        self.get_logger().info('Reboot button clicked')

    def publish_callback(self):
        # Update publishers based on slider values
        msg_data = Float64MultiArray()
        msg_data.data = [
            self.tx_slider.val,
            self.ty_slider.val,
            self.tz_slider.val,
            self.rx_slider.val,
            self.ry_slider.val,
            self.rz_slider.val,
            self.gr_slider.val,
            self.rb
        ]
        self.pub_data.publish(msg_data)
        
        msg_chatter = String()
        msg_chatter.data = f"Arm Position: X={self.tx_slider.val:.2f}, Y={self.ty_slider.val:.2f}"
        self.pub_chatter.publish(msg_chatter)
        
        if self.rb == 1.0:
            self.rb = 0.0 # Reset after one publish

def main(args=None):
    rclpy.init(args=args)
    node = SliderNode()
    
    # Run matplotlib in a way that doesn't block ROS 2 spin
    # Using plt.ion() or similar or just spinning manually
    plt.ion()
    plt.show()
    
    while rclpy.ok():
        rclpy.spin_once(node, timeout_sec=0.05)
        plt.pause(0.01)
        
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
