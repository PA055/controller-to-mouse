from typing import Any
import mouse
import keyboard
import time
import math
import win32gui
import contextlib
import button
from utils import *
from config import config

last = time.time()
dt = .0
mode = 'enabled'

keyboard_open_time = 0.5
keyboard_win: Any = None
mouse_pos = [0, 0]
keyboard_map = [
    ([.03866, .107388, .168385, .235395, .297251, .358247, .421821, .481959, .548969, .610825, .67268, .74055, .802405, .867698, .945876], .2292042), 
    ([.056701, .135739, .20189, .261168, .325601, .390893, .454467, .518041, .580756, .645189, .707904, .771478, .835052, .898625, .962199], .3705943), 
    ([.06701, .165808, .231959, .295533, .359107, .421821, .486254, .548969, .61512, .677835, .74055, .804124, .908935], .511736), 
    ([.080756, .199313, .265464, .325601, .388316, .454467, .518041, .582474, .643471, .710481, .773196, .834192, .931271], .662329), 
    ([.037801, .103952, .165808, .232818, .44244, .643471, .705326, .769759, .832474, .898625, .962199], .811865)
]

def index_to_window(index: tuple[int, int]) -> tuple[float, float]:
    global mode
    try:
        keyboard_win_rect = win32gui.GetWindowRect(keyboard_win)
    except Exception:
        mode = 'enabled'
        return (0, 0)
    width, height = keyboard_win_rect[2] - keyboard_win_rect[0], keyboard_win_rect[3] - keyboard_win_rect[1]
    key_x = keyboard_win_rect[0] + (keyboard_map[index[1]][0][index[0]] * (width - 214))
    key_y = keyboard_win_rect[1] + (keyboard_map[index[1]][1] * (height)) + 30
    return key_x, key_y

def snap_keyboard(pos: tuple[int, int]) -> tuple[int, int]:
    global mode
    try:
        keyboard_win_rect = win32gui.GetWindowRect(keyboard_win)
    except Exception:
        mode = 'enabled'
        return (0, 0)
    width, height = keyboard_win_rect[2] - keyboard_win_rect[0], keyboard_win_rect[3] - keyboard_win_rect[1]
    x_index, y_index = -1, -1
    dist = math.inf
    for i, (row, y) in enumerate(keyboard_map):
        for j, x in enumerate(row):
            key_x = keyboard_win_rect[0] + (x * (width - 214))
            key_y = keyboard_win_rect[1] + (y * (height)) + 30
            if math.hypot(key_x - pos[0], key_y - pos[1]) < dist:
                x_index, y_index = j, i
                dist = math.hypot(key_x - pos[0], key_y - pos[1])
    return x_index, y_index
    
def keyboard_controls():
    global mouse_pos, mode, keyboard_open_time
    try: keyboard_win_rect = win32gui.GetWindowRect(keyboard_win)
    except Exception: mode = 'enabled'; return
    width, height = keyboard_win_rect[2] - keyboard_win_rect[0], keyboard_win_rect[3] - keyboard_win_rect[1]
    joysticks = get_joysticks()
    
    if mouse_pos[0] > keyboard_win_rect[0] and mouse_pos[0] < keyboard_win_rect[2] - 220 and \
       mouse_pos[1] > keyboard_win_rect[1] + 80 and mouse_pos[1] < keyboard_win_rect[3]:
        i_x, i_y = snap_keyboard(mouse_pos)
        key_x, key_y = index_to_window((i_x, i_y))
        mouse_pos = [key_x, key_y]
        
        mouse.move(key_x, key_y)
        
        if button.LEFT_JOYSTICK_UP.get_repeated_new_press() or button.LEFT_JOYSTICK_DOWN.get_repeated_new_press() or \
           button.LEFT_JOYSTICK_LEFT.get_repeated_new_press() or button.LEFT_JOYSTICK_RIGHT.get_repeated_new_press(): 
            mouse_pos[0] += joysticks[0][0] * (width - 214) * (.5 * ((keyboard_map[i_y][0][i_x] - keyboard_map[i_y][0][i_x - 1]) if i_x > 0 else keyboard_map[i_y][0][i_x]) + 0.5 * ((keyboard_map[i_y][0][i_x + 1] - keyboard_map[i_y][0][i_x]) if i_x < len(keyboard_map[i_y][0]) - 1 else keyboard_map[i_y][0][0]))
            mouse_pos[1] -= joysticks[0][1] * 0.9 * keyboard_map[0][1] * height
            mouse.move(*mouse_pos)
        
        for keys, binding in config.get("keyboard_bindings", {}).items():
            if isinstance(binding, dict):
                results = binding.get("result", '')
                trigger = binding.get("trigger", "new_press").lower()
                threshold = float(binding.get("threshold", 0.5)) # TODO make threshold work here
                if trigger in ["long_press", "short_release", "long_release"]:
                    args = (float(config.get("hold_threshold", 0.75)),)
                elif trigger == 'repeat':
                    args = (float(config.get("start_delay", 0.5)), float(config.get("repeat_delay", 0.1)))
                else: args = ()
            else:
                results = binding.lower()
                trigger = "new_press"
                threshold = 0.5
                args = ()
            
            if not isinstance(results, list): results = [results.lower()]
            else: results = [i.lower() for i in results]
            
            for result in results:
                if result in ['\\left_mouse', '\\right_mouse', '\\middle_mouse']:
                    if get_keys_active(keys, "new_press", args): mouse.press(result[1:-6])
                    if get_keys_active(keys, "release", args): mouse.release(result[1:-6])


                if result == '\\up' and get_keys_active(keys, trigger, args):
                    mouse_pos[1] -= 0.9 * keyboard_map[0][1] * height
                    mouse.move(*mouse_pos)
                
                if result == '\\down' and get_keys_active(keys, trigger, args):
                    mouse_pos[1] += 0.9 * keyboard_map[0][1] * height
                    mouse.move(*mouse_pos)
                
                if result == '\\left' and get_keys_active(keys, trigger, args):
                    mouse_pos[0] -= (width - 214) * (.5 * ((keyboard_map[i_y][0][i_x] - keyboard_map[i_y][0][i_x - 1]) if i_x > 0 else keyboard_map[i_y][0][i_x]) + 0.5 * ((keyboard_map[i_y][0][i_x + 1] - keyboard_map[i_y][0][i_x]) if i_x < len(keyboard_map[i_y][0]) - 1 else keyboard_map[i_y][0][0]))
                    mouse.move(*mouse_pos)
                
                if result == '\\right' and get_keys_active(keys, trigger, args):
                    mouse_pos[0] += (width - 214) * (.5 * ((keyboard_map[i_y][0][i_x] - keyboard_map[i_y][0][i_x - 1]) if i_x > 0 else keyboard_map[i_y][0][i_x]) + 0.5 * ((keyboard_map[i_y][0][i_x + 1] - keyboard_map[i_y][0][i_x]) if i_x < len(keyboard_map[i_y][0]) - 1 else keyboard_map[i_y][0][0]))
                    mouse.move(*mouse_pos)
                
                
                if result == '\\shift' and get_keys_active(keys, trigger, args):
                    mouse.move(
                        keyboard_win_rect[0] + (keyboard_map[3][0][0] * (width - 214)),
                        keyboard_win_rect[1] + (keyboard_map[3][1] * (height)) + 30
                    )
                    mouse.click()

                if result == '\\fn' and get_keys_active(keys, trigger, args):
                    mouse.move(
                        keyboard_win_rect[0] + (keyboard_map[4][0][0] * (width - 214)),
                        keyboard_win_rect[1] + (keyboard_map[4][1] * (height)) + 30
                    )
                    mouse.click()

                if result == '\\ctrl' and get_keys_active(keys, trigger, args):
                    mouse.move(
                        keyboard_win_rect[0] + (keyboard_map[4][0][1] * (width - 214)),
                        keyboard_win_rect[1] + (keyboard_map[4][1] * (height)) + 30
                    )
                    mouse.click()

                if result == '\\win' and get_keys_active(keys, trigger, args):
                    mouse.move(
                        keyboard_win_rect[0] + (keyboard_map[4][0][2] * (width - 214)),
                        keyboard_win_rect[1] + (keyboard_map[4][1] * (height)) + 30
                    )
                    mouse.click()

                if result == '\\alt' and get_keys_active(keys, trigger, args):
                    mouse.move(
                        keyboard_win_rect[0] + (keyboard_map[4][0][3] * (width - 214)),
                        keyboard_win_rect[1] + (keyboard_map[4][1] * (height)) + 30
                    )
                    mouse.click()


                if result == '\\keyboard_toggle' and get_keys_active(keys, trigger, args):
                    keyboard.send('ctrl+win+o')
                    keyboard_open_time = 0.5
                    mode = 'enabled' if mode == 'keyboard' else 'keyboard'
                    
                if result == '\\keyboard_enable' and mode == 'enabled' and get_keys_active(keys, trigger, args):
                    keyboard.send('ctrl+win+o')
                    keyboard_open_time = 0.5
                    mode = 'keyboard'
                
                if result == '\\keyboard_disable' and mode == 'keyboard' and get_keys_active(keys, trigger, args):
                    keyboard.send('ctrl+win+o')
                    keyboard_open_time = 0.5
                    mode = 'enable'
                    
                if get_keys_active(keys, trigger, args):
                    parse_result(result)
            
    else:
        normal_keybinds()
        if mouse.get_position()[0] > keyboard_win_rect[0] and \
           mouse.get_position()[0] < keyboard_win_rect[2] - 220 and \
           mouse.get_position()[1] > keyboard_win_rect[1] + 80 and \
           mouse.get_position()[1] < keyboard_win_rect[3]:
            mouse_pos = list(mouse.get_position())

def get_keys_active(keys: str, function: str = 'new_press', args: tuple = ()) -> bool:
    if function == 'new_press':
        return all(
            button.buttons[btn.strip().upper()].get_pressed() or 
            button.buttons[btn.strip().upper()].get_new_press() 
            for btn in keys.split('+')
        ) and any(
            button.buttons[btn.strip().upper()].get_new_press() 
            for btn in keys.split('+')
        ) 
    if function == 'pressed':
        return all(button.buttons[btn.strip().upper()].get_pressed() for btn in keys.split('+'))
    if function == 'new_long_press':
        return any(
            button.buttons[btn.strip().upper()].get_new_long_press(*args) 
            for btn in keys.split('+')
        ) and all(
            button.buttons[btn.strip().upper()].get_new_long_press(*args) or \
            button.buttons[btn.strip().upper()].get_long_pressed(*args) 
            for btn in keys.split('+')
        )
    if function == 'long_press':
        return all(button.buttons[btn.strip().upper()].get_long_pressed(*args) for btn in keys.split('+'))


    if function == 'release':
        return all(
            button.buttons[btn.strip().upper()].get_pressed() or 
            button.buttons[btn.strip().upper()].get_release() 
            for btn in keys.split('+')
        ) and any(
            button.buttons[btn.strip().upper()].get_release() 
            for btn in keys.split('+')
        )
    if function == 'short_release':
        return all(
            button.buttons[btn.strip().upper()].get_short_release(*args) or (
                button.buttons[btn.strip().upper()].get_pressed() and 
                not button.buttons[btn.strip().upper()].get_long_pressed(*args)
            ) 
            for btn in keys.split('+')
        ) and any(
            button.buttons[btn.strip().upper()].get_short_release(*args) 
            for btn in keys.split('+') 
        )
    if function == 'long_release':
        return all (
            button.buttons[btn.strip().upper()].get_long_release(*args) or 
            button.buttons[btn.strip().upper()].get_long_pressed(*args)
            for btn in keys.split('+')
        ) and any(
            button.buttons[btn.strip().upper()].get_long_release(*args)
            for btn in keys.split('+')
        )
    
    if function == 'repeat':
        return button.buttons[keys.split('+')[0].strip().upper()].get_repeated_new_press(*args) and \
               all(button.buttons[btn.strip().upper()].get_pressed() for btn in keys.split('+'))
    return False

def parse_result(result):
    if result[0] == '\\':
        if result == '\\right_click': mouse.click('right')
        if result == '\\right_press': mouse.press('right')
        if result == '\\right_release': mouse.release('right')
        
        if result == '\\middle_click': mouse.click('middle')
        if result == '\\middle_press': mouse.press('middle')
        if result == '\\middle_release': mouse.release('middle')
        
        if result == '\\left_click': mouse.click('left')
        if result == '\\left_press': mouse.press('left')
        if result == '\\left_release': mouse.release('left')
        
        if result.startswith('\\type '): keyboard.write(result[6:])
        
    else:
        keyboard.send(result)

def normal_keybinds():
    global mode, keyboard_open_time, mouse_pos
    joysticks = get_joysticks()
    moveJoystick = joysticks[0 if config.get("mouse_joystick", 'left').lower() == "left" else 1]
    scrollJoystick = joysticks[0 if config.get("scroll_joystick", 'right').lower() == "left" else 1]
    
    mouse.move(
        moveJoystick[0] * config.get("mouse_sensitivity", 20), 
        moveJoystick[1] * -config.get("mouse_sensitivity", 20), 
        absolute=False, duration=.01
    )
    mouse.wheel(scrollJoystick[1] * config.get("scroll_sensitivity", 10))
    if joysticks[1][0] != 0:
        keyboard.press("shift")
        mouse.wheel(-scrollJoystick[0] * config.get("scroll_sensitivity", 10))
        keyboard.release("shift")

    for keys, binding in config.get("bindings", {}).items():
        if isinstance(binding, dict):
            results = binding.get("result", '')
            trigger = binding.get("trigger", "new_press").lower()
            threshold = float(binding.get("threshold", 0.5)) # TODO make threshold work here
            if trigger.lower() in ["long_press", "new_long_press", "short_release", "long_release"]: # TODO add new long press
                args = (float(config.get("hold_threshold", 0.5)),)
            elif trigger.lower() == 'repeat':
                args = (float(config.get("start_delay", 0.5)), float(config.get("repeat_delay", 0.1)))
            else: args = ()
        else:
            results = binding.lower()
            trigger = "new_press"
            threshold = 0.5
            args = ()
        
        if not isinstance(results, list): results = [results.lower()]
        else: results = [i.lower() for i in results]
        
        for result in results:
            if result in ['\\left_mouse', '\\right_mouse', '\\middle_mouse']:
                if get_keys_active(keys, "new_press", args): mouse.press(result[1:-6])
                if get_keys_active(keys, "release", args): mouse.release(result[1:-6])
                
            if trigger == 'hold':
                if get_keys_active(keys, "new_press", args): keyboard.press(result)
                if get_keys_active(keys, "release", args): keyboard.release(result)
                
            if result == '\\keyboard_toggle' and get_keys_active(keys, trigger, args):
                keyboard.send('ctrl+win+o')
                keyboard_open_time = 0.5
                mouse_pos = list(index_to_window(snap_keyboard(mouse.get_position())))
                mode = 'enabled' if mode == 'keyboard' else 'keyboard'
                
            if result == '\\keyboard_enable' and mode == 'enabled' and get_keys_active(keys, trigger, args):
                keyboard.send('ctrl+win+o')
                keyboard_open_time = 0.5
                mouse_pos = list(index_to_window(snap_keyboard(mouse.get_position())))
                mode = 'keyboard'
            
            if result == '\\keyboard_disable' and mode == 'keyboard' and get_keys_active(keys, trigger, args):
                keyboard.send('ctrl+win+o')
                mode = 'enable'
                
            if get_keys_active(keys, trigger, args):
                parse_result(result)
   
def controller_loop():
    global last, dt, mode, keyboard_open_time, keyboard_win
    button.update_all()
    if mode == 'enabled':
        normal_keybinds()

    if mode == 'keyboard' and keyboard_open_time > 0:
        keyboard_open_time -= dt
        if keyboard_open_time < 0:
            with contextlib.suppress(Exception):
                keyboard_win = win32gui.FindWindow(None, "On-Screen Keyboard")
        
    if mode == 'keyboard' and keyboard_open_time < 0:
        keyboard_controls()
    
    if mode == 'disabled' and get_keys_active(config.get("enable_binding"), "new_press"):
        mode = 'enabled'
    
    elif mode != 'disabled' and get_keys_active(config.get("disable_binding"), "new_press"):
        if mode == 'keyboard': keyboard.send('ctrl+win+o')
        mode = 'disabled'

    dt = time.time() - last
    last = time.time()

if __name__ == "__main__":
    try:
        while True:
            controller_loop()
    except KeyboardInterrupt:
        print("Exiting...")
    finally:
        keyboard.release("shift")
        mouse.release('left')
        # mouse.release('right')
    