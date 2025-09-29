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
0 = Madgwick()
q = np.array([1.0, 0.0, 0.0, 0.0])  # initial quaternion

# Integration variables
velocity = np.zeros(3)
position = np.zeros(3)

# Time tracking
last_time = None

# Low-pass filter for accelerometer data
ALPHA = 0.8  # Filter coefficient (0 < alpha < 1, higher = less filtering)
filtered_accel = np.zeros(3)

# Calibration bias (from idle recording analysis)
# These values represent the average drift when sensor is stationary
ACCEL_BIAS = np.array([0.33, -0.29, 1.97])  # X, Y, Z bias from idle data

# For 3D plotting
history = deque(maxlen=500)
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
cube_lim = 0.5
ax.set_xlim([-cube_lim, cube_lim])
ax.set_ylim([-cube_lim, cube_lim])
ax.set_zlim([-cube_lim, cube_lim])
ax.set_box_aspect([1,1,1])  # keep the cube aspect ratio fixed

# Plot optimization variables
plot_update_counter = 0
PLOT_UPDATE_INTERVAL = 5  # Update plot every N iterations
line_plot = None
point_plot = None


def update_plot():
    global line_plot, point_plot
    
    data = np.array(history)
    if len(data) == 0:
        return
    
    # Clear only the plot data, not the entire axes
    if line_plot is not None:
        line_plot.remove()
    if point_plot is not None:
        point_plot.remove()
    
    # Plot the trajectory and current position
    line_plot = ax.plot(data[:, 0], data[:, 1], data[:, 2], color='blue', alpha=0.7)[0]
    point_plot = ax.scatter(data[-1, 0], data[-1, 1], data[-1, 2], color='red', s=50)
    
    # Set fixed axis limits to prevent dynamic resizing (only once after clearing)
    ax.set_xlim([-cube_lim, cube_lim])
    ax.set_ylim([-cube_lim, cube_lim])
    ax.set_zlim([-cube_lim, cube_lim])
    ax.set_box_aspect([1,1,1])
    
    # Set labels and title (only if not already set)
    if not ax.get_xlabel():
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        ax.set_title("Estimated Position from MPU6050 - Symbol Capture")
    
    plt.pause(0.001)  # Reduced pause time for better performance
    
def quaternion_to_matrix(q):
    """
    Convert quaternion to rotation matrix (optimized).
    Quaternion format: q = [w, x, y, z]
    """
    w, x, y, z = q
    
    # Pre-calculate common terms to avoid redundant computation
    xx, yy, zz = x*x, y*y, z*z
    xy, xz, yz = x*y, x*z, y*z
    wx, wy, wz = w*x, w*y, w*z
    
    # Build rotation matrix with pre-calculated terms
    R = np.array([
        [1 - 2*(yy + zz),     2*(xy - wz),       2*(xz + wy)],
        [2*(xy + wz),         1 - 2*(xx + zz),   2*(yz - wx)],
        [2*(xz - wy),         2*(yz + wx),       1 - 2*(xx + yy)]
    ])
    return R

def parse_line(line):
    # Expected line format: accel_x,accel_y,accel_z,gyro_x,gyro_y,gyro_z
    if not line or line.count(',') < 5:  # Quick validation
        return None, None
    
    try:
        # More efficient parsing - avoid intermediate list creation
        parts = line.split(',', 5)  # Only split what we need
        
        # Parse accelerometer data (with calibration offsets)
        ax_ = float(parts[0]) + 1.2
        ay_ = float(parts[1]) + 0.98
        az_ = float(parts[2])
        accel_m_s2 = np.array([ax_, ay_, az_]) * 1.22625  # Pre-calculated 9.81/8.0
        
        # Parse gyroscope data and convert to radians
        gx_ = float(parts[3]) * 0.017453292519943295  # Pre-calculated pi/180
        gy_ = float(parts[4]) * 0.017453292519943295
        gz_ = float(parts[5]) * 0.017453292519943295
        gyro_rad = np.array([gx_, gy_, gz_])
        
        return accel_m_s2, gyro_rad
    except (ValueError, IndexError):
        return None, None

def main():
    global q, velocity, position, last_time

    try:
        with serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1) as ser:
            print(f"Connected to {SERIAL_PORT} at {BAUD_RATE} baud.")
            plt.ion()

            # Symbol capture timing
            symbol_start_time = time.time()
            SYMBOL_DURATION = 2.0  # Capture each symbol for 2 seconds
            
            while True:
                try:
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

                    # Apply low-pass filter to reduce noise
                    global filtered_accel
                    filtered_accel = ALPHA * accel + (1 - ALPHA) * filtered_accel

                    # Remove gravity component only in Z-axis and calibration bias
                    linear_accel = filtered_accel.copy()
                    linear_accel[2] -= 9.81  # Remove gravity from Z-axis only
                    linear_accel -= ACCEL_BIAS  # Remove calibration bias from all axes

                    # Integrate to get velocity and position
                    velocity += linear_accel * dt
                    position += velocity * dt

                    # Reset position for new symbol capture
                    print("velocity:",velocity)
                    print("Linear accerleration:",linear_accel)
                    if current_time - symbol_start_time >= SYMBOL_DURATION:
                        position = np.zeros(3)
                        velocity = np.zeros(3)
                        history.clear()
                        symbol_start_time = current_time

                    history.append(position.copy())
                    
                    # Optimize plot updates - only update every few iterations
                    global plot_update_counter
                    plot_update_counter += 1
                    if plot_update_counter >= PLOT_UPDATE_INTERVAL:
                        update_plot()
                        plot_update_counter = 0

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