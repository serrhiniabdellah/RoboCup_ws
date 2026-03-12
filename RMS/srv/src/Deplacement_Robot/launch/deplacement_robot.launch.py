from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='deplacement_robot',
            executable='deplacement_robot_node',
            name='republish_joy_node',
            output='screen'
        )
    ])
