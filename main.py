import serial
import serial.tools.list_ports
import time
import re
import uinput
from keys import keys  # your signal-to-key mapping

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
    'backspace': uinput.KEY_BACKSPACE
}

def find_esp32_port():
    ports = serial.tools.list_ports.comports()
    for port in ports:
        if "USB" in port.description or "UART" in port.description:
            return port.device
    return None

def main():
    port = find_esp32_port()
    if not port:
        print("ESP32 not found.")
        return

    print(f"Connecting to ESP32 on {port}...")
    ser = serial.Serial(port, 115200, timeout=1)
    time.sleep(2)

    shift_next = False

    # Define all possible events for uinput device
    events = list(set(key_map.values()) | {uinput.KEY_LEFTSHIFT})
    device = uinput.Device(events)

    try:
        while True:
            line = ser.readline().decode('utf-8').strip()
            if line:
                signal = ''.join(re.findall(r'\d+', line))
                if signal in keys:
                    word = keys[signal]
                    if word == 'shift':
                        shift_next = True
                        continue

                    key = key_map.get(word.lower())
                    if not key:
                        print(f"[!] Unknown key mapping: '{word}'")
                        continue

                    if shift_next and word.isalpha():
                        device.emit_combo([uinput.KEY_LEFTSHIFT, key])
                        shift_next = False
                    else:
                        device.emit_click(key)

                    print(f"[+] Sent key: {word}")
                else:
                    print(f"[-] Unknown signal: {signal}")
    except Exception as e:
        print(f"[!] Error: {e}")
    finally:
        ser.close()

if __name__ == "__main__":
    main()
