import RPi.GPIO as GPIO
import time
import random
import psutil
# Set GPIO numbering mode
GPIO.setmode(GPIO.BCM)

# Set pin 11 as an output, and define as servo1 as PWM pin
#GPIO.setup(17,GPIO.OUT)
#servo1 = GPIO.PWM(17,50)

GPIO.setup(17,GPIO.OUT)
servo1 = GPIO.PWM(17,50) # pin 11 for servo1, pulse 50Hz

# Start PWM running, with value of 0 (pulse off)
servo1.start(0)

# Loop to allow user to set servo angle. Try/finally allows exit
# with execution of servo.stop and GPIO cleanup :)
for proc in psutil.process_iter():
    if proc.name() == 'libgpiod_pulsein' or proc.name() == 'libgpiod_pulsei':
        proc.kill()

def function(v):
        #Ask user for angle and turn servo to it
        servo1.ChangeDutyCycle(2+(180/18))
        if(v<=20):
            servo1.ChangeDutyCycle(2+(160/18))
        elif(v>20 and v<=30):
            servo1.ChangeDutyCycle(2+(90/18))
        elif(v>30):
            servo1.ChangeDutyCycle(2+(45/18))

        #servo1.start(0)
        time.sleep(1)
        print(v)
        #servo1.ChangeDutyCycle(0)

