# ✋ Gesture-Controlled Presentation Tool

A real-time computer vision application that enables **touchless presentation control using predefined hand gestures**. The system uses a webcam to detect and track hand landmarks, interprets gestures through rule-based logic, and converts them into keyboard commands using PyAutoGUI.

The goal is to provide a more **hands-free, interactive, and natural presentation experience** without requiring a physical remote, keyboard, or mouse for basic presentation control.

---

## 📌 Problem Statement

During presentations, presenters often need to repeatedly interact with a keyboard, mouse, or presentation remote to navigate slides. This can interrupt the flow of the presentation and shift the presenter's attention away from the audience.

This project addresses that problem by providing a **touchless presentation-control interface** where predefined hand gestures can be used to control presentation actions through a webcam.

---

## 🎯 Objectives

* Enable touchless slide navigation using hand gestures
* Detect and track hand landmarks in real time
* Recognize predefined static and dynamic gestures
* Prevent accidental commands using an explicit activation gesture
* Prevent repeated actions using a cooldown mechanism
* Provide an on-screen gesture guide for user assistance
* Work with commonly used presentation software through keyboard events
* Provide a lightweight solution requiring only a standard webcam

---

## 💡 Key Features

### ✋ Gesture-Based Presentation Control

The system recognizes predefined hand gestures and maps them to presentation actions.

| Gesture        | Description                  | Action                            |
| -------------- | ---------------------------- | --------------------------------- |
| ✋ Open Palm    | Five fingers clearly visible | Activates gesture control         |
| 👉 Swipe Right | Rightward hand movement      | Next slide                        |
| 👈 Swipe Left  | Leftward hand movement       | Previous slide                    |
| ✊ Fist         | Fingers closed               | Deactivates/exits gesture control |
| ✌️ Peace Sign  | Two fingers raised           | Displays gesture guide            |

> **Important:** Presentation gestures are processed only after gesture control has been activated using the open-palm gesture. This helps reduce accidental slide changes.

---

## 🖥️ Gesture Guide Popup

The system includes a floating gesture guide to help the user understand the available controls.

* The **peace sign** activates the gesture guide.
* The guide displays the supported gestures and their corresponding actions.
* The popup is designed to appear beside the presentation rather than obstructing the main presentation window.
* The guide disappears when the gesture is no longer detected.

This provides assistance without requiring the user to interrupt the presentation.

---

## 🧠 How the System Works

The overall processing pipeline is:

Webcam
   ↓
OpenCV
(Video Capture & Frame Processing)
   ↓
MediaPipe Hands
(Hand Detection & 21 Landmark Estimation)
   ↓
Gesture Recognition Logic
(Rule-Based Analysis)
   ↓
PyAutoGUI
(Keyboard Events)
   ↓
Presentation Software


### Step-by-step flow

1. **Webcam Capture**

   * OpenCV accesses the webcam using `cv2.VideoCapture()`.
   * Frames are continuously captured from the camera.

2. **Frame Processing**

   * OpenCV handles the captured image frames.
   * Frames are converted from **BGR to RGB** before being passed to MediaPipe.

3. **Hand Detection and Landmark Estimation**

   * MediaPipe Hands detects the hand and estimates **21 hand landmarks**.
   * The landmarks provide the position of important points such as fingertips and finger joints.

4. **Gesture Recognition**

   * The application uses the landmark coordinates to determine finger states and hand movement.
   * Static gestures are identified using finger-position relationships.
   * Dynamic gestures such as swipes are identified using landmark movement across consecutive frames.

5. **Action Control**

   * Once a gesture is recognized, the corresponding presentation command is triggered through PyAutoGUI.

6. **Cooldown Protection**

   * A cooldown timer prevents the same gesture from repeatedly triggering an action across multiple video frames.

---

## 🤖 Computer Vision & ML Component

The project uses **MediaPipe Hands**, which contains pretrained machine-learning models for hand perception.

The MediaPipe pipeline performs two important tasks:

### 1. Palm/Hand Detection

A pretrained detection model first identifies the hand region in the image.

### 2. Hand Landmark Estimation

A landmark model then estimates **21 hand landmarks** from the detected hand region.

These landmarks are used by our application to perform gesture recognition.

### Important distinction

The project **does not train its own gesture classification model**.

Instead:

```text
Pretrained MediaPipe Models
          ↓
21 Hand Landmarks
          ↓
Our Rule-Based Gesture Logic
          ↓
Presentation Command
```

The gesture recognition layer uses predefined rules based on:

* Finger positions
* Fingertip and joint relationships
* Horizontal landmark movement
* Changes between consecutive frames
* Distance/position thresholds where required

This makes the system lightweight and easy to interpret.

---

## ✋ Gesture Recognition Logic

### Static Gestures

Static gestures are primarily identified from the current hand configuration.

Examples:

* **Open Palm** → activation
* **Fist** → deactivation/exit
* **Peace Sign** → gesture guide

Finger states are determined by comparing fingertip positions with relevant finger joints.

---

### 👉 Dynamic Gestures

Dynamic gestures depend on movement across multiple frames.

For swipe detection, the application tracks the movement of the **index fingertip landmark**.

Conceptually:

Previous X Position
        ↓
Current X Position
        ↓
Calculate Horizontal Displacement
        ↓
Compare Against Threshold
        ↓
Left Swipe / Right Swipe


A sufficiently large positive or negative displacement is interpreted as a swipe.

---

## ⏱️ Cooldown Mechanism

A gesture can remain visible for multiple webcam frames. Without protection, one gesture could therefore trigger the same keyboard command repeatedly.

To prevent this, the application uses a cooldown period between actions.

Conceptually:


Current Time - Last Action Time > Cooldown


Only when the cooldown period has elapsed is another presentation command allowed.

This improves stability and prevents unintended repeated slide changes.



## ⚙️ MediaPipe Configuration

The project processes a single hand at a time:

hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)


### Configuration

| Parameter                  |   Value | Purpose                                           |
| -------------------------- | ------: | ------------------------------------------------- |
| static_image_mode          |   False | Enables video/live-stream processing and tracking |
|  max_num_hands             |     1   | Processes one hand at a time                      |
|  min_detection_confidence  |     0.7 | Filters low-confidence hand detections            |
|  min_tracking_confidence   |    0.7  | Helps maintain stable hand tracking               |

> The confidence values are detection/tracking thresholds and should not be interpreted as model accuracy percentages.


## 🛠️ Technology Stack

| Technology          | Role                                                             |
| ------------------- | ---------------------------------------------------------------- |
| **Python 3.11**     | Core programming language                                        |
| **OpenCV**          | Webcam access, frame capture, color conversion and visualization |
| **MediaPipe Hands** | Hand detection, tracking and 21-landmark estimation              |
| **NumPy**           | Numerical and image-array operations                             |
| **Math**            | Distance and geometric calculations                              |
| **PyAutoGUI**       | Sends keyboard commands to presentation software                 |
| **Standard Webcam** | Captures real-time hand movements                                |

---

## 🏗️ System Architecture

┌──────────────────────┐
│       Webcam         │
└──────────┬───────────┘
           ↓
┌──────────────────────┐
│       OpenCV         │
│ Frame Capture        │
│ BGR → RGB            │
└──────────┬───────────┘
           ↓
┌──────────────────────┐
│    MediaPipe Hands   │
│ Hand Detection       │
│ 21 Landmark Tracking │
└──────────┬───────────┘
           ↓
┌──────────────────────┐
│ Gesture Recognition  │
│      Logic           │
│ Rule-Based Analysis  │
└──────────┬───────────┘
           ↓
┌──────────────────────┐
│      PyAutoGUI       │
│ Keyboard Events      │
└──────────┬───────────┘
           ↓
┌──────────────────────┐
│ Presentation Software│
│ PowerPoint / Slides  │
└──────────────────────┘


## 📁 Project Structure

gesture-control/
│
├── slide_control.py
├── webcam_test.py
├── hand_detect.py
├── finger_count.py
├── requirements.txt
└── README.md


### File Description

| File               | Purpose                                                |
| ------------------ | ------------------------------------------------------ |
| `slide_control.py` | Final integrated presentation-control implementation   |
| `webcam_test.py`   | Tests webcam capture and video input                   |
| `hand_detect.py`   | Tests MediaPipe hand detection and landmark extraction |
| `finger_count.py`  | Contains finger-state/counting logic                   |
| `requirements.txt` | Lists required Python dependencies                     |
| `README.md`        | Project documentation                                  |

---

## 🚀 How to Run

### 1. Clone the Repository


git clone <your-repository-url>
cd gesture-control


### 2. Create a Virtual Environment

python3.11 -m venv gesture_env

### 3. Activate the Environment

#### Linux / macOS


source gesture_env/bin/activate


#### Windows


gesture_env\Scripts\activate


### 4. Install Dependencies


pip install -r requirements.txt


### 5. Start Your Presentation

* Open PowerPoint or Google Slides.
* Start the slideshow.
* Keep the presentation window in the foreground.

### 6. Run the Application


python slide_control.py


### 7. Activate Gesture Control

Show an **open palm** to activate the gesture controls.

You can then use the supported gestures to navigate the presentation.

=
## 💻 System Requirements

* Python 3.11
* Standard webcam
* Good lighting conditions
* PowerPoint, Google Slides, or another presentation application that responds to keyboard events
* Windows / macOS / Linux

---

## 📊 Current Gesture Pipeline


Camera Frame
     ↓
RGB Conversion
     ↓
Hand Detection
     ↓
21 Hand Landmarks
     ↓
Finger State Analysis
     ↓
Movement / Gesture Analysis
     ↓
Activation Check
     ↓
Cooldown Check
     ↓
Presentation Command


---

## 🔒 Stability & Safety Measures

The system includes several mechanisms to reduce unintended actions:

* **Explicit activation:** gesture control must first be activated using an open palm.
* **Single-hand processing:** only one hand is processed at a time.
* **Detection/tracking thresholds:** low-confidence detections can be filtered.
* **Cooldown timer:** prevents repeated commands from a single gesture.
* **Predefined gesture rules:** only recognized gesture patterns trigger actions.

---

## ⚠️ Limitations

The current system can be affected by:

* Poor lighting
* Hand occlusion
* Very fast hand movements
* Camera placement
* Distance between the user and camera
* Similar-looking gestures
* Fixed gesture thresholds
* Background or visual conditions that make hand detection difficult

The system is therefore intended as a **computer-vision prototype for controlled presentation environments**, rather than a universal gesture-control system.

---

## 🔮 Future Enhancements

Potential improvements include:

* Voice + gesture hybrid control
* Annotation and highlighting gestures
* Zoom and pointer gestures
* Multi-hand gesture support
* Adaptive gesture thresholds
* Temporal smoothing for more stable gesture recognition
* User-specific gesture calibration
* Mobile application integration
* AI-based adaptive gesture recognition
* Training a dedicated gesture-classification model for a larger gesture vocabulary

---

## 💼 Business / Real-World Impact

The project addresses a simple human-computer interaction problem: **reducing dependency on physical input devices during presentations**.

By using a standard webcam instead of specialized hardware, the system provides a low-cost way to introduce touchless interaction into:

* Smart classrooms
* Academic presentations
* Corporate presentations
* Demonstrations
* Interactive training environments
* Situations where hands-free interaction is useful

The main impact is improved **presentation flow and user interaction**, allowing presenters to spend less time physically interacting with a keyboard or mouse and more time engaging with their audience.

---

## 🌟 Advantages

* ✋ Touchless and intuitive interaction
* 💻 Works with existing presentation software
* 📷 Requires only a standard webcam
* 🧠 Uses real-time computer vision
* ⚡ Lightweight and responsive
* 🔒 Explicit activation reduces accidental actions
* ⏱️ Cooldown mechanism prevents repeated triggers
* 🎓 Useful for academic demonstrations and HCI applications

---

## 📌 Conclusion

The Gesture-Controlled Presentation Tool demonstrates how **computer vision, hand landmark estimation, rule-based gesture recognition, and system automation** can be combined to create a practical human-computer interaction application.

Rather than requiring specialized hardware, the system uses a standard webcam to detect hand gestures and translate them into presentation commands. The combination of explicit activation, landmark-based gesture recognition, and cooldown protection makes the interaction more controlled and suitable for real-time presentation environments.
