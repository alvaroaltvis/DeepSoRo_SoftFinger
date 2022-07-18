import RPi.GPIO as GPIO
import time
from timelaps_new import *

#Code for the pump
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(12,GPIO.OUT)
GPIO.setup(13,GPIO.OUT)

pwmo = GPIO.PWM(12,100)
pwm = GPIO.PWM(13,100)

pwm.start(0)
pwmo.start(0)

def inflate():
    max_time = 1
    start_time = time.time()
    while time.time() < max_time + start_time:
        pwm.ChangeDutyCycle(int(dutycycle))
    else: 
        pwm.ChangeDutyCycle(0)
         
def deflate():
    max_time = 1
    start_time = time.time()
    while time.time() < max_time + start_time:
        pwmo.ChangeDutyCycle(int(dutycycle))
    else: 
        pwmo.ChangeDutyCycle(0)
        
stopit = False

while(stopit!= True):
    dutycycle = input("Enter the percentage of Duty Cycle, 100 max value, 1 to quit: ")
    if int(dutycycle) == 1:
        stopit = True
        break
    #name = input("Enter the name of the pictures: ")
    inflate()
    deflate()
    #pictures(name)
   
GPIO.cleanup()
print("Finish")
