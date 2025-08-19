#include <Arduino.h>

const int buttonPins[5] = {32, 27, 26, 33, 25};  // GPIOs
volatile int inputs[5] = {0, 0, 0, 0, 0};
bool isTriggered = false;
#define DELAYED 300

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


void setup() {
  Serial.begin(115200);
  delay(100);

  // Set all button pins as input with internal pull-up
  for (int i = 0; i < 5; i++) {
    pinMode(buttonPins[i], INPUT_PULLDOWN);
  }

  set_interrupts();
}

void loop() {
  while (!isTriggered) {
    delay(1);  // Wait until a button is pressed
  }

  delay(DELAYED);  // Debounce delay

  isTriggered = false;

  Serial.print("Button Inputs: ");
  for (int i = 0; i < 5; i++) {
    Serial.print(inputs[i]);
    Serial.print(" ");
    inputs[i] = 0;  // Reset input status
  }
  Serial.println();

  set_interrupts();  // Re-enable interrupts
}