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
global redBulbs
redBulbs = []
global redBulbsPicked
redBulbsPicked = 0
robot.settings(200, 1000, 90, 1000)

#-------------- Starting main program ----

print("[MAIN-INFO] Starting main.py")
def completeLineFollow(stopAt, stopsensor, speed=135):
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
        #print("[Line Follow] turn rate: " + str(turn_rate))
        robot.drive(speed, int(turn_rate))
    robot.stop()
def timedLineFollow(stopAt, line_sensor, speed=135):
    stopping = False
    print("[Line Follow] *** STARTING mod.LINE FOLLOW ***")
    print("[Line Follow] Line Follower (LF) 2 v1.5.1")
    print("[Line Follow] Inputted stop at time: "+str(stopAt))
    if line_sensor == left_color:
        varEline = 0.7
    else:
        varEline = -0.7
    passed_lines = 0
    print("[Line Follow] Defining new thread")
    print("[Line Follow] Passing stopAt variable...")
    timer.reset()
    while int(timer.time()) <= stopAt*1000:
        turn_rate = (line_sensor.reflection() - 40) * varEline
        #print("[Line Follow] turn rate: " + str(turn_rate))
        robot.drive(speed, int(turn_rate))
    robot.stop()
    print("[Line Follow] ***********************")
    print("[Line Follow] Line follow complete")
    print("[Line Follow] ***********************")
def consolePrint():
    while True:
        wait(200)
        print("")    
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
            if timer.time() > threshold or threshold == 0:
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

'''
def getObject(striaght, color, type, currentpos):
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
'''
def getObject(striaght, color, type, currentPos):
    
    print("[Get Object] Pass line")
    robot.straight(striaght)
    print("[Get Object] CLEAR-")
    print("[Get Object] READY TO TURN")
    global redBulbsPicked
    if redBulbsPicked != 3:
        wait(1500)
        if currentPos == "R4":
            print("[Object Door] ^^^^^^^^^ claw full up ^^^^^^^^^^^")
            claw_motor.run_angle(100, 180, then=Stop.HOLD, wait=False)
        else:
            print("[Object Door] ^^^^^^^^^ claw half up ^^^^^^^^^^^")
            claw_motor.run_angle(80, color, then=Stop.HOLD, wait=False)
        if type == "short":
            robot.turn(93)
            timer.reset()
            robot.straight(110)
        elif type == "long":
            robot.turn(93)
            timer.reset()
            robot.straight(190)
            wait(500)
        elif type == "sinklong":
            robot.turn(90)
            timer.reset()
            robot.straight(180)
            wait(400)
        elif type == "bedcrasher":
            robot.turn(93)
            timer.reset()
            robot.straight(230)
            wait(500)
        robot.stop()
        seconds = timer.time()
        robot.straight(17)
        print("[Get Object] Loop done")
        wait(500)
        robot.stop()
        if currentPos == "R4":
            output = "red"
            redBulbs.append(currentPos)
            redBulbsPicked += 1
            print("[Get Object] Bulbs picked up is " + str(redBulbsPicked))
            print("[Get Object] Appending currentPos to redBulbs")
            print("[Get Object] redBulbs is currently " + str(redBulbs))
            print("[Object Door] Fulling extanding claw")
            robot.straight(100)
            claw_motor.hold()
            print("[Object Door] vvvvvvvvv claw down vvvvvvvvvv")
            claw_motor.run_angle(200, -160, then=Stop.HOLD, wait=True)
            robot.straight(-100)
        else:
            print("[Object Door] -----------------------------------")
            objectrgb = left_color.rgb()
            altobjectrgb = right_color.rgb()
            print("[Object Door] RGB reading (1) is: " + str(objectrgb) + " or " + str(altobjectrgb))
            print("[Object Door] -----------------------------------")
            wait(500)
            objectrgb = left_color.rgb()
            altobjectrgb = right_color.rgb()
            print("[Object Door] RGB reading (2) is: " + str(objectrgb)+ " or " + str(altobjectrgb))
            print("[Object Door] -----------------------------------")
            if (objectrgb[0] > 1 and objectrgb[1] > 1) or (altobjectrgb[0] > 1 and altobjectrgb[1] > 1 ):
                output = "yellow"
                print("[Object Door] vvvvvvvvv claw down vvvvvvvvvv")
                claw_motor.run_angle(100, -100, then=Stop.HOLD, wait=False) 
            elif (objectrgb[0] > 1 and objectrgb[2] < 2) or (altobjectrgb[0] > 1 and altobjectrgb[2] < 2):
                output = "red"
                redBulbs.append(currentPos)
                redBulbsPicked += 1
                print("[Get Object] Bulbs picked up is " + str(redBulbsPicked))
                print("[Get Object] Appending currentPos to redBulbs")
                print("[Get Object] redBulbs is currently " + str(redBulbs))
                wait(1000)
                print("[Object Door] Fulling extanding claw")
                print("[Object Door] ^^^^^^^^^ claw full up ^^^^^^^^^^^")
                claw_motor.run_angle(100, 100, then=Stop.HOLD, wait=False)
                wait(1000)
                robot.straight(100)
                claw_motor.hold()
                print("[Object Door] vvvvvvvvv claw down vvvvvvvvvv")
                claw_motor.run_angle(200, -160, then=Stop.HOLD, wait=True)
                robot.straight(-100)
            else:
                print("[Object Door] Failed to get color")
                print("[Object Door] vvvvvvvvv claw down vvvvvvvvvv")
                claw_motor.run_angle(100, -80, then=Stop.HOLD, wait=False)
        robot.drive(-100, 0)
        wait(seconds)
        robot.straight(-45)
        robot.stop()
        robot.turn(-95)
        print("[Get Object] Back on line")
    else:
        print("[Get Object] Already picked up 3 bulbs, skipping...")
def invertGetObject(striaght, color, type, currentPos):
    print("[Get Object] Pass line")
    robot.straight(striaght)
    print("[Get Object] CLEAR-")
    print("[Get Object] READY TO TURN")
    robot.turn(-93)
    timer.reset()
    print("[Object Door] ^^^^^^^^^ claw half up ^^^^^^^^^^^")
    claw_motor.run_angle(100, color, then=Stop.HOLD, wait=False)
    if type == "short":
        robot.straight(120)
    elif type == "long":
        robot.straight(220)
        wait(500)
    elif type == "sinklong":
        robot.straight(200)
        wait(400)
    elif type == "bedcrasher":
        robot.straight(230)
        wait(500)
    robot.stop()
    seconds = timer.time()
    robot.straight(17)
    print("[Get Object] Loop done")
    wait(500)
    robot.stop()
            
    print("[Object Door] -----------------------------------")
    objectrgb = left_color.rgb()
    altobjectrgb = right_color.rgb()
    print("[Object Door] RGB reading (1) is: " + str(objectrgb) + " or " + str(altobjectrgb))
    print("[Object Door] -----------------------------------")
    wait(500)
    objectrgb = left_color.rgb()
    altobjectrgb = right_color.rgb()
    print("[Object Door] RGB reading (2) is: " + str(objectrgb)+ " or " + str(altobjectrgb))
    print("[Object Door] -----------------------------------")
    if (objectrgb[0] > 1 and objectrgb[1] > 1) or (altobjectrgb[0] > 1 and altobjectrgb[1] > 1 ):
        output = "yellow"
        print("[Object Door] vvvvvvvvv claw down vvvvvvvvvv")
        claw_motor.run_angle(80, -(color), then=Stop.HOLD, wait=True) 
    elif (objectrgb[0] > 1 and objectrgb[2] < 2) or (altobjectrgb[0] > 1 and altobjectrgb[2] < 2):
        output = "red"
        global redBulbsPicked
        redBulbs.append(currentPos)
        redBulbsPicked += 1
        print("[Get Object] Bulbs picked up is " + str(redBulbsPicked))
        print("[Get Object] Appending currentPos to redBulbs")
        print("[Get Object] redBulbs is currently " + str(redBulbs))
        wait(1000)
        print("[Object Door] Fulling extanding claw")
        print("[Object Door] ^^^^^^^^^ claw full up ^^^^^^^^^^^")
        claw_motor.run_angle(100, 100, then=Stop.HOLD, wait=False)
        wait(1000)
        robot.straight(100)
        claw_motor.hold()
        print("[Object Door] vvvvvvvvv claw down vvvvvvvvvv")
        claw_motor.run_angle(70, -160, then=Stop.HOLD, wait=True)
        robot.straight(-100)
    else:
        print("[Object Door] Failed to get color")
        print("[Object Door] vvvvvvvvv claw down vvvvvvvvvv")
        claw_motor.run_angle(70, -80, then=Stop.HOLD, wait=True)
    robot.drive(-100, 0)
    wait(seconds)
    robot.straight(-50)
    robot.stop()
    robot.turn(95)
    print("[Get Object] Back on line")
def specialGetObject(striaght=40, color=90, type="turnbad"):
    print("[Get Object] Pass line")
    robot.straight(striaght)
    print("[Get Object] CLEAR-")
    print("[Get Object] READY TO TURN")
    robot.turn(93)
    print("[Object Door] ^^^^^^^^^ claw half up ^^^^^^^^^^^")
    claw_motor.run_angle(80, color, then=Stop.HOLD, wait=False)
    robot.straight(200)
    wait(400)

    robot.stop()
    seconds = timer.time()
    robot.straight(12)
    print("[Get Object] Loop done")
    robot.stop()
        
    print("[Object Door] -----------------------------------")
    objectrgb = left_color.rgb()
    altobjectrgb = right_color.rgb()
    print("[Object Door] RGB reading (1) is: " + str(objectrgb) + " or " + str(altobjectrgb))
    print("[Object Door] -----------------------------------")
    wait(500)
    objectrgb = left_color.rgb()
    altobjectrgb = right_color.rgb()
    print("[Object Door] RGB reading (2) is: " + str(objectrgb)+ " or " + str(altobjectrgb))
    if (objectrgb[0] > 1 and objectrgb[1] > 1) or (altobjectrgb[0] > 1 and altobjectrgb[1] > 1 ):
        output = "yellow"
        print("[Object Door] vvvvvvvvv claw down vvvvvvvvvv")
        claw_motor.run_angle(100, -100, then=Stop.HOLD, wait=True) 
    elif (objectrgb[0] > 1 and objectrgb[2] < 2) or (altobjectrgb[0] > 1 and altobjectrgb[2] < 2):
        output = "red"
        redBulbs.append("R2")
        global redBulbsPicked
        redBulbsPicked += 1
        print("[Get Object] Bulbs picked up is " + str(redBulbsPicked))
        print("[Get Object] Appending currentPos to redBulbs")
        print("[Get Object] redBulbs is currently " + str(redBulbs))
        wait(1000)
        print("[Object Door] Fulling extanding claw")
        print("[Object Door] ^^^^^^^^^ claw full up ^^^^^^^^^^^")
        claw_motor.run_angle(100, 100, then=Stop.HOLD, wait=False)
        wait(1000)
        robot.straight(100)
        claw_motor.hold()
        print("[Object Door] vvvvvvvvv claw down vvvvvvvvvv")
        claw_motor.run_angle(100, -160, then=Stop.HOLD, wait=True)
        robot.straight(-100)
    else:
        print("[Object Door] vvvvvvvvv claw down vvvvvvvvvv")
        claw_motor.run_angle(100, -110, then=Stop.HOLD, wait=False)
    robot.straight(-215)
    robot.stop()
    robot.turn(-95)
    print("[Get Object] Back on line")

def waitUntilReflect(compareValue):
    while True:
        if left_color.reflection() == compareValue or left_color.reflection() < compareValue:
            break
        else:
            pass

def tossObject(striaght, color, type):
    print("[Get Object] Pass line")
    robot.straight(striaght)
    print("[Get Object] CLEAR-")
    print("[Get Object] READY TO TURN")
    robot.turn(-93)
    timer.reset()
    if type == "short":
        robot.straight(110)
    elif type == "long":
        robot.straight(190)
        wait(500)
    elif type == "sinklong":
        robot.straight(140)
        wait(400)
    elif type == "turnbad":
        robot.straight(170)
        wait(500)
    elif type == "bedcrasher":
        robot.straight(230)
        wait(500)
    robot.stop()
    seconds = timer.time()
    robot.straight(12)
    wait(1000)
    robot.straight(20)
    print("[Get Object] Loop done")
    wait(500)
    print("[Object Door] Fulling extanding claw")
    print("[Object Door] ^^^^^^^^^ claw full up ^^^^^^^^^^^")
    claw_motor.run_angle(100, 100, then=Stop.HOLD, wait=False)
    wait(1000)
    robot.straight(95)
    claw_motor.hold()
    print("[Object Door] vvvvvvvvv claw down vvvvvvvvvv")
    claw_motor.run_angle(70, -145, then=Stop.HOLD, wait=True)
    robot.straight(-95)
    robot.drive(-70, 0)
    wait(seconds)
    robot.straight(-15)
    robot.stop()
    robot.turn(95)
    print("[Get Object] Back on line")
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
def getSunPos():
    print("[Object Door] ^^^^^^^^^ claw half up ^^^^^^^^^^^")
    claw_motor.run_angle(80, 80, then=Stop.HOLD, wait=True)
    robot.turn(95)
    robot.straight(70)
    print("[Object Door] -----------------------------------")
    objectrgb = left_color.rgb()
    altobjectrgb = right_color.rgb()
    print("[Object Door] RGB reading (1) is: " + str(objectrgb) + " or " + str(altobjectrgb))
    print("[Object Door] -----------------------------------")
    wait(500)
    objectrgb = left_color.rgb()
    altobjectrgb = right_color.rgb()
    print("[Object Door] RGB reading (2) is: " + str(objectrgb)+ " or " + str(altobjectrgb))
    if (objectrgb[0] == 0 and objectrgb[1] == 0 and objectrgb[2] == 0) or (altobjectrgb[0] == 0 and altobjectrgb[1] == 0 and altobjectrgb[2] == 0):
        sunPos = "left"
        print("[Solar Panel] " + str(sunPos))
        return sunPos
    else:
        sunPos = "right"
        print("[Solar Panel] " + str(sunPos))
        return sunPos
        '''
        print("[Object Door] ^^^^^^^^^ claw half up ^^^^^^^^^^^")
        claw_motor.run_angle(80, -80, then=Stop.HOLD, wait=False)
        robot.straight(-90)
        robot.turn(-95)
        robot.straight(50)
        completeLineFollow(4, right_color)
        wait(1500)
        robot.turn(-90)
        robot.straight(-590)
        robot.straight(500)
        robot.turn(90)
        '''

def MAINYEETPANEL():
    sunPos = getSunPos()
    print("[Object Door] ^^^^^^^^^ claw half up ^^^^^^^^^^^")
    claw_motor.run_angle(80, -80, then=Stop.HOLD, wait=False)
    robot.straight(-70)
    robot.turn(-95)
    robot.straight(70)
    completeLineFollow(1, right_color)
    getObject(50, 100, "short", "R1")
    if sunPos == "left":
        robot.straight(139)
        wait(1500)

        robot.straight(20)
        robot.turn(90)
        robot.straight(-590)
        completeLineFollow(1, right_color)
        wait(1500)
        robot.straight(30)
        robot.turn(-93) 
        robot.straight(80)
    else:
        completeLineFollow(1, right_color)
        wait(1500)
    specialGetObject()
    robot.straight(40)
    if redBulbsPicked != 3:
        invertGetObject(30, 80, "short", "L1")
    else:
        robot.straight(60)
        print("[Get Object] Already picked up 3 bulbs, skipping") 
    threshold = 500
    if redBulbsPicked != 3:
        completeLineFollow(1, right_color)
        getObject(30, 100, "short", "R3")
        completeLineFollow(1, right_color)
        if sunPos == "right":
            wait(1500)
            robot.straight(30)
            robot.turn(-90)
            robot.straight(-590)
            completeLineFollow(1, right_color)
            wait(1500)
            robot.turn(93)
        if redBulbsPicked != 3:
            wait(1500)
            robot.straight(100)
            invertGetObject(50, 90, "long" , "L2")
            if redBulbsPicked != 3:
                robot.straight(101)
                getObject(10, 80, "sinklong", "R4")
                completeLineFollow(1, right_color)
            else:
                completeLineFollow(1, right_color)
        else:
            print("[Get Object] Already picked up 3 bulbs, skipping")
            print("[Line Follow] Last line follow")
            completeLineFollow(2, right_color, 200)
    else:
        if sunPos == "right":
            completeLineFollow(2, right_color)
            wait(1500)
            robot.straight(30)
            robot.turn(-90)
            robot.straight(-590)
            completeLineFollow(1, right_color)
            wait(1500)
            robot.turn(90)
            completeLineFollow(2, right_color, 200)
            
        else:
            ompleteLineFollow(4, right_color, 200)
        
    
    wait(2000)
    print("[MAIN-INFO] Turning")
    robot.straight(20)
    robot.turn(93)
    robot.stop()
    robot.settings(200, 100, 90, 100)
    print("[Object Door] ^^^^^^^^^ claw full up ^^^^^^^^^^^")
    claw_motor.run_angle(100, 190, then=Stop.HOLD, wait=False)
    robot.straight(500)
    print("[MAIN-INFO] Dumped bulbs")
    robot.straight(-500)
    robot.stop()
def MAINYEETNOPANEL():
    robot.straight(70)
    completeLineFollow(1, right_color)
    getObject(50, 100, "short", "R1")
    completeLineFollow(1, right_color)
    wait(1500)
    specialGetObject()
    robot.straight(40)
    if redBulbsPicked != 3:
        invertGetObject(30, 90, "short", "L1")
    else:
        robot.straight(60)
        print("[Get Object] Already picked up 3 bulbs, skipping") 
    threshold = 500
    if redBulbsPicked != 3:
        completeLineFollow(1, right_color)
        getObject(30, 100, "short", "R3")
        completeLineFollow(1, right_color)
        if redBulbsPicked != 3:
            wait(1500)
            robot.straight(100)
            invertGetObject(50, 100, "long" , "L2")
            if redBulbsPicked != 3:
                robot.straight(101)
                getObject(10, 90, "sinklong", "R4")
                completeLineFollow(1, right_color)
            else:
                completeLineFollow(1, right_color)
        else:
            print("[Get Object] Already picked up 3 bulbs, skipping")
            print("[Line Follow] Last line follow")
            completeLineFollow(2, right_color, 200)
    else:     
        completeLineFollow(4, right_color, 200)
        
    
    wait(2000)
    print("[MAIN-INFO] Turning")
    robot.straight(20)
    robot.turn(93)
    robot.stop()
    print("[Object Door] ^^^^^^^^^ claw full up ^^^^^^^^^^^")
    claw_motor.run_angle(100, 190, then=Stop.HOLD, wait=False)
    robot.straight(500)
    print("[MAIN-INFO] Dumped bulbs")
    robot.straight(-500)
    robot.stop()
def MAINYEETBUTBACKWARDS():
    claw_motor.stop()
    print("[Object Door] ^^^^^^^^^ claw full up ^^^^^^^^^^^")
    claw_motor.run_angle(100, -190, then=Stop.HOLD, wait=False)
    robot.turn(95)
    timedLineFollow(12, left_color, 200)
    robot.straight(-100)
def MAINWHITEYEET():
    robot.straight(115)
    robot.turn(90)
    print("[Object Door] ^^^^^^^^^ claw full up ^^^^^^^^^^^")
    claw_motor.run_until_stalled(90, then=Stop.HOLD, duty_limit=None)
    robot.straight(190)
    print("[Object Door] vvvvvvvvv claw down vvvvvvvvvv")
    claw_motor.run_angle(70, -170, then=Stop.HOLD, wait=True)
    claw_motor.hold()
    robot.straight(-190)
    robot.turn(-90)
    completeLineFollow(1, right_color)
    wait(2000)
    robot.straight(20)
    robot.turn(95)
    completeLineFollow(1, right_color)
    wait(2000)
    robot.straight(-10)
    robot.turn(93)
    print("[Object Door] ^^^^^^^^^ claw full up ^^^^^^^^^^^")
    claw_motor.run_angle(100, 180, then=Stop.HOLD, wait=False)
    robot.straight(200)
    print("[Object Door] vvvvvvvvv claw down vvvvvvvvvv")
    claw_motor.run_angle(70, -170, then=Stop.HOLD, wait=True)





    

    
#---------------------- MAIN PROGRAM STARTs HERE -----------------------------

#tt = Thread(target=consolePrint)
#tt.start()
#robot.straight(50)  

MAINYEETNOPANEL()
print("-------------------------------------")
print("     |                       |")
print(" ")
print("      robot.st ")
MAINYEETBUTBACKWARDS()
'''
timedLineFollow(12, left_color, 200)
robot.straight(-100)
'''

print("[MAIN-INFO] Finished main.py")
