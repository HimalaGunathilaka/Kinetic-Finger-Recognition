#include <Arduino.h>
#include "SPIFFS.h"

struct __attribute__((packed)) Entry {
  uint16_t hash;
  float probability;
};

void setup() {
  Serial.begin(115200);
  delay(1000);

  if (!SPIFFS.begin(true)) {
    Serial.println("SPIFFS Mount Failed!");
    return;
  }

  File file = SPIFFS.open("/lookup.bin", "r");
  if (!file) {
    Serial.println("Failed to open lookup.bin");
    return;
  }

  Serial.println("Reading hashed lookup table:");
  while (file.available()) {
    uint8_t buf[6];
    int readBytes = file.read(buf, 6);
    if (readBytes < 6) break;

    // Decode manually (safe against padding)
    uint16_t hash = buf[0] | (buf[1] << 8);

    float prob;
    memcpy(&prob, &buf[2], sizeof(float));  // raw float bytes

    char first = (hash >> 8) & 0xFF;
    char second = hash & 0xFF;
    Serial.printf("%c%c (hash=%u) -> %.6f\n", first, second, hash, prob);
  }

  file.close();
  Serial.println("Done reading lookup table.");
}

void loop() {}


// #include <Arduino.h>
// #include "SPIFFS.h"

// void setup() {
//   Serial.begin(115200);
//   if (SPIFFS.begin(true)) {
//     Serial.println("SPIFFS formatted and mounted!");
//   } else {
//     Serial.println("SPIFFS mount failed!");
//   }
// }

// void loop() {}
