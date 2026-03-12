import rclpy
from rclpy.node import Node
import cv2
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError

class SquareDetectorNode(Node):
    def __init__(self):
        super().__init__('square_detector')
        self.bridge = CvBridge()
        
        self.subscription = self.create_subscription(
            Image,
            '/cv_camera/image_raw',
            self.image_callback,
            10)
        
        self.get_logger().info('SquareDetectorNode has been started.')

    def detect_square(self, frame):
        # Conversion en niveaux de gris
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Application d'un flou pour réduire le bruit
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        
        # Utilisation du seuillage adaptatif pour obtenir une image binaire
        thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)
        
        # Recherche de contours
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for contour in contours:
            # Filtrage des petits contours
            if cv2.contourArea(contour) < 100:
                continue

            # Approximation du contour pour détecter les formes rectangulaires
            approx = cv2.approxPolyDP(contour, 0.02 * cv2.arcLength(contour, True), True)
            if len(approx) == 4:
                # Détection de carré
                (x, y, w, h) = cv2.boundingRect(approx)
                aspect_ratio = w / float(h)
                if 0.95 <= aspect_ratio <= 1.05:
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    def image_callback(self, msg):
        try:
            # Conversion du message ROS en image OpenCV
            frame = self.bridge.imgmsg_to_cv2(msg, "bgr8")
            
            # Détection du carré noir
            self.detect_square(frame)
            
            # Affichage de l'image (optionnel)
            # cv2.imshow("feed", frame)
            # if cv2.waitKey(1) == ord('q'):
            #     pass
            
        except CvBridgeError as e:
            self.get_logger().error(f'CvBridge Error: {e}')

def main(args=None):
    rclpy.init(args=args)
    node = SquareDetectorNode()
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
