import pyautogui


class MouseController:

    def __init__(self):

        self.screen_width, self.screen_height = pyautogui.size()

        pyautogui.FAILSAFE = False

    def move_mouse(self, x, y, frame_width, frame_height):

        screen_x = self.screen_width / frame_width * x
        screen_y = self.screen_height / frame_height * y

        pyautogui.moveTo(screen_x, screen_y)

    def left_click(self):

        pyautogui.click()