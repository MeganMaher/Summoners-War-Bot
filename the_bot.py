from PIL import ImageGrab
import os, sys, shutil
import time
import cv2
import win32api, win32con
import time
import random
from datetime import datetime, timedelta
import shutil

images_path = os.path.join(os.getcwd(), 'images')
templates_path = os.path.join(images_path, 'templates')

MATCH_METHOD = cv2.TM_SQDIFF_NORMED
TEMPLATE_MATCH_TOLERANCE = 0.01

class SummonersWarBot:
    def __init__(self):
        pass

    def get_current_window(self):
            # Get a screenshot of the full screen
            im = ImageGrab.grab()
            filename = os.path.join(images_path, 'full_screen.png')
            im.save(filename, 'PNG')
            self.full_screen = cv2.imread(filename)
    
    def click(self, x, y):
        #x += self.BOX_LEFT
        #y += self.BOX_TOP
        win32api.SetCursorPos((x,y))
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,x,y,0,0)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,x,y,0,0)

    def click_on_template(self, template_name, tolerance=TEMPLATE_MATCH_TOLERANCE):
        swb.get_current_window()
        template_image = cv2.imread(os.path.join(templates_path, template_name))
        result = cv2.matchTemplate(self.full_screen, template_image, MATCH_METHOD)
        match_data = cv2.minMaxLoc(result)
        match_deviation = match_data[0]
        template_location = match_data[2]
        print(template_name + ': ', match_data)

        if match_deviation < tolerance:
            x_location = template_location[0] + 10
            y_location = template_location[1] + 15

            self.click(x_location, y_location)
            return (x_location, y_location)
        return False

    def click_through_victory_screen(self):
        r = self.click_on_template('template_victory_bolt.png', tolerance=0.2)
        if r:
            x_location, y_location = r
            time.sleep(1.0)
            self.click(x_location, y_location)
            time.sleep(2.0)

            ok_result = self.click_on_template('template_ok_button.png', tolerance = 0.15)
            get_result = False
            if not ok_result:
                get_result = self.click_on_template('template_get_button.png')

            if ok_result or get_result:
                time.sleep(2.0)
                if self.click_on_template('template_replay_button.png', tolerance=0.25):
                    time.sleep(2.0)
                    self.click_on_template('template_startbattle_button.png', tolerance=0.15)
        else:
            self.click_on_template('template_levelup_screen.png', tolerance=0.08)






if __name__ == "__main__":
    swb = SummonersWarBot()

    while True:
        swb.click_through_victory_screen()
        time.sleep(20.0)