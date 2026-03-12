/*
Programme réalisé dans le cadre du projet RoboCup Rescue de MT5 de l'ISTY
Année 2024 — Migration ROS 2 Jazzy

recuperation_data_auto : enregistre les commandes manette (/joy) dans un fichier .txt
avec horodatage pour pouvoir les rejouer ensuite.
*/

#include <rclcpp/rclcpp.hpp>
#include <sensor_msgs/msg/joy.hpp>
#include <sensor_msgs/msg/laser_scan.hpp>
#include <nav_msgs/msg/path.hpp>
#include <geometry_msgs/msg/pose_stamped.hpp>
#include <geometry_msgs/msg/quaternion.hpp>
#include <tf2/LinearMath/Quaternion.hpp>
#include <tf2/LinearMath/Matrix3x3.hpp>
#include <tf2_geometry_msgs/tf2_geometry_msgs.hpp>

#include <fstream>
#include <iostream>
#include <sstream>
#include <cmath>
#include <unistd.h>
#include <sys/stat.h>

#define NUM_SCANS  1
#define NUM_VALUES 682

class RecuperationDataAuto : public rclcpp::Node
{
public:
    RecuperationDataAuto() : Node("ROBOCUP2024_recuperation_data_auto_node")
    {
        start_time_ = this->now();

        // Créer le dossier des commandes manette si inexistant
        const char* dir_joy = "/home/ros/ros2_ws/src/RMS/commandes_manette";
        if (access(dir_joy, F_OK) == -1)
            mkdir(dir_joy, S_IRWXU | S_IRWXG | S_IROTH | S_IXOTH);

        outfile_joy_.open(std::string(dir_joy) + "/commandes_manette.txt",
                          std::ios::out | std::ios::app);
        if (!outfile_joy_.is_open())
            RCLCPP_ERROR(this->get_logger(), "Impossible d'ouvrir le fichier commandes_manette.txt");

        joy_sub_ = this->create_subscription<sensor_msgs::msg::Joy>(
            "/joy", 10,
            [this](const sensor_msgs::msg::Joy::SharedPtr joy) { last_joy_ = joy; });

        // Timer à 20 Hz pour loguer les commandes manette
        timer_ = this->create_wall_timer(
            std::chrono::milliseconds(50),
            [this]() {
                if (!last_joy_) return;

                rclcpp::Duration elapsed = this->now() - start_time_;
                outfile_joy_ << elapsed.seconds() << " ";

                for (size_t i = 0; i < last_joy_->buttons.size(); i++)
                    outfile_joy_ << last_joy_->buttons[i] << " ";
                for (size_t i = 0; i < last_joy_->axes.size(); i++)
                    outfile_joy_ << last_joy_->axes[i] << " ";
                outfile_joy_ << std::endl;

                RCLCPP_INFO_STREAM(this->get_logger(),
                    "t=" << elapsed.seconds() << "s — manette enregistrée");
            });
    }

    ~RecuperationDataAuto()
    {
        if (outfile_joy_.is_open()) outfile_joy_.close();
    }

private:
    rclcpp::Time   start_time_;
    std::ofstream  outfile_joy_;
    sensor_msgs::msg::Joy::SharedPtr last_joy_;
    rclcpp::Subscription<sensor_msgs::msg::Joy>::SharedPtr joy_sub_;
    rclcpp::TimerBase::SharedPtr timer_;
};

int main(int argc, char **argv)
{
    rclcpp::init(argc, argv);
    rclcpp::spin(std::make_shared<RecuperationDataAuto>());
    rclcpp::shutdown();
    return 0;
}
