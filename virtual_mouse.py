import time

import cv2
import mediapipe as mp
import pyautogui


CLICK_DISTANCE = 45
MOVE_DISTANCE = 150
DOUBLE_CLICK_SECONDS = 0.3


def landmark_to_screen(landmark, frame_width, frame_height, screen_width, screen_height):
    x = int(landmark.x * frame_width)
    y = int(landmark.y * frame_height)
    screen_x = screen_width / frame_width * x
    screen_y = screen_height / frame_height * y
    return x, y, screen_x, screen_y


def run_virtual_mouse(camera_index=0):
    cap = cv2.VideoCapture(camera_index)
    if not cap.isOpened():
        raise RuntimeError("Could not open webcam")

    hands_detector = mp.solutions.hands.Hands(
        max_num_hands=1,
        min_detection_confidence=0.7,
        min_tracking_confidence=0.7,
    )
    drawing_utils = mp.solutions.drawing_utils
    screen_width, screen_height = pyautogui.size()
    last_click_time = 0

    try:
        while True:
            ok, frame = cap.read()
            if not ok:
                break

            frame = cv2.flip(frame, 1)
            frame_height, frame_width, _ = frame.shape
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            result = hands_detector.process(rgb_frame)

            if result.multi_hand_landmarks:
                hand = result.multi_hand_landmarks[0]
                drawing_utils.draw_landmarks(frame, hand, mp.solutions.hands.HAND_CONNECTIONS)
                landmarks = hand.landmark

                index_x, index_y, screen_x, screen_y = landmark_to_screen(
                    landmarks[8],
                    frame_width,
                    frame_height,
                    screen_width,
                    screen_height,
                )
                thumb_x, thumb_y, _, _ = landmark_to_screen(
                    landmarks[4],
                    frame_width,
                    frame_height,
                    screen_width,
                    screen_height,
                )

                cv2.circle(frame, (index_x, index_y), 10, (0, 255, 255), -1)
                cv2.circle(frame, (thumb_x, thumb_y), 10, (0, 255, 255), -1)

                finger_gap = abs(index_y - thumb_y)
                if finger_gap < CLICK_DISTANCE:
                    current_time = time.time()
                    clicks = 2 if current_time - last_click_time < DOUBLE_CLICK_SECONDS else 1
                    pyautogui.click(clicks=clicks)
                    last_click_time = current_time
                elif finger_gap < MOVE_DISTANCE:
                    pyautogui.moveTo(screen_x, screen_y)

            cv2.imshow("Gesture Mouse Control", frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
    finally:
        hands_detector.close()
        cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    run_virtual_mouse()
