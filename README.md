# Controller to Mouse
## About the program
This program reads controller inputs and translates them into keyboard and mouse functions.

## Installation
unzip the file in a directory of your choosing, and then run main.exe as an administrator

## How to use it
After installing plug your controller into the device and run the program as an administrator 
    
## Configurations
`config.json` is where the configurations are located  
`mouse_sensitivity` - the movement speed when the mouse joystick is moved  
`scroll_sensitivity` - the scroll speed when the scroll joystick is moved  
`mouse_joystick` - either `left`, `right`, or `none`  
`scroll_joystick` - either `left`, `right`, or `none`  
`disable_binding` - a keystroke (see below) that temporarily disables the controller controls   
`enable_binding` - a keystroke (see below) that enables the controller controls  
`bindings` - a dictionary of keystrokes to responses  
`keyboard_bindings` - a dictionary of bindings to use when the keyboard is focused  
**keystrokes**  
each keystroke is one or more of the following keys separated by pluses (all have to be pressed at the same time)  
```
LEFT_JOYSTICK_UP
LEFT_JOYSTICK_DOWN
LEFT_JOYSTICK_LEFT
LEFT_JOYSTICK_RIGHT
RIGHT_JOYSTICK_UP
RIGHT_JOYSTICK_DOWN
RIGHT_JOYSTICK_LEFT
RIGHT_JOYSTICK_RIGHT
L1
L2
L3
R1
R2
R3
A
B
X
Y
UP
DOWN
LEFT
RIGHT
START
BACK
```

**results**  
can be a string with a keyboard keystroke, a dict with special parameters, or a list of keystrokes  
a keystroke can be a string with a list of keys to press (see keyboard module's send) or a special command (you will have to escape the backslash),  
`\keyboard_toggle` - toggles the keyboard  
`\keyboard_enable` - enables the keyboard  
`\keyboard_disable` - disables the keyboard  
`\left_mouse` - presses and holds the left mouse button until the key is released  
`\right_mouse` - presses and holds the right mouse button until the key is released  
`\middle_mouse` - presses and holds the middle mouse button until the key is released  
`\right_click` - clicks the right mouse button  
`\right_press` - presses the right mouse button until released by the following  
`\right_release` - releases the right mouse button  
`\left_click` - clicks the left mouse button  
`\left_press` - presses the left mouse button until released by the following  
`\left_release` - releases the left mouse button  
`\middle_click` - clicks the middle mouse button  
`\middle_press` - presses the middle mouse button until released by the following  
`\middle_release` - releases the middle mouse button  
`\type `... - types the following text into whatever text box is in focus
*The following is only when the keyboard is in focus*  
`\up` - moves one key up on the keyboard  
`\down` - moves one key down on the keyboard  
`\left` - moves one key left on the keyboard  
`\right` - moves one key right on the keyboard  
`\shift` - toggles the shift modifier for one key
`\ctrl` - toggles the ctrl modifier for one key
`\fn` - toggles the fn modifier for one key
`\win` - toggles the windows modifier for one key
`\alt` - toggles the alt modifier for one key

**dict**
required - `result` - a keystroke or list of keystrokes that result from the hotkey
`trigger` - the trigger that runs on the keystroke - one of 
    `new_press` - the rising edge of the keystroke, no extra parameters  
    `pressed` - every frame the keystroke is pressed, no extra parameters  
    `new_long_press` - the first frame of the press turning into a hold, parameter - `hold_threshold` - how long the keystroke needs to be held  
    `long_press` - every frame of a hold - parameter - `hold_threshold` - how long the keystroke needs to be held  
    `release` - the falling edge of the keystroke - no extra parameters
    `short_release` - the falling edge of the keystroke if the press was not a hold - parameter - `hold_threshold` - how long the keystroke needs to be held  
    `long_release` - the falling edge of the keystroke if the press was a hold - parameter - `hold_threshold` - how long the keystroke needs to be held  
    `hold` - hold the keystroke down until the hotkey is released
    `repeat` repeat the keystroke after an initial delay of `x` seconds with a delay of `y` seconds between each iteration - parameters - `start_delay` - `x`, `repeat_delay` - `y`
`threshold` - unused unless hotkey includes `L2`, `R2` or one of the joysticks - the threshold for the press to be considered a press
    
    
