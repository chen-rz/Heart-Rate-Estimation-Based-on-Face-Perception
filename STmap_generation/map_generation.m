clear all;
addpath('./utils');

video_file_root = '../PFFdatabase/';
landmark_dir_root = '../face_landmarks_81p/';
gt_file_root = '../gt_HR/';
Target_path_root = '../STmap/';

scenario = {'DM', 'DS', 'NM', 'NS', 'NSE'};

% for i = 1 : 13 % 数据集01-13循环开始
for i = 6 : 13
    
    if i < 10
        no_str = ['0', num2str(i)];
    else
        no_str = num2str(i);
    end
    
    video_file_pre = [video_file_root, no_str, '/', no_str, '_'];
    landmark_dir_pre = [landmark_dir_root, no_str, '/', no_str, '_'];
    gt_file_pre = [gt_file_root, no_str, '/', no_str, '_'];
    Target_path_pre = [Target_path_root, no_str, '/', no_str, '_'];
    
    for si = 1 : 5 % 场景循环开始
        
        video_file = [video_file_pre, scenario{si}, '_f.MOV'];
        
        % If you use Seetaface(https://github.com/seetaface/SeetaFaceEngine), you will get 81 facial landmarks;
        % While when you use the OpenFace SDK (https://github.com/TadasBaltrusaitis/OpenFace), you will get 68
        % facial landmarks. The landmark_num should be set based on the facial
        % landmark engine you use.
        landmark_num = 81;
        % location for the landmarks
        landmark_dir = [landmark_dir_pre, scenario{si}, '/'];
        
        % get the ground truth HR for the whole video
        gt_file = [gt_file_pre, scenario{si}, '_gt_HR.csv'];
        
        if ~exist(gt_file, 'file')
            disp(['Skipped ', video_file, ' (File does not exist)']);
            continue;
        end
        gt = xlsread(gt_file);
        
        % get the frame rate for the input face video
        fps = 50;
        
        % the video clip length
        % 每取300帧作为一段
        clip_length = 300;
        
        % location of the generated STmaps
        Target_path = [Target_path_pre, scenario{si}, '/'];
        
        
        % The MSTmap generation for the whole video
        if ~exist(video_file, 'file')
            disp(['Skipped ', video_file, ' (File does not exist)']);
            continue;
        end
        
        obj = VideoReader(video_file);
        numFrames = obj.NumberOfFrames;
        
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
        idx = save_MSTmaps(Target_path, MSTmap_whole_video, gt, fps, clip_length, idx);
        
        disp(['Completed ST-maps in directory ', Target_path]);
    end % 场景循环结束
end % 数据集01-13循环结束