import serial
import re
import numpy as np
from ahrs.filters import Madgwick
from collections import deque
import time

# ----------------------------
# Configuration
# ----------------------------
SERIAL_PORT = '/dev/ttyUSB0'
BAUD_RATE = 115200
SAMPLE_WINDOW = 100  # initial idle samples for gravity
dt = 0.02            # IMU sample interval in seconds

# ----------------------------
# Queues for averaging initial gravity
# ----------------------------
ax_queue = deque(maxlen=SAMPLE_WINDOW)
ay_queue = deque(maxlen=SAMPLE_WINDOW)
az_queue = deque(maxlen=SAMPLE_WINDOW)

# ----------------------------
# Madgwick filter
# ----------------------------
madgwick = Madgwick(Dt=dt)
q = np.array([1.0, 0.0, 0.0, 0.0])  # initial quaternion

# ----------------------------
# Globals for sensor values
# ----------------------------
ax = ay = az = gx = gy = gz = None

# ----------------------------
# Helper functions
# ----------------------------
def quaternion_to_rotation_matrix(q):
    w, x, y, z = q
    R = np.array([
        [1-2*(y**2+z**2), 2*(x*y - z*w), 2*(x*z + y*w)],
        [2*(x*y + z*w), 1-2*(x**2+z**2), 2*(y*z - x*w)],
        [2*(x*z - y*w), 2*(y*z + x*w), 1-2*(x**2+y**2)]
    ])
    return R

def extract_line(line):
    """Extract ax, ay, az, gx, gy, gz from serial line."""
    global ax, ay, az, gx, gy, gz
    if not line:
        return False

    pattern = re.compile(
        r"ax:\s*(-?\d+\.?\d*)\s*ay[,:]?\s*(-?\d+\.?\d*)\s*az[,:]?\s*(-?\d+\.?\d*)\s*gx[,:]?\s*(-?\d+\.?\d*)\s*gy[,:]?\s*(-?\d+\.?\d*)\s*gz[,:]?\s*(-?\d+\.?\d*)"
    )
    match = pattern.search(line)
    if match:
        ax, ay, az, gx, gy, gz = map(float, match.groups())
        return True
    return False

# ----------------------------
# Main Loop
# ----------------------------
with serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1) as ser:
    print("Collecting initial idle samples to determine gravity...")
    gravity_initialized = False
    point_down = None

    while True:
        try:
            line = ser.readline().decode('utf-8', errors='ignore').strip()
            if extract_line(line):
                # Collect initial samples
                if not gravity_initialized:
                    # print(len(ax_queue))
                    ax_queue.append(ax)
                    ay_queue.append(ay)
                    az_queue.append(az)
                    if len(ax_queue) == SAMPLE_WINDOW:
                        # Compute initial gravity vector
                        gravity = np.array([
                            sum(ax_queue)/SAMPLE_WINDOW,
                            sum(ay_queue)/SAMPLE_WINDOW,
                            sum(az_queue)/SAMPLE_WINDOW
                        ])
                        point_down = gravity / np.linalg.norm(gravity)
                        gravity_initialized = True
                        print("Initial gravity vector (unit):", point_down)
                        print("Starting real-time tracking...\n")
                else:
                    # Update orientation with Madgwick filter
                    q = madgwick.updateIMU(q, gyr=np.array([gx, gy, gz]),
                                           acc=np.array([ax, ay, az]))
                    R = quaternion_to_rotation_matrix(q)
                    g_current = R @ point_down
                    print("Current down vector:", np.round(g_current, 3))
            else:
                # Optional: print if line is not parsed
                print("Skipping unrecognized line:", line)

            time.sleep(dt)  # maintain sample rate

        except KeyboardInterrupt:
            print("\nStopping tracking...")
            break
