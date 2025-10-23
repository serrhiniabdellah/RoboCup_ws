# 🚀 GUIDE DE DÉMARRAGE ROBOT - ROS1 sur Ubuntu 22.04

## ⚠️ Problème identifié

Votre système Ubuntu 22.04 n'a **pas de support officiel pour ROS1 Noetic** (qui nécessite Ubuntu 20.04).

## 🎯 Solutions possibles

### Solution 1 : Utiliser un container Docker avec ROS1 (RECOMMANDÉ) ⭐

C'est la meilleure solution pour exécuter ROS1 Noetic sur Ubuntu 22.04.

#### Installation Docker (si pas déjà fait)

```bash
# Docker est déjà installé sur votre système
docker --version
```

#### Créer un conteneur ROS1 Noetic

```bash
# 1. Télécharger l'image ROS1 Noetic
docker pull ros:noetic-robot

# 2. Lancer un conteneur avec accès au code
docker run -it --rm \
  --name robocup_ros1 \
  --network host \
  --privileged \
  -v /dev:/dev \
  -v /home/ser/RoboCup_ws:/workspace \
  -e DISPLAY=$DISPLAY \
  -v /tmp/.X11-unix:/tmp/.X11-unix \
  ros:noetic-robot \
  bash

# 3. Dans le conteneur, installer les dépendances
apt-get update
apt-get install -y \
    ros-noetic-cv-bridge \
    ros-noetic-image-transport \
    ros-noetic-urg-node \
    ros-noetic-hector-slam \
    ros-noetic-hector-geotiff \
    ros-noetic-rviz \
    libopencv-dev \
    python3-opencv

# 4. Sourcer ROS1
source /opt/ros/noetic/setup.bash

# 5. Aller dans le workspace
cd /workspace/"Robocup 2024/RaspBerry/Lidar_embarqué/ROBOCUP2024"

# 6. Lancer roscore dans un terminal
roscore

# 7. Dans un autre terminal Docker, lancer le robot
roslaunch ROBOCUP2024 Rescue.launch
```

---

### Solution 2 : Machine virtuelle Ubuntu 20.04

Installer Ubuntu 20.04 dans VirtualBox ou VMware avec ROS1 Noetic.

---

### Solution 3 : Dual boot Ubuntu 20.04

Installer Ubuntu 20.04 en dual boot pour avoir ROS1 nativement.

---

### Solution 4 : Compiler ROS1 depuis les sources (AVANCÉ)

Plus complexe et peut causer des problèmes de compatibilité.

---

## 🐳 Script Docker automatisé (SOLUTION LA PLUS SIMPLE)

Créez un fichier `start_robot_ros1.sh` :

```bash
#!/bin/bash

# Permettre l'affichage X11 depuis Docker
xhost +local:docker

# Lancer le conteneur ROS1
docker run -it --rm \
  --name robocup_ros1 \
  --network host \
  --privileged \
  -v /dev:/dev \
  -v "$(pwd)":/workspace \
  -e DISPLAY=$DISPLAY \
  -v /tmp/.X11-unix:/tmp/.X11-unix \
  -w /workspace \
  ros:noetic-robot \
  bash -c "
    # Installation des dépendances
    apt-get update && apt-get install -y \
      ros-noetic-cv-bridge \
      ros-noetic-image-transport \
      ros-noetic-urg-node \
      ros-noetic-hector-slam \
      ros-noetic-hector-geotiff \
      ros-noetic-hector-geotiff-launch \
      ros-noetic-rviz \
      libopencv-dev \
      python3-opencv \
      && source /opt/ros/noetic/setup.bash \
      && bash
  "
```

Rendez-le exécutable et lancez-le :

```bash
chmod +x start_robot_ros1.sh
./start_robot_ros1.sh
```

---

## 📝 Commandes dans le conteneur Docker

Une fois dans le conteneur :

```bash
# 1. Sourcer ROS1
source /opt/ros/noetic/setup.bash

# 2. Vérifier que ROS fonctionne
roscore &
sleep 3
rostopic list

# 3. Lancer le robot (assurez-vous que le LIDAR est branché)
cd /workspace/"Robocup 2024/RaspBerry/Lidar_embarqué/ROBOCUP2024"
roslaunch ROBOCUP2024 Rescue.launch
```

---

## 🔧 Vérifications avant de lancer

### 1. Vérifier le LIDAR

```bash
# Le LIDAR doit être sur /dev/ttyACM0
ls -l /dev/ttyACM*

# Si besoin, donner les permissions
sudo chmod 666 /dev/ttyACM0
```

### 2. Vérifier la caméra (si utilisée)

```bash
ls -l /dev/video*
```

### 3. Tester la connexion matérielle

```bash
# Dans le conteneur Docker
roscore &
sleep 2
rosrun urg_node urg_node _device_path:=/dev/ttyACM0

# Dans un autre terminal
rostopic echo /scan
```

---

## 🎮 Lancement complet du robot

### Terminal 1 : Roscore

```bash
docker exec -it robocup_ros1 bash
source /opt/ros/noetic/setup.bash
roscore
```

### Terminal 2 : LIDAR + Navigation

```bash
docker exec -it robocup_ros1 bash
source /opt/ros/noetic/setup.bash
cd /workspace/"Robocup 2024/RaspBerry/Lidar_embarqué/ROBOCUP2024"
roslaunch ROBOCUP2024 Rescue.launch
```

### Terminal 3 : Monitoring (optionnel)

```bash
docker exec -it robocup_ros1 bash
source /opt/ros/noetic/setup.bash

# Voir les topics actifs
rostopic list

# Voir les données du LIDAR
rostopic echo /scan

# Lancer RViz pour visualisation
rviz
```

---

## 🎯 Ce qui sera lancé par Rescue.launch

D'après le fichier de lancement :

1. **urg_node** - Driver du LIDAR Hokuyo
2. **hector_mapping** - SLAM (cartographie)
3. **hector_geotiff** - Export des cartes en GeoTIFF
4. **rviz** - Visualisation 3D

---

## 🆘 Dépannage Docker

### Problème : "Cannot connect to X server"

```bash
# Sur l'hôte Ubuntu
xhost +local:docker
export DISPLAY=:0
```

### Problème : "Device /dev/ttyACM0 not found"

```bash
# Vérifier que le LIDAR est branché
ls -l /dev/ttyACM*

# Redémarrer le conteneur avec les bonnes permissions
docker run -it --rm --privileged -v /dev:/dev ...
```

### Problème : "Package 'hector_slam' not found"

```bash
# Dans le conteneur, installer manuellement
apt-get update
apt-get install -y ros-noetic-hector-slam ros-noetic-hector-geotiff-launch
```

---

## 📊 Architecture du système

```
Ubuntu 22.04 (Hôte)
    │
    └─── Docker Container (ROS1 Noetic)
            │
            ├─── roscore
            ├─── urg_node (LIDAR)
            ├─── hector_mapping (SLAM)
            └─── rviz (Visualisation)
```

---

## 🚀 Alternative : Script tout-en-un

Créez `launch_robot.sh` :

```bash
#!/bin/bash

echo "🤖 Démarrage du robot RoboCup en ROS1..."

# Vérifier Docker
if ! command -v docker &> /dev/null; then
    echo "❌ Docker n'est pas installé"
    exit 1
fi

# Autoriser X11
xhost +local:docker 2>/dev/null

# Vérifier le LIDAR
if [ ! -e /dev/ttyACM0 ]; then
    echo "⚠️  ATTENTION : LIDAR non détecté sur /dev/ttyACM0"
    echo "   Vérifiez que le LIDAR est branché"
fi

# Lancer Docker
echo "📦 Démarrage du conteneur ROS1..."
docker run -it --rm \
  --name robocup_ros1 \
  --network host \
  --privileged \
  -v /dev:/dev \
  -v "$PWD":/workspace \
  -e DISPLAY=$DISPLAY \
  -v /tmp/.X11-unix:/tmp/.X11-unix \
  -w /workspace \
  ros:noetic-robot \
  bash -c '
    echo "📥 Installation des dépendances ROS1..."
    apt-get update -qq && apt-get install -y -qq \
      ros-noetic-cv-bridge \
      ros-noetic-image-transport \
      ros-noetic-urg-node \
      ros-noetic-hector-slam \
      ros-noetic-hector-geotiff-launch \
      ros-noetic-rviz > /dev/null 2>&1
    
    source /opt/ros/noetic/setup.bash
    
    echo "✅ ROS1 Noetic prêt !"
    echo ""
    echo "🎮 Commandes disponibles :"
    echo "  - roslaunch ROBOCUP2024 Rescue.launch  (lancer le robot)"
    echo "  - rostopic list                         (voir les topics)"
    echo "  - rviz                                  (visualisation)"
    echo ""
    
    cd "/workspace/Robocup 2024/RaspBerry/Lidar_embarqué/ROBOCUP2024"
    bash
  '
```

Usage :

```bash
chmod +x launch_robot.sh
./launch_robot.sh
```

---

**🎉 Avec cette solution Docker, vous pourrez exécuter votre robot ROS1 sur Ubuntu 22.04 !**
