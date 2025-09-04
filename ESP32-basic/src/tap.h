#ifndef TAP_H
#define TAP_H

#include <Arduino.h>

const int buttonPins[5] = {32, 27, 26, 33, 25};  // GPIOs
volatile int inputs[5] = {0, 0, 0, 0, 0};
volatile bool isTriggered = false;
bool gyroZ = false;


// Interrupt Service Routines (ISR)
void IRAM_ATTR ISR_0() { inputs[0] = 1; isTriggered = true; detachInterrupt(buttonPins[0]); }
void IRAM_ATTR ISR_1() { inputs[1] = 1; isTriggered = true; detachInterrupt(buttonPins[1]); }
void IRAM_ATTR ISR_2() { inputs[2] = 1; isTriggered = true; detachInterrupt(buttonPins[2]); }
void IRAM_ATTR ISR_3() { inputs[3] = 1; isTriggered = true; detachInterrupt(buttonPins[3]); }
void IRAM_ATTR ISR_4() { inputs[4] = 1; isTriggered = true; detachInterrupt(buttonPins[4]); }

void set_interrupts() {
  attachInterrupt(buttonPins[0], ISR_0, RISING);
  attachInterrupt(buttonPins[1], ISR_1, RISING);
  attachInterrupt(buttonPins[2], ISR_2, RISING);
  attachInterrupt(buttonPins[3], ISR_3, RISING);
  attachInterrupt(buttonPins[4], ISR_4, RISING);
}

void set_pins()
{
  for (int i = 0; i < 5; i++)
  {
    pinMode(buttonPins[i], INPUT_PULLDOWN);
  }
}

#endif