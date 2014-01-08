#	Simple Test Code for Rapsberry Pi Laser Engraver
#	Ian D. Miller
#	Jan 7, 2014
#	http://www.pxlweavr.com
#	info [at] pxlweavr.com

print "Program Started"

import RPi.GPIO as GPIO
import Motor_control
from Bipolar_Stepper_Motor_Class import Bipolar_Stepper_Motor
import time
from numpy import pi, sin, cos, sqrt, arccos, arcsin

#Test program for stepper motor

GPIO.setmode(GPIO.BOARD)
GPIO.setup(3,GPIO.OUT)

motor=Bipolar_Stepper_Motor(8,10,12,16)

try:
    while True:
        direction = int(raw_input("Input Direction: "))
        steps = int(raw_input("Input Step Number: "))
        laservar = int(raw_input("Laser state: "))
        GPIO.output(3,laservar)
        motor.move(direction,steps,0.01)

except KeyboardInterrupt:
    GPIO.cleanup()
