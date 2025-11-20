from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    serial_port = LaunchConfiguration('serial_port')
    baudrate = LaunchConfiguration('baudrate')
    frame_id = LaunchConfiguration('frame_id')
    base_frame_id = LaunchConfiguration('base_frame_id')
    publish_tf = LaunchConfiguration('publish_tf')

    return LaunchDescription([
        DeclareLaunchArgument('serial_port', default_value='COM3', description='Serial port for Arduino'),
        DeclareLaunchArgument('baudrate', default_value='115200', description='Serial baudrate'),
        DeclareLaunchArgument('frame_id', default_value='odom', description='Odometry frame id'),
        DeclareLaunchArgument('base_frame_id', default_value='base_link', description='Base frame id'),
        DeclareLaunchArgument('publish_tf', default_value='true', description='Whether to publish TF odom->base_link'),

        Node(
            package='robocup_simulation',
            executable='arduino_bridge',
            name='arduino_bridge',
            output='screen',
            parameters=[{
                'serial_port': serial_port,
                'baudrate': baudrate,
                'frame_id': frame_id,
                'base_frame_id': base_frame_id,
                'publish_tf': publish_tf,
            }]
        )
    ])
