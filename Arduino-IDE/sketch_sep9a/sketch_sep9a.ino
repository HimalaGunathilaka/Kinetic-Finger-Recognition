#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>
#include <Wire.h>

Adafruit_MPU6050 mpu;

// Threshold for detecting rotation (rad/s)
float gyroThreshold = 2;  // Adjust as needed
int sampleDelay = 20;       // Sampling interval in ms (50 Hz)
int output = 0;
int trapDelay = 400;

void setup() {
  Serial.begin(115200);
  while (!Serial) delay(10);

  Serial.println("MPU6050 Gyro Fine Motion Test");

  if (!mpu.begin()) {
    Serial.println("Failed to find MPU6050 chip");
    while (1) delay(10);
  }
  Serial.println("MPU6050 Found!");

  mpu.setGyroRange(MPU6050_RANGE_250_DEG);     // ±500 deg/s
  mpu.setFilterBandwidth(MPU6050_BAND_10_HZ);  // Smooth out noise
}

void loop() {
  sensors_event_t a, g, temp;
  mpu.getEvent(&a, &g, &temp);

  float gx = g.gyro.x;
  float gy = g.gyro.y;
  float gz = g.gyro.z;

  // Find largest absolute rotation
  float maxVal = gx;
  if (gx > 0) {
    output = 1;
  } else {
    output = -1;
  }

  if (abs(gy) > abs(maxVal)) {
    maxVal = gy;
    if (gx > 0) {
      output = 2;
    } else {
      output = -2;
    }
  }
  if (abs(gz) > abs(maxVal)) {
    maxVal = gz;
    if (gx > 0) {
      output = 3;
    } else {
      output = -3;
    }
  }

  // Check against threshold
  if (abs(maxVal) > gyroThreshold) {
    Serial.print("Rotation detected on axis ");
    Serial.println(output);
    delay(trapDelay);
  }
  output = 0;

  delay(sampleDelay);
}
