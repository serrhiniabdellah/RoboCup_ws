import rclpy
from rclpy.node import Node
import cv2
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError

class MotionDetectorNode(Node):
    def __init__(self):
        super().__init__('motion_detector')
        self.bridge = CvBridge()
        self.frame1 = None
        self.frame2 = None
        
        self.subscription = self.create_subscription(
            Image,
            '/cv_camera/image_raw',
            self.image_callback,
            10)
        
        self.get_logger().info('MotionDetectorNode has been started.')

    def image_callback(self, msg):
        try:
            # Conversion du message ROS en image OpenCV
            frame = self.bridge.imgmsg_to_cv2(msg, "bgr8")
            
            # Initialisation des frames
            if self.frame1 is None:
                self.frame1 = frame
                return
            
            if self.frame2 is None:
                self.frame2 = frame
                return
            
            # Calcul de la différence absolue entre deux images consécutives
            diff = cv2.absdiff(self.frame1, self.frame2)
            
            # Conversion en niveau de gris
            gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
            
            # Application d'un flou pour réduire le bruit
            blur = cv2.GaussianBlur(gray, (5, 5), 0)
            
            # Seuil pour obtenir une image binaire
            _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
            
            # Dilatation de l'image pour combler les trous
            dilated = cv2.dilate(thresh, None, iterations=3)
            
            # Recherche des contours
            contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            
            for contour in contours:
                # Filtrage des petits mouvements
                if cv2.contourArea(contour) < 500:
                    continue
                
                # Dessin des rectangles autour des mouvements détectés
                (x, y, w, h) = cv2.boundingRect(contour)
                cv2.rectangle(self.frame1, (x, y), (x + w, y + h), (0, 255, 0), 2)
            
            # Affichage de l'image
            # cv2.imshow("feed", self.frame1)
            # if cv2.waitKey(40) == ord('q'):
            #     pass
            
            # Mise à jour des images
            self.frame1 = self.frame2
            self.frame2 = frame
            
        except CvBridgeError as e:
            self.get_logger().error(f'CvBridge Error: {e}')

def main(args=None):
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
