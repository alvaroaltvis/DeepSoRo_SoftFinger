import os, sys
from turtle import distance
import cv2
import numpy as np
import tkinter

#import pyKinectAzure library from folder
sys.path.insert(1, './pyKinectAzure')
import pykinect_azure as pykinect
from pykinect_azure.utils import Open3dVisualizer


class KINECT():

    def __init__(self):
        # initialize the library
        pykinect.initialize_libraries()
        # load camera configuration
        self.device_config = pykinect.default_configuration
        
    def set_camera_configuration(self, color_format='JPEG', color_resolution='720', depth_mode='WFOV'):
        # set color format
        if color_format == 'JPEG':
            self.device_config.color_format = pykinect.K4A_IMAGE_FORMAT_COLOR_MJPG
        elif color_format == 'BGRA':
            self.device_config.color_format = pykinect.K4A_IMAGE_FORMAT_COLOR_BGRA32
        else:
            print(f'[ERROR] Unknown Color Format: {color_format}')
            exit(-1)

        # set color resolution to 1080P
        if color_resolution == '720':
            self.device_config.color_resolution = pykinect.K4A_COLOR_RESOLUTION_720P
        elif color_resolution == '1080':
            self.device_config.color_resolution = pykinect.K4A_COLOR_RESOLUTION_1080P
        elif color_resolution == 'OFF':
            self.device_config.color_resolution = pykinect.K4A_COLOR_RESOLUTION_OFF
        else:
            print(f'[ERROR] Unknown Color Resolution: {color_resolution}')
            exit(-1)
        
        # set depth mode
        if depth_mode == 'NFOV':
            self.device_config.depth_mode = pykinect.K4A_DEPTH_MODE_NFOV_2X2BINNED
        elif depth_mode == 'WFOV':
            self.device_config.depth_mode = pykinect.K4A_DEPTH_MODE_WFOV_2X2BINNED
        elif depth_mode == 'OFF':
            self.device_config.depth_mode = pykinect.K4A_DEPTH_MODE_OFF
        else:
            print(f'[ERROR] Unknown Depth Mode: {depth_mode}')
            exit(-1)
    
        print(self.device_config)

        # start the device
        self.device = pykinect.start_device(config=self.device_config)

    def show_colorImage(self):
        self.set_camera_configuration(color_format='JPEG', color_resolution='1080', depth_mode='OFF')
        cv2.namedWindow('Color Image', cv2.WINDOW_NORMAL)
        while True:
            capture = self.device.update()
            ret, color_image = capture.get_color_image()
            if not ret: continue
            cv2.imshow("Color Image", color_image)
            # Press q key to stop
            if cv2.waitKey(1) == ord('q'): 
                break
    
    def show_depthImage(self):
        self.set_camera_configuration(color_format='JPEG', color_resolution='OFF', depth_mode='WFOV')
        cv2.namedWindow('Depth Image', cv2.WINDOW_NORMAL)
        while True:
            capture = self.device.update()
            ret, color_image = capture.get_colored_depth_image()
            if not ret: continue
            cv2.imshow("Depth Image", color_image)
            # Press q key to stop
            if cv2.waitKey(1) == ord('q'): 
                break

    def show_pointCloud(self):
        self.set_camera_configuration(color_format='JPEG', color_resolution='OFF', depth_mode='WFOV')
        open3dVisualizer = Open3dVisualizer()
        while True:
            capture = self.device.update()
            ret, points = capture.get_pointcloud()
            if not ret: continue
            open3dVisualizer(points)

    def show_colorPointCloud(self):
        self.set_camera_configuration(color_format='BGRA', color_resolution='720', depth_mode='WFOV')
        open3dVisualizer = Open3dVisualizer()
        cv2.namedWindow('Color Image',cv2.WINDOW_NORMAL)
        while True:
            capture = self.device.update()
            ret, points = capture.get_pointcloud()
            if not ret: continue
            ret, color_image = capture.get_transformed_color_image()
            if not ret: continue
            open3dVisualizer(points, color_image)
            cv2.imshow('Color Image', color_image)
            # Press q key to stop
            if cv2.waitKey(1) == ord('q'): 
                break

    def show_depth2Color(self):
        self.set_camera_configuration(color_format='BGRA', color_resolution='720', depth_mode='WFOV')
        cv2.namedWindow('Depth 2 Color',cv2.WINDOW_NORMAL)
        while True:
            capture = self.device.update()
            ret, color_image = capture.get_color_image()
            if not ret: continue
            ret, transformed_colored_depth_image = capture.get_transformed_colored_depth_image()
            if not ret: continue
            combined_image = cv2.addWeighted(color_image[:,:,:3], 0.7, transformed_colored_depth_image, 0.3, 0)
            cv2.imshow('Depth 2 Color', combined_image)
            # Press q key to stop
            if cv2.waitKey(1) == ord('q'): 
                break

    def show_color2Depth(self):
        self.set_camera_configuration(color_format='BGRA', color_resolution='720', depth_mode='WFOV')
        cv2.namedWindow('Color 2 Depth',cv2.WINDOW_NORMAL)
        while True:
            capture = self.device.update()
            ret, depth_image = capture.get_colored_depth_image()
            if not ret: continue
            ret, color_image = capture.get_transformed_color_image()
            if not ret: continue
            combined_image = cv2.addWeighted(color_image[:,:,:3], 0.7, depth_image, 0.3, 0)
            cv2.imshow('Color 2 Depth', combined_image)
            # Press q key to stop
            if cv2.waitKey(1) == ord('q'): 
                break


    def data_collection(self):
        self.set_camera_configuration(color_format='BGRA', color_resolution='720', depth_mode='WFOV')
        open3dVisualizer = Open3dVisualizer()
        cv2.namedWindow('Color Image',cv2.WINDOW_NORMAL)
        while True:
            capture = self.device.update()
            ret, points = capture.get_pointcloud()
            if not ret: continue
            ret, color_image = capture.get_transformed_color_image()
            if not ret: continue
            
            print(f'PointCloud: {np.shape(points)}')
            distance = np.linalg.norm(points, ord=2, axis=1)
            print(f'Distance: {np.shape(distance)}, AVG: {np.mean(distance)}, MIN: {np.min(distance)}, MAX: {np.max(distance)}')
            
            filter_index = distance < 700
            print(f'Selected PointCloud: {np.sum(filter_index)}')
            
            open3dVisualizer(points[filter_index], color_image)
            
            cv2.imshow('Color Image', color_image)
            # Press q key to stop
            if cv2.waitKey(1) == ord('q'): 
                break
    
    

if __name__ == "__main__":

    # change working directory
    os.chdir(sys.path[0])

    # class instance
    kinect = KINECT()
    # kinect.show_colorImage()
    # kinect.show_depthImage()
    # kinect.show_pointCloud()
    # kinect.show_colorPointCloud()
    # kinect.show_depth2Color()
    # kinect.show_color2Depth()


    kinect.data_collection()
    
