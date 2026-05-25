import cv2

from hand_tracker import HandTracker
from gesture_detector import GestureDetector

cap = cv2.VideoCapture(0)

tracker = HandTracker()

detector = GestureDetector()

while True:

    success, frame = cap.read()

    if not success:
        break

    frame = cv2.flip(frame, 1)

    results = tracker.detect_hands(frame)

    frame = tracker.draw_landmarks(frame, results)

    if results.multi_hand_landmarks:

        for hand_landmarks in results.multi_hand_landmarks:

            fingers = detector.get_fingers_up(hand_landmarks)

            total_fingers = fingers.count(1)

            cv2.putText(
                frame,
                f"Fingers: {total_fingers}",
                (20, 50),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 0),
                2
            )

    cv2.imshow("AI Gesture Control", frame)

    key = cv2.waitKey(1)

    if key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()