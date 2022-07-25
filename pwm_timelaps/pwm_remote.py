import RPi.GPIO as GPIO
import time 
from picamera import PiCamera
import argparse

# If using multiple cameras
# from timelaps_new import *

#Code for the pump
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(12,GPIO.OUT)
#GPIO.setup(13,GPIO.OUT)
GPIO.setup(6, GPIO.OUT)

pwm = GPIO.PWM(12,100)
#pwmo = GPIO.PWM(13,100)

pwm.start(0)
#pwmo.start(0)

#Set up for the camera
camera = PiCamera()
camera.resolution = (1024, 768)
camera.vflip = True
#camera.saturation = 0.2

# Set the command line arguments
parser = argparse.ArgumentParser(description= "Input the name and the power of the air pump")
parser.add_argument("--name", default="image", type=str, required=False, help="The name of the image")
parser.add_argument("--power", default=10, type= int, required=True, help="Enter the percentage of Duty Cycle, 100 max value, 1 to quit: ")

#Use parameters
args = parser.parse_args()
name = args.name
power = args.power 

# Take embeded image
def capture(name):
    for i in range(2):
        camera.capture("/home/raspberrypi/Desktop/EmbededImages/" + name + f"camera{i}.jpg")

# The else statement keeps repeating, I used quit but I want to use a more elegant solution
def inflate(name):
    max_time = 1
    start_time = time.time()
    while time.time() < max_time + start_time:
        GPIO.output(6, 0)
        pwm.ChangeDutyCycle(power)
    else:
        capture(name)
        pwm.stop()
        GPIO.output(6, 1)
        quit()

## If two cameras were to be used 
#def deflate():  
#    max_time = 0.5
#    start_time = time.time()
#    while time.time() < max_time + start_time:
#        pwmo.ChangeDutyCycle(int(dutycycle))
#    else: 
#        pwmo.ChangeDutyCycle(0)
        
stopit = False
while(stopit!= True):
    if power == 1:
        stopit = True
        break
    inflate(name)
    #deflate()
   
GPIO.cleanup()
print("Finish")
