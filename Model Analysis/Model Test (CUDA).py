import os
import random
import sys
import time

import scipy.io as sio
import torch
from torch.autograd import Variable
import torchvision.transforms.functional as transF
from torchvision import transforms
from PIL import Image
from torch.utils.data import Dataset, DataLoader

sys.path.append("../input/hr-model-training-cuda-utils/")


class PixelMap_fold_STmap(Dataset):
    def __init__(self, root_dir, Training=True, transform=None, VerticalFlip=False, video_length=300):
        self.train = Training
        self.root_dir = root_dir
        self.transform = transform
        self.video_length = video_length
        self.VerticalFlip = VerticalFlip

    def __len__(self):
        return len(os.listdir(self.root_dir))

    def __getitem__(self, idx):
        dir_idx = idx + 1
        img_name1 = str(dir_idx) + '/img_rgb.png'
        img_name2 = str(dir_idx) + '/img_yuv.png'

        img_path1 = os.path.join(self.root_dir, img_name1)
        img_path2 = os.path.join(self.root_dir, img_name2)
        feature_map1 = Image.open(img_path1).convert('RGB')
        feature_map2 = Image.open(img_path2).convert('RGB')

        if self.transform:
            feature_map1 = self.transform(feature_map1)
            feature_map2 = self.transform(feature_map2)

        if self.VerticalFlip:
            if random.random() < 0.5:
                feature_map1 = transF.vflip(feature_map1)
                feature_map2 = transF.vflip(feature_map2)

        feature_map = torch.cat((feature_map1, feature_map2), dim=0)

        bpm_path = self.root_dir + str(dir_idx) + '/bpm.mat'
        bpm = sio.loadmat(bpm_path)['bpm']
        bpm = bpm.astype('float32')

        fps_path = self.root_dir + str(dir_idx) + '/fps.mat'
        fps = sio.loadmat(fps_path)['fps']
        fps = fps.astype('float32')

        return feature_map, bpm, fps, idx


model_id = "1661906413"
model_dir = "../input/heart-rate-estimation-models/hr_model_cuda_" + model_id + ".pt"
net = torch.load(model_dir)

toTensor = transforms.ToTensor()
resize = transforms.Resize(size=(320, 320))
test_dataset = PixelMap_fold_STmap(root_dir='../input/stmaps-lite/STmap Dataset Lite/',
                                   Training=False, transform=transforms.Compose([resize, toTensor]),
                                   VerticalFlip=False, video_length=300)
test_loader = DataLoader(test_dataset, batch_size=1, shuffle=False, num_workers=2)

net.eval()
test_loss = []
lossFunc = torch.nn.L1Loss()
for (data, hr, f, i) in test_loader:
    data = Variable(data)
    hr = Variable(hr.view(-1, 1))

    data, hr = data.cuda(), hr.cuda()

    feat_hr, feat_n, output, img_out, \
    feat_hrf1, feat_nf1, hrf1, idx1, \
    feat_hrf2, feat_nf2, hrf2, idx2 = net(data)

    loss = lossFunc(output, hr)
    test_loss.append(loss.item())

    print("[" + time.ctime(), end="] ")
    print(
        'Model Tested. Data: {:.0f}, Loss: {:.4f}'.format(i.item(), loss.item())
    )

wf = open("./model_test_cuda_" + model_id + ".txt", 'w')
wf.write(str(test_loss))
wf.close()
