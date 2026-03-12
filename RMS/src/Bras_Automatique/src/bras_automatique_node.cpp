#include <rclcpp/rclcpp.hpp>
#include <image_transport/image_transport.hpp>
#include <cv_bridge/cv_bridge.hpp>
#include <sensor_msgs/image_encodings.hpp>
#include <opencv2/opencv.hpp>
#include <geometry_msgs/msg/vector3.hpp>
#include <std_msgs/msg/string.hpp>
#include <vector>
#include "bras_automatique/snpi5_V3.h"
#include "bras_automatique/Finder.h"
#include "rms_interfaces/srv/traitement_hsv.hpp"
#include "rms_interfaces/srv/pas.hpp"

using namespace std::placeholders;

class BrasAutomatiqueNode : public rclcpp::Node
{
public:
    BrasAutomatiqueNode() : Node("bras_automatique_node")
    {
        rmw_qos_profile_t custom_qos = rmw_qos_profile_default;
        
        image_transport::ImageTransport it(shared_from_this());
        
        // Publishers
        image_pub_ = it.advertise("/image_converter/output_obstacle", 1);
        image_pub2_ = it.advertise("/image_converter/traitement_bleu", 1);
        image_pub3_ = it.advertise("/image_converter/traitement_rouge", 1);
        image_pub4_ = it.advertise("/image_converter/traitement_ligne", 1);
        coo_blop_pub_ = this->create_publisher<geometry_msgs::msg::Vector3>("coo_blop_node", 10);

        // Subscriber
        image_sub_ = it.subscribe("/cv_camera/image_raw", 1, std::bind(&BrasAutomatiqueNode::imageCb, this, _1));

        // Services
        service_hsv_ = this->create_service<rms_interfaces::srv::TraitementHSV>(
            "traitement_hsv", std::bind(&BrasAutomatiqueNode::serv_Traitement_HSV, this, _1, _2));
        service_pas_ = this->create_service<rms_interfaces::srv::Pas>(
            "pas", std::bind(&BrasAutomatiqueNode::serv_Pas, this, _1, _2));

        L1 = 0.06f; L2 = 0.3f; L3 = 0.0f; L4 = 0.2f; L5 = 0.077f; L6 = 0.014f;
        
        readParam();
        
        timer_ = this->create_wall_timer(std::chrono::milliseconds(100), std::bind(&BrasAutomatiqueNode::on_timer, this));

        RCLCPP_INFO(this->get_logger(), "Bras Automatique Node started");
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

        // Logic from Clement_Ligne.cpp / Bras_Automatique.cpp here
        // ... (simplified for this step, but keeping the core structure)
        
        cv::Mat img_test, img_obstacle;
        img_test = Thresholded(cv_ptr, iLowH, iHighH, iLowS, iHighS, iLowV, iHighV, 1);
        img_obstacle = Thresholded(cv_ptr, iLowH_Obstacle, iHighH_Obstacle, iLowS_Obstacle, iHighS_Obstacle, iLowV_Obstacle, iHighV_Obstacle, 0);

        auto contour_rouge = Blopblop(img_obstacle, cv_ptr, 1, 255, 0, 0);
        auto contour_bleu = Blopblop(img_test, cv_ptr, 2, 0, 0, 255);

        // Co.x etc logic...
        
        image_pub4_.publish(cv_ptr->toImageMsg());
    }

    cv::Mat Thresholded(cv_bridge::CvImagePtr cv_ptr, int lH, int hH, int lS, int hS, int lV, int hV, int k)
    {
        cv::Mat imgHSV, imgThresholded;
        cv::cvtColor(cv_ptr->image, imgHSV, cv::COLOR_BGR2HSV);
        cv::inRange(imgHSV, cv::Scalar(lH, lS, lV), cv::Scalar(hH, hS, hV), imgThresholded);
        
        cv::erode(imgThresholded, imgThresholded, cv::getStructuringElement(cv::MORPH_ELLIPSE, cv::Size(5, 5)));
        cv::dilate(imgThresholded, imgThresholded, cv::getStructuringElement(cv::MORPH_ELLIPSE, cv::Size(5, 5)));
        
        auto img_msg = cv_bridge::CvImage(std_msgs::msg::Header(), "mono8", imgThresholded).toImageMsg();
        if (k == 1) image_pub2_.publish(img_msg);
        else image_pub3_.publish(img_msg);
        
        return imgThresholded;
    }

    std::vector<std::vector<cv::Point>> Blopblop(cv::Mat imgMono, cv_bridge::CvImagePtr cv_ptr, int, int r, int g, int b)
    {
        std::vector<std::vector<cv::Point>> contours;
        std::vector<cv::Vec4i> hierarchy;
        cv::findContours(imgMono, contours, hierarchy, cv::RETR_TREE, cv::CHAIN_APPROX_NONE);
        cv::drawContours(cv_ptr->image, contours, -1, cv::Scalar(b, g, r), 2);
        image_pub_.publish(cv_ptr->toImageMsg());
        return contours;
    }

    bool serv_Traitement_HSV(const std::shared_ptr<rms_interfaces::srv::TraitementHSV::Request> req,
                            std::shared_ptr<rms_interfaces::srv::TraitementHSV::Response> res)
    {
        iLowH = req->low_h; iHighH = req->high_h;
        iLowS = req->low_s; iHighS = req->high_s;
        iLowV = req->low_v; iHighV = req->high_v;
        RCLCPP_INFO(this->get_logger(), "HSV thresholds updated via service");
        return true;
    }

    bool serv_Pas(const std::shared_ptr<rms_interfaces::srv::Pas::Request> req,
                 std::shared_ptr<rms_interfaces::srv::Pas::Response> res)
    {
        if (req->tolerance < 1) {
            RCLCPP_WARN(this->get_logger(), "Tolerance must be >= 1");
        } else {
            co_msg_.z = req->tolerance;
            RCLCPP_INFO(this->get_logger(), "Tolerance set to %ld", req->tolerance);
        }
        return true;
    }

    void on_timer()
    {
        coo_blop_pub_->publish(co_msg_);
    }

    image_transport::Publisher image_pub_, image_pub2_, image_pub3_, image_pub4_;
    image_transport::Subscriber image_sub_;
    rclcpp::Publisher<geometry_msgs::msg::Vector3>::SharedPtr coo_blop_pub_;
    rclcpp::Service<rms_interfaces::srv::TraitementHSV>::SharedPtr service_hsv_;
    rclcpp::Service<rms_interfaces::srv::Pas>::SharedPtr service_pas_;
    rclcpp::TimerBase::SharedPtr timer_;
    
    geometry_msgs::msg::Vector3 co_msg_;
    float L1, L2, L3, L4, L5, L6;
    int iLowH = 0, iHighH = 179, iLowS = 0, iHighS = 255, iLowV = 0, iHighV = 255;
    int iLowH_Obstacle = 0, iHighH_Obstacle = 179, iLowS_Obstacle = 0, iHighS_Obstacle = 255, iLowV_Obstacle = 0, iHighV_Obstacle = 255;
};

int main(int argc, char ** argv)
{
    rclcpp::init(argc, argv);
    auto node = std::make_shared<BrasAutomatiqueNode>();
    rclcpp::spin(node);
    rclcpp::shutdown();
    return 0;
}
