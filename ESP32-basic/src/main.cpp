#include <Arduino.h>
#include <BleKeyboard.h>
#include "tap.h"
#include "mpu.h"
#include "keys.h"

#define DELAYED 300

BleKeyboard bleKeyboard;

void setup()
{
  Serial.begin(115200);
  Serial.println("Starting BLE work!");
  bleKeyboard.begin();
  // init_mpu();
  set_interrupts();
  set_pins();
}

void loop()
{
  if (bleKeyboard.isConnected())
  {
    while (!isTriggered)
    {
      delay(1);
    }
    delay(DELAYED);

    String lookup ="";

    // Concatanate the interrupts inputs
    for(int i = 0; i <5; i++){
      lookup += String(inputs[i]);
      inputs[i] = 0;
    }

    auto it = keys.find(lookup.c_str());
    String output = (it != keys.end()) ? String(it->second.c_str()) : "";

    bleKeyboard.print(output);
    Serial.println(output);

    set_interrupts();
    isTriggered = false;
  }
}
