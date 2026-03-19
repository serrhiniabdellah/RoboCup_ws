"""
Fichier launch ROS 2 (Python) — Lidar.launch.py
Remplace l'ancien Lidar.launch XML de ROS 1.

Lance :
  - Le driver Hokuyo (urg_node2) sur /dev/ttyACM0
  - Le nœud d'exploration autonome (Exploration_Publisher)
"""

from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([

        # ── Driver LIDAR Hokuyo ──────────────────────────────────────────────
        Node(
            package='urg_node2',
            executable='urg_node2_node',
            name='hokuyo_node',
            output='screen',
            parameters=[{
                'ip_address': '',
                'serial_port': '/dev/ttyACM0',
                'serial_baud': 115200,
                'laser_frame_id': 'laser',
                'publish_intensity': False,
                'publish_multiecho': False,
            }],
        ),

        # ── Nœud principal : exploration autonome avec LIDAR ─────────────────
        Node(
            package='rms_lidar',
            executable='exploration_publisher_node',
            name='exploration_publisher',
            output='screen',
        ),

        # ── (optionnel) Enregistrement commandes manette ─────────────────────
        # Décommenter pour enregistrer une trajectoire manuelle :
        # Node(
        #     package='rms_lidar',
        #     executable='recuperation_data_auto_node',
        #     name='recuperation_data_auto',
        #     output='screen',
        # ),

        # ── (optionnel) Rejeu de trajectoire enregistrée ─────────────────────
        # Décommenter pour rejouer une trajectoire :
        # Node(
        #     package='rms_lidar',
        #     executable='copie_trajet_node',
        #     name='copie_trajet',
        #     output='screen',
        # ),

        # ── (optionnel) Exploration automatique intelligente ──────────────────
        # Node(
        #     package='rms_lidar',
        #     executable='exploration_auto_intelligente_node',
        #     name='exploration_auto_intelligente',
        #     output='screen',
        # ),

        # ── SLAM : Hector Mapping (Optionnel) ──────────────────────────────────
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
                'scan_topic': 'scan',
                'map_resolution': 0.05,
                'map_size': 2048,
            }],
        ),

        # ── (optionnel) Initialisation accéléromètre ─────────────────────────
        # Node(
        #     package='rms_lidar',
        #     executable='init_accelero_node',
        #     name='init_accelero',
        #     output='screen',
        # ),

    ])
