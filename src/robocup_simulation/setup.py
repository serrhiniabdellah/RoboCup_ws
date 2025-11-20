from setuptools import setup
import os
from glob import glob

package_name = 'robocup_simulation'

launch_files = [
    ('share/' + package_name + '/launch', f) for f in glob('launch/*.launch.py')
]

data_files = [
    ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
    ('share/' + package_name, ['package.xml']),
] + launch_files

setup(
    name=package_name,
    version='0.1.0',
    packages=[package_name],
    data_files=data_files,
    install_requires=['setuptools', 'pyserial'],
    zip_safe=True,
    maintainer='Your Name',
    maintainer_email='you@example.com',
    description='Arduino Mega serial bridge for ROS2 (cmd_vel <-> odom)',
    license='MIT',
    entry_points={
        'console_scripts': [
            'arduino_bridge = robocup_simulation.arduino_bridge:main',
        ],
    },
)
