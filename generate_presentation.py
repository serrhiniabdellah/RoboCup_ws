#!/usr/bin/env python3
"""
Génération de la présentation PPTX — Projet RoboCup RMS
Interface IHM + Intégration de tous les modules
"""

from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.util import Cm
import copy

# ─────────────────────────────────────────────
# PALETTE
# ─────────────────────────────────────────────
DARK_BG    = RGBColor(0x05, 0x05, 0x1A)   # Fond sombre bleu nuit
ACCENT     = RGBColor(0x00, 0xE5, 0xFF)   # Cyan vif
ACCENT2    = RGBColor(0x00, 0x96, 0xC0)   # Cyan foncé
WHITE      = RGBColor(0xFF, 0xFF, 0xFF)
LIGHT_GRAY = RGBColor(0xCC, 0xCC, 0xCC)
MEDIUM_GRAY= RGBColor(0x44, 0x44, 0x66)
DARK_CARD  = RGBColor(0x0D, 0x0D, 0x2E)   # Fond carte

prs = Presentation()
prs.slide_width  = Inches(13.33)
prs.slide_height = Inches(7.5)


# ─────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────

def blank_slide():
    layout = prs.slide_layouts[6]  # entièrement vide
    return prs.slides.add_slide(layout)


def fill_bg(slide, color=DARK_BG):
    fill = slide.background.fill
    fill.solid()
    fill.fore_color.rgb = color


def add_rect(slide, l, t, w, h, color, transparency=0):
    shape = slide.shapes.add_shape(1, Inches(l), Inches(t), Inches(w), Inches(h))
    shape.line.fill.background()
    shape.fill.solid()
    shape.fill.fore_color.rgb = color
    if transparency:
        shape.fill.fore_color.transparency = transparency
    return shape


def add_text(slide, text, l, t, w, h,
             size=18, bold=False, color=WHITE,
             align=PP_ALIGN.LEFT, wrap=True):
    txb = slide.shapes.add_textbox(Inches(l), Inches(t), Inches(w), Inches(h))
    txb.word_wrap = wrap
    tf = txb.text_frame
    tf.word_wrap = wrap
    p = tf.paragraphs[0]
    p.alignment = align
    run = p.add_run()
    run.text = text
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.color.rgb = color
    return txb


def add_multiline(slide, lines, l, t, w, h,
                  size=13, color=WHITE, line_spacing=1.2):
    """lines: list of (text, bold, color_override)"""
    txb = slide.shapes.add_textbox(Inches(l), Inches(t), Inches(w), Inches(h))
    txb.word_wrap = True
    tf = txb.text_frame
    tf.word_wrap = True
    first = True
    for (txt, bold, col) in lines:
        p = tf.paragraphs[0] if first else tf.add_paragraph()
        first = False
        p.space_after  = Pt(2)
        run = p.add_run()
        run.text = txt
        run.font.size = Pt(size)
        run.font.bold = bold
        run.font.color.rgb = col or color
    return txb


def accent_bar(slide, y=0.55, h=0.06):
    """Barre d'accent horizontale sous le titre"""
    add_rect(slide, 0.5, y, 12.33, h, ACCENT)


def slide_title(slide, title, subtitle=None):
    """Titre + sous-titre standard en haut"""
    add_rect(slide, 0, 0, 13.33, 0.5, DARK_CARD)
    add_text(slide, title, 0.4, 0.05, 12, 0.45,
             size=22, bold=True, color=ACCENT, align=PP_ALIGN.LEFT)
    accent_bar(slide)
    if subtitle:
        add_text(slide, subtitle, 0.4, 0.62, 12, 0.35,
                 size=13, bold=False, color=LIGHT_GRAY, align=PP_ALIGN.LEFT)


def card(slide, l, t, w, h, title, body_lines, icon=""):
    """Carte info avec titre coloré et liste de points"""
    add_rect(slide, l, t, w, h, DARK_CARD)
    # Bord gauche coloré
    add_rect(slide, l, t, 0.06, h, ACCENT)
    add_text(slide, f"{icon}  {title}" if icon else title,
             l+0.12, t+0.08, w-0.2, 0.32,
             size=13, bold=True, color=ACCENT, align=PP_ALIGN.LEFT)
    lines = [(f"• {b}" if not b.startswith("•") else b, False, LIGHT_GRAY) for b in body_lines]
    add_multiline(slide, lines, l+0.16, t+0.42, w-0.28, h-0.55, size=11, color=LIGHT_GRAY)


# ══════════════════════════════════════════════════════
#   SLIDE 1 — COUVERTURE
# ══════════════════════════════════════════════════════
s = blank_slide()
fill_bg(s)
add_rect(s, 0, 0, 13.33, 0.8, DARK_CARD)
add_rect(s, 0, 0.8, 0.12, 6.7, ACCENT)  # barre verticale gauche

add_text(s, "RoboCup Rescue — Projet RMS",
         0.4, 0.1, 12, 0.6, size=32, bold=True, color=ACCENT, align=PP_ALIGN.CENTER)

add_text(s, "Interface IHM & Intégration Globale du Système",
         0.4, 1.1, 12, 0.5, size=22, bold=True, color=WHITE, align=PP_ALIGN.CENTER)

add_text(s, "Robot Management System — ROS 2 Jazzy",
         0.4, 1.75, 12, 0.4, size=16, bold=False, color=LIGHT_GRAY, align=PP_ALIGN.CENTER)

# Séparateur
add_rect(s, 3.5, 2.3, 6.3, 0.05, ACCENT)

add_text(s, "📡  LIDAR  |  🦾  Bras  |  📷  Caméra  |  🕹️  IHM  |  🤖  Navigation",
         0.4, 2.5, 12, 0.5, size=14, bold=False, color=ACCENT2, align=PP_ALIGN.CENTER)

add_rect(s, 0, 6.8, 13.33, 0.7, DARK_CARD)
add_text(s, "IATIC4 — Groupe RMS — 2024 / 2025   |   UVSQ",
         0.4, 6.88, 12, 0.4, size=12, color=LIGHT_GRAY, align=PP_ALIGN.CENTER)


# ══════════════════════════════════════════════════════
#   SLIDE 2 — PLAN
# ══════════════════════════════════════════════════════
s = blank_slide()
fill_bg(s)
slide_title(s, "Plan de la présentation")

sections = [
    ("01", "Présentation du projet RMS",        "Contexte, objectifs et architecture générale"),
    ("02", "Architecture du système",            "Modules ROS 2, interfaces et communication"),
    ("03", "Module Navigation & LIDAR",          "Exploration, cartographie, détection d'obstacles"),
    ("04", "Module Bras Robotique",              "Contrôle automatique et manuel"),
    ("05", "Module Vision (Caméra)",             "Flux vidéo, traitement HSV, QR Code"),
    ("06", "Module Interface IHM",               "Dashboard Web, rosbridge, contrôle robot"),
    ("07", "Intégration & Tests",                "ROS 2, launch files, simulation Docker"),
    ("08", "Conclusion & Perspectives",          "Résultats, améliorations futures"),
]

for i, (num, title, desc) in enumerate(sections):
    col = i % 2
    row = i // 2
    l = 0.4 + col * 6.5
    t = 0.9 + row * 1.45
    add_rect(s, l, t, 6.2, 1.3, DARK_CARD)
    add_rect(s, l, t, 0.55, 1.3, ACCENT)
    add_text(s, num, l+0.07, t+0.38, 0.45, 0.5, size=18, bold=True, color=DARK_BG, align=PP_ALIGN.CENTER)
    add_text(s, title, l+0.65, t+0.1, 5.45, 0.42, size=13, bold=True, color=WHITE)
    add_text(s, desc,  l+0.65, t+0.58, 5.45, 0.62, size=11, color=LIGHT_GRAY)


# ══════════════════════════════════════════════════════
#   SLIDE 3 — PRÉSENTATION DU PROJET
# ══════════════════════════════════════════════════════
s = blank_slide()
fill_bg(s)
slide_title(s, "01 — Présentation du projet RMS",
            "Robot d'assistance en mission Rescue (Sauvetage) — Compétition RoboCup 2024")

add_text(s, "Contexte", 0.4, 1.05, 5.8, 0.35, size=15, bold=True, color=ACCENT)
add_multiline(s, [
    ("La compétition RoboCup Rescue met en scène des robots autonomes et semi-autonomes capables de naviguer dans des environnements sinistrés pour localiser des victimes.", False, LIGHT_GRAY),
    ("", False, LIGHT_GRAY),
    ("Notre robot est équipé d'un LIDAR, d'une caméra, de flippers, d'un bras robotique et d'un accéléromètre, tous coordonnés via ROS 2.", False, LIGHT_GRAY),
], 0.4, 1.42, 5.8, 2.3, size=12, color=LIGHT_GRAY)

add_text(s, "Objectifs", 7.1, 1.05, 5.8, 0.35, size=15, bold=True, color=ACCENT)
objectives = [
    "🗺️  Navigation autonome et cartographie LIDAR",
    "🦾  Contrôle précis du bras robotique",
    "📷  Surveillance vidéo en temps réel",
    "🕹️  Interface de pilotage à distance (IHM Web)",
    "📱  Application Android de supervision",
    "🔗  Intégration complète sous ROS 2 Jazzy",
]
for j, obj in enumerate(objectives):
    add_text(s, obj, 7.1, 1.42 + j*0.48, 5.8, 0.45, size=12, color=LIGHT_GRAY)

add_rect(s, 0, 6.9, 13.33, 0.6, DARK_CARD)
add_text(s, "Technologie : ROS 2 Jazzy  ●  C++17  ●  Python 3  ●  WebSocket / roslibjs  ●  Docker  ●  Kotlin (Android)",
         0.4, 6.96, 12, 0.4, size=11, color=ACCENT2, align=PP_ALIGN.CENTER)


# ══════════════════════════════════════════════════════
#   SLIDE 4 — ARCHITECTURE GLOBALE
# ══════════════════════════════════════════════════════
s = blank_slide()
fill_bg(s)
slide_title(s, "02 — Architecture du système",
            "Tous les modules communiquent via des topics et services ROS 2")

modules = [
    ("LIDAR",      "rms_lidar",       "sensor_msgs/LaserScan\n/scan"),
    ("Navigation", "rms_navigation",  "nav_msgs/OccupancyGrid\n/map"),
    ("Caméra",     "rms_camera",      "sensor_msgs/CompressedImage\n/cv_camera/image_raw/compressed"),
    ("Bras Auto",  "rms_bras_auto",   "std_msgs/Int16MultiArray\n/choix_pos"),
    ("Bras Manuel","rms_bras_manuel", "sensor_msgs/Joy\n/joy_ihm"),
    ("Accéléro",   "rms_accelero",    "std_msgs/Int32\n/inclinaison1, /inclinaison2"),
    ("IHM Web",    "rosbridge",       "WebSocket ws://robot:9090"),
    ("Android App","RoboCup App",     "API REST / rosbridge"),
]

cols = 4
for i, (name, pkg, topics) in enumerate(modules):
    col = i % cols
    row = i // cols
    l = 0.3 + col * 3.25
    t = 1.0 + row * 2.0
    add_rect(s, l, t, 3.0, 1.8, DARK_CARD)
    add_rect(s, l, t, 3.0, 0.38, ACCENT)
    add_text(s, name, l+0.1, t+0.04, 2.8, 0.32, size=13, bold=True, color=DARK_BG, align=PP_ALIGN.CENTER)
    add_text(s, pkg,  l+0.1, t+0.42, 2.8, 0.32, size=10, bold=True, color=ACCENT, align=PP_ALIGN.CENTER)
    add_text(s, topics, l+0.12, t+0.78, 2.78, 0.9, size=9.5, color=LIGHT_GRAY, align=PP_ALIGN.CENTER)

# Flèche centrale (texte)
add_text(s, "⟷  Communication inter-modules via DDS (ROS 2)",
         0.4, 5.05, 12.5, 0.4, size=13, bold=True, color=ACCENT, align=PP_ALIGN.CENTER)
add_rect(s, 0.5, 5.48, 12.33, 0.05, ACCENT2)
add_text(s, "rms_interfaces : messages et services partagés entre tous les nodes",
         0.4, 5.6, 12.5, 0.35, size=12, color=LIGHT_GRAY, align=PP_ALIGN.CENTER)


# ══════════════════════════════════════════════════════
#   SLIDE 5 — LIDAR & NAVIGATION
# ══════════════════════════════════════════════════════
s = blank_slide()
fill_bg(s)
slide_title(s, "03 — Module Navigation & LIDAR",
            "Exploration automatique, cartographie Hector SLAM et détection d'obstacles")

card(s, 0.35, 1.0, 3.8, 2.4, "Capteur", [
    "Hokuyo UST-10LX (LIDAR 2D)",
    "Driver : urg_node2 (ROS 2)",
    "Plage : 0.06 m → 10 m",
    "Fréquence : 25 Hz / 270°",
    "Topic : /scan → LaserScan",
], "📡")

card(s, 4.35, 1.0, 3.8, 2.4, "Cartographie", [
    "Hector Mapping (SLAM sans odométrie)",
    "Topic sortie : /map (OccupancyGrid)",
    "Sauvegarde GeoTIFF via hector_geotiff",
    "Launch : hector_mapping.launch.py",
], "🗺️")

card(s, 8.35, 1.0, 4.6, 2.4, "Exploration Intelligente", [
    "Exploration automatique (Frontier-based)",
    "Exploration_Publisher.cpp",
    "Arrêt si obstacle < seuil",
    "Récupération des données auto",
    "Mode Rescue.cpp : priorité sauvetage",
], "🤖")

card(s, 0.35, 3.65, 5.45, 2.5, "Launch Lidar.launch.py", [
    "Lance urg_node2 pour le LIDAR",
    "Lance hector_mapping pour la carte",
    "Lance hector_geotiff pour l'export",
    "Configurable : port USB, IP robot",
    "Mode Docker ou natif ROS 2",
], "⚙️")

card(s, 6.0, 3.65, 6.9, 2.5, "Visualisation IHM — Canvas LIDAR", [
    "Page vision_lidar.html dans l'IHM Web",
    "Abonné au topic /scan via roslibjs",
    "Dessin HTML5 Canvas en temps réel",
    "Couleurs dynamiques : rouge=proche / vert=loin",
    "Cercles de distance + labels AVANT/ARRIÈRE",
    "Compteur de points valides en temps réel",
], "📡")


# ══════════════════════════════════════════════════════
#   SLIDE 6 — BRAS ROBOTIQUE
# ══════════════════════════════════════════════════════
s = blank_slide()
fill_bg(s)
slide_title(s, "04 — Module Bras Robotique",
            "Contrôle automatique (trajectoires pré-définies) + Manuel (IHM sliders)")

card(s, 0.35, 1.0, 6.0, 2.7, "Bras Automatique", [
    "Package : rms_bras_automatique",
    "Positions pré-définies : Rangement, Déploiement, Haute",
    "Service ROS 2 : /bras_position",
    "C++ : BrasAutomatique.cpp",
    "Retour de position via feedback topic",
    "Intégré au launch Rescue.launch",
], "🦾")

card(s, 6.55, 1.0, 6.4, 2.7, "Bras Manuel — IHM", [
    "Page deplacement_bras.html",
    "6 sliders : X, Y, Z (déplacements) + RX, RY, RZ (rotations)",
    "Publié sur /choix_pos (Int16MultiArray)",
    "Boutons rapides : Rangement / Déploiement / Position haute",
    "Valeurs persistées entre actions (objet sliderValues)",
    "Clavier configurable à venir",
], "🎮")

add_text(s, "Flux de contrôle du bras", 0.35, 3.9, 12.5, 0.35, size=15, bold=True, color=ACCENT)
add_rect(s, 0.35, 4.3, 12.6, 0.05, MEDIUM_GRAY)

steps = [
    ("IHM Web\n(sliders)", "publier\n/choix_pos"),
    ("Node Bras\n(ROS 2)", "commandes\nservo"),
    ("Contrôleur\nSabre/PWM", "mouvement\nmoteurs"),
    ("Feedback\nPosition", "topic\n/bras_retour"),
]
for i, (box, arrow) in enumerate(steps):
    lx = 0.4 + i * 3.2
    add_rect(s, lx, 4.5, 2.5, 1.5, DARK_CARD)
    add_rect(s, lx, 4.5, 2.5, 0.35, ACCENT)
    add_text(s, box, lx+0.1, 4.53, 2.3, 0.3, size=11, bold=True, color=DARK_BG, align=PP_ALIGN.CENTER)
    add_text(s, arrow, lx+0.1, 4.95, 2.3, 0.9, size=10, color=LIGHT_GRAY, align=PP_ALIGN.CENTER)
    if i < 3:
        add_text(s, "→", lx+2.57, 5.05, 0.55, 0.5, size=20, bold=True, color=ACCENT, align=PP_ALIGN.CENTER)


# ══════════════════════════════════════════════════════
#   SLIDE 7 — CAMÉRA & VISION
# ══════════════════════════════════════════════════════
s = blank_slide()
fill_bg(s)
slide_title(s, "05 — Module Vision (Caméra & QR Code)",
            "Flux vidéo temps réel, traitement HSV, détection QR Code")

card(s, 0.35, 1.0, 4.0, 2.6, "Caméra Économique", [
    "Package : rms_camera_economique",
    "Driver : cv_camera (OpenCV → ROS 2)",
    "Topic : /cv_camera/image_raw/compressed",
    "Format : CompressedImage (JPEG)",
    "Calibration HSV via service ROS 2",
    "Résolution configurable",
], "📷")

card(s, 4.55, 1.0, 4.0, 2.6, "QR Code", [
    "Package : rms_qrcode",
    "Bibliothèque : ZBar / OpenCV",
    "Décode les QR Codes en temps réel",
    "Publie le contenu sur /qrcode_data",
    "Utile pour identifier les victimes",
    "Intégré dans le pipeline Rescue",
], "📱")

card(s, 8.75, 1.0, 4.2, 2.6, "Détection Mouvement", [
    "Package : rms_detection_mouvement",
    "Analyse de flux caméra frame à frame",
    "Soustraction de fond (BackgroundSubtractor)",
    "Topic : /mouvement_detecte (Bool)",
    "Déclenche une alarme sur l'IHM",
], "👁️")

card(s, 0.35, 3.8, 7.5, 2.55, "Visualisation Caméra — IHM Web", [
    "Page vision_camera.html dans le dashboard",
    "Abonnée au topic /cv_camera/image_raw/compressed via roslib.js",
    "Affichage de l'image Base64 dans un <img> (id unique)",
    "Message 'En attente du flux...' si aucune image reçue",
    "Indicateur 🟢/🔴 de connexion ROS en temps réel",
], "🖥️")

card(s, 8.05, 3.8, 4.9, 2.55, "Caméra 8MP", [
    "Package : rms_flux_8mp",
    "Caméra haute résolution Pi Camera v2",
    "Flux MJPEG haute qualité",
    "Launch : Flux_8MP.launch",
    "Utilisée pour l'inspection fine",
], "🎥")


# ══════════════════════════════════════════════════════
#   SLIDE 8 — IHM WEB (DÉTAIL)
# ══════════════════════════════════════════════════════
s = blank_slide()
fill_bg(s)
slide_title(s, "06 — Module Interface IHM (détail)",
            "Dashboard Web 4 panneaux — ROS bridge WebSocket — roslibjs")

# Schéma central
add_rect(s, 4.7, 0.85, 4.0, 0.85, DARK_CARD)
add_rect(s, 4.7, 0.85, 4.0, 0.28, ACCENT)
add_text(s, "index.html — Dashboard", 4.8, 0.88, 3.8, 0.26, size=12, bold=True,
         color=DARK_BG, align=PP_ALIGN.CENTER)
add_text(s, "4 iframes : Robot | LIDAR | Caméra | Bras",
         4.8, 1.18, 3.8, 0.45, size=10, color=LIGHT_GRAY, align=PP_ALIGN.CENTER)

panels = [
    (0.35, 2.0, "🕹️ Déplacement\nRobot", "deplacement_robot.html\n/joy_ihm (Joy)"),
    (3.65, 2.0, "📡 Vision\nLIDAR",        "vision_lidar.html\n/scan (LaserScan) + Canvas"),
    (6.95, 2.0, "📷 Caméra",               "vision_camera.html\n/cv_camera/.../compressed"),
    (10.25, 2.0,"🦾 Bras",                "deplacement_bras.html\n/choix_pos (Int16MultiArray)"),
]
for (l, t, name, desc) in panels:
    add_rect(s, l, t, 2.9, 2.2, DARK_CARD)
    add_rect(s, l, t, 2.9, 0.45, ACCENT)
    add_text(s, name, l+0.1, t+0.04, 2.7, 0.4, size=11, bold=True,
             color=DARK_BG, align=PP_ALIGN.CENTER)
    add_text(s, desc, l+0.12, t+0.55, 2.68, 1.55, size=10,
             color=LIGHT_GRAY, align=PP_ALIGN.CENTER)

# Flèche de connexion
add_text(s, "rosbridge_server", 5.3, 4.35, 2.8, 0.35, size=13, bold=True, color=ACCENT, align=PP_ALIGN.CENTER)
add_rect(s, 5.3, 4.72, 2.8, 0.05, ACCENT)
add_text(s, "ws://robot_ip:9090", 5.3, 4.8, 2.8, 0.35, size=11, color=LIGHT_GRAY, align=PP_ALIGN.CENTER)

corrections = [
    "✅  Subscribers 2→5 corrigés (plus de duplicates subscriber1.subscribe())",
    "✅  Nom JS corrigé : vision-lidar.js → vision_lidar.js",
    "✅  IDs HTML uniques dans vision_camera.html (un seul id='image_sub')",
    "✅  Éléments DOM telémétrie ajoutés : vitesse1/2, inclinaison1/2, boussole",
    "✅  IP robot configurable dynamiquement via localStorage",
    "✅  Indicateurs connexion ROS 🟢/🔴 sur toutes les pages",
]
add_text(s, "Corrections apportées :", 0.35, 5.3, 12.5, 0.3, size=13, bold=True, color=ACCENT)
for j, c in enumerate(corrections):
    add_text(s, c, 0.35, 5.65 + j*0.3, 12.5, 0.28, size=11, color=LIGHT_GRAY)


# ══════════════════════════════════════════════════════
#   SLIDE 9 — ACCÉLÉROMÈTRE & INTÉGRATION RESCUE
# ══════════════════════════════════════════════════════
s = blank_slide()
fill_bg(s)
slide_title(s, "07 — Intégration & Tests",
            "Rescue.launch, Docker, Accéléromètre, Application Android")

card(s, 0.35, 1.0, 3.9, 2.5, "Accéléromètre", [
    "Package : rms_accelerometre",
    "Topics : /inclinaison1, /inclinaison2",
    "Mesure l'inclinaison du robot",
    "Utile pour flippers adaptatifs",
    "Affiché en temps réel sur l'IHM",
    "Init : Init_Accelero.launch",
], "📐")

card(s, 4.45, 1.0, 4.2, 2.5, "Rescue.launch — Intégration", [
    "Lance tous les nodes en une commande",
    "urg_node2 + hector_mapping + cv_camera",
    "Bras automatique + Déplacement",
    "rosbridge pour l'IHM Web",
    "Configurable par paramètres YAML",
], "🚀")

card(s, 8.85, 1.0, 4.1, 2.5, "Application Android", [
    "Projet : RoboCup_app-main (Kotlin)",
    "Interface de supervision tactile",
    "Connexion via rosbridge WebSocket",
    "Vue état du robot + caméra",
    "Compatible tablette / téléphone Android",
], "📱")

# Docker section
add_rect(s, 0.35, 3.7, 12.6, 2.55, DARK_CARD)
add_rect(s, 0.35, 3.7, 12.6, 0.36, ACCENT2)
add_text(s, "Environnement Docker — Développement et Test",
         0.5, 3.72, 12.3, 0.3, size=13, bold=True, color=DARK_BG)

docker_steps = [
    ("1. Lancer Docker", "docker run -it \\\n-v $(pwd)/RMS:/ros2_ws/src/RMS \\\nosrf/ros:jazzy-desktop bash"),
    ("2. Installer dépendances", "apt install ros-jazzy-urg-node2\nros-jazzy-diagnostic-updater\nrosdep install ..."),
    ("3. Compiler", "cd /ros2_ws\ncolcon build \\\n--packages-select urg_node2 rms_lidar"),
    ("4. Lancer", "source install/setup.bash\nros2 launch rms_lidar\n  Lidar.launch.py"),
]
for i, (title, cmd) in enumerate(docker_steps):
    lx = 0.5 + i * 3.17
    add_text(s, title, lx, 4.15, 3.0, 0.3, size=11, bold=True, color=ACCENT)
    add_rect(s, lx, 4.5, 2.9, 1.6, RGBColor(0x03, 0x03, 0x12))
    add_text(s, cmd, lx+0.1, 4.58, 2.75, 1.5, size=9.5, color=RGBColor(0xA0, 0xFF, 0xA0))


# ══════════════════════════════════════════════════════
#   SLIDE 10 — CONCLUSION
# ══════════════════════════════════════════════════════
s = blank_slide()
fill_bg(s)
slide_title(s, "08 — Conclusion & Perspectives")

add_text(s, "Ce qui a été réalisé", 0.4, 0.95, 6.2, 0.35, size=15, bold=True, color=ACCENT)
done = [
    "✅  Interface IHM Web complète (Dashboard 4 panneaux)",
    "✅  Visualiseur LIDAR en temps réel (Canvas HTML5)",
    "✅  Correction de tous les bugs de l'interface",
    "✅  Navigation autonome avec Hector SLAM",
    "✅  Contrôle du bras (automatique + manuel)",
    "✅  Flux caméra + détection QR Code",
    "✅  Déploiement Docker + ROS 2 Jazzy",
    "✅  Application Android de supervision",
]
for j, d in enumerate(done):
    add_text(s, d, 0.5, 1.35 + j*0.46, 6.0, 0.42, size=12, color=LIGHT_GRAY)

add_text(s, "Perspectives d'amélioration", 7.2, 0.95, 5.7, 0.35, size=15, bold=True, color=ACCENT)
future = [
    "🔮  Navigation 3D avec LIDAR 3D",
    "🔮  Détection et localisation de victimes (IA)",
    "🔮  Interface mobile améliorée (PWA)",
    "🔮  Contrôle du robot via joystick physique",
    "🔮  Mapping en temps réel affiché dans l'IHM",
    "🔮  Communication multi-robots",
]
for j, f in enumerate(future):
    add_text(s, f, 7.2, 1.35 + j*0.46, 5.7, 0.42, size=12, color=LIGHT_GRAY)

add_rect(s, 0, 6.2, 13.33, 1.3, DARK_CARD)
add_rect(s, 0, 6.2, 13.33, 0.07, ACCENT)
add_text(s, "Merci pour votre attention — Questions ?",
         0.4, 6.35, 12.5, 0.5, size=22, bold=True, color=ACCENT, align=PP_ALIGN.CENTER)
add_text(s, "Groupe RMS — IATIC4 — UVSQ  |  RoboCup Rescue 2025",
         0.4, 6.85, 12.5, 0.35, size=12, color=LIGHT_GRAY, align=PP_ALIGN.CENTER)


# ─────────────────────────────────────────────
# SAUVEGARDE
# ─────────────────────────────────────────────
OUTPUT = "/home/ser/RoboCup_ws/Présentation_RMS_Interface.pptx"
prs.save(OUTPUT)
print(f"✅  Présentation générée : {OUTPUT}")
print(f"    Slides : {len(prs.slides)}")
