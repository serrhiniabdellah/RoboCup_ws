# Commandes pour le Projet Navigation & LIDAR (ROS 2 Jazzy)

Voici toutes les commandes nécessaires pour configurer, compiler et lancer ton projet dans le conteneur Docker.

## 1. Lancement du Docker
Depuis ton terminal habituel (dans `RoboCup_ws/`) :
```bash
docker run -it -v $(pwd)/RMS:/ros2_ws/src/RMS osrf/ros:jazzy-desktop bash
```

## 2. Configuration Initiale (Une seule fois dans le Docker)
Si tu n'as pas encore installé les dépendances :
```bash
apt update
apt install ros-jazzy-urg-node2 ros-jazzy-diagnostic-updater ros-jazzy-laser-proc
rosdep update
rosdep install --from-paths src --ignore-src -r -y
```

Si le driver LIDAR manque (source build) :
```bash
cd /ros2_ws/src/
git clone https://github.com/Hokuyo-aut/urg_node2.git
cd urg_node2
git submodule update --init --recursive
```

## 3. Compilation
```bash
cd /ros2_ws/
colcon build --packages-select urg_node2 rms_lidar
```

## 4. Lancement
```bash
source install/setup.bash
ros2 launch rms_lidar Lidar.launch.py
```

## 5. Test de Simulation (Sans le robot)
Dans un deuxième onglet de ton terminal habituel :
```bash
docker exec -it ros_robot bash
source /opt/ros/jazzy/setup.bash
# Simuler un obstacle à 0.5m
ros2 topic pub -1 /scan sensor_msgs/msg/LaserScan "{header: {frame_id: 'laser'}, angle_min: -1.57, angle_max: 1.57, angle_increment: 0.01, range_min: 0.0, range_max: 10.0, ranges: [0.5, 0.5, 0.5, 0.5, 0.5]}"
```
(Regarde alors le premier terminal pour voir la décision du robot).
