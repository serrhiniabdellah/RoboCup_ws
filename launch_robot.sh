#!/bin/bash

echo "🤖 Démarrage du robot RoboCup en ROS1..."
echo ""

# Vérifier Docker
if ! command -v docker &> /dev/null; then
    echo "❌ Docker n'est pas installé"
    echo "   Installez Docker avec : sudo apt-get install docker.io"
    exit 1
fi

# Vérifier que Docker fonctionne
if ! docker ps &> /dev/null; then
    echo "❌ Docker n'est pas démarré ou vous n'avez pas les permissions"
    echo "   Essayez : sudo usermod -aG docker $USER"
    echo "   Puis déconnectez-vous et reconnectez-vous"
    exit 1
fi

# Autoriser X11
xhost +local:docker 2>/dev/null

# Vérifier le LIDAR
if [ ! -e /dev/ttyACM0 ]; then
    echo "⚠️  ATTENTION : LIDAR non détecté sur /dev/ttyACM0"
    echo "   Vérifiez que le LIDAR Hokuyo est branché"
    echo ""
    read -p "   Continuer quand même ? (o/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Oo]$ ]]; then
        exit 1
    fi
fi

# Lancer Docker
echo "📦 Démarrage du conteneur ROS1 Noetic..."
echo "   (Cela peut prendre quelques minutes la première fois)"
echo ""

docker run -it --rm \
  --name robocup_ros1 \
  --network host \
  --privileged \
  -v /dev:/dev \
  -v "$PWD":/workspace \
  -e DISPLAY=$DISPLAY \
  -v /tmp/.X11-unix:/tmp/.X11-unix \
  -w /workspace \
  ros:noetic-robot \
  bash -c '
    echo "📥 Installation des dépendances ROS1..."
    apt-get update -qq 2>/dev/null && apt-get install -y -qq \
      ros-noetic-cv-bridge \
      ros-noetic-image-transport \
      ros-noetic-urg-node \
      ros-noetic-hector-slam \
      ros-noetic-hector-geotiff-launch \
      ros-noetic-hector-mapping \
      ros-noetic-rviz \
      libopencv-dev \
      python3-opencv 2>/dev/null
    
    source /opt/ros/noetic/setup.bash
    
    clear
    echo "════════════════════════════════════════════════════════════"
    echo "  🤖 Robot RoboCup - ROS1 Noetic Environnement"
    echo "════════════════════════════════════════════════════════════"
    echo ""
    echo "✅ ROS1 Noetic est prêt !"
    echo ""
    echo "📂 Répertoire actuel : /workspace"
    echo "📍 Code du robot : /workspace/Robocup 2024/RaspBerry/Lidar_embarqué/ROBOCUP2024"
    echo ""
    echo "🎮 Commandes principales :"
    echo "  ┌─────────────────────────────────────────────────────────┐"
    echo "  │ 1. roscore                                   (Terminal 1)│"
    echo "  │ 2. cd \"Robocup 2024/RaspBerry/Lidar_embarqué/ROBOCUP2024\"│"
    echo "  │ 3. roslaunch ROBOCUP2024 Rescue.launch      (Terminal 2)│"
    echo "  └─────────────────────────────────────────────────────────┘"
    echo ""
    echo "🔧 Commandes utiles :"
    echo "  • rostopic list          - Lister les topics"
    echo "  • rostopic echo /scan    - Voir données LIDAR"
    echo "  • rviz                   - Visualisation 3D"
    echo "  • rqt_graph              - Graphe des noeuds"
    echo ""
    echo "⚙️  Matériel attendu :"
    echo "  • LIDAR Hokuyo sur /dev/ttyACM0"
    echo "  • (Optionnel) Caméra sur /dev/video0"
    echo ""
    echo "════════════════════════════════════════════════════════════"
    echo ""
    
    cd "/workspace/Robocup 2024/RaspBerry/Lidar_embarqué/ROBOCUP2024" 2>/dev/null || cd /workspace
    
    # Proposer de lancer directement
    echo "🚀 Voulez-vous lancer le robot maintenant ?"
    echo "   1) Oui - Lancer roscore + Rescue.launch"
    echo "   2) Non - Ouvrir un shell interactif"
    echo ""
    read -p "Choix (1/2) : " choice
    
    case $choice in
        1)
            echo ""
            echo "🎬 Lancement du robot..."
            echo ""
            # Lancer roscore en arrière-plan
            roscore &
            ROSCORE_PID=$!
            sleep 3
            
            # Vérifier que roscore fonctionne
            if ! ps -p $ROSCORE_PID > /dev/null; then
                echo "❌ Erreur : roscore na pas démarré"
                bash
                exit 1
            fi
            
            echo "✅ roscore démarré (PID: $ROSCORE_PID)"
            echo "🚀 Lancement de Rescue.launch..."
            echo ""
            
            # Lancer le robot
            cd "/workspace/Robocup 2024/RaspBerry/Lidar_embarqué/ROBOCUP2024"
            roslaunch ROBOCUP2024 Rescue.launch
            
            # Si on arrive ici, c'\''est que roslaunch s'\''est arrêté
            kill $ROSCORE_PID 2>/dev/null
            ;;
        2|*)
            echo ""
            echo "💻 Shell interactif ouvert. Bonne chance ! 🚀"
            echo ""
            bash
            ;;
    esac
  '

echo ""
echo "👋 Conteneur Docker arrêté. À bientôt !"
