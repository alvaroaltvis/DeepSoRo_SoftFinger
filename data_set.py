import os, sys
import numpy as np
# import pymesh
import cv2
import multiprocessing as mp
from scipy.spatial.transform import Rotation as R
# from data_utils import *
from tqdm.contrib.concurrent import process_map
import open3d as o3d
from random import seed
from random import randint
from random import choices

print(dir(o3d))

DEBUG = False

class MAKE_DATASET():
    
    def __init__(self, sim_folder):
        # parameters
        OUTPUT_PREFIX = '/home/nuc/Desktop/kinect_camera/DATASET'

        # prepare path for file reading
        self.image_path = os.path.join(sim_folder, 'Images')
        self.pcd_path = os.path.join(sim_folder, 'PointCloud')
        
        # check file length
        self.simulation_length = len(os.listdir(self.image_path))
        print(self.simulation_length)

        if DEBUG:
            print('Loading Files ...')

        # load image and point cloud sequence files
        image_seq, pcd_seq = self.load_files()

        # image_seq = np.expand_dims(image_seq, axis=0)
        # pcd_seq = np.expand_dims(pcd_b_seq, axis=0)
        # com_coordinate_seq = np.expand_dims(com_coordinate_seq, axis=0)
        # rotated_com_translation_seq = np.expand_dims(rotated_com_translation_seq, axis=0)
        # com_rotation_seq = np.expand_dims(com_rotation_seq, axis=0)
        # idx_seq = np.expand_dims(idx_seq, axis=0)       

        print(f'IMG Dim: {np.shape(image_seq)}')
        print(f'PCD Dim: {np.shape(pcd_seq)}')
        # print(f'IDX Dim: {np.shape(idx_seq)}')
        # print(f'TRJ Dim: {np.shape(com_coordinate_seq)}')
        # print(f'TSL Dim: {np.shape(rotated_com_translation_seq)}')
        # print(f'ROT Dim: {np.shape(com_rotation_seq)}')

            
        # create output path 
        for i in range(101):
            self.output_path = os.path.join(OUTPUT_PREFIX, os.path.basename(sim_folder)+f'_{i}.npz')
            np.savez(self.output_path, img=image_seq[i], pcd=pcd_seq[i])
        
    def load_files(self):
        imgs_path = [os.path.join(self.image_path, f'{i}.jpg') for i in range(1, 102)] 
        pcds_path = [os.path.join(self.pcd_path, f'data_{i}.npz') for i in range(1, 102)]
        
        # container to store data
        img_seq = np.zeros((self.simulation_length, 1, 256, 256))
        pcd_seq = np.zeros((self.simulation_length, 6216, 3))
        
        for i in range(101):
            img_seq[i] = self.load_img_from_file_singlecam(imgs_path[i])
            pcd_seq[i] = self.load_pcd_from_file(pcds_path[i])
        return img_seq, pcd_seq
    
    def load_img_from_file_singlecam(self, filename, size=(256,256)):
        img_path_1 = filename
        # load the first image
        img_1 = cv2.imread(img_path_1, cv2.IMREAD_GRAYSCALE)
        img_1 = cv2.resize(img_1, size)
        return img_1

    def load_pcd_from_file(self, filename):
        #print(f'##### PROCRESS MESH FILE ##### Progress: {filename}')
        data = np.load(filename)
        # get vertices from mesh
        vertices = data['pcd']
        #print(len(vertices)) #-- Min point cloud is 6216 points 
        # if len(vertices) > 6216:
        extra_points=len(vertices) - 6216
        ran = range(0, len(vertices))
        eliminate=choices(ran, k=extra_points)
        vertices = np.delete(vertices, eliminate, 0)
        print(len(vertices))
        #return vertices

    
    #def resize all the pointclouds that are not the minimum size. 
    
def parallel_worker(sim_folder):
    # print('\n'+sim_folder)
    MAKE_DATASET(sim_folder)

    
if __name__ == '__main__':
    
    os.chdir(sys.path[0])
    
    DATA_PATH = '/home/nuc/Desktop/kinect_camera/DATA/'
    
    SIM_FOLDERS = []
    for dir in os.listdir(DATA_PATH):
        SIM_FOLDERS.append(os.path.abspath(os.path.join(DATA_PATH, dir)))

    process_map(parallel_worker, SIM_FOLDERS, max_workers=24)
    
#   extra_points=len(vertices) - 6216
#         random = []
#         for i in range(extra_points):
#             random.append(randint(0, len(vertices)-1))
#         vertices = np.delete(vertices, random, 0)
#         print(len(vertices)) 
