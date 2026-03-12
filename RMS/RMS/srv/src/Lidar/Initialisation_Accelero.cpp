/*
Programme réalisé dans le cadre du projet RoboCup Rescue de MT5 de l'ISTY
Année 2024 — Migration ROS 2 Jazzy

Initialisation_Accelero : souscrit au topic /Pub_Accelero (geometry_msgs/Vector3)
et lit la rotation Z de l'accéléromètre en compensant l'offset initial.
*/

#include <rclcpp/rclcpp.hpp>
#include <geometry_msgs/msg/vector3.hpp>
#include <tf2_ros/transform_listener.h>
#include <tf2_ros/buffer.h>
#include <tf2_geometry_msgs/tf2_geometry_msgs.hpp>

#include <iostream>
#include <memory>

class InitAcceleroNode : public rclcpp::Node
{
public:
    InitAcceleroNode() : Node("ROBOCUP2024_Initialisation_Accelero_node")
    {
        sub_ = this->create_subscription<geometry_msgs::msg::Vector3>(
            "/Pub_Accelero", 1000,
            [this](const geometry_msgs::msg::Vector3::SharedPtr msg) {
                accCallback(msg);
            });
        RCLCPP_INFO(this->get_logger(), "Initialisation Accéléromètre démarrée.");
    }

private:
    rclcpp::Subscription<geometry_msgs::msg::Vector3>::SharedPtr sub_;
    std::shared_ptr<geometry_msgs::msg::Vector3> rotation_accelero_;
    bool   passage_accelero_ = false;
    double offset_Z_ = 0.0;

    void accCallback(const geometry_msgs::msg::Vector3::SharedPtr msg)
    {
        if (!rotation_accelero_)
            rotation_accelero_ = std::make_shared<geometry_msgs::msg::Vector3>();

        // Initialisation de l'offset au premier message
        if (!passage_accelero_) {
            offset_Z_ = msg->z;
            passage_accelero_ = true;
        }

        double adjusted_z = msg->z - offset_Z_;
        if      (adjusted_z >  180) adjusted_z -= 360;
        else if (adjusted_z < -180) adjusted_z += 360;

        rotation_accelero_->z = adjusted_z;

        std::cout << "ROTATION_ACCELERO EN Z : " << rotation_accelero_->z << std::endl;
    }
};

int main(int argc, char **argv)
{
    rclcpp::init(argc, argv);
    rclcpp::spin(std::make_shared<InitAcceleroNode>());
    rclcpp::shutdown();
    return 0;
}
