import keyboard
import pyautogui
import time
import ctypes
import winsound
import os
import mss
from colorama import Fore, Style, init
import PIL.ImageGrab 

S_HEIGHT, S_WIDTH = (PIL.ImageGrab.grab().size)
PURPLE_COLOR = (250, 100, 250)
TOLERANCE = 31
GRABZONE = 10
TRIGGER_KEY = "f12"
SWITCH_KEY = "ctrl + tab"
GRABZONE_KEY_UP = "ctrl + up"
GRABZONE_KEY_DOWN = "ctrl + down"
MODE_KEYS = ["f1", "f2", "f3", "f4", "f5", "f6", "f7", "f8"]
MODES = ["SHERIFF", "SPECTRE", "GUARDIAN/SHOTGUN", "VANDAL/PHANTOM", "MARSHAL FASTSCOPE", "OPERATOR FASTSCOPE", "MARSHAL/OPERATOR SCOPE", "ODIN"]
DELAY_TIMES = [0.09, 0.025, 0.0995, 0.045, 0.0995, 0.0995, 0]

class FoundEnemy(Exception):
    pass

class TriggerBot:
    def __init__(self):
        self.toggled = False
        self.mode = 0
        self.last_reac = 0
        self.ctrl_pressed = False
        self.shooting = False

    def toggle(self):
        self.toggled = not self.toggled

    def switch(self):
        self.mode = (self.mode + 1) % len(MODES)

    def click(self):
        if self.mode == 3:
            keyboard.press('w+a+s+d')
            time.sleep(DELAY_TIMES[self.mode])
            ctypes.windll.user32.mouse_event(2, 0, 0, 0, 0)
            time.sleep(0.25)
            ctypes.windll.user32.mouse_event(4, 0, 0, 0, 0)
            keyboard.release('w+a+s+d')
        elif self.mode < len(DELAY_TIMES):
            keyboard.press('w+a+s+d')
            time.sleep(DELAY_TIMES[self.mode])
            ctypes.windll.user32.mouse_event(2, 0, 0, 0, 0)
            ctypes.windll.user32.mouse_event(4, 0, 0, 0, 0)
            keyboard.release('w+a+s+d')
            
        else:
            while True:
                if keyboard.is_pressed('ctrl'):
                    self.ctrl_pressed = True
                    if not self.shooting:
                        ctypes.windll.user32.mouse_event(2, 0, 0, 0, 0)
                        self.shooting = True
                else:
                    if self.shooting:
                        self.shooting = False
                        ctypes.windll.user32.mouse_event(4, 0, 0, 0, 0)
                    if self.ctrl_pressed:
                        self.ctrl_pressed = False
                    break

    def approx(self, r, g, b):
        return all(PURPLE_COLOR[i] - TOLERANCE < c < PURPLE_COLOR[i] + TOLERANCE for i, c in enumerate([r, g, b]))

    def grab(self):
        with mss.mss() as sct:
            bbox = (
                int(S_HEIGHT / 2 - GRABZONE),
                int(S_WIDTH / 2 - GRABZONE),
                int(S_HEIGHT / 2 + GRABZONE),
                int(S_WIDTH / 2 + GRABZONE),
            )
            sct_img = sct.grab(bbox)
            return PIL.Image.frombytes('RGB', sct_img.size, sct_img.bgra, 'raw', 'BGRX')

    def scan(self):
        start_time = time.time()
        pmap = self.grab()
        
        try:
            for x in range(0, GRABZONE * 2):
                for y in range(0, GRABZONE * 2):
                    r, g, b = pmap.getpixel((x, y))
                    if self.approx(r, g, b):
                        raise FoundEnemy
        except FoundEnemy:
            self.last_reac = int((time.time() - start_time) * 1000)
            self.click()
            if self.mode < len(DELAY_TIMES):
                time.sleep(0.5)
            else:
                time.sleep(0.5)  

def print_banner(bot):
    os.system("cls")
    print(Style.BRIGHT + Fore.CYAN + "kk278" + Style.RESET_ALL)
    print("===== Controls =====")
    print("Active     :", Fore.YELLOW + TRIGGER_KEY + Style.RESET_ALL)
    print("Change gun f(1 - 8) ", Fore.YELLOW + Style.RESET_ALL)
    print("Range      :", Fore.YELLOW + GRABZONE_KEY_UP + "/" + GRABZONE_KEY_DOWN + Style.RESET_ALL)
    print("====================")
    print("Gun        :", Fore.CYAN + MODES[bot.mode] + Style.RESET_ALL)
    print("Range      :", Fore.CYAN + str(GRABZONE) + "x" + str(GRABZONE) + Style.RESET_ALL)
    print("Trigger bot:", (Fore.GREEN if bot.toggled else Fore.RED) + ("On" if bot.toggled else "Off") + Style.RESET_ALL)
    print("Delay      :", Fore.CYAN + str(bot.last_reac) + Style.RESET_ALL + " ms (" + str((bot.last_reac) / (GRABZONE * GRABZONE)) + "ms/pixel)")

bot = TriggerBot()
print_banner(bot)

while True:
    if keyboard.is_pressed(SWITCH_KEY):
        bot.switch()
        winsound.Beep(200, 200)
        print_banner(bot)
        while keyboard.is_pressed(SWITCH_KEY):
            pass
    elif keyboard.is_pressed(GRABZONE_KEY_UP):
        GRABZONE += 5
        print_banner(bot)
        winsound.Beep(400, 200)
        while keyboard.is_pressed(GRABZONE_KEY_UP):
            pass
    elif keyboard.is_pressed(GRABZONE_KEY_DOWN):
        GRABZONE -= 5
        print_banner(bot)
        winsound.Beep(300, 200)
        while keyboard.is_pressed(GRABZONE_KEY_DOWN):
            pass
    elif keyboard.is_pressed(TRIGGER_KEY):
        bot.toggle()
        print_banner(bot)
        if bot.toggled:
            winsound.Beep(440, 75)
            winsound.Beep(700, 100)
        else:
            winsound.Beep(440, 75)
            winsound.Beep(200, 100)
        while keyboard.is_pressed(TRIGGER_KEY):
            pass
    else:
        for key_combination, new_mode in zip(MODE_KEYS, range(len(MODES))):
            if keyboard.is_pressed(key_combination):
                bot.mode = new_mode
                winsound.Beep(200, 200)
                print_banner(bot)
                while keyboard.is_pressed(key_combination):
                    pass

    if bot.toggled:
        bot.scan()
