import os, sys
import subprocess

def pictures():
    os.chdir(sys.path[0])
    
    for i in range(3):
        x1 = 'raspi-gpio set 4 op'
        x2 = 'raspi-gpio set 17 op'
        
        os.system(x1)
        os.system(x2)
        # select cam 1
        x3 = 'i2cset -y 1 0x70 0x00 0x01'
        x4 = 'raspi-gpio set 17 dl' #set the gpio17 low
        x5 = 'raspi-gpio set  4 dl' #set the gpio4 low
        os.system(x3)
        os.system(x4)
        os.system(x5)
        bash_command = f'libcamera-still -o camera{i}.jpg'
        process = subprocess.Popen(bash_command.split(), stdout=subprocess.PIPE)
        output, error = process.communicate()
    
        # select cam 2
        x6 = 'i2cset -y 1 0x70 0x00 0x02'
        x7 = 'raspi-gpio set 17 dl' #set the gpio17 low
        x8 = 'raspi-gpio set  4 dh' #set the gpio4 high
        os.system(x6)
        os.system(x7)
        os.system(x8)
        bash_command = f'libcamera-still -o camera_two{i}.jpg'
        process = subprocess.Popen(bash_command.split(), stdout=subprocess.PIPE)
        output, error = process.communicate()
     
    print('Finished')
