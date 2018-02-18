#!/usr/bin/env python

import pigpio
import time

pi = pigpio.pi()

if not pi.connected:
   exit()

button = 17
dataOut = [12, 25, 26, 6]
ledRed = 13
ledYellow = 5
ledGreen = 16
dataIn = [24, 23, 22, 27]
servo = 4

buttonPressed = False
def cbf(GPIO, level, tick):
	global buttonPressed
	buttonPressed = True

buttonCallback = pi.callback(button, pigpio.FALLING_EDGE, cbf)

def resetState():
    pi.set_servo_pulsewidth(servo, 2000)
    time.sleep(0.5)
    pi.set_servo_pulsewidth(servo, 0)
    pi.write(ledRed, 0)
    pi.write(ledYellow, 0)
    pi.write(ledGreen, 0)
    for d in dataOut:
        pi.write(d, 0)

def checkInputs():
    inputsOK = True
    pi.write(ledYellow, 1)
    time.sleep(0.2)
    for d in dataOut:
        pi.write(d, 0)
    print "Thinking..."
    time.sleep(0.2)
    for i, d in enumerate(dataOut):
        pi.write(dataOut[i], 1)
        time.sleep(0.2)
        if pi.read(dataIn[i]) == 0:
            inputsOK = False
            print str(i)+" Digit wrong"
        pi.write(dataOut[i], 0)
        time.sleep(0.2)
    return inputsOK

def pulseServo():
    pi.set_servo_pulsewidth(servo, 1000)
    time.sleep(0.5)
    pi.set_servo_pulsewidth(servo, 0)

def waitForButton():
    global buttonPressed
    while buttonPressed == False:
        print "waiting..."
        time.sleep(0.1)
    #while pi.read(button) > 0:
    #    print "Button pressed..."
    #    time.sleep(0.1)
    print "Button released..."
    buttonPressed = False

while True:
    try:
        resetState()
        waitForButton()
        puzzleSolved = checkInputs()
        pi.write(ledYellow, 0)
        if puzzleSolved:
            pi.write(ledGreen, 1)
            print "Puzzle solved!"
            pulseServo()
            waitForButton()
            resetState()
            pi.write(ledYellow, 1)
            time.sleep(2)
        else:
            pi.write(ledRed, 1)
            print "Wrong answer!"
            time.sleep(2)

    except KeyboardInterrupt:
      break

resetState()
buttonCallback.cancel()
pi.stop()