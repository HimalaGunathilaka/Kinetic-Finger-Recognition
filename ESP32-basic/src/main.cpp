#include <Arduino.h>
#include <BleKeyboard.h>
#include "tap.h"
#include "mpu.h"
#include "keys.h"

// Constants
#define DELAYED 500

const u_int8_t ROTATE_LEFT = 0x01;
const u_int8_t ROTATE_RIGHT = 0x02;

// Global variables
int head = 0;                             // Current pack of letters
BleKeyboard bleKeyboard;

String send = "";

// keys to press
void tapKey(uint8_t key)
{
  bleKeyboard.press(key);
  delay(10); // short delay to simulate a real tap
  bleKeyboard.release(key);
}

/**
 * Arduino setup function - initializes all components
 */
void setup() {
    Serial.begin(115200);
    Serial.println("Starting BLE work!");
    
    // Initialize components
    bleKeyboard.begin();
    init_mpu();
    set_interrupts();
    set_pins();
}

/**
 * Main Arduino loop function
 */
void loop() {
    if (!bleKeyboard.isConnected()) {
        return;
    }

    mpu_loop();

    // Gesture detection
    if (abs(maxVal) > GYRO_THRESHOLD) {
        switch (gyro_output) {
            case 1:
              tapKey(KEY_CAPS_LOCK);
            break;
            case 2:
              tapKey(KEY_NUM_ENTER);
            break;
            case 3: {
              tapKey(KEY_LEFT_ARROW);
            break;
            }
            case 4: {
              tapKey(KEY_RIGHT_ARROW);
            break;
            }
            case 5:
              head -= 5;
              if (head < 0) { 
                head += 30;
              }
              head %= 30;
              tapKey(KEY_LEFT_CTRL);
            break;
            case 6:
              head += 5;
              head %= 30;
              tapKey(KEY_RIGHT_CTRL);
        }
        delay(TRAP_DELAY);
    }

    // Tap detection
    if (isTriggered) {
        // Need to be delayed to capture the specific events
        delay(DELAYED);

        String lookup = "";
        for (int i = 0; i < 5; i++) {
            lookup += inputs[i];
            inputs[i] = 0;
        }

        Serial.print("Lookup: ");
        Serial.println(lookup);

        // Process tap patterns
        if (lookup == "10000") { 
            bleKeyboard.print(order[head].c_str()); 
        }
        else if (lookup == "01000") { 
            bleKeyboard.print(order[head + 1].c_str()); 
        }
        else if (lookup == "00100") { 
            bleKeyboard.print(order[head + 2].c_str()); 
        }
        else if (lookup == "00010") { 
            bleKeyboard.print(order[head + 3].c_str()); 
        }
        else if (lookup == "00001") { 
            bleKeyboard.print(order[head + 4].c_str()); 
        }
        else if (lookup == "11000") {
            tapKey(KEY_BACKSPACE);
        }
        else if (lookup == "00011") {
            tapKey(KEY_DELETE);
        }
        else {
            Serial.print("No match for lookup: ");
            Serial.println(lookup);
        }

        set_interrupts();
        isTriggered = false;
    }
}
