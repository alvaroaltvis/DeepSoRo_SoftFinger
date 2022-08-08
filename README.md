# DeepSoRo_SoftFinger

## Soft Robotics

Soft robotics is a subfield in robotics that specializes in the building and controlling of bodies with flexible and deformable materials instead of traditional rigid links. The compliant materials allow the robot to change shape either passively or actively and provide a high degree of sensitivity to external factors. This allows soft robots to perform tasks like grasping and manipulating irregular surfaces in a safer and more effective way than traditional rigid robotics. Nonetheless, due to its multidimensional deformation capabilities, proprioceptive sensing has proven to be a great challenge, and very few methods have provided reliable 3D representation using embedded sensors. 

## Primary Objective of DeepSoRo_SoftFinger

The primary objective of this research project is to develop a soft robot finger that enables 3D shape reconstruction and force estimation using vision-based proprioception and deep learning models. The ultimate goal is to employ soft finger grippers to pick, handle, and sense fragile objects that would be challenging for conventional rigid grippers. The soft finger was designed with a constraint layer that permits the soft finger to extend along a particular curve when powered by pneumatic actuation. In addition, a data-gathering system was designed to collect training data for neural network models. The system consists of an RGB camera that captures the interior image of the soft finger, which contains bumps in a specific pattern, and two RGBD cameras that collect the external shape/geometry information of the soft finger. The deformation of the embedded bumps combined with the data from the RGBD camera will allow the convolution neural network to assimilate internal deformations with specific 3D shapes and angles. This correlation will allow the neural network to estimate the 3D shape and angle of the soft finger under arbitrary deformations based solely on the embedded images.

This research project is a collaborative effort with AI4CE lab at NYU Tandon School of Engineering. 

## How to use repository 

### CAD Files 
 
The STL files can be found under CAD_Soft_Robot, for the exception of the Exoskeleton file as it's too large to be in an STL format. The materials used to build them are described in the Readme under CAD files. 

### PointCloud 

The code needed to take two pointclouds from different Azure SDK Cameras and combine them into one same cloud can be found under pointclouds. The description of each of them can be found in the Readme folder. 

### PWM and TimeLaps 

This folder contains the code to send one or two PWM signals from a raspberry pi to power the pneumatic pump at different percentages, and therefore achive a controlled inflation and deflation with different deformations. It also includes the commands to take an image during the inflation process with the raspberry pi fish eye camera. The description of each of them can be found in the Readme folder. 

### Make Data 

The make_dataset remotly access the embedded images taken with the raspberry pi and copies them to a specific folder in the local computer. Then the script combines the embedded images with their respective pointclouds, so that they can be later processed by the machine learning algorithm from DeepSoRo. 
