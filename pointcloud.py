

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
            if (36 <= color[0]) and (color[0] >= 70) and (25 <= color[1]) and (color[1] >= 255) and (25 <= color[2]) and (color[2] >= 255):
                new_index.append(index_count)

        #Delete the green color pixel 
        for index in new_index:
            colors = np.delete(colors, index, 0)
            points = np.delete(points, index, 0) 
    
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

