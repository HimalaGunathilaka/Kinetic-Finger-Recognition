/*
[x] Create a BLE device
  [] Import BLE device library
[] Create a server

[] Create Server callbacks

[] Create service

[] Create characteristic

[] Create characteristic callbacks

[]
*/
#include <BLEDevice.h>
#include <BLE2901.h> // For the descriptor - A predefined one / Named descriptor

#define DEVICE_NAME "Himala's ESP32"
#define SERVICE_1_UUID "60907f75-22aa-4d96-987d-655efc5cbcfd"
#define CHARACTERISTIC_1A_UUID "5fa57eaa-3ddb-4f8c-bd94-7cc8cfd6087e"

// Callbacks
class MyServerCallbacks : public BLEServerCallbacks {
  void onConnect(BLEServer *pServer){
    digitalWrite(2,HIGH);
    Serial.println("Client connected");
  }

  void onDisconnect(BLEServer *pServer){
    digitalWrite(2, LOW);
    Serial.println("Client Disconnected");
    BLEDevice::startAdvertising();
  }
};

class MyCharacteristicCallbacks : public BLECharacteristicCallbacks {
  void onRead(BLECharacteristic *pCharacteristic){
    uint32_t currentMillis = millis() / 1000;
    pCharacteristic->setValue(currentMillis);
  }
};

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  Serial.println("ESP32 BLE server setup begining...");

  // Pin modes
  pinMode(2,OUTPUT);

  // Initialize Device
  BLEDevice::init(DEVICE_NAME);

  // Create server
  BLEServer *pServer = BLEDevice::createServer();
  pServer->setCallbacks(new MyServerCallbacks());

  // Services
  BLEService *pService = pServer->createService(SERVICE_1_UUID);

  // Characteristics
  BLECharacteristic *pCharacteristic = pService->createCharacteristic(
    CHARACTERISTIC_1A_UUID,
    BLECharacteristic::PROPERTY_READ | BLECharacteristic::PROPERTY_WRITE
  );

  pCharacteristic->setCallbacks(new MyCharacteristicCallbacks());

  // Descriptors
  BLE2901 *pDescriptor_2901 = new BLE2901();
  pDescriptor_2901->setDescription("Time");
  pCharacteristic->addDescriptor(pDescriptor_2901);

  pService->start();

  // Start Advertising
  BLEDevice::startAdvertising();

}

void loop() {
  // put your main code here, to run repeatedly:

}
