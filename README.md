# Hands-Free
A touchless gesture controlled mouse system

---

## Overview
This project is a real-time gesture recognition system that replaces a traditional mouse with hand movements. It uses Python along with OpenCV, MediaPipe, and PyAutoGUI to track hand landmarks and convert gestures into system actions such as cursor movement, clicking, scrolling, and dragging.
The goal of this project is to create a touch-free way of interacting with a computer using only a webcam, making it useful for accessibility, presentations, and modern human-computer interaction systems.

---

## Features
- Real-time hand tracking using MediaPipe
- Cursor movement controlled by index finger
- Scroll functionality using index and middle fingers
- Left click using thumb + index finger pinch
- Drag and drop by holding pinch gesture
- Double click using rapid pinch
- Right click using thumb + middle finger gesture
- Close application using fist gesture
- On-screen status display for current action

---

## Tools Used
- Python 3.x
- OpenCV (for video capture and image processing)
- MediaPipe (for hand tracking and landmark detection)
- PyAutoGUI (for controlling mouse and system actions)
- Math & Time modules (for gesture calculations and timing logic)

---

## Steps to Install and Run the Project
- Ensure Python 3 is installed on your system
- Install the required libraries: opencv-python, mediapipe, pyautogui
- Download or clone the repository:
- Run the Python file. 

Your webcam will open, and the gesture control system will start running

---

## How to Use
- Move your index finger to control the cursor
- Use index + middle finger to scroll (up/down based on position)
- Pinch thumb + index finger to perform a left click
- Hold the pinch to drag objects
- Quickly pinch twice for double click
- Pinch thumb + middle finger for right click
- Make a fist and hold for 3 seconds to close the active application
- Press ‘Q’ key to exit the program

Try different lighting conditions and hand positions to evaluate detection accuracy. Also test rapid and slow gestures to ensure correct interpretation.

