#include <rclcpp/rclcpp.hpp>
#include <sensor_msgs/msg/image.hpp>
#include <cv_bridge/cv_bridge.hpp>
#include <opencv2/opencv.hpp>
#include <opencv2/objdetect.hpp>
#include <image_transport/image_transport.hpp>

class QRCodeDetectorNode : public rclcpp::Node
{
public:
  QRCodeDetectorNode()
  : Node("my_qr_code_detector")
  {
    sub_ = image_transport::create_subscription(this, "/cv_camera/image_raw",
      std::bind(&QRCodeDetectorNode::imageCallback, this, std::placeholders::_1),
      "raw", rmw_qos_profile_default);
      
    RCLCPP_INFO(this->get_logger(), "QRCodeDetectorNode has been started.");
  }

private:
  void imageCallback(const sensor_msgs::msg::Image::ConstSharedPtr msg)
  {
    try
    {
      cv_bridge::CvImagePtr cv_ptr = cv_bridge::toCvCopy(msg, "bgr8");
      cv::QRCodeDetector qrDecoder;

      std::string data;
      std::vector<cv::Point> points;
      if (qrDecoder.detect(cv_ptr->image, points))
      {
        data = qrDecoder.decode(cv_ptr->image, points);
        if (!data.empty())
        {
          RCLCPP_INFO(this->get_logger(), "QR Code Data: %s", data.c_str());
          for (size_t i = 0; i < points.size(); i++)
          {
            cv::line(cv_ptr->image, points[i], points[(i + 1) % points.size()], cv::Scalar(0, 0, 255), 2);
          }
        }
      }

      // Note: cv::imshow might not work well in headless Docker environments
      // cv::imshow("QR Code Detector", cv_ptr->image);
      // cv::waitKey(3);
    }
    catch (cv_bridge::Exception& e)
    {
      RCLCPP_ERROR(this->get_logger(), "cv_bridge exception: %s", e.what());
    }
  }

  image_transport::Subscriber sub_;
};

int main(int argc, char ** argv)
{
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<QRCodeDetectorNode>());
  rclcpp::shutdown();
  return 0;
}
