import XInput, keyboard
print("Checking for connected controllers...")
if not any(XInput.get_connected()):
    controller_index = -1
    print("Failed to connect, try again later")
else: 
    controller_index = XInput.get_connected().index(True)
    print("Connected.")

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
