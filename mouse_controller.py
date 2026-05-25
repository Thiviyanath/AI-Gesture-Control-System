import pyautogui


class MouseController:

    def __init__(self):

        self.screen_width, self.screen_height = pyautogui.size()

        pyautogui.FAILSAFE = False

        # Previous mouse position
        self.prev_x = 0
        self.prev_y = 0

        # Smoothening factor
        self.smoothening = 2

    def move_mouse(self, x, y, frame_width, frame_height):

        # Convert webcam coordinates to screen coordinates
        screen_x = self.screen_width / frame_width * x
        screen_y = self.screen_height / frame_height * y

        # Smooth movement
        current_x = self.prev_x + (screen_x - self.prev_x) / self.smoothening
        current_y = self.prev_y + (screen_y - self.prev_y) / self.smoothening

        pyautogui.moveTo(current_x, current_y)

        # Store previous position
        self.prev_x = current_x
        self.prev_y = current_y

    def left_click(self):

        pyautogui.click()