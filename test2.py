import win32gui
import mouse
import keyboard

window = win32gui.FindWindow(None, "On-Screen Keyboard")
left, top, right, bottom = win32gui.GetWindowRect(window)
width, height  = right - left, bottom - top

keyboard_map = []
y_avg = 0.0
x_pos: list[float] = []
while True:
    keyboard.read_key()
    if (keyboard.is_pressed('enter')):
        keyboard_map.append((x_pos[:], y_avg))
        y_avg = 0
        x_pos = []
        print(f"line: {y_avg}\n")
    if keyboard.is_pressed('space'):
        x, y = round((mouse.get_position()[0] - left) / (width - 214), 6), round((mouse.get_position()[1] - top - 30) / height, 6)
        y_avg = (y_avg * len(x_pos) + y) / (len(x_pos) + 1)
        x_pos.append(x)
        print(x, y)
    if keyboard.is_pressed('escape'):
        keyboard_map.append((x_pos[:], y_avg))
        break
print(keyboard_map)


keyboard_map = [
    ([0.03866, 0.107388, 0.168385, 0.235395, 0.297251, 0.358247, 0.421821, 0.481959, 0.548969, 0.610825, 0.67268, 0.74055, 0.802405, 0.867698, 0.945876], 0.22920420000000005), 
    ([0.056701, 0.135739, 0.20189, 0.261168, 0.325601, 0.390893, 0.454467, 0.518041, 0.580756, 0.645189, 0.707904, 0.771478, 0.835052, 0.898625, 0.962199], 0.37059426666666667), 
    ([0.06701, 0.165808, 0.231959, 0.295533, 0.359107, 0.421821, 0.486254, 0.548969, 0.61512, 0.677835, 0.74055, 0.804124, 0.908935], 0.5117359999999999), 
    ([0.080756, 0.199313, 0.265464, 0.325601, 0.388316, 0.454467, 0.518041, 0.582474, 0.643471, 0.710481, 0.773196, 0.834192, 0.931271], 0.6623286153846155), 
    ([0.037801, 0.103952, 0.165808, 0.232818, 0.44244, 0.643471, 0.705326, 0.769759, 0.832474, 0.898625, 0.962199], 0.8118648181818181)
]

