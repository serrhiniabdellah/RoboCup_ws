# Code Arduino - Documentation

## 📋 Vue d'ensemble

Le code Arduino contrôle les **servomoteurs Dynamixel AX-12** du bras robotique via une connexion série RS-485 et gère l'**accéléromètre MPU-9250** pour les mesures d'inclinaison.

---

## ⚠️ PROBLÈME DE DUPLICATION

**Attention** : Ce dossier contient **PLUSIEURS COPIES** du code (structures complexes) :

```
Bras_Manuel/src/Arduino/
├── Bras_ROS.ino/              ❌ COPIE ANCIENNE
├── Bras_ROS_Mega (autre copie)/  ❌ COPIE ANCIENNE  
├── Bras_ROS_Mega (copie)/     ❌ COPIE ANCIENNE
├── Bras_ROS_Mega/             ✅ VERSION ACTIVE (probablement)
├── new/                        ❌ VERSION EN CONSTRUCTION ?
└── SAVEax132/                  ❌ SAUVEGARDE ANCIENNES VERSION
```

**→ À NETTOYER : Garder UNE SEULE version** et archiver le reste.

---

## 📁 Structure - Version Active Supposée

### **Fichiers Cibles principales : `/Bras_ROS_Mega/` et `/new/`**

#### **Fichiers .ino (Arduino Sketches)**

| Fichier | Fonction |
|---------|----------|
| `Bras_ROS_Mega.ino` / `catkin.ino` | Sketch principal - initialisation et boucle |
| `Fonctions.ino` | Fonctions utilitaires (communication série, convertion données) |
| `Dynamixel.ino` | Communications AX-12 (protocole Dynamixel) |

#### **Fichiers .h (Headers)**

| Fichier | Contenu |
|---------|---------|
| `Dynamixel.h` | Définitions des registres AX-12, fonctions d'accès |
| `BrasMSGS.h` | Structures de messages pour communication ROS/Arduino |
| `simple_mpu.h` | Driver minimaliste pour capteur MPU-9250 |
| `ax12.h` | Classe pour contrôle individuels des servos AX-12 |

#### **Fichiers .cpp (Implementations)**

| Fichier | Détail |
|---------|--------|
| `ax12.cpp` | Implémentation classe AX-12 (envoi commandes, lecture retours) |

---

## 🎯 Rôles des Composants

### **1. Servomoteurs Dynamixel AX-12**

**Objectif** : Actionneurs du bras (6 articulations)

**Caractéristiques** :
- Protocole **RS-485** demi-duplex
- Adressage par ID (0-253)
- Couple nominal : ~1.5 Nm
- Vitesse : 0-60 rpm (configurable)
- Feedback : Position, charge, température, voltage

**Exemple de commande** :
```cpp
// Définition dans Dynamixel.h
#define AX_GOAL_POSITION     0x1E
#define AX_MOVING_SPEED      0x20
#define AX_TORQUE_LIMIT      0x22

// Utilisation
ax12.move(id, position);  // Déplacement servo id vers position (0-1023)
int pos = ax12.readPosition(id);  // Lecture position actuelle
```

### **2. Accéléromètre MPU-9250 (9-axes)**

**Objectif** : Mesurer l'orientation et l'inclinaison du bras

**Axes mesurés** :
- **Accélération** (X, Y, Z) → g-force
- **Gyroscope** (X, Y, Z) → taux rotation
- **Magnétomètre** (X, Y, Z) → champ magnétique

**Utilité** : 
- Feedback de positionnement
- Détection de collision (pics d'accélération)
- Compensation gravitaire

**Connexion** : I2C (pins SDA/SCL Arduino Mega)

---

## 🔌 Protocole de Communication

### **ROS ↔ Arduino (Série USB, 9600 baud)**

**Format du message entrant ROS** (exemple) :
```
[ID] [POSITION_H] [POSITION_L] [VITESSE_H] [VITESSE_L] [PINCE_ETAT]
```

**Traitement**:
1. Reçoit via `Serial.read()`
2. Valide la séquence
3. Décode position/vitesse
4. Envoie commande Dynamixel via RS-485

**Feedback retourné à ROS** :
```
[STATUS_BYTE] [POSITIONS_ARRAY] [ERREURS]
```

### **Communication Dynamixel AX-12**

Utilise le **protocole Dynamixel v1.0** :
- Structure : `0xFF 0xFF [ID] [LENGTH] [INSTRUCTION_BYTE] [PARAM1...] [CHECKSUM]`
- Exemples d'instructions :
  - `0x03` : READ DATA
  - `0x04` : WRITE DATA
  - `0x05` : REG WRITE (écriture différée)
  - `0x06` : ACTION (exécute writes différées)

---

## 🛠️ Initialisation & Setup

**Dans `Bras_ROS_Mega.ino` ou `catkin.ino`:**

```cpp
void setup() {
  // Initialisation série USB (ROS communication)
  Serial.begin(9600);
  
  // Initialisation RS-485 pour Dynamixel (pins DE/RE)
  pinMode(RS485_DE, OUTPUT);    // Driver Enable
  pinMode(RS485_RE, OUTPUT);    // Receiver Enable
  digitalWrite(RS485_DE, LOW);  // Mode réception par défaut
  digitalWrite(RS485_RE, LOW);
  
  // Initialisation I2C pour MPU-9250
  Wire.begin();
  MPU9250_init();
  
  // Configuration des AX-12
  for (int id = 1; id <= 6; id++) {
    ax12.setTorque(id, 1);              // Activation couple
    ax12.setSpeed(id, 100);              // Vitesse par défaut
  }
}
```

---

## ⚙️ Boucle Principale

**Dans `catkin.ino` ou sketch principal :**

```cpp
void loop() {
  // 1. Lecture données ROS (si disponible)
  if (Serial.available()) {
    parseRosCommand();
  }
  
  // 2. Mise à jour servos
  updateServos();
  
  // 3. Lecture senseurs
  readMPU9250();
  
  // 4. Envoi statut retour à ROS
  sendStatusMessage();
  
  delay(20);  // ~50 Hz update rate
}
```

---

## 📊 Fichiers de Données

### **Pas.txt** (non visible, probablement effacé)
Contenait peut-être : plages de mouvement, calibrations initiales

### **Ranges_moteurs** (Fichier texte)
**Rôle** : Tableau de configuration des servos
```
ID   MIN_ANGLE   MAX_ANGLE   OFFSET
1    0           300         0
2    100         250         10
...
```

### **Commandes.txt**
**Rôle** : Exemples de séquence de commandes pour tests manuels
```
Servos ID 1-6: initialisation
Move servo 1 → position 512
Move servo 2 → position 256
...
```

---

## 🔧 Contrôle du Servos AX-12

### **Registres importants** (définis dans `Dynamixel.h`)

| Adresse | Registre | Description | Accès |
|---------|----------|-------------|-------|
| 0x06 | TORQUE_ENABLE | Active/désactive le couple | W |
| 0x1E | GOAL_POSITION | Position cible (0-1023) | W |
| 0x20 | MOVING_SPEED | Vitesse (0-1023) | W |
| 0x22 | TORQUE_LIMIT | Limite de couple | W |
| 0x24 | PRESENT_POSITION | Position actuelle (lecture) | R |
| 0x26 | PRESENT_SPEED | Vitesse actuelle (lecture) | R |
| 0x2E | PRESENT_LOAD | Charge appliquée (lecture) | R |
| 0x2F | PRESENT_VOLTAGE | Tension d'alimentation (lecture) | R |

### **Exemple de fonction**

```cpp
// Dans ax12.cpp
void AX12::move(int id, int position) {
  // Limiter position à [0, 1023]
  position = constrain(position, 0, 1023);
  
  byte pos_h = (position >> 8) & 0xFF;
  byte pos_l = position & 0xFF;
  
  // Envoyer commande WRITE DATA
  sendCommand(id, 0x04, 0x1E, pos_h, pos_l);
}
```

---

## 📡 Lectures MPU-9250

**Fonction d'initialisation** (`simple_mpu.h`) :
```cpp
void MPU9250_init() {
  Wire.beginTransmission(MPU9250_ADDR);
  // Réinitialiser, activer DMP, configurer plages g
  Wire.endTransmission();
}

void readMPU9250() {
  Wire.requestFrom(MPU9250_ADDR, 14);  // 7 registres × 2 octets
  accel_x = wire.read() << 8 | Wire.read();
  accel_y = wire.read() << 8 | Wire.read();
  // ... etc gyro, magnéto
}
```

---

## ⚠️ Problèmes & Solutions

| Problème | Cause | Solution |
|----------|-------|----------|
| Servos ne répondent pas | Pas de tension RS-485 | Vérifier alimentation +5V |
| Communication série garbled | Vitesse erronée | Vérifier 9600 baud |
| MPU-9250 non détecté | Adresse I2C incorrecte | Utiliser scan I2C |
| Servo saccadé | Conflits ID | Vérifier ID unique (1-6) |

---

## 🚀 Compilation & Upload

```bash
# Via Arduino IDE
1. Ouvrir Bras_ROS_Mega.ino
2. Sélectionner Board → Arduino Mega 2560
3. Port → /dev/ttyACM0 (ou ACM1)
4. Sketch → Upload

# Vérifier dans Serial Monitor à 9600 baud
```

---

## 📚 Références

- [Dynamixel AX-12 Documentation](https://emanual.robotis.com/docs/en/dxl/ax/ax-12a/)
- [MPU-9250 Datasheet](https://invensense.tdk.com/wp-content/uploads/2015/02/MPU-9250-Datasheet.pdf)
- [Arduino Mega Pinout](https://www.arduino.cc/en/uploads/Main/Arduino_Mega-PIN.pdf)

---

## 👥 Auteurs

- Groupe MT5 RoboCup Rescue ISTY (2024-2025)
- **Responsable Programmation Arduino** : À identifier
- **Dernière mise à jour** : 19 mars 2026

---

**⚠️ ATTENTION** : Ces fichiers Arduino contiennent plusieurs versions dupliquées. Une **refactorisation majeure** est nécessaire pour maintenir une version unique, bien documentée et testée.
