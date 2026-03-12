cmake_minimum_required(VERSION 3.8)
project(rms_interfaces)

find_package(ament_cmake REQUIRED)
find_package(rosidl_default_generators REQUIRED)
find_package(sensor_msgs REQUIRED)
find_package(std_msgs REQUIRED)

rosidl_generate_interfaces(${PROJECT_NAME}
  "msg/DonneesComparaison.msg"
  "msg/NbPieces.msg"
  "msg/PiecesInfo.msg"
  "srv/Pas.srv"
  "srv/TraitementHSV.srv"
  DEPENDENCIES sensor_msgs std_msgs
)

ament_package()
