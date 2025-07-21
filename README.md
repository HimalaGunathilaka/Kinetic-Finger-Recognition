# Kinetic-Finger-Recognition
The project is aming to use finger tapping and motion for symbol recognition and drawing.
# About the project
---
The hand is the most frequently used organ of the body for performing fine tasks. This project aims to leverage that by recognizing drawn symbols and aiding digital drawing through hand gestures.

The system involves building a glove-like wearable device capable of detecting taps and finger movements on a surface.

## Functional objectives

| Function                                                  | Module or feature of use                                                                                                                                                                                                                                                          |
| --------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Identifying taps                                          | ![Piezo Sensor Plate 35mm](https://img.drz.lazcdn.com/static/lk/p/05ac26c5149de16ac768cda79522c684.jpg_720x720q80.jpg_.webp)<br><br> Piezo Sensor                                                                                                                                 |
| Identifying the motion of a finger on surface  (Option 1) | Optical Sensor  [](https://tronic.lk/shop/products)<br><br>[![ADNS-9800 Optical Sensor with ADNS-6190-002 Lens](https://tronic.lk/assets/uploads/80d5fb78c6c2f0a1dc40f053c3c52956.jpg)](https://tronic.lk/product/adns-9800-optical-sensor-with-adns-6190-002-lens#)              |
| (Option 2)                                                | Accelerometer  [](https://tronic.lk/shop/products)<br><br>[![ADXL345 Triple Digital Accelerometer Module for Arduino](https://tronic.lk/assets/uploads/6450b2bc95ac186b86a6d8ee0cc57627.jpg)](https://tronic.lk/product/adxl345-triple-digital-accelerometer-module-for-arduino#) |
| Mode of communication                                     | Plan to use ESP32-S3 super mini, since it is small and has inbuilt BLE capability. ![ESP32-S3 Super Mini](https://www.duino.lk/wp-content/uploads/2025/04/COM0320-5.jpg)

# Timeline

| Week  | Objective                                                                                                                            |
| ----- | ------------------------------------------------------------------------------------------------------------------------------------ |
| 1~2   | Mount an accelerometer on a finger and evaluate motion capture reliability. If ineffective, switch to the optical sensor.      |
| 2~3   | Calibrate and test piezo sensors for tap detection. Build safety circuits for them.                                     |
| 3~4   | Visualize pointer finger movement on screen when in contact with a surface. Develop a basic drawing canvas. |
| 4~5   | Train a machine learning model to recognize drawn symbols.                                                                              |
| 5~6   | Map functional inputs like Shift, Enter, etc., to other fingers.                                                                          |
| 6~7   |                                                                                                                                      |
| 7~8   |                                                                                                                                      |
| 8~9   |                                                                                                                                      |
| 9~10  |                                                                                                                                      |
| 10~11 |                                                                                                                                      |
| 11~12 |                                                                                                                                      |

