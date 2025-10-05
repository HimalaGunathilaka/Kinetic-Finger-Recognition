import asyncio
import uinput
from bleak import BleakScanner, BleakClient
from keys import keys


CHAR_UUID = "abcdefab-1234-5678-1234-abcdefabcdef"

# UInput key lookup table
key_map = {
    'a': uinput.KEY_A,
    'b': uinput.KEY_B,
    'c': uinput.KEY_C,
    'd': uinput.KEY_D,
    'e': uinput.KEY_E,
    'f': uinput.KEY_F,
    'g': uinput.KEY_G,
    'h': uinput.KEY_H,
    'i': uinput.KEY_I,
    'j': uinput.KEY_J,
    'k': uinput.KEY_K,
    'l': uinput.KEY_L,
    'm': uinput.KEY_M,
    'n': uinput.KEY_N,
    'o': uinput.KEY_O,
    'p': uinput.KEY_P,
    'q': uinput.KEY_Q,
    'r': uinput.KEY_R,
    's': uinput.KEY_S,
    't': uinput.KEY_T,
    'u': uinput.KEY_U,
    'v': uinput.KEY_V,
    'w': uinput.KEY_W,
    'x': uinput.KEY_X,
    'y': uinput.KEY_Y,
    'z': uinput.KEY_Z,
    'enter': uinput.KEY_ENTER,
    'space': uinput.KEY_SPACE,
    'capslock': uinput.KEY_CAPSLOCK,
    'backspace': uinput.KEY_BACKSPACE,
    'delete' : uinput.KEY_DELETE
}

# Create a virtual keyboard device
device = uinput.Device(list(key_map.values()))

# Handle BLE notifications
def handler(sender, data):
    key_str = data.decode().strip().lower()
    print("Received:", key_str)
    if key_str in keys:
        device.emit_click(key_map[keys[key_str]])
        print(f"Emitted key: {key_str}")
    else:
        print(f"⚠ Unknown key: {key_str}")

async def main():
    print("Scanning for ESP32...")
    device_found = await BleakScanner.find_device_by_name("ESP32-K")
    if not device_found:
        print("ESP32 not found!")
        return

    async with BleakClient(device_found) as client:
        print("Connected to ESP32")
        await client.start_notify(CHAR_UUID, handler)
        print("Listening for notifications...")
        await asyncio.Future()  # keep running

asyncio.run(main())
