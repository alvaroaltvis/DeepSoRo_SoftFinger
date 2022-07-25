import os, sys
import cv2
import numpy as np
import open3d as o3d
import copy
import time
import subprocess

# import pyKinectAzure library from folder
sys.path.insert(1, './pyKinectAzure')
import pykinect_azure as pykinect
from pykinect_azure.utils import Open3dVisualizer


class KINECT():

    def __init__(self):
        # initialize the library
        pykinect.initialize_libraries()
        # load camera configuration
        self.device_config = pykinect.default_configuration
        # container for kinect device
        self.device = []
        
    def set_camera_configuration(self, device_index=0,
                                        color_format='JPEG',
                                        color_resolution='720',
                                        depth_mode='WFOV',
                                        camera_fps='30FPS',
                                        synchronized_images_only=False,
                                        depth_delay_off_color_usec=0,
                                        sync_mode='Standalone',
                                        subordinate_delay_off_master_usec=0):
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

        # camera fps
        if camera_fps == '5FPS':
            self.device_config.camera_fps = pykinect.K4A_FRAMES_PER_SECOND_5
        elif camera_fps == '15FPS':
            self.device_config.camera_fps = pykinect.K4A_FRAMES_PER_SECOND_15
        elif camera_fps == '30FPS':
            self.device_config.camera_fps = pykinect.K4A_FRAMES_PER_SECOND_30

        # synchronized_images_only
        self.device_config.synchronized_images_only = synchronized_images_only

        # depth_delay_off_color_usec
        self.device_config.depth_delay_off_color_usec = depth_delay_off_color_usec

        # wire sync mode
        if sync_mode == 'Standalone':
            self.device_config.wired_sync_mode = pykinect.K4A_WIRED_SYNC_MODE_STANDALONE
        elif sync_mode == 'Master':
            self.device_config.wired_sync_mode = pykinect.K4A_WIRED_SYNC_MODE_STANDALONE
        if sync_mode == 'Subordinate':
            self.device_config.wired_sync_mode = pykinect.K4A_WIRED_SYNC_MODE_STANDALONE

        # subordinate_delay_off_master_usec
        self.device_config.subordinate_delay_off_master_usec = subordinate_delay_off_master_usec

        print(self.device_config)
        # start the device
        self.device.append(pykinect.start_device(device_index=device_index, config=self.device_config))

    def sync_capture_config(self):
        # configure the left camera
        self.set_camera_configuration(device_index=0,
                                        color_format='BGRA',
                                        color_resolution='720',
                                        depth_mode='WFOV',
                                        camera_fps='30FPS',
                                        synchronized_images_only=False,
                                        depth_delay_off_color_usec=0,
                                        sync_mode='Standalone',
                                        subordinate_delay_off_master_usec=0)

        # configure the right camera
        self.set_camera_configuration(device_index=1,
                                        color_format='BGRA',
                                        color_resolution='720',
                                        depth_mode='WFOV',
                                        camera_fps='30FPS',
                                        synchronized_images_only=False,
                                        depth_delay_off_color_usec=0,
                                        sync_mode='Standalone',
                                        subordinate_delay_off_master_usec=0)
    
    def capture_colorPCD(self, device_index):
        while True:
            # perform capture
            capture = self.device[device_index].update()
            # capture point cloud
            ret, points = capture.get_pointcloud()
            if not ret: continue
            ret, color_image = capture.get_transformed_color_image()
            if not ret: continue
            # print(f'Capturing COLOR_PCD ...')
            
            return points, color_image

    def distance_filter(self, point_cloud, distance_threshold):

        distance = np.linalg.norm(point_cloud, ord=2, axis=1)
        filter_index = distance < distance_threshold

        return point_cloud[filter_index]

    def draw_registration_result(self, source, target, transformation):
        source_temp = copy.deepcopy(source)
        target_temp = copy.deepcopy(target)
        source_temp.paint_uniform_color([1, 0.706, 0])
        target_temp.paint_uniform_color([0, 0.651, 0.929])
        source_temp.transform(transformation)
        o3d.visualization.draw_geometries([source_temp, target_temp],
                                        zoom=0.4559,
                                        front=[0.6452, -0.3036, -0.7011],
                                        lookat=[1.9892, 2.0208, 1.8945],
                                        up=[-0.2779, -0.9482, 0.1556])

    def preprocess_point_cloud(self, pcd, voxel_size):
        print(":: Downsample with a voxel size %.3f." % voxel_size)
        pcd_down = pcd.voxel_down_sample(voxel_size)

        radius_normal = voxel_size * 2
        print(":: Estimate normal with search radius %.3f." % radius_normal)
        pcd_down.estimate_normals(
            o3d.geometry.KDTreeSearchParamHybrid(radius=radius_normal, max_nn=30))

        radius_feature = voxel_size * 5
        print(":: Compute FPFH feature with search radius %.3f." % radius_feature)
        pcd_fpfh = o3d.pipelines.registration.compute_fpfh_feature(
            pcd_down,
            o3d.geometry.KDTreeSearchParamHybrid(radius=radius_feature, max_nn=100))
        return pcd_down, pcd_fpfh

    def execute_fast_global_registration(self, source_down, target_down, source_fpfh,
                                     target_fpfh, voxel_size):

        distance_threshold = voxel_size * 0.5
        print(":: Apply fast global registration with distance threshold %.3f" \
                % distance_threshold)
        result = o3d.pipelines.registration.registration_fgr_based_on_feature_matching(
        source_down, target_down, source_fpfh, target_fpfh,
        o3d.pipelines.registration.FastGlobalRegistrationOption(
            maximum_correspondence_distance=distance_threshold))
        return result



    def sync_capture(self):

        # configure the sync cameras
        self.sync_capture_config()
        # show number of device
        print(self.device)

        #open3dVisualizer_left = Open3dVisualizer()
        #open3dVisualizer_right = Open3dVisualizer()

        # while True:
        for i in range(1):
            # Code to connect to raspi and power the actuation mechanism
            subprocess.run(["ssh","raspberrypi@192.168.1.2","python3 /home/raspberrypi/Desktop/New_code/pwm_one.py --name remotecontrol --power 40"], capture_output=True)
            # capture using the left camera
            pt_left, img_left = self.capture_colorPCD(device_index=0)
            # capture using the right camera
            pt_right, img_right = self.capture_colorPCD(device_index=1)
            # Code to connect to raspi and powerdown the finger 
            subprocess.run(["ssh","raspberrypi@192.168.1.2","python3 /home/raspberrypi/Desktop/New_code/pwm_one.py --power 0"], capture_output=True)

            print(f'LEFT  PCD: {np.shape(pt_left)}, LEFT  IMG: {np.shape(img_left)}')
            print(f'RIGHT PCD: {np.shape(pt_right)}, RIGHT IMG: {np.shape(img_right)}')
            
            # use distance filter
            distance_threshold = 700
            pt_left = self.distance_filter(pt_left, distance_threshold)
            pt_right = self.distance_filter(pt_right, distance_threshold)
            
            # open3dVisualizer_left(pt_left, img_left)
            # open3dVisualizer_right(pt_right, img_right)

            pcd_left = o3d.geometry.PointCloud()
            pcd_left.points = o3d.utility.Vector3dVector(pt_left)
            pcd_right = o3d.geometry.PointCloud()
            pcd_right.points = o3d.utility.Vector3dVector(pt_right)

            # self.draw_registration_result(pcd_left, pcd_right, np.identity(4))

            voxel_size = 10
            left_down, left_fpfh = self.preprocess_point_cloud(pcd_left, voxel_size)
            right_down, right_fpfh = self.preprocess_point_cloud(pcd_right, voxel_size)

            print(f'Downsampled PCD: {np.shape(left_down.points)}')

            # fast global registration
            start = time.time()
            result_fast = self.execute_fast_global_registration(left_down, right_down,
                                                                left_fpfh, right_fpfh,
                                                                voxel_size)

            print("Fast global registration took %.3f sec.\n" % (time.time() - start))
            print(result_fast)
            print(result_fast.transformation)
            self.draw_registration_result(left_down, right_down, result_fast.transformation)


            # ICP
            print("\n\nApply point-to-point ICP")
            threshold = 12
            trans_init = result_fast.transformation
            start = time.time()
            reg_p2p = o3d.pipelines.registration.registration_icp(
                left_down, right_down, threshold, trans_init,
                o3d.pipelines.registration.TransformationEstimationPointToPoint(),
                o3d.pipelines.registration.ICPConvergenceCriteria(max_iteration=5000))
            print("ICP registration took %.3f sec.\n" % (time.time() - start))
            print(reg_p2p)
            print(f"Transformation is:\n {reg_p2p.transformation}")
            pcd_left_crop = pcd_left.crop(o3d.geometry.AxisAlignedBoundingBox(np.array([-200, -400, 1]),
															   np.array([0, 200, 320])))
            pcd_right_crop = pcd_right.crop(o3d.geometry.AxisAlignedBoundingBox(np.array([0, -400, 1]),
															   np.array([80, 200, 500])))
            self.draw_registration_result(left_down, right_down, reg_p2p.transformation)
            self.draw_registration_result(pcd_left_crop, pcd_right_crop, reg_p2p.transformation)
            open3dVisualizer_left(pcd_left.points, img_left)


            



    

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
    kinect.sync_capture()
    
