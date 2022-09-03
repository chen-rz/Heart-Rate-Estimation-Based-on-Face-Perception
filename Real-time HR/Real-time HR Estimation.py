import os
import shutil
import subprocess
import sys
import time

import cv2
import numpy as np
import torch
from torch.autograd import Variable
from torch.utils.data import DataLoader
from torchvision import transforms

from utils.database.Pixelmap import PixelMap_fold_STmap

raw_video = "./VideoCapture/raw_video.MOV"
time_stamps_txt = "./VideoCapture/time_stamps.txt"
camera_dir = "./Camera/"
landmark_exe = "points81.exe"
face_landmarks_dir = "./VideoCapture/rt_face_landmarks/"
st_maps_dir = "./VideoCapture/STmaps/"
matlab_dir = "./Matlab for STmap/"
matlab_exe = "map_generation.exe"
out_video_dir = "./Test Record/"

# Clear Cache
face_landmarks_cache = os.listdir(face_landmarks_dir)
for f in face_landmarks_cache:
    os.remove(face_landmarks_dir + f)

st_maps_cache = os.listdir(st_maps_dir)
for f in st_maps_cache:
    shutil.rmtree(st_maps_dir + f)

if os.path.exists(raw_video):
    os.remove(raw_video)

if os.path.exists(time_stamps_txt):
    os.remove(time_stamps_txt)

# Show Welcome Prompt
welcome_window = "Welcome to Heart Rate Estimation Based on Face Perception"
frame_welcome_raw = np.zeros((540, 960, 3), np.uint8)
frame_welcome_raw[0:, 0:, 0], frame_welcome_raw[0:, 0:, 1], frame_welcome_raw[0:, 0:, 2] \
    = 239, 173, 0  # BGR
cv2.namedWindow(welcome_window, cv2.WINDOW_NORMAL)
cv2.resizeWindow(welcome_window, 960, 540)
welcome_end_time = time.time() + 5
while time.time() < welcome_end_time:
    frame_welcome = frame_welcome_raw.copy()
    cv2.putText(
        frame_welcome, "Welcome!", (50, 80),
        cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 5
    )
    cv2.putText(
        frame_welcome, "Heart Rate Estimation Based on Face Perception", (50, 140),
        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 3
    )
    cv2.putText(
        frame_welcome,
        "The camera will be opened in " + str(round(welcome_end_time - time.time())) + "s.",
        (50, 200), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255, 255, 255), 2
    )
    cv2.putText(
        frame_welcome,
        "After being opened, it may take another few seconds for the camera to be ready.",
        (50, 250), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1
    )
    cv2.putText(
        frame_welcome, "Press Esc before the camera is opened to exit the program.", (50, 300),
        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1
    )
    cv2.imshow(welcome_window, frame_welcome)
    if cv2.waitKey(10) == 27:
        print("Keyboard Interrupt: Program ended by Esc")
        sys.exit(0)

# Record Raw Video
# Open Camera
camera_id = 0
capture = cv2.VideoCapture(camera_id)
capture.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

# Close Welcome Window
cv2.destroyWindow(welcome_window)

# Video Writer
vw = cv2.VideoWriter()
codec = vw.fourcc('a', 'v', 'c', '1')
vw.open(raw_video, codec, 30.0, (1280, 720))
if not vw.isOpened():
    print("Error: Failed to instantiate video writer")
    sys.exit(1)

# Process Each Frame
frame_count = 0
while True:
    cap_suc, frame = capture.read()
    if not cap_suc:
        print("Error: Failed to open camera")
        sys.exit(1)
    frame_count += 1

    # Write Time
    wf = open(time_stamps_txt, mode='a')
    wf.write(str(round(time.time() * 1000)) + "\n")
    wf.close()

    # Write Video
    vw.write(frame)

    cv2.putText(
        frame, time.ctime() + "    Frame: " + str(frame_count), (10, 30),
        cv2.FONT_HERSHEY_SIMPLEX, 0.75, (128, 128, 255), 2
    )
    cv2.putText(
        frame, "Press Esc to Stop Recording After 360 Frames", (10, 80),
        cv2.FONT_HERSHEY_SIMPLEX, 1, (128, 128, 255), 2
    )

    camera_window = "Heart Rate Estimation Based on Face Perception"
    cv2.namedWindow(camera_window, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(camera_window, 960, 540)
    cv2.imshow(camera_window, frame)

    if cv2.waitKey(1) == 27 and frame_count > 360:
        break

capture.release()
vw.release()
cv2.destroyWindow(camera_window)

# Face Landmarking
os.chdir(camera_dir)
try:
    subprocess.check_output(landmark_exe, creationflags=subprocess.CREATE_NEW_CONSOLE)
except subprocess.CalledProcessError:
    print("Error: No face detected in the current frame. Please keep steady and try again.")
    sys.exit(1)

# Show prompt
stmap_window = "Generating STmaps..."
frame_stmap = np.zeros((540, 960, 3), np.uint8)
frame_stmap[0:, 0:, 0], frame_stmap[0:, 0:, 1], frame_stmap[0:, 0:, 2] \
    = 239, 173, 0  # BGR
cv2.putText(
    frame_stmap, "Heart Rate Estimation Based on Face Perception",
    (50, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 3
)
cv2.putText(
    frame_stmap, "Generating Spatial-Temporal Maps (STmaps) of the video...",
    (50, 150), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255, 255, 255), 2
)
cv2.putText(
    frame_stmap, "A console application implemented by MATLAB should be running.",
    (50, 200), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255, 255, 255), 2
)
cv2.putText(
    frame_stmap, "This may take up to several minutes. Please wait...",
    (50, 250), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255, 255, 255), 2
)
cv2.imshow(stmap_window, frame_stmap)
cv2.waitKey(10)

# STmap Generation
os.chdir("../")
os.chdir(matlab_dir)
try:
    subprocess.check_output(matlab_exe, creationflags=subprocess.CREATE_NEW_CONSOLE)
except subprocess.CalledProcessError:
    print("Error: An unexpected error occurred while generating STmaps.")
    sys.exit(1)

# Close Prompt
cv2.destroyWindow(stmap_window)

# Get Heart Rate from Network
os.chdir("../")

video_length = 300

toTensor = transforms.ToTensor()
resize = transforms.Resize(size=(320, 320))

test_dataset = PixelMap_fold_STmap(root_dir='./VideoCapture/STmaps/',
                                   Training=False,
                                   transform=transforms.Compose([resize, toTensor]),
                                   VerticalFlip=False,
                                   video_length=video_length)
test_loader = DataLoader(test_dataset, batch_size=1, shuffle=False, num_workers=0)

################################################################################
net_id = "1662170218"

net_file = "./model.pt"
if os.path.exists("./HR_models/"):
    net_file = './HR_models/hr_model_cuda_' + net_id + ".pt"

net = torch.load(net_file, map_location=torch.device('cpu'))

net.to(torch.device("cpu"))
net.eval()

################################################################################
output_list = []
for (data, fps, idx) in test_loader:
    data = Variable(data)

    data = data.to(torch.device("cpu"))

    feat_hr, feat_n, output, img_out, \
    feat_hrf1, feat_nf1, hrf1, idx1, \
    feat_hrf2, feat_nf2, hrf2, idx2 = net(data)

    output_list.append(output.item() / (video_length / fps.item()) * 60)

################################################################################
# Show Output
print("Estimation completed: ", end="")
print(output_list)

capture_o = cv2.VideoCapture(raw_video)

vw_o = cv2.VideoWriter()
out_codec = vw_o.fourcc('a', 'v', 'c', '1')
out_video_file = out_video_dir + "Test_" + str(round(time.time())) + ".MOV"
vw_o.open(out_video_file, out_codec, 30.0, (1280, 720))

# Read All Timestamps
rf = open(time_stamps_txt, 'r')
time_list = []
line = rf.readline()
while line:
    time_list.append(eval(line[:-1]))
    line = rf.readline()
rf.close()

# Calculate Average FPS
frame_num = len(time_list)
avr_fps = frame_num / (time_list[-1] - time_list[0]) * 1000.0
frame_interval = round(avr_fps / 2)
clip_num = int((frame_num - 300) / avr_fps * 2)

# Update Output Value Every 0.5s
frm_o_count = 0
clip_idx = 0
while frm_o_count < frame_num:
    out_cap_suc, frame_o = capture_o.read()
    if not out_cap_suc:
        print("Error: Failed to read video file " + raw_video)
        sys.exit(1)
    frm_o_count += 1

    # Update Output
    if frm_o_count % frame_interval == 0 and clip_idx < clip_num - 1:
        clip_idx += 1

    # Out of Bound
    if clip_idx >= len(output_list):
        print("Warning: No more output values @ Frame " + str(frm_o_count) + " of " + str(frame_num))
        clip_idx = len(output_list) - 1

    # Put Text
    cv2.putText(
        frame_o,
        time.ctime(time_list[frm_o_count - 1] / 1000.0) + "    Frame: " + str(frm_o_count),
        (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (239, 173, 0), 2
    )
    cv2.putText(
        frame_o, "Estimated Heart Rate: ",
        (10, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (239, 173, 0), 2
    )
    cv2.putText(
        frame_o, str(round(output_list[clip_idx], 1)),
        (50, 160), cv2.FONT_HERSHEY_SIMPLEX, 2, (239, 173, 0), 5
    )

    # Write Output Video
    vw_o.write(frame_o)

    # Last Frame
    if frm_o_count == frame_num - 1:
        cv2.putText(
            frame_o, "Successfully finished! You can close this window and view the video at ",
            (10, 210), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (16, 255, 16), 2
        )
        cv2.putText(
            frame_o, out_video_file,
            (10, 250), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (16, 255, 16), 2
        )

    output_window = "Estimated Heart Rates"
    cv2.namedWindow(output_window, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(output_window, 960, 540)
    cv2.imshow(output_window, frame_o)

    if frm_o_count == frame_num - 1:
        cv2.waitKey(0)
    else:
        cv2.waitKey(round(1000 / avr_fps))

capture_o.release()
vw_o.release()
