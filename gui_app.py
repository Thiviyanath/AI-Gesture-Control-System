from hand_tracker import HandTracker
from gesture_detector import GestureDetector
from mouse_controller import MouseController

import time
import sys
import cv2

from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QFrame
)

from PyQt5.QtCore import Qt, QTimer

from PyQt5.QtGui import QFont, QImage, QPixmap


class GestureApp(QWidget):

    def __init__(self):

        super().__init__()

        # =========================
        # CAMERA
        # =========================

        self.cap = None

        # =========================
        # AI SYSTEM
        # =========================

        self.tracker = HandTracker()

        self.detector = GestureDetector()

        self.mouse = MouseController()

        # =========================
        # GESTURE SETTINGS
        # =========================

        self.gesture_text = "No Gesture"

        self.click_threshold = 40

        self.click_cooldown = 0

        # =========================
        # FPS VARIABLES
        # =========================

        self.previous_time = time.time()

        self.current_time = 0

        # =========================
        # TIMER
        # =========================

        self.timer = QTimer()

        self.timer.timeout.connect(self.update_frame)

        # =========================
        # WINDOW SETTINGS
        # =========================

        self.setWindowTitle("AI Gesture Control System")

        self.setGeometry(100, 100, 1000, 650)

        self.setStyleSheet("""
            background-color: #0f172a;
        """)

        # Build UI
        self.init_ui()

    # =========================
    # UI
    # =========================

    def init_ui(self):

        # =========================
        # MAIN LAYOUT
        # =========================

        main_layout = QHBoxLayout()

        main_layout.setContentsMargins(30, 30, 30, 30)

        # =========================
        # SIDEBAR
        # =========================

        sidebar = QFrame()

        sidebar.setFixedWidth(220)

        sidebar.setStyleSheet("""
            QFrame {
                background: rgba(255,255,255,0.06);
                border-radius: 25px;
                border: 1px solid rgba(255,255,255,0.1);
            }
        """)

        sidebar_layout = QVBoxLayout()

        sidebar_layout.setContentsMargins(20, 20, 20, 20)

        sidebar_layout.setSpacing(20)

        # =========================
        # SIDEBAR TITLE
        # =========================

        sidebar_title = QLabel("AI Dashboard")

        sidebar_title.setFont(QFont("Segoe UI", 18, QFont.Bold))

        sidebar_title.setStyleSheet("""
            color: white;
        """)

        sidebar_layout.addWidget(sidebar_title)

        # =========================
        # SIDEBAR BUTTONS
        # =========================

        buttons = [
            "Mouse Control",
            "Presentation",
            "Drawing Mode",
            "Media Control",
            "Settings"
        ]

        for text in buttons:
            button = QPushButton(text)

            button.setCursor(Qt.PointingHandCursor)

            button.setFixedHeight(50)

            button.setStyleSheet("""
                QPushButton {
                    background-color: rgba(255,255,255,0.05);
                    color: white;
                    border-radius: 15px;
                    font-size: 15px;
                    text-align: left;
                    padding-left: 15px;
                }

                QPushButton:hover {
                    background-color: rgba(6,182,212,0.3);
                    border: 1px solid #06b6d4;
                }
            """)

            sidebar_layout.addWidget(button)

        sidebar_layout.addStretch()

        sidebar.setLayout(sidebar_layout)

        # =========================
        # CONTENT AREA
        # =========================

        content_layout = QVBoxLayout()

        # =========================
        # TOP INFO CARDS
        # =========================

        info_layout = QHBoxLayout()

        info_layout.setSpacing(15)

        card_style = """
            QFrame {
                background: rgba(255,255,255,0.06);
                border-radius: 20px;
                border: 1px solid rgba(255,255,255,0.1);
            }
        """

        # FPS CARD

        fps_card = QFrame()

        fps_card.setStyleSheet(card_style)

        fps_layout = QVBoxLayout()

        fps_title = QLabel("FPS")

        fps_title.setStyleSheet("color: #94a3b8; font-size: 14px;")

        self.fps_value = QLabel("0")

        self.fps_value.setStyleSheet("""
            color: white;
            font-size: 28px;
            font-weight: bold;
        """)

        fps_layout.addWidget(fps_title)

        fps_layout.addWidget(self.fps_value)

        fps_card.setLayout(fps_layout)

        info_layout.addWidget(fps_card)

        # GESTURE CARD

        gesture_card = QFrame()

        gesture_card.setStyleSheet(card_style)

        gesture_layout = QVBoxLayout()

        gesture_title = QLabel("Gesture")

        gesture_title.setStyleSheet("""
            color: #94a3b8;
            font-size: 14px;
        """)

        self.gesture_value = QLabel("None")

        self.gesture_value.setStyleSheet("""
            color: #06b6d4;
            font-size: 22px;
            font-weight: bold;
        """)

        gesture_layout.addWidget(gesture_title)

        gesture_layout.addWidget(self.gesture_value)

        gesture_card.setLayout(gesture_layout)

        info_layout.addWidget(gesture_card)

        # STATUS CARD

        status_card = QFrame()

        status_card.setStyleSheet(card_style)

        status_layout = QVBoxLayout()

        status_title = QLabel("System")

        status_title.setStyleSheet("""
            color: #94a3b8;
            font-size: 14px;
        """)

        self.system_value = QLabel("Ready")

        self.system_value.setStyleSheet("""
            color: #22c55e;
            font-size: 22px;
            font-weight: bold;
        """)

        status_layout.addWidget(status_title)

        status_layout.addWidget(self.system_value)

        status_card.setLayout(status_layout)

        info_layout.addWidget(status_card)

        # =========================
        # TITLE
        # =========================

        title = QLabel("AI Gesture Control System")

        title.setFont(QFont("Segoe UI", 24, QFont.Bold))

        title.setStyleSheet("""
            color: white;
            margin-bottom: 20px;
        """)

        title.setAlignment(Qt.AlignCenter)

        # =========================
        # GLASS CARD
        # =========================

        glass_card = QFrame()

        glass_card.setStyleSheet("""
            QFrame {
                background: rgba(255, 255, 255, 0.08);
                border-radius: 25px;
                border: 1px solid rgba(255, 255, 255, 0.15);
            }
        """)

        card_layout = QVBoxLayout()

        card_layout.setContentsMargins(30, 30, 30, 30)

        # =========================
        # STATUS LABEL
        # =========================

        self.status_label = QLabel("System Ready")

        self.status_label.setFont(QFont("Segoe UI", 16))

        self.status_label.setStyleSheet("""
            color: #cbd5e1;
            margin-bottom: 20px;
        """)

        self.status_label.setAlignment(Qt.AlignCenter)

        card_layout.addWidget(self.status_label)

        # =========================
        # CAMERA BOX
        # =========================

        self.camera_box = QLabel("Live Camera Feed")

        self.camera_box.setFixedHeight(350)

        self.camera_box.setAlignment(Qt.AlignCenter)

        self.camera_box.setStyleSheet("""
            background-color: rgba(255,255,255,0.05);
            border-radius: 20px;
            border: 2px dashed rgba(255,255,255,0.1);
            color: #94a3b8;
            font-size: 18px;
        """)

        card_layout.addWidget(self.camera_box)

        # =========================
        # BUTTON LAYOUT
        # =========================

        button_layout = QHBoxLayout()

        # START BUTTON

        self.start_button = QPushButton("Start System")

        self.start_button.setCursor(Qt.PointingHandCursor)

        self.start_button.setStyleSheet("""
            QPushButton {
                background-color: #06b6d4;
                color: white;
                border-radius: 15px;
                padding: 15px;
                font-size: 16px;
                font-weight: bold;
            }

            QPushButton:hover {
                background-color: #0891b2;
            }
        """)

        self.start_button.clicked.connect(self.start_camera)

        button_layout.addWidget(self.start_button)

        # STOP BUTTON

        self.stop_button = QPushButton("Stop System")

        self.stop_button.setCursor(Qt.PointingHandCursor)

        self.stop_button.setStyleSheet("""
            QPushButton {
                background-color: #ef4444;
                color: white;
                border-radius: 15px;
                padding: 15px;
                font-size: 16px;
                font-weight: bold;
            }

            QPushButton:hover {
                background-color: #dc2626;
            }
        """)

        self.stop_button.clicked.connect(self.stop_camera)

        button_layout.addWidget(self.stop_button)

        # =========================
        # ADD LAYOUTS
        # =========================

        card_layout.addLayout(button_layout)

        glass_card.setLayout(card_layout)

        content_layout.addWidget(title)
        content_layout.addLayout(info_layout)

        fps = 1 / (
                self.current_time - self.previous_time
        )
        self.fps_value.setText(str(int(fps)))
        self.gesture_text = "LEFT CLICK"

        self.gesture_value.setText(self.gesture_text)
        self.gesture_text = "MOVE MODE"

        content_layout.addWidget(glass_card)

        # =========================
        # FINAL MAIN LAYOUT
        # =========================

        main_layout.addWidget(sidebar)

        main_layout.addLayout(content_layout)

        self.setLayout(main_layout)

    # =========================
    # START CAMERA
    # =========================

    def start_camera(self):

        self.system_value.setText("Running")
        self.system_value.setText("Stopped")

        self.cap = cv2.VideoCapture(0)

        self.timer.start(30)

        self.status_label.setText("System Running")

    # =========================
    # STOP CAMERA
    # =========================

    def stop_camera(self):

        self.timer.stop()

        if self.cap:
            self.cap.release()
            self.cap = None

        self.camera_box.setText("Camera Stopped")

        self.status_label.setText("System Stopped")

    # =========================
    # UPDATE FRAME
    # =========================

    def update_frame(self):

        if self.cap is None:
            return

        success, frame = self.cap.read()

        if not success:
            return

        # Reset gesture text
        self.gesture_text = "No Gesture"

        # Flip camera
        frame = cv2.flip(frame, 1)

        # =========================
        # AI HAND DETECTION
        # =========================

        frame_height, frame_width, _ = frame.shape

        results = self.tracker.detect_hands(frame)

        frame = self.tracker.draw_landmarks(
            frame,
            results
        )

        if results.multi_hand_landmarks:

            for hand_landmarks in results.multi_hand_landmarks:

                fingers = self.detector.get_fingers_up(
                    hand_landmarks
                )

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
                # MOVE MOUSE
                # =========================

                if fingers == [0, 1, 0, 0, 0]:

                    self.gesture_text = "MOVE MODE"

                    self.mouse.move_mouse(
                        x,
                        y,
                        frame_width,
                        frame_height
                    )

                # =========================
                # THUMB
                # =========================

                thumb_tip = landmarks[4]

                thumb_x = int(thumb_tip.x * frame_width)
                thumb_y = int(thumb_tip.y * frame_height)

                # =========================
                # CLICK DISTANCE
                # =========================

                distance = self.detector.calculate_distance(
                    (x, y),
                    (thumb_x, thumb_y)
                )

                # =========================
                # DRAW LINE
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

                if distance < self.click_threshold:

                    self.gesture_text = "LEFT CLICK"

                    cv2.putText(
                        frame,
                        "LEFT CLICK",
                        (20, 100),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1,
                        (0, 0, 255),
                        3
                    )

                    if self.click_cooldown == 0:

                        self.mouse.left_click()

                        self.click_cooldown = 20

        # =========================
        # REDUCE COOLDOWN
        # =========================

        if self.click_cooldown > 0:

            self.click_cooldown -= 1

        # =========================
        # FPS
        # =========================

        self.current_time = time.time()

        fps = 1 / (
            self.current_time - self.previous_time
        )

        self.previous_time = self.current_time

        cv2.putText(
            frame,
            f"FPS: {int(fps)}",
            (20, 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (255, 255, 255),
            2
        )

        # =========================
        # GESTURE TEXT
        # =========================

        cv2.putText(
            frame,
            f"Gesture: {self.gesture_text}",
            (20, 150),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 255),
            2
        )

        # =========================
        # CONVERT FRAME
        # =========================

        rgb_frame = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2RGB
        )

        h, w, ch = rgb_frame.shape

        bytes_per_line = ch * w

        # Convert to QImage
        qt_image = QImage(
            rgb_frame.data,
            w,
            h,
            bytes_per_line,
            QImage.Format_RGB888
        )

        # Convert to Pixmap
        pixmap = QPixmap.fromImage(qt_image)

        # Display inside UI
        self.camera_box.setPixmap(
            pixmap.scaled(
                self.camera_box.width(),
                self.camera_box.height(),
                Qt.KeepAspectRatio
            )
        )

    # =========================
    # WINDOW CLOSE EVENT
    # =========================

    def closeEvent(self, event):

        self.stop_camera()

        event.accept()


# =========================
# RUN APPLICATION
# =========================

app = QApplication(sys.argv)

window = GestureApp()

window.show()

sys.exit(app.exec_())