## Point Clouds 

### Three main scripts 

#### Combined_pointcloud 

Combined_pointcloud activates both of the azure Kinect cameras that are pointing at the soft finger at 90° angle, sets the configuration of the cameras, takes an image simultaneously. Then it processes the pointclouds, filters the points from a specific threshold (in mm), it downsizes the pointclouds with a voxel size. Then it combines both pointcloud to get a calibrated merged single pointcloud, it crops the pointcloud with the respective measurments, (given in mm) and returns a combined cropped pointcloud. 

#### Kinect_Camera_synconeP

Kinect_Camera_synconeP follows a similar process from combined_pointcloud, it also sends a signal to the raspberry pi between pointcloud captures. These signales are passed with parameters that are defined as input on each experimental run. Those parameters define the name of the images, the power of the pneumatic pump, and the name of the folder where the raspberry pi fisheye camera images are stored. This script also returns a cropped and calibrated pointcloud of the soft finger at a variable amount of power. 


#### Kinect_Camera_synctwoC

Kinect_Camera_synctwoC follows almost the same process as Kinect_Camera_synconeP, with the calibrated pointcloud and the information to the raspberry pi, nonetheless this script doesn't end the first signal of power of the raspberry pi until after the pointcloud images are taken. This allows for more reliable results if there is to be an air leakage in the soft body. 

#### pointcloudOneP_fixed 

PointcloudOneP_fixed follows almost the same process as Kinect_Camera_synconeP, nonetheless, instead of calibrating the two pointcloud with a new transformation matrix each time, the best transformation matrix for the experiment was hardcoded and used to combine all the future pointclouds, generating more accurate results, but with a very specific experimental setup. 

### Rest of scripts 

PointcloudGreenScreen filters all the green points from the pointcloud, in case of using a green screen. Although the RGB parameters still need adjustment. 
Pointcloud_boxDepth filters all the points after a threshold. 
pointcloud_boxLeft and pointcloud_boxRight filter pints with two vertices of a rectangle from different real-world camera positions. At around 45° angle from the front of the object. 


#### Note: All distance measurements are in mm 
