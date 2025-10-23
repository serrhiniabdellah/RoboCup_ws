# 🤖 RÔLES DE ROS ET ARDUINO DANS LE PROJET ROBOCUP

## 🎯 Vue d'ensemble de l'architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    ORDINATEUR / RASPBERRY PI                 │
│                                                              │
│  ┌────────────────────────────────────────────────────┐    │
│  │              ROS (Robot Operating System)          │    │
│  │                                                     │    │
│  │  • Navigation autonome                             │    │
│  │  • Cartographie (SLAM)                             │    │
│  │  • Traitement d'images                             │    │
│  │  • Planification de trajectoire                    │    │
│  │  • Coordination générale                           │    │
│  │  • Interface utilisateur                           │    │
│  └────────────────────────────────────────────────────┘    │
│                          ↕                                   │
│              Communication USB/Série                         │
└─────────────────────────────────────────────────────────────┘
                          ↕
┌─────────────────────────────────────────────────────────────┐
│                      ARDUINO MEGA                            │
│                                                              │
│  ┌────────────────────────────────────────────────────┐    │
│  │         Contrôle Temps Réel Bas Niveau             │    │
│  │                                                     │    │
│  │  • Contrôle des servomoteurs Dynamixel (Bras)     │    │
│  │  • Lecture des capteurs                            │    │
│  │  • Génération de PWM                               │    │
│  │  • Sécurité temps réel                             │    │
│  └────────────────────────────────────────────────────┘    │
│                          ↕                                   │
│              Protocole Dynamixel / PWM / GPIO                │
└─────────────────────────────────────────────────────────────┘
                          ↕
┌─────────────────────────────────────────────────────────────┐
│                   ACTIONNEURS PHYSIQUES                      │
│                                                              │
│  • Servos Dynamixel AX-12 (Bras robotique)                 │
│  • Moteurs DC (Roues - via Sabertooth)                     │
│  • LED, Buzzer, etc.                                        │
└─────────────────────────────────────────────────────────────┘
```

---

## 🖥️ RÔLE DE ROS (Robot Operating System)

### 📌 Qu'est-ce que ROS ?

**ROS** est un **framework logiciel** qui s'exécute sur l'ordinateur principal (PC ou Raspberry Pi).

### 🎯 Responsabilités principales

#### 1️⃣ **Cerveau du robot** - Décisions de haut niveau
```
ROS décide :
├── Où aller ?           → Planification de trajectoire
├── Comment éviter ?     → Navigation autonome
├── Que voir ?           → Traitement d'images
└── Quoi faire ?         → Coordination des tâches
```

#### 2️⃣ **Intégration de tous les composants**

ROS connecte et fait communiquer :

| Composant | Package ROS | Topic/Service |
|-----------|-------------|---------------|
| **LIDAR Hokuyo** | `urg_node` | `/scan` |
| **Caméra** | `cv_camera` | `/camera/image_raw` |
| **SLAM** | `hector_mapping` | `/map` |
| **Odométrie** | Custom node | `/odom` |
| **Navigation** | `move_base` | `/cmd_vel` |
| **Bras (Arduino)** | `rosserial` | `/servo_angles` |
| **Moteurs** | Custom node | `/motor_cmd` |
| **IHM** | `rosboard` / `rviz` | Tous les topics |

#### 3️⃣ **Traitement des données complexes**

```python
# Exemple : Navigation autonome avec LIDAR
def scanCallback(scan_data):
    # ROS traite les 720 points du LIDAR
    obstacles = detect_obstacles(scan_data)
    
    if obstacle_proche:
        # Décision : tourner à gauche
        publier_commande(vitesse=0, rotation=-0.5)
    else:
        # Décision : avancer
        publier_commande(vitesse=0.3, rotation=0)
```

**Pourquoi ROS et pas Arduino ?**
- Arduino n'a **pas assez de RAM** (8 Ko) pour traiter 720 points LIDAR
- Arduino n'a **pas assez de puissance CPU** pour faire du SLAM
- Arduino ne peut **pas exécuter OpenCV** pour la vision

#### 4️⃣ **Visualisation et debugging**

ROS fournit des outils puissants :
- **RViz** : Visualisation 3D du robot et de son environnement
- **rqt_graph** : Voir les connexions entre nodes
- **rqt_image_view** : Voir les images des caméras
- **rostopic echo** : Débugger les messages
- **rosbag** : Enregistrer et rejouer des données

#### 5️⃣ **Communication par Topics et Services**

```
┌──────────────┐     Topic: /scan      ┌──────────────┐
│  LIDAR Node  │ ──────────────────►   │ SLAM Node    │
└──────────────┘                        └──────────────┘
                                              │
                                              │ Topic: /map
                                              ▼
                                        ┌──────────────┐
                                        │  RViz        │
                                        └──────────────┘
```

**Topics ROS dans notre projet :**

```bash
# Topics de perception
/scan                    # Données LIDAR (sensor_msgs/LaserScan)
/camera/image_raw        # Image caméra (sensor_msgs/Image)
/realsense/depth         # Profondeur RealSense

# Topics de localisation
/odom                    # Odométrie (nav_msgs/Odometry)
/map                     # Carte SLAM (nav_msgs/OccupancyGrid)
/tf                      # Transformations (tf2_msgs/TFMessage)

# Topics de commande
/cmd_vel                 # Commande vitesse moteurs (geometry_msgs/Twist)
/servo_angles            # Commande servos bras (std_msgs/Float32MultiArray)
/direction               # Direction robot (custom message)

# Topics de diagnostic
/diagnostics             # État système
/battery_voltage         # Niveau batterie
```

---

## 🔌 RÔLE DE L'ARDUINO

### 📌 Qu'est-ce que l'Arduino dans notre projet ?

**Arduino Mega** est un **microcontrôleur** qui gère le **contrôle temps réel** des actionneurs.

### 🎯 Responsabilités principales

#### 1️⃣ **Contrôle Temps Réel des Servomoteurs**

```cpp
// Arduino : Contrôle PRÉCIS et RAPIDE
void loop() {
    // Mise à jour toutes les 20ms (50Hz)
    Dynamixel.moveSpeed(SERVO_1, target_position, 200);
    Dynamixel.moveSpeed(SERVO_2, target_position, 200);
    Dynamixel.moveSpeed(SERVO_3, target_position, 200);
    
    // Vérification immédiate
    if (position_servo > MAX_ANGLE) {
        STOP_IMMEDIATELY();  // Sécurité
    }
    
    delay(20);
}
```

**Pourquoi Arduino et pas directement ROS ?**
- ✅ **Timing précis** : Arduino garantit 50Hz sans interruption
- ✅ **Temps réel** : Pas de système d'exploitation qui ralentit
- ✅ **Sécurité** : Si ROS crash, Arduino continue de protéger le matériel
- ✅ **Fiabilité** : Pas de latence aléatoire

#### 2️⃣ **Protocole Dynamixel pour les Servos AX-12**

```cpp
// Arduino gère la communication complexe Dynamixel
void setServoPosition(int id, int position) {
    // Protocole Dynamixel :
    // 1. Envoyer paquet de commande
    // 2. Calculer le checksum
    // 3. Attendre l'accusé réception
    // 4. Vérifier les erreurs
    
    Dynamixel.moveSpeed(id, position, speed);
}

int readServoPosition(int id) {
    return Dynamixel.readPosition(id);
}
```

**Le protocole Dynamixel est complexe :**
- Communication série half-duplex à 1 Mbps
- Calculs de checksum
- Gestion des erreurs matérielles
- Arduino le fait de manière **optimisée**

#### 3️⃣ **Lecture de Capteurs Locaux**

```cpp
// Capteurs connectés directement à l'Arduino
int lire_capteur_courant() {
    return analogRead(PIN_CURRENT_SENSOR);
}

int lire_encodeur() {
    return digitalRead(PIN_ENCODER_A);
}

float lire_tension_batterie() {
    int raw = analogRead(PIN_BATTERY);
    return raw * (5.0 / 1023.0) * 3.0; // Pont diviseur
}
```

#### 4️⃣ **Sécurités Matérielles**

```cpp
void check_securite() {
    // Sécurité 1 : Limites articulaires
    if (angle_servo > ANGLE_MAX) {
        STOP_SERVO();
        LED_ERROR_ON();
    }
    
    // Sécurité 2 : Surintensité
    if (courant > COURANT_MAX) {
        COUPER_ALIMENTATION();
        BUZZER_ALARM();
    }
    
    // Sécurité 3 : Batterie faible
    if (tension_batterie < TENSION_MIN) {
        MODE_SECURITE();
    }
    
    // Sécurité 4 : Watchdog
    if (millis() - dernier_message_ros > 1000) {
        // Pas de commande ROS depuis 1s
        POSITION_SECURITE();
    }
}
```

**L'Arduino protège le matériel même si ROS tombe en panne !**

#### 5️⃣ **Communication avec ROS via rosserial**

```cpp
#include <ros.h>
#include <std_msgs/Float32MultiArray.h>

ros::NodeHandle nh;

// Callback : Arduino reçoit des commandes de ROS
void servo_callback(const std_msgs::Float32MultiArray& msg) {
    // ROS envoie les angles souhaités
    float angle1 = msg.data[0];
    float angle2 = msg.data[1];
    float angle3 = msg.data[2];
    
    // Arduino les applique aux servos
    setServoPosition(1, angle_to_dynamixel(angle1));
    setServoPosition(2, angle_to_dynamixel(angle2));
    setServoPosition(3, angle_to_dynamixel(angle3));
}

// Abonnement au topic ROS
ros::Subscriber<std_msgs::Float32MultiArray> sub("servo_angles", servo_callback);

void setup() {
    nh.initNode();
    nh.subscribe(sub);
}

void loop() {
    nh.spinOnce();  // Traiter les messages ROS
    delay(10);
}
```

---

## 🔄 COMMUNICATION ROS ↔ ARDUINO

### 📡 rosserial : Le pont entre ROS et Arduino

```
┌─────────────────┐                    ┌─────────────────┐
│   ROS (Python)  │                    │  Arduino (C++)  │
│                 │                    │                 │
│  Publication:   │   USB Série        │  Réception:     │
│  servo_angles   │ ──────────────►    │  callback()     │
│                 │   115200 baud      │                 │
│                 │                    │  ↓              │
│                 │                    │  Mouvement      │
│                 │                    │  servos         │
│                 │                    │                 │
│  Réception:     │   USB Série        │  Publication:   │
│  servo_status   │ ◄──────────────    │  état servos    │
└─────────────────┘                    └─────────────────┘
```

### 📝 Exemple concret : Contrôler le bras

#### Côté ROS (Python) :

```python
#!/usr/bin/env python
import rospy
from std_msgs.msg import Float32MultiArray

# Node ROS pour contrôler le bras
rospy.init_node('bras_controller')
pub = rospy.Publisher('servo_angles', Float32MultiArray, queue_size=10)

# Envoyer des angles au bras
msg = Float32MultiArray()
msg.data = [90.0, 45.0, 120.0, 60.0, 0.0, 90.0]  # 6 servos
pub.publish(msg)

# ROS gère l'envoi via USB série automatiquement !
```

#### Côté Arduino (C++) :

```cpp
#include <ros.h>
#include <std_msgs/Float32MultiArray.h>
#include <Dynamixel.h>

ros::NodeHandle nh;

void servo_callback(const std_msgs::Float32MultiArray& msg) {
    // Arduino reçoit les angles et les applique
    for (int i = 0; i < 6; i++) {
        int servo_id = i + 1;
        int position = angle_to_dynamixel(msg.data[i]);
        Dynamixel.moveSpeed(servo_id, position, 100);
    }
}

ros::Subscriber<std_msgs::Float32MultiArray> sub("servo_angles", servo_callback);

void setup() {
    nh.initNode();
    nh.subscribe(sub);
    Dynamixel.begin(1000000, DIRECTION_PIN);
}

void loop() {
    nh.spinOnce();
    delay(10);
}
```

---

## 🎭 QUI FAIT QUOI ? Tableau récapitulatif

| Tâche | ROS | Arduino | Raison |
|-------|-----|---------|--------|
| **Navigation autonome** | ✅ | ❌ | Traitement complexe des données LIDAR |
| **SLAM (Cartographie)** | ✅ | ❌ | Algorithmes gourmands en RAM/CPU |
| **Traitement d'images** | ✅ | ❌ | OpenCV nécessite beaucoup de ressources |
| **Planification de trajectoire** | ✅ | ❌ | Calculs mathématiques complexes |
| **Contrôle servos Dynamixel** | ❌ | ✅ | Timing précis et protocole spécifique |
| **Lecture capteurs analogiques** | ❌ | ✅ | Conversion ADC temps réel |
| **Génération PWM** | ❌ | ✅ | Signal précis avec timers hardware |
| **Sécurités temps réel** | ❌ | ✅ | Réponse immédiate sans latence |
| **Interface utilisateur** | ✅ | ❌ | RViz, rosboard, GUI |
| **Enregistrement de données** | ✅ | ❌ | rosbag pour analyse |
| **Coordination générale** | ✅ | ❌ | Chef d'orchestre du système |
| **Exécution des commandes** | ❌ | ✅ | Contrôle direct du matériel |

---

## 💡 ANALOGIE SIMPLE

Imaginez un **orchestre** :

### 🎼 ROS = Le chef d'orchestre
- **Voit tout** l'ensemble (caméras, LIDAR, capteurs)
- **Décide** de la stratégie globale (où aller, quoi faire)
- **Coordonne** tous les musiciens (LIDAR, caméras, bras, moteurs)
- **Communique** avec le public (interface utilisateur)

### 🎻 Arduino = Les musiciens experts
- **Exécutent** les notes avec **précision** (contrôle servos)
- **Timing parfait** (50Hz sans faille)
- **Expertise technique** (protocole Dynamixel)
- **Réactivité immédiate** (sécurités)

**Sans le chef, les musiciens ne savent pas quoi jouer ensemble.**
**Sans les musiciens, le chef ne peut rien produire.**

---

## 🏗️ ARCHITECTURE COMPLÈTE DU ROBOT ROBOCUP

```
┌─────────────────────────────────────────────────────────────────┐
│                      NIVEAU DÉCISION (ROS)                      │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │  Navigation  │  │    Vision    │  │     SLAM     │         │
│  │  Autonome    │  │   OpenCV     │  │   Mapping    │         │
│  └──────────────┘  └──────────────┘  └──────────────┘         │
│         │                  │                  │                 │
│         └──────────────────┴──────────────────┘                 │
│                            │                                    │
│                  ┌─────────▼─────────┐                          │
│                  │  ROS Master       │                          │
│                  │  (Coordination)   │                          │
│                  └─────────┬─────────┘                          │
│                            │                                    │
└────────────────────────────┼────────────────────────────────────┘
                             │
                    ┌────────▼────────┐
                    │   rosserial     │
                    │  (USB Série)    │
                    └────────┬────────┘
                             │
┌────────────────────────────┼────────────────────────────────────┐
│                  NIVEAU CONTRÔLE (Arduino)                      │
│                  ┌─────────▼─────────┐                          │
│                  │  Arduino Mega     │                          │
│                  │  (Contrôleur)     │                          │
│                  └─────────┬─────────┘                          │
│                            │                                    │
│         ┌──────────────────┼──────────────────┐                 │
│         │                  │                  │                 │
│  ┌──────▼──────┐  ┌────────▼────────┐  ┌──────▼──────┐        │
│  │  Dynamixel  │  │   ADC/GPIO      │  │   Sécurité  │        │
│  │  Protocol   │  │   Capteurs      │  │   Watchdog  │        │
│  └──────┬──────┘  └────────┬────────┘  └──────┬──────┘        │
└─────────┼──────────────────┼──────────────────┼────────────────┘
          │                  │                  │
┌─────────▼──────────────────▼──────────────────▼────────────────┐
│                   NIVEAU PHYSIQUE (Matériel)                    │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐       │
│  │ Servo 1  │  │ Servo 2  │  │  LED     │  │ Buzzer   │       │
│  │  AX-12   │  │  AX-12   │  │  Status  │  │  Alarm   │       │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘       │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🚀 WORKFLOW TYPIQUE : Navigation avec bras

### Scénario : Le robot doit naviguer et saisir un objet

```
1. ROS - PERCEPTION
   └─► LIDAR détecte obstacles
   └─► Caméra détecte objet
   └─► SLAM construit carte

2. ROS - DÉCISION
   └─► Planifier trajectoire vers objet
   └─► Calculer position bras nécessaire
   └─► Éviter obstacles

3. ROS - COMMANDE
   └─► Publier /cmd_vel pour moteurs
   └─► Publier /servo_angles pour bras

4. ARDUINO - RÉCEPTION
   └─► Recevoir commandes via rosserial
   └─► Vérifier sécurités

5. ARDUINO - EXÉCUTION
   └─► Contrôler servos Dynamixel (bras)
   └─► Générer PWM pour moteurs
   └─► Surveiller courant/température

6. ARDUINO - FEEDBACK
   └─► Publier position réelle servos
   └─► Publier état capteurs

7. ROS - VÉRIFICATION
   └─► Comparer position réelle vs désirée
   └─► Ajuster si nécessaire
   └─► Boucle fermée (feedback loop)
```

---

## 📚 FICHIERS CLÉS DU PROJET

### Fichiers ROS (Python/C++)
```
Robocup 2024/RaspBerry/Lidar_embarqué/ROBOCUP2024/
├── src/
│   ├── Exploration_Tom.cpp          # Navigation autonome
│   ├── odometrie_lidar.cpp          # Calcul odométrie
│   └── Sabertooth_manette/          # Contrôle moteurs
├── launch/
│   └── Rescue.launch                # Lancement complet système
└── CMakeLists.txt                   # Compilation ROS
```

### Fichiers Arduino (C++)
```
Robocup 2024/RaspBerry/RaspBerry_Bras/Arduino/
└── Bras_ROS_Mega/
    ├── Bras_ROS_Mega.ino            # Programme principal
    ├── Dynamixel.ino                # Contrôle servos Dynamixel
    ├── Fonctions.ino                # Fonctions utilitaires
    └── libraries/
        └── Dynamixel/               # Bibliothèque protocole
```

### Fichiers Python pour interface
```
Robocup 2024/RaspBerry/RaspBerry_Bras/bras_robot/src/
├── slider.py                        # Interface graphique contrôle
└── sliderbras2.py                   # Version améliorée
```

---

## ❓ FAQ - Questions fréquentes

### Q1 : Pourquoi ne pas tout faire avec ROS ?
**R :** ROS n'est pas temps réel. Linux peut interrompre un processus à tout moment. Arduino garantit un timing précis essentiel pour les servos.

### Q2 : Pourquoi ne pas tout faire avec Arduino ?
**R :** Arduino Mega a 256 Ko de mémoire flash et 8 Ko de RAM. Impossible de faire tourner SLAM, OpenCV, ou traiter les 720 points du LIDAR.

### Q3 : Peut-on utiliser un Raspberry Pi seul ?
**R :** Oui pour ROS, mais le RPi n'a pas de GPIO temps réel fiable pour le protocole Dynamixel. Arduino gère mieux le matériel bas niveau.

### Q4 : Comment débugger la communication ROS ↔ Arduino ?
```bash
# Vérifier la connexion série
rosrun rosserial_python serial_node.py /dev/ttyACM1

# Voir les messages
rostopic echo /servo_angles
rostopic echo /servo_status

# Moniteur série Arduino
# Ouvrir Arduino IDE > Outils > Moniteur Série (115200 baud)
```

### Q5 : Que se passe-t-il si ROS crash ?
**R :** Arduino continue de fonctionner et active les sécurités :
- Watchdog détecte l'absence de messages ROS
- Servos vont en position de sécurité
- Moteurs s'arrêtent
- LED d'erreur s'allume

---

## 🎯 RÉSUMÉ EN 3 POINTS

### 1️⃣ ROS = Cerveau 🧠
- Décisions intelligentes
- Traitement de données complexes
- Coordination générale

### 2️⃣ Arduino = Muscles 💪
- Exécution précise et rapide
- Contrôle direct du matériel
- Sécurités temps réel

### 3️⃣ rosserial = Système nerveux 🔌
- Communication entre cerveau et muscles
- Échange de commandes et de retours
- Synchronisation

---

## 🔗 RESSOURCES COMPLÉMENTAIRES

### Documentation ROS
- http://wiki.ros.org/rosserial_arduino
- http://wiki.ros.org/rosserial/Tutorials

### Documentation Arduino
- https://www.arduino.cc/reference/en/
- http://emanual.robotis.com/docs/en/dxl/ax/ax-12a/ (Dynamixel)

### Tutoriels intégration ROS + Arduino
- http://wiki.ros.org/rosserial_arduino/Tutorials/Arduino%20IDE%20Setup
- http://wiki.ros.org/rosserial_arduino/Tutorials/Hello%20World

---

**💡 Pensez à ROS et Arduino comme une équipe : ROS pense, Arduino agit ! 🤝**
