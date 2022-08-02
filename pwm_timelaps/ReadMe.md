# PWM and Images

### PWM Latest 

This script sends out a PWM signal to the raspberry pi to determine the amount of power coming out of the pneumatic pump. This process goes on for one second. Then it takes three consecutive images using the raspberry pi embedded fish eye camera. And finally, it opens a valve and releases the air. 

### PWM OneP and PWM TwoC

As you can see, the names have similarities with the PointCloud scripts because each pointcloud script calls the specific PWM script with the same name. This is a more advanced script than the one before. It takes in parameters from the PointCloud script and runs the code remotely. It inflates the soft finger, takes an image, and then opens a valve to deflate. 
The difference between PWM OneP and PWM TwoC is that OneP inflates the soft finger for one second and then takes the embedded image, while PWM Two C keeps inflating as it takes the embedded image. 

All the images are saved in a specific file that was created with the name given as a parameter by the PointCloud script. 

