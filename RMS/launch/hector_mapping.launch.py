import os
from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='hector_mapping',
            executable='hector_mapping',
            name='hector_mapping',
            output='screen',
            parameters=[{
                'pub_map_odom_transform': True,
                'map_frame': 'map',
                'base_frame': 'base_link',
                'odom_frame': 'odom',
                'map_resolution': 0.05,
                'map_size': 2048,
                'map_start_x': 0.5,
                'map_start_y': 0.5,
                'map_multi_res_levels': 2,
                'update_factor_free': 0.4,
                'update_factor_occupied': 0.9,
                'map_update_distance_thresh': 0.4,
                'map_update_angle_thresh': 0.06,
                'laser_z_min_value': -1.0,
                'laser_z_max_value': 1.0,
                'laser_max_dist': 30.0,
                'laser_min_dist': 0.4,
                'scan_topic': 'scan',
                'pub_map_scanline': True,
                'output_timing': False,
                'map_pub_period': 2.0,
            }],
        ),
    ])
