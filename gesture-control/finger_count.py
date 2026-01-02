import cv2
import mediapipe as mp

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

# Finger tip landmarks
TIP_IDS = [4, 8, 12, 16, 20]

def count_fingers(hand_landmarks):
    fingers = []

    # Thumb (x-axis check)
    fingers.append(
        hand_landmarks.landmark[TIP_IDS[0]].x <
        hand_landmarks.landmark[TIP_IDS[0] - 1].x
    )

    # Other fingers (y-axis check)
    for i in range(1, 5):
        fingers.append(
            hand_landmarks.landmark[TIP_IDS[i]].y <
            hand_landmarks.landmark[TIP_IDS[i] - 2].y
        )

    return fingers.count(True)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            count = count_fingers(hand_landmarks)

            cv2.putText(frame, f"Fingers: {count}",
                        (20, 50), cv2.FONT_HERSHEY_SIMPLEX,
                        1, (0, 255, 0), 2)

    cv2.imshow("Finger Count", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
