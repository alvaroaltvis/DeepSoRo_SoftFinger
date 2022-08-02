## Point Clouds 

### Three main scripts 

#### Combined_pointcloud 

Combined_pointcloud activates both of the azure kinect cameras that are pointing at the soft finger at 90° angle, sets the configuration of the cameras, takes an image at the same time. Then it process the pointcloud, it filters the points froma specific threashold (in mm), it downsizes the pointcloud with a voxel size. Then it combines both pointclouds to get a calibrated merged single pointcloud, it crops the pointcloud with the respective measurments, (given in mm) and returns a combined croped pointcloud. 

#### Kinect_Camera_synconeP

Kinect_Camera_synconeP follows a similar process from combined_pointcloud, but it also sends signal to the raspberry pi in between pointcloud captures. This signales are passed with parameters that are defined as input on each experimental run. Those parameters define the name of the images, the power of the pneumatic pump and the name of the folder where the raspberry pi fisheye camera images are stored. This script also returns a croped and calibrated pointcloud of the soft finger at a varbiale amount of power. 


#### Kinect_Camera_synctwoC

Kinect_Camera_synctwoC follows alsmot the exact same process as Kinect_Camera_synconeP, with the calibrated pointcloud and the informaiton to the raspberry pi, nontheless this script doesn't end the first signal of power of the raspberry pi until after the pointcloud images are taken. This allows for more reliable results if there was to be an air leakage in the soft body. 

### Rest of scripts 

PointcloudGreenScreen filters all the green points from the pointcloud, in case of using a green screen. Although the RGB parametes still need adjustment. 
Pointcloud_boxDepth filters all the points after a threashold. 
pointcloud_boxLeft and pointcloud_boxRight filter pints with two vertices of a rectangle, from different real world camera possitions. At around 45° angle from the front of the object. 


#### Note: All distance measurments are in mm 
