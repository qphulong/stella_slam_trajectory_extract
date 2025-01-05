import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import cv2
from scipy.spatial.transform import Rotation as R

# === Step 1: Parse SLAM Data ===
def parse_slam_data(file_path):
    data = np.loadtxt(file_path)
    timestamps = data[:, 0]
    
    # Swap x and z coordinates
    positions = data[:, 1:4]
    positions[:, [0, 2]] = positions[:, [2, 0]]  # Swap x (index 0) and z (index 2), z,y,x
    
    quaternions = data[:, 4:]  # qx, qy, qz, qw
    return timestamps, positions, quaternions

# === Step 2: 3D Visualization ===
def plot_3d_trajectory(positions):
    """
    x, y, z
    x, z, y
    """
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Plot the 3D path using dots
    ax.scatter(positions[:, 0], positions[:, 2], positions[:, 1], c=np.linspace(0, 1, len(positions)), cmap='viridis')

    # Draw the axes: X (forward), Y (upward), Z (right)
    max_range = np.ptp(positions, axis=0).max()  # Get the maximum range for scaling
    center = positions.mean(axis=0)

    # Draw X axis (forward)
    ax.quiver(center[0], center[1], center[2], max_range / 5, 0, 0, color='red', label='X (Forward)')
    # Draw Y axis (upward)
    ax.quiver(center[0], center[1], center[2], 0, 0, max_range / 5, color='green', label='Y (Upward)')
    # Draw Z axis (right)
    ax.quiver(center[0], center[1], center[2], 0, max_range / 5, 0, color='blue', label='Z (Right)')

    # Set labels
    ax.set_title("Camera Trajectory in 3D Space")
    ax.set_xlabel("X (Forward)")
    ax.set_ylabel("Z (Right)")
    ax.set_zlabel("Y (Upward)")

    # Set the aspect ratio of the axes to be 1:1:1
    mid_x = (positions[:, 0].min() + positions[:, 0].max()) / 2
    mid_y = (positions[:, 1].min() + positions[:, 1].max()) / 2
    mid_z = (positions[:, 2].min() + positions[:, 2].max()) / 2
    
    ax.set_xlim(mid_x - max_range, mid_x + max_range)# x points toward
    ax.set_ylim(mid_y + max_range, mid_y - max_range)# z points to the right
    ax.set_zlim(mid_z - max_range, mid_z + max_range)# y points upward

    ax.view_init(elev=25, azim=-170,roll = 0) # rotate for easy visualization

    ax.legend()
    plt.show()


# === Step 3: Overlay Path on Video ===
def overlay_trajectory_on_vr360_video(video_path, output_path, timestamps, positions, quaternions):
    cap = cv2.VideoCapture(video_path)
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    frame_idx = 0

    # Initial rotation to align with the right-hand rule (X-forward, Z-right, Y-up)
    initial_rotation = R.from_euler('xyz', [0, 0, 0], degrees=False)  # Identity rotation

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Compute the current timestamp based on the frame index
        current_time = timestamps[0] + frame_idx / fps

        # Find the closest timestamp index in the SLAM data
        idx = np.argmin(np.abs(timestamps - current_time))

        # Get the current quaternion and compute total rotation
        quaternion = quaternions[idx]
        current_rotation = R.from_quat(quaternion)  # Rotation from SLAM data

        # Combine the initial rotation with the current camera rotation
        total_rotation = current_rotation * initial_rotation

        # Transform all trajectory points relative to the current camera orientation
        transformed_positions = total_rotation.apply(positions - positions[idx])

        # Overlay the transformed positions
        overlay_frame = frame.copy()

        for pos in transformed_positions:
            # Convert 3D position to spherical coordinates
            x, y, z = pos
            longitude = np.arctan2(y, x)  # Angle in the XY-plane
            latitude = np.arctan2(z, np.sqrt(x**2 + y**2))  # Angle from the XY-plane

            # Map spherical coordinates to equirectangular projection
            px = int((longitude + np.pi) / (2 * np.pi) * width)  # Normalize longitude to [0, 2π]
            py = int((np.pi / 2 - latitude) / np.pi * height)    # Normalize latitude to [0, π]

            if 0 <= px < width and 0 <= py < height:  # Ensure the points are within bounds
                cv2.circle(overlay_frame, (px, py), 3, (0, 255, 0), -1)

        out.write(overlay_frame)
        frame_idx += 1

    cap.release()
    out.release()

# === Main Function ===
def main():
    trajectory_file = "./output/frame_trajectory.txt"  # Path to trajectory file
    video_file = "./input/tokyo_0800_1010.mp4"  # Path to input video
    output_video_file = "output_video_with_trajectory.mp4"  # Path for saving output video

    # Parse SLAM data
    timestamps, positions, quaternions = parse_slam_data(trajectory_file)

    # 3D visualization
    plot_3d_trajectory(positions)

    # Overlay trajectory on video
    # overlay_trajectory_on_vr360_video(video_file, output_video_file, timestamps, positions, quaternions)

if __name__ == "__main__":
    main()
