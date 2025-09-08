#ifndef BLE_H
#define BLE_H

#include <BLEDevice.h>
#include <BLEUtils.h>
#include <BLEServer.h>

class BLEManager : public BLEServerCallbacks
{
public:
    BLEManager();
    void init(const char *name);
    void notify(const std::string &msg);

    void onConnect(BLEServer *pServer) override;
    void onDisconnect(BLEServer *pServer) override;

private:
    BLECharacteristic *pCharacteristic;
    bool deviceConnected;
};

#endif