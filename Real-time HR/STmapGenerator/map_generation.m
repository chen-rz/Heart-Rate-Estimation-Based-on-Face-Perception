clear all;
addpath('./utils');

video_file = '../VideoCapture/raw_video.MOV';
landmark_dir = '../VideoCapture/rt_face_landmarks/';
time_file = '../VideoCapture/time_stamps.txt';
Target_path = '../VideoCapture/STmaps/';

landmark_num = 81;

% get the frame rate for the input face video
time = load(time_file);
fps = length(time)/(time(end) - time(1))*1000;
disp(['FPS: ',num2str(fps)]);

% the video clip length
% 每取300帧作为一段
clip_length = 300;

% The MSTmap generation for the whole video
obj = VideoReader(video_file);
numFrames = obj.NumberOfFrames;
disp(['Number of Frames: ', num2str(numFrames)])

MSTmap_whole_video = zeros(63, numFrames, 6);
for k = 1 : numFrames
    frame = read(obj,k);
    lmk_path = strcat(landmark_dir, 'landmarks', num2str(k), '.dat');
    % processing for each frame
    if exist(lmk_path, 'file')
        fid = fopen(lmk_path, 'r');
        if fid > 0
            landmarks = fread(fid,inf,'int');
            landmarks = reshape(landmarks, [2, landmark_num]);
        else
            error(['Error: Failed to open ', lmk_path]);
        end
        fclose(fid);
        
        % get the landmarks for each video frame.
        % landmarks are sorted in a 2*landmark_num martrix in the format of
        % [x0 x1 x2 ... xn; y0 y1 y2 ... yn];
        MSTmap_whole_video = GenerateSignalMap(MSTmap_whole_video, frame, k, landmarks, landmark_num);
        disp(['Generated Signal Map for Frame ', num2str(k)])
    else
        error(['Error: ', lmk_path, ' does not exist']);
    end
end

% Save MSTmaps for the video clips
idx = 1;
% Since the frame rate of VIPL-HR is not stable, we use the number of the
% heart beats as the ground truth of the video clip for normalization.
% i.e., heart_beats_num = gt_HR * clip_length / fps / 60;
% 这一小段（共clip_length帧）内的心跳次数
idx = save_MSTmaps(Target_path, MSTmap_whole_video, fps, clip_length, idx);