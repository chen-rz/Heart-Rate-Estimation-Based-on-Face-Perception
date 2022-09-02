function dir_idx = save_MSTmaps(HR_train_path, SignalMap, gt, fps, clip_length, dir_idx)

img_num = size(SignalMap,2); % ��Ƶ�ﹲ�ж���֡
channel_num = size(SignalMap,3);

clip_num = floor((img_num - clip_length)/fps*2); % ÿ��300֡��ȥ�����һ�Σ�����fps�õ�ʱ�䣬��2��Ϊ��ÿ0.5��ȡһ��

for i = 1:clip_num
    begin_idx = floor(0.5*fps*(i-1)+1); % ÿ0.5��ȡһ��
    
    if (begin_idx + clip_length - 1 > img_num) % �������һ֡��Խ��
        continue
    end
    
    if floor(begin_idx/fps) >= length(gt) % ʱ��Խ��
        continue;
    end
    
    gt_temp = mean(gt(max(1,floor(begin_idx/fps)):min(length(gt), floor((begin_idx+clip_length)/fps)))); % ����HRƽ��ֵ
    % ��С1�����Ϊʱ�����ޣ���֤��Խ��
    
    final_signal = SignalMap(:, begin_idx: begin_idx + clip_length - 1, :); % ȡ��һ��ʱ��
    judge = mean(final_signal,1);
    
    if ~isempty(find(judge(1,:,2) == 0))
        continue;
    else
        dir_name = strcat(HR_train_path, num2str(dir_idx), '/');
        if ~exist(dir_name, 'dir')
            mkdir(dir_name);
        end
        
        bpm = gt_temp*clip_length/fps/60; % ��һС�Σ���clip_length֡���ڵ���������
        
        label_path = strcat(dir_name, '/gt.mat');
        fps_path = strcat(dir_name, '/fps.mat');
        bpm_path = strcat(dir_name, '/bpm.mat');
        
        eval(['save ', label_path, ' gt_temp']);
        eval(['save ', fps_path, ' fps']);
        eval(['save ', bpm_path, ' bpm']);
        
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
    end
end

end