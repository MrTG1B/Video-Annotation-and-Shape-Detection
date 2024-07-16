# Video Annotation and Shape Detection

Author: Tirthankar Dasgupta  
GitHub: [MrTG1B](https://github.com/MrTG1B)

## Description

This Python script captures video from the default camera, allows users to draw or erase on the video frame, saves annotated frames, and detects basic shapes in the drawings. It includes functionalities for drawing with the mouse, toggling between draw and erase modes, saving frames, and clearing the canvas. Shape detection identifies triangles, squares, rectangles, circles, and arrows.

## Features

- **Drawing and Erasing:** Toggle between drawing (red color) and erasing (black color).
- **Shape Detection:** Detects basic shapes like triangles, squares, rectangles, circles, and arrows.
- **Frame Saving:** Save annotated frames with detected shapes.

## Instructions

- Press 'm' to toggle between draw and erase modes.
- Press 's' to save the current annotated frame and detect shapes.
- Press 'c' to clear the canvas.
- Press 'q' to quit the application.

## Requirements

- Python 3.11
- OpenCV (`pip install opencv-python`)
- NumPy (`pip install numpy`)

## Usage

1. Clone the repository:

   ```bash
   git clone https://github.com/MrTG1B/Video-Annotation-and-Shape-Detection.git
   ```

2. Navigate into the project directory:

   ```bash
   cd Video-Annotation-and-Shape-Detection
   ```

3. Run the script:

   ```bash
   python video_annotation_shape_detection.py
   ```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
