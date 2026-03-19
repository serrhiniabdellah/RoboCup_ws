# Message ROS 2 : Informations détaillées sur une pièce détectée
# Utilisé pour transmettre les caractéristiques géométriques et l'état d'une pièce
# dans le contexte du défi RoboCup Rescue (gestion des pièces/débris)

std_msgs/Header header           # En-tête standard ROS (timestamp, frame_id)
int32 rang                        # Classement/indice de la pièce (ordre de détection)
float32 x1                        # Coordonnée X du coin 1 du bounding box
float32 y1                        # Coordonnée Y du coin 1 du bounding box
float32 x2                        # Coordonnée X du coin 2 du bounding box
float32 y2                        # Coordonnée Y du coin 2 du bounding box
float32 x_centre                  # Coordonnée X du centre de la pièce
float32 y_centre                  # Coordonnée Y du centre de la pièce
bool jouee                        # Flag : true si la pièce a déjà été traitée/jouée
sensor_msgs/Image image           # Imagen snapshot de la pièce détectée
