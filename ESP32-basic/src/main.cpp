#include <Arduino.h>

const int piezoSensors[5] = {19, 18, 26, 25,33};
volatile int inputs[5] = {0, 0, 0, 0, 0};
bool isTriggered = false;

void IRAM_ATTR ISR_0() { inputs[0] = 1; isTriggered = true; detachInterrupt(piezoSensors[0]);}
void IRAM_ATTR ISR_1() { inputs[1] = 1; isTriggered = true; detachInterrupt(piezoSensors[1]);}
void IRAM_ATTR ISR_2() { inputs[2] = 1; isTriggered = true; detachInterrupt(piezoSensors[2]);}
void IRAM_ATTR ISR_3() { inputs[3] = 1; isTriggered = true; detachInterrupt(piezoSensors[3]);}
void IRAM_ATTR ISR_4() { inputs[4] = 1; isTriggered = true; detachInterrupt(piezoSensors[4]);}

void set_interrupts() {
  attachInterrupt(piezoSensors[0], ISR_0, RISING);
  attachInterrupt(piezoSensors[1], ISR_1, RISING);
  attachInterrupt(piezoSensors[2], ISR_2, RISING);
  attachInterrupt(piezoSensors[3], ISR_3, RISING);
  attachInterrupt(piezoSensors[4], ISR_4, RISING);
}

void setup() {
  Serial.begin(115200);
  delay(100);
  set_interrupts();
}

void loop() {

  while(!isTriggered){
    delay(1);
  }
  delay(200);

  isTriggered = false;
  
  Serial.print("Inputs: ");
  for (int i = 0; i < 5; i++) {
    Serial.print(inputs[i]);
    Serial.print(" ");
    inputs[i] = 0;
  }
  Serial.println();

  set_interrupts();
}
