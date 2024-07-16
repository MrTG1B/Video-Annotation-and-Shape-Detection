"""
Author: Tirthankar Dasgupta
GitHub: https://github.com/MrTG1B
Date: 16-07-2024
Description: This script captures video from the default camera, allows users to draw or erase on the video frame,
             save annotated frames, and detect shapes in the drawings. It includes functionalities for drawing with
             the mouse, toggling between draw and erase modes, saving frames, and clearing the canvas. Shape detection
             identifies basic shapes such as triangles, squares, rectangles, circles, and arrows.

Instructions:
- Press 'm' to toggle between draw and erase modes.
- Press 's' to save the current annotated frame and detect shapes.
- Press 'c' to clear the canvas.
- Press 'q' to quit the application.
"""

import cv2
import os
import numpy as np

drawing = False  # True if the mouse is pressed
mode = True  # If True, draw. Press 'm' to toggle to erase
ix, iy = -1, -1

def draw(event, x, y, flags, param):
    """
    This function handles the mouse events when drawing on the canvas.
    It is called whenever the user interacts with the canvas.

    Parameters:
    event (int): The type of mouse event that occurred.
    x (int): The x-coordinate of the mouse.
    y (int): The y-coordinate of the mouse.
    flags (int): Additional flags related to the mouse event.
    param (object): Additional parameters related to the mouse event.
    """

    global ix, iy, drawing, mode, canvas

    # Check if the left mouse button is pressed
    if event == cv2.EVENT_LBUTTONDOWN:
        # Start drawing
        drawing = True
        # Save the current mouse coordinates
        ix, iy = x, y

    # Check if the mouse is moving
    elif event == cv2.EVENT_MOUSEMOVE:
        # Check if the user is drawing
        if drawing:
            # Check if the user is in draw mode
            if mode:
                # Draw a line on the canvas with red color
                cv2.line(canvas, (ix, iy), (x, y), (0, 0, 255), 5)
                # Update the current mouse coordinates
                ix, iy = x, y
            else:
                # Erase a line on the canvas with black color
                cv2.line(canvas, (ix, iy), (x, y), (0, 0, 0), 20)
                # Update the current mouse coordinates
                ix, iy = x, y

    # Check if the left mouse button is released
    elif event == cv2.EVENT_LBUTTONUP:
        # Stop drawing
        drawing = False
        # Check if the user is in draw mode
        if mode:
            # Draw a line on the canvas with red color
            cv2.line(canvas, (ix, iy), (x, y), (0, 0, 255), 5)
        else:
            # Erase a line on the canvas with black color
            cv2.line(canvas, (ix, iy), (x, y), (0, 0, 0), 20)

def capture():
    # Make frame and canvas global to use in the draw function
    global frame, canvas

    # Define the directory where you want to save the frames
    save_dir = "frames"
    os.makedirs(save_dir, exist_ok=True)

    # Open the video capture (0 for the default camera)
    cap = cv2.VideoCapture(0)

    # Check if the camera opened successfully
    if not cap.isOpened():
        print("Error: Could not open video capture.")
        exit()

    # Create a window named 'Frame' and set the mouse callback function to draw
    cv2.namedWindow('Frame')
    cv2.setMouseCallback('Frame', draw)

    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()

        # Check if frame is captured successfully
        if not ret:
            print("Error: Could not read frame.")
            break

        # If canvas is not initialized, initialize it to the size of the frame
        if 'canvas' not in globals():
            canvas = np.zeros_like(frame)

        # Combine the frame and the canvas with a certain weight
        combined_frame = cv2.addWeighted(frame, 0.7, canvas, 0.3, 0)

        # Display the resulting frame
        cv2.imshow('Frame', combined_frame)

        # Check for key presses
        k = cv2.waitKey(1) & 0xFF

        if k == ord('q'):
            break
        elif k == ord('m'):
            # Toggle the drawing mode
            global mode
            mode = not mode
        elif k == ord('s'):
            # Save the annotated frame
            frame_filename = os.path.join(save_dir, "annotated_frame.jpg")
            cv2.imwrite(frame_filename, combined_frame)
            print(f"Saved: {frame_filename}")

            # Detect the shape on the canvas
            shape = detect_shape(canvas)
            print(f"Detected shape: {shape}")
        elif k == ord('c'):
            # Clear the canvas
            canvas = np.zeros_like(frame)

    # Release the capture and close any open windows when everything is done
    cap.release()
    cv2.destroyAllWindows()

def detect_shape(canvas):
    # Convert the canvas to grayscale
    # The grayscale image is used for edge detection
    gray = cv2.cvtColor(canvas, cv2.COLOR_BGR2GRAY)
    
    # Apply Gaussian blur to the grayscale image
    # This helps to reduce noise and smooth the image
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    
    # Perform edge detection on the blurred image
    # The edges are the boundaries between different intensities
    # Canny edge detection is used here
    edged = cv2.Canny(blurred, 50, 150)
    
    # Find contours in the edged image
    # Contours are boundaries of connected pixels of the same intensity
    contours, _ = cv2.findContours(edged, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    # If no contours are found, return "No shape detected"
    if len(contours) == 0:
        return "No shape detected"
    
    # Among all the found contours, select the one with the largest area
    # This is assumed to be the shape on the canvas
    c = max(contours, key=cv2.contourArea)
    
    # Approximate the contour using a polygon
    # This reduces the number of points in the contour
    # The epsilon value determines the approximation accuracy
    epsilon = 0.04 * cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, epsilon, True)
    
    # Identify the shape based on the number of vertices in the approximated contour
    # If the shape has 3 vertices, it is a triangle
    # If the shape has 4 vertices, it is either a square or a rectangle
    # If the shape has more than 4 vertices, it may be a circle or an arrow
    if len(approx) == 3:
        return "Triangle"
    elif len(approx) == 4:
        # Calculate the aspect ratio of the bounding rectangle of the shape
        # If the aspect ratio is within a certain range, it is a square
        # Otherwise, it is a rectangle
        (x, y, w, h) = cv2.boundingRect(approx)
        aspect_ratio = w / float(h)
        if 0.95 <= aspect_ratio <= 1.05:
            return "Square"
        else:
            return "Rectangle"
    elif len(approx) > 4:
        # Check if the shape is an arrow
        # If it is, return "Arrow"
        # Otherwise, return "Circle"
        if is_arrow(c):
            return "Arrow"
        return "Circle"
    # If the shape is neither a triangle nor a quadrilateral, return "Unknown shape"
    return "Unknown shape"

def is_arrow(contour):
    # Find the convex hull of the contour
    hull = cv2.convexHull(contour, returnPoints=False)
    
    # If the number of points in the hull is less than 3, it is not an arrow
    if len(hull) < 3:
        return False
    
    # Find the convexity defects of the contour
    defects = cv2.convexityDefects(contour, hull)
    
    # If no defects are found, it is not an arrow
    if defects is None:
        return False
    
    # Initialize a count for angles less than or equal to 90 degrees
    count = 0
    
    # Iterate over the defects to calculate the angle between the points
    for i in range(defects.shape[0]):
        s, e, f, d = defects[i, 0]
        start = tuple(contour[s][0])
        end = tuple(contour[e][0])
        far = tuple(contour[f][0])
        a = np.linalg.norm(np.array(start) - np.array(end))
        b = np.linalg.norm(np.array(start) - np.array(far))
        c = np.linalg.norm(np.array(end) - np.array(far))
        angle = np.arccos((b**2 + c**2 - a**2) / (2 * b * c)) * 180.0 / np.pi
        
        # If the angle is less than or equal to 90 degrees, increment count
        if angle <= 90:
            count += 1
        
        # If there are more than 1 angle less than or equal to 90 degrees, it is an arrow
        if count > 1:
            return True
    
    # If no arrow-like shape is found, return False
    return False

if __name__ == "__main__":
    capture()
