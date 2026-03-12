cmake_minimum_required(VERSION 3.8)
project(rms_lidar)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# Find dependencies
find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(std_msgs REQUIRED)
find_package(sensor_msgs REQUIRED)
find_package(geometry_msgs REQUIRED)
find_package(nav_msgs REQUIRED)
find_package(tf2 REQUIRED)
find_package(tf2_ros REQUIRED)
find_package(tf2_geometry_msgs REQUIRED)
find_package(image_transport REQUIRED)
find_package(cv_bridge REQUIRED)
find_package(OpenCV REQUIRED)

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

# ── Exploration Publisher (nœud principal navigation autonome) ──
add_executable(exploration_publisher_node
  src/Lidar/Exploration_Publisher.cpp
)
ament_target_dependencies(exploration_publisher_node ${LIDAR_DEPS})
target_link_libraries(exploration_publisher_node ${OpenCV_LIBS})

# ── Exploration automatique intelligente ──
add_executable(exploration_auto_intelligente_node
  src/Lidar/Exploration_automatique_intelligente.cpp
)
ament_target_dependencies(exploration_auto_intelligente_node ${LIDAR_DEPS})
target_link_libraries(exploration_auto_intelligente_node ${OpenCV_LIBS})

# ── Récupération données auto (enregistrement trajectoire + manette) ──
add_executable(recuperation_data_auto_node
  src/Lidar/recuperation_data_auto.cpp
)
ament_target_dependencies(recuperation_data_auto_node ${LIDAR_DEPS})
target_link_libraries(recuperation_data_auto_node ${OpenCV_LIBS})

# ── Copie Trajet (rejeu trajectoire) ──
add_executable(copie_trajet_node
  src/Lidar/Copie_Trajet.cpp
)
ament_target_dependencies(copie_trajet_node ${LIDAR_DEPS})
target_link_libraries(copie_trajet_node ${OpenCV_LIBS})

# ── Rescue (prise de photos caméra) ──
add_executable(rescue_node
  src/Lidar/Rescue.cpp
)
ament_target_dependencies(rescue_node ${LIDAR_DEPS})
target_link_libraries(rescue_node ${OpenCV_LIBS})

# ── Initialisation Accéléromètre ──
add_executable(init_accelero_node
  src/Lidar/Initialisation_Accelero.cpp
)
ament_target_dependencies(init_accelero_node ${LIDAR_DEPS})
target_link_libraries(init_accelero_node ${OpenCV_LIBS})

# Install executables
install(TARGETS
  exploration_publisher_node
  exploration_auto_intelligente_node
  recuperation_data_auto_node
  copie_trajet_node
  rescue_node
  init_accelero_node
  DESTINATION lib/${PROJECT_NAME}
)

# Install launch files
install(DIRECTORY launch/
  DESTINATION share/${PROJECT_NAME}/launch
)

ament_package()
