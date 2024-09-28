import XInput
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

while True:
    state = XInput.get_state(controller_index)
    buttons = XInput.get_button_values(state)
    for key, value in buttons.items():
        if value: print(key)
