import copy
import json
import numpy as np


ngp2scan = np.array([[0,1,0,0],[0,0,1,0],[1,0,0,0],[0,0,0,1]])

with open("transforms_train_10.json", "rb") as f:
    transforms = json.load(f)

selected_transforms = copy.deepcopy(transforms)
selected_transforms.pop('frames')
selected_transforms['frames'] = []
selected_transforms['aabb_scale'] = 4

positions = []

for frame_idx in range(len(transforms['frames'])):
    if (frame_idx % 5 == 0):
        transformed_w2c = np.array(transforms['frames'][frame_idx]["transform_matrix"])
        transformed_w2c =  ngp2scan @ transformed_w2c
        transforms['frames'][frame_idx]["transform_matrix"] =  transformed_w2c.tolist()
        selected_transforms['frames'].append(transforms['frames'][frame_idx])

with open("transforms_train_50_modified.json", "w") as f:
    json.dump(obj=selected_transforms, fp=f)