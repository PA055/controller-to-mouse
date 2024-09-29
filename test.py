import win32gui
import mouse
import time

window = win32gui.FindWindow(None, "On-Screen Keyboard")
left, top, right, bottom = win32gui.GetWindowRect(window)
width, height  = right - left, bottom - top

keyboard_map = [
    ([0.03866, 0.107388, 0.168385, 0.235395, 0.297251, 0.358247, 0.421821, 0.481959, 0.548969, 0.610825, 0.67268, 0.74055, 0.802405, 0.867698, 0.945876], 0.2292042), 
    ([0.056701, 0.135739, 0.20189, 0.261168, 0.325601, 0.390893, 0.454467, 0.518041, 0.580756, 0.645189, 0.707904, 0.771478, 0.835052, 0.898625, 0.962199], 0.3705943), 
    ([0.06701, 0.165808, 0.231959, 0.295533, 0.359107, 0.421821, 0.486254, 0.548969, 0.61512, 0.677835, 0.74055, 0.804124, 0.908935], 0.511736), 
    ([0.080756, 0.199313, 0.265464, 0.325601, 0.388316, 0.454467, 0.518041, 0.582474, 0.643471, 0.710481, 0.773196, 0.834192, 0.931271], 0.662329), 
    ([0.037801, 0.103952, 0.165808, 0.232818, 0.44244, 0.643471, 0.705326, 0.769759, 0.832474, 0.898625, 0.962199], 0.811865)
]


for row, y in keyboard_map:
    key_y = top + (y * (height)) + 30
    for x in row:
        key_x = left + (x * (width - 214))
        mouse.move(key_x, key_y)
        time.sleep(0.25)
    key_x = left + width - 171
    mouse.move(key_x, key_y)
    time.sleep(0.25)
    key_x = left + width - 105
    mouse.move(key_x, key_y)
    time.sleep(0.25)
    key_x = left + width - 43
    mouse.move(key_x, key_y)
    time.sleep(0.25)
        
