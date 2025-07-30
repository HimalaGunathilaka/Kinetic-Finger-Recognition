import serial
import numpy as np
from ahrs.filters import Madgwick
from ahrs.common.orientation import q2euler
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from collections import deque
import time

# Serial config
SERIAL_PORT = '/dev/ttyUSB0'
BAUD_RATE = 115200

# Madgwick filter
madgwick = Madgwick()
q = np.array([1.0, 0.0, 0.0, 0.0])  # initial quaternion

# Integration variables
velocity = np.zeros(3)
position = np.zeros(3)

# Time tracking
last_time = None

# For 3D plotting
history = deque(maxlen=500)
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

def update_plot():
    ax.clear()
    data = np.array(history)
    if len(data) > 0:
        ax.plot(data[:, 0], data[:, 1], data[:, 2], color='blue')
        ax.scatter(data[-1, 0], data[-1, 1], data[-1, 2], color='red')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title("Estimated Position from MPU6050")
    plt.pause(0.01)
    
def quaternion_to_matrix(q):
    """
    Convert quaternion to rotation matrix.
    Quaternion format: q = [w, x, y, z]
    """
    w, x, y, z = q
    R = np.array([
        [1 - 2*(y**2 + z**2),     2*(x*y - z*w),       2*(x*z + y*w)],
        [2*(x*y + z*w),           1 - 2*(x**2 + z**2), 2*(y*z - x*w)],
        [2*(x*z - y*w),           2*(y*z + x*w),       1 - 2*(x**2 + y**2)]
    ])
    return R

def parse_line(line):
    # Expected line format:
    # accel_x,accel_y,accel_z,gyro_x,gyro_y,gyro_z,timestamp
    parts = line.split(',')
    if len(parts) < 7:
        return None, None
    try:
        ax_, ay_, az_ = map(float, parts[0:3])
        gx_, gy_, gz_ = map(float, parts[3:6])
        # timestamp = float(parts[6])  # If you want to use Arduino timestamp
        # Convert gyro from degrees/s to radians/s
        gyro_rad = np.radians([gx_, gy_, gz_])
        accel_m_s2 = np.array([ax_, ay_, az_]) * 9.81 / 8.0  # Because Arduino range is ±8g
        # Note: The Arduino MPU6050 readings are in g units? Check if scaling is needed.
        return accel_m_s2, gyro_rad
    except ValueError:
        return None, None

def main():
    global q, velocity, position, last_time

    try:
        with serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1) as ser:
            print(f"Connected to {SERIAL_PORT} at {BAUD_RATE} baud.")
            plt.ion()

            while True:
                try:
                    velocity = np.zeros(3)
                    position = np.zeros(3)
                    line = ser.readline().decode('utf-8', errors='ignore').strip()
                    if not line:
                        continue
                    
                    accel, gyro = parse_line(line)
                    if accel is None or gyro is None:
                        continue

                    # Time step
                    current_time = time.time()
                    if last_time is None:
                        last_time = current_time
                        continue
                    dt = current_time - last_time
                    last_time = current_time

                    # Update orientation
                    q = madgwick.updateIMU(q, gyro, accel)

                    # Remove gravity component
                    g = np.array([0.0, 0.0, 9.81])  # gravity vector
                    # Rotate gravity to sensor frame
                    R = quaternion_to_matrix(q)
                    gravity = R.T @ g

                    linear_accel = accel - gravity  # in m/s²

                    # Integrate to get velocity and position
                    print(linear_accel)
                    velocity += linear_accel * dt
                    position += velocity * dt

                    history.append(position.copy())
                    update_plot()

                except UnicodeDecodeError:
                    continue

    except serial.SerialException as e:
        print(f"Serial connection error: {e}")
    except KeyboardInterrupt:
        print("Exiting...")
        plt.ioff()
        plt.show()

if __name__ == "__main__":
    main()