# Set up SDK softwear for Linux 18.04

### First make sure that your linux is AMD64 

``` 
dpkg --print-architecture 
```

### Then download the Microsoft SDK package 

Make sure you have cmake 3.9 > version 

``` 
git clone https://github.com/microsoft/Azure-Kinect-Sensor-SDK.git
cd Azure-Kinect-Sensor-SDK
mkdir build && cd build
sudo apt install libsoundio-dev
cmake .. -GNinja
ninja
sudo ninja install
```

### Now configure Microsoft repository 

Important: Make sure you use the libk4a1.3 and libk4a1.3-dev version, and newer versions are not yet stable and might crash

``` 
curl -sSL https://packages.microsoft.com/keys/microsoft.asc | sudo apt-key add -
sudo apt-add-repository https://packages.microsoft.com/ubuntu/18.04/prod
sudo apt-get update
sudo apt install libk4a1.3
sudo apt install libk4a1.3-dev
```
NOTE: In other tutorials they download k4a-tools, nontheless it has an inbuilt version 1.4.1, therefore when you try running the code the system will crash as you have both 1.3 and 1.4 version. 
If you already did this, be sure to remove libk4a1.4, libk4a1.3-dev and k4a-tools and start again. 


### Test if the programm got set up correctly 
``` 
whereis k4aviewer
sudo k4aviewer
```

### Invoke k4aviewer without root, needed for ROS

Copy ‘scripts/99-k4a.rules’ into ‘/etc/udev/rules.d/’.
``` 
cd /etc/udev/rules.d/
sudo vi 99-k4a.rules
```
Now try calling without sudo 

``` 
k4aviewer
```
NOTE: If its not working disconnect and connect camera from the computer

#### Finally add the path to k4a 


