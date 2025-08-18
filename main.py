import serial
import serial.tools.list_ports
import time
import re
import keyboard  # Simulates key presses
from keys import keys  # Your custom signal-to-key dictionary

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

    try:
        while True:
            line = ser.readline().decode('utf-8').strip()
            if line:
                signal = ''.join(re.findall(r'\d+', line))
                if signal in keys:
                    word = keys[signal]
                    if word == "space":
                        keyboard.write(" ")
                    elif word == "enter":
                        keyboard.send("enter")
                    elif word == "backspace":
                        keyboard.send("backspace")
                    elif word == "shift":
                        shift_next = True
                    else:
                        char = word.upper() if shift_next else word
                        shift_next = False
                        keyboard.write(char)
                else:
                    print(f"Unknown signal: {signal}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        ser.close()

if __name__ == "__main__":
    main()
