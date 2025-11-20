/*
 * RoboCup 2024 - Firmware Arduino Mega
 * Contrôle des moteurs et navigation pour robot différentiel
 * Communication avec ROS2 via Serial
 */

#include "Config.h"
#include "Motor.h"
#include "Encoder.h"

// ============================================
// OBJETS GLOBAUX
// ============================================

Motor motorLeft(MOTOR_LEFT_PWM, MOTOR_LEFT_DIR1, MOTOR_LEFT_DIR2);
Motor motorRight(MOTOR_RIGHT_PWM, MOTOR_RIGHT_DIR1, MOTOR_RIGHT_DIR2);

Encoder encoderLeft(ENCODER_LEFT_A, ENCODER_LEFT_B);
Encoder encoderRight(ENCODER_RIGHT_A, ENCODER_RIGHT_B);

// ============================================
// VARIABLES GLOBALES
// ============================================

// Commandes de vitesse (m/s et rad/s)
float cmdLinear = 0.0;
float cmdAngular = 0.0;

// Odométrie
float posX = 0.0;
float posY = 0.0;
float posTheta = 0.0;

// Timestamps
unsigned long lastCmdTime = 0;
unsigned long lastOdomTime = 0;
unsigned long lastControlTime = 0;
unsigned long lastSafetyCheck = 0;

// État
bool emergencyStop = false;
bool motorEnabled = true;
bool useArrayCmd = false; // vrai si dernière commande est un tableau 9 octets

// ============================================
// INTERRUPTIONS ENCODEURS
// ============================================

void isrEncoderLeftA() {
  encoderLeft.update();
}

void isrEncoderRightA() {
  encoderRight.update();
}

// ============================================
// SETUP
// ============================================

void setup() {
  // Initialisation série
  Serial.begin(SERIAL_BAUD);
  Serial.setTimeout(SERIAL_TIMEOUT_MS);
  
  // Initialisation moteurs
  motorLeft.init();
  motorRight.init();
  
  // Initialisation encodeurs
  encoderLeft.init();
  encoderRight.init();
  
  // Attacher interruptions
  attachInterrupt(digitalPinToInterrupt(ENCODER_LEFT_A), isrEncoderLeftA, RISING);
  attachInterrupt(digitalPinToInterrupt(ENCODER_RIGHT_A), isrEncoderRightA, RISING);
  
  // Initialisation pins
  pinMode(LED_STATUS, OUTPUT);
  pinMode(BUTTON_ESTOP, INPUT_PULLUP);
  
  // LED startup
  for (int i = 0; i < 3; i++) {
    digitalWrite(LED_STATUS, HIGH);
    delay(200);
    digitalWrite(LED_STATUS, LOW);
    delay(200);
  }
  
  DEBUG_PRINTLN("RoboCup 2024 - Arduino Mega Ready");
  DEBUG_PRINT("Wheel separation: ");
  DEBUG_PRINTLN(WHEEL_SEPARATION);
  DEBUG_PRINT("Wheel radius: ");
  DEBUG_PRINTLN(WHEEL_RADIUS);
  
  lastCmdTime = millis();
  lastOdomTime = millis();
  lastControlTime = millis();
  lastSafetyCheck = millis();
}

// ============================================
// LOOP PRINCIPAL
// ============================================

void loop() {
  unsigned long currentTime = millis();
  
  // 1. Lire commandes série
  if (Serial.available() > 0) {
    readSerialCommand();
  }
  
  // 2. Vérifications de sécurité
  if (currentTime - lastSafetyCheck >= SAFETY_CHECK_MS) {
    performSafetyChecks();
    lastSafetyCheck = currentTime;
  }
  
  // 3. Boucle de contrôle moteurs (50 Hz)
  if (currentTime - lastControlTime >= (1000 / CONTROL_FREQ_HZ)) {
    updateMotorControl();
    lastControlTime = currentTime;
  }
  
  // 4. Publication odométrie (20 Hz)
  if (currentTime - lastOdomTime >= (1000 / ODOM_FREQ_HZ)) {
    updateOdometry();
    publishOdometry();
    lastOdomTime = currentTime;
  }
  
  // 5. LED status (clignotement)
  digitalWrite(LED_STATUS, (currentTime / 500) % 2);
}

// ============================================
// LECTURE COMMANDES SÉRIE
// ============================================

void readSerialCommand() {
  if (Serial.read() != MSG_START_BYTE) {
    return;
  }
  
  uint8_t msgType = Serial.read();
  
  switch (msgType) {
    case MSG_CMD_VEL:
      readCmdVel();
      break;
    case MSG_CMD_ARRAY:
      readCmdArray();
      break;
      
    case MSG_RESET:
      resetOdometry();
      break;
      
    case MSG_ESTOP:
      emergencyStop = true;
      motorLeft.stop();
      motorRight.stop();
      DEBUG_PRINTLN("EMERGENCY STOP");
      break;
      
    default:
      // Message inconnu
      break;
  }
}

void readCmdVel() {
  // Format attendu APRÈS avoir lu [START][TYPE]: [linear(4)][angular(4)][END]
  // Total global envoyé par l'hôte: 1+1+4+4+1 = 11 octets
  byte buffer[9];
  
  // Lire 9 octets (8 pour 2 floats + 1 pour END)
  if (Serial.readBytes(buffer, 9) != 9) {
    return;
  }
  
  // Vérifier fin de message
  if (buffer[8] != MSG_END_BYTE) {
    DEBUG_PRINTLN("Invalid message end");
    return;
  }
  
  // Extraire vitesses (float 4 octets chacun, little-endian)
  memcpy(&cmdLinear, &buffer[0], 4);
  memcpy(&cmdAngular, &buffer[4], 4);
  
  // Limiter les vitesses
  cmdLinear = constrain(cmdLinear, -MAX_LINEAR_SPEED, MAX_LINEAR_SPEED);
  cmdAngular = constrain(cmdAngular, -MAX_ANGULAR_SPEED, MAX_ANGULAR_SPEED);
  
  lastCmdTime = millis();
  useArrayCmd = false; // bascule en mode vitesse différentielle
  
  DEBUG_PRINT("CMD: lin=");
  DEBUG_PRINT(cmdLinear);
  DEBUG_PRINT(" ang=");
  DEBUG_PRINTLN(cmdAngular);
}

// Convertit int8_t (-127..127) en PWM (-255..255)
static int int8ToPwm(int8_t v) {
  int val = (int)v;
  // éviter une très petite zone morte autour de 0
  const int dead = 4;
  if (val >= -dead && val <= dead) return 0;
  // échelle linéaire
  long pwm = (long)val * 255L / 127L;
  if (pwm > 255) pwm = 255;
  if (pwm < -255) pwm = -255;
  return (int)pwm;
}

void readCmdArray() {
  // Après [START][TYPE], lire 9 octets signés + [END]
  byte buffer[10];
  if (Serial.readBytes(buffer, 10) != 10) {
    return;
  }
  if (buffer[9] != MSG_END_BYTE) {
    DEBUG_PRINTLN("Invalid array end");
    return;
  }

  // data[0]=gauche, data[1]=droite (reste ignoré ici)
  int8_t leftCmd = (int8_t)buffer[0];
  int8_t rightCmd = (int8_t)buffer[1];

  int leftPWM = int8ToPwm(leftCmd);
  int rightPWM = int8ToPwm(rightCmd);

  motorLeft.setSpeed(leftPWM);
  motorRight.setSpeed(rightPWM);

  lastCmdTime = millis();
  useArrayCmd = true; // évite que la boucle de contrôle écrase ces valeurs
}

// ============================================
// CONTRÔLE MOTEURS
// ============================================

void updateMotorControl() {
  if (emergencyStop || !motorEnabled) {
    motorLeft.stop();
    motorRight.stop();
    return;
  }
  // En mode tableau direct, on n'écrase pas les vitesses fixées par readCmdArray
  if (useArrayCmd) {
    return;
  }
  
  // Cinématique différentielle
  // v_left = v - ω * L / 2
  // v_right = v + ω * L / 2
  
  float leftSpeed = cmdLinear - (cmdAngular * WHEEL_SEPARATION / 2.0);
  float rightSpeed = cmdLinear + (cmdAngular * WHEEL_SEPARATION / 2.0);
  
  // Convertir m/s en PWM (0-255)
  // PWM = (speed / max_speed) * 255
  int leftPWM = (leftSpeed / MAX_LINEAR_SPEED) * MAX_MOTOR_SPEED;
  int rightPWM = (rightSpeed / MAX_LINEAR_SPEED) * MAX_MOTOR_SPEED;
  
  // Appliquer aux moteurs
  motorLeft.setSpeed(leftPWM);
  motorRight.setSpeed(rightPWM);
}

// ============================================
// ODOMÉTRIE
// ============================================

void updateOdometry() {
  // Lire changements encodeurs
  long deltaLeft = encoderLeft.getTicksDelta();
  long deltaRight = encoderRight.getTicksDelta();
  
  // Convertir ticks en distance (m)
  float distLeft = deltaLeft / ENCODER_TICKS_PER_M;
  float distRight = deltaRight / ENCODER_TICKS_PER_M;
  
  // Calculer déplacement
  float distCenter = (distLeft + distRight) / 2.0;
  float deltaTheta = (distRight - distLeft) / WHEEL_SEPARATION;
  
  // Mettre à jour position
  posX += distCenter * cos(posTheta + deltaTheta / 2.0);
  posY += distCenter * sin(posTheta + deltaTheta / 2.0);
  posTheta += deltaTheta;
  
  // Normaliser angle
  while (posTheta > PI) posTheta -= 2 * PI;
  while (posTheta < -PI) posTheta += 2 * PI;
}

void publishOdometry() {
  // Format: [START][TYPE][x][y][theta][vx][vtheta][END]
  
  Serial.write(MSG_START_BYTE);
  Serial.write(MSG_ODOM);
  
  // Position
  Serial.write((byte*)&posX, sizeof(float));
  Serial.write((byte*)&posY, sizeof(float));
  Serial.write((byte*)&posTheta, sizeof(float));
  
  // Vitesses (reprendre les commandes)
  Serial.write((byte*)&cmdLinear, sizeof(float));
  Serial.write((byte*)&cmdAngular, sizeof(float));
  
  Serial.write(MSG_END_BYTE);
}

void resetOdometry() {
  posX = 0.0;
  posY = 0.0;
  posTheta = 0.0;
  encoderLeft.reset();
  encoderRight.reset();
  
  DEBUG_PRINTLN("Odometry reset");
}

// ============================================
// SÉCURITÉ
// ============================================

void performSafetyChecks() {
  // Vérifier timeout commande
  if (millis() - lastCmdTime > CMD_TIMEOUT_MS) {
    cmdLinear = 0.0;
    cmdAngular = 0.0;
    if (useArrayCmd) {
      // En mode tableau, arrêter moteurs sur timeout
      motorLeft.stop();
      motorRight.stop();
      useArrayCmd = false; // repasser en mode vitesse par défaut
    }
    DEBUG_PRINTLN("Command timeout - stopping");
  }
  
  // Vérifier bouton d'arrêt d'urgence
  if (digitalRead(BUTTON_ESTOP) == LOW) {
    if (!emergencyStop) {
      emergencyStop = true;
      motorLeft.stop();
      motorRight.stop();
      DEBUG_PRINTLN("Emergency button pressed");
    }
  }
  
  // Publier statut
  if (emergencyStop) {
    Serial.write(MSG_START_BYTE);
    Serial.write(MSG_STATUS);
    Serial.write(0x00);  // Status: ESTOP
    Serial.write(MSG_END_BYTE);
  }
}
