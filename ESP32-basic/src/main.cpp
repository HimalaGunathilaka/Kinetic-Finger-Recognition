#include "FS.h"
#include "SPIFFS.h"

void setup() {
  Serial.begin(115200);
  if (!SPIFFS.begin(true)) {
    Serial.println("SPIFFS Mount Failed!");
    return;
  }

  Serial.println("SPIFFS mounted successfully.");

  File file = SPIFFS.open("/test.txt", "r");
  if (!file) {
    Serial.println("Failed to open /test.txt");
    return;
  }

  Serial.println("Reading file contents:\n");
  while (file.available()) {
    Serial.write(file.read());
  }

  file.close();
  Serial.println("\n\n--- File read complete ---");
}

void loop() {}
