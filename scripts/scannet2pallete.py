import argparse
import os
import numpy as np
import cv2
import json
import csv
from utils import nyu40_colour_code

def load_scannet_nyu40_mapping(path):
    mapping = {}
    with open(os.path.join(path, 'scannetv2-labels.combined.tsv')) as tsvfile:
        tsvreader = csv.reader(tsvfile, delimiter='\t')
        for i, line in enumerate(tsvreader):
            if i==0:
                continue
            scannet_id, nyu40id = int(line[0]), int(line[4])
            mapping[scannet_id] = nyu40id
    return mapping


parser = argparse.ArgumentParser(description="Run neural graphics primitives testbed with additional configuration & output options")

parser.add_argument("--scene_folder", type=str, default="")
args = parser.parse_args()
basedir = args.scene_folder

# frame_ids = os.listdir(os.path.join(basedir, 'color'))
# frame_ids = [int(os.path.splitext(frame)[0]) for frame in frame_ids]
# frame_ids =  sorted(frame_ids)

# os.makedirs(os.path.join(basedir, 'label'), exist_ok=True)
# os.makedirs(os.path.join(basedir, 'label_scaled'), exist_ok=True)
# label_mapping_nyu = load_scannet_nyu40_mapping(basedir)
# all_semantics = []
# for frame_id in frame_ids:
#     file_name_label = os.path.join(basedir, 'label-filt', '%d.png'% frame_id)
#     semantic = cv2.imread(file_name_label, cv2.IMREAD_UNCHANGED)
#     all_semantics.append(semantic)

# all_semantics = np.asarray(all_semantics)
# semantic_classes = []
# semantic_classes.append(0)
# for scan_id, nyu_id in label_mapping_nyu.items():
#     if scan_id in all_semantics:
#         semantic_classes.append(nyu_id)
# # each scene may not contain all 40-classes
# semantic_classes.sort()


semantic_classes = [0, 1, 2, 3, 3, 4, 6, 7, 7, 8, 8, 9, 12, 14, 15, 16, 18, 19, 22, 24, 25, 32, 33, 34, 38, 39, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40]
semantic_classes = np.unique(np.array(semantic_classes)).tolist()
num_semantic_class = len(semantic_classes)  # number of semantic classes
pallete = []
for i in range(num_semantic_class):
    pallete.append(nyu40_colour_code[semantic_classes[i]].tolist())

print("pallete of this scene:")
print(pallete)
print("semantic_classes")
print(semantic_classes)


semantic_json = {}
semantic_json["semantic_classes"] = semantic_classes
semantic_json["pallete"] = pallete

file_name = "pallete.json"
out_file = open(os.path.join(basedir, file_name), "w")
json.dump(semantic_json, out_file, indent = 4)
out_file.close()


