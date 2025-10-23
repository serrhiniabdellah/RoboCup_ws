# 🤖 QUICK START GUIDE - RoboCup Rescue Robot

> Guide de démarrage rapide pour comprendre et utiliser le code du robot RoboCup Rescue
> 
> **Projet:** RoboCup Rescue MT5 ISTY - Année 2024
> 
> **Équipe:** Marya Pasukhova, Tanguy Foret, Elian Dussart, Tom Roudaut, Clément Cat, Baptiste Giraud, Angélique Da Costa, Aurélien Lelay
> 
> **Encadrants:** Pierre Blazevic, Olivier Snoeck

---

## 📋 Table des Matières

1. [Vue d'ensemble](#vue-densemble)
2. [Architecture du projet](#architecture-du-projet)
3. [Composants principaux](#composants-principaux)
4. [Installation rapide](#installation-rapide)
5. [Démarrage du robot](#démarrage-du-robot)
6. [Structure du code](#structure-du-code)
7. [Workflows de développement](#workflows-de-développement)
8. [Dépannage](#dépannage)

---

## 🎯 Vue d'ensemble

Ce projet est un **robot de sauvetage autonome** développé pour la compétition RoboCup Rescue. Le robot utilise **ROS1 Noetic** (Robot Operating System) et intègre plusieurs systèmes :

- **Navigation autonome** avec LIDAR Hokuyo
- **Vision par caméras** (8MP, RGBD, caméras économiques)
- **Bras robotique** avec servomoteurs Dynamixel AX-12
- **Contrôle de plateforme mobile** avec moteurs Sabertooth
- **IHM (Interface Homme-Machine)** pour le pilotage manuel

⚠️ **IMPORTANT** : Ce projet utilise **ROS1 Noetic**. Sur Ubuntu 22.04, utilisez **Docker** pour exécuter le code.

🚀 **DÉMARRAGE RAPIDE** : Consultez `DEMARRAGE_RAPIDE.md` pour lancer le robot en 3 étapes !

---

## 🏗️ Architecture du projet

```
RoboCup_ws/
├── src/                          # Code source ROS2 (actuellement vide)
├── Robocup 2024/                 # Répertoire principal du code
│   ├── RaspBerry/                # Code embarqué sur Raspberry Pi
│   │   ├── Lidar_embarqué/       # Code LIDAR + Navigation autonome ⭐
│   │   ├── RaspBerry_Bras/       # Contrôle du bras robotique
│   │   └── Fichiers catkin/      # Anciens packages ROS1
│   ├── PaysBas/                  # Code utilisé aux Pays-Bas (compétition)
│   │   └── Robocup2024_PaysBas/
│   │       └── src/              # Packages ROS principaux
│   │           ├── Bras_Manuel/
│   │           ├── IHM_Robot/
│   │           ├── Camera_Economique/
│   │           └── Accelerometre/
│   ├── Arduino/                  # Librairies Arduino (rosserial)
│   ├── Bras/                     # Projets liés au bras robotique
│   ├── Caméras de vision/        # Code des différentes caméras
│   ├── Capteurs de position/     # LIDAR, Accéléromètre, Caméra RGBD
│   ├── Manette & IHM/            # Interface de contrôle (Rosboard)
│   └── Mécanique et déplacement/ # CAO et code moteurs/codeurs
└── README.md                      # Documentation principale
```

### 📁 Répertoires clés

| Répertoire | Description | Technologies |
|-----------|-------------|--------------|
| `RaspBerry/Lidar_embarqué/ROBOCUP2024/src/` | **Code principal de navigation** | C++, ROS, OpenCV |
| `PaysBas/Robocup2024_PaysBas/src/` | **Code de compétition** | Python, C++, ROS |
| `RaspBerry/RaspBerry_Bras/Arduino/` | **Firmware Arduino du bras** | Arduino, Dynamixel |
| `Manette & IHM/IHM_Robot_RMS/rosboard/` | **Interface web de contrôle** | Python, ROS |

---

## 🔧 Composants principaux

### 1. **Navigation autonome** (Exploration)
📂 `RaspBerry/Lidar_embarqué/ROBOCUP2024/src/`

**Fichiers principaux:**
- `Exploration_Tom.cpp` - Programme principal d'exploration autonome
- `Rescue.cpp` - Mode rescue/sauvetage
- `odometrie_lidar.cpp` - Odométrie basée sur LIDAR
- `trajectoire/` - Génération et suivi de trajectoires

**Fonctionnalités:**
- Détection d'obstacles avec LIDAR
- Cartographie de l'environnement
- Navigation autonome avec évitement d'obstacles
- Génération de trajectoires optimales

### 2. **Contrôle du bras robotique**
📂 `RaspBerry/RaspBerry_Bras/Arduino/Bras_ROS_Mega/`

**Fichiers Arduino:**
- `Bras_ROS_Mega.ino` - Programme principal
- `Dynamixel.ino` - Communication avec servos Dynamixel AX-12
- `Fonctions.ino` - Fonctions utilitaires du bras

**Interfaces Python:**
- `slider.py` / `sliderbras2.py` - Interface graphique de contrôle manuel

### 3. **Système de vision**
📂 `Caméras de vision/`

**Types de caméras:**
- **Caméra 8MP** - Haute résolution pour détection de victimes
- **Caméra RGBD** (RealSense) - Perception 3D et profondeur
- **Caméra économique** - Vision secondaire

**Outils:**
- `bag2video.py` - Conversion des enregistrements ROS bags en vidéo

### 4. **Contrôle de la plateforme mobile**
📂 `Mécanique et déplacement de la plateforme/Sabertooth et moteurs/`

**Composants:**
- Contrôleur Sabertooth (moteurs DC)
- Encodeurs pour odométrie
- Communication série avec Arduino/Raspberry Pi

### 5. **IHM (Interface Homme-Machine)**
📂 `Manette & IHM/IHM_Robot_RMS/rosboard/`

**Interface web Rosboard:**
- Visualisation en temps réel des données
- Contrôle manuel du robot
- Monitoring des capteurs

---

## 🚀 Installation rapide

### Prérequis

- **OS:** Ubuntu 20.04 / 22.04
- **ROS:** **ROS Noetic (ROS1)** - Le code actuel utilise ROS1 !
  - ROS2 Humble est installé mais le code n'a pas encore été migré
- **Python:** 3.8+
- **Matériel:** Raspberry Pi 4, Arduino Mega, LIDAR, Caméras

⚠️ **Note importante** : Ce projet utilise actuellement **ROS1 Noetic**. Bien que ROS2 soit installé sur le système, le code dans `Robocup 2024/` n'a pas été migré vers ROS2.

### 1. Cloner le projet

```bash
git clone https://github.com/BenjaminPellieux/RoboCup_ws.git
cd RoboCup_ws
```

### 2. Installer les dépendances ROS

```bash
# Installer ROS1 Noetic (si pas déjà fait)
sudo apt-get update
sudo apt-get install -y ros-noetic-desktop-full

# Dépendances ROS1 pour le projet actuel
sudo apt-get install -y \
    ros-noetic-cv-bridge \
    ros-noetic-image-transport \
    ros-noetic-sensor-msgs \
    ros-noetic-nav-msgs \
    ros-noetic-geometry-msgs \
    ros-noetic-rviz \
    ros-noetic-rosserial \
    ros-noetic-rosserial-arduino \
    libopencv-dev \
    python3-opencv

# Dépendances ROS2 (déjà installées sur votre système)
sudo apt-get install -y \
    ros-humble-image-transport \
    ros-humble-cv-bridge \
    ros-humble-sensor-msgs \
    ros-humble-nav-msgs \
    ros-humble-geometry-msgs
```

### 3. Compiler le workspace

⚠️ **IMPORTANT** : Le code actuel est principalement en **ROS1** (pas ROS2). Le dossier `Robocup 2024/` contient des packages catkin (ROS1).

```bash
# Option A: Utiliser ROS2 (workspace vide pour l'instant)
cd /home/ser/RoboCup_ws
colcon build --symlink-install
source install/setup.bash

# Option B: Utiliser ROS1 pour le code existant
cd "Robocup 2024/RaspBerry/Fichiers catkin/robocup2024"
catkin_make
source devel/setup.bash
```

**Note :** Si vous obtenez des erreurs de paquets dupliqués avec colcon, c'est normal. Le code actuel n'est pas conçu pour ROS2. Utilisez plutôt ROS1 Noetic avec catkin.

### 4. Sourcer l'environnement ROS

```bash
# Pour ROS1 Noetic (code actuel du robot)
source /opt/ros/noetic/setup.bash
cd "Robocup 2024/RaspBerry/Fichiers catkin/robocup2024"
source devel/setup.bash

# Pour ROS2 Humble (développement futur)
source /opt/ros/humble/setup.bash
cd /home/ser/RoboCup_ws
source install/setup.bash
```

---

## 🎮 Démarrage du robot

### Mode 1: Navigation autonome (Exploration)

```bash
# Se placer dans le répertoire
cd "Robocup 2024/RaspBerry/Lidar_embarqué/ROBOCUP2024"

# Lancer le launch file (ROS1)
roslaunch ROBOCUP2024 Rescue.launch
```

**Ce qui est lancé:**
- Node de lecture LIDAR
- Node de traitement d'images
- Node de navigation autonome
- Node de contrôle moteurs

### Mode 2: Contrôle manuel avec IHM

```bash
# Lancer Rosboard (interface web)
cd "Robocup 2024/Manette & IHM/IHM_Robot_RMS/rosboard"
python3 -m rosboard

# Ouvrir dans navigateur: http://localhost:8888
```

### Mode 3: Contrôle du bras robotique

```bash
# Téléverser le code Arduino
# Fichier: RaspBerry/RaspBerry_Bras/Arduino/Bras_ROS_Mega/Bras_ROS_Mega.ino
# Utiliser Arduino IDE ou platformio

# Lancer l'interface de contrôle
cd "Robocup 2024/RaspBerry/RaspBerry_Bras/bras_robot/src"
python3 slider.py
```

### Mode 4: Caméras

```bash
# Caméra RealSense (RGBD)
ros2 launch realsense2_camera rs_launch.py

# Caméra 8MP
cd "Robocup 2024/Caméras de vision/Caméra 8Mpi/Code"
# Suivre les instructions du README local
```

---

## 📚 Structure du code

### Navigation autonome (C++)

**Fichier principal:** `Exploration_Tom.cpp`

```cpp
// Callbacks principales
void scanCallback(const sensor_msgs::LaserScan::ConstPtr& scan);
void trajectoryCallback(const nav_msgs::Path::ConstPtr& msg);

// Fonction de décision de déplacement
geometry_msgs::Vector3 deplacement_automatique(double (*scan_data)[NUM_VALUES]);
```

**Topics ROS utilisés:**
- `/scan` - Données LIDAR (input)
- `/camera/image_raw` - Image caméra (input)
- `/direction` - Commandes de mouvement (output)
- `/trajectory` - Trajectoire planifiée (output)

### Contrôle du bras (Arduino + Python)

**Arduino (`Bras_ROS_Mega.ino`):**
```cpp
// Communication avec servos Dynamixel
void setServoPosition(int id, int angle);
void readServoPosition(int id);

// Interface ROS
ros::Subscriber<...> sub("servo_angles", servoCallback);
```

**Python (`slider.py`):**
```python
# Interface graphique pour contrôle manuel
class SliderControl:
    def __init__(self):
        self.pub = rospy.Publisher('servo_angles', ...)
```

### Vision (Python + OpenCV)

**Traitement d'images:**
```python
import cv2
import cv_bridge
from sensor_msgs.msg import Image

def image_callback(msg):
    bridge = cv_bridge.CvBridge()
    cv_image = bridge.imgmsg_to_cv2(msg, "bgr8")
    # Traitement...
```

---

## 🔄 Workflows de développement

### Workflow 1: Tester la navigation

1. **Vérifier le LIDAR**
   ```bash
   rostopic echo /scan
   ```

2. **Lancer la navigation**
   ```bash
   roslaunch ROBOCUP2024 Rescue.launch
   ```

3. **Visualiser dans RViz**
   ```bash
   rviz
   # Ajouter /scan, /trajectory, /map
   ```

### Workflow 2: Développer pour le bras

1. **Modifier le code Arduino**
   - Éditer `Bras_ROS_Mega.ino`
   - Téléverser sur Arduino Mega

2. **Tester avec l'interface Python**
   ```bash
   python3 slider.py
   ```

3. **Intégrer avec ROS**
   ```bash
   rosrun rosserial_python serial_node.py /dev/ttyACM0
   ```

### Workflow 3: Enregistrer et rejouer des données

1. **Enregistrer un bag**
   ```bash
   rosbag record -a -O mon_test.bag
   ```

2. **Rejouer**
   ```bash
   rosbag play mon_test.bag
   ```

3. **Convertir en vidéo**
   ```bash
   python3 bag2video.py mon_test.bag
   ```

---

## 🛠️ Dépannage

### Problème: LIDAR non détecté

```bash
# Vérifier les permissions
sudo chmod 666 /dev/ttyUSB0

# Vérifier la connexion
ls -l /dev/ttyUSB*

# Tester la communication
sudo apt-get install cutecom
cutecom
```

### Problème: Arduino non reconnu

```bash
# Ajouter l'utilisateur au groupe dialout
sudo usermod -a -G dialout $USER
# Redémarrer la session

# Vérifier le port
ls -l /dev/ttyACM*
```

### Problème: Erreurs de compilation ROS

```bash
# Nettoyer et recompiler
rm -rf build/ install/ log/
colcon build --cmake-clean-cache
```

### Problème: Caméra RealSense non détectée

```bash
# Installer/réinstaller le SDK
sudo apt-get install ros-$ROS_DISTRO-realsense2-camera

# Vérifier la détection
realsense-viewer
```

### Problème: Rosserial ne se connecte pas

```bash
# Relancer roscore
roscore

# Vérifier le port série
ls -l /dev/ttyACM* /dev/ttyUSB*

# Lancer rosserial avec le bon port
rosrun rosserial_python serial_node.py /dev/ttyACM0 _baud:=57600
```

---

## 📖 Documentation complémentaire

### Fichiers de documentation

- `README.md` - Vue d'ensemble du projet
- `CONTRIBUTING.md` - Guide de contribution
- `CODE_OF_CONDUCT.md` - Code de conduite
- `LICENSE` - Licence MIT

### Ressources externes

- [ROS Documentation](https://docs.ros.org/)
- [OpenCV Documentation](https://docs.opencv.org/)
- [Dynamixel SDK](https://emanual.robotis.com/docs/en/software/dynamixel/dynamixel_sdk/)
- [Sabertooth Motor Controllers](https://www.dimensionengineering.com/datasheets/Sabertooth2x60.pdf)

### Contacts

- **GitHub:** https://github.com/BenjaminPellieux/RoboCup_ws
- **Email:** benjamin.pellieux@ens.uvsq.fr

---

## 🎓 Concepts clés à comprendre

### 1. ROS Topics et Messages
- **Topics** = canaux de communication
- **Messages** = structures de données
- **Publishers** = émetteurs
- **Subscribers** = récepteurs

### 2. Transformation de coordonnées (TF)
- Conversion entre repères du robot, LIDAR, caméras
- Crucial pour la navigation et la manipulation

### 3. Odométrie
- Estimation de la position du robot
- Fusion de données: encodeurs + LIDAR + IMU

### 4. SLAM (Simultaneous Localization and Mapping)
- Cartographie et localisation simultanées
- Base de la navigation autonome

### 5. Cinématique du bras
- Calcul des angles des servos
- Modèle URDF pour simulation

---

## ⚡ Commandes utiles

```bash
# Lister les topics ROS actifs
rostopic list

# Afficher les messages d'un topic
rostopic echo /scan

# Afficher la fréquence de publication
rostopic hz /camera/image_raw

# Visualiser le graphe des nodes
rqt_graph

# Monitorer les performances
rqt_top

# Sauvegarder une configuration
rosparam dump params.yaml

# Recharger une configuration
rosparam load params.yaml
```

---

## 🎯 Prochaines étapes

1. **Parcourir le code principal** dans `Exploration_Tom.cpp`
2. **Tester chaque composant** individuellement
3. **Comprendre les topics ROS** utilisés
4. **Modifier et expérimenter** avec les paramètres
5. **Contribuer** en suivant `CONTRIBUTING.md`

---

**Bon développement ! 🚀**

*Guide créé pour l'équipe RoboCup Rescue 2024 - ISTY MT5*
