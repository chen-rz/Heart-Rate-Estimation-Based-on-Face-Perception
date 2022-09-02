function dir_idx = save_MSTmaps(HR_train_path, SignalMap, fps, clip_length, dir_idx)

img_num = size(SignalMap,2); % 视频里共有多少帧
channel_num = size(SignalMap,3);

clip_num = floor((img_num - clip_length)/fps*2); % 每段300帧，去掉最后一段，除以fps得到时间，乘2是为了每0.5秒取一次

for i = 1:clip_num
    begin_idx = floor(0.5*fps*(i-1)+1); % 每0.5秒取一次
    
    if (begin_idx + clip_length - 1 > img_num) % 超过最后一帧，越界
        continue
    end
    
    final_signal = SignalMap(:, begin_idx: begin_idx + clip_length - 1, :); % 取这一段时间
    judge = mean(final_signal,1);
    
    if ~isempty(find(judge(1,:,2) == 0))
        continue;
    else
        dir_name = strcat(HR_train_path, num2str(dir_idx), '/');
        if ~exist(dir_name, 'dir')
            mkdir(dir_name);
        end
        
        fps_path = strcat(dir_name, '/fps.mat');
        
        eval(['save ', fps_path, ' fps']);
        
        final_signal1 = final_signal;
        for idx = 1:size(final_signal,1)
            for c = 1:channel_num
                temp = final_signal(idx,:,c);
                temp = movmean(temp,3);
                final_signal1(idx,:,c) = (temp - min(temp))/(max(temp) - min(temp))*255;
            end
        end
        
        img1 = final_signal1(:,:,[1 2 3]);
        img2 = final_signal1(:,:,[4 5 6]);
        
        img1_path = strcat(dir_name, '/img_rgb.png');
        img2_path = strcat(dir_name, '/img_yuv.png');
        
        imwrite(uint8(img1), img1_path);
        imwrite(uint8(img2), img2_path);
        
        dir_idx = dir_idx + 1;
        
        disp(['Completed STmap ',num2str(dir_idx)])
    end
end

end