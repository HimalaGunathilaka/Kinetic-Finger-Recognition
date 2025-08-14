import serial
import time

# Import your existing visualization functions from the file or copy-paste them here
import matplotlib.pyplot as plt

fig = None
ax = None

def initialize_graph(xlim=[-15, 15], ylim=[-15, 15], zlim=[-15, 15]):
    global fig, ax

    plt.ion()
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')

    ax.set_xlim(xlim)
    ax.set_ylim(ylim)
    ax.set_zlim(zlim)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.grid(True)
    ax.set_title('3D Vector Visualization')

    plt.show()

def visualize_vector(vector, origin=[0, 0, 0], color='blue', label=None):
    global fig, ax

    if ax is None:
        print("Graph not initialized. Call initialize_graph() first.")
        return

    ax.clear()

    # Dynamically update limits based on vector components with margin
    margin = 2
    xmin = min(0, vector[0]) - margin
    xmax = max(0, vector[0]) + margin
    ymin = min(0, vector[1]) - margin
    ymax = max(0, vector[1]) + margin
    zmin = min(0, vector[2]) - margin
    zmax = max(0, vector[2]) + margin

    ax.set_xlim([xmin, xmax])
    ax.set_ylim([ymin, ymax])
    ax.set_zlim([zmin, zmax])

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.grid(True)
    ax.set_title('3D Vector Visualization')

    ax.quiver(origin[0], origin[1], origin[2],
              vector[0], vector[1], vector[2],
              color=color, arrow_length_ratio=0.1, linewidth=2)

    if label:
        ax.text(origin[0] + vector[0]/2,
                origin[1] + vector[1]/2,
                origin[2] + vector[2]/2,
                label, fontsize=12)

    plt.draw()
    plt.pause(0.01)

def parse_line(line):
    """Parse line like:
    gyro_x, gyro_y, gyro_z, accel_x, accel_y, accel_z
    Return accel vector or None"""
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
    SERIAL_PORT = '/dev/ttyUSB0'  # Change this to your serial port
    BAUD_RATE = 115200

    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    initialize_graph()

    try:
        while True:
            line = ser.readline().decode('utf-8', errors='ignore')
            accel = parse_line(line)
            if accel:
                visualize_vector(accel, color='red', label='Acceleration')
            else:
                # No valid data, just wait a bit
                time.sleep(0.01)
    except KeyboardInterrupt:
        print("Exiting...")
        plt.ioff()
        plt.show()

if __name__ == "__main__":
    main()
