cmake_minimum_required(VERSION 3.8)
project(rms_lidar)

# ═══════════════════════════════════════════════════════════════════════════
# Configuration du compilateur - Activer les warnings sanitaires
# ═══════════════════════════════════════════════════════════════════════════

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  # Flags compilateur C++ pour détection d'avertissements
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# ═══════════════════════════════════════════════════════════════════════════
# Recherche des dépendances - find_package() depuis package.xml
# ═══════════════════════════════════════════════════════════════════════════

# Framework ROS 2
find_package(ament_cmake REQUIRED)      # Build system ROS 2

# Bibliothèques ROS principales (C++)
find_package(rclcpp REQUIRED)            # Client C++ ROS 2
find_package(std_msgs REQUIRED)          # Messages types standard
find_package(sensor_msgs REQUIRED)       # Messages capteurs (Image, LaserScan)
find_package(geometry_msgs REQUIRED)     # Messages géométrie (Pose, Twist)
find_package(nav_msgs REQUIRED)          # Messages navigation

# Transformations (TF2) - Gestion des repères
find_package(tf2 REQUIRED)               # Bibliothèque transforms
find_package(tf2_ros REQUIRED)           # Interface ROS pour TF2
find_package(tf2_geometry_msgs REQUIRED) # Conversion TF2 ↔ geometry_msgs

# Traitement d'image
find_package(image_transport REQUIRED)   # Transport efficace des images
find_package(cv_bridge REQUIRED)         # Bridge OpenCV ↔ ROS messages
find_package(OpenCV REQUIRED)            # Bibliothèque OpenCV (vision)

# ═══════════════════════════════════════════════════════════════════════════
# Déclaration des variables de dépendances réutilisables
# ═══════════════════════════════════════════════════════════════════════════

# Liste des dépendances communes à tous les nœuds lidar
set(LIDAR_DEPS
  rclcpp
  std_msgs
  sensor_msgs
  geometry_msgs
  nav_msgs
  tf2
  tf2_ros
  tf2_geometry_msgs
  image_transport
  cv_bridge
)

# ═══════════════════════════════════════════════════════════════════════════
# Compilation des nœuds exécutables
# ═══════════════════════════════════════════════════════════════════════════

# ── Exploration Publisher (nœud principal navigation autonome) ──
add_executable(exploration_publisher_node
  src/Lidar/Exploration_Publisher.cpp
)
# Lier les dépendances ROS à l'exécutable
ament_target_dependencies(exploration_publisher_node ${LIDAR_DEPS})
# Lier la bibliothèque OpenCV
target_link_libraries(exploration_publisher_node ${OpenCV_LIBS})

# ── Exploration automatique intelligente ──
# Contrôle autonome optimisé du robot (IA/planification)
add_executable(exploration_auto_intelligente_node
  src/Lidar/Exploration_automatique_intelligente.cpp
)
ament_target_dependencies(exploration_auto_intelligente_node ${LIDAR_DEPS})
target_link_libraries(exploration_auto_intelligente_node ${OpenCV_LIBS})

# ── Récupération données auto (enregistrement trajectoire + manette) ──
# Enregistrement des données pour replay/apprentissage
add_executable(recuperation_data_auto_node
  src/Lidar/recuperation_data_auto.cpp
)
ament_target_dependencies(recuperation_data_auto_node ${LIDAR_DEPS})
target_link_libraries(recuperation_data_auto_node ${OpenCV_LIBS})

# ── Copie Trajet (rejeu trajectoire) ──
# Rejoue une trajectoire enregistrée précédemment
add_executable(copie_trajet_node
  src/Lidar/Copie_Trajet.cpp
)
ament_target_dependencies(copie_trajet_node ${LIDAR_DEPS})
target_link_libraries(copie_trajet_node ${OpenCV_LIBS})

# ── Rescue (prise de photos caméra pour sauvetage) ──
# Capture d'images pour enregistrement mission de secours
add_executable(rescue_node
  src/Lidar/Rescue.cpp
)
ament_target_dependencies(rescue_node ${LIDAR_DEPS})
target_link_libraries(rescue_node ${OpenCV_LIBS})

# ── Initialisation Accéléromètre ──
# Calibration et lancement du capteur MPU-9250
add_executable(init_accelero_node
  src/Lidar/Initialisation_Accelero.cpp
)
ament_target_dependencies(init_accelero_node ${LIDAR_DEPS})
target_link_libraries(init_accelero_node ${OpenCV_LIBS})

# ═══════════════════════════════════════════════════════════════════════════
# Installation des exécutables
# ═══════════════════════════════════════════════════════════════════════════

install(TARGETS
  exploration_publisher_node
  exploration_auto_intelligente_node
  recuperation_data_auto_node
  copie_trajet_node
  rescue_node
  init_accelero_node
  DESTINATION lib/${PROJECT_NAME}
)

# ═══════════════════════════════════════════════════════════════════════════
# Installation des ressources (launch files, configs)
# ═══════════════════════════════════════════════════════════════════════════

# Copier tous les fichiers .launch.py vers le répertoire install
install(DIRECTORY launch/
  DESTINATION share/${PROJECT_NAME}/launch
)

# ═══════════════════════════════════════════════════════════════════════════
# Finalisation du paquet ROS 2
# ═══════════════════════════════════════════════════════════════════════════

ament_package()  # Enregistre le paquet auprès de ROS 2
