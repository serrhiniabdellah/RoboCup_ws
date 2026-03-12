from setuptools import setup

package_name = 'detection_mouvement'

setup(
    name=package_name,
    version='1.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='ubuntu',
    maintainer_email='ubuntu@todo.todo',
    description='The detection_mouvement package for RoboCup Rescue',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'motion_detector = detection_mouvement.detection_mouvement_node:main',
            'square_detector = detection_mouvement.square_detector_node:main',
        ],
    },
)
