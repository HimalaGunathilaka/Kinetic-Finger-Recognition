import serial

# Serial config
SERIAL_PORT = '/dev/ttyUSB0'
BAUD_RATE = 115200


with serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1) as ser:
    while True:
        line = ser.readline().decode('utf-8', errors='ignore').strip()
        if line:
            print(line)
        else: 
            break
