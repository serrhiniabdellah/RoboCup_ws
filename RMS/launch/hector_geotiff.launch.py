import os
from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='hector_geotiff',
            executable='geotiff_node',
            name='hector_geotiff',
            output='screen',
            parameters=[{
                'map_file_path': os.path.expanduser('~/maps'),
                'map_file_base_name': 'hector_SLAM_map',
                'geotiff_save_period': 60.0,
                'draw_background_checkerboard': False,
                'draw_free_space_grid': True,
                'plugins': ['hector_geotiff/TrajectoryMapWriter']
            }],
        ),
    ])
