# 👥 RÉPARTITION DES TÂCHES - ÉQUIPE ROBOCUP (4 PERSONNES)

## 👤 PERSONNE 1 : RESPONSABLE NAVIGATION & LIDAR

### 🎯 Objectifs

#### ✅ Tâche 1.1 : Faire fonctionner le LIDAR
- [ ] Tester la connexion du LIDAR Hokuyo (`/dev/ttyACM0`)
- [ ] Vérifier le node `urg_node`
- [ ] S'assurer que le topic `/scan` publie des données
- [ ] Documenter les fréquences et formats de données

#### ✅ Tâche 1.2 : SLAM et Cartographie
- [ ] Configurer `hector_mapping` pour la construction de carte
- [ ] Ajuster les paramètres de cartographie
- [ ] Tester la génération de cartes GeoTIFF
- [ ] Optimiser la qualité de la carte

#### ✅ Tâche 1.3 : Navigation autonome
- [ ] Analyser `Exploration_Tom.cpp`
- [ ] Comprendre l'algorithme d'évitement d'obstacles
- [ ] Tester la fonction `deplacement_automatique()`
- [ ] Documenter le comportement du robot

**Délivrables :**
- [ ] Node LIDAR fonctionnel en ROS2
- [ ] SLAM opérationnel en ROS2
- [ ] Code de navigation migré
- [ ] Documentation de migration


## 👤 PERSONNE 2 : RESPONSABLE VISION & CAMÉRAS

### 🎯 Objectifs 

#### ✅ Tâche 2.1 : Caméra 8MP
- [ ] Tester la connexion caméra 8MP
- [ ] Vérifier le node `cv_camera`
- [ ] S'assurer que `/camera/image_raw` fonctionne
- [ ] Enregistrer des images de test

#### ✅ Tâche 2.2 : Caméra RealSense (RGBD)
- [ ] Installer et configurer `realsense2_camera`
- [ ] Tester la détection de profondeur
- [ ] Publier les topics RGB + Depth
- [ ] Calibrer la caméra

#### ✅ Tâche 2.3 : Traitement d'images
- [ ] Implémenter la détection de victimes (si nécessaire)
- [ ] Utiliser OpenCV pour le traitement
- [ ] Publier les résultats de détection
- [ ] Optimiser les performances

**Délivrables :**
- [ ] Toutes les caméras fonctionnelles en ROS2
- [ ] Pipeline de vision migré
- [ ] Documentation caméras ROS2
- [ ] Exemples de code

---

## 👤 PERSONNE 3 : RESPONSABLE BRAS ROBOTIQUE & ARDUINO

### 🎯 Objectifs

#### ✅ Tâche 3.1 : Arduino et Dynamixel
- [ ] Téléverser le code Arduino `Bras_ROS_Mega.ino`
- [ ] Tester la communication avec les servos AX-12
- [ ] Vérifier les angles min/max de chaque servo
- [ ] Documenter les IDs des servomoteurs

#### ✅ Tâche 3.2 : ROS Serial
- [ ] Configurer `rosserial_arduino`
- [ ] Établir la communication Arduino ↔ ROS
- [ ] Publier/Souscrire aux topics du bras
- [ ] Tester la latence de communication

#### ✅ Tâche 3.3 : Interface de contrôle Python
- [ ] Tester `slider.py` pour contrôle manuel
- [ ] Créer une interface graphique améliorée (optionnel)
- [ ] Implémenter des positions prédéfinies
- [ ] Ajouter des limites de sécurité

#### ✅ Tâche 3.4 : Modèle URDF du bras
- [ ] Vérifier le fichier URDF existant
- [ ] Afficher le modèle dans RViz
- [ ] Tester la cinématique inverse (si implémentée)

#### ✅ Tâche 3.6 : Interface Python
- [ ] Réécrire `slider.py` avec `rclpy`
- [ ] Utiliser `rclpy.node.Node`
- [ ] Adapter les publishers/subscribers

#### ✅ Tâche 3.7 : URDF et RViz2
- [ ] Migrer le modèle URDF vers ROS2
- [ ] Tester dans RViz2
- [ ] Utiliser `robot_state_publisher` ROS2

**Délivrables :**
- [ ] Bras fonctionnel en ROS2
- [ ] Communication Arduino stable
- [ ] Interface de contrôle migrée
- [ ] Documentation complète du bras

---

## 👤 PERSONNE 4 : RESPONSABLE PLATEFORME MOBILE & INTÉGRATION

### 🎯 Objectifs

#### ✅ Tâche 4.1 : Moteurs Sabertooth
- [ ] Tester les contrôleurs Sabertooth
- [ ] Configurer la communication série
- [ ] Implémenter le contrôle de vitesse
- [ ] Calibrer les moteurs gauche/droite

#### ✅ Tâche 4.2 : Odométrie
- [ ] Configurer les encodeurs
- [ ] Implémenter le calcul de l'odométrie
- [ ] Publier le topic `/odom`
- [ ] Fusionner avec les données LIDAR

#### ✅ Tâche 4.3 : Transformation TF
- [ ] Configurer l'arbre TF (base_link, laser, odom)
- [ ] Publier les transformations correctes
- [ ] Vérifier dans RViz

#### ✅ Tâche 4.4 : Intégration Docker
- [ ] Améliorer le script `launch_robot.sh`
- [ ] Créer des scripts pour chaque mode
- [ ] Gérer les dépendances automatiquement
- [ ] Documenter le workflow Docker

#### ✅ Tâche 4.5 : IHM et Rosboard
- [ ] Configurer Rosboard pour ROS2
- [ ] Créer un dashboard personnalisé
- [ ] Ajouter les widgets pour tous les capteurs
- [ ] Tester l'interface web

**Fichiers concernés :**
- `Robocup 2024/Manette & IHM/IHM_Robot_RMS/rosboard/`

### 🎯 Objectifs Phase 2 (Migration ROS2)

#### ✅ Tâche 4.6 : Migration contrôle moteurs
- [ ] Adapter le code Sabertooth pour ROS2
- [ ] Utiliser `rclcpp` pour le node
- [ ] Tester la réactivité

#### ✅ Tâche 4.7 : Odométrie ROS2
- [ ] Migrer le calcul d'odométrie
- [ ] Utiliser `nav_msgs/Odometry` ROS2
- [ ] Publier les TF avec `tf2_ros`

#### ✅ Tâche 4.8 : Intégration complète ROS2
- [ ] Créer un workspace ROS2 propre
- [ ] Organiser les packages par fonction
- [ ] Créer des launch files Python
- [ ] Documenter l'architecture

**Structure proposée :**
```
src/
├── robocup_navigation/    (LIDAR + SLAM)
├── robocup_vision/        (Caméras)
├── robocup_arm/           (Bras)
├── robocup_base/          (Plateforme mobile)
└── robocup_bringup/       (Launch files globaux)
```

#### ✅ Tâche 4.9 : Tests d'intégration
- [ ] Tester tous les composants ensemble en ROS2
- [ ] Vérifier la communication entre nodes
- [ ] Optimiser les performances
- [ ] Créer des tests automatisés

**Délivrables :**
- [ ] Plateforme mobile fonctionnelle en ROS1 et ROS2
- [ ] Système d'intégration Docker optimisé
- [ ] IHM complète
- [ ] Architecture ROS2 documentée
- [ ] Guide de migration complet

---

## 🛠️ OUTILS COMMUNS À TOUS

### Environnement de développement
- **Docker** avec ROS1 Noetic (Phase 1)
- **ROS2 Humble** natif (Phase 2)
- **Git** pour versioning
- **VS Code** avec extensions ROS

### Documentation
- Chaque personne documente son travail dans `docs/`
- Utiliser Markdown pour les guides
- Créer des diagrammes avec draw.io

### Communication
- Réunions hebdomadaires de synchronisation
- Slack/Discord pour communication rapide
- GitHub Issues pour suivi des tâches

---

## 📊 INDICATEURS DE SUCCÈS

### Phase 1 ✅
- [ ] LIDAR publie sur `/scan` à >10Hz
- [ ] Carte construite visible dans RViz
- [ ] Robot navigue en autonome sans collision
- [ ] Caméras publient des images à >15fps
- [ ] Bras répond aux commandes en <100ms
- [ ] Moteurs répondent correctement
- [ ] Tout fonctionne ensemble dans Docker

### Phase 2 ✅
- [ ] Tous les nodes fonctionnent en ROS2
- [ ] Launch files Python opérationnels
- [ ] Performance égale ou meilleure qu'en ROS1
- [ ] Code documenté et testé
- [ ] CI/CD configuré (optionnel)
- [ ] Guide de migration complet


## 🎯 PRIORITÉS

### 🔴 Priorité Haute (Critique)
1. LIDAR fonctionnel
2. Communication Arduino
3. Contrôle moteurs
4. Docker stable

### 🟡 Priorité Moyenne (Important)
1. Caméras
2. SLAM
3. Navigation autonome
4. IHM

### 🟢 Priorité Basse (Optionnel)
1. Détection de victimes
2. Optimisations avancées
3. Interface web élaborée

