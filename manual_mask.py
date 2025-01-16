import cv2
import os
import numpy as np


# Initialize global variables
drawing = False   # True if the user is drawing
ix, iy = -1, -1   # Initial mouse position
brush_radius = 10  # Default brush size
ignore_color = (0, 0, 0)  # Default ignore region color (black)


def draw_mask(event, x, y, flags, param):
    """Callback function for mouse events to draw the mask."""
    global ix, iy, drawing, brush_radius, ignore_color

    if event == cv2.EVENT_LBUTTONDOWN:  # Start drawing
        drawing = True
        ix, iy = x, y

    elif event == cv2.EVENT_MOUSEMOVE:  # Draw as the mouse moves
        if drawing:
            # Draw on the mask and overlay image
            cv2.circle(mask, (x, y), brush_radius, 0, -1)  # Black on the mask
            cv2.circle(temp_img, (x, y), brush_radius, ignore_color, -1)

    elif event == cv2.EVENT_LBUTTONUP:  # Stop drawing
        drawing = False


def extract_middle_frame(video_path):
    """Extract the middle frame of a video."""
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Error: Unable to open video file {video_path}")
        return None

    # Get total number of frames
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    middle_frame_idx = total_frames // 2

    # Set the video to the middle frame
    cap.set(cv2.CAP_PROP_POS_FRAMES, middle_frame_idx)

    # Read the frame
    ret, frame = cap.read()
    cap.release()

    if not ret:
        print(f"Error: Unable to read the middle frame of {video_path}")
        return None

    return frame


# Locate the video file
video_dir = "./input"
video_files = [f for f in os.listdir(video_dir) if f.endswith(".mp4")]

if len(video_files) == 0:
    print(f"Error: No MP4 files found in {video_dir}")
    exit()

# Assuming there's only one video file in the directory
video_path = os.path.join(video_dir, video_files[0])

# Extract the middle frame from the video
image = extract_middle_frame(video_path)
if image is None:
    exit()

# Create a copy for overlaying the mask
temp_img = image.copy()

# Initialize the mask (white by default, indicating all regions are processed)
mask = np.ones((image.shape[0], image.shape[1]), dtype=np.uint8) * 255

# Create a window and set the mouse callback
cv2.namedWindow('Draw Mask')
cv2.setMouseCallback('Draw Mask', draw_mask)

print("Instructions:")
print(" - Left mouse button: Draw (ignored regions will be black)")
print(" - Press 'c': Change the brush color")
print(" - Press '+': Increase brush size")
print(" - Press '-': Decrease brush size")
print(" - Press 's': Save the mask and exit")
print(" - Press 'q': Exit without saving")

while True:
    # Show the image with the current mask overlay
    cv2.imshow('Draw Mask', temp_img)

    # Wait for a key press
    key = cv2.waitKey(1) & 0xFF

    if key == ord('+'):  # Increase brush size
        brush_radius = min(brush_radius + 5, 100)
        print(f"Brush size: {brush_radius}")

    elif key == ord('-'):  # Decrease brush size
        brush_radius = max(brush_radius - 5, 1)
        print(f"Brush size: {brush_radius}")

    elif key == ord('c'):  # Change brush color
        print("Enter brush color (R G B, e.g., 255 0 0 for red):")
        try:
            r, g, b = map(int, input().split())
            ignore_color = (b, g, r)  # OpenCV uses BGR format
            print(f"Brush color set to: {ignore_color}")
        except ValueError:
            print("Invalid input. Please enter three integers separated by spaces.")

    elif key == ord('s'):  # Save the mask
        output_path = './input/mask.png'
        cv2.imwrite(output_path, mask)
        print(f"Mask saved to {output_path}")
        break

    elif key == ord('q'):  # Quit without saving
        print("Exiting without saving.")
        break

# Clean up
cv2.destroyAllWindows()
