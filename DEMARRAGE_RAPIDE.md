# 🚀 DÉMARRAGE RAPIDE DU ROBOT - 3 ÉTAPES

## ✅ Prérequis (À FAIRE UNE SEULE FOIS)

```bash
# 1. Ajouter votre utilisateur au groupe Docker
sudo usermod -aG docker $USER

# 2. REDÉMARRER votre session
#    Déconnectez-vous et reconnectez-vous, ou redémarrez l'ordinateur

# 3. Vérifier que Docker fonctionne
docker ps
```

---

## 🎮 MÉTHODE 1 : Script automatique (LE PLUS SIMPLE) ⭐

```bash
cd ~/RoboCup_ws
./launch_robot.sh
```

**C'est tout !** Le script va :
- ✅ Démarrer Docker avec ROS1 Noetic
- ✅ Installer toutes les dépendances
- ✅ Vous proposer de lancer le robot automatiquement

---

## 🎮 MÉTHODE 2 : Lancement manuel

### Étape 1 : Démarrer le conteneur Docker

```bash
cd ~/RoboCup_ws

# Autoriser X11 pour affichage graphique
xhost +local:docker

# Lancer le conteneur
docker run -it --rm \
  --name robocup_ros1 \
  --network host \
  --privileged \
  -v /dev:/dev \
  -v "$PWD":/workspace \
  -e DISPLAY=$DISPLAY \
  -v /tmp/.X11-unix:/tmp/.X11-unix \
  ros:noetic-robot bash
```

### Étape 2 : Dans le conteneur, installer les dépendances (première fois)

```bash
apt-get update && apt-get install -y \
  ros-noetic-cv-bridge \
  ros-noetic-urg-node \
  ros-noetic-hector-slam \
  ros-noetic-hector-geotiff-launch \
  ros-noetic-rviz

source /opt/ros/noetic/setup.bash
```

### Étape 3 : Lancer le robot

#### Terminal 1 - Roscore
```bash
roscore
```

#### Terminal 2 - Robot (dans un nouveau terminal)
```bash
# Entrer dans le conteneur existant
docker exec -it robocup_ros1 bash

# Sourcer ROS
source /opt/ros/noetic/setup.bash

# Aller dans le bon répertoire
cd "/workspace/Robocup 2024/RaspBerry/Lidar_embarqué/ROBOCUP2024"

# Lancer le robot
roslaunch ROBOCUP2024 Rescue.launch
```

---

## 🔍 Vérifications

### 1. Docker est-il installé et actif ?

```bash
docker --version
docker ps
```

### 2. Le LIDAR est-il branché ?

```bash
ls -l /dev/ttyACM*
# Vous devriez voir /dev/ttyACM0
```

### 3. Les permissions sont-elles correctes ?

```bash
# Donner les permissions au LIDAR
sudo chmod 666 /dev/ttyACM0
```

---

## 📊 Ce qui va se lancer

Quand vous exécutez `roslaunch ROBOCUP2024 Rescue.launch`, cela démarre :

1. **urg_node** 🎯
   - Driver du LIDAR Hokuyo
   - Topic: `/scan`

2. **hector_mapping** 🗺️
   - SLAM (Cartographie et localisation)
   - Topic: `/map`

3. **hector_geotiff** 💾
   - Sauvegarde des cartes en format GeoTIFF

4. **rviz** 👁️
   - Visualisation 3D en temps réel
   - Vous verrez la carte se construire !

---

## 🎯 Tester que tout fonctionne

### Dans un terminal (dans le conteneur) :

```bash
# 1. Lister les topics actifs
rostopic list

# Vous devriez voir :
# /scan          <- Données LIDAR
# /map           <- Carte construite
# /tf            <- Transformations
# /odom          <- Odométrie

# 2. Voir les données du LIDAR en temps réel
rostopic echo /scan

# 3. Voir la fréquence de publication
rostopic hz /scan
# Devrait être environ 10-40 Hz

# 4. Visualiser le graphe des noeuds
rqt_graph
```

---

## ⚡ Commandes utiles

```bash
# Lister tous les noeuds actifs
rosnode list

# Information sur un noeud
rosnode info /hokuyo_node

# Tuer un noeud
rosnode kill /nom_du_noeud

# Sauvegarder la carte construite
rosrun map_server map_saver -f ma_carte

# Enregistrer toutes les données
rosbag record -a -O mon_test.bag

# Rejouer un enregistrement
rosbag play mon_test.bag
```

---

## 🆘 Dépannage

### ❌ "Cannot connect to X server"

```bash
# Sur Ubuntu (hors du conteneur)
xhost +local:docker
export DISPLAY=:0
```

### ❌ "Device /dev/ttyACM0 not found"

```bash
# Vérifier les ports série
ls -l /dev/tty*

# Le LIDAR peut être sur un autre port
# Modifiez le fichier launch :
# <param name="device_path" value="/dev/ttyUSB0"/>
```

### ❌ "Permission denied /dev/ttyACM0"

```bash
sudo chmod 666 /dev/ttyACM0
# Ou ajoutez-vous au groupe dialout
sudo usermod -aG dialout $USER
```

### ❌ "Package 'ROBOCUP2024' not found"

Le code n'est pas compilé. Dans ROS1, si le code est en C++, il faut le compiler :

```bash
cd "/workspace/Robocup 2024/RaspBerry/Fichiers catkin/robocup2024"
catkin_make
source devel/setup.bash
```

### ❌ "Docker: permission denied"

```bash
# Vérifier que vous êtes dans le groupe docker
groups | grep docker

# Si non, ajoutez-vous
sudo usermod -aG docker $USER

# PUIS REDÉMARREZ votre session !
```

---

## 📸 À quoi ça doit ressembler

Quand tout fonctionne, vous devriez voir :

### Terminal 1 (roscore)
```
[ INFO] [1234567890.123]: Started roscore...
```

### Terminal 2 (roslaunch)
```
[INFO] [1234567890.456]: Hokuyo LIDAR connected
[INFO] [1234567890.789]: hector_mapping started
[INFO] [1234567891.012]: Map size: 1024x1024
```

### RViz (fenêtre graphique)
- Une grille avec le robot au centre
- Des points rouges (données LIDAR)
- Une carte qui se construit en temps réel (murs, obstacles)

---

## 🎓 Pour aller plus loin

1. **Modifier les paramètres de navigation**
   - Fichier: `Robocup 2024/RaspBerry/Lidar_embarqué/ROBOCUP2024/launch/Rescue.launch`

2. **Comprendre le code C++**
   - Fichier: `Robocup 2024/RaspBerry/Lidar_embarqué/ROBOCUP2024/src/Exploration_Tom.cpp`

3. **Tester la caméra**
   - Décommenter les lignes cv_camera dans le launch file

4. **Ajouter des fonctionnalités**
   - Créer de nouveaux noeuds ROS
   - Publier/souscrire à de nouveaux topics

---

## 📞 Besoin d'aide ?

Consultez :
- `QUICK_START_GUIDE.md` - Guide complet du projet
- `DEMARRAGE_ROBOT_ROS1.md` - Détails sur Docker et ROS1
- `IMPORTANT_README.md` - Structure ROS1/ROS2

---

**🎉 Bon lancement ! Le robot devrait maintenant fonctionner avec ROS1 dans Docker.**
