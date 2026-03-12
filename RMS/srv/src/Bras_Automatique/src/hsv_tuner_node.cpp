#include <rclcpp/rclcpp.hpp>
#include <image_transport/image_transport.hpp>
#include <cv_bridge/cv_bridge.hpp>
#include <sensor_msgs/image_encodings.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <opencv2/imgproc/imgproc.hpp>
#include <fstream>
#include "bras_automatique/snpi5_V3.h"

class HSVTunerNode : public rclcpp::Node
{
public:
    HSVTunerNode() : Node("hsv_tuner_node")
    {
        image_transport::ImageTransport it(shared_from_this());
        image_sub_ = it.subscribe("/cv_camera/image_raw", 1, std::bind(&HSVTunerNode::imageCb, this, std::placeholders::_1));
        
        cv::namedWindow("Control", cv::WINDOW_AUTOSIZE);
        cv::createTrackbar("LowH", "Control", &iLowH, 255);
        cv::createTrackbar("HighH", "Control", &iHighH, 255);
        cv::createTrackbar("LowS", "Control", &iLowS, 255);
        cv::createTrackbar("HighS", "Control", &iHighS, 255);
        cv::createTrackbar("LowV", "Control", &iLowV, 255);
        cv::createTrackbar("HighV", "Control", &iHighV, 255);
        
        RCLCPP_INFO(this->get_logger(), "HSV Tuner Node started. Use 'Control' window to adjust thresholds.");
    }

private:
    void imageCb(const sensor_msgs::msg::Image::ConstSharedPtr& msg)
    {
        cv_bridge::CvImagePtr cv_ptr;
        try {
            cv_ptr = cv_bridge::toCvCopy(msg, sensor_msgs::image_encodings::BGR8);
        } catch (cv_bridge::Exception& e) {
            RCLCPP_ERROR(this->get_logger(), "cv_bridge exception: %s", e.what());
            return;
        }

        cv::Mat imgHSV, imgThresholded;
        cv::cvtColor(cv_ptr->image, imgHSV, cv::COLOR_BGR2HSV);
        cv::inRange(imgHSV, cv::Scalar(iLowH, iLowS, iLowV), cv::Scalar(iHighH, iHighS, iHighV), imgThresholded);
        
        cv::imshow("Original", cv_ptr->image);
        cv::imshow("Thresholded", imgThresholded);
        cv::waitKey(1);
    }

    image_transport::Subscriber image_sub_;
    int iLowH = 0, iHighH = 179, iLowS = 0, iHighS = 255, iLowV = 0, iHighV = 255;
};

int main(int argc, char ** argv)
{
    rclcpp::init(argc, argv);
    auto node = std::make_shared<HSVTunerNode>();
    rclcpp::spin(node);
    rclcpp::shutdown();
    return 0;
}
