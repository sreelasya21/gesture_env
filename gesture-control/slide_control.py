import cv2
import mediapipe as mp
import pyautogui
import time
import numpy as np
import math

# -------------------- MediaPipe Setup --------------------
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)
mp_draw = mp.solutions.drawing_utils

# -------------------- Webcam --------------------
cap = cv2.VideoCapture(0)

# -------------------- Constants --------------------
TIP_IDS = [4, 8, 12, 16, 20]
SWIPE_THRESHOLD = 0.15
ZOOM_THRESHOLD = 0.03
COOLDOWN = 1.0

prev_x = None
prev_zoom_dist = None
last_action_time = 0
control_active = False
show_help = False

# -------------------- Finger Count --------------------
def count_fingers(hand_landmarks):
    fingers = []

    # Thumb
    fingers.append(
        hand_landmarks.landmark[4].x <
        hand_landmarks.landmark[3].x
    )

    # Other fingers
    for i in [8, 12, 16, 20]:
        fingers.append(
            hand_landmarks.landmark[i].y <
            hand_landmarks.landmark[i - 2].y
        )

    return fingers.count(True)

# -------------------- Distance --------------------
def distance(p1, p2):
    return math.hypot(p1.x - p2.x, p1.y - p2.y)

# -------------------- Main Loop --------------------
while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    show_help = False

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            fingers = count_fingers(hand_landmarks)
            index_x = hand_landmarks.landmark[8].x
            current_time = time.time()

            # -------- Activate Control --------
            if fingers == 5:
                control_active = True
                cv2.putText(frame, "CONTROL ACTIVE", (20, 40),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            # -------- Help Gesture --------
            if fingers == 2:
                show_help = True

            # -------- Actions --------
            if control_active:

                # ---- Swipe ----
                if prev_x is not None and fingers >= 4:
                    if index_x - prev_x > SWIPE_THRESHOLD and current_time - last_action_time > COOLDOWN:
                        pyautogui.press('right')
                        last_action_time = current_time

                    elif prev_x - index_x > SWIPE_THRESHOLD and current_time - last_action_time > COOLDOWN:
                        pyautogui.press('left')
                        last_action_time = current_time

                prev_x = index_x

                # ---- Zoom (Thumb + Index) ----
                if fingers == 2:
                    thumb = hand_landmarks.landmark[4]
                    index = hand_landmarks.landmark[8]
                    zoom_dist = distance(thumb, index)

                    if prev_zoom_dist is not None:
                        diff = zoom_dist - prev_zoom_dist

                        if abs(diff) > ZOOM_THRESHOLD and current_time - last_action_time > 0.3:
                            if diff > 0:
                                pyautogui.hotkey('ctrl', '+')  # Zoom In
                            else:
                                pyautogui.hotkey('ctrl', '-')  # Zoom Out

                            last_action_time = current_time

                    prev_zoom_dist = zoom_dist
                else:
                    prev_zoom_dist = None

                # ---- Exit ----
                if fingers == 0 and current_time - last_action_time > COOLDOWN:
                    pyautogui.press('esc')
                    control_active = False
                    last_action_time = current_time

            cv2.putText(frame, f"Fingers: {fingers}", (20, 80),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)

    # -------------------- Help Popup --------------------
    if show_help:
        guide = np.ones((300, 460, 3), dtype=np.uint8) * 245

        cv2.putText(guide, "GESTURE GUIDE", (120, 35),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 2)

        gestures = [
            "✋ Open Palm  : Activate Control",
            "👉 Swipe Right : Next Slide",
            "👈 Swipe Left  : Previous Slide",
            "🤏 Pinch In/Out : Zoom",
            "✊ Fist : Exit Presentation"
        ]

        y = 90
        for g in gestures:
            cv2.putText(guide, g, (20, y),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)
            y += 40

        cv2.imshow("Gesture Guide", guide)
        cv2.moveWindow("Gesture Guide", 900, 200)
    else:
        cv2.destroyWindow("Gesture Guide")

    cv2.imshow("Gesture-Controlled Presentation", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
