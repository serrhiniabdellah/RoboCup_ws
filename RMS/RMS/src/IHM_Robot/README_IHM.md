# Interface Homme-Machine (IHM) Web - Documentation

## 📋 Vue d'ensemble

L'IHM est une interface web complète permettant de contrôler et de monitorer le robot **RoboCup Rescue** de manière intuitive via un navigateur.

Elle offre :
- **Contrôle du robot** (mouvements omnidirectionnels)
- **Contrôle du bras** (positionnement, rotation, pince)
- **Visualisation vidéo** (caméras, lidar)
- **Joystick virtuel** pour manette analogique

---

## 📁 Structure des fichiers

### **Fichiers HTML (Pages)**

#### `index.html`
- **Rôle** : Page d'accueil/frameset principal
- **Description** : Point d'entrée de l'IHM, contient la navigation vers les autres pages
- **Liens** : Accès aux différents modules (robot, bras, caméras, lidar)

#### `joystick.html`
- **Rôle** : Interface de manette virtuelle
- **Description** : Contrôle analogique du robot avec deux joysticks (mouvement + rotation)
- **Utilité** : Alternative au clavier pour un contrôle plus fluide et intuitif

#### `deplacement_robot.html`
- **Rôle** : Contrôle du robot (déplacement base)
- **Description** : Interface de contrôle directionnel (avant/arrière/gauche/droite)
- **Composants** : Boutons directionnels, indicateur de vitesse

#### `deplacement_bras.html`
- **Rôle** : Contrôle du bras robotique
- **Description** : Interface pour positionner le bras (X, Y, Z), rotation (Rot X/Y/Z), et pince
- **Liaison** : Se connecte au nœud ROS `slider_node` qui expose les sliders Matplotlib

#### `vision_camera.html`
- **Rôle** : Visualisation du flux caméra
- **Description** : Affiche en temps réel le flux vidéo de la caméra du robot
- **Utilité** : Feedback vidéo pour téléopération

#### `vision_lidar.html`
- **Rôle** : Visualisation des données Lidar
- **Description** : Affichage 2D/3D de la carte construite par le lidar (nuage de points)
- **Utilité** : Navigation autonome, détection d'obstacles

### **Fichiers CSS (Styles)**

Chaque page HTML a son fichier CSS associé pour la mise en forme et le responsive design :

| Fichier CSS | Page associée | Description |
|------------|---|---|
| `style.css` | Global | Styles globaux (couleurs, polices, layout général) |
| `deplacement_robot.css` | deplacement_robot.html | Styles des boutons directionnels du robot |
| `deplacement_bras.css` | deplacement_bras.html | Styles des sliders et contrôles du bras |
| `vision_camera.css` | vision_camera.html | Styles du lecteur vidéo caméra |
| `vision_lidar.css` | vision_lidar.html | Styles de la visualisation lidar |

### **Fichiers JavaScript (Logique)**

Chaque page HTML a son `.js` associé pour les interactions client-ROS2 bridging :

| Fichier JS | Page associée | Description |
|-----------|---|---|
| `deplacement_robot.js` | deplacement_robot.html | Gère les événements clavier/souris → publish topics ROS |
| `deplacement_bras.js` | deplacement_bras.html | Synchronisation sliders web ↔ nœud Python slider_node |
| `vision_camera.js` | vision_camera.html | Souscription au topic `/output_image_topic*` et affichage |
| `vision_lidar.js` | vision_lidar.html | Souscription aux données lidar, rendu 2D/3D canvas/WebGL |

### **Ressources (Images/Assets)**

```
photos/
  ├── UVSQ.png              # Logo UVSQ (en-tête)
  ├── robot.png             # Icône du robot
  ├── fleche_haut.png       # Bouton directionnel ↑
  ├── fleche_bas.png        # Bouton directionnel ↓
  ├── fleche_gauche.png     # Bouton directionnel ←
  └── fleche_droite.png     # Bouton directionnel →

Pour_la_pethouse/              # Ressources alternatives (version pethouse)
  ├── favicon.ico
  ├── camera_2.html
```

---

## 🔌 Communication ROS 2 - Web

### **Topics publiés par l'IHM**

| Topic | Type | Description |
|-------|------|---|
| `/cmd_vel` | geometry_msgs/Twist | Commandes de vitesse du robot (linéaire + angulaire) |
| `/pince` | std_msgs/Bool | Commande d'ouverture/fermeture de la pince |
| `/chatter` | std_msgs/String | Messages textes (debug/status) |
| `/data` | std_msgs/Float64MultiArray | Données du slider node (position + orientation bras) |

### **Topics souscrits par l'IHM**

| Topic | Type | Utilité |
|-------|------|---|
| `/cv_camera/image_raw` | sensor_msgs/Image | Flux caméra 1 pour visualisation |
| `/cv_camera2/image_raw` | sensor_msgs/Image | Flux caméra 2 |
| `/lidar/scan` | sensor_msgs/LaserScan | Données brutes du lidar |
| `/nav/path` | nav_msgs/Path | Trajectoire planifiée |

---

## 🚀 Démarrage de l'IHM

### **Prérequis**
- Serveur **rosbridge_suite** ROS 2 en cours d'exécution (Websocket sur port 9090)
- Serveur web HTTP (ex: Python SimpleHTTPServer, nginx, Apache)

### **Lancement**

```bash
# 1. Démarrer rosbridge_websocket
ros2 launch rosbridge_server rosbridge_websocket_launch.xml

# 2. Servir les fichiers web (depuis le dossier IHM_Robot)
cd src/IHM_Robot
python3 -m http.server 8000

# 3. Accéder via navigateur
http://localhost:8000/index.html
```

---

## 🔧 Configuration

### **Parameter : Port Websocket ROS**
Dans les fichiers `.js`, modifiez si besoin la connexion :
```javascript
// Exemple dans deplacement_robot.js
const roslibConnection = new ROSLIB.Ros({
    url: 'ws://localhost:9090'  // ← Adapter si serveur distant
});
```

### **Color Coding**
- **Vert** : Système opérationnel
- **Orange** : Avertissement (batterie faible, etc.)
- **Rouge** : Erreur/Arrêt d'urgence

---

## 📝 Développement Futur

- [ ] Mode autonome (prédéfinition de missions)
- [ ] Graphe du chemin exploré
- [ ] Système d'alarme visuel/sonore
- [ ] Multi-caméras avec sélection
- [ ] Enregistrement de sessions

---

## 👥 Auteurs

- Groupe MT5 RoboCup Rescue ISTY (2024-2025)
- **Responsable Web** : À identifier
- **Framework** : HTML5 + CSS3 + JavaScript + [roslibjs](http://docs.ros.org/en/hydro/api/rosjava_js/html/)

---

**Dernière mise à jour** : 19 mars 2026
