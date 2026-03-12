/*
Programme réalisé dans le cadre du projet RoboCup Rescue de MT5 de l'ISTY
Année 2024 — Migration ROS 2 Jazzy

Exploration automatique intelligente — souscrit à /scan, décide de la direction
selon les sommes de distances gauche/centre/droite du LIDAR.
*/

#include <rclcpp/rclcpp.hpp>
#include <sensor_msgs/msg/laser_scan.hpp>
#include <geometry_msgs/msg/vector3.hpp>
#include <nav_msgs/msg/path.hpp>
#include <geometry_msgs/msg/pose_stamped.hpp>
#include <geometry_msgs/msg/quaternion.hpp>
#include <tf2/LinearMath/Quaternion.hpp>
#include <tf2/LinearMath/Matrix3x3.hpp>
#include <tf2_geometry_msgs/tf2_geometry_msgs.hpp>

#include <iostream>
#include <vector>
#include <cmath>
#include <fstream>
#include <sstream>

#define NUM_SCANS  1
#define NUM_VALUES 682

struct Point_Espace {
    bool   Cul_de_Sac;
    bool   Chemin;
    double X;
    double Y;
};

static double (*pscan)[NUM_VALUES] = nullptr;
static double* rotation_Lidar_ptr = nullptr;
static int     deblocage_gauche = 0;
static int     deblocage_droite = 0;
static Point_Espace Position_Points_dans_Espace;
static std::vector<Point_Espace> points;
static double* x_ptr = nullptr;
static double* y_ptr = nullptr;

// Prototype
bool Verification_Tourner_Droite();

bool Verification_Tourner_Droite()
{
    double Somme_droite = 0;
    int    compteur_boucle = 0;
    for (int i = 0; i < NUM_SCANS; i++) {
        for (int jj = 45; jj < 85; jj++) {
            if (pscan[i][jj] > 0.2) {
                Somme_droite += pscan[i][jj];
                compteur_boucle++;
            }
        }
        if (compteur_boucle > 0 && Somme_droite / compteur_boucle > 3.5)
            return true;
    }
    return false;
}

double deplacement_automatique(double (*scan_data)[NUM_VALUES])
{
    int somme_repere_distance_scan[NUM_SCANS][227] = {0};
    int compteur_somme = 0;

    for (int i = 0; i < NUM_SCANS; i++) {
        for (int jj = 1; jj < NUM_VALUES; jj++) {
            if (jj % 3 == 0) {
                compteur_somme++;
                somme_repere_distance_scan[i][compteur_somme] =
                    (int)(scan_data[i][jj] + scan_data[i][jj-1] + scan_data[i][jj-2]);
            }
        }
        compteur_somme = 0;
    }

    int somme_gauche = 0, somme_centre = 0, somme_droite = 0;
    for (int i = 0; i < NUM_SCANS; i++) {
        for (int jj = 0; jj < 227; jj++) {
            if      (jj < 75)              somme_droite  += somme_repere_distance_scan[i][jj];
            else if (jj >= 75 && jj < 151) somme_centre  += somme_repere_distance_scan[i][jj];
            else                           somme_gauche  += somme_repere_distance_scan[i][jj];
        }
    }

    std::cout << "somme_valeurs_gauche = " << somme_gauche << std::endl;
    std::cout << "somme_valeurs_centre = " << somme_centre << std::endl;
    std::cout << "somme_valeurs_droite = " << somme_droite << std::endl;

    bool diff_significant =
        (std::abs(somme_gauche - somme_droite) > 3000) &&
        (std::abs(somme_gauche - somme_centre) > 3000) &&
        (std::abs(somme_centre - somme_droite) > 3000);
    bool any_low = (somme_gauche < 20000 || somme_centre < 20000 || somme_droite < 20000);

    if (diff_significant || any_low) {
        if (somme_gauche > somme_centre && somme_gauche > somme_droite) {
            if (Verification_Tourner_Droite()) { std::cout << "Tourner à droite de 90°" << std::endl; deblocage_droite++; }
            else                               { std::cout << "Tourner à gauche"         << std::endl; deblocage_gauche++; }
        } else if (somme_centre > somme_gauche && somme_centre > somme_droite) {
            if (Verification_Tourner_Droite()) { std::cout << "Tourner à droite de 90°" << std::endl; deblocage_droite++; }
            else                               { std::cout << "Continuer tout droit" << std::endl; deblocage_droite = deblocage_gauche = 0; }
        } else {
            std::cout << "Tourner à droite" << std::endl;
            deblocage_droite++;
        }
        std::cout << "deblocage_droite : " << deblocage_droite << std::endl;
        std::cout << "deblocage_gauche : " << deblocage_gauche << std::endl;
        if (deblocage_droite != 0 && deblocage_gauche != 0 && std::abs(deblocage_gauche + deblocage_droite) > 4) {
            std::cout << "Tourner à droite de 180°" << std::endl;
            deblocage_droite = deblocage_gauche = 0;
        }
    } else {
        std::cout << "Tourner de 90° à droite (pour se décoincer)" << std::endl;
    }
    return 0.0;
}

class ExplorationAutoIntelligente : public rclcpp::Node
{
public:
    ExplorationAutoIntelligente() : Node("ROBOCUP2024_Exploration_automatique_intelligente_node")
    {
        start_time_ = this->now();
        scan_sub_ = this->create_subscription<sensor_msgs::msg::LaserScan>(
            "/scan", 1000,
            [this](const sensor_msgs::msg::LaserScan::SharedPtr msg) {
                double scan_data_recuperation[NUM_SCANS][NUM_VALUES] = {0};
                for (int i = 0; i < NUM_SCANS; i++) {
                    for (int jj = 0; jj < NUM_VALUES; jj++) {
                        scan_data_recuperation[i][jj] = (jj < (int)msg->ranges.size()) ? msg->ranges[jj] : 0.0;
                        if (std::isnan(scan_data_recuperation[i][jj]))
                            scan_data_recuperation[i][jj] = 0;
                    }
                }
                pscan = scan_data_recuperation;
                deplacement_automatique(scan_data_recuperation);
            });
    }
private:
    rclcpp::Time start_time_;
    rclcpp::Subscription<sensor_msgs::msg::LaserScan>::SharedPtr scan_sub_;
};

int main(int argc, char **argv)
{
    rclcpp::init(argc, argv);
    rclcpp::spin(std::make_shared<ExplorationAutoIntelligente>());
    rclcpp::shutdown();
    return 0;
}
