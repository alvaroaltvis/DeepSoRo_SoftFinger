import numpy as np
from matplotlib import pyplot as plt
from mpl_toolkits import mplot3d  # noqa: F401
import time, os, sys
import pyk4a
from pyk4a import Config, PyK4A

np.set_printoptions(threshold=np.inf)
class CAPTURE_DATA: 

    def __init__(self) -> None:
        
        self.k4a = PyK4A(
        Config(
            color_resolution=pyk4a.ColorResolution.RES_720P,
            camera_fps=pyk4a.FPS.FPS_5,
            depth_mode=pyk4a.DepthMode.NFOV_2X2BINNED,
            synchronized_images_only=True,
        ))

        self.k4a.start()

    def capture(self):
        
        # getters and setters directly get and set on device
        self.k4a.whitebalance = 4500
        assert self.k4a.whitebalance == 4500
        self.k4a.whitebalance = 4510
        assert self.k4a.whitebalance == 4510
        while True:
            capture = self.k4a.get_capture()
            if np.any(capture.depth) and np.any(capture.color):
                break
        points = capture.depth_point_cloud.reshape((-1, 3))
        colors = capture.transformed_color[..., (2, 1, 0)].reshape((-1, 3))
        #Iterate through each color RGB, look at parameters and get index for green 
        new_index = []
        index_count = -1
        for color in colors:
            index_count += 1
            if (1 <= color[1]) and (255 >= color[1]): # Edit this values to get better results color[0] R color [1] G color [2] Blue, Range 0 - 255
                new_index.append(index_count)
        #print(new_index)
        rows, columns = colors.shape
        #print(rows)

        # Delete the green color pixel 
        colors = np.delete(colors, new_index, 0)
        points = np.delete(points, new_index, 0) 
        return points, colors

def main():

    # create class instant
    camera = CAPTURE_DATA()

    # capture data
    points, colors = camera.capture()

    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(111, projection='3d')

    ax.scatter(points[:, 0],points[:, 1],points[:, 2],s=1, c=colors / 255)

    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_zlabel("z")   

    plt.show()
    plt.savefig('1.png') 


if __name__ == "__main__":
    os.chdir(sys.path[0])
    main()


# if (color[0]=124 and color[1]=252 and color[2]=0) or (color[0]=127 and color[1]=255 and color[2]=0) or (color[0]=50 and color[1]=205 and color[2]=50) or (color[0]=0 and color[1]=255 and color[2]=0) or (color[0]=34 and color[1]=139 and color[2]=34) or (color[0]=0 and color[1]=128 and color[2]=0) or (color[0]=0 and color[1]=100 and color[2]=0) or (color[0]=173 and color[1]=255 and color[2]=47) or (color[0]=154 and color[1]=205 and color[2]=50) or (color[0]=0 and color[1]=255 and color[2]=154) or (color[0]=144 and color[1]=238 and color[2]=144) or (color[0]=152 and color[1]=251 and color[2]=152) or (color[0]=143 and color[1]=188 and color[2]=143) or (color[0]=60 and color[1]=179 and color[2]=113) or (color[0]=32 and color[1]=178 and color[2]=170) or (color[0]=46 and color[1]=139 and color[2]=87) or (color[0]=128 and color[1]=128 and color[2]=0) or (color[0]=85 and color[1]=107 and color[2]=47) or (color[0]=85 and color[1]=107 and color[2]=47) or (color[0]=107 and color[1]=142 and color[2]=35):
