#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, ColorSensor
from pybricks.parameters import Port, Direction, Stop, Color
from pybricks.tools import wait, DataLog, StopWatch
from pybricks.robotics import DriveBase
from threading import Thread

ev3 = EV3Brick()
data = DataLog('time', 'value', name='data', timestamp= False, extension='csv')
left_motor = Motor(Port.B)
right_motor = Motor(Port.C)
claw_motor = Motor(Port.A, positive_direction=Direction.CLOCKWISE, gears=[12, 20])


robot = DriveBase(left_motor, right_motor, wheel_diameter=56, axle_track=120)

left_color = ColorSensor(Port.S2)
right_color = ColorSensor(Port.S3)
object_color = ColorSensor(Port.S4)

passed_lines =0
def completeLineFollow(stopAt, colorsensor):
    print("stopAt:"+str(stopAt))
    global passed_lines 
    if colorsensor == right_color:
        print("right color ")
        line_sensor = left_color
        varEline = 0.7
    else:
        print("left color ")
        line_sensor = right_color
        varEline = -0.7
    stop_lines = stopAt
    passed_lines = 0
    t = Thread(target=stopLine,args=(stopAt, colorsensor))
    t.start()
    while passed_lines < stopAt:
        turn_rate = (line_sensor.reflection() - 50) * varEline
        robot.drive(50, turn_rate)
    robot.stop()

    

def stopLine(stopAt, colorsesor):
    global passed_lines
    wait(1000)
    while passed_lines < stopAt:
        if colorsesor.reflection() < 20:
            global passed_lines
            passed_lines += 1
            print("passed_line:"+str(passed_lines))
            ev3.speaker.beep()
            wait(1000)
        else:
            pass
    robot.stop()
    print("stop line")

def waitUntilReflect(compareValue):
    while True:
        if left_color.reflection() == compareValue or left_color.reflection() < compareValue:
            break
        else:
            pass
def pickup():
    robot.straight(50)
    ev3.speaker.beep()
    wait(500)
    robot.turn(-90)
    ev3.speaker.beep()
    robot.straight(200)
    robot.turn(180)
    robot.drive(50, 0)
    waitUntilReflect(20)
    wait(100)
    robot.stop()
    robot.straight(150)
    claw_motor.run_angle(100, 100, then=Stop.COAST, wait=True)
    color = object_color.color()
    ev3.speaker.say(str(color))
    return color
    
def getOut(turnRight, howMuch):
    robot.drive(-50, 0)
    wait(howMuch)
    robot.stop
    if turnRight == True:
        robot.turn(-90)
    else:
        robot.turn(90)
        

'''
watch = StopWatch()
while True:
    ev3.screen.print(left_color.reflection())
    value = left_color.reflection()
    time = watch.time()
    data.log(time, value)
    wait(10)
    ev3.screen.clear()


completeLineFollow(1)

#next code here

robot.straight(1000)
robot.turn(-95)

#!start code here
'''
def red1posmed():
    robot.drive(60, 0)
    waitUntilReflect(20)
    robot.straight(100)
    robot.stop()
    robot.turn(90)

    completeLineFollow(2, right_color)
    pickup()
    getOut(False, 1500)
    completeLineFollow(1, left_color)
    robot.stop()
    print("stop....")
    robot.straight(1000)
    print("straight....")
    ev3.speaker.beep()
    print("straight....-500")

    #code 
    robot.turn(90)
    print("correcting....")
    robot.drive(80, -10)
    waitUntilReflect(20)
    print("find line")

    completeLineFollow(3, right_color)


    wait(2000)
    print("stopped")

    robot.turn(100)
    print("turned")
    robot.drive(60, 0)
    wait(200)
    claw_motor.run_angle(100, -100, then=Stop.COAST, wait=False)
    wait(4200)

    robot.straight(-200)

    robot.turn(90)

    completeLineFollow(2, right_color)
    robot.straight(100)

robot.straight(50)
robot.turn(-90)
completeLineFollow(3, right_color)
pickup()