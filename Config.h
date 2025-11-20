/*
 * RoboCup 2024 - Configuration Arduino Mega
 * Configuration matérielle et paramètres du robot
 */

#ifndef CONFIG_H
#define CONFIG_H

// ============================================
// CONFIGURATION PINS ARDUINO MEGA
// ============================================

// Moteur Gauche
#define MOTOR_LEFT_PWM    2    // PWM pin
#define MOTOR_LEFT_DIR1   22   // Direction pin 1
#define MOTOR_LEFT_DIR2   23   // Direction pin 2

// Moteur Droit
#define MOTOR_RIGHT_PWM   3    // PWM pin
#define MOTOR_RIGHT_DIR1  24   // Direction pin 1
#define MOTOR_RIGHT_DIR2  25   // Direction pin 2

// Encodeurs
#define ENCODER_LEFT_A    18   // Interrupt pin (INT5)
#define ENCODER_LEFT_B    19   // Interrupt pin (INT4)
#define ENCODER_RIGHT_A   20   // Interrupt pin (INT3)
#define ENCODER_RIGHT_B   21   // Interrupt pin (INT2)

// LED et boutons
#define LED_STATUS        13   // LED intégrée
#define BUTTON_ESTOP      26   // Bouton d'arrêt d'urgence

// ============================================
// PARAMÈTRES PHYSIQUES DU ROBOT
// ============================================

// Dimensions du robot (en mètres)
#define WHEEL_SEPARATION  0.44    // Distance entre roues (m)
#define WHEEL_RADIUS      0.05    // Rayon des roues (m)
#define WHEEL_DIAMETER    0.10    // Diamètre des roues (m)

// Encodeurs
#define ENCODER_TICKS_PER_REV  360    // Nombre de ticks par tour de roue
#define ENCODER_TICKS_PER_M    (ENCODER_TICKS_PER_REV / (PI * WHEEL_DIAMETER))

// ============================================
// LIMITES ET SÉCURITÉ
// ============================================

// Vitesses maximales
#define MAX_LINEAR_SPEED   1.0     // m/s
#define MAX_ANGULAR_SPEED  2.0     // rad/s
#define MAX_MOTOR_SPEED    255     // PWM (0-255)

// Timeouts
#define CMD_TIMEOUT_MS     1000    // Timeout commande (ms)
#define SAFETY_CHECK_MS    100     // Fréquence checks sécurité (ms)

// ============================================
// COMMUNICATION SÉRIE
// ============================================

#define SERIAL_BAUD        115200  // Vitesse série
#define SERIAL_TIMEOUT_MS  100     // Timeout lecture série

// Protocole de communication
#define MSG_START_BYTE     0xAA    // Début de message
#define MSG_END_BYTE       0x55    // Fin de message

// Types de messages
#define MSG_CMD_VEL        0x01    // Commande vitesse
#define MSG_ODOM           0x02    // Odométrie
#define MSG_STATUS         0x03    // Statut
#define MSG_ESTOP          0x04    // Arrêt d'urgence
#define MSG_RESET          0x05    // Reset encodeurs
// Commande tableau (9 octets signés) pour pistes/flippers/caméra
#define MSG_CMD_ARRAY      0x10

// ============================================
// PARAMÈTRES DE CONTRÔLE
// ============================================

// Fréquences
#define CONTROL_FREQ_HZ    50      // Fréquence boucle contrôle (Hz)
#define ODOM_FREQ_HZ       20      // Fréquence publication odom (Hz)

// PID (si nécessaire)
#define KP_LEFT            1.0
#define KI_LEFT            0.0
#define KD_LEFT            0.0
#define KP_RIGHT           1.0
#define KI_RIGHT           0.0
#define KD_RIGHT           0.0

// ============================================
// DEBUG
// ============================================

#define DEBUG_ENABLED      1       // 1 = activer debug, 0 = désactiver
#define DEBUG_SERIAL       Serial  // Port série pour debug

#if DEBUG_ENABLED
  #define DEBUG_PRINT(x)    DEBUG_SERIAL.print(x)
  #define DEBUG_PRINTLN(x)  DEBUG_SERIAL.println(x)
#else
  #define DEBUG_PRINT(x)
  #define DEBUG_PRINTLN(x)
#endif

#endif // CONFIG_H
