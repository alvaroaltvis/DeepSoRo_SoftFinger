import sys
import cv2
import open3d as o3d
from os import listdir, getcwd, path
import numpy as np
import time
import imageio.v2 as imageio

sys.path.insert(1, '../')
import pykinect_azure as pykinect
from pykinect_azure.utils import Open3dVisualizer

num_captures = 1 # number of image captures (~.2s per capture)
cwd = getcwd()
pcd_folder = path.join(cwd, 'PCD Files')
pcd_images_folder = path.join(cwd, 'PCD Image Files')
images_folder = path.join(cwd, 'Internal Image Files')

# Initialize the library, if the library is not found, add the library path as argument
pykinect.initialize_libraries()

# Modify camera configuration
device_config = pykinect.default_configuration
device_config.color_resolution = pykinect.K4A_COLOR_RESOLUTION_OFF
device_config.depth_mode = pykinect.K4A_DEPTH_MODE_NFOV_2X2BINNED

# Start kinect
device = pykinect.start_device(config=device_config)

# Initialize the Open3d visualizer
open3dVisualizer = Open3dVisualizer()
cv2.namedWindow('Depth Image', cv2.WINDOW_NORMAL)

# take series of captures and store images accordingly
def collect_data():
	for cap in range(num_captures):
		# Get kinect capture
		capture = device.update()

		# Get the color depth image from the capture
		ret, depth_image = capture.get_colored_depth_image()

		if not ret:
			continue

		# Get the 3D point cloud
		ret, points = capture.get_pointcloud()

		# live visualization
		open3dVisualizer(points)
		cv2.imshow('Depth Image', depth_image)

		# crop pointcloud to zoom in on area of interest
		shape = o3d.geometry.PointCloud()
		shape.points = o3d.utility.Vector3dVector(points)
		shape = shape.crop(o3d.geometry.AxisAlignedBoundingBox(np.array([10, -50, 1]),  # Left hand side Camera 
															   np.array([80, 150, 500])))

		# shape = shape.crop(o3d.geometry.AxisAlignedBoundingBox(np.array([-500, 70, 1]),  # Right hand side camera 
		# 													   np.array([500, 250, 300])))  

		# save cropped pointcloud for each capture
		filename = path.join(pcd_folder, f'pcdR{cap}.ply')
		o3d.io.write_point_cloud(filename, shape, write_ascii=False, compressed=False, print_progress=False)
		o3d.visualization.draw_geometries([shape])

# Acces and save pointcloud 
def create_pcd():
	for cap in range(num_captures):
		# access pointcloud
		filename = path.join(pcd_folder, f'pcdR{cap}.ply')
		shape = o3d.io.read_point_cloud(filename)
		points = np.array(shape.points)
		print(points)
		# visualize pointcloud
		vis = o3d.visualization.Visualizer()
		vis.create_window(width=800, height=800)
		vis.add_geometry(shape)
		# save image
		pcd_f = path.join(pcd_images_folder, f'imgR{cap}.png')
		vis.capture_screen_image(pcd_f, do_render=True)
		vis.destroy_window()


collect_data()
create_pcd()
