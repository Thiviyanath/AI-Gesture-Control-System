import cv2
import time

from hand_tracker import HandTracker
from gesture_detector import GestureDetector
from mouse_controller import MouseController

# Open webcam
cap = cv2.VideoCapture(0)

# Initialize classes
tracker = HandTracker()
detector = GestureDetector()
mouse = MouseController()

# FPS variables
previous_time = 0
current_time = 0

# Click settings
click_threshold = 40

click_cooldown = 0
right_click_cooldown = 0
slide_cooldown = 0

# Gesture text
gesture_text = "No Gesture"

current_mode = "MOUSE MODE"

# Scroll tracking
previous_scroll_y = 0



while True:

    success, frame = cap.read()

    if not success:
        break

    # Flip frame for mirror effect
    frame = cv2.flip(frame, 1)

    # Get frame size
    frame_height, frame_width, _ = frame.shape

    # Detect hands
    results = tracker.detect_hands(frame)

    # Draw hand landmarks
    frame = tracker.draw_landmarks(frame, results)

    if results.multi_hand_landmarks:

        for hand_landmarks in results.multi_hand_landmarks:

            # Get finger states
            fingers = detector.get_fingers_up(hand_landmarks)

            # Switch to Presentation Mode
            if fingers == [1, 1, 1, 1, 1]:
                current_mode = "PRESENTATION MODE"

            # Switch to Mouse Mode
            if fingers == [0, 0, 0, 0, 0]:
                current_mode = "MOUSE MODE"

            # Get all landmarks
            landmarks = hand_landmarks.landmark

            # =========================
            # INDEX FINGER
            # =========================

            index_tip = landmarks[8]

            x = int(index_tip.x * frame_width)
            y = int(index_tip.y * frame_height)

            # Draw cursor point
            cv2.circle(
                frame,
                (x, y),
                20,
                (255, 0, 255),
                cv2.FILLED
            )

            # =========================
            # MOUSE MOVE MODE
            # =========================

            if fingers == [0, 1, 0, 0, 0]:

                gesture_text = "MOVE MODE"

                mouse.move_mouse(
                    x,
                    y,
                    frame_width,
                    frame_height
                )

            # =========================
            # SCROLL MODE
            # =========================

            if fingers == [0, 1, 1, 0, 0]:

                gesture_text = "SCROLL MODE"

                middle_tip = landmarks[12]

                middle_y = int(middle_tip.y * frame_height)

                # Scroll Up
                if middle_y < previous_scroll_y - 15:
                    mouse.scroll(80)

                # Scroll Down
                elif middle_y > previous_scroll_y + 15:
                    mouse.scroll(-80)

                previous_scroll_y = middle_y

            # =========================
            # THUMB LANDMARK
            # =========================

            thumb_tip = landmarks[4]

            thumb_x = int(thumb_tip.x * frame_width)
            thumb_y = int(thumb_tip.y * frame_height)

            # =========================
            # MIDDLE FINGER
            # =========================

            middle_tip = landmarks[12]

            middle_x = int(middle_tip.x * frame_width)
            middle_y = int(middle_tip.y * frame_height)

            # =========================
            # DISTANCES
            # =========================

            # Left click distance
            left_click_distance = detector.calculate_distance(
                (x, y),
                (thumb_x, thumb_y)
            )

            # Right click distance
            right_click_distance = detector.calculate_distance(
                (thumb_x, thumb_y),
                (middle_x, middle_y)
            )

            # =========================
            # VISUAL LINES
            # =========================

            cv2.line(
                frame,
                (x, y),
                (thumb_x, thumb_y),
                (0, 255, 0),
                3
            )

            # =========================
            # LEFT CLICK
            # =========================

            if left_click_distance < click_threshold:

                gesture_text = "LEFT CLICK"

                cv2.putText(
                    frame,
                    "LEFT CLICK",
                    (20, 150),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 0, 255),
                    3
                )

                if click_cooldown == 0:

                    mouse.left_click()

                    click_cooldown = 20

            # =========================
            # RIGHT CLICK
            # =========================

            if right_click_distance < click_threshold:

                gesture_text = "RIGHT CLICK"

                cv2.putText(
                    frame,
                    "RIGHT CLICK",
                    (20, 300),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (255, 0, 0),
                    3
                )

                if right_click_cooldown == 0:

                    mouse.right_click()

                    right_click_cooldown = 20

            # =========================
            # PRESENTATION MODE
            # =========================

            if current_mode == "PRESENTATION MODE":

                # Next Slide Gesture
                if fingers == [0, 1, 1, 1, 0]:

                    gesture_text = "NEXT SLIDE"

                    cv2.putText(
                        frame,
                        "NEXT SLIDE",
                        (20, 400),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1,
                        (0, 255, 0),
                        3
                    )

                    if slide_cooldown == 0:
                        mouse.next_slide()

                        slide_cooldown = 30

                # Previous Slide Gesture
                if fingers == [0, 1, 0, 0, 1]:

                    gesture_text = "PREVIOUS SLIDE"

                    cv2.putText(
                        frame,
                        "PREVIOUS SLIDE",
                        (20, 400),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1,
                        (0, 255, 255),
                        3
                    )

                    if slide_cooldown == 0:
                        mouse.previous_slide()

                        slide_cooldown = 30

            # =========================
            # DISTANCE DISPLAY
            # =========================

            cv2.putText(
                frame,
                f"Distance: {int(left_click_distance)}",
                (20, 100),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (255, 255, 0),
                2
            )

            # =========================
            # APP TITLE
            # =========================

            cv2.putText(
                frame,
                "Thivi's AI Gesture System",
                (20, 450),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (255, 255, 255),
                2
            )

    # =========================
    # REDUCE COOLDOWNS
    # =========================

    if click_cooldown > 0:
        click_cooldown -= 1

    if right_click_cooldown > 0:
        right_click_cooldown -= 1

    if slide_cooldown > 0:
            slide_cooldown -= 1

    # =========================
    # FPS CALCULATION
    # =========================

    current_time = time.time()

    fps = 1 / (current_time - previous_time)

    previous_time = current_time

    cv2.putText(
        frame,
        f"FPS: {int(fps)}",
        (20, 200),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (255, 255, 255),
        2
    )

    # =========================
    # GESTURE DISPLAY
    # =========================

    cv2.putText(
        frame,
        f"Gesture: {gesture_text}",
        (20, 250),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 255),
        2
    )

    cv2.putText(
        frame,
        f"Mode: {current_mode}",
        (20, 350),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 0),
        2
    )

    # Show webcam window
    cv2.imshow("AI Gesture Mouse Control", frame)

    # Press Q to quit
    key = cv2.waitKey(1)

    if key == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()