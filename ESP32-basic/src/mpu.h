#ifndef MPU_H
#define MPU_H

#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>
#include <Wire.h>

Adafruit_MPU6050 mpu;

// Threshold for detecting rotation (rad/s)
float gyroThreshold = 2;
// gyro_output that should be sent
// When detect movement delay the all functionalities for this number of milliseconds
int gyro_output = 1;
// Obiviously other than ISR
int trapDelay = 500;

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
    if (gx > 0)
    {
        gyro_output = 1;
    }
    else
    {
        gyro_output = 2;
    }

    if (abs(gy) > abs(maxVal))
    {
        maxVal = gy;
        if (gx > 0)
        {
            gyro_output = 3;
        }
        else
        {
            gyro_output = 4;
        }
    }

    if (abs(gz) > abs(maxVal))
    {
        maxVal = gz;
        if (gx > 0)
        {
            gyro_output = 5;
        }
        else
        {
            gyro_output = 6;
        }
    }
}

#endif
