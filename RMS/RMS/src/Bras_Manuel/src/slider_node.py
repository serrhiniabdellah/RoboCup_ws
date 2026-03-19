#!/usr/bin/env python3
"""
Module: slider_node.py
Interface GUI pour contrôle manuel du bras robotique via sliders Matplotlib

Ce nœud ROS 2 fournit une interface graphique avec 7 sliders permettant de contrôler:
    - Position: X, Y, Z (coordonnées cartésiennes)
    - Orientation: Rot X, Rot Y, Rot Z (angles d'Euler)
    - Pince: 0.0 (fermée) à 1.0 (ouverte)

Les valeurs sont publiées régulièrement pour contrôler le bras en temps réel.

Publications:
    - /chatter : Message texte avec position actuelle
    - /data : Array Float64 avec les 8 valeurs (7 sliders + état reboot)

@author: Groupe MT5 RoboCup Rescue ISTY
@date: 2024-2025
"""

#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import String, Float64MultiArray
import matplotlib.pyplot as plt
from matplotlib.widgets import Button, Slider
import numpy as np

class SliderNode(Node):
    """
    Interface de contrôle du bras par sliders interactifs.
    
    Émet régulièrement les positions des 7 sliders et l'état du bouton reboot
    qu'un contrôleur d'asservissement peut utiliser pour piloter le bras.
    """
    
    def __init__(self):
        super().__init__('slider_node')
        
        # Publishers pour les données de contrôle
        self.pub_chatter = self.create_publisher(String, 'chatter', 10)
        self.pub_data = self.create_publisher(Float64MultiArray, 'data', 10)
        
        # Flag pour le bouton reboot
        self.rb = 0.0
        
        # ─────────────────────────────────────────────────────────────
        # Configuration de l'interface Matplotlib
        # ─────────────────────────────────────────────────────────────
        
        # Création de la figure et axes principaux
        self.fig, self.ax = plt.subplots(figsize=(8, 6))
        plt.subplots_adjust(left=0.25, bottom=0.25)
        
        # ─────────────────────────────────────────────────────────────
        # Création des 7 sliders de contrôle
        # ─────────────────────────────────────────────────────────────
        
        # Sliders pour la position (coordonnées cartésiennes X, Y, Z)
        ax_tx = plt.axes([0.25, 0.8, 0.65, 0.03])
        ax_ty = plt.axes([0.25, 0.7, 0.65, 0.03])
        ax_tz = plt.axes([0.25, 0.6, 0.65, 0.03])
        
        # Sliders pour l'orientation (angles d'Euler Rot X, Y, Z)
        ax_rx = plt.axes([0.25, 0.5, 0.65, 0.03])
        ax_ry = plt.axes([0.25, 0.4, 0.65, 0.03])
        ax_rz = plt.axes([0.25, 0.3, 0.65, 0.03])
        
        # Slider pour la pince (0=fermée, 1=ouverte)
        ax_gr = plt.axes([0.25, 0.2, 0.65, 0.03])
        
        # Instanciation des sliders avec leurs plages de valeurs
        self.tx_slider = Slider(ax_tx, 'X', -1.0, 1.0, valinit=0.0)
        self.ty_slider = Slider(ax_ty, 'Y', 0.0, 2.0, valinit=0.75)
        self.tz_slider = Slider(ax_tz, 'Z', -1.0, 1.0, valinit=0.0)
        self.rx_slider = Slider(ax_rx, 'Rot X', -180.0, 180.0, valinit=90.0)
        self.ry_slider = Slider(ax_ry, 'Rot Y', -180.0, 180.0, valinit=0.0)
        self.rz_slider = Slider(ax_rz, 'Rot Z', -180.0, 180.0, valinit=0.0)
        self.gr_slider = Slider(ax_gr, 'Pince', 0.0, 1.0, valinit=0.0)
        
        # ─────────────────────────────────────────────────────────────
        # Bouton Reboot
        # ─────────────────────────────────────────────────────────────
        
        ax_button = plt.axes([0.45, 0.05, 0.2, 0.075])
        self.button = Button(ax_button, 'Reboot')
        self.button.on_clicked(self.reboot_callback)

        # Timer ROS pour publier les données périodiquement
        self.timer = self.create_timer(0.1, self.publish_callback)
        self.get_logger().info('SliderNode has been started.')

    def reboot_callback(self, event):
        """
        Callback appelé lorsque le bouton 'Reboot' est cliqué.
        
        Positionne le flag de reboot à 1.0 pour un cycle de publication.
        """
        self.rb = 1.0
        self.get_logger().info('Reboot button clicked')

    def publish_callback(self):
        """
        Callback du timer (100 ms) - publie l'état des sliders.
        
        Crée un message Float64Array avec les 8 valeurs :
        [X, Y, Z, RotX, RotY, RotZ, Pince, Reboot]
        """
        # Construction du message avec toutes les valeurs des sliders
        msg_data = Float64MultiArray()
        msg_data.data = [
            self.tx_slider.val,        # Position X
            self.ty_slider.val,        # Position Y
            self.tz_slider.val,        # Position Z
            self.rx_slider.val,        # Rotation X
            self.ry_slider.val,        # Rotation Y
            self.rz_slider.val,        # Rotation Z
            self.gr_slider.val,        # Ouverture pince
            self.rb                    # Flag reboot
        ]
        self.pub_data.publish(msg_data)
        
        # Publication d'une description textuelle (pour débogage/visualisation)
        msg_chatter = String()
        msg_chatter.data = f"Arm Position: X={self.tx_slider.val:.2f}, Y={self.ty_slider.val:.2f}"
        self.pub_chatter.publish(msg_chatter)
        
        # Réinitialisation du flag reboot après publication
        if self.rb == 1.0:
            self.rb = 0.0

def main(args=None):
    """Lance le nœud ROS 2 avec interface Matplotlib interactive."""
    rclpy.init(args=args)
    node = SliderNode()
    
    # Activation du mode interactif de Matplotlib
    plt.ion()
    plt.show()
    
    # Boucle d'exécution : spin ROS + événements Matplotlib
    while rclpy.ok():
        rclpy.spin_once(node, timeout_sec=0.05)
        plt.pause(0.01)
        
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
