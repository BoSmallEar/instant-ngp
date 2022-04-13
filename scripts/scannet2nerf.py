import copy
import json
import numpy as np
import os

def rotmat(a, b):
	a, b = a / np.linalg.norm(a), b / np.linalg.norm(b)
	v = np.cross(a, b)
	c = np.dot(a, b)
	s = np.linalg.norm(v)
	kmat = np.array([[0, -v[2], v[1]], [v[2], 0, -v[0]], [-v[1], v[0], 0]])
	return np.eye(3) + kmat + kmat.dot(kmat) * ((1 - c) / (s ** 2 + 1e-10))

def closest_point_2_lines(oa, da, ob, db): # returns point closest to both rays of form o+t*d, and a weight factor that goes to 0 if the lines are parallel
	da = da / np.linalg.norm(da)
	db = db / np.linalg.norm(db)
	c = np.cross(da, db)
	denom = np.linalg.norm(c)**2
	t = ob - oa
	ta = np.linalg.det([t, db, c]) / (denom + 1e-10)
	tb = np.linalg.det([t, da, c]) / (denom + 1e-10)
	if ta > 0:
		ta = 0
	if tb > 0:
		tb = 0
	return (oa+ta*da+ob+tb*db) * 0.5, denom

scannet_folder = "/home/harmony_asl/instant_ngp_scannet/scene0000_00"
json_for_frame_selection = (
	"/home/harmony_asl/instant_ngp_scannet/scene0000_00/"
	"transforms_train.json")

# Select the frames from the json. This are the frames of which we want to find
# the actual transform.
c2ws = []
frame_names = []
with open(json_for_frame_selection, "r") as f:
    transforms = json.load(f)
# - Get filenames and concurrently load the c2w.
for frame_idx, frame in enumerate(transforms['frames']):
	if (frame_idx % 50 == 0):
		frame_name = os.path.basename(frame['file_path']).split('.jpg')[0]
		pose_name =	os.path.join(scannet_folder, f"pose/{frame_name}.txt")
		frame_names.append(frame_name)
		c2w = np.loadtxt(pose_name)
		c2ws.append(c2w)

selected_transforms = copy.deepcopy(transforms)
selected_transforms.pop('frames')
selected_transforms['frames'] = []



up = np.zeros(3)
for c2w_idx in range(len(c2ws)):
	c2ws[c2w_idx][0:3,2] *= -1 # flip the y and z axis
	c2ws[c2w_idx][0:3,1] *= -1
	c2ws[c2w_idx] = c2ws[c2w_idx][[1,0,2,3],:] # swap y and z
	c2ws[c2w_idx][2,:] *= -1 # flip whole world upside down

	up += c2ws[c2w_idx][0:3,1]

nframes = len(c2ws)
up = up / np.linalg.norm(up)
print("up vector was", up)
R = rotmat(up,[0,0,1]) # rotate up vector to [0,0,1]
R = np.pad(R,[0,1])
R[-1, -1] = 1

for c2w_idx in range(len(c2ws)):
	c2ws[c2w_idx] = np.matmul(R, c2ws[c2w_idx]) # rotate up to be the z axis

# find a central point they are all looking at
print("computing center of attention...")
totw = 0.0
totp = np.array([0.0, 0.0, 0.0])
for c2w_idx_1 in range(len(c2ws)):
	mf = c2ws[c2w_idx_1][0:3,:]
	for c2w_idx_2 in range(len(c2ws)):
		mg = c2ws[c2w_idx_2][0:3,:]
		p, w = closest_point_2_lines(mf[:,3], mf[:,2], mg[:,3], mg[:,2])
		if w > 0.01:
			totp += p*w
			totw += w
totp /= totw
print(totp) # the cameras are looking at totp
for c2w_idx in range(len(c2ws)):
	c2ws[c2w_idx][0:3,3] -= totp

avglen = 0.
for c2w_idx in range(len(c2ws)):
	avglen += np.linalg.norm(c2ws[c2w_idx][0:3,3])
avglen /= nframes
print("avg camera distance from origin", avglen)
for c2w_idx in range(len(c2ws)):
	c2ws[c2w_idx][0:3,3] *= 4.0 / avglen # scale to "nerf sized"

curr_frame_name_idx = 0
for frame_idx in range(len(transforms['frames'])):
	if (curr_frame_name_idx == len(frame_names)):
		break
	frame = transforms['frames'][frame_idx]
	frame_name = os.path.basename(frame['file_path']).split('.jpg')[0]
	if (frame_name == frame_names[curr_frame_name_idx]):	
		c2w = c2ws[curr_frame_name_idx]
		transforms['frames'][frame_idx]['transform_matrix'] = c2w.tolist()
		selected_transforms['frames'].append(transforms['frames'][frame_idx])
		curr_frame_name_idx += 1

with open("transforms_train_50_modified.json", "w") as f:
    json.dump(obj=selected_transforms, fp=f)
