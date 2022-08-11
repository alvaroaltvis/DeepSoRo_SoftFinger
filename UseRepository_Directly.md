# Use Code to collect data 
This file describes how to use the code writen above step by step for the specific experimental setup set at AI4CE Lab, nontheless it can be replicated if followed carefully. 

### RaspberryPi
If the experiemntal setup is used as it is in the AI4CE lab, the raspberrypi already contains the scripts needed. If not, please use the pwm_OneP.py script to activate the pump, take an embedded image and open the valvue to deflate.

### Collect Embedded images and pointclouds 
First run crop_pointcloud.py, to make sure the object is well represented in the pointcloud and that there isn't extra or less points than needed. You need to connect only one camera when running tests. You can edit this by changing the dimentions of shape.crop. The dimmentions are in mm and they represent the two opporiste vertices of a rectangle. First is right/left, then up/down and then backa dn forward. This generates a rectangle that eliminates everything around it. 

For the first step, use kinect_camera_synconeP.py to choose the best transformation matrix for the pointcloud combination. It will take an embedded image and pointcloud. When the code runs, it will ask you for two inputs. Place the name of the folder and the number of repetitions you need. 
You can uncomment self.draw_registration_result to see how well the pointclouds got comgined. Store the transformation matrix for the best pointclouds. 

Once you have the transformation matrix that generates the best combined pointcloud, use pointcloudOneP_fixed.py and change the transformation matrix in reg_p2p to the one you chose. Run that code and place the number of repetitions you want your dataset to have and the name of the folder to store them. 

You can start with a small batch and verify the pointclouds are correct with view_pointcloud.py. 

### Import embedded images from Raspi and Create DATASET 
make_dataset.py is the following step. This script contains many things that need to be changed, depending on the size of the data and name, therefore follow the comments on the script to make sure it works properly.
It will ask you to input the name of the folder where the images are coming from (it is important its the same name you place in the last script).

### Upload the Dataset to the server and continue DeepSoRo_Plus process to create and train a model 
