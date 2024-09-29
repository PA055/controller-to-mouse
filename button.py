import time
import utils

class Button:    
    def __init__(self, name: str, threshold = 0.5):
        self.name = name
        self.special = any(i in self.name for i in ["TRIGGER", "JOYSTICK"])
        self.threshold = threshold
        self.pressed = False
        self.rising_edge = False
        self.falling_edge = False
        self.repeat_cooldown = 10.0
        self.hold_time = -1
        self.release_time = -1
        self.last_update_time = time.time()
        self.last_long_press_time = time.time()
    
    def update(self):
        if not self.special:
            held = utils.get_buttons()[self.name]
        elif "TRIGGER" in self.name:
            triggers = utils.get_triggers()
            if "LEFT" in self.name: held = triggers[0] >= self.threshold
            if "RIGHT" in self.name: held = triggers[1] >= self.threshold
        elif "JOYSTICK" in self.name:
            joysticks = utils.get_joysticks()
            if self.name.startswith("LEFT"): joystick = joysticks[0]
            if self.name.startswith("RIGHT"): joystick = joysticks[1]
            
            if self.name.endswith("UP"): held = joystick[1] >= self.threshold
            if self.name.endswith("DOWN"): held = -joystick[1] >= self.threshold
            if self.name.endswith("RIGHT"): held = joystick[0] >= self.threshold
            if self.name.endswith("LEFT"): held = -joystick[0] >= self.threshold
        
        self.rising_edge = not self.pressed and held
        self.falling_edge = self.pressed and not held
        self.pressed = held
        dt = time.time() - self.last_update_time
        if self.pressed: 
            self.hold_time += dt
            self.repeat_cooldown -= dt
        else: self.release_time += dt
        if self.rising_edge: 
            self.hold_time = 0
        if self.falling_edge: self.release_time = 0
        self.last_update_time = time.time()
        

    def get_pressed(self) -> bool:
        return self.pressed
            
    def get_new_press(self) -> bool:
        return self.rising_edge
    
    def get_new_long_press(self, long_press_threshold = 1.0) -> bool:
        if self.pressed and self.hold_time >= long_press_threshold: 
            new_long_press = self.last_long_press_time <= time.time() - self.hold_time
            self.last_long_press_time = time.time()
            return new_long_press
        return False
    
    def get_long_pressed(self, long_press_threshold = 1.0) -> bool:
        return self.pressed and self.hold_time >= long_press_threshold
    
    def get_release(self) -> bool:
        return self.falling_edge
    
    def get_short_release(self, long_press_threshold = 1.0) -> bool:
        return self.falling_edge and self.hold_time < long_press_threshold
    
    def get_long_release(self, long_press_threshold = 1.0) -> bool:
        return self.falling_edge and self.hold_time >= long_press_threshold
    
    def get_repeated_new_press(self, repeat_start_delay = 0.5, repeat_delay = 0.1) -> bool:
        if self.rising_edge: 
            self.repeat_cooldown = repeat_start_delay
            return True
        if self.pressed and self.repeat_cooldown < 0:
            self.repeat_cooldown = repeat_delay
            return True
        return False
    
def update_all():
    LEFT_JOYSTICK_UP.update()
    LEFT_JOYSTICK_DOWN.update()
    LEFT_JOYSTICK_LEFT.update()
    LEFT_JOYSTICK_RIGHT.update()
    RIGHT_JOYSTICK_UP.update()
    RIGHT_JOYSTICK_DOWN.update()
    RIGHT_JOYSTICK_LEFT.update()
    RIGHT_JOYSTICK_RIGHT.update()
    L1.update()
    L2.update()
    L3.update()
    R1.update()
    R2.update()
    R3.update()
    A.update()
    B.update()
    X.update()
    Y.update()
    UP.update()
    DOWN.update()
    LEFT.update()
    RIGHT.update()
    START.update()
    BACK.update()

LEFT_JOYSTICK_UP = Button("LEFT_JOYSTICK_UP")
LEFT_JOYSTICK_DOWN = Button("LEFT_JOYSTICK_DOWN")
LEFT_JOYSTICK_LEFT = Button("LEFT_JOYSTICK_LEFT")
LEFT_JOYSTICK_RIGHT = Button("LEFT_JOYSTICK_RIGHT")
RIGHT_JOYSTICK_UP = Button("RIGHT_JOYSTICK_UP")
RIGHT_JOYSTICK_DOWN = Button("RIGHT_JOYSTICK_DOWN")
RIGHT_JOYSTICK_LEFT = Button("RIGHT_JOYSTICK_LEFT")
RIGHT_JOYSTICK_RIGHT = Button("RIGHT_JOYSTICK_RIGHT")
L1 = Button("LEFT_SHOULDER")
L2 = Button("LEFT_TRIGGER")
L3 = Button("LEFT_THUMB")
R1 = Button("RIGHT_SHOULDER")
R2 = Button("RIGHT_TRIGGER")
R3 = Button("RIGHT_THUMB")
A = Button("A")
B = Button("B")
X = Button("X")
Y = Button("Y")
UP = Button("DPAD_UP")
DOWN = Button("DPAD_DOWN")
LEFT = Button("DPAD_LEFT")
RIGHT = Button("DPAD_RIGHT")
START = Button("START")
BACK = Button("BACK")

buttons = {
    "LEFT_JOYSTICK_UP": LEFT_JOYSTICK_UP, 
    "LEFT_JOYSTICK_DOWN": LEFT_JOYSTICK_DOWN, 
    "LEFT_JOYSTICK_LEFT": LEFT_JOYSTICK_LEFT, 
    "LEFT_JOYSTICK_RIGHT": LEFT_JOYSTICK_RIGHT, 
    "RIGHT_JOYSTICK_UP": RIGHT_JOYSTICK_UP, 
    "RIGHT_JOYSTICK_DOWN": RIGHT_JOYSTICK_DOWN, 
    "RIGHT_JOYSTICK_LEFT": RIGHT_JOYSTICK_LEFT, 
    "RIGHT_JOYSTICK_RIGHT": RIGHT_JOYSTICK_RIGHT, 
    "L1": L1, 
    "L2": L2, 
    "L3": L3, 
    "R1": R1, 
    "R2": R2, 
    "R3": R3, 
    "A": A, 
    "B": B, 
    "X": X, 
    "Y": Y, 
    "UP": UP, 
    "DOWN": DOWN, 
    "LEFT": LEFT, 
    "RIGHT": RIGHT, 
    "START": START, 
    "BACK": BACK
}
