#include "ble.h"

BLEManager::BLEManager() : pCharacteristic(nullptr), deviceConnected(false) {}

void BLEManager::init(const char *name)
{
    BLEDevice::init(name);
    BLEServer *pServer = BLEDevice::createServer();
    pServer->setCallbacks(this);

    BLEService *pService = pServer->createService("12345678-1234-1234-1234-1234567890ab");
    pCharacteristic = pService->createCharacteristic(
        "abcdefab-1234-5678-1234-abcdefabcdef",
        BLECharacteristic::PROPERTY_NOTIFY);

    pService->start();
    pServer->getAdvertising()->start();
}

void BLEManager::notify(const std::string &msg)
{
    if (deviceConnected && pCharacteristic)
    {
        pCharacteristic->setValue(msg);
        pCharacteristic->notify();
    }
}

void BLEManager::onConnect(BLEServer *pServer)
{
    deviceConnected = true;
}

void BLEManager::onDisconnect(BLEServer *pServer)
{
    deviceConnected = false;
    pServer->getAdvertising()->start();
}