import XInput
import mouse
import keyboard
import time
 
sensitivity = 20
keyboard_map = [
    [0.051] * 13 + [0.096, 0.061, 0.061, 0.065],
    [0.077] + [0.051] * 13 + [0.063, 0.061, 0.061, 0.065],
    [0.103]
]

def get_joysticks() -> tuple[tuple[float, float], tuple[float, float]]:
    if controller_index >= 0:
        return XInput.get_thumb_values(XInput.get_state(controller_index))
    
    x_axis = keyboard.is_pressed("right") - keyboard.is_pressed("left")
    y_axis = keyboard.is_pressed("up") - keyboard.is_pressed("down")
    return (x_axis, y_axis), (0, 0)

def get_buttons() -> dict[str, bool]:
    if controller_index >= 0: 
        return XInput.get_button_values(XInput.get_state(controller_index))
    
    return {
        "DPAD_UP": keyboard.is_pressed('w'),
        "DPAD_LEFT": keyboard.is_pressed('a'),
        "DPAD_DOWN": keyboard.is_pressed('s'),
        "DPAD_RIGHT": keyboard.is_pressed('d'),
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
dt = 0.0
disabled = False
while True:
    buttons = get_buttons()
    LT, RT = get_triggers()
    (LX, LY), (RX, RY) = get_joysticks()
    if not disabled:
        mouse.move(LX * sensitivity, LY * -sensitivity, absolute=False, duration=0.01)
        if RY != 0:
            mouse.wheel(RY)
        if RX != 0:
            keyboard.press("SHIFT")
            mouse.wheel(-RX)
        keyboard.release("SHIFT")
        if (not (last_buttons["DPAD_DOWN"] and last_buttons["LEFT_SHOULDER"])) and buttons["DPAD_DOWN"] and buttons["LEFT_SHOULDER"]:
            keyboard.send('ctrl+win+o')
        
        if LT > .3: mouse.click(button = 'right')
        if RT > .3: mouse.click(button = 'left')
        
    if buttons["START"] and buttons["LEFT_SHOULDER"] and not (last_buttons["START"] and last_buttons["LEFT_SHOULDER"]):
        disabled = not disabled
    
    dt = time.time() - last
    last = time.time()
    last_buttons = buttons
        