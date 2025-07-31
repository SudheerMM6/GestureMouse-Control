#!/usr/bin/env python
# coding: utf-8

# In[2]:


import cv2
import mediapipe as mp
import pyautogui
import os  # to open files
import time  # for double-click timing

cap = cv2.VideoCapture(0)  # Open the webcam
hand_detector = mp.solutions.hands.Hands()  # Initialize the hand detector
drawing_utils = mp.solutions.drawing_utils  # Utility for drawing hand landmarks
screen_width, screen_height = pyautogui.size()  # Get the screen size
index_y = 0  # Variable to store index finger's y-coordinate

# Variable to store time for double-click
last_click_time = 0

while True:
    ret, frame = cap.read()  # Read a frame from the webcam
    if not ret:
        break  # If there's an error, break the loop

    frame = cv2.flip(frame, 1)  # Flip the frame horizontally
    frame_height, frame_width, _ = frame.shape  # Get frame dimensions
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convert to RGB
    output = hand_detector.process(rgb_frame)  # Detect hands
    hands = output.multi_hand_landmarks  # Get hand landmarks

    if hands:  # If hands are detected
        for hand in hands:
            drawing_utils.draw_landmarks(frame, hand)  # Draw the hand landmarks
            landmarks = hand.landmark  # Get landmarks for the hand
            for id, landmark in enumerate(landmarks):
                x = int(landmark.x * frame_width)  # Convert to pixel coordinates
                y = int(landmark.y * frame_height)

                if id == 8:  # Index finger
                    cv2.circle(img=frame, center=(x, y), radius=10, color=(0, 255, 255))
                    index_x = screen_width / frame_width * x
                    index_y = screen_height / frame_height * y

                if id == 4:  # Thumb
                    cv2.circle(img=frame, center=(x, y), radius=10, color=(0, 255, 255))
                    thumb_x = screen_width / frame_width * x
                    thumb_y = screen_height / frame_height * y

                    # Condition to detect thumb and index finger proximity
                    if abs(index_y - thumb_y) < 50:  # When thumb is close to the index
                        # Check for double-click based on timing
                        current_time = time.time()
                        if current_time - last_click_time < 0.3:
                            pyautogui.click(clicks=2)  # Double-click
                            # Open a specific file (modify the path as needed)
                            #os.startfile("Desktop\\poster.jpg")  # Example file
                        else:
                            pyautogui.click()  # Single-click
                        last_click_time = current_time
                    elif (abs(index_y - thumb_y) > 50 and abs(index_y - thumb_y) < 150):
                        pyautogui.moveTo(index_x, index_y)  # Move cursor

    cv2.imshow('Virtual Mouse', frame)  # Show the frame

    if cv2.waitKey(1) & 0xFF == ord('q'):  # Exit if 'q' is pressed
        break  # Exit the loop

cap.release()  # Release the webcam
cv2.destroyAllWindows()  # Close all OpenCV windows


# In[ ]:





# In[ ]:




