import XInput
import mouse
import keyboard
import time
 
sensitivity = 20
key_height = 0.165
keyboard_map = [
    [0.051] * 13 + [0.096, 0.061, 0.065, 0.061],
    [0.077] + [0.051] * 13 + [0.070, 0.061, 0.065, 0.061],
    [0.103] + [0.051] * 11 + [0.146, 0.061, 0.065, 0.061],
    [0.129] + [0.051] * 11 + [0.120, 0.061, 0.065, 0.061],
    [0.051] * 3 + [0.284] + [0.051] * 5 + [0.067, 0.061, 0.065, 0.061],
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

controller_index = -1
print("Checking for connected controllers...")

for _ in range(50):
    if any(XInput.get_connected()): break
    time.sleep(0.1)
if not any(XInput.get_connected()): 
    print("Failed to connect, try again later")
    # exit(1)
else:
    print("Connected.")
    controller_index = XInput.get_connected().index(True)

last = time.time()
last_buttons = {key: False for key in get_buttons()}
last_triggers = (0.0, 0.0)
dt = 0.0
mode = 'enabled'
keyboard_open = False
while True:
    buttons = get_buttons()
    LT, RT = get_triggers()
    (LX, LY), (RX, RY) = get_joysticks()
    if mode == 'enabled':
        mouse.move(LX * sensitivity, LY * -sensitivity, absolute=False, duration=0.01)
        if RY != 0: mouse.wheel(RY)
        if RX != 0:
            keyboard.press("SHIFT")
            mouse.wheel(-RX)
            keyboard.release("SHIFT")
        
    if mode == 'keyboard' and not keyboard_open:
        pass

    if mode != 'disabled':
        if (not (last_buttons["DPAD_DOWN"] and last_buttons["LEFT_SHOULDER"])) and buttons["DPAD_DOWN"] and buttons["LEFT_SHOULDER"]:
            keyboard.send('ctrl+win+o')
            keyboard_open = False
            mode = 'enabled' if mode == 'keyboard' else 'keyboard'
        
        if LT > .3 and last_triggers[0] < .3: 
            mouse.press('right')
        if LT < .3 and last_triggers[0] > .3:
            mouse.release('right')
            
        if RT > .3 and last_triggers[1] < .3:
            mouse.press('left')
        if RT < .3 and last_triggers[1] > .3:
            mouse.release('left')
        
    if buttons["START"] and buttons["LEFT_SHOULDER"] and not (last_buttons["START"] and last_buttons["LEFT_SHOULDER"]):
        mode = 'enabled' if mode == 'disabled' else 'disabled'
    
    dt = time.time() - last
    last = time.time()
    last_buttons = buttons
    last_triggers = (LT, RT)
        