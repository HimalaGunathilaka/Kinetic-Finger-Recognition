import serial
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401
import numpy as np

SERIAL_PORT = '/dev/ttyUSB0'  # Update to your port
BAUD_RATE = 115200

def parse_line(line):
    try:
        parts = line.strip().split(',')
        if len(parts) != 6:
            return None
        values = list(map(float, parts))
        accel = values[3:6]
        return accel
    except:
        return None

def main():
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    plt.ion()
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    margin = 2

    while True:
        line = ser.readline().decode('utf-8', errors='ignore')
        accel = parse_line(line)
        if accel:
            x, y, z = accel

            ax.clear()
            ax.set_xlabel('Accel X (m/s²)')
            ax.set_ylabel('Accel Y (m/s²)')
            ax.set_zlabel('Accel Z (m/s²)')

            # Set axis limits dynamically centered around the current vector with margin
            ax.set_xlim([-20, 20])
            ax.set_ylim([-20, 20])
            ax.set_zlim([-20, 20])

            # Draw an arrow from origin (0,0,0) to (x,y,z)
            ax.quiver(0, 0, 0, x, y, z, length=1, normalize=True, color='r')

            plt.draw()
            plt.pause(0.01)

if __name__ == "__main__":
    main()
