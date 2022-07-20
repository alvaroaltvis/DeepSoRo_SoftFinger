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
# start internal camera and video writer
internal_cam = cv2.VideoCapture(2, cv2.CAP_DSHOW)
vid_writer = imageio.get_writer(path.join(cwd, 'internal_vid.mp4'), fps=20)

# Initialize the Open3d visualizer
open3dVisualizer = Open3dVisualizer()
cv2.namedWindow('Depth Image', cv2.WINDOW_NORMAL)

# take series of captures and store images accordingly
def collect_data():
	for cap in range(num_captures):
		# Get kinect capture
		capture = device.update()
		# get internal camera capture and save image
		#captured, img = internal_cam.read()
		#img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
		#cv2.imwrite(path.join(images_folder, f'cam_img{cap}.png'), img)
		#vid_writer.append_data(img)

		# Get the color depth image from the capture
		ret, depth_image = capture.get_colored_depth_image()

		if not ret:
			continue

		# Get the 3D point cloud
		ret, points = capture.get_pointcloud()

		# live visualization
		open3dVisualizer(points)
		cv2.imshow('Depth Image', depth_image)

		# crop pointcloud to zoom in on area of interest (eg balloon)
		shape = o3d.geometry.PointCloud()
		shape.points = o3d.utility.Vector3dVector(points)
		shape = shape.crop(o3d.geometry.AxisAlignedBoundingBox(np.array([30, -400, 1]),
															   np.array([80, 200, 500])))

		# save cropped pointcloud for each capture
		filename = path.join(pcd_folder, f'pcd{cap}.ply')
		o3d.io.write_point_cloud(filename, shape, write_ascii=False, compressed=False, print_progress=False)
		o3d.visualization.draw_geometries([shape])
	# close internal camera video recorder
	vid_writer.close()

# write video of captured pointclouds
def create_pcd_video():
	pcd_vid_writer = imageio.get_writer(path.join(cwd, 'pcd_vid.mp4'), fps=20)
	for cap in range(num_captures):
		# access pointcloud
		filename = path.join(pcd_folder, f'pcd{cap}.ply')
		shape = o3d.io.read_point_cloud(filename)
		# visualize pointcloud
		vis = o3d.visualization.Visualizer()
		vis.create_window(width=800, height=800)
		vis.add_geometry(shape)
		# save image
		pcd_f = path.join(pcd_images_folder, f'img{cap}.png')
		vis.capture_screen_image(pcd_f, do_render=True)
		vis.destroy_window()
		# write image to video
		pcd_vid_writer.append_data(imageio.imread(pcd_f))
	# close video writer
	pcd_vid_writer.close()


collect_data()
create_pcd_video()
