import matplotlib.pyplot as plt

# Global variables to store the figure and axis
fig = None
ax = None

def initialize_graph(xlim=[-15, 15], ylim=[-15, 15], zlim=[-15, 15]):
    """
    Initialize the 3D graph for vector visualization

    Args:
        xlim: X-axis limits as [min, max]
        ylim: Y-axis limits as [min, max]
        zlim: Z-axis limits as [min, max]
    """
    global fig, ax

    plt.ion()  # Turn on interactive mode for real-time updates

    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')

    # Set axis properties
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
    """
    Visualize a vector, clearing any previously displayed vectors

    Args:
        vector: The vector to visualize as [x, y, z]
        origin: Starting point of the vector as [x, y, z]
        color: Color of the vector arrow
        label: Optional label for the vector
    """
    global fig, ax

    if ax is None:
        print("Graph not initialized. Call initialize_graph() first.")
        return

    # Clear previous vectors
    ax.clear()

    # Restore axis properties
    xlim = ax.get_xlim() if hasattr(ax, '_xlim') else [-15, 15]
    ylim = ax.get_ylim() if hasattr(ax, '_ylim') else [-15, 15]
    zlim = ax.get_zlim() if hasattr(ax, '_zlim') else [-15, 15]

    ax.set_xlim(xlim)
    ax.set_ylim(ylim)
    ax.set_zlim(zlim)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.grid(True)
    ax.set_title('3D Vector Visualization')

    # Draw the vector
    ax.quiver(origin[0], origin[1], origin[2],
              vector[0], vector[1], vector[2],
              color=color, arrow_length_ratio=0.1, linewidth=2)

    # Add label if provided
    if label:
        ax.text(origin[0] + vector[0]/2,
                origin[1] + vector[1]/2,
                origin[2] + vector[2]/2,
                label, fontsize=12)

    # Update the display
    plt.draw()
    plt.pause(0.01)

# Example usage:
if __name__ == "__main__":
    # Initialize the graph
    initialize_graph()

    # Visualize different vectors
    import time

    vectors = [
        [1, 2, 1],
        [2, -1, 2],
        [-1.5, 1.5, -1],
        [0, 0, 3],
        [2.5, 0, 0]
    ]

    for i, vec in enumerate(vectors):
        visualize_vector(vec, color='red', label=f'Vector {i+1}')
        time.sleep(1)  # Wait 1 second between vectors

    plt.ioff()  # Turn off interactive mode
    input("Press Enter to close...")