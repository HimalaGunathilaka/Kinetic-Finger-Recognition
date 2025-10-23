#ifndef MPU_H
#define MPU_H

#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>
#include <Wire.h>

// Global MPU6050 instance
Adafruit_MPU6050 mpu;

// Configuration constants
const float GYRO_THRESHOLD = 2.0f;        // Threshold for detecting rotation (rad/s)
const int TRAP_DELAY = 500;               // Delay in milliseconds when movement is detected

// Global variables
int gyro_output = 1;                      // Gyro output value to be sent
float maxVal = 0.0f;                      // Maximum value detected by gyro

/**
 * Initialize the MPU6050 sensor
 */
void init_mpu() {
    if (!mpu.begin()) {
        Serial.println("Failed to find MPU6050 chip");
        while (1) {
            delay(10);
        }
    }
    
    Serial.println("MPU6050 Found!");
    
    // Configure sensor settings
    mpu.setGyroRange(MPU6050_RANGE_250_DEG);
    mpu.setFilterBandwidth(MPU6050_BAND_10_HZ);
}

/**
 * Main MPU6050 processing loop
 * Reads gyroscope data and determines movement direction
 */
void mpu_loop() {
    sensors_event_t a, g, temp;
    mpu.getEvent(&a, &g, &temp);

    // Extract gyroscope values
    float gx = g.gyro.x;
    float gy = g.gyro.y;
    float gz = g.gyro.z;

    // Initialize with X-axis values
    maxVal = gx;
    gyro_output = (gx > 0) ? 1 : 2;

    // Check if Y-axis has larger magnitude
    if (abs(gy) > abs(maxVal)) {
        maxVal = gy;
        gyro_output = (gy > 0) ? 3 : 4;
    }

    // Check if Z-axis has the largest magnitude
    if (abs(gz) > abs(maxVal)) {
        maxVal = gz;
        gyro_output = (gz > 0) ? 5 : 6;
    }
}

#endif

/*
    x+ --> 1
    x- --> 2

    y+ --> 3
    y- --> 4

    z (clockwise) --> 6
    z (anticlockwise) --> 5

*/