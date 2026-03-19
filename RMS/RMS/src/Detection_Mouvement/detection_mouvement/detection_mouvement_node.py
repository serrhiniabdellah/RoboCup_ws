"""
Module: detection_mouvement_node.py
Détecteur de mouvement basé sur la différence optique entre frames consécutives

Ce nœud ROS 2 détecte les mouvements dans un flux vidéo en calculant la différence
absolue entre deux images consécutives. Les régions avec un fort changement sont
isolées par seuillage et nettoyage morphologique.

Souscriptions:
    - /cv_camera/image_raw : Flux vidéo brut de la caméra

Publications:
    - (Optionnel) Visualisation directe via OpenCV (pour débogage)

@author: Groupe MT5 RoboCup Rescue ISTY
@date: 2024-2025
"""

import rclpy
from rclpy.node import Node
import cv2
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError

class MotionDetectorNode(Node):
    """
    Détecteur de mouvements par analyse de différence optique entre frames.
    
    Utilise l'algorithme de détection de mouvement classique :
    1. Capture deux frames consécutives
    2. Calcule leur différence absolue
    3. Applique un seuillage et un nettoyage morphologique
    4. Extrait et dessine les contours des régions mouvantes
    """
    
    def __init__(self):
        super().__init__('motion_detector')
        self.bridge = CvBridge()
        
        # Buffers pour stocker les deux dernières images (pour calcul différence)
        self.frame1 = None
        self.frame2 = None
        
        # Souscription au flux vidéo brut
        self.subscription = self.create_subscription(
            Image,
            '/cv_camera/image_raw',
            self.image_callback,
            10)
        
        self.get_logger().info('MotionDetectorNode has been started.')

    def image_callback(self, msg):
        """
        Callback pour traiter chaque frame du flux vidéo.
        
        Effectue la détection de mouvement par différence optique et trace
        les bounding boxes autour des régions mouvantes.
        
        Args:
            msg: Message ROS2 d'image
        """
        try:
            # Conversion du message ROS en image OpenCV
            frame = self.bridge.imgmsg_to_cv2(msg, "bgr8")
            
            # ─────────────────────────────────────────────────────────────
            # Initialisation des deux premières frames
            # ─────────────────────────────────────────────────────────────
            
            if self.frame1 is None:
                self.frame1 = frame
                return
            
            if self.frame2 is None:
                self.frame2 = frame
                return
            
            # ─────────────────────────────────────────────────────────────
            # Détection de mouvement par différence optique
            # ─────────────────────────────────────────────────────────────
            
            # Calcul de la différence absolue entre deux frames consécutives
            diff = cv2.absdiff(self.frame1, self.frame2)
            
            # Conversion en niveau de gris
            gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
            
            # Application d'un flou gaussien pour réduire le bruit haute-fréquence
            blur = cv2.GaussianBlur(gray, (5, 5), 0)
            
            # Seuillage binaire : isole les pixels avec changement significatif (>20)
            _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
            
            # Dilatation : comble les petits trous et relie les régions fragmentées
            dilated = cv2.dilate(thresh, None, iterations=3)
            
            # ─────────────────────────────────────────────────────────────
            # Extraction et visualisation des mouvements
            # ─────────────────────────────────────────────────────────────
            
            # Recherche des contours des régions mouvantes
            contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            
            for contour in contours:
                # Filtrage : ignore les très petits mouvements (< 500 pixels²)
                if cv2.contourArea(contour) < 500:
                    continue
                
                # Calcul du bounding rectangle et dessin sur l'image
                (x, y, w, h) = cv2.boundingRect(contour)
                cv2.rectangle(self.frame1, (x, y), (x + w, y + h), (0, 255, 0), 2)
            
            # Affichage optionnel pour débogage (commenté par défaut)
            # cv2.imshow("feed", self.frame1)
            # if cv2.waitKey(40) == ord('q'):
            #     pass
            
            # Décalage des frames pour préparer le prochain cycle
            self.frame1 = self.frame2
            self.frame2 = frame
            
        except CvBridgeError as e:
            self.get_logger().error(f'CvBridge Error: {e}')

def main(args=None):
    """Lance le nœud ROS 2 et gère le cycle de vie."""
    rclpy.init(args=args)
    node = MotionDetectorNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()
        cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
