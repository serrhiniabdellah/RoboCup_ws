import os

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.conditions import IfCondition
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

def generate_launch_description():
    view_arg = DeclareLaunchArgument(
        'view', default_value='true',
        description='Whether to show image views'
    )

    # Note: cv_camera is not a standard ROS 2 package by default. 
    # Usually v4l2_camera or usb_cam is used. 
    # We maintain the cv_camera node names as requested, assuming the user 
    # has a ROS 2 port of cv_camera installed or will replace it with v4l2_camera.
    
    cv_camera_node = Node(
        package='cv_camera',
        executable='cv_camera_node',
        name='cv_camera',
        output='screen',
        parameters=[
            {'flip_image': False},
            {'device_path': '/dev/video0'}
        ]
    )

    cv_camera2_node = Node(
        package='cv_camera',
        executable='cv_camera_node',
        name='cv_camera2',
        output='screen',
        parameters=[
            {'flip_image': True},
            {'device_id': 2},
            {'image_width': 320},
            {'image_height': 240},
            {'frame_rate': 1.0}
        ]
    )

    cv_camera4_node = Node(
        package='cv_camera',
        executable='cv_camera_node',
        name='cv_camera4',
        output='screen',
        parameters=[
            {'flip_image': True},
            {'device_id': 4},
            {'image_width': 320},
            {'image_height': 240},
            {'frame_rate': 1.0}
        ]
    )

    cv_camera6_node = Node(
        package='cv_camera',
        executable='cv_camera_node',
        name='cv_camera6',
        output='screen',
        parameters=[
            {'flip_image': True},
            {'device_id': 6},
            {'image_width': 320},
            {'image_height': 240},
            {'frame_rate': 1.0}
        ]
    )

    camera_economique_node = Node(
        package='camera_economique',
        executable='camera_economique_node',
        name='camera_economique',
        output='screen'
    )

    image_view_node = Node(
        package='rqt_image_view',
        executable='rqt_image_view',
        name='image_view',
        arguments=['/output_image_topic'],
        condition=IfCondition(LaunchConfiguration('view'))
    )

    image_view2_node = Node(
        package='rqt_image_view',
        executable='rqt_image_view',
        name='image_view2',
        arguments=['/output_image_topic2'],
        condition=IfCondition(LaunchConfiguration('view'))
    )

    image_view3_node = Node(
        package='rqt_image_view',
        executable='rqt_image_view',
        name='image_view3',
        arguments=['/output_image_topic3'],
        condition=IfCondition(LaunchConfiguration('view'))
    )

    image_view4_node = Node(
        package='rqt_image_view',
        executable='rqt_image_view',
        name='image_view4',
        arguments=['/output_image_topic4'],
        condition=IfCondition(LaunchConfiguration('view'))
    )

    return LaunchDescription([
        view_arg,
        cv_camera_node,
        cv_camera2_node,
        cv_camera4_node,
        cv_camera6_node,
        camera_economique_node,
        image_view_node,
        image_view2_node,
        image_view3_node,
        image_view4_node
    ])
