/*

Programme réalisé dans le cadre du projet RoboCup Rescue de MT5 de l'ISTY
Année 2024 — Migration ROS 2 Jazzy
Groupe de Marya Pastukhova, Tanguy Foret, Elian Dussart, Tom Roudaut,
Clément Cat, Baptiste Giraud, Angélique Da Costa, Aurélien Lelay.
Professeur encadrant : Pierre Blazevic, Olivier Snoeck

Commande pour lancer : ros2 launch rms_lidar Lidar.launch.py

*/

#include <rclcpp/rclcpp.hpp>
#include <sensor_msgs/msg/laser_scan.hpp>
#include <sensor_msgs/msg/imu.hpp>
#include <geometry_msgs/msg/vector3.hpp>
#include <nav_msgs/msg/path.hpp>
#include <geometry_msgs/msg/pose_stamped.hpp>
#include <geometry_msgs/msg/transform_stamped.hpp>
#include <tf2_msgs/msg/tf_message.hpp>
#include <tf2/LinearMath/Quaternion.hpp>
#include <tf2/LinearMath/Matrix3x3.hpp>
#include <tf2_geometry_msgs/tf2_geometry_msgs.hpp>
#include <tf2_ros/transform_listener.h>
#include <tf2_ros/buffer.h>

#include <fstream>
#include <iostream>
#include <sstream>
#include <vector>
#include <cmath>
#include <algorithm>
#include <unistd.h>
#include <sys/stat.h>

#define NUM_SCANS  1
#define NUM_VALUES 682

// ─── Structures ──────────────────────────────────────────────────────────────

struct Point_Espace {
    bool   Mur;
    int    Recompense;
    double X;
    double Y;
};

// ─── Globals ─────────────────────────────────────────────────────────────────

static int  compteur_effacement = 0;
static geometry_msgs::msg::Vector3 Com;
static geometry_msgs::msg::Vector3* p_Commande = &Com;
static int j_global = 0;
static int p_global = 0;
static const char* dir = "/home/ros/ros2_ws/src/RMS/trajectoire";
static std::ifstream trajectory_file;
static int  i_global = 0;
static int  changement_coord_fichier = 0;
static int  k_arr[6] = {0};
static double recuperation_x = 0;
static double recuperation_y = 0;
static double recuperation_qw = 0;
static double somme_x = 0;
static double somme_y = 0;
static double somme_qw = 0;
static int    compteur_for = 0;
static float  value2 = 0;
static float  value1 = 0;
static size_t q_global = 0;

static std::vector<std::string> col1, col2, col3, col4;
static std::string val1, val2, val3, val4;
static double (*pscan)[NUM_VALUES] = nullptr;
static bool*  position_atteignable = new bool;
static double sommage_point_dans_scan = 0;
static double somme_point_dans_scan = 0;
static double compteur_point_scan = 0.0;
static std::vector<Point_Espace> points;
static double rotation_Lidar_precedent = -180;
static double x_precedent = -9999999;
static int    wait_cnt = 0;
static bool   passage_scan = false;
static int    progression_avance = 0;
static int    progression_droite = 0;
static int    progression_gauche = 0;

// ─── Helper prototypes ────────────────────────────────────────────────────────

double Reward(double (*scan_data)[NUM_VALUES],
              double x, double y,
              double x_fichier, double y_fichier,
              double rotation_Lidar, double x_prec);

bool comparePoints(const Point_Espace& a, const Point_Espace& b);
bool Existence_Point(const std::vector<Point_Espace>& pts, double x, double y, double tolerance);
bool operator==(const Point_Espace& lhs, const Point_Espace& rhs);
int  calculerRecompense(double x, double y, double x_f, double y_f);
geometry_msgs::msg::Vector3 deplacement_vers_point(
        double x, double y, double x_f, double y_f,
        const Point_Espace& a, double rotation_Lidar);

// ─── Helper implementations ───────────────────────────────────────────────────

bool Existence_Point(const std::vector<Point_Espace>& pts, double x, double y, double tolerance)
{
    for (const auto& p : pts)
        if (std::abs(p.X - x) <= tolerance && std::abs(p.Y - y) <= tolerance)
            return true;
    return false;
}

bool comparePoints(const Point_Espace& a, const Point_Espace& b)
{
    if (a.X < b.X) return true;
    if (a.X > b.X) return false;
    return a.Y < b.Y;
}

bool operator==(const Point_Espace& lhs, const Point_Espace& rhs)
{
    return (lhs.X == rhs.X) && (lhs.Y == rhs.Y);
}

int calculerRecompense(double x, double y, double x_f, double y_f)
{
    double distance = std::sqrt((x - x_f)*(x - x_f) + (y - y_f)*(y - y_f));
    double proportion = 1.0 / (distance + 1);
    int recompense = static_cast<int>(proportion * 1000);
    return recompense * 1000000 / ((std::abs(x - x_f) + std::abs(y - y_f)) * 1000 + 1);
}

// ─── Nœud principal ───────────────────────────────────────────────────────────

class ExplorationPublisherNode : public rclcpp::Node
{
public:
    ExplorationPublisherNode() : Node("ROBOCUP2024_Exploration_Publisher_node")
    {
        start_time_ = this->now();

        // Ouvrir le fichier de trajectoire
        trajectory_file.open(std::string(dir) + "/trajectory_data.txt");

        chatter_pub_ = this->create_publisher<geometry_msgs::msg::Vector3>("chatter", 1000);

        scan_sub_ = this->create_subscription<sensor_msgs::msg::LaserScan>(
            "/scan", 1000,
            [this](const sensor_msgs::msg::LaserScan::SharedPtr msg) { scanCallback(msg); });

        tf_sub_ = this->create_subscription<tf2_msgs::msg::TFMessage>(
            "/tf", 1000,
            [this](const tf2_msgs::msg::TFMessage::SharedPtr msg) { tfCallback(msg); });

        timer_ = this->create_wall_timer(
            std::chrono::milliseconds(3),  // ~300 Hz
            [this]() {
                chatter_pub_->publish(Com);
            });
    }

private:
    rclcpp::Time start_time_;
    rclcpp::Publisher<geometry_msgs::msg::Vector3>::SharedPtr chatter_pub_;
    rclcpp::Subscription<sensor_msgs::msg::LaserScan>::SharedPtr scan_sub_;
    rclcpp::Subscription<tf2_msgs::msg::TFMessage>::SharedPtr tf_sub_;
    rclcpp::TimerBase::SharedPtr timer_;

    void scanCallback(const sensor_msgs::msg::LaserScan::SharedPtr scan)
    {
        std::vector<float> scan_data[NUM_SCANS];
        static double scan_data_recuperation[NUM_SCANS][NUM_VALUES]; // Changed to static to avoid dangling pointer

        for (int i = 0; i < NUM_SCANS; i++) {
            scan_data[i] = scan->ranges;
            for (int jj = 0; jj < NUM_VALUES; jj++) {
                scan_data_recuperation[i][jj] = (jj < (int)scan_data[i].size()) ? scan_data[i][jj] : 0.0;
                if (std::isnan(scan_data_recuperation[i][jj]))
                    scan_data_recuperation[i][jj] = 0;
            }
            pscan = scan_data_recuperation;
        }
        passage_scan = true;
    }

    void tfCallback(const tf2_msgs::msg::TFMessage::SharedPtr msg)
    {
        double x_fichier = 0, y_fichier = 0, Rotation_Lidar = 0;
        std::string line;

        // Lire le fichier trajectoire une seule fois
        if (p_global == 0) {
            while (getline(trajectory_file, line)) {
                std::istringstream iss(line);
                iss >> val1 >> val2 >> val3 >> val4;
                col1.push_back(val1);
                col2.push_back(val2);
                col3.push_back(val3);
                col4.push_back(val4);
            }
            trajectory_file.close();
            p_global++;
        }

        if (msg->transforms.empty()) return;
        const auto& transformStamped = msg->transforms[0];

        double x = transformStamped.transform.translation.x;
        double y = transformStamped.transform.translation.y * (-1);

        tf2::Quaternion q;
        tf2::convert(transformStamped.transform.rotation, q);
        double roll, pitch, yaw;
        tf2::Matrix3x3(q).getRPY(roll, pitch, yaw);
        double qw = q.w();
        double qx = roll;
        double qy = pitch;
        double qz = yaw;

        if (x != 0 && y != 0) {
            if (!col2.empty() && changement_coord_fichier < (int)col2.size()) {
                x_fichier = std::atof(col2[changement_coord_fichier].c_str());
                y_fichier = std::atof(col3[changement_coord_fichier].c_str());
            }
            double siny_cosp = 2 * (qw * qz + qx * qy);
            double cosy_cosp = 1 - 2 * (qy * qy + qz * qz);
            Rotation_Lidar = atan2(siny_cosp, cosy_cosp) * 180.0 / M_PI * (-1);

            if (pscan != nullptr)
                Reward(pscan, x, y, x_fichier, y_fichier, Rotation_Lidar, x_precedent);

            rotation_Lidar_precedent = Rotation_Lidar;

            std::sort(points.begin(), points.end(),
                      [](const Point_Espace& a, const Point_Espace& b) {
                          return a.Recompense > b.Recompense;
                      });

            if (pscan != nullptr) {
                for (const auto& pt : points) {
                    if (pt.Recompense >= 0) {
                        std::cout << "Point: X=" << pt.X << ", Y=" << pt.Y
                                  << ", Mur=" << pt.Mur
                                  << ", Recompense=" << pt.Recompense << std::endl;
                        *p_Commande = deplacement_vers_point(x, y, x_fichier, y_fichier, pt, Rotation_Lidar);
                    }
                    break;
                }
            }
            x_precedent = x;
        }
        passage_scan = false;
    }
};

// ─── Reward ───────────────────────────────────────────────────────────────────

double Reward(double (*scan_data)[NUM_VALUES],
              double x, double y,
              double x_fichier, double y_fichier,
              double rotation_Lidar, double x_prec)
{
    double calcul_x[NUM_SCANS][NUM_VALUES] = {0};
    double calcul_y[NUM_SCANS][NUM_VALUES] = {0};
    double angle_point_scan = 0.0;
    double angle_point_scan_rad = 0.0;
    Point_Espace pos;
    double rot_rad = 0.0;

    // Murs
    for (int i = 0; i < NUM_SCANS; i++) {
        for (int jj = 0; jj < NUM_VALUES; jj++) {
            if (jj != 0 && (pscan[i][jj] < pscan[i][jj-1] + 0.1)) {
                angle_point_scan = (jj <= NUM_VALUES/2)
                    ? ((NUM_VALUES/2) - jj) * 0.3519
                    : -(jj - (NUM_VALUES/2)) * 0.3519;
                rot_rad = rotation_Lidar * M_PI / 180.0;
                angle_point_scan_rad = angle_point_scan * M_PI / 180.0;
                calcul_x[i][jj] = std::round((pscan[i][jj]*std::cos(angle_point_scan_rad + rot_rad) + x)*10)/10;
                calcul_y[i][jj] = std::round((pscan[i][jj]*std::sin(angle_point_scan_rad + rot_rad) + y)*10)/10;
                pos.X = calcul_x[i][jj];
                pos.Y = calcul_y[i][jj];
                pos.Mur = true;
                pos.Recompense = -99999;
                points.push_back(pos);
            }
        }
    }

    // Points libres (entre le robot et les murs)
    for (int i = 0; i < NUM_SCANS; i++) {
        for (int jj = 0; jj < NUM_VALUES; jj++) {
            if (jj != 0 && pscan[i][jj] != 0 && (pscan[i][jj] < pscan[i][jj-1] + 0.1)) {
                double dist = 0.0;
                angle_point_scan = (jj <= NUM_VALUES/2)
                    ? ((NUM_VALUES/2) - jj) * 0.3519
                    : -(jj - (NUM_VALUES/2)) * 0.3519;
                rot_rad = rotation_Lidar * M_PI / 180.0;
                angle_point_scan_rad = angle_point_scan * M_PI / 180.0;

                while (dist < pscan[i][jj] - 0.5) {
                    calcul_x[i][jj] = std::round((dist*std::cos(angle_point_scan_rad+rot_rad)+x)*10)/10;
                    calcul_y[i][jj] = std::round((dist*std::sin(angle_point_scan_rad+rot_rad)+y)*10)/10;
                    dist += 0.1;
                    pos.X = calcul_x[i][jj];
                    pos.Y = calcul_y[i][jj];
                    if (!Existence_Point(points, pos.X, pos.Y, 0.0)) {
                        pos.Mur = false;
                        pos.Recompense = calculerRecompense(pos.X, pos.Y, x_fichier, y_fichier);
                        points.push_back(pos);
                    }
                }
            }
        }
    }

    std::sort(points.begin(), points.end(), comparePoints);
    points.erase(std::unique(points.begin(), points.end()), points.end());

    std::sort(points.begin(), points.end(),
              [](const Point_Espace& a, const Point_Espace& b){ return a.Recompense > b.Recompense; });

    for (auto& pt : points)
        if ((pt.X < x+1) && (pt.Y < y+1) && (pt.X > x-1) && (pt.Y > y-1))
            pt.Recompense /= 100;

    std::sort(points.begin(), points.end(),
              [](const Point_Espace& a, const Point_Espace& b){ return a.Recompense > b.Recompense; });

    std::cout << "x_fichier_trajectoire : " << x_fichier << std::endl;
    std::cout << "y_fichier_trajectoire : " << y_fichier << std::endl;
    return 0.0;
}

// ─── Déplacement vers point ───────────────────────────────────────────────────

geometry_msgs::msg::Vector3 deplacement_vers_point(
    double x, double y, double x_f, double y_f,
    const Point_Espace& a, double rotation_Lidar)
{
    geometry_msgs::msg::Vector3 Commande;
    int compteur_droite = 0, compteur_tout_droit = 0, compteur_gauche = 0;

    double angleToTarget = std::atan2(a.Y - y, a.X - x) * 180.0 / M_PI;
    double angleRelative = angleToTarget - rotation_Lidar;
    angleRelative = fmod(angleRelative + 360.0, 360.0);
    if (angleRelative > 180.0) angleRelative -= 360.0;

    double somme_verif = 0, somme_verif_gauche = 0, somme_verif_droite = 0;

    for (int i = 0; i < NUM_SCANS; i++) {
        for (int jj = 100; jj < 200; jj++)
            if (pscan[i][jj] != 0) { somme_verif_droite += pscan[i][jj]; compteur_droite++; }
        for (int jj = 281; jj < 381; jj++) {
            if (pscan[i][jj] != 0) { somme_verif += pscan[i][jj]; }
            else                   { somme_verif += 1; }
            compteur_tout_droit++;
        }
        for (int jj = 480; jj < 583; jj++)
            if (pscan[i][jj] != 0) { somme_verif_gauche += pscan[i][jj]; compteur_gauche++; }

        if (compteur_tout_droit > 0)  somme_verif        /= compteur_tout_droit;
        if (compteur_droite > 0)      somme_verif_droite /= compteur_droite;
        if (compteur_gauche > 0)      somme_verif_gauche /= compteur_gauche;
    }

    if (angleRelative < -5 && somme_verif_gauche > 0.7) {
        progression_gauche++;
        if (progression_gauche == 5) {
            std::cout << "Tourner à gauche" << std::endl;
            Commande.x = -1; Commande.y = 1;
            progression_avance = progression_droite = progression_gauche = 0;
        }
    } else if (somme_verif_droite > 0.7 && angleRelative > 5) {
        progression_droite++;
        if (progression_droite == 5) {
            std::cout << "Tourner à droite" << std::endl;
            Commande.x = 1; Commande.y = -1;
            progression_avance = progression_droite = progression_gauche = 0;
        }
    } else if (somme_verif >= 0.7) {
        progression_avance++;
        if (progression_avance == 5) {
            std::cout << "Avancer" << std::endl;
            Commande.x = 1; Commande.y = 1;
            progression_avance = progression_droite = progression_gauche = 0;
        }
    } else {
        std::cout << "Reculer" << std::endl;
        Commande.x = -1; Commande.y = -1;
    }

    // Sécurité proximité < 30 cm
    if ((pscan[0][341] > 0.05 && pscan[0][341] < 0.3) ||
        (pscan[0][208] > 0.05 && pscan[0][208] < 0.3) ||
        (pscan[0][464] > 0.05 && pscan[0][464] < 0.3)) {
        std::cout << "Endroit inférieur à 30cm" << std::endl;
        if (!((pscan[0][341] != 0 && pscan[0][341] < 0.3) && (Commande.x == -1 || Commande.y == -1)) &&
            !((pscan[0][208] != 0 && pscan[0][208] < 0.3) && Commande.x == -1) &&
            !((pscan[0][464] != 0 && pscan[0][464] < 0.3) && Commande.y == -1)) {
            Commande.x = -1; Commande.y = -1;
        }
    }

    if (std::abs(x - x_f) + std::abs(y - y_f) < 1) {
        std::cout << "Arrivé au point" << std::endl;
        points.clear();
        Commande.x = 0; Commande.y = 0;
        changement_coord_fichier++;
    }
    return Commande;
}

// ─── main ─────────────────────────────────────────────────────────────────────

int main(int argc, char **argv)
{
    rclcpp::init(argc, argv);
    rclcpp::spin(std::make_shared<ExplorationPublisherNode>());
    rclcpp::shutdown();
    return 0;
}
