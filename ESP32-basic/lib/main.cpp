#include <Arduino.h>
#include <Adafruit_MPU6050.h>
#include <Wire.h>

#include "tap.h"

#define DELAYED 300

Adafruit_MPU6050 mpu;

void setup()
{
  Serial.begin(115200);
  delay(100);

  // Set all button pins as input with internal pull-up
  for (int i = 0; i < 5; i++)
  {
    pinMode(buttonPins[i], INPUT_PULLDOWN);
  }

  set_interrupts();

  // Initialize the accelerometer
  if (!mpu.begin())
  {
    while (1)
    {
      delay(10);
    }
  }

  // Set gyro range to +- 250 deg/s
  mpu.setGyroRange(MPU6050_RANGE_250_DEG);

  // Set filter bandwidth to 21 Hz
  mpu.setFilterBandwidth(MPU6050_BAND_21_HZ);

  delay(100);
}

void loop()
{
  while (!isTriggered)
  {
    delay(1); // Wait until a button is pressed
  }

  delay(DELAYED); // Debounce delay

  isTriggered = false;

  if (gyroZ)
  {
    attachInterrupt(buttonPins[2], ISR_2, RISING);
  }
  while (gyroZ)
  {
    sensors_event_t a, g, temp;
    mpu.getEvent(&a, &g, &temp);
    Serial.println(g.gyro.z);
  }

  Serial.print("Button Inputs: ");
  for (int i = 0; i < 5; i++)
  {
    Serial.print(inputs[i]);
    Serial.print(" ");
    inputs[i] = 0; // Reset input status
  }

  Serial.println();

  set_interrupts(); // Re-enable interrupts
}