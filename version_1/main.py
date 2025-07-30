import serial
import re
import vector_visualize as vv
import numpy as np

# Replace with your serial port and baud rate
SERIAL_PORT = '/dev/ttyUSB0'
BAUD_RATE = 115200

# Regular expressions to parse each type of data
accel_re = re.compile(r"Acceleration X:\s*([-\d.]+), Y:\s*([-\d.]+), Z:\s*([-\d.]+)")
gyro_re = re.compile(r"Rotation X:\s*([-\d.]+), Y:\s*([-\d.]+), Z:\s*([-\d.]+)")
# temp_re = re.compile(r"Temperature:\s*([-\d.]+)")

def parse_line(line):
    accel = accel_re.search(line)
    gyro = gyro_re.search(line)
    # temp = temp_re.search(line)

    if accel:
        ax, ay, az = map(float, accel.groups())
        # az = -az
        # ax = -ax
        # ay = -ay
        print(f"Accel: X={ax:.2f}, Y={ay:.2f}, Z={az:.2f} m/s²")
        
        return np.array([ax,ay,az])
        
        # """
        # For visulizing the vector
        # """
        # vv.visualize_vector(vector=[ax,ay,az])
    return np.array([0,0,0])

def main():
    # For initializing the vector visualization
    vv.initialize_graph()
    
    # Initialize old acceleration
    old_acceleration = np.array([0,0,0])

    
    try:
        with serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1) as ser:
            print(f"Connected to {SERIAL_PORT} at {BAUD_RATE} baud.")
            while True:
                try:
                    line = ser.readline().decode('utf-8', errors='ignore').strip()
                    if line:
                        # Newest acceleration
                        new_acceleration = parse_line(line)
                        difference_vector = new_acceleration - old_acceleration
                        vv.visualize_vector(vector=difference_vector)
                except UnicodeDecodeError:
                    continue  # skip malformed lines

    except serial.SerialException as e:
        print(f"Serial connection error: {e}")

if __name__ == "__main__":
    main()
