from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='bras_manuel',
            executable='bras_manuel_node',
            name='bras_manuel_ik',
            output='screen'
        ),
        Node(
            package='bras_manuel',
            executable='slider_node.py',
            name='bras_manuel_gui',
            output='screen'
        )
    ])
