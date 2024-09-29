import XInput
import mouse
import keyboard
import time
import win32gui
import contextlib
import button
from utils import *

last = time.time()
dt = .0
mode = 'enabled'

keyboard_open_time = 0.5
keyboard_win_rect = (.0, .0, .0, .0)
keyboard_index = [0, 0]


sensitivity = 20
keyboard_map = [
    ([.03866, .107388, .168385, .235395, .297251, .358247, .421821, .481959, .548969, .610825, .67268, .74055, .802405, .867698, .945876], .2292042), 
    ([.056701, .135739, .20189, .261168, .325601, .390893, .454467, .518041, .580756, .645189, .707904, .771478, .835052, .898625, .962199], .3705943), 
    ([.06701, .165808, .231959, .295533, .359107, .421821, .486254, .548969, .61512, .677835, .74055, .804124, .908935], .511736), 
    ([.080756, .199313, .265464, .325601, .388316, .454467, .518041, .582474, .643471, .710481, .773196, .834192, .931271], .662329), 
    ([.037801, .103952, .165808, .232818, .44244, .643471, .705326, .769759, .832474, .898625, .962199], .811865)
]

    
def keyboard_controls():
    global keyboard_index
    keyboard_win_rect = win32gui.GetWindowRect(keyboard_win)
    if keyboard_index[1] >= 0 and keyboard_index[1] < len(keyboard_map) and \
        keyboard_index[0] >= 0 and keyboard_index[0] < len(keyboard_map[keyboard_index[1]][0]):
            width, height = keyboard_win_rect[2] - keyboard_win_rect[0], keyboard_win_rect[3] - keyboard_win_rect[1]
            key_x = keyboard_win_rect[0] + (keyboard_map[keyboard_index[1]][0][keyboard_index[0]] * (width - 214))
            key_y = keyboard_win_rect[1] + (keyboard_map[keyboard_index[1]][1] * (height)) + 30
            
            mouse.move(key_x, key_y)
            if button.A.get_new_press(): mouse.click()
            
            if button.LEFT_JOYSTICK_UP.get_repeated_new_press(): 
                keyboard_index[1] -= 1
                mouse.move(key_x, keyboard_win_rect[1] + 60)
                
            if button.LEFT_JOYSTICK_DOWN.get_repeated_new_press(): 
                keyboard_index[1] += 1
                mouse.move(key_x, keyboard_win_rect[3] + 20)
                
            if button.LEFT_JOYSTICK_LEFT.get_repeated_new_press(): 
                keyboard_index[0] -= 1
                mouse.move(keyboard_win_rect[0] - 20, key_y)
                
            if button.LEFT_JOYSTICK_RIGHT.get_repeated_new_press(): 
                keyboard_index[0] += 1
                mouse.move(keyboard_win_rect[2] - 200, key_y)
            
            if button.B.get_new_press():
                mouse.move(
                    keyboard_win_rect[0] + (keyboard_map[0][0][14] * (width - 214)),
                    keyboard_win_rect[1] + (keyboard_map[0][1] * (height)) + 30
                )
                mouse.click()
            
            if button.Y.get_new_press():
                mouse.move(
                    keyboard_win_rect[0] + (keyboard_map[4][0][4] * (width - 214)),
                    keyboard_win_rect[1] + (keyboard_map[4][1] * (height)) + 30
                )
                mouse.click()
            
            if button.X.get_new_press():
                mouse.move(
                    keyboard_win_rect[0] + (keyboard_map[3][0][0] * (width - 214)),
                    keyboard_win_rect[1] + (keyboard_map[3][1] * (height)) + 30
                )
                mouse.click()
                
            if button.UP.get_repeated_new_press() or button.RIGHT_JOYSTICK_UP.get_repeated_new_press():
                mouse.move(
                    keyboard_win_rect[0] + (keyboard_map[3][0][11] * (width - 214)),
                    keyboard_win_rect[1] + (keyboard_map[3][1] * (height)) + 30
                )
                mouse.click()
                
            if button.LEFT.get_repeated_new_press() or button.RIGHT_JOYSTICK_LEFT.get_repeated_new_press():
                mouse.move(
                    keyboard_win_rect[0] + (keyboard_map[4][0][7] * (width - 214)),
                    keyboard_win_rect[1] + (keyboard_map[4][1] * (height)) + 30
                )
                mouse.click()
                
            if button.DOWN.get_repeated_new_press() or button.RIGHT_JOYSTICK_DOWN.get_repeated_new_press():
                mouse.move(
                    keyboard_win_rect[0] + (keyboard_map[4][0][8] * (width - 214)),
                    keyboard_win_rect[1] + (keyboard_map[4][1] * (height)) + 30
                )
                mouse.click()
                
            if button.RIGHT.get_repeated_new_press() or button.RIGHT_JOYSTICK_RIGHT.get_repeated_new_press():
                mouse.move(
                    keyboard_win_rect[0] + (keyboard_map[4][0][9] * (width - 214)),
                    keyboard_win_rect[1] + (keyboard_map[4][1] * (height)) + 30
                )
                mouse.click()
            
    else:
        joysticks = get_joysticks()
        mouse.move(joysticks[0][0] * sensitivity, joysticks[0][1] * -sensitivity, absolute=False, duration=.01)
        mouse.wheel(joysticks[1][1])
        if joysticks[1][0] != 0:
            keyboard.press("shift")
            mouse.wheel(-joysticks[1][0])
            keyboard.release("shift")
        print(mouse.get_position())
        print(keyboard_win_rect)
        if mouse.get_position()[0] > keyboard_win_rect[0] and \
           mouse.get_position()[0] < keyboard_win_rect[2] - 220 and \
           mouse.get_position()[1] > keyboard_win_rect[1] + 80 and \
           mouse.get_position()[1] < keyboard_win_rect[3]:
            keyboard_index[1] = max(0, min(len(keyboard_map) - 1, keyboard_index[1]))
            keyboard_index[0] = max(0, min(len(keyboard_map[keyboard_index[1]][0]) - 1, keyboard_index[0]))
                
def controller_loop():
    global last, dt, mode, keyboard_open_time, keyboard_win
    button.update_all()
    joysticks = get_joysticks()
    if mode == 'enabled':
        mouse.move(joysticks[0][0] * sensitivity, joysticks[0][1] * -sensitivity, absolute=False, duration=.01)
        mouse.wheel(joysticks[1][1])
        if joysticks[1][0] != 0:
            keyboard.press("shift")
            mouse.wheel(-joysticks[1][0])
            keyboard.release("shift")

    if mode == 'keyboard' and keyboard_open_time > 0:
        keyboard_open_time -= dt
        if keyboard_open_time < 0:
            with contextlib.suppress(Exception):
                keyboard_win = win32gui.FindWindow(None, "On-Screen Keyboard")
        
    if mode == 'keyboard' and keyboard_open_time < 0:
        keyboard_controls()
    
    if mode != 'disabled':
        if button.L1.pressed and button.DOWN.rising_edge or button.L1.rising_edge and button.DOWN.pressed:
            keyboard.send('ctrl+win+o')
            keyboard_open_time = 0.5
            mode = 'enabled' if mode == 'keyboard' else 'keyboard'

        if button.L2.rising_edge: mouse.press('right')
        if button.L2.falling_edge: mouse.release('right')

        if button.R2.rising_edge: mouse.press('left')
        if button.R2.falling_edge: mouse.release('left')

    if button.L1.pressed and button.START.rising_edge or button.L1.rising_edge and button.START.pressed:
        mode = 'enabled' if mode == 'disabled' else 'disabled'

    dt = time.time() - last
    last = time.time()

if __name__ == "__main__":
    print("Checking for connected controllers...")
    if not any(XInput.get_connected()): 
        print("Failed to connect, try again later")
        exit(1)
    else:
        print("Connected.")

    try:
        while True:
            controller_loop()
    except KeyboardInterrupt:
        print("Exiting...")
    finally:
        keyboard.release("shift")
        mouse.release('left')
        mouse.release('right')
    