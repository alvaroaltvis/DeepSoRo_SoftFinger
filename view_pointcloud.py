import open3d as o3d
import os
import numpy as np
from matplotlib import pyplot as plt
import imageio.v2 as imageio


dpoints = np.load(f"/home/nuc/Desktop/kinect_camera/prototype_finger2/prototype.npy")
shape_edit = o3d.geometry.PointCloud()
shape_edit.points = o3d.utility.Vector3dVector(dpoints)
o3d.visualization.draw_geometries([shape_edit])
