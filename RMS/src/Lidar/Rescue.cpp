/*
Programme réalisé dans le cadre du projet RoboCup Rescue de MT5 de l'ISTY
Année 2024 — Migration ROS 2 Jazzy

Rescue : souscrit au flux caméra /cv_camera/image_raw et sauvegarde les images
en JPEG dans un dossier horodaté.
*/

#include <rclcpp/rclcpp.hpp>
#include <image_transport/image_transport.hpp>
#include <cv_bridge/cv_bridge.hpp>
#include <sensor_msgs/msg/image.hpp>
#include <sensor_msgs/image_encodings.hpp>
#include <sensor_msgs/msg/joy.hpp>

#include <opencv2/imgproc/imgproc.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <opencv2/imgcodecs.hpp>

#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <unistd.h>
#include <sys/stat.h>

static int photo_index = 1;

class RescueNode : public rclcpp::Node
{
public:
    RescueNode() : Node("ROBOCUP2024_node")
    {
        // Créer le dossier images si inexistant
        const char* dir = "/home/ros/ros2_ws/src/RMS/images";
        if (access(dir, F_OK) == -1)
            mkdir(dir, S_IRWXU | S_IRWXG | S_IROTH | S_IXOTH);
        images_dir_ = std::string(dir);

        image_transport::ImageTransport it(shared_from_this());
        image_sub_ = it.subscribe(
            "/cv_camera/image_raw", 1,
            [this](const sensor_msgs::msg::Image::ConstSharedPtr& msg) {
                imageCb(msg);
            });

        RCLCPP_INFO(this->get_logger(), "Nœud Rescue démarré — enregistrement des images dans %s", images_dir_.c_str());
    }

private:
    image_transport::Subscriber     image_sub_;
    std::string images_dir_;

    void imageCb(const sensor_msgs::msg::Image::ConstSharedPtr& msg)
    {
        cv_bridge::CvImagePtr cv_ptr;
        try {
            cv_ptr = cv_bridge::toCvCopy(msg, sensor_msgs::image_encodings::BGR8);
        } catch (const cv_bridge::Exception& e) {
            RCLCPP_ERROR(this->get_logger(), "cv_bridge exception: %s", e.what());
            return;
        }

        // Sauvegarde de l'image
        if (photo_index < 10000000) {
            std::string filepath = images_dir_ + "/captured_image" +
                                   std::to_string(photo_index) + ".jpg";
            if (access(filepath.c_str(), F_OK) != -1) {
                photo_index++;
            } else {
                std::cout << filepath << std::endl;
                cv::imwrite(filepath, cv_ptr->image);
            }
        }
    }
};

int main(int argc, char **argv)
{
    rclcpp::init(argc, argv);
    rclcpp::spin(std::make_shared<RescueNode>());
    rclcpp::shutdown();
    return 0;
}
