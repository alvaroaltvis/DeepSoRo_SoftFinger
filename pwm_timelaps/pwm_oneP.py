import RPi.GPIO as GPIO
import time 
from picamera import PiCamera
import argparse
import os

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
parser.add_argument("--folder", default="image", type=str, required=True, help="Name of the folder where the images will be stored")

#Use parameters
args = parser.parse_args()
name = args.name
power = args.power
folder_name = args.folder
# Preview Camera
camera.start_preview()

# Take embeded image
def capture(name):
    for i in range(1):
        camera.capture(f"/home/raspberrypi/Desktop/EmbededImages/{folder_name}/" + name + f".jpg")

# The else statement keeps repeating, I used quit but I want to use a more elegant solution
def inflate(name):
    if power == 0:
       GPIO.output(6, 1) # Open Valvue
    else:
        max_time = 1
        start_time = time.time()
        while time.time() < max_time + start_time:
            GPIO.output(6, 0) # Close Valvue
            pwm.ChangeDutyCycle(power)
        else:
            capture(name)
            pwm.stop()

inflate(name)

#GPIO.cleanup()
print("Finish")
