import RPi.GPIO as GPIO
import time
from timelaps_new import *

#Code for the pump
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(12,GPIO.OUT)

pwm = GPIO.PWM(12,100)
pwm.start(0)

def time_air():
    max_time = 1
    start_time = time.time()
    while time.time() < max_time + start_time:
        pwm.ChangeDutyCycle(int(dutycycle))
    else: 
        pwm.ChangeDutyCycle(0)   

stopit = False

while(stopit!= True):
    dutycycle = input("Enter the percentage of Duty Cycle, 100 max value, 1 to quit: ")
    if int(dutycycle) == 1:
        stopit = True
        break
    name = input("Enter the name of the pictures: ")
    time_air()
    pictures(name)
   
GPIO.cleanup()
print("Finish")
