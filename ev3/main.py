#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, ColorSensor
from pybricks.parameters import Port, Direction, Stop, Color
from pybricks.tools import wait, DataLog, StopWatch
from pybricks.robotics import DriveBase
from threading import Thread

ev3 = EV3Brick()

left_motor = Motor(Port.B)
right_motor = Motor(Port.C)
claw_motor = Motor(Port.A, positive_direction=Direction.CLOCKWISE, gears=[12, 20])

timer = StopWatch()
robot = DriveBase(left_motor, right_motor, wheel_diameter = 57.15, axle_track = 171.45)

left_color = ColorSensor(Port.S2)
right_color = ColorSensor(Port.S3)

passed_lines = 0
threshold = 1000

#-------------- Starting main program ----

print("[MAIN-INFO] Starting main.py")
def completeLineFollow(stopAt, stopsensor):
    print("[Line Follow] *** STARTING LINE FOLLOW ***")
    print("[Line Follow] Line Follower (LF) 2 v1.5.1")
    print("[Line Follow] Inputted stop at intersection: "+str(stopAt))
    global passed_lines 
    if stopsensor == right_color:
        print("[Line Follow] Line stop sensor: right color ")
        line_sensor = left_color
        varEline = 0.7
    else:
        print("[Line Follow] Line stop sensor: left color ")
        line_sensor = right_color
        varEline = -0.7
    stop_lines = stopAt
    passed_lines = 0
    print("[Line Follow] Defining new thread")
    print("[Line Follow] Passing stopAt variable...")
    t = Thread(target=stopLine,args=(stopAt, stopsensor))
    print("[Line Follow] Calling thread 2...")
    t.start()
    print("[Line Follow] Waiting...")
    while passed_lines < stopAt:
        turn_rate = (line_sensor.reflection() - 40) * varEline
        print("[Line Follow] turn rate: " + str(turn_rate))
        robot.drive(70, int(turn_rate))
    robot.stop()

    

def stopLine(stopAt, colorsesor): 
    print("[Line Follow - Thread 2] Starting Thread 2")
    print("[Line Follow - Thread 2] Opening new thread")
    print("[Line Follow] Detected Thread 2 - hooking...")
    print("[Line Follow] Hooked into Thead 2 - will now stop after passing " + str(stopAt) + " intersections")
    print("[Line Follow - Thread 2] Started Thread 2 - target = stopLine")
    global passed_lines
    timer.reset()
    while passed_lines < stopAt:
        if colorsesor.reflection() < 20:
            global threshold
            if timer.time() > threshold:
                global passed_lines
                passed_lines += 1
                timer.reset()
                print("[Line Follow - Thread 2] Passed_line: " + str(passed_lines))
                ev3.speaker.beep()
            else:
                print("[Line Follow - Thread 2] !!!!!!!!!!!!!!!!!!!!")
                print("[Line Follow - Thread 2] Passed two lines too quickly!")
                print("[Line Follow - Thread 2] !!!!!!!!!!!!!!!!!!!!")



            wait(1000)
        else:
            pass
    print("[Line Follow - Thread 2] Passed " + str(stopAt) + " intersections. Stopping...")
    robot.stop()
    print("[Line Follow] Got stop message from Thread 2")
    print("[Line Follow - Thread 2] ***********************")
    print("[Line Follow - Thread 2] Line follow complete")
    print("[Line Follow - Thread 2] ***********************")


def getObject(striaght, color, type):
    print("[Get Object] Pass line")
    robot.straight(striaght)
    print("[Get Object] CLEAR-")
    print("[Get Object] READY TO TURN")
    robot.turn(93)
    timer.reset()
    if type == "short":
        robot.straight(110)
    elif type == "long":
        robot.straight(190)
        wait(500)
    robot.stop()
    seconds = timer.time()
    robot.straight(12)
    wait(1000)
    robot.straight(5)
    print("[Get Object] Loop done")
    wait(500)
    robot.stop()
    print("[Object Door] ^^^^^^^^^ claw half up ^^^^^^^^^^^")
    claw_motor.run_angle(80, 80, then=Stop.HOLD, wait=True)
    print("[Object Door] -----------------------------------")
    wait(2000)
    objectrgb = left_color.rgb()
    print("[Object Door] RGB reading (1) is: " + str(objectrgb))
    print("[Object Door] -----------------------------------")
    wait(1000)
    objectrgb = left_color.rgb()
    print("[Object Door] RGB reading (2) is: " + str(objectrgb))
    print("[Object Door] -----------------------------------")
    wait(1000)
    if objectrgb[0] > 1 and objectrgb[1] > 1:
        output = "yellow"
        print("[Object Door] vvvvvvvvv claw down vvvvvvvvvv")
        claw_motor.run_angle(80, -100, then=Stop.HOLD, wait=True) 
    elif objectrgb[0] > 1 and objectrgb[2] < 2 and objectrgb[1] < 2:
        output = "red"
        wait(1000)
        print("[Object Door] Fulling extanding claw")
        print("[Object Door] ^^^^^^^^^ claw full up ^^^^^^^^^^^")
        claw_motor.run_angle(100, 100, then=Stop.HOLD, wait=False)
        wait(1000)
        robot.straight(95)
        claw_motor.hold()
        print("[Object Door] vvvvvvvvv claw down vvvvvvvvvv")
        claw_motor.run_angle(70, -145, then=Stop.HOLD, wait=True)
        robot.straight(-95)
    else:
        print("[Object Door] vvvvvvvvv claw down vvvvvvvvvv")
        claw_motor.run_angle(70, -80, then=Stop.HOLD, wait=True)
    robot.drive(-70, 0)
    wait(seconds)
    robot.straight(-15)
    robot.stop()
    robot.turn(-95)
    print("[Get Object] Back on line")

def getObject(striaght, color, type):
    print("[Get Object] Pass line")
    robot.straight(striaght)
    print("[Get Object] CLEAR-")
    print("[Get Object] READY TO TURN")
    robot.turn(93)
    timer.reset()
    if type == "short":
        robot.straight(110)
    elif type == "long":
        robot.straight(190)
        wait(500)
    elif type == "sinklong":
        robot.straight(140)
        wait(400)
    elif type == "bedcrasher":
        robot.straight(230)
        wait(500)
    robot.stop()
    seconds = timer.time()
    robot.straight(12)
    wait(1000)
    robot.straight(5)
    print("[Get Object] Loop done")
    wait(500)
    robot.stop()
    print("[Object Door] ^^^^^^^^^ claw half up ^^^^^^^^^^^")
    claw_motor.run_angle(80, color, then=Stop.HOLD, wait=True)
    print("[Object Door] -----------------------------------")
    wait(2000)
    objectrgb = left_color.rgb()
    print("[Object Door] RGB reading (1) is: " + str(objectrgb))
    print("[Object Door] -----------------------------------")
    wait(1000)
    objectrgb = left_color.rgb()
    print("[Object Door] RGB reading (2) is: " + str(objectrgb))
    print("[Object Door] -----------------------------------")
    wait(1000)
    if objectrgb[0] > 1 and objectrgb[1] > 1:
        output = "yellow"
        print("[Object Door] vvvvvvvvv claw down vvvvvvvvvv")
        claw_motor.run_angle(80, -100, then=Stop.HOLD, wait=True) 
    elif objectrgb[0] > 1 and objectrgb[2] < 2 and objectrgb[1] < 2:
        output = "red"
        wait(1000)
        print("[Object Door] Fulling extanding claw")
        print("[Object Door] ^^^^^^^^^ claw full up ^^^^^^^^^^^")
        claw_motor.run_angle(100, 100, then=Stop.HOLD, wait=False)
        wait(1000)
        robot.straight(95)
        claw_motor.hold()
        print("[Object Door] vvvvvvvvv claw down vvvvvvvvvv")
        claw_motor.run_angle(70, -145, then=Stop.HOLD, wait=True)
        robot.straight(-95)
    else:
        print("[Object Door] vvvvvvvvv claw down vvvvvvvvvv")
        claw_motor.run_angle(70, -80, then=Stop.HOLD, wait=True)
    robot.drive(-70, 0)
    wait(seconds)
    robot.straight(-15)
    robot.stop()
    robot.turn(-95)
    print("[Get Object] Back on line")

def specialGetObject(striaght=50, color=80, type="sinklong"):
    print("[Get Object] Pass line")
    robot.straight(striaght)
    print("[Get Object] CLEAR-")
    print("[Get Object] READY TO TURN")
    robot.turn(87)
    timer.reset()
    if type == "short":
        robot.straight(110)
    elif type == "long":
        robot.straight(190)
        wait(500)
    elif type == "sinklong":
        robot.straight(150)
        wait(400)
    elif type == "bedcrasher":
        robot.straight(230)
        wait(500)
    robot.stop()
    seconds = timer.time()
    robot.straight(12)
    wait(1000)
    robot.straight(5)
    print("[Get Object] Loop done")
    wait(500)
    robot.stop()
    print("[Object Door] ^^^^^^^^^ claw half up ^^^^^^^^^^^")
    claw_motor.run_angle(80, color, then=Stop.HOLD, wait=True)
    print("[Object Door] -----------------------------------")
    wait(2000)
    objectrgb = left_color.rgb()
    print("[Object Door] RGB reading (1) is: " + str(objectrgb))
    print("[Object Door] -----------------------------------")
    wait(1000)
    objectrgb = left_color.rgb()
    print("[Object Door] RGB reading (2) is: " + str(objectrgb))
    print("[Object Door] -----------------------------------")
    wait(1000)
    if objectrgb[0] > 1 and objectrgb[1] > 1:
        output = "yellow"
        print("[Object Door] vvvvvvvvv claw down vvvvvvvvvv")
        claw_motor.run_angle(80, -100, then=Stop.HOLD, wait=True) 
    elif objectrgb[0] > 1 and objectrgb[2] < 2 and objectrgb[1] < 2:
        output = "red"
        wait(1000)
        print("[Object Door] Fulling extanding claw")
        print("[Object Door] ^^^^^^^^^ claw full up ^^^^^^^^^^^")
        claw_motor.run_angle(100, 100, then=Stop.HOLD, wait=False)
        wait(1000)
        robot.straight(95)
        claw_motor.hold()
        print("[Object Door] vvvvvvvvv claw down vvvvvvvvvv")
        claw_motor.run_angle(70, -145, then=Stop.HOLD, wait=True)
        robot.straight(-95)
    else:
        print("[Object Door] vvvvvvvvv claw down vvvvvvvvvv")
        claw_motor.run_angle(70, -80, then=Stop.HOLD, wait=True)
    robot.drive(-70, 0)
    wait(seconds)
    robot.straight(-15)
    robot.stop()
    robot.turn(-87)
    print("[Get Object] Back on line")

def waitUntilReflect(compareValue):
    while True:
        if left_color.reflection() == compareValue or left_color.reflection() < compareValue:
            break
        else:
            pass
'''
print("[SUN-FINDER] Finding sun")
robot.turn(-110)
robot.straight(70)
claw_motor.run_angle(70, 90, then=Stop.HOLD, wait=True)
ev3.speaker.say(str(left_color.color()))
tempStore = left_color.color()
print("[SUN-FINDER] Right position is " + str(left_color.color()))
robot.straight(-70)
robot.turn(110)
if tempStore == None:
    posOfSun = "right"
else:
    posOfSunn = "left"
robot.straight(100)
print("[SUN-FINDER] Finished sun")
claw_motor.run_angle(70, -90, then=Stop.HOLD, wait=True)
'''
def testRGBYEET():
    print(ColorSensor(Port.S2).rgb())

def MAINYEET():
    completeLineFollow(1, right_color)
    wait(2000)
    getObject(20, 80, "short")


    completeLineFollow(1, left_color)
    wait(1000)
    completeLineFollow(1, right_color)
    wait(2000)
    getObject(30, 80, "long")
    threshold = 2000
    completeLineFollow(1, right_color)
    wait(2000)
    threshold = 500
    getObject(20, 80, "short")
    completeLineFollow(1, right_color)
    wait(1000)
    robot.straight(50)
    completeLineFollow(1, right_color)
    wait(2000)
    getObject(30, 100, "long")
    robot.straight(30)
    completeLineFollow(1, right_color)
    wait(2000)
    print("[MAIN-INFO] Turning")
    robot.straight(20)
    robot.turn(95)
    robot.straight(450)
    print("[Object Door] ^^^^^^^^^ claw full up ^^^^^^^^^^^")
    claw_motor.run_until_stalled(90, then=Stop.HOLD, duty_limit=None)
    print("[MAIN-INFO] Dumped bulbs")
    robot.straight(-300)
def MAINYEETBUTBACKWARDS():
    print("[Object Door] vvvvvvvvv claw down vvvvvvvvvv")
    claw_motor.run_angle(70, -140, then=Stop.HOLD, wait=True)
    robot.drive(-60, 0)
    while True:
        if right_color.reflection() < 20:
            ev3.speaker.beep()
            break
    robot.stop()
    robot.straight(30)
    robot.turn(93)
        
    completeLineFollow(2, right_color)
    pass
    pass
    #^^every random
    pass
    pass
    wait(2000)
    specialGetObject()
    robot.straight(70)
    completeLineFollow(1, right_color)
    wait(2000)
    getObject(50, 80, "short")

    robot.turn(185)
    completeLineFollow(2, right_color)
    robot.straight(50)
    completeLineFollow(2, right_color)
    wait(2000)
    print("[MAIN-INFO] Turning")
    robot.straight(20)
    robot.turn(95)
    robot.straight(450)
    print("[Object Door] ^^^^^^^^^ claw full up ^^^^^^^^^^^")
    claw_motor.run_until_stalled(90, then=Stop.HOLD, duty_limit=None)
    print("[MAIN-INFO] Dumped bulbs")
    robot.straight(-300)
#---------------------- MAIN PROGRAM STARTs HERE -----------------------------

robot.straight(30)  
MAINYEET()

#completeLineFollow(1, right_color)
#wait(2000)

MAINYEETBUTBACKWARDS()

#testRGBYEET()
#getObject(20, 220, "long")
'''
'''
print("[MAIN-INFO] Finished main.py")
