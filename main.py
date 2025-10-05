from pynput import keyboard
from ble import is_device_connected

def on_press(key):
    if is_device_connected("ESP32 Keyboard"):
        print("ESP32 Keyboard is connected.")
        try:
            print(f"Key pressed: {key.char}")
        except AttributeError:
            print(f"Special key pressed: {key}")
    else:
        print("ESP32 Keyboard not connected.")

def on_release(key):
    if key == keyboard.Key.esc:
        # Stop listener when ESC is pressed
        return False

listener = keyboard.Listener(on_press=on_press, on_release=on_release)
listener.start()

print("Listening for keypresses... (press ESC to quit)")
listener.join()