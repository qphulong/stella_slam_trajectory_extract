import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy.spatial.transform import Rotation as R
from matplotlib.animation import FuncAnimation
from pprint import pprint
from typing import List
import math

def visualize_quaternion_animation(quaternions:List[List[float]]):
    """
    Animate a series of quaternions as 3D rotations, including the origin axes.
    :param quaternions: List of quaternions as [[x, y, z, w], ...]
    """
    # Normalize the quaternions
    quaternions = [q / np.linalg.norm(q) for q in quaternions]

    # Set up the figure
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.set_xlim([-1, 1])
    ax.set_ylim([-1, 1])
    ax.set_zlim([-1, 1])
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    ax.view_init(elev=14, azim=170,roll = -92)

    # Plot the original reference frame (static)
    ax.quiver(0, 0, 0, 1, 0, 0, color='gray', linestyle='--', label='X-axis (origin)', alpha=0.5)
    ax.quiver(0, 0, 0, 0, 1, 0, color='gray', linestyle='--', label='Y-axis (origin)', alpha=0.5)
    ax.quiver(0, 0, 0, 0, 0, 1, color='gray', linestyle='--', label='Z-axis (origin)', alpha=0.5)

    # Initialize lines for rotated axes
    x_axis_line, = ax.plot([], [], [], color='r', label='X-axis (rotated)')
    y_axis_line, = ax.plot([], [], [], color='g', label='Y-axis (rotated)')
    z_axis_line, = ax.plot([], [], [], color='b', label='Z-axis (rotated)')

    # Function to update each frame
    def update(frame):
        q = quaternions[frame]
        r = R.from_quat(q)  # Convert quaternion to rotation matrix
        rotation_matrix = r.as_matrix()

        # Extract rotated axes
        x_axis = rotation_matrix[:, 0]
        y_axis = rotation_matrix[:, 1]
        z_axis = rotation_matrix[:, 2]

        # Update lines
        x_axis_line.set_data([0, x_axis[0]], [0, x_axis[1]])
        x_axis_line.set_3d_properties([0, x_axis[2]])
        
        y_axis_line.set_data([0, y_axis[0]], [0, y_axis[1]])
        y_axis_line.set_3d_properties([0, y_axis[2]])
        
        z_axis_line.set_data([0, z_axis[0]], [0, z_axis[1]])
        z_axis_line.set_3d_properties([0, z_axis[2]])

        return x_axis_line, y_axis_line, z_axis_line

    # Create the animation
    anim = FuncAnimation(fig, update, frames=len(quaternions), interval=33.36666667, blit=True, repeat= False)

    # Display the animation
    plt.legend()
    plt.title('Quaternion Animation with Origin Axes')
    plt.show()

    # To save the animation (optional)
    # anim.save('quaternion_animation.mp4', writer='ffmpeg')

# Example: List of quaternions
# Initialize an empty list to hold the quaternions
quaternions = [] # List[List[qx,qy,qz,qw]]

# Define the path to your file
quaternions_file = './output/frame_trajectory.txt'

# Open the file and read it line by line
with open(quaternions_file, 'r') as file:
    for line in file:
        # Split the line by spaces or tabs (depending on file format)
        numbers = line.split()
        
        # Ensure the line has at least 4 numbers
        if len(numbers) >= 4:
            # Get the last 4 numbers and convert them to floats
            quat = [float(numbers[-4]), float(numbers[-3]), float(numbers[-2]), 0-float(numbers[-1])]
            quaternions.append(quat)

# Print the list of quaternions (or further process it as needed)
pprint(quaternions)



visualize_quaternion_animation(quaternions)
