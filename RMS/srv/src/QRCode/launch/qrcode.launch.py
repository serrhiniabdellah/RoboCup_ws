from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='qrcode',
            executable='qrcode_node',
            name='my_qr_code_detector',
            output='screen'
        )
    ])
