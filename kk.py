import keyboard
import pyautogui
import time
import ctypes
import PIL.ImageGrab
import PIL.Image
import winsound
import os
import mss
from colorama import Fore, Style, init

S_HEIGHT, S_WIDTH = (PIL.ImageGrab.grab().size)
PURPLE_R, PURPLE_G, PURPLE_B = (250, 100, 250)
TOLERANCE = 31
GRABZONE = 10
TRIGGER_KEY = "f12"
SWITCH_KEY = "ctrl + tab"
GRABZONE_KEY_UP = "ctrl + up"
GRABZONE_KEY_DOWN = "ctrl + down"
mods = ["SHERIFF", "SPECTRE", "GUARDIAN/SHOTGUN", "VANDAL/PHANTOM", "MARSHAL FASTSCOPE", "OPERATOR FASTSCOPE", "MARSHAL/OPERATOR SCOPE", "ODIN"]

# Mapping of key combinations to mode values
mode_key_map = {
    "f1": 0,
    "f2": 1,
    "f3": 2,
    "f4": 3,
    "f5": 4,
    "f6": 5,
    "f7": 6,
    "f8": 7

}

pyautogui.FAILSAFE = False

class FoundEnemy(Exception):
    pass

class triggerBot():
    def __init__(self) -> None:
        self.toggled = False
        self.mode = 0
        self.last_reac = 0

    def toggle(self) -> None:
        self.toggled = not self.toggled

    def switch(self):
        if self.mode != 6:
            self.mode += 1
        else:
            self.mode = 0

    def click(self) -> None:
        if self.mode == 0:
            keyboard.press('w+a+s+d')
            time.sleep(0.09)
            ctypes.windll.user32.mouse_event(2, 0, 0, 0, 0)
            ctypes.windll.user32.mouse_event(4, 0, 0, 0, 0)
            keyboard.release('w+a+s+d')
        elif self.mode == 1:
            keyboard.press('w+a+s+d')
            time.sleep(0.025)
            ctypes.windll.user32.mouse_event(2, 0, 0, 0, 0)
            time.sleep(0.3)
            ctypes.windll.user32.mouse_event(4, 0, 0, 0, 0)
            keyboard.release('w+a+s+d')
        elif self.mode == 2:
            keyboard.press('w+a+s+d')
            time.sleep(0.0995)
            ctypes.windll.user32.mouse_event(2, 0, 0, 0, 0)
            ctypes.windll.user32.mouse_event(4, 0, 0, 0, 0)
            keyboard.release('w+a+s+d')
        elif self.mode == 3:
            keyboard.press('w+a+s+d')
            time.sleep(0.07)
            ctypes.windll.user32.mouse_event(2, 0, 0, 0, 0)
            ctypes.windll.user32.mouse_event(4, 0, 0, 0, 0)
            keyboard.release('w+a+s+d')
        elif self.mode == 4:
            keyboard.press('w+a+s+d')
            time.sleep(0.0995)
            ctypes.windll.user32.mouse_event(0x0008, 0, 0, 0, 0)
            time.sleep(0.18)
            ctypes.windll.user32.mouse_event(2, 0, 0, 0, 0)
            ctypes.windll.user32.mouse_event(4, 0, 0, 0, 0)
            ctypes.windll.user32.mouse_event(0x0010, 0, 0, 0, 0)
            keyboard.release('w+a+s+d')
        elif self.mode == 5:
            keyboard.press('w+a+s+d')
            time.sleep(0.0995)
            ctypes.windll.user32.mouse_event(0x0008, 0, 0, 0, 0)
            time.sleep(0.22)
            ctypes.windll.user32.mouse_event(2, 0, 0, 0, 0)
            ctypes.windll.user32.mouse_event(4, 0, 0, 0, 0)
            ctypes.windll.user32.mouse_event(0x0010, 0, 0, 0, 0)
            keyboard.release('w+a+s+d')
        elif self.mode == 6:
            keyboard.press('w+a+s+d')
            ctypes.windll.user32.mouse_event(2, 0, 0, 0, 0)
            ctypes.windll.user32.mouse_event(4, 0, 0, 0, 0)
            keyboard.release('w+a+s+d')
        else:
            self.ctrl_pressed = False 
            self.shooting = False  

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

    def approx(self, r, g, b) -> bool:
        return PURPLE_R - TOLERANCE < r < PURPLE_R + TOLERANCE and PURPLE_G - TOLERANCE < g < PURPLE_G + TOLERANCE and PURPLE_B - TOLERANCE < b < PURPLE_B + TOLERANCE

    def grab(self) -> None:
        with mss.mss() as sct:
            bbox = (int(S_HEIGHT/2-GRABZONE), int(S_WIDTH/2-GRABZONE), int(S_HEIGHT/2+GRABZONE), int(S_WIDTH/2+GRABZONE))
            sct_img = sct.grab(bbox)
            return PIL.Image.frombytes('RGB', sct_img.size, sct_img.bgra, 'raw', 'BGRX')

    def scan(self) -> None:
        start_time = time.time()
        pmap = self.grab()
        
        try:
            for x in range(0, GRABZONE*2):
                for y in range(0, GRABZONE*2):
                    r, g, b = pmap.getpixel((x, y))
                    if self.approx(r, g, b):
                        raise FoundEnemy
        except FoundEnemy:
            self.last_reac = int((time.time() - start_time) * 1000)
            self.click()
            if self.mode == 0:
                time.sleep(0.5)
            elif self.mode == 1:
                time.sleep(0.15)
            elif self.mode == 2:
                time.sleep(0.17)
            elif self.mode == 3:
                time.sleep(0.1)
            elif self.mode == 4:
                time.sleep(0.5)
            elif self.mode == 5:
                time.sleep(0.6)
            elif self.mode == 6:
                time.sleep(0.5)
            print_banner(self)

def print_banner(bot: triggerBot) -> None:
    os.system("cls")
    print(Style.BRIGHT + Fore.CYAN + "thienkhoilewlew" + Style.RESET_ALL)
    print("===== Controls =====")
    print("Bật     :", Fore.YELLOW + TRIGGER_KEY + Style.RESET_ALL)
    print("Đổi súng: f(1 - 8) ", Fore.YELLOW  + Style.RESET_ALL)
    print("Range   :", Fore.YELLOW + GRABZONE_KEY_UP + "/" + GRABZONE_KEY_DOWN + Style.RESET_ALL)
    print("====================")
    print("Súng    :", Fore.CYAN + mods[bot.mode] + Style.RESET_ALL)
    print("Range   :", Fore.CYAN + str(GRABZONE) + "x" + str(GRABZONE) + Style.RESET_ALL)
    print("Auto bắn:", (Fore.GREEN if bot.toggled else Fore.RED) + ("Bật" if bot.toggled else "Tắt") + Style.RESET_ALL)
    print("Độ trễ  :", Fore.CYAN + str(bot.last_reac) + Style.RESET_ALL + " ms (" + str((bot.last_reac) / (GRABZONE * GRABZONE)) + "ms/pix)")

if __name__ == "__main__":
    bot = triggerBot()
    print_banner(bot)
    while True:
        if keyboard.is_pressed(SWITCH_KEY):
            bot.switch()
            winsound.Beep(200, 200)
            print_banner(bot)
            while keyboard.is_pressed(SWITCH_KEY):
                pass
        if keyboard.is_pressed(GRABZONE_KEY_UP):
            GRABZONE += 5
            print_banner(bot)
            winsound.Beep(400, 200)
            while keyboard.is_pressed(GRABZONE_KEY_UP):
                pass
        if keyboard.is_pressed(GRABZONE_KEY_DOWN):
            GRABZONE -= 5
            print_banner(bot)
            winsound.Beep(300, 200)
            while keyboard.is_pressed(GRABZONE_KEY_DOWN):
                pass
        if keyboard.is_pressed(TRIGGER_KEY):
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

        # Listen for mode change key combinations
        for key_combination, new_mode in mode_key_map.items():
            if keyboard.is_pressed(key_combination):
                bot.mode = new_mode
                winsound.Beep(200, 200)
                print_banner(bot)
                while keyboard.is_pressed(key_combination):
                    pass

        if bot.toggled:
            bot.scan()