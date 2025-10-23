# 🔧 INVENTAIRE DES MOTEURS ET SERVOMOTEURS - ROBOT ROBOCUP

## 📊 RÉSUMÉ RAPIDE

| Type | Quantité | Modèle/Type | Fonction | Contrôleur |
|------|----------|-------------|----------|------------|
| **Servomoteurs Dynamixel** | **7-8** | AX-12A | Bras robotique | Arduino Mega |
| **Moteur DC pour Gripper** | **1** | AX-12A (mode continu) | Pince/Gripper | Arduino Mega |
| **Moteurs DC Plateforme** | **2** | Moteurs DC | Roues gauche/droite | Sabertooth |

**TOTAL : 10-11 actionneurs**

---

## 🤖 DÉTAIL PAR SOUS-SYSTÈME

### 1️⃣ BRAS ROBOTIQUE : 7-8 Servomoteurs Dynamixel AX-12A

D'après le code Arduino `Bras_ROS_Mega.ino`, voici les servomoteurs utilisés :

| ID | Variable | Fonction | Type | Limites | Notes |
|----|----------|----------|------|---------|-------|
| **0** | `servoID_0` | Axe 1 (Base rotation) | AX-12A | 0-4095 | Rotation complète |
| **1** | `servoID_1` | Axe 2 (Épaule) - Servo 1 | AX-12A | 1024-3072 | Doublé avec ID 2 |
| **2** | `servoID_2` | Axe 2 (Épaule) - Servo 2 | AX-12A | 1024-3072 | Doublé avec ID 1 |
| **3** | `servoID_3` | Axe 3 (Coude) - Servo 1 | AX-12A | 1024-3072 | Doublé avec ID 4 |
| **4** | `servoID_4` | Axe 3 (Coude) - Servo 2 | AX-12A | 1024-3072 | Doublé avec ID 3 |
| **5** | `servoID_5` | Axe 4 (Poignet rotation) | AX-12A | 0-4095 | Rotation complète |
| **6** | `servoID_6` | Axe 5 (Poignet inclinaison) | AX-12A | 1024-3072 | - |
| **7** | `servoID_7` | Axe 6 (Rotation finale) | XL430 ? | Variable | Commenté dans code |
| **8** | `servoID_8` | Gripper (Pince) | AX-12A | 0-1023 | Mode rotation continue |

#### 📝 Explication des servos "doublés" :

Certains axes utilisent **2 servos en parallèle** pour plus de force :
- **Axe 2 (Épaule)** : IDs 1 + 2 → Plus de couple pour lever le bras
- **Axe 3 (Coude)** : IDs 3 + 4 → Supporte le poids de l'avant-bras

#### 🔢 Configuration détaillée :

```cpp
// Code Arduino extrait
const byte servoID_0 = 0x00; // Axe1 - Base
const byte servoID_1 = 0x01; // Axe2 - Épaule servo 1
const byte servoID_2 = 0x02; // Axe2 - Épaule servo 2
const byte servoID_3 = 0x03; // Axe3 - Coude servo 1
const byte servoID_4 = 0x04; // Axe3 - Coude servo 2
const byte servoID_5 = 0x05; // Axe4 - Poignet rotation
const byte servoID_6 = 0x06; // Axe5 - Poignet inclinaison
const byte servoID_7 = 0x07; // Axe6 - (optionnel)
const byte servoID_8 = 0x08; // Gripper

// Initialisation des limites
ServoInit(servoID_0, 0, 4095);       // Axe1 : 360°
ServoInit(servoID_1, 1024, 3072);    // Axe2 : ~180°
ServoInit(servoID_2, 1024, 3072);    // Axe2 : ~180°
ServoInit(servoID_3, 1024, 3072);    // Axe3 : ~180°
ServoInit(servoID_4, 1024, 3072);    // Axe3 : ~180°
ServoInit(servoID_5, 0, 4095);       // Axe4 : 360°
ServoInit(servoID_6, 1024, 3072);    // Axe5 : ~180°
```

#### 📊 Résumé Bras :

**Configuration principale (utilisée actuellement) :**
- **7 servos Dynamixel AX-12A** (IDs 0-6)
- **1 moteur AX-12A en mode continu** pour le gripper (ID 8)
- **Total Bras : 8 actionneurs**

**Configuration étendue (si ID 7 activé) :**
- **8 servos Dynamixel**
- **1 gripper**
- **Total : 9 actionneurs**

---

### 2️⃣ PLATEFORME MOBILE : 2 Moteurs DC

#### Spécifications :

| Moteur | Position | Fonction | Contrôle |
|--------|----------|----------|----------|
| **Moteur Gauche** | Roue gauche | Propulsion + Direction différentielle | Sabertooth Canal 1 |
| **Moteur Droit** | Roue droite | Propulsion + Direction différentielle | Sabertooth Canal 2 |

#### 🔌 Contrôleur Sabertooth :

- **Modèle** : Sabertooth 2x25 ou 2x32 (à vérifier)
- **Canaux** : 2 canaux indépendants
- **Tension** : 12V ou 24V
- **Communication** : Série UART
- **Port** : `/dev/ttyUSB0` ou `/dev/ttyACM*`

#### 🎮 Mode de contrôle :

La plateforme utilise un **système différentiel** :
- **Avancer** : Les 2 moteurs tournent dans le même sens à vitesse égale
- **Tourner à gauche** : Moteur droit rapide, moteur gauche lent/inverse
- **Tourner à droite** : Moteur gauche rapide, moteur droit lent/inverse
- **Rotation sur place** : Les 2 moteurs tournent en sens inverse

---

## 📊 TABLEAU RÉCAPITULATIF COMPLET

### Vue d'ensemble :

```
┌─────────────────────────────────────────────────────────────┐
│                    ROBOT ROBOCUP                            │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  🦾 BRAS ROBOTIQUE                                          │
│  ├─ Servo 0 (ID 0x00) : Base rotation         [AX-12A]     │
│  ├─ Servo 1 (ID 0x01) : Épaule servo 1        [AX-12A]     │
│  ├─ Servo 2 (ID 0x02) : Épaule servo 2        [AX-12A]     │
│  ├─ Servo 3 (ID 0x03) : Coude servo 1         [AX-12A]     │
│  ├─ Servo 4 (ID 0x04) : Coude servo 2         [AX-12A]     │
│  ├─ Servo 5 (ID 0x05) : Poignet rotation      [AX-12A]     │
│  ├─ Servo 6 (ID 0x06) : Poignet inclinaison   [AX-12A]     │
│  └─ Gripper (ID 0x08) : Pince/Gripper         [AX-12A]     │
│                                          ─────────────────  │
│                                          TOTAL BRAS : 8     │
│                                                             │
│  🚗 PLATEFORME MOBILE                                       │
│  ├─ Moteur Gauche : Roue gauche               [DC Motor]   │
│  └─ Moteur Droit  : Roue droite               [DC Motor]   │
│                                          ─────────────────  │
│                                          TOTAL MOBILE : 2   │
│                                                             │
├─────────────────────────────────────────────────────────────┤
│  TOTAL GÉNÉRAL : 10 ACTIONNEURS                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔋 ALIMENTATION

### Servomoteurs Dynamixel AX-12A :
- **Tension nominale** : 11.1V - 12V
- **Courant par servo** : ~1.5A en charge max
- **Courant total bras** : 8 × 1.5A = **12A max** (simultané)
- **Batterie recommandée** : LiPo 3S (11.1V) 5000mAh ou plus

### Moteurs DC Plateforme :
- **Tension** : 12V ou 24V (selon moteur)
- **Courant total** : Variable selon charge (3-10A par moteur)
- **Batterie recommandée** : Séparée des servos (isolation électrique)

---

## 📡 COMMUNICATION

### Bus Dynamixel (Bras) :
- **Protocole** : Dynamixel Protocol 1.0 ou 2.0
- **Interface** : UART half-duplex
- **Baudrate** : 1 Mbps (1000000 baud)
- **Topologie** : Daisy chain (bus série)
- **Connexion** : Arduino Mega Serial3 → Direction pin 4

### Sabertooth (Plateforme) :
- **Protocole** : Série simplifié ou Packet Serial
- **Baudrate** : 9600 ou 38400 baud
- **Connexion** : Raspberry Pi ou Arduino → `/dev/ttyUSB*`

---

## 🛠️ CONFIGURATION MATÉRIELLE

### Adresses des servos Dynamixel :

Les servos doivent être configurés avec les bonnes IDs :

| Servo physique | ID à configurer | Commande Dynamixel Wizard |
|----------------|-----------------|---------------------------|
| Base | 0 | Set ID = 0 |
| Épaule servo 1 | 1 | Set ID = 1 |
| Épaule servo 2 | 2 | Set ID = 2 |
| Coude servo 1 | 3 | Set ID = 3 |
| Coude servo 2 | 4 | Set ID = 4 |
| Poignet rotation | 5 | Set ID = 5 |
| Poignet inclinaison | 6 | Set ID = 6 |
| Gripper | 8 | Set ID = 8 |

**⚠️ Important :** Utilisez **Dynamixel Wizard** pour configurer les IDs avant montage !

---

## 📝 NOTES TECHNIQUES

### Servos en mode "Doublé" :

Certains axes utilisent 2 servos **mécaniquement couplés** :
```cpp
// Exemple : Axe 2 (Épaule)
DoublePose(servoID_1, servoID_2, angle, angle, vitesse);
// Les 2 servos reçoivent la MÊME commande simultanément
```

**Avantages :**
- ✅ **Double couple** pour soulever des charges lourdes
- ✅ **Meilleure rigidité** mécanique
- ✅ **Répartition de la chaleur**

**Contraintes :**
- ⚠️ Nécessite un **alignement mécanique parfait**
- ⚠️ Les 2 servos doivent avoir des **IDs différentes**
- ⚠️ Consommation électrique doublée

### Gripper en mode rotation continue :

```cpp
void motor_init () {
    motor.writeInfo(24, 1);               // Active le torque
    motor.setEndlessTurnMode(false);      // Mode position
    // Configuration des limites et vitesses
}

void motor_position(int pos) {
    // Contrôle position 0-1023
    motor.writeInfo(30, pos);
}
```

Le gripper utilise un **AX-12A en mode position** (pas rotation continue finalement).

---

## 🎯 RÉPARTITION PAR RESPONSABLE

### Personne 3 (Bras & Arduino) :
**Responsable de :**
- ✅ 7-8 servomoteurs Dynamixel AX-12A
- ✅ 1 gripper AX-12A
- ✅ Bus Dynamixel
- ✅ Arduino Mega
- ✅ Code `Bras_ROS_Mega.ino`

**Total : 8-9 actionneurs**

### Personne 4 (Plateforme Mobile) :
**Responsable de :**
- ✅ 2 moteurs DC (gauche + droite)
- ✅ Contrôleur Sabertooth
- ✅ Encodeurs (optionnels)
- ✅ Odométrie

**Total : 2 moteurs**

---

## ✅ CHECKLIST DE VÉRIFICATION

### Avant démarrage :

#### Bras :
- [ ] Tous les servos Dynamixel ont une **ID unique** (0-8)
- [ ] **Alimentation 12V** disponible et stable
- [ ] **Bus Dynamixel** correctement câblé en daisy chain
- [ ] Arduino Mega connecté via **Serial3**
- [ ] Direction pin configuré (pin 4)
- [ ] Limites angulaires configurées dans le code

#### Plateforme :
- [ ] **2 moteurs DC** connectés au Sabertooth
- [ ] Polarité des moteurs vérifiée (gauche/droite)
- [ ] Sabertooth configuré (dip switches)
- [ ] Connexion série **9600 baud** opérationnelle
- [ ] Alimentation moteurs séparée (12V ou 24V)

---

## 📚 DOCUMENTATION UTILE

### Dynamixel AX-12A :
- Manuel : http://emanual.robotis.com/docs/en/dxl/ax/ax-12a/
- Wizard : https://emanual.robotis.com/docs/en/software/dynamixel/dynamixel_wizard2/
- Specs :
  - Couple : 1.5 N⋅m (à 12V)
  - Vitesse : 59 RPM
  - Résolution : 0.29° (1024 positions)
  - Protocole : TTL Half-Duplex

### Sabertooth :
- Manuel : https://www.dimensionengineering.com/datasheets/Sabertooth2x25.pdf
- Configuration : DIP switches pour mode série
- Commandes : Packet Serial Protocol

---

## 🔢 RÉSUMÉ FINAL

```
╔═══════════════════════════════════════════════════════════╗
║           INVENTAIRE COMPLET DES ACTIONNEURS             ║
╠═══════════════════════════════════════════════════════════╣
║                                                           ║
║  SERVOMOTEURS DYNAMIXEL AX-12A (Bras)        7 servos    ║
║  GRIPPER AX-12A (Pince)                      1 servo     ║
║  ─────────────────────────────────────────────────────    ║
║  SOUS-TOTAL BRAS                             8 servos    ║
║                                                           ║
║  MOTEURS DC (Plateforme mobile)              2 moteurs   ║
║  ─────────────────────────────────────────────────────    ║
║  SOUS-TOTAL PLATEFORME                       2 moteurs   ║
║                                                           ║
║  ═════════════════════════════════════════════════════    ║
║  TOTAL GÉNÉRAL                               10 actionneurs║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
```

**Note :** Si le servo ID 7 est activé, le total passe à **11 actionneurs** (9 pour le bras + 2 pour la plateforme).

---

**📌 Ce document est basé sur l'analyse du code Arduino `Bras_ROS_Mega.ino` et la structure du projet.**
