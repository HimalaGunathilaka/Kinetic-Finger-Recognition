#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>
#include <Wire.h>

Adafruit_MPU6050 mpu;

// Threshold for detecting rotation (rad/s)
float gyroThreshold = 2;
// output that should be sent
// When detect movement delay the all functionalities for this number of milliseconds
String output = "";
// Obiviously other than ISR
int trapDelay = 800;

// Max value by gyro of the mpu
float maxVal = .0f;

void init_mpu()
{
    if (!mpu.begin())
    {
        Serial.println("Failed to find MPU6050 chip");
        while (1)
            delay(10);
    }
    Serial.println("MPU6050 Found!");

    mpu.setGyroRange(MPU6050_RANGE_250_DEG);
    mpu.setFilterBandwidth(MPU6050_BAND_10_HZ);
}

void mpu_loop()
{
    sensors_event_t a, g, temp;
    mpu.getEvent(&a, &g, &temp);

    float gx = g.gyro.x;
    float gy = g.gyro.y;
    float gz = g.gyro.z;

    // Capture the maximum value by the mpu
    maxVal = gx;
    if (gx > 0){ output = "1"; }
    else{ output = "2"; }

    if (abs(gy) > abs(maxVal))
    {
        maxVal = gy;
        if (gx > 0){ output = "3"; }
        else{ output = "4"; }
    }

    if (abs(gz) > abs(maxVal))
    {
        maxVal = gz;
        if (gx > 0){ output = "5"; }
        else{ output = "6"; }
    }
}