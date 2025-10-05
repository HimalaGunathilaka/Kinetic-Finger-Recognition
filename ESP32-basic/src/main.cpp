#include <BleKeyboard.h>
#include <Arduino.h>

BleKeyboard bleKeyboard;

void setup() {
  Serial.begin(115200);
  Serial.println("Starting BLE work!");
  bleKeyboard.begin();
  if(bleKeyboard.isConnected()) {
    Serial.println("Sending 'Hello world'...");
    bleKeyboard.print("Hello world");
  
    delay(1000);
  
    Serial.println("Sending Enter key...");
    bleKeyboard.write(KEY_RETURN);
  
    delay(1000);
  
    Serial.println("Sending Play/Pause media key...");
    bleKeyboard.write(KEY_MEDIA_PLAY_PAUSE);
  
    delay(1000);
  }
}

void loop() {

  Serial.println("Waiting 5 seconds...");
  delay(5000);
}