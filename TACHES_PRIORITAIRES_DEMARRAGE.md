# 🚀 TÂCHES PRIORITAIRES POUR DÉMARRER LE PROJET

## ⚡ DÉMARRAGE IMMÉDIAT (Jour 1-2)

### 🔴 PRIORITÉ CRITIQUE #1 : Configuration de l'environnement Docker

**Responsable :** Personne 4 (+ aide de tous)

**Objectif :** Avoir un environnement ROS1 fonctionnel pour tous

#### Actions immédiates :
```bash
# 1. Vérifier Docker
docker --version
docker ps

# 2. Tester le script de lancement
cd ~/RoboCup_ws
./launch_robot.sh

# 3. Si problème de permissions
sudo usermod -aG docker $USER
# PUIS SE DÉCONNECTER ET SE RECONNECTER

# 4. Télécharger l'image ROS1
docker pull ros:noetic-robot
```

**Temps estimé :** 1-2 heures
**Critère de succès :** ✅ Tous peuvent lancer `./launch_robot.sh` sans erreur

---

### 🔴 PRIORITÉ CRITIQUE #2 : Vérifier la structure du projet

**Responsable :** Tous ensemble

**Objectif :** Comprendre où se trouvent les fichiers importants

#### Actions immédiates :
```bash
# 1. Explorer la structure
cd ~/RoboCup_ws
tree -L 3 "Robocup 2024/RaspBerry/Lidar_embarqué/ROBOCUP2024/"

# 2. Identifier les packages ROS1
find "Robocup 2024/" -name "package.xml" -o -name "CMakeLists.txt"

# 3. Lire les launch files
cat "Robocup 2024/RaspBerry/Lidar_embarqué/ROBOCUP2024/launch/Rescue.launch"
```

**Temps estimé :** 1 heure
**Critère de succès :** ✅ Chacun connaît l'emplacement de "son" code

---

### 🔴 PRIORITÉ CRITIQUE #3 : Compiler le code ROS1 existant

**Responsable :** Personne 4 (+ Personne 1)

**Objectif :** Vérifier que le code compile sans erreur

#### Actions immédiates :
```bash
# Dans le container Docker ROS1
./launch_robot.sh
# Puis choisir l'option "Entrer dans le container"

# Une fois dans le container
cd /home/ser/RoboCup_ws/Robocup\ 2024/RaspBerry/Lidar_embarqué/ROBOCUP2024/
source /opt/ros/noetic/setup.bash
catkin_make

# Vérifier les erreurs de compilation
echo $?  # Doit retourner 0 si succès
```

**Temps estimé :** 2-3 heures (avec corrections éventuelles)
**Critère de succès :** ✅ `catkin_make` réussit sans erreur

---

## 🟠 SEMAINE 1 : Tests matériels de base

### 🔴 PRIORITÉ #4 : Test LIDAR Hokuyo

**Responsable :** Personne 1

**Objectif :** Vérifier que le LIDAR est détecté et publie des données

#### Actions :
```bash
# 1. Connecter le LIDAR Hokuyo via USB

# 2. Vérifier la détection
ls -l /dev/ttyACM*
# Devrait afficher /dev/ttyACM0

# 3. Donner les permissions
sudo chmod 666 /dev/ttyACM0

# 4. Lancer le test LIDAR
./launch_robot.sh
# Choisir "Lancer le robot en mode Navigation"

# 5. Dans un autre terminal (dans Docker)
docker exec -it robocup_ros1 bash
source /opt/ros/noetic/setup.bash
rostopic list | grep scan
rostopic echo /scan -n 1
rostopic hz /scan
```

**Temps estimé :** 2-3 heures
**Critère de succès :** 
- ✅ `/scan` publie à ~10Hz
- ✅ Données de distance cohérentes

---

### 🔴 PRIORITÉ #5 : Test Arduino + Servos Dynamixel

**Responsable :** Personne 3

**Objectif :** Vérifier la communication avec les servos du bras

#### Actions :
```bash
# 1. Connecter l'Arduino Mega via USB

# 2. Identifier le port
ls -l /dev/ttyACM* /dev/ttyUSB*

# 3. Téléverser le code Arduino
# Ouvrir Arduino IDE
# Fichier > Ouvrir > RoboCup_ws/Robocup 2024/RaspBerry/RaspBerry_Bras/Arduino/Bras_ROS_Mega/Bras_ROS_Mega.ino

# 4. Dans l'IDE Arduino :
# - Sélectionner "Arduino Mega"
# - Port : /dev/ttyACM1 (ou autre)
# - Téléverser

# 5. Ouvrir le Moniteur Série (115200 baud)
# Vérifier les messages de démarrage
```

**Temps estimé :** 3-4 heures
**Critère de succès :** 
- ✅ Arduino communique via le port série
- ✅ Servos Dynamixel répondent aux commandes

---

### 🟡 PRIORITÉ #6 : Test Moteurs Sabertooth

**Responsable :** Personne 4

**Objectif :** Contrôler les moteurs de la plateforme mobile

#### Actions :
```bash
# 1. Connecter Sabertooth via série

# 2. Identifier le port
ls -l /dev/ttyUSB*

# 3. Tester avec minicom
sudo apt install minicom
sudo minicom -D /dev/ttyUSB0 -b 9600

# 4. Envoyer des commandes manuelles
# (voir documentation Sabertooth)

# 5. Tester avec le code ROS
# (après compilation réussie)
```

**Temps estimé :** 2-3 heures
**Critère de succès :** 
- ✅ Moteurs répondent aux commandes
- ✅ Direction gauche/droite fonctionnelle

---

### 🟡 PRIORITÉ #7 : Test Caméra 8MP

**Responsable :** Personne 2

**Objectif :** Capturer des images depuis la caméra

#### Actions :
```bash
# 1. Connecter caméra USB

# 2. Vérifier avec v4l2
sudo apt install v4l-utils
v4l2-ctl --list-devices

# 3. Tester avec cv_camera dans Docker
docker exec -it robocup_ros1 bash
source /opt/ros/noetic/setup.bash
rosrun cv_camera cv_camera_node

# 4. Dans un autre terminal
rostopic list | grep camera
rqt_image_view
# Sélectionner /cv_camera/image_raw
```

**Temps estimé :** 2 heures
**Critère de succès :** 
- ✅ Image visible dans `rqt_image_view`
- ✅ Topic `/camera/image_raw` publie à >15fps

---

## 📋 CHECKLIST DE DÉMARRAGE (à faire dans l'ordre)

### ✅ Jour 1 : Setup environnement
- [ ] **TOUS :** Installer et tester Docker
- [ ] **TOUS :** Cloner/mettre à jour le dépôt Git
- [ ] **TOUS :** Exécuter `./launch_robot.sh` avec succès
- [ ] **Personne 4 :** Vérifier que tout le monde peut accéder au container

### ✅ Jour 2-3 : Compilation et structure
- [ ] **Personne 4 :** Compiler le code ROS1 dans Docker
- [ ] **TOUS :** Explorer et comprendre la structure du code
- [ ] **Personne 1 :** Lire `Exploration_Tom.cpp`
- [ ] **Personne 2 :** Identifier les nodes de vision
- [ ] **Personne 3 :** Comprendre le code Arduino
- [ ] **Personne 4 :** Analyser les launch files

### ✅ Semaine 1 : Tests matériels
- [ ] **Personne 1 :** LIDAR fonctionnel et publie `/scan`
- [ ] **Personne 2 :** Caméra publie `/camera/image_raw`
- [ ] **Personne 3 :** Arduino communique avec les servos
- [ ] **Personne 4 :** Moteurs Sabertooth répondent

### ✅ Semaine 2 : Intégration de base
- [ ] **Personne 1 :** SLAM crée une carte simple
- [ ] **Personne 2 :** Traitement d'image basique
- [ ] **Personne 3 :** Bras bouge via commandes ROS
- [ ] **Personne 4 :** Odométrie basique fonctionne

---

## 🎯 OBJECTIF SEMAINE 2 : PREMIÈRE DÉMONSTRATION

**Mission :** Robot capable de :
1. ✅ Scanner l'environnement avec le LIDAR
2. ✅ Construire une carte simple
3. ✅ Afficher l'image de la caméra
4. ✅ Bouger les moteurs en avant/arrière
5. ✅ Contrôler le bras manuellement

**Critère de succès :** Démonstration de 5 minutes où tous les composants fonctionnent

---

## 📊 TABLEAU DE SUIVI QUOTIDIEN

### Personne 1 - Navigation & LIDAR
| Jour | Tâche | Status | Blocage ? |
|------|-------|--------|-----------|
| J1 | Docker setup | ⏳ | |
| J2 | Compilation ROS1 | ⏳ | |
| J3 | Test LIDAR | ⏳ | |
| J4 | Debug LIDAR | ⏳ | |
| J5 | SLAM basique | ⏳ | |

### Personne 2 - Vision & Caméras
| Jour | Tâche | Status | Blocage ? |
|------|-------|--------|-----------|
| J1 | Docker setup | ⏳ | |
| J2 | Explorer code vision | ⏳ | |
| J3 | Test caméra 8MP | ⏳ | |
| J4 | Debug caméra | ⏳ | |
| J5 | Capture images | ⏳ | |

### Personne 3 - Bras & Arduino
| Jour | Tâche | Status | Blocage ? |
|------|-------|--------|-----------|
| J1 | Arduino IDE setup | ⏳ | |
| J2 | Lire code Arduino | ⏳ | |
| J3 | Upload code | ⏳ | |
| J4 | Test servos | ⏳ | |
| J5 | ROS Serial | ⏳ | |

### Personne 4 - Plateforme & Intégration
| Jour | Tâche | Status | Blocage ? |
|------|-------|--------|-----------|
| J1 | Setup Docker tous | ⏳ | |
| J2 | Compilation ROS1 | ⏳ | |
| J3 | Test Sabertooth | ⏳ | |
| J4 | Debug moteurs | ⏳ | |
| J5 | Intégration tests | ⏳ | |

**Légende :** ⏳ À faire | 🔄 En cours | ✅ Terminé | ❌ Bloqué

---

## 🆘 PROCÉDURE EN CAS DE BLOCAGE

### Si Docker ne fonctionne pas
```bash
# Vérifier l'installation
docker --version

# Vérifier les permissions
sudo usermod -aG docker $USER
newgrp docker  # Ou se déconnecter/reconnecter

# Tester
docker run hello-world
```

### Si la compilation échoue
```bash
# Vérifier les dépendances
rosdep install --from-paths src --ignore-src -r -y

# Nettoyer et recompiler
catkin_make clean
catkin_make

# Vérifier les erreurs spécifiques
catkin_make 2>&1 | grep error
```

### Si le LIDAR ne se connecte pas
```bash
# Vérifier la détection USB
lsusb | grep -i hokuyo

# Vérifier les permissions
ls -l /dev/ttyACM*
sudo chmod 666 /dev/ttyACM0

# Tester avec le driver
rosrun urg_node urg_node _serial_port:=/dev/ttyACM0
```

### Si les servos ne répondent pas
```bash
# Vérifier l'alimentation
# Les servos Dynamixel nécessitent 12V

# Vérifier les IDs avec le logiciel Dynamixel Wizard
# Télécharger depuis : https://emanual.robotis.com/

# Vérifier le baud rate (1000000 par défaut)
```

---

## 📞 COMMUNICATION D'ÉQUIPE

### Daily Standup (15 min/jour)
**Quand :** Chaque matin 9h00

**Format :**
1. Qu'ai-je fait hier ?
2. Que vais-je faire aujourd'hui ?
3. Ai-je des blocages ?

### Réunion technique (1h/semaine)
**Quand :** Vendredi 16h00

**Format :**
1. Démonstration de ce qui fonctionne
2. Problèmes techniques rencontrés
3. Plan pour la semaine suivante

### Outil de suivi
- **GitHub Issues** pour les bugs
- **GitHub Projects** pour le kanban
- **Discord/Slack** pour la communication rapide

---

## 🎓 RESSOURCES POUR DÉMARRER

### ROS1 Basics (à lire en priorité)
1. http://wiki.ros.org/ROS/Tutorials/UnderstandingNodes
2. http://wiki.ros.org/ROS/Tutorials/UnderstandingTopics
3. http://wiki.ros.org/ROS/Tutorials/WritingPublisherSubscriber%28c%2B%2B%29

### Docker + ROS
1. Lire : `DEMARRAGE_RAPIDE.md` (dans le projet)
2. Lire : `DEMARRAGE_ROBOT_ROS1.md` (dans le projet)

### Debugging ROS
```bash
# Voir tous les nodes actifs
rosnode list

# Voir tous les topics
rostopic list

# Voir les infos d'un topic
rostopic info /scan

# Afficher les messages
rostopic echo /scan

# Tester la fréquence
rostopic hz /scan

# Graphe des connections
rqt_graph
```

---

## ✅ CRITÈRES DE SUCCÈS - FIN SEMAINE 1

### Minimum Viable Product (MVP)
- [ ] **Environnement :** Docker ROS1 fonctionne pour tout le monde
- [ ] **Compilation :** Le code ROS1 compile sans erreur
- [ ] **LIDAR :** Détecté et publie des données
- [ ] **Caméra :** Publie des images
- [ ] **Arduino :** Communique avec l'ordinateur
- [ ] **Moteurs :** Répondent aux commandes basiques

### Bonus (si temps disponible)
- [ ] **SLAM :** Commence à construire une carte
- [ ] **Bras :** Bouge via des commandes manuelles
- [ ] **IHM :** RViz affiche LIDAR + caméra
- [ ] **Documentation :** Problèmes rencontrés documentés

---

## 🚀 APRÈS LA SEMAINE 1

Une fois les bases fonctionnelles, passez à :
1. **Semaine 2-3 :** Intégration et tests (voir `REPARTITION_TACHES_EQUIPE.md`)
2. **Semaine 4-6 :** Optimisation ROS1
3. **Semaine 7+ :** Début migration ROS2

---

## 📝 TEMPLATE DE RAPPORT QUOTIDIEN

```markdown
# Rapport - [Prénom] - [Date]

## ✅ Réalisé aujourd'hui
- 

## 🔄 En cours
- 

## ⏳ Prévu demain
- 

## ❌ Blocages
- 

## 💡 Notes / Découvertes
- 
```

---

**🎯 Objectif : À la fin de la Semaine 1, tout le monde doit pouvoir lancer le robot et voir au moins un composant fonctionner !**

**🤝 N'hésitez pas à vous entraider ! Le succès est collectif ! 🚀**
