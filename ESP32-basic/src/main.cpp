#include <Arduino.h>
#include "ble.h"
#include "tap.h"

#define DELAYED 300
String msg = "";

BLEManager ble;

void setup()
{
  Serial.begin(115200);
  ble.init("ESP32-K");
  set_interrupts();
  set_pins();
}

void loop()
{
  while (!isTriggered)
  {
    delay(1);
  }

  delay(DELAYED); // Wait until all relevant buttons are pressed
  
  Serial.print("Button pressed!");
  msg = "";
  
  for (int i = 0; i < 5; i++)
  {
    msg+=String(inputs[i]);
    inputs[i] = 0;
  }
  ble.notify(msg.c_str());
  set_interrupts();

  isTriggered = false;
}