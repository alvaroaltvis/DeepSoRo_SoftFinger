import RPi.GPIO as GPIO
from time import sleep
from timelapsbull import *

#Code for the pump
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(12,GPIO.OUT)

pwm = GPIO.PWM(12,100)
pwm.start(0)

stopit = False

while(stopit!= True):
    dutycycle = input("Enter the percentage of Duty Cycle, 100 max value, 1 to quit: ")
    if int(dutycycle) == 1:
        stopit = True
        break
    name = input("Enter the name of the pictures: ")
    pwm.ChangeDutyCycle(int(dutycycle))1
    
    picture(name)
   
GPIO.cleanup()
print("Finish")
