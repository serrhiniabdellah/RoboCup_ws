/*
 * RoboCup 2024 - Classe Motor
 * Gestion des moteurs DC avec driver L298N ou similaire
 */

#ifndef MOTOR_H
#define MOTOR_H

#include <Arduino.h>

class Motor {
private:
  uint8_t pwmPin;
  uint8_t dir1Pin;
  uint8_t dir2Pin;
  int currentSpeed;  // -255 à 255
  
public:
  Motor(uint8_t pwm, uint8_t dir1, uint8_t dir2) 
    : pwmPin(pwm), dir1Pin(dir1), dir2Pin(dir2), currentSpeed(0) {}
  
  void init() {
    pinMode(pwmPin, OUTPUT);
    pinMode(dir1Pin, OUTPUT);
    pinMode(dir2Pin, OUTPUT);
    stop();
  }
  
  // Définir la vitesse (-255 à 255)
  void setSpeed(int speed) {
    // Limiter la vitesse
    speed = constrain(speed, -255, 255);
    currentSpeed = speed;
    
    // Calculer PWM et direction
    int pwmValue = abs(speed);
    
    if (speed > 0) {
      // Avant
      digitalWrite(dir1Pin, HIGH);
      digitalWrite(dir2Pin, LOW);
    } else if (speed < 0) {
      // Arrière
      digitalWrite(dir1Pin, LOW);
      digitalWrite(dir2Pin, HIGH);
    } else {
      // Arrêt
      digitalWrite(dir1Pin, LOW);
      digitalWrite(dir2Pin, LOW);
    }
    
    analogWrite(pwmPin, pwmValue);
  }
  
  void stop() {
    setSpeed(0);
  }
  
  int getSpeed() const {
    return currentSpeed;
  }
};

#endif // MOTOR_H
