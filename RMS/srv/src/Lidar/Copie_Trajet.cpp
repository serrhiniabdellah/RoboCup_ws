/*
Programme réalisé dans le cadre du projet RoboCup Rescue de MT5 de l'ISTY
Année 2024 — Migration ROS 2 Jazzy

Copie_Trajet : rejoue en temps réel les commandes manette enregistrées dans
commandes_manette.txt en respectant les délais originaux entre chaque commande.
*/

#include <rclcpp/rclcpp.hpp>
#include <sensor_msgs/msg/joy.hpp>
#include <nav_msgs/msg/path.hpp>
#include <geometry_msgs/msg/pose_stamped.hpp>
#include <geometry_msgs/msg/quaternion.hpp>
#include <tf2/LinearMath/Quaternion.hpp>
#include <tf2/LinearMath/Matrix3x3.hpp>
#include <tf2_geometry_msgs/tf2_geometry_msgs.hpp>

#include <fstream>
#include <iostream>
#include <sstream>
#include <vector>
#include <string>
#include <chrono>
#include <thread>

// Colonnes du fichier de commandes manette
static std::vector<std::string> col0, col1, col2, col3, col4, col5, col6,
                                  col7, col8, col9, col10, col11, col12,
                                  col13, col14, col15, col16, col17, col18;

void Copie_joy(rclcpp::Node::SharedPtr node)
{
    const char* dir_joy = "/home/ros/ros2_ws/src/RMS/commandes_manette";
    std::ifstream file_joy(std::string(dir_joy) + "/commandes_manette.txt");

    if (!file_joy.is_open()) {
        RCLCPP_ERROR(node->get_logger(), "Impossible d'ouvrir commandes_manette.txt");
        return;
    }

    std::string line;
    int idx = 0;
    float value1 = 0, value2 = 0;

    while (getline(file_joy, line)) {
        std::istringstream iss(line);
        std::string v0,v1,v2,v3,v4,v5,v6,v7,v8,v9,v10,v11,v12,v13,v14,v15,v16,v17,v18;
        if (iss >> v0 >> v1 >> v2 >> v3 >> v4 >> v5 >> v6 >> v7 >> v8 >> v9
               >> v10 >> v11 >> v12 >> v13 >> v14 >> v15 >> v16 >> v17 >> v18) {
            col0.push_back(v0);  col1.push_back(v1);  col2.push_back(v2);
            col3.push_back(v3);  col4.push_back(v4);  col5.push_back(v5);
            col6.push_back(v6);  col7.push_back(v7);  col8.push_back(v8);
            col9.push_back(v9);  col10.push_back(v10); col11.push_back(v11);
            col12.push_back(v12); col13.push_back(v13); col14.push_back(v14);
            col15.push_back(v15); col16.push_back(v16); col17.push_back(v17);
            col18.push_back(v18);

            // Affichage état flipper / robot
            if      (col14[idx] == "1")  std::cout << "Avancement Flipper"   << std::endl;
            else if (col14[idx] == "-1") std::cout << "Reculement Flipper"   << std::endl;
            else                         std::cout << "Pas de Mouvement Flipper" << std::endl;

            if      (col15[idx] == "1")  std::cout << "Avancement Robot"    << std::endl;
            else if (col15[idx] == "-1") std::cout << "Reculement Robot"    << std::endl;
            else                         std::cout << "Pas de Déplacement Robot" << std::endl;

            if      (col16[idx] == "1")  std::cout << "Rotation Gauche Robot" << std::endl;
            else if (col16[idx] == "-1") std::cout << "Rotation Droite Robot" << std::endl;
            else                         std::cout << "Pas de Rotation Robot"  << std::endl;

            // Respecter le délai entre commandes
            value1 = std::atof(col0[idx].c_str());
            value2 = (idx > 0) ? std::atof(col0[idx - 1].c_str()) : value1;
            float time_diff = value1 - value2;
            if (time_diff > 0)
                std::this_thread::sleep_for(
                    std::chrono::milliseconds(static_cast<int>(time_diff * 1000)));
            idx++;
        }
    }
    file_joy.close();
}

int main(int argc, char **argv)
{
    rclcpp::init(argc, argv);
    auto node = rclcpp::Node::make_shared("ROBOCUP2024_copie_trajet_node");
    RCLCPP_INFO(node->get_logger(), "Démarrage du rejeu de trajectoire...");
    Copie_joy(node);
    RCLCPP_INFO(node->get_logger(), "Rejeu terminé.");
    rclcpp::shutdown();
    return 0;
}
