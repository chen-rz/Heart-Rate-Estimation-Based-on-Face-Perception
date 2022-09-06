import sys
import time

import torch
from torch.autograd import Variable
from torch.utils.data import DataLoader
from torchvision import transforms

sys.path.append('../input/hr-model-training-cuda-utils/')

from utils.database.Pixelmap import PixelMap_fold_STmap

################################################################################
toTensor = transforms.ToTensor()
resize = transforms.Resize(size=(320, 320))

video_length = 300
################################################################################
test_dataset = PixelMap_fold_STmap(root_dir='../input/stmap/STmap Dataset/',
                                   Training=False,
                                   transform=transforms.Compose([resize, toTensor]),
                                   VerticalFlip=False,
                                   video_length=video_length)
test_loader = DataLoader(test_dataset,
                         batch_size=1,
                         shuffle=False, num_workers=2)
################################################################################
model_id = "mysterious18920"

net = torch.load('../input/models-to-be-tested/hr_model_cuda_' + model_id + '.pt')

net.cuda()

net.eval()
test_gt, test_output = [], []

for (data, hr, fps, idx) in test_loader:
    data = Variable(data)
    hr = Variable(hr.view(-1, 1))

    data, hr = data.cuda(), hr.cuda()

    feat_hr, feat_n, output, img_out, \
    feat_hrf1, feat_nf1, hrf1, idx1, \
    feat_hrf2, feat_nf2, hrf2, idx2 = net(data)

    test_gt.append(hr.item())
    test_output.append(output.item())

    if idx % 100 == 0:
        print("[" + time.ctime(), end="] ")
        print('Testing Data ' + str(idx.item()) +
              ", Ground Truth: " + str(test_gt[-1]) +
              ", Output: " + str(test_output[-1]))

    # 释放内存
    del feat_hr, feat_n, output, img_out, \
        feat_hrf1, feat_nf1, hrf1, idx1, \
        feat_hrf2, feat_nf2, hrf2, idx2

wf = open("./test_gt_model_" + model_id + ".txt", mode='w')
wf.write(str(test_gt))
wf.close()

wf = open("./test_output_model_" + model_id + ".txt", mode='w')
wf.write(str(test_output))
wf.close()

print("[" + time.ctime(), end="] ")
print("Saved statistics")
