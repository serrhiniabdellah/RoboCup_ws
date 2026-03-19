/**
 * @file camera_economique_node.cpp
 * @brief Nœud ROS 2 pour gérer 4 flux vidéo de caméras avec rotation d'image
 * 
 * Ce nœud capture les flux vidéo de 4 caméras (interfaces différentes) et effectue
 * une rotation de 180° sur chaque image avant de les republier. Cela corrige les
 * orientations incorrectes des caméras montées sur le robot.
 * 
 * Publications:
 *   - /output_image_topic : Flux caméra 1 (cv_camera/image_raw) tourné 180°
 *   - /output_image_topic2 : Flux caméra 2 (cv_camera2/image_raw) tourné 180°
 *   - /output_image_topic3 : Flux caméra 3 (cv_camera4/image_raw) tourné 180°
 *   - /output_image_topic4 : Flux caméra 4 (cv_camera6/image_raw) tourné 180°
 * 
 * Souscriptions:
 *   - /cv_camera/image_raw, /cv_camera2/image_raw, /cv_camera4/image_raw, /cv_camera6/image_raw
 * 
 * @date 2024-2025
 * @author Groupe MT5 RoboCup Rescue ISTY
 */

#include <rclcpp/rclcpp.hpp>
#include <image_transport/image_transport.hpp>
#include <cv_bridge/cv_bridge.hpp>
#include <sensor_msgs/image_encodings.hpp>
#include <sensor_msgs/msg/image.hpp>
#include <opencv2/imgproc/imgproc.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <opencv2/core/core.hpp>

using std::placeholders::_1;

/**
 * @class CameraEconomiqueNode
 * @brief Gère 4 flux vidéo et applique une rotation 180° à chaque image
 */
class CameraEconomiqueNode : public rclcpp::Node
{
public:
  /**
   * @brief Constructeur - initialise les 4 paires publisher/subscriber
   */
  CameraEconomiqueNode()
  : Node("camera_economique_node")
  {
    // Publications pour les 4 flux vidéo corrigés
    pub_rotated_1_ = this->create_publisher<sensor_msgs::msg::Image>("/output_image_topic", 10);
    pub_rotated_2_ = this->create_publisher<sensor_msgs::msg::Image>("/output_image_topic2", 10);
    pub_rotated_3_ = this->create_publisher<sensor_msgs::msg::Image>("/output_image_topic3", 10);
    pub_rotated_4_ = this->create_publisher<sensor_msgs::msg::Image>("/output_image_topic4", 10);

    // Souscriptions aux 4 flux caméras bruts - chaque callback sera routé vers son traitement
    sub_1_ = this->create_subscription<sensor_msgs::msg::Image>(
      "/cv_camera/image_raw", 10, std::bind(&CameraEconomiqueNode::imageCb1, this, _1));
    sub_2_ = this->create_subscription<sensor_msgs::msg::Image>(
      "/cv_camera2/image_raw", 10, std::bind(&CameraEconomiqueNode::imageCb2, this, _1));
    sub_3_ = this->create_subscription<sensor_msgs::msg::Image>(
      "/cv_camera4/image_raw", 10, std::bind(&CameraEconomiqueNode::imageCb3, this, _1));
    sub_4_ = this->create_subscription<sensor_msgs::msg::Image>(
      "/cv_camera6/image_raw", 10, std::bind(&CameraEconomiqueNode::imageCb4, this, _1));
      
    RCLCPP_INFO(this->get_logger(), "CameraEconomiqueNode has been started.");
  }

private:
  /**
   * @brief Callback pour l'image brute de caméra 1
   * 
   * @param msg Message d'image ROS2
   */
  void imageCb1(const sensor_msgs::msg::Image::SharedPtr msg)
  {
    process_and_publish(msg, pub_rotated_1_);
  }

  /**
   * @brief Callback pour l'image brute de caméra 2
   */
  void imageCb2(const sensor_msgs::msg::Image::SharedPtr msg)
  {
    process_and_publish(msg, pub_rotated_2_);
  }

  /**
   * @brief Callback pour l'image brute de caméra 3
   */
  void imageCb3(const sensor_msgs::msg::Image::SharedPtr msg)
  {
    process_and_publish(msg, pub_rotated_3_);
  }

  /**
   * @brief Callback pour l'image brute de caméra 4
   */
  void imageCb4(const sensor_msgs::msg::Image::SharedPtr msg)
  {
    process_and_publish(msg, pub_rotated_4_);
  }

  /**
   * @brief Traitement commun : conversion ROS → OpenCV, rotation 180°, republication
   * 
   * Convertit le message ROS en mat OpenCV, effectue une rotation de 180°,
   * puis republié le résultat transformé
   * 
   * @param msg Message d'image ROS2 en entrée
   * @param pub Publisher pour envoyer l'image traitée
   */
  void process_and_publish(const sensor_msgs::msg::Image::SharedPtr msg, rclcpp::Publisher<sensor_msgs::msg::Image>::SharedPtr pub)
  {
    cv_bridge::CvImagePtr cv_ptr;
    try
    {
      // Conversion du message ROS2 en format OpenCV (BGR)
      cv_ptr = cv_bridge::toCvCopy(msg, sensor_msgs::image_encodings::BGR8);
    }
    catch (cv_bridge::Exception& e)
    {
      RCLCPP_ERROR(this->get_logger(), "cv_bridge exception: %s", e.what());
      return;
    }

    // Rotation de 180° (inversion horizontale + verticale)
    cv::Mat rotated_image;
    cv::rotate(cv_ptr->image, rotated_image, cv::ROTATE_180);
    cv_ptr->image = rotated_image;

    // Conversion retour en message ROS2 et publication
    pub->publish(*(cv_ptr->toImageMsg()));
  }

  // Subscriptions aux 4 flux caméras
  rclcpp::Subscription<sensor_msgs::msg::Image>::SharedPtr sub_1_;
  rclcpp::Subscription<sensor_msgs::msg::Image>::SharedPtr sub_2_;
  rclcpp::Subscription<sensor_msgs::msg::Image>::SharedPtr sub_3_;
  rclcpp::Subscription<sensor_msgs::msg::Image>::SharedPtr sub_4_;

  // Publishers pour les 4 images traitées (tournées 180°)
  rclcpp::Publisher<sensor_msgs::msg::Image>::SharedPtr pub_rotated_1_;
  rclcpp::Publisher<sensor_msgs::msg::Image>::SharedPtr pub_rotated_2_;
  rclcpp::Publisher<sensor_msgs::msg::Image>::SharedPtr pub_rotated_3_;
  rclcpp::Publisher<sensor_msgs::msg::Image>::SharedPtr pub_rotated_4_;
};

/**
 * @brief Fonction principale - initialise ROS 2 et lance le nœud
 */
int main(int argc, char **argv)
{
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<CameraEconomiqueNode>());
  rclcpp::shutdown();
  return 0;
}
