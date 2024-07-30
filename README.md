# Virtual Paint

The Virtual Paint Project is an innovative application that allows users to draw on a virtual canvas using hand gestures. This project leverages the power of Python, Tkinter, OpenCV, and MediaPipe to detect hand movements and translate them into drawing actions on the screen.

## Features
- **Real-time Hand Detection:** Utilizes MediaPipe to detect and track the user's hand in real-time.
- **Gesture-based Drawing:** Based on the hand landmarks, the application interprets gestures and draws corresponding paths on the canvas.
- **Interactive GUI:** A user-friendly graphical interface built with Tkinter.
- **Customizable Drawing:** Options to change brush colors, sizes, and other drawing settings.

## Technologies Used
- **Python:** The core programming language used for the project.
- **Tkinter:** For creating the graphical user interface.
- **OpenCV:** For capturing video feed from the webcam and processing the frames.
- **MediaPipe:** For detecting and tracking hand landmarks.


## Installation

### 1. Clone the repository
```sh
git clone
git cd virtual-paint/
```
### 2. Create a virtual environment using `virtualenv`
```sh
sudo pip install virtualenv
virtualenv env
```
### 3. Activate the virtual environment
```sh
source env/bin/activate
```
### 4. Install the dependencies
```sh
pip install -r requirements.txt
```
### 5. Run `Painter.py` file
```sh
python Painter.py
```




![Workflow Diagram](https://github.com/shubh1007/virtual-paint/blob/main/documentation/workflow.png)

## User Interface
![User Interface](https://github.com/shubh1007/virtual-paint/blob/main/documentation/virtual-paint-UI.png)
