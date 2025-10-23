#include <Arduino.h>
#include <BleKeyboard.h>
#include "tap.h"
#include "mpu.h"
#include "keys.h"
#include "mpu.h"

#define DELAYED 500

u_int8_t ROTATE_LEFT = 0x01;
u_int8_t ROTATE_RIGHT = 0x02;

// current pack of letters
int head = 0;

BleKeyboard bleKeyboard;

void tapKey(uint8_t key)
{
  bleKeyboard.press(key);
  delay(10); // short delay to simulate a real tap
  bleKeyboard.release(key);
}

String send = "";

void setup()
{
  Serial.begin(115200);
  Serial.println("Starting BLE work!");
  bleKeyboard.begin();
  init_mpu();
  set_interrupts();
  set_pins();
}

void loop()
{
  if (!bleKeyboard.isConnected())
    return;

  mpu_loop();

  // Gesture detection
  if (abs(maxVal) > gyroThreshold)
  {
    switch (gyro_output)
    {
    case 1:
      tapKey(KEY_CAPS_LOCK);
      break;
    case 2:
      tapKey(KEY_NUM_ENTER);
      break;
    case 3:
      tapKey(KEY_DELETE);
      break;
    case 4:
      tapKey(KEY_BACKSPACE);
      break;
    case 5:
      bleKeyboard.print(".");
      break;
    case 6:
      bleKeyboard.print(",");
      break;
    }
    delay(trapDelay);
  }

  // Tap detection
  if (isTriggered)
  {
    // Need to be delayed to capture the specific eventsj
    delay(DELAYED);

    String lookup = "";
    for (int i = 0; i < 5; i++)
    {
      lookup += inputs[i];
      inputs[i] = 0;
    }

    Serial.print("Lookup: ");
    Serial.println(lookup);

    if (lookup == "10000")
    {
      Serial.print("Sending: ");
      Serial.println(order[head].c_str());
      bleKeyboard.print(order[head].c_str());
    }
    else if (lookup == "01000")
    {
      Serial.print("Sending: ");
      Serial.println(order[head + 1].c_str());
      bleKeyboard.print(order[head + 1].c_str());
    }
    else if (lookup == "00100")
    {
      Serial.print("Sending: ");
      Serial.println(order[head + 2].c_str());
      bleKeyboard.print(order[head + 2].c_str());
    }
    else if (lookup == "00010")
    {
      Serial.print("Sending: ");
      Serial.println(order[head + 3].c_str());
      bleKeyboard.print(order[head + 3].c_str());
    }
    else if (lookup == "00001")
    {
      Serial.print("Sending: ");
      Serial.println(order[head + 4].c_str());
      bleKeyboard.print(order[head + 4].c_str());
    }
    else if (lookup == "11000")
    {
      int prev = head;
      head -= 5;
      if (head < 0)
        head += 30;
      head %= 30;
      Serial.print("Rotate left: head ");
      Serial.print(prev);
      Serial.print(" -> ");
      Serial.println(head);

      bleKeyboard.press(KEY_LEFT_CTRL);
      delay(10);
      bleKeyboard.release(KEY_LEFT_CTRL);
    }
    else if (lookup == "00011")
    {
      int prev = head;
      head += 5;
      head %= 30;
      Serial.print("Rotate right: head ");
      Serial.print(prev);
      Serial.print(" -> ");
      Serial.println(head);

      bleKeyboard.press(KEY_RIGHT_CTRL);
      delay(10);
      bleKeyboard.release(KEY_RIGHT_CTRL);
    }
    else
    {
      Serial.print("No match for lookup: ");
      Serial.println(lookup);
    }

    set_interrupts();
    isTriggered = false;
  }
}
