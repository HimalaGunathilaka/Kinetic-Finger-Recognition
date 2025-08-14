import serial
import serial.tools.list_ports
import time

def find_esp32_port():
    ports = serial.tools.list_ports.comports()
    for port in ports:
        if "USB" in port.description or "UART" in port.description:
            return port.device
    return None

def read_piezo_serial():
    port = find_esp32_port()
    if not port:
        print("ESP32 not found. Check connection.")
        return

    print(f"Connecting to ESP32 on {port}...")
    ser = serial.Serial(port, 115200, timeout=1)
    time.sleep(2)  # Give time for ESP32 to reset

    try:
        while True:
            line = ser.readline().decode('utf-8').strip()
            print(line)

    except KeyboardInterrupt:
        print("\nStopped by user.")
    finally:
        ser.close()

if __name__ == "__main__":
    read_piezo_serial()
