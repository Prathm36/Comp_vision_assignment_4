import cv2
import mediapipe as mp
import numpy as np
import random

# Initialize MediaPipe Hands
mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils

# Game settings
width, height = 1280, 640
player_pos = [320, 440]  # Initial player position

# Initialize score
score = 0

flag = 0
# Initialize webcam
cap = cv2.VideoCapture(0)
a = random.randint(0, 900)
c = a + 100
b, d = 0, 100

while True:
    ret, frame = cap.read()

    frame = cv2.flip(frame, 1)  # Flip frame to mirror the user
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Reset enemy position when it reaches bottom of screen or gets hit
    if d >= 640 or flag == 1:
        a = random.randint(0, 600)
        b, d = 0, 100
        c = a + 100
        score += 20
    flag = 0
    cv2.rectangle(frame, (a, b), (c, d), (255, 0, 0), 1)

    b += 20     #speed of enemy
    d += 20

    # Process the frame with MediaPipe for hand detection
    results = hands.process(rgb_frame)

    # Get coordinates of the index finger tip (landmark 8) without affecting the rectangle
    if results.multi_hand_landmarks:
        handLms = results.multi_hand_landmarks[0]
        id_8_landmark = handLms.landmark[8]

        frame_height, frame_width, _ = frame.shape
        cx, cy = int(id_8_landmark.x * frame_width), int(id_8_landmark.y * frame_height)

        # Draw circle at the index finger tip (landmark 8)
        cv2.circle(frame, (cx, cy), 10, (255, 0, 0), cv2.FILLED)

        # Update player position based on the hand movement
        player_pos = [cx, cy]  # Move player based on hand movement

    # Draw player (for example, based on hand movement)
    cv2.circle(frame, tuple(player_pos), 20, (0, 255, 0), cv2.FILLED)

    # Display score on the frame
    cv2.putText(frame, f'Score: {score}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

    # Display the frame
    frame = cv2.resize(frame, (1280, 640))
    cv2.imshow("Object Dodging Game", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    if player_pos[0] > a and player_pos[0] < c and player_pos[1] > b and player_pos[1] < d:
        flag = 1
        '''a = random.randint(0, 1200)
        b, d = 0, 100
        c = a + 100'''
        score -= 30

cap.release()
cv2.destroyAllWindows()
