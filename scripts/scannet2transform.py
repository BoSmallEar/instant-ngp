 
import json
import argparse
import os
import numpy as np
import cv2
import copy

parser = argparse.ArgumentParser(description="Run neural graphics primitives testbed with additional configuration & output options")

parser.add_argument("--scene_folder", type=str, default="")
args = parser.parse_args()
basedir = args.scene_folder
step = 1

frame_ids = os.listdir(os.path.join(basedir, 'color'))
frame_ids = [int(os.path.splitext(frame)[0]) for frame in frame_ids]
frame_ids =  sorted(frame_ids)

imgs = []
poses = []

W = 320
H = 240
K = np.asarray([
[1169.621094, 0, 646.295044],
[0,  1167.105103, 489.927032],
[0, 0, 1]])
focal = 1168.
scale = 240. / 972.



focal = focal * scale

K[1,2] += 2 # we add c_y by 2 since we pad the height by 4 pixels
K[0, 0] = K[0, 0]*scale # fx
K[1, 1] = K[1, 1]*scale # fy
K[0, 2] = K[0, 2]*scale  # cx
K[1, 2] = K[1, 2]*scale  # cy



train_ids = frame_ids[::step]
test_ids = [x+ (step//2) for x in train_ids]
test_id_step = 10
test_ids = test_ids[::test_id_step]  # only use 10% of the test frames to speed up inference   

print(f"total number of training frames: {len(train_ids)}")
print(f"total number of testing frames: {len(test_ids)}")

os.makedirs(os.path.join(basedir, 'color_scaled'), exist_ok=True)


all_imgs = []
all_poses = []
counts = []
for ids in (train_ids, test_ids):
    imgs = []
    poses = []
    transform_json = {}
    tran
    transform_json["fl_x"] = K[0, 0]
    transform_json["fl_y"] = K[1, 1]
    transform_json["cx"] = K[0, 2]
    transform_json["cy"] = K[1, 2]
    transform_json["w"] = W
    transform_json["h"] = H
    transform_json["camera_angle_x"] = np.arctan2(W/2,K[0, 0]) * 2
    transform_json["camera_angle_y"] = np.arctan2(H/2,K[1, 1]) * 2
    transform_json["aabb_scale"] = 16
    transform_json["scale"] = 1
    transform_json["offset"] = [0., 0., 0.]
    transform_json["frames"] = []
    for frame_id in ids:
        pose = np.loadtxt(os.path.join(basedir, 'pose', '%d.txt' % frame_id))
        pose = pose.reshape((4, 4))
        file_name_image = os.path.join(basedir, 'color', '%d.jpg'% frame_id)
        image = cv2.imread(file_name_image)[:,:,::-1] # change from BGR uinit 8 to RGB float
        image = cv2.copyMakeBorder(src=image, top=2, bottom=2, left=0, right=0, borderType=cv2.BORDER_CONSTANT, value=[0,0,0]) # pad 4 pixels to height so that images have aspect ratio of 4:3
        assert image.shape[0] * 4==3 * image.shape[1] 
        image = image/255.0
        image = cv2.resize(image, (W, H), interpolation=cv2.INTER_LINEAR)
        
        json_image_dict ={}
        json_image_dict["file_path"] = os.path.join('color_scaled', '%d.jpg'% frame_id)
        json_image_dict["transform_matrix"] = pose.tolist()
        image_save = cv2.cvtColor(image.astype(np.float32), cv2.COLOR_BGR2RGB)
        image_save = image_save * 255.0
        cv2.imwrite(os.path.join(basedir, 'color_scaled', '%d.jpg'% frame_id), image_save)

        poses.append(pose)
        imgs.append(image)
        transform_json["frames"].append(json_image_dict)
    if ids == train_ids:
        file_name =  'transforms_train.json'
    else:
        file_name = 'transforms_test.json'
    out_file = open(os.path.join(basedir, file_name), "w")
    json.dump(transform_json, out_file, indent = 4)
    out_file.close()
 
  
 