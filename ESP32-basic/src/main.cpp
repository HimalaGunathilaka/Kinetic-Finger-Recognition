#include <Arduino.h>

const int piezoSensors[4] = {34, 35, 32, 33};
volatile int inputs[4] = {0, 0, 0, 0};

void IRAM_ATTR ISR_0() { inputs[0] = 1; }
void IRAM_ATTR ISR_1() { inputs[1] = 1; }
void IRAM_ATTR ISR_2() { inputs[2] = 1; }
void IRAM_ATTR ISR_3() { inputs[3] = 1; }

void set_interrupts() {
  attachInterrupt(piezoSensors[0], ISR_0, RISING);
  attachInterrupt(piezoSensors[1], ISR_1, RISING);
  attachInterrupt(piezoSensors[2], ISR_2, RISING);
  attachInterrupt(piezoSensors[3], ISR_3, RISING);
}

void setup() {
  Serial.begin(115200);
  delay(100);
  set_interrupts();
}

void loop() {
  for (int i = 0; i < 4; i++) {
    detachInterrupt(piezoSensors[i]);
  }

  Serial.print("Inputs: ");
  for (int i = 0; i < 4; i++) {
    Serial.print(inputs[i]);
    Serial.print(" ");
    inputs[i] = 0;
  }
  Serial.println();

  set_interrupts();
  delay(200);
}
