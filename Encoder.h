/*
 * RoboCup 2024 - Classe Encoder
 * Lecture des encodeurs rotatifs avec interruptions
 */

#ifndef ENCODER_H
#define ENCODER_H

#include <Arduino.h>

class Encoder {
private:
  uint8_t pinA;
  uint8_t pinB;
  volatile long ticks;
  volatile long lastTicks;
  
public:
  Encoder(uint8_t pA, uint8_t pB) 
    : pinA(pA), pinB(pB), ticks(0), lastTicks(0) {}
  
  void init() {
    pinMode(pinA, INPUT_PULLUP);
    pinMode(pinB, INPUT_PULLUP);
    ticks = 0;
    lastTicks = 0;
  }
  
  // À appeler dans l'ISR
  void update() {
    // Lecture simple (peut être amélioré avec détection de direction)
    if (digitalRead(pinB)) {
      ticks++;
    } else {
      ticks--;
    }
  }
  
  long getTicks() {
    noInterrupts();
    long t = ticks;
    interrupts();
    return t;
  }
  
  long getTicksDelta() {
    noInterrupts();
    long delta = ticks - lastTicks;
    lastTicks = ticks;
    interrupts();
    return delta;
  }
  
  void reset() {
    noInterrupts();
    ticks = 0;
    lastTicks = 0;
    interrupts();
  }
  
  float getDistance(float ticksPerMeter) {
    return getTicks() / ticksPerMeter;
  }
};

#endif // ENCODER_H
