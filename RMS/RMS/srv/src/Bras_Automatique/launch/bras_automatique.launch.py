import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='bras_automatique',
            executable='bras_automatique_node',
            name='bras_automatique',
            output='screen'
        ),
        # You can add the hsv_tuner_node here if needed, but it's usually run separately
        # Node(
        #     package='bras_automatique',
        #     executable='hsv_tuner_node',
        #     name='hsv_tuner',
        #     output='screen'
        # )
    ])
