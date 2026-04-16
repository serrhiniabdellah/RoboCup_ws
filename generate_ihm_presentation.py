#!/usr/bin/env python3
"""
Présentation PPTX dédiée — Interface IHM RoboCup RMS
"""

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN

# ── Palette ──────────────────────────────────────────
DARK_BG    = RGBColor(0x05, 0x05, 0x1A)
DARK_CARD  = RGBColor(0x0D, 0x0D, 0x30)
ACCENT     = RGBColor(0x00, 0xE5, 0xFF)
ACCENT2    = RGBColor(0x00, 0x88, 0xAA)
WHITE      = RGBColor(0xFF, 0xFF, 0xFF)
LIGHT      = RGBColor(0xCC, 0xCC, 0xDD)
GREEN      = RGBColor(0x4C, 0xAF, 0x50)
RED        = RGBColor(0xF4, 0x43, 0x36)
ORANGE     = RGBColor(0xFF, 0x98, 0x00)
PURPLE     = RGBColor(0xAB, 0x47, 0xBC)

prs = Presentation()
prs.slide_width  = Inches(13.33)
prs.slide_height = Inches(7.5)


# ── Helpers ───────────────────────────────────────────

def blank_slide():
    return prs.slides.add_slide(prs.slide_layouts[6])

def bg(slide, color=DARK_BG):
    f = slide.background.fill
    f.solid()
    f.fore_color.rgb = color

def rect(slide, l, t, w, h, color):
    s = slide.shapes.add_shape(1,
        Inches(l), Inches(t), Inches(w), Inches(h))
    s.line.fill.background()
    s.fill.solid()
    s.fill.fore_color.rgb = color
    return s

def txt(slide, text, l, t, w, h,
        size=12, bold=False, color=WHITE,
        align=PP_ALIGN.LEFT, italic=False):
    tb = slide.shapes.add_textbox(Inches(l), Inches(t), Inches(w), Inches(h))
    tb.word_wrap = True
    tf = tb.text_frame
    tf.word_wrap = True
    p  = tf.paragraphs[0]
    p.alignment = align
    r  = p.add_run()
    r.text = text
    r.font.size   = Pt(size)
    r.font.bold   = bold
    r.font.italic = italic
    r.font.color.rgb = color
    return tb

def multi(slide, lines, l, t, w, h, default_size=11, default_color=LIGHT):
    """lines = list of (text, size, bold, color)"""
    tb = slide.shapes.add_textbox(Inches(l), Inches(t), Inches(w), Inches(h))
    tb.word_wrap = True
    tf = tb.text_frame
    tf.word_wrap = True
    for i, (text, size, bold, color) in enumerate(lines):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.space_after = Pt(3)
        r = p.add_run()
        r.text = text
        r.font.size  = Pt(size or default_size)
        r.font.bold  = bold
        r.font.color.rgb = color or default_color

def header(slide, title, sub=None):
    rect(slide, 0, 0, 13.33, 0.58, DARK_CARD)
    rect(slide, 0, 0.58, 13.33, 0.055, ACCENT)
    txt(slide, title, 0.35, 0.06, 12.6, 0.5,
        size=22, bold=True, color=ACCENT, align=PP_ALIGN.LEFT)
    if sub:
        txt(slide, sub, 0.35, 0.65, 12.6, 0.32,
            size=12, color=LIGHT, align=PP_ALIGN.LEFT)

def card(slide, l, t, w, h, title, icon, body, title_color=ACCENT):
    rect(slide, l, t, w, h, DARK_CARD)
    rect(slide, l, t, 0.07, h, title_color)
    txt(slide, f"{icon}  {title}", l+0.14, t+0.07,
        w-0.2, 0.32, size=12, bold=True, color=title_color)
    multi(slide,
          [(f"• {b}", 10, False, LIGHT) for b in body],
          l+0.14, t+0.42, w-0.2, h-0.5)

def code_block(slide, code, l, t, w, h):
    rect(slide, l, t, w, h, RGBColor(0x02, 0x02, 0x10))
    txt(slide, code, l+0.1, t+0.08, w-0.15, h-0.1,
        size=9.5, color=RGBColor(0x80, 0xFF, 0x80), italic=False)

def badge(slide, text, l, t, w, h, color=ACCENT):
    rect(slide, l, t, w, h, color)
    txt(slide, text, l+0.05, t+0.04, w-0.08, h-0.06,
        size=9.5, bold=True, color=DARK_BG, align=PP_ALIGN.CENTER)


# ══════════════════════════════════════════════════════
#  SLIDE 1 — COUVERTURE
# ══════════════════════════════════════════════════════
s = blank_slide()
bg(s)

# Barre gauche verticale
rect(s, 0, 0, 0.18, 7.5, ACCENT)

txt(s, "Interface IHM",
    0.5, 0.7, 12, 0.85, size=54, bold=True, color=ACCENT, align=PP_ALIGN.LEFT)
txt(s, "RoboCup Rescue — Robot Management System",
    0.5, 1.65, 12, 0.5, size=22, bold=False, color=WHITE, align=PP_ALIGN.LEFT)

rect(s, 0.5, 2.35, 8, 0.055, ACCENT)

txt(s, "Dashboard Web  ·  LIDAR Canvas  ·  Caméra  ·  Bras  ·  rosbridge",
    0.5, 2.5, 12, 0.45, size=14, color=LIGHT, align=PP_ALIGN.LEFT)

# Badges techno
techs = ["HTML5", "CSS3", "JavaScript", "roslibjs", "ROS 2 Jazzy", "WebSocket"]
for i, t in enumerate(techs):
    badge(s, t, 0.5 + i*1.85, 3.15, 1.7, 0.38, ACCENT2)

rect(s, 0, 6.85, 13.33, 0.65, DARK_CARD)
txt(s, "IATIC4 — Groupe RMS — UVSQ  ·  2024 / 2025",
    0.4, 6.93, 12.5, 0.4, size=12, color=LIGHT, align=PP_ALIGN.CENTER)


# ══════════════════════════════════════════════════════
#  SLIDE 2 — PLAN
# ══════════════════════════════════════════════════════
s = blank_slide()
bg(s)
header(s, "Plan de la présentation")

items = [
    ("01", "Contexte & Rôle de l'IHM",         "Pourquoi une interface web dans la boucle de contrôle ?"),
    ("02", "Architecture Technique",             "rosbridge, roslibjs, WebSocket, flux de données"),
    ("03", "Dashboard — index.html",             "Vue d'ensemble 4 panneaux, configuration IP"),
    ("04", "Page Déplacement Robot",             "Contrôle clavier/boutons, flippers, caméra orientable"),
    ("05", "Page Visualisation LIDAR",           "Canvas HTML5, abonnement /scan, rendu polaire"),
    ("06", "Page Caméra",                        "Flux caméra temps réel, topic CompressedImage"),
    ("07", "Page Contrôle Bras",                 "Sliders 6 axes, positions pré-définies ROS 2"),
    ("08", "Bugs corrigés & Améliorations",      "Corrections critiques, indicateurs de connexion"),
    ("09", "Démo & Lancement",                   "Commandes, URL, simulation sans robot"),
]

cols = 3
for i, (num, title, desc) in enumerate(items):
    col = i % cols
    row = i // cols
    l = 0.3 + col * 4.37
    t = 0.98 + row * 2.1
    rect(s, l, t, 4.15, 1.9, DARK_CARD)
    badge(s, num, l, t, 0.62, 1.9, ACCENT)
    txt(s, title, l+0.72, t+0.12, 3.32, 0.45, size=12, bold=True, color=WHITE)
    txt(s, desc,  l+0.72, t+0.6,  3.32, 1.2,  size=10, color=LIGHT)


# ══════════════════════════════════════════════════════
#  SLIDE 3 — CONTEXTE & RÔLE
# ══════════════════════════════════════════════════════
s = blank_slide()
bg(s)
header(s, "01 — Contexte & Rôle de l'IHM",
       "L'interface permet aux opérateurs de piloter le robot à distance, sans RViz ni terminal")

card(s, 0.35, 1.0, 5.9, 2.6, "Problème résolu", "🎯", [
    "Le robot RMS tourne sous ROS 2 — inaccessible directement depuis un navigateur",
    "Besoin d'une interface légère, accessible depuis n'importe quel appareil sur le même réseau",
    "Pas de dépendance à RViz, pas de ROS côté client",
    "Fonctionner sur tablette Android ou PC pendant la compétition",
], ACCENT)

card(s, 6.45, 1.0, 6.5, 2.6, "Solution : IHM Web + rosbridge", "💡", [
    "rosbridge_server expose les topics ROS 2 en WebSocket",
    "roslibjs (JavaScript) s'y connecte depuis le navigateur",
    "L'opérateur ouvre simplement un navigateur en http://robot_ip:8080",
    "Fonctionne sur ordinateur, tablette, téléphone",
    "Aucune installation côté client requise",
], GREEN)

# Schéma flèches
nodes = ["Navigateur\n(IHM Web)", "WebSocket\nws://ip:9090", "rosbridge\nserver", "Topics\nROS 2", "Robot\n(hardware)"]
colors = [ACCENT, ACCENT2, GREEN, ORANGE, PURPLE]
for i, (n, c) in enumerate(zip(nodes, colors)):
    lx = 0.5 + i * 2.52
    rect(s, lx, 3.82, 2.1, 1.5, DARK_CARD)
    rect(s, lx, 3.82, 2.1, 0.3, c)
    txt(s, n, lx+0.08, 3.85, 1.95, 0.28, size=9, bold=True,
        color=DARK_BG, align=PP_ALIGN.CENTER)
    txt(s, "ws" if i == 1 else "API", lx+0.08, 4.2, 1.95, 0.9,
        size=10, color=LIGHT, align=PP_ALIGN.CENTER)
    if i < 4:
        txt(s, "→", lx + 2.16, 4.35, 0.3, 0.5, size=20, bold=True, color=ACCENT, align=PP_ALIGN.CENTER)

txt(s, "Protocole de bout en bout :", 0.35, 5.52, 12.5, 0.3, size=12, bold=True, color=ACCENT)
code_block(s,
    "Navigateur  ──[WebSocket]──►  rosbridge_server  ──[DDS]──►  Node ROS 2  ──►  Hardware",
    0.35, 5.88, 12.6, 0.65)


# ══════════════════════════════════════════════════════
#  SLIDE 4 — ARCHITECTURE TECHNIQUE
# ══════════════════════════════════════════════════════
s = blank_slide()
bg(s)
header(s, "02 — Architecture Technique",
       "Stack : HTML + CSS + JavaScript vanilla · roslibjs · EventEmitter2 · rosbridge_server")

card(s, 0.35, 1.0, 4.0, 2.7, "Côté Client (Navigateur)", "🖥️", [
    "HTML5 / CSS3 / JavaScript (vanilla)",
    "roslibjs — bibliothèque officielle ROS/JS",
    "EventEmitter2 — gestion des événements",
    "Canvas HTML5 — dessin LIDAR",
    "localStorage — persistance IP du robot",
    "Aucun framework (React, Vue...) nécessaire",
], ACCENT)

card(s, 4.55, 1.0, 4.1, 2.7, "Côté Serveur (Robot)", "🤖", [
    "rosbridge_server (ROS 2 Jazzy)",
    "Port WebSocket : 9090",
    "python3 -m http.server 8080 (fichiers statiques)",
    "Aucun backend supplémentaire requis",
    "Topics ROS 2 exposés en temps réel",
], GREEN)

card(s, 8.85, 1.0, 4.1, 2.7, "Structure des Fichiers", "📁", [
    "index.html          → Dashboard principal",
    "deplacement_robot.* → Téléopération",
    "vision_lidar.*      → Visualiseur LIDAR",
    "vision_camera.*     → Flux caméra",
    "deplacement_bras.*  → Contrôle bras",
    "style.css / *.css   → Styles par page",
], ORANGE)

txt(s, "Topics ROS 2 utilisés par l'IHM :", 0.35, 3.9, 12.5, 0.3, size=13, bold=True, color=ACCENT)
topics = [
    ("/joy_ihm",                            "sensor_msgs/Joy",           "Publié", ACCENT,  "Déplacement robot + flippers + caméra"),
    ("/choix_pos",                          "std_msgs/Int16MultiArray",  "Publié", ACCENT,  "Commandes bras (6 axes)"),
    ("/scan",                               "sensor_msgs/LaserScan",     "Abonné", GREEN,   "Données brutes LIDAR"),
    ("/cv_camera/image_raw/compressed",     "sensor_msgs/CompressedImage","Abonné",GREEN,   "Flux caméra JPEG Base64"),
    ("/vitesse1  /vitesse2",               "std_msgs/Int32",             "Abonné", ORANGE,  "Vitesses moteurs gauche/droite"),
    ("/inclinaison1  /inclinaison2",       "std_msgs/Int32",             "Abonné", ORANGE,  "Inclinaison avant/arrière"),
]
for i, (topic, mtype, direction, col, desc) in enumerate(topics):
    lx = 0.35
    ty = 4.25 + i * 0.52
    badge(s, direction, lx, ty, 0.58, 0.38, col)
    txt(s, topic, lx+0.65, ty+0.04, 3.3, 0.35, size=9.5, bold=True, color=WHITE)
    txt(s, mtype, lx+4.0, ty+0.04, 3.5, 0.35, size=9.5, color=ACCENT2, italic=True)
    txt(s, desc,  lx+7.6, ty+0.04, 5.4, 0.35, size=9.5, color=LIGHT)


# ══════════════════════════════════════════════════════
#  SLIDE 5 — DASHBOARD index.html
# ══════════════════════════════════════════════════════
s = blank_slide()
bg(s)
header(s, "03 — Dashboard principal (index.html)",
       "Vue unifiée — 4 iframes côte à côte — configuration IP centralisée")

# Maquette du dashboard
rect(s, 0.35, 1.0, 12.6, 5.8, DARK_CARD)
rect(s, 0.35, 1.0, 12.6, 0.45, RGBColor(0x0A, 0x14, 0x28))
txt(s, "🤖  RMS — Tableau de bord",
    0.5, 1.05, 6, 0.35, size=12, bold=True, color=ACCENT)
txt(s, "🌐 IP Robot: [192.168.137.82]  [Appliquer]",
    7.5, 1.05, 5.2, 0.35, size=10, color=LIGHT)
rect(s, 0.35, 1.45, 12.6, 0.06, ACCENT2)

panels = [
    (0.4,  1.55, 6.25, 2.5, "🕹️ Déplacement Robot", "deplacement_robot.html", ACCENT),
    (6.7,  1.55, 6.25, 2.5, "📡 Vision LIDAR",       "vision_lidar.html",      GREEN),
    (0.4,  4.1,  6.25, 2.5, "📷 Caméra",             "vision_camera.html",     ORANGE),
    (6.7,  4.1,  6.25, 2.5, "🦾 Contrôle Bras",      "deplacement_bras.html",  PURPLE),
]
for (l, t, w, h, name, src, col) in panels:
    rect(s, l, t, w, h, RGBColor(0x08, 0x08, 0x20))
    rect(s, l, t, w, 0.3, col)
    txt(s, name, l+0.1, t+0.03, w-0.15, 0.25, size=10, bold=True,
        color=DARK_BG, align=PP_ALIGN.CENTER)
    txt(s, f'<iframe src="{src}">',
        l+0.1, t+0.4, w-0.15, 0.4, size=9, color=ACCENT2, italic=True,
        align=PP_ALIGN.CENTER)

# Note IP
txt(s, "💡  L'IP du robot est stockée en localStorage — toutes les iframes se rechargent automatiquement après modification.",
    0.35, 6.88, 12.6, 0.38, size=11, color=LIGHT, align=PP_ALIGN.CENTER)


# ══════════════════════════════════════════════════════
#  SLIDE 6 — DÉPLACEMENT ROBOT
# ══════════════════════════════════════════════════════
s = blank_slide()
bg(s)
header(s, "04 — Page Déplacement Robot",
       "Téléopération clavier + boutons · Flippers · Caméra orientable · Télémétrie temps réel")

card(s, 0.35, 1.0, 3.8, 2.7, "Contrôle Directionnel", "🕹️", [
    "Boutons ↑ ↓ ← → + ⏹ Stop",
    "Clavier : Z/S/Q/D (AZERTY) · Espace = Stop",
    "Anti-rebond : throttle 200 ms sur avancer",
    "keydown → commande · keyup → Stop automatique",
    "Topic publié : /joy_ihm (sensor_msgs/Joy)",
], ACCENT)

card(s, 4.35, 1.0, 4.3, 2.7, "Flippers & Caméra", "🔧", [
    "Flipper AVG : axe [0,0,±1,0,0,0]",
    "Flipper AVD / AR : boutons buttons[1,2]",
    "Caméra haut : buttons[5]",
    "Caméra bas : buttons[7]",
    "Touches : A/E (flipper) · M/P (caméra)",
    "Même topic /joy_ihm — axes différents",
], ORANGE)

card(s, 8.85, 1.0, 4.1, 2.7, "Télémétrie (Subscribers)", "📊", [
    "vitesse1 → /vitesse1  (motor G, m/s)",
    "vitesse2 → /vitesse2  (motor D, m/s)",
    "inclinaison1 → /inclinaison1  (AV, °)",
    "inclinaison2 → /inclinaison2  (AR, °)",
    "boussole → /boussole  (cap, °)",
    "Mis à jour en temps réel dans le DOM",
], GREEN)

txt(s, "Format du message Joy publié sur /joy_ihm :", 0.35, 3.9, 12.5, 0.32, size=13, bold=True, color=ACCENT)
code_block(s,
    'axes:    [0.0, 1.0, 0.0, 0.0, 0.0, 0.0]   // [Roulis, Avancer, Flipper, -, -, -]\n'
    'buttons: [0,   0,   0,   0,   0,   1,   0, 1, 0, 0, 0, 0]   // [-, AVD, AR, -, -, CamH, -, CamB, ...]',
    0.35, 4.26, 12.6, 0.95)

txt(s, "⚠️  Le robot s'arrête automatiquement à chaque keyup — sécurité intégrée.", 0.35, 5.35, 12.6, 0.32,
    size=11, bold=True, color=ORANGE, align=PP_ALIGN.CENTER)


# ══════════════════════════════════════════════════════
#  SLIDE 7 — VISUALISEUR LIDAR
# ══════════════════════════════════════════════════════
s = blank_slide()
bg(s)
header(s, "05 — Page Visualisation LIDAR",
       "Canvas HTML5 · Abonné à /scan · Rendu polaire en temps réel")

card(s, 0.35, 1.0, 4.2, 2.8, "Fonctionnement", "📡", [
    "Abonnement au topic /scan (LaserScan) via roslibjs",
    "throttle_rate: 100 ms (10 Hz max pour le rendu)",
    "Chaque message contient ranges[], angle_min, angle_increment",
    "Filtrage des valeurs NaN / Inf / hors range_max",
    "Dessin de chaque point en coordonnées cartésiennes",
    "Fond redessiné à chaque frame (pas d'accumulation)",
], ACCENT)

card(s, 4.75, 1.0, 4.2, 2.8, "Rendu Canvas", "🎨", [
    "Fond noir #0a0a1a",
    "4 cercles de distance (2.5m / 5m / 7.5m / 10m)",
    "Croix de quadrant (avant/arrière/gauche/droite)",
    "Point central cyan = position du robot",
    "Couleur des points : rouge si proche, vert si loin (ratio)",
    "Labels : AVANT · ARRIÈRE · G · D",
], GREEN)

card(s, 9.15, 1.0, 3.8, 2.8, "Indicateurs IHM", "🟢", [
    "Badge 🟢 Connecté / 🔴 Déconnecté",
    "Compteur : 'N pts valides'",
    "Champ IP configurable → updateRosUrl()",
    "IP persistée en localStorage",
    "Message 'En attente de /scan...' au démarrage",
], ORANGE)

txt(s, "Algorithme de projection polaire → cartésienne :", 0.35, 4.0, 12.5, 0.3, size=13, bold=True, color=ACCENT)
code_block(s,
    "for (var i = 0; i < ranges.length; i++) {\n"
    "    var r     = ranges[i];\n"
    "    if (!isFinite(r) || r <= 0 || r > rangeMax) continue;      // filtre\n"
    "    var angle = angleMin + i * angleIncrement;                   // rad\n"
    "    var x     = cx + Math.sin(angle) * r * scale;               // pixel X\n"
    "    var y     = cy - Math.cos(angle) * r * scale;               // pixel Y (axe Y inversé)\n"
    "    var ratio = r / rangeMax;                                    // 0 (proche) → 1 (loin)\n"
    "    ctx.fillStyle = 'rgb(' + Math.round(255*(1-ratio)) + ',' + Math.round(255*ratio) + ',100)';\n"
    "    ctx.fillRect(x-2, y-2, 4, 4);\n"
    "}",
    0.35, 4.35, 12.6, 2.2)


# ══════════════════════════════════════════════════════
#  SLIDE 8 — CAMÉRA
# ══════════════════════════════════════════════════════
s = blank_slide()
bg(s)
header(s, "06 — Page Vision Caméra",
       "Flux MJPEG temps réel via rosbridge · sensor_msgs/CompressedImage · Base64")

card(s, 0.35, 1.0, 5.8, 2.7, "Abonnement & Affichage", "📷", [
    "Topic : /cv_camera/image_raw/compressed",
    "Type  : sensor_msgs/CompressedImage",
    "Contenu : message.data = image JPEG encodée en Base64",
    "Affichage : img.src = 'data:image/jpeg;base64,' + message.data",
    "ID unique : id='image_sub' (bug corrigé : 8 IDs dupliqués → 1)",
    "Masquage du message 'Pas de signal' à la 1ère image reçue",
], ACCENT)

card(s, 6.35, 1.0, 6.6, 2.7, "Subscribers de télémétrie", "📊", [
    "vitesse1, vitesse2, inclinaison1, inclinaison2, boussole",
    "Chaque subscriber est distinct (bug corrigé)",
    "Mise à jour directe du DOM via getElementById()",
    "Plus de réseau partagé entre subscribers",
    "Statut ROS 🟢/🔴 affiché en haut de page",
], GREEN)

txt(s, "Code — réception image flux caméra :", 0.35, 3.88, 12.5, 0.3, size=13, bold=True, color=ACCENT)
code_block(s,
    "var listener = new ROSLIB.Topic({\n"
    "    ros         : ros,\n"
    "    name        : '/cv_camera/image_raw/compressed',\n"
    "    messageType : 'sensor_msgs/CompressedImage'\n"
    "});\n"
    "listener.subscribe(function(message) {\n"
    "    var img = document.getElementById('image_sub');\n"
    "    img.src = 'data:image/jpeg;base64,' + message.data;\n"
    "    document.getElementById('cam-no-signal').style.display = 'none';  // cache le message 'En attente'\n"
    "});",
    0.35, 4.22, 12.6, 2.35)


# ══════════════════════════════════════════════════════
#  SLIDE 9 — CONTRÔLE BRAS
# ══════════════════════════════════════════════════════
s = blank_slide()
bg(s)
header(s, "07 — Page Contrôle Bras",
       "6 sliders (déplacement + rotation) · 3 positions pré-définies · topic /choix_pos")

card(s, 0.35, 1.0, 6.0, 2.7, "Sliders 6 axes", "🦾", [
    "Slider 1 (X) : déplacement axe 1  [1600–2400, centre=2048]",
    "Slider 2 (Y) : déplacement axe 2  [1400–2400, centre=2048]",
    "Slider 3 (Z) : déplacement axe 3  [0–1, binaire]",
    "Slider 4 (RX): rotation axe 4     [0–4095, centre=2048]",
    "Slider 5 (RY): rotation axe 5     [700–3200, centre=2048]",
    "Slider 6 (RZ): rotation axe 6     [−180–+180°]",
], ACCENT)

card(s, 6.55, 1.0, 6.4, 2.7, "Boutons positions pré-définies", "🎯", [
    "Bouton 'Rangement'      → setButtonValueAndSend(1)",
    "Bouton 'Déploiement'    → setButtonValueAndSend(2)",
    "Bouton 'Position haute' → setButtonValueAndSend(3)",
    "La valeur 'bouton' est ajoutée au message MultiArray",
    "Le node ROS 2 lit [dx, dy, dz, rx, ry, rz, bouton]",
    "Passage automatique aux positions fixes",
], GREEN)

txt(s, "Message publié sur /choix_pos (Int16MultiArray) :", 0.35, 3.9, 12.5, 0.3, size=13, bold=True, color=ACCENT)
code_block(s,
    "var message = new ROSLIB.Message({\n"
    "    layout : { dim: [], data_offset: 0 },\n"
    "    data   : [\n"
    "        sliderValues.dx,     // position axe X\n"
    "        sliderValues.dy,     // position axe Y\n"
    "        sliderValues.dz,     // position axe Z\n"
    "        sliderValues.rx,     // rotation X\n"
    "        sliderValues.ry,     // rotation Y\n"
    "        sliderValues.rz,     // rotation Z\n"
    "        sliderValues.bouton  // 0=manuel, 1=rangement, 2=deploiement, 3=haut\n"
    "    ]\n"
    "});\ntopic.publish(message);",
    0.35, 4.26, 12.6, 2.3)


# ══════════════════════════════════════════════════════
#  SLIDE 10 — BUGS CORRIGÉS
# ══════════════════════════════════════════════════════
s = blank_slide()
bg(s)
header(s, "08 — Bugs corrigés & Améliorations apportées",
       "6 corrections critiques rendant l'interface 100% fonctionnelle")

bugs = [
    (RED,    "🐛 AVANT",
     "deplacement_robot.js + vision_camera.js",
     "Subscribers 2, 3, 4, 5 appelaient tous subscriber1.subscribe()\n→ Seul subscriber1 recevait les données. Les 4 autres champs restaient vides."),
    (GREEN,  "✅ APRÈS",
     "Bug corrigé",
     "subscriber2.subscribe() · subscriber3.subscribe() · subscriber4.subscribe() · subscriber5.subscribe()\n→ Chaque champ (vitesse2, inclinaison1, inclinaison2, boussole) reçoit ses propres données."),
    (RED,    "🐛 AVANT",
     "vision_lidar.html",
     "Référençait vision-lidar.js (avec tiret)\n→ Fichier introuvable → JavaScript non chargé → page silencieusement cassée."),
    (GREEN,  "✅ APRÈS",
     "Bug corrigé",
     "Corrigé en vision_lidar.js (underscore)\n→ Le script se charge et le canvas s'initialise correctement."),
    (RED,    "🐛 AVANT",
     "vision_camera.html",
     "8 éléments <img id='image_sub'> identiques\n→ querySelector('#image_sub') ne peut cibler qu'un seul élément → 7 images ignorées."),
    (GREEN,  "✅ APRÈS",
     "Bug corrigé",
     "Réduit à 1 seul <img id='image_sub'>\n→ Le flux caméra s'affiche correctement."),
    (RED,    "🐛 AVANT",
     "deplacement_robot.html",
     "Inputs sans id → les subscribers écrivaient dans null\n→ document.getElementById('vitesse1') retournait null → erreur silencieuse."),
    (GREEN,  "✅ APRÈS",
     "Bug corrigé",
     "Telemetry cards ajoutées : <span id='vitesse1'>, <span id='vitesse2'>, <span id='inclinaison1'>, <span id='inclinaison2'>, <span id='boussole'>\n→ Données affichées en temps réel."),
]

# 4 paires avant/après
col_w = 6.25
for pair in range(4):
    i0 = pair * 2
    for j in range(2):
        item = bugs[i0 + j]
        col_idx = pair % 2
        row_idx = pair // 2
        l = 0.35 + col_idx * 6.55
        t = 1.05 + row_idx * 2.8 + j * 1.3
        col = item[0]
        rect(s, l, t, col_w, 1.22, DARK_CARD)
        rect(s, l, t, 0.06, 1.22, col)
        txt(s, f"{item[1]} — {item[2]}",
            l+0.14, t+0.06, col_w-0.2, 0.3, size=10, bold=True, color=col)
        txt(s, item[3],
            l+0.14, t+0.4, col_w-0.2, 0.78, size=9.5, color=LIGHT)


# ══════════════════════════════════════════════════════
#  SLIDE 11 — DÉMO & LANCEMENT
# ══════════════════════════════════════════════════════
s = blank_slide()
bg(s)
header(s, "09 — Démo & Lancement",
       "Lancer l'interface en 2 commandes · Test sans robot possible")

txt(s, "Étape 1 — Lancer le serveur de fichiers", 0.35, 0.9, 12.5, 0.35, size=14, bold=True, color=ACCENT)
code_block(s,
    "# Se placer dans le dossier de l'interface (branche : interface)\n"
    "cd /home/ser/RoboCup_ws/IHM_Robot_RMS\n"
    "python3 -m http.server 8080\n"
    "# Ouvrir dans le navigateur → http://localhost:8080",
    0.35, 1.28, 12.6, 1.05)

txt(s, "Étape 2 — Démarrer rosbridge sur le robot (ROS 2)", 0.35, 2.45, 12.5, 0.35, size=14, bold=True, color=ACCENT)
code_block(s,
    "# Sur le robot (ROS 2 Jazzy)\n"
    "ros2 launch rosbridge_server rosbridge_websocket_launch.xml\n"
    "# ou\n"
    "ros2 run rosbridge_server rosbridge_websocket",
    0.35, 2.83, 12.6, 0.95)

txt(s, "Étape 3 — Configurer l'IP dans le Dashboard", 0.35, 3.9, 12.5, 0.32, size=14, bold=True, color=ACCENT)
txt(s, "Dans le champ 'IP Robot' en haut du dashboard → saisir l'IP du robot → cliquer 'Appliquer'",
    0.35, 4.25, 12.6, 0.38, size=12, color=LIGHT)

rect(s, 0.35, 4.75, 12.6, 0.06, ACCENT2)

txt(s, "Test sans robot connecté :", 0.35, 4.92, 5, 0.32, size=13, bold=True, color=ORANGE)
multi(s, [
    ("✓  L'IHM s'ouvre normalement dans le navigateur", 11, False, LIGHT),
    ("✓  Les pages s'affichent avec toute l'interface graphique", 11, False, LIGHT),
    ("✓  Les indicateurs affichent 🔴 Déconnecté (normal)", 11, False, LIGHT),
    ("✓  Le canvas LIDAR affiche 'En attente de /scan...'", 11, False, LIGHT),
    ("✓  Aucune erreur JavaScript dans la console (F12)", 11, False, WHITE),
], 0.35, 5.28, 5.8, 1.85, default_size=11)

multi(s, [
    ("Branche Git :", 11, True, ACCENT),
    ("interface", 11, False, WHITE),
    ("", 10, False, LIGHT),
    ("Dossier :", 11, True, ACCENT),
    ("IHM_Robot_RMS/", 11, False, WHITE),
    ("", 10, False, LIGHT),
    ("URL locale :", 11, True, ACCENT),
    ("http://localhost:8080", 11, False, WHITE),
    ("", 10, False, LIGHT),
    ("URL robot :", 11, True, ACCENT),
    ("http://robot_ip:8080/IHM_Robot_RMS/", 11, False, WHITE),
], 7.2, 4.92, 5.8, 2.3, default_size=11)


# ══════════════════════════════════════════════════════
#  SLIDE 12 — CONCLUSION
# ══════════════════════════════════════════════════════
s = blank_slide()
bg(s)
rect(s, 0, 0, 0.18, 7.5, ACCENT)

txt(s, "Interface IHM — Récapitulatif",
    0.45, 0.4, 12, 0.7, size=38, bold=True, color=ACCENT)
rect(s, 0.45, 1.2, 8, 0.06, ACCENT)

achievements = [
    (ACCENT,  "Dashboard 4 panneaux",        "Vue unifiée Robot + LIDAR + Caméra + Bras sur une seule page"),
    (GREEN,   "LIDAR Canvas temps réel",      "Rendu polaire HTML5, abonné à /scan, couleurs distance"),
    (GREEN,   "Caméra flux live",             "JPEG Base64 via rosbridge, affichage instantané"),
    (GREEN,   "Téléopération complète",       "Clavier AZERTY + boutons, flippers, caméra orientable"),
    (GREEN,   "Contrôle bras 6 axes",         "Sliders + positions pré-définies (Rangement, Déploiement, Haut)"),
    (GREEN,   "6 bugs critiques corrigés",    "Subscribers, IDs, noms de fichiers, DOM manquant"),
    (ORANGE,  "Indicateurs dynamiques",       "🟢/🔴 connexion ROS, compteur de points LIDAR, télémétrie"),
    (ACCENT2, "IP configurable",              "localStorage → une IP, toutes les iframes rechargées"),
]

for i, (col, title, desc) in enumerate(achievements):
    row = i % 4
    c   = i // 4
    l = 0.45 + c * 6.45
    t = 1.38 + row * 1.35
    rect(s, l, t, 6.2, 1.22, DARK_CARD)
    rect(s, l, t, 0.07, 1.22, col)
    txt(s, "✅  " + title, l+0.16, t+0.07, 5.9, 0.35, size=12, bold=True, color=WHITE)
    txt(s, desc,           l+0.16, t+0.48, 5.9, 0.65, size=10, color=LIGHT)

rect(s, 0, 6.85, 13.33, 0.65, DARK_CARD)
txt(s, "Merci · Questions ?   —   Groupe RMS · IATIC4 · UVSQ",
    0.4, 6.93, 12.5, 0.4, size=15, bold=True, color=ACCENT, align=PP_ALIGN.CENTER)


# ── Sauvegarde ────────────────────────────────────────
OUTPUT = "/home/ser/RoboCup_ws/Présentation_IHM_Interface.pptx"
prs.save(OUTPUT)
print(f"✅  Présentation générée : {OUTPUT}")
print(f"    Slides : {len(prs.slides)}")
