#include <rclcpp/rclcpp.hpp>
#include <image_transport/image_transport.hpp>
#include <cv_bridge/cv_bridge.hpp>
#include <sensor_msgs/image_encodings.hpp>
#include <sensor_msgs/msg/image.hpp>
#include <opencv2/imgproc/imgproc.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <opencv2/core/core.hpp>

using std::placeholders::_1;

class CameraEconomiqueNode : public rclcpp::Node
{
public:
  CameraEconomiqueNode()
  : Node("camera_economique_node")
  {
    // Publishers
    pub_rotated_1_ = this->create_publisher<sensor_msgs::msg::Image>("/output_image_topic", 10);
    pub_rotated_2_ = this->create_publisher<sensor_msgs::msg::Image>("/output_image_topic2", 10);
    pub_rotated_3_ = this->create_publisher<sensor_msgs::msg::Image>("/output_image_topic3", 10);
    pub_rotated_4_ = this->create_publisher<sensor_msgs::msg::Image>("/output_image_topic4", 10);

    // Subscribers
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
  void imageCb1(const sensor_msgs::msg::Image::SharedPtr msg)
  {
    process_and_publish(msg, pub_rotated_1_);
  }

  void imageCb2(const sensor_msgs::msg::Image::SharedPtr msg)
  {
    process_and_publish(msg, pub_rotated_2_);
  }

  void imageCb3(const sensor_msgs::msg::Image::SharedPtr msg)
  {
    process_and_publish(msg, pub_rotated_3_);
  }

  void imageCb4(const sensor_msgs::msg::Image::SharedPtr msg)
  {
    process_and_publish(msg, pub_rotated_4_);
  }

  void process_and_publish(const sensor_msgs::msg::Image::SharedPtr msg, rclcpp::Publisher<sensor_msgs::msg::Image>::SharedPtr pub)
  {
    cv_bridge::CvImagePtr cv_ptr;
    try
    {
      cv_ptr = cv_bridge::toCvCopy(msg, sensor_msgs::image_encodings::BGR8);
    }
    catch (cv_bridge::Exception& e)
    {
      RCLCPP_ERROR(this->get_logger(), "cv_bridge exception: %s", e.what());
      return;
    }

    cv::Mat rotated_image;
    cv::rotate(cv_ptr->image, rotated_image, cv::ROTATE_180);
    cv_ptr->image = rotated_image;

    pub->publish(*(cv_ptr->toImageMsg()));
  }

  rclcpp::Subscription<sensor_msgs::msg::Image>::SharedPtr sub_1_;
  rclcpp::Subscription<sensor_msgs::msg::Image>::SharedPtr sub_2_;
  rclcpp::Subscription<sensor_msgs::msg::Image>::SharedPtr sub_3_;
  rclcpp::Subscription<sensor_msgs::msg::Image>::SharedPtr sub_4_;

  rclcpp::Publisher<sensor_msgs::msg::Image>::SharedPtr pub_rotated_1_;
  rclcpp::Publisher<sensor_msgs::msg::Image>::SharedPtr pub_rotated_2_;
  rclcpp::Publisher<sensor_msgs::msg::Image>::SharedPtr pub_rotated_3_;
  rclcpp::Publisher<sensor_msgs::msg::Image>::SharedPtr pub_rotated_4_;
};

int main(int argc, char **argv)
{
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<CameraEconomiqueNode>());
  rclcpp::shutdown();
  return 0;
}
