import asyncio
from bleak import BleakScanner, BleakClient

CHAR_UUID = "abcdefab-1234-5678-1234-abcdefabcdef"

def handler(sender, data):
    print("Received:", data.decode())

async def main():
    print("Scanning for ESP32...")
    device = await BleakScanner.find_device_by_name("ESP32-K")
    if not device:
        print("ESP32 not found!")
        return

    async with BleakClient(device) as client:
        print("Connected to ESP32")
        await client.start_notify(CHAR_UUID, handler)
        print("Listening for notifications...")
        await asyncio.Future()  # run forever

asyncio.run(main())
