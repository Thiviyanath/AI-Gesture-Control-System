import cv2

from hand_tracker import HandTracker
from gesture_detector import GestureDetector
from mouse_controller import MouseController

cap = cv2.VideoCapture(0)

tracker = HandTracker()

detector = GestureDetector()

mouse = MouseController()

click_threshold = 40

click_cooldown = 0

while True:

    success, frame = cap.read()

    if not success:
        break

    frame = cv2.flip(frame, 1)

    frame_height, frame_width, _ = frame.shape

    results = tracker.detect_hands(frame)

    frame = tracker.draw_landmarks(frame, results)

    if results.multi_hand_landmarks:

        for hand_landmarks in results.multi_hand_landmarks:

            fingers = detector.get_fingers_up(hand_landmarks)

            landmarks = hand_landmarks.landmark

            # Index finger tip
            index_tip = landmarks[8]

            x = int(index_tip.x * frame_width)
            y = int(index_tip.y * frame_height)

            # Draw cursor point
            cv2.circle(frame, (x, y), 20,(255, 0, 255), cv2.FILLED)

            # Move mouse if index finger up
            if fingers[1] == 1:

                mouse.move_mouse(
                    x,
                    y,
                    frame_width,
                    frame_height
                )

            # Thumb tip
            thumb_tip = landmarks[4]

            thumb_x = int(thumb_tip.x * frame_width)
            thumb_y = int(thumb_tip.y * frame_height)

            # Calculate distance
            distance = detector.calculate_distance(
                (x, y),
                (thumb_x, thumb_y)
            )

            # Draw line
            cv2.line(
                frame,
                (x, y),
                (thumb_x, thumb_y),
                (0, 255, 0),
                3
            )
            cv2.putText(
                frame,
                "Thivi's AI Gesture Sysem",
                (20, 450),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (255, 255, 255),
                2
            )
            # Show distance
            cv2.putText(
                frame,
                f"Distance: {int(distance)}",
                (20, 100),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (255, 255, 0),
                2
            )

            # Click detection
            if distance < click_threshold:

                cv2.putText(
                    frame,
                    "CLICK",
                    (20, 150),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 0, 255),
                    3
                )

                if click_cooldown == 0:

                    mouse.left_click()

                    click_cooldown = 20

    # Reduce cooldown
    if click_cooldown > 0:
        click_cooldown -= 1

    cv2.imshow("AI Gesture Mouse Control", frame)

    key = cv2.waitKey(1)

    if key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()