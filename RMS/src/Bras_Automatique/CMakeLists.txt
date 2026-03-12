cmake_minimum_required(VERSION 3.8)
project(bras_automatique)

if(NOT CMAKE_CXX_STANDARD)
  set(CMAKE_CXX_STANDARD 17)
endif()

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# Find dependencies
find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(std_msgs REQUIRED)
find_package(sensor_msgs REQUIRED)
find_package(geometry_msgs REQUIRED)
find_package(cv_bridge REQUIRED)
find_package(image_transport REQUIRED)
find_package(tf2 REQUIRED)
find_package(tf2_ros REQUIRED)
find_package(tf2_geometry_msgs REQUIRED)
find_package(rms_interfaces REQUIRED)
find_package(OpenCV REQUIRED)

# Common library for shared logic
add_library(bras_auto_lib
  src/Finder.cpp
)
target_include_directories(bras_auto_lib PUBLIC
  $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
  $<INSTALL_INTERFACE:include>)
ament_target_dependencies(bras_auto_lib
  "rclcpp"
  "cv_bridge"
  "OpenCV"
  "sensor_msgs"
  "geometry_msgs"
)

# Main autonomous node
add_executable(bras_automatique_node src/bras_automatique_node.cpp)
target_link_libraries(bras_automatique_node bras_auto_lib)
ament_target_dependencies(bras_automatique_node
  "rclcpp"
  "std_msgs"
  "sensor_msgs"
  "geometry_msgs"
  "cv_bridge"
  "image_transport"
  "tf2"
  "tf2_ros"
  "tf2_geometry_msgs"
  "rms_interfaces"
  "OpenCV"
)

# HSV Tuner node
add_executable(hsv_tuner_node src/hsv_tuner_node.cpp)
target_link_libraries(hsv_tuner_node bras_auto_lib)
ament_target_dependencies(hsv_tuner_node
  "rclcpp"
  "std_msgs"
  "sensor_msgs"
  "cv_bridge"
  "image_transport"
  "OpenCV"
)

# Install
install(TARGETS bras_auto_lib bras_automatique_node hsv_tuner_node
  ARCHIVE DESTINATION lib
  LIBRARY DESTINATION lib
  RUNTIME DESTINATION lib/${PROJECT_NAME}
)

install(DIRECTORY include/
  DESTINATION include/
)

install(DIRECTORY launch/
  DESTINATION share/${PROJECT_NAME}/launch
)

ament_package()
