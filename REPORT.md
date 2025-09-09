# 19. Background Replacement with Segmentation
**Use semantic segmentation to isolate human subject. Replace background with static image or blur effect (Zoom style).**

## Project Overview

This project implements a real-time background replacement system using semantic segmentation to isolate human subjects in images or video streams. The system allows users to replace the background with either static images or a blur effect similar to what's seen in Zoom video calls.

## Steps Taken

### 1. Project Setup and Cloning
- Cloned the original repository from https://github.com/BakingBrains/Real-Time_Background_remover.git
- Created a dedicated directory structure for the project

### 2. Environment Configuration
- Set up a virtual environment using Python 3.10.15 to ensure compatibility with all dependencies
- Installed required system libraries to support Python compilation with all extensions
- Created multiple initialization scripts for easy environment setup

### 3. Dependency Management
- Installed core dependencies:
  - OpenCV for image processing
  - MediaPipe for semantic segmentation
  - cvzone for simplified computer vision operations
  - Streamlit for web interface development
- Resolved version compatibility issues between libraries

### 4. Code Implementation and Fixes
- Fixed the original BackgroundRemover.py script to work with current library versions
- Corrected method signature mismatches in the SelfiSegmentation module
- Removed deprecated FPS functionality that was incompatible with the current cvzone version
- Resolved OpenCV image stacking issues for better visualization

### 5. Feature Enhancement
- Added blur effect functionality as requested (Zoom-style background blur)
- Implemented multiple background options:
  - Solid color backgrounds
  - Blur effect with adjustable strength
  - Custom image backgrounds
- Enhanced the original script with better user controls and instructions

### 6. Web Interface Development
- Created a Streamlit-based web interface for easier user interaction
- Implemented file upload functionality for processing images
- Added real-time preview of background replacement results
- Included download functionality for processed images

### 7. Deployment Preparation
- Created comprehensive documentation in README.md
- Generated requirements.txt for dependency management
- Developed setup.py for package distribution
- Added .gitignore to exclude unnecessary files
- Created initialization and run scripts for easy deployment

## Problems Faced and Solutions

### 1. Python Version Compatibility
**Problem:** The original code was designed for a specific Python version and library versions that were not compatible with the current system.

**Solution:**
- Installed Python 3.10.15 using pyenv
- Installed required system libraries to ensure all Python extensions compiled correctly
- Created a virtual environment to isolate dependencies

### 2. Library Version Mismatches
**Problem:** The required cvzone version 1.3.4 was not available on PyPI, and method signatures had changed in newer versions.

**Solution:**
- Installed the closest available version (1.3.3) and adapted the code accordingly
- Modified method calls to match the current API (changed `threshold` to `cutThreshold`)
- Removed incompatible FPS functionality

### 3. Missing System Dependencies
**Problem:** Several system libraries were missing, causing Python extensions to not compile correctly.

**Solution:**
- Installed required libraries including libbz2-dev, libffi-dev, liblzma-dev, libncurses-dev, libreadline-dev, libsqlite3-dev, and tk-dev
- Reinstalled Python to ensure all extensions were compiled

### 4. MediaPipe Installation Issues
**Problem:** MediaPipe had compatibility issues with newer Python versions.

**Solution:**
- Used Python 3.10 which has good compatibility with MediaPipe
- Installed MediaPipe directly from PyPI after ensuring Python compatibility

### 5. Streamlit Deprecation Warnings
**Problem:** The Streamlit interface showed deprecation warnings for `use_column_width` parameter.

**Solution:**
- Updated the code to use the new `use_container_width` parameter
- Ensured compatibility with the latest Streamlit version

### 6. OpenCV Image Stacking Issues
**Problem:** The cvzone.stackImages function failed with certain image types, causing runtime errors.

**Solution:**
- Added error checking for image loading
- Implemented fallback visualization method when stackImages fails
- Fixed Gaussian blur implementation for the blur background option

## Features Implemented

### Core Functionality
1. **Semantic Segmentation:** Uses MediaPipe's Selfie Segmentation to isolate human subjects
2. **Background Replacement:** Replaces removed background with:
   - Solid colors
   - Blur effect (Zoom-style)
   - Custom images
3. **Real-time Processing:** Works with live webcam feed

### User Interfaces
1. **Command-line Interface:**
   - Keyboard controls for background switching
   - Real-time preview
   - Simple execution

2. **Web Interface (Streamlit):**
   - File upload for image processing
   - Interactive background selection
   - Adjustable blur strength
   - Download functionality for results

### Deployment Features
1. **Easy Setup:**
   - Automated initialization script
   - Requirements file for dependency management
   - Clear documentation

2. **Multiple Execution Options:**
   - Direct script execution
   - Shell scripts for CLI and web interfaces
   - Package installation support

## Technical Details

### Segmentation Approach
The project uses MediaPipe's Selfie Segmentation model which:
- Employs a deep neural network for real-time segmentation
- Provides accurate human boundary detection
- Works efficiently on CPU without requiring specialized hardware

### Background Replacement Techniques
1. **Solid Color:** Replaces background with a uniform color
2. **Blur Effect:** Applies Gaussian blur to the original background
3. **Image Replacement:** Uses a user-provided image as the new background

### Performance Considerations
- Optimized for real-time processing
- Works with standard webcams
- Minimal system requirements

## Usage Instructions

### Quick Start
1. Run `./init.sh` to set up the environment
2. For CLI version: `./run_cli.sh`
3. For web version: `./run_streamlit.sh`

### Controls
- CLI version: 'a' (previous background), 'd' (next background), 'q' (quit)
- Web version: Interactive controls through the browser interface

## Conclusion

The project successfully implements background replacement with semantic segmentation as requested. It provides both the core functionality of isolating human subjects and replacing backgrounds with static images or blur effects. The solution is deployable, well-documented, and offers multiple interfaces for different user preferences.

The implementation addresses all the challenges faced during development and provides a robust, user-friendly solution for background replacement in images and video streams.