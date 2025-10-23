from pynput import keyboard

def on_press(key):
    try:
        print(f"Character key: '{key.char}'")
    except AttributeError:
        print(f"Special key: '{str(key)}'")

print("Press keys to see their string representation. Press Ctrl+C to exit.")
print("Try pressing the left control key...")

listener = keyboard.Listener(on_press=on_press)
listener.start()

try:
    listener.join()
except KeyboardInterrupt:
    print("\nExiting...")
    listener.stop()