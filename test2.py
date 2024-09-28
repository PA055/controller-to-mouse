import keyboard
import mouse

resolution=[1920,1080]
xpos=0
ypos=0
sensitivity=2
xposprev=0
yposprev=0   

while True:
    ypos=0
    xpos=0
    if keyboard.is_pressed("up"):
        ypos=-1.0
    if keyboard.is_pressed("down"):
        ypos=1.0
    if keyboard.is_pressed("left"):
        xpos=-1.0
    if keyboard.is_pressed("right"):
        xpos=1.0
    ypos*=sensitivity
    xpos*=sensitivity
     
    mouse.move(xpos, ypos, absolute=False, duration=0.001)
    
    
    
    
    print(str(xpos) + "   " + str(ypos))