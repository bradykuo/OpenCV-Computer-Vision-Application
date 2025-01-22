# OpenCV Computer Vision Application

This project implements various computer vision algorithms including contour detection, camera calibration, augmented reality, and stereo disparity mapping using Python and OpenCV.

## Features

1. **Image Processing**
   - 1.1 Draw Contour 
   - 1.2 Count Rings 

2. **Camera Calibration**
   - 2.1 Corner detection 
   - 2.2 Find intrinsic matrix 
   - 2.3 Find extrinsic matrix 
   - 2.4 Find distortion matrix 
   - 2.5 Show undistorted result 

3. **Augmented Reality**
   - 3.1 Show words on board 
   - 3.2 Show words vertically 

4. **Stereo Disparity Map**
   - 4.1 Generate Stereo Disparity Map 
   - 4.2 Check Disparity Value 

## Requirements

- Python 3.7
- opencv-contrib-python (3.4.2.17)
- Matplotlib 3.1.1
- PyQt5 (5.15.1)

## Installation

```bash
# Clone the repository
git clone [your-repository-url]

# Install required packages
pip install opencv-contrib-python==3.4.2.17
pip install matplotlib==3.1.1
pip install PyQt5==5.15.1
```

## Project Structure

```
project/
├── main.py            # Main entry point
├── UI.py             # PyQt5 UI definition
├── controller.py     # Main logic controller
└── Q2_lib/          # Library files
    ├── alphabet_lib_onboard.txt
    └── alphabet_lib_vertical.txt
```

## Usage

1. Run the program:
```bash
python main.py
```

2. Use the interface to:
   - Load images using "Load Image1" and "Load Image2" buttons
   - Load folder for calibration images using "Load Folder" button
   - Process images using the corresponding function buttons

## Function Details

### 1. Find Contour
- Processes two color images to detect and draw contours
- Counts the number of rings in the images

### 2. Camera Calibration
- Processes chessboard calibration images
- Detects corners and calculates camera parameters
- Shows undistorted results

### 3. Augmented Reality
- Input text (up to 6 characters) to display on chessboard
- Shows text both horizontally and vertically
- Uses calibration data for accurate projection

### 4. Stereo Disparity
- Generates disparity map from stereo image pairs
- Allows interactive checking of disparity values
- Visualizes corresponding points between image pairs

## Notes

- Camera calibration uses 15 chessboard images (1.bmp ~ 15.bmp)
- Augmented reality requires calibrated camera parameters
- The stereo disparity implementation uses StereoBM with parameters:
  - numDisparities = 256
  - blockSize = 25

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is available for academic and educational purposes.

## Reference

https://reurl.cc/GpWKNZ
