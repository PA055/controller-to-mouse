import XInput
import mouse
import keyboard
import time
import win32gui
 
sensitivity = 20
keyboard_map = [
    ([.03866, .107388, .168385, .235395, .297251, .358247, .421821, .481959, .548969, .610825, .67268, .74055, .802405, .867698, .945876], .2292042), 
    ([.056701, .135739, .20189, .261168, .325601, .390893, .454467, .518041, .580756, .645189, .707904, .771478, .835052, .898625, .962199], .3705943), 
    ([.06701, .165808, .231959, .295533, .359107, .421821, .486254, .548969, .61512, .677835, .74055, .804124, .908935], .511736), 
    ([.080756, .199313, .265464, .325601, .388316, .454467, .518041, .582474, .643471, .710481, .773196, .834192, .931271], .662329), 
    ([.037801, .103952, .165808, .232818, .44244, .643471, .705326, .769759, .832474, .898625, .962199], .811865)
]

def get_joysticks() -> tuple[tuple[float, float], tuple[float, float]]:
    if controller_index >= 0:
        return XInput.get_thumb_values(XInput.get_state(controller_index))
    
    lx_axis = keyboard.is_pressed("right") - keyboard.is_pressed("left")
    ly_axis = keyboard.is_pressed("up") - keyboard.is_pressed("down")
    rx_axis = keyboard.is_pressed("d") - keyboard.is_pressed("a")
    ry_axis = keyboard.is_pressed("w") - keyboard.is_pressed("s")
    return (lx_axis, ly_axis), (rx_axis, ry_axis)

def get_buttons() -> dict[str, bool]:
    if controller_index >= 0: 
        return XInput.get_button_values(XInput.get_state(controller_index))
    
    return {
        "DPAD_UP": keyboard.is_pressed('t'),
        "DPAD_LEFT": keyboard.is_pressed('f'),
        "DPAD_DOWN": keyboard.is_pressed('g'),
        "DPAD_RIGHT": keyboard.is_pressed('h'),
        "START": keyboard.is_pressed('='),
        "BACK": keyboard.is_pressed('-'),
        "LEFT_THUMB": keyboard.is_pressed('/'),
        "RIGHT_THUMB": keyboard.is_pressed('.'),
        "LEFT_SHOULDER": keyboard.is_pressed('q'),
        "RIGHT_SHOULDER": keyboard.is_pressed('e'),
        "A": keyboard.is_pressed('k'),
        "B": keyboard.is_pressed('l'),
        "X": keyboard.is_pressed('j'),
        "Y": keyboard.is_pressed('i')
    }

def get_triggers() -> tuple[float, float]:
    if controller_index >= 0: return XInput.get_trigger_values(XInput.get_state(controller_index))
    return 1 if keyboard.is_pressed('x') else 0, 1 if keyboard.is_pressed('c') else 0

import contextlib
controller_index = -1
print("Checking for connected controllers...")

for _ in range(50):
    if any(XInput.get_connected()): break
    time.sleep(.1)
if not any(XInput.get_connected()): 
    print("Failed to connect, try again later")
    # exit(1)
else:
    print("Connected.")
    controller_index = XInput.get_connected().index(True)

last = time.time()
last_buttons = {key: False for key in get_buttons()}
last_triggers = (.0, .0)
dt = .0
mode = 'enabled'

keyboard_open_time = 0.5
keyboard_win = None
keyboard_win_rect = (.0, .0, .0, .0)
keyboard_index = (0, 0)

while True:
    buttons = get_buttons()
    LT, RT = get_triggers()
    (LX, LY), (RX, RY) = get_joysticks()
    if mode == 'enabled':
        mouse.move(LX * sensitivity, LY * -sensitivity, absolute=False, duration=.01)
        if RY != 0: mouse.wheel(RY)
        if RX != 0:
            keyboard.press("SHIFT")
            mouse.wheel(-RX)
            keyboard.release("SHIFT")

    if mode == 'keyboard' and keyboard_open_time > 0:
        keyboard_open_time -= dt
        if keyboard_open_time < 0:
            with contextlib.suppress(Exception):
                keyboard_win = win32gui.FindWindow(None, "On-Screen Keyboard")
                keyboard_win_rect = win32gui.GetWindowRect(keyboard_win)
        
    if mode == 'keyboard' and keyboard_open_time < 0:
        width, height  = keyboard_win_rect[2] - keyboard_win_rect[0], keyboard_win_rect[3] - keyboard_win_rect[1]
        key_x = keyboard_win_rect[0] + (keyboard_map[keyboard_index[1]][0][keyboard_index[0]] * (width - 214))
        key_y = keyboard_win_rect[1] + (keyboard_map[keyboard_index[1]][1] * (height)) + 30
        mouse.move(key_x, key_y)
         
    if mode != 'disabled':
        if (not (last_buttons["DPAD_DOWN"] and last_buttons["LEFT_SHOULDER"])) and buttons["DPAD_DOWN"] and buttons["LEFT_SHOULDER"]:
            keyboard.send('ctrl+win+o')
            keyboard_open_time = 0.5
            mode = 'enabled' if mode == 'keyboard' else 'keyboard'

        if LT >= .3 and last_triggers[0] < .3: mouse.press('right')
        if LT <= .3 and last_triggers[0] > .3: mouse.release('right')

        if RT >= .3 and last_triggers[1] < .3: mouse.press('left')
        if RT <= .3 and last_triggers[1] > .3: mouse.release('left')

    if buttons["START"] and buttons["LEFT_SHOULDER"] and not (last_buttons["START"] and last_buttons["LEFT_SHOULDER"]):
        mode = 'enabled' if mode == 'disabled' else 'disabled'

    dt = time.time() - last
    last = time.time()
    last_buttons = buttons
    last_triggers = (LT, RT)
        