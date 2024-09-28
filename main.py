import XInput
import pyautogui
import time

controller_index = -1
print("checking for connected controllers...")

for _ in range(50):
    if any(XInput.get_connected()): break
    time.sleep(0.1)
if not any(XInput.get_connected()): 
    print("Failed to connect, try again later")
    exit(1)
controller_index = XInput.get_connected().index(True)

last = time.time()
last_buttons = {"DPAD_DOWN": False}
dt = 0.0
while True:
    state = XInput.get_state(controller_index)
    buttons = XInput.get_button_values(state)
    (LX, LY), _ = XInput.get_thumb_values(state)
    pyautogui.move(LX * 50, LY * -50)
    if (not last_buttons["DPAD_DOWN"]) and buttons["DPAD_DOWN"]:
        print('test')
        pyautogui.hotkey('ctrl','win','o')

    dt = time.time() - last
    last = time.time()    
    last_buttons = buttons
    