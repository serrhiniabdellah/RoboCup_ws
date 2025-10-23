# ⚠️ IMPORTANT - Structure du Projet RoboCup

## 🔍 État actuel du projet

### ROS1 vs ROS2

Ce projet utilise **deux versions de ROS** :

| Version ROS | Emplacement | État | Utilisation |
|-------------|-------------|------|-------------|
| **ROS1 Noetic** | `Robocup 2024/` | ✅ **Actif** | Code du robot actuel |
| **ROS2 Humble** | `src/` (vide) | 🔄 En préparation | Migration future |

### 📁 Structure importante

```
RoboCup_ws/
├── src/                          # ❌ VIDE - Pour ROS2 (futur)
├── Robocup 2024/                 # ✅ CODE ACTIF - ROS1
│   ├── RaspBerry/
│   │   ├── Lidar_embarqué/ROBOCUP2024/     # Navigation principale
│   │   ├── Fichiers catkin/robocup2024/    # Packages ROS1
│   │   └── RaspBerry_Bras/                 # Contrôle bras
│   └── PaysBas/Robocup2024_PaysBas/        # Code compétition
└── COLCON_IGNORE                 # Fichier créé pour éviter conflits
```

## 🚀 Comment utiliser le projet

### Pour travailler avec le code ACTUEL (ROS1) :

```bash
# 1. Sourcer ROS1
source /opt/ros/noetic/setup.bash

# 2. Aller dans le workspace ROS1
cd "~/RoboCup_ws/Robocup 2024/RaspBerry/Fichiers catkin/robocup2024"

# 3. Compiler (si nécessaire)
catkin_make

# 4. Sourcer le workspace
source devel/setup.bash

# 5. Lancer un programme
roslaunch ROBOCUP2024 Rescue.launch
```

### Pour préparer la migration vers ROS2 :

```bash
# 1. Sourcer ROS2
source /opt/ros/humble/setup.bash

# 2. Aller à la racine du workspace
cd ~/RoboCup_ws

# 3. Compiler (actuellement vide)
colcon build --symlink-install

# 4. Sourcer
source install/setup.bash
```

## ⚠️ Problèmes résolus

### Erreur "Duplicate package names"

**Cause :** Plusieurs versions du même package dans différents dossiers (sauvegardes, anciennes versions).

**Solution :** Fichiers `COLCON_IGNORE` créés dans :
- `Robocup 2024/` (tout le dossier ignoré par colcon)
- `Sauvegarde Elian 15-08-2024/`
- `Fichiers catkin/v05_03_2024/`
- `Fichiers catkin/v22_02_2024/`
- `Fichiers catkin/v_19_02_2024_Angelique/`

### Erreur "find_package catkin"

**Cause :** Tentative de compiler des packages ROS1 avec colcon (outil ROS2).

**Solution :** Utiliser `catkin_make` pour ROS1, `colcon build` pour ROS2.

## 📝 Commandes essentielles

### Vérifier quelle version de ROS est active

```bash
echo $ROS_DISTRO
# Devrait afficher: "noetic" (ROS1) ou "humble" (ROS2)
```

### Basculer entre ROS1 et ROS2

```bash
# Passer à ROS1
source /opt/ros/noetic/setup.bash

# Passer à ROS2
source /opt/ros/humble/setup.bash
```

### Lister les packages disponibles

```bash
# ROS1
rospack list | grep robocup

# ROS2
ros2 pkg list | grep robocup
```

## 🎯 Recommandations

1. **Pour le développement actuel** : Utilisez ROS1 Noetic
2. **Pour les nouveaux packages** : Envisagez ROS2 Humble
3. **Migration** : Planifiez la migration progressive des packages ROS1 vers ROS2

## 📚 Documentation

- **Guide complet** : `QUICK_START_GUIDE.md`
- **README principal** : `README.md`
- **Contribution** : `CONTRIBUTING.md`

## 🔗 Ressources

- [ROS1 Noetic Documentation](http://wiki.ros.org/noetic)
- [ROS2 Humble Documentation](https://docs.ros.org/en/humble/)
- [Migration ROS1 → ROS2](https://docs.ros.org/en/humble/How-To-Guides/Migrating-from-ROS1.html)

---

**Dernière mise à jour** : Octobre 2025
