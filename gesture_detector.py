import math


class GestureDetector:

    def __init__(self):

        self.finger_tips = [4, 8, 12, 16, 20]

    def get_fingers_up(self, hand_landmarks):

        fingers = []

        landmarks = hand_landmarks.landmark

        # Thumb
        if landmarks[4].x < landmarks[3].x:
            fingers.append(1)
        else:
            fingers.append(0)

        # Other fingers
        for tip in self.finger_tips[1:]:

            if landmarks[tip].y < landmarks[tip - 2].y:
                fingers.append(1)
            else:
                fingers.append(0)

        return fingers

    def calculate_distance(self, point1, point2):

        x1, y1 = point1
        x2, y2 = point2

        distance = math.hypot(x2 - x1, y2 - y1)

        return distance