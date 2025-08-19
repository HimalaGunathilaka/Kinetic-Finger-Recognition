import cv2
import mediapipe as mp
import uinput
import numpy as np

# Example: screen width/height or step scaling
step = 100  # relative movement step size

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=2,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)
mp_draw = mp.solutions.drawing_utils

# Start webcam
cap = cv2.VideoCapture(0)

# Create the uinput device once
device = uinput.Device([uinput.REL_X, uinput.REL_Y, uinput.BTN_LEFT])

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    result = hands.process(rgb_frame)

    if result.multi_hand_landmarks and result.multi_handedness:
        for hand_landmarks, handedness in zip(result.multi_hand_landmarks, result.multi_handedness):
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            
            landmarks = np.array([[lm.x, lm.y] for lm in hand_landmarks.landmark])
            
            go_vector = landmarks[8]-landmarks[7]
            
            diff1 = (go_vector) / np.sqrt(go_vector[0] ** 2 + go_vector[1]**2)
            

            # Convert normalized coordinates to relative movement
            dx = int((go_vector[0] ) * step * 2)
            dy = int((go_vector[1] ) * step * 2)
            
            print(go_vector)

            # Move the mouse
            device.emit(uinput.REL_X, dx)
            device.emit(uinput.REL_Y, dy)

    cv2.imshow("Hand Landmarks", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
