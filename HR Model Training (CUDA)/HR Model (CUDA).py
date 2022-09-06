import sys
import time

import torch
import torch.nn as nn
from torch.autograd import Variable
from torch.optim.lr_scheduler import MultiStepLR
from torch.utils.data import DataLoader
from torchvision import transforms

sys.path.append('../input/hr-model-training-cuda-utils/')

from utils.database.Pixelmap import PixelMap_fold_STmap

from utils.model.model_disentangle import HR_disentangle_cross
from utils.loss.loss_cross import Cross_loss


################################################################################
batch_size_num = 2
eval_batch_size = 5

toTensor = transforms.ToTensor()
resize = transforms.Resize(size=(320, 320))

################################################################################
lambda_hr = 1
lambda_img = 0.0000025
lambda_cross_fhr = 0.000005
lambda_cross_fn = 0.000005
lambda_cross_hr = 1

video_length = 300
################################################################################
train_dataset = PixelMap_fold_STmap(root_dir='../input/stmaps-lite-training/STmap 5665 Training/',
                                    Training=True,
                                    transform=transforms.Compose([resize, toTensor]),
                                    VerticalFlip=True,
                                    video_length=video_length)
train_loader = DataLoader(train_dataset,
                          batch_size=batch_size_num,
                          shuffle=True, num_workers=2)

eval_dataset = PixelMap_fold_STmap(root_dir='../input/stmaps-lite-evaluation/STmap 5665 Evaluation/',
                                   Training=False,
                                   transform=transforms.Compose([resize, toTensor]),
                                   VerticalFlip=False,
                                   video_length=video_length)
eval_loader = DataLoader(eval_dataset,
                         batch_size=eval_batch_size,
                         shuffle=False, num_workers=2)
################################################################################
net = HR_disentangle_cross()

net.cuda()
################################################################################
lossfunc_HR = nn.L1Loss()
lossfunc_img = nn.L1Loss()
lossfunc_cross = Cross_loss(lambda_cross_fhr=lambda_cross_fhr, lambda_cross_fn=lambda_cross_fn,
                            lambda_cross_hr=lambda_cross_hr)

optimizer = torch.optim.Adam([{'params': net.parameters(), 'lr': 0.0005}])


################################################################################
def net_train():
    net.train()
    train_loss = 0
    train_loss_hr = 0

    for batch_idx, (data, bpm, fps, idx) in enumerate(train_loader):
        data = Variable(data)
        bpm = Variable(bpm.view(-1, 1))

        data, bpm = data.cuda(), bpm.cuda()

        feat_hr, feat_n, output, img_out, \
        feat_hrf1, feat_nf1, hrf1, idx1, \
        feat_hrf2, feat_nf2, hrf2, idx2 = net(data)

        loss_hr = lossfunc_HR(output, bpm) * lambda_hr
        loss_img = lossfunc_img(data, img_out) * lambda_img

        loss = loss_hr + loss_img

        loss_cross, loss_hr1, loss_hr2, \
        loss_fhr1, loss_fhr2, loss_fn1, loss_fn2, \
        loss_hr_dis1, loss_hr_dis2 = lossfunc_cross(
            feat_hr, feat_n, output,
            feat_hrf1, feat_nf1, hrf1, idx1,
            feat_hrf2, feat_nf2, hrf2, idx2, bpm
        )
        loss += loss_cross

        train_loss += loss.item()
        train_loss_hr += loss_hr.item()

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        # print("[" + time.ctime(), end="] ")
        # print(
        #     'Training... Epoch: {:.0f}, Batch: {:.0f}, Loss: {:.4f} '
        #     '(Loss_HR: {:.4f}, Loss_IMG: {:.4f}, Loss_Cross: {:.4f})'.format(
        #         epoch, batch_idx, loss, loss_hr, loss_img, loss_cross
        #     )
        # )

        # 释放内存
        del feat_hr, feat_n, output, img_out, \
            feat_hrf1, feat_nf1, hrf1, idx1, \
            feat_hrf2, feat_nf2, hrf2, idx2
        del loss_cross, loss_hr1, loss_hr2, \
            loss_fhr1, loss_fhr2, loss_fn1, loss_fn2, \
            loss_hr_dis1, loss_hr_dis2
        # 查看内存
        # get_memory_info()

    train_loss /= len(train_loader)
    train_loss_hr /= len(train_loader)
    return train_loss, train_loss_hr


def net_eval():
    net.eval()
    eval_loss = 0

    for (data, hr, fps, idx) in eval_loader:
        data = Variable(data)
        hr = Variable(hr.view(-1, 1))

        data, hr = data.cuda(), hr.cuda()

        feat_hr, feat_n, output, img_out, \
        feat_hrf1, feat_nf1, hrf1, idx1, \
        feat_hrf2, feat_nf2, hrf2, idx2 = net(data)

        loss = lossfunc_HR(output, hr)

        eval_loss += loss.item()

        # print("[" + time.ctime(), end="] ")
        # print(
        #     'Model Evaluated. Epoch: {:.0f}, Loss: {:.4f}'.format(epoch, loss)
        # )

        # 释放内存
        del feat_hr, feat_n, output, img_out, \
            feat_hrf1, feat_nf1, hrf1, idx1, \
            feat_hrf2, feat_nf2, hrf2, idx2
        del loss

    eval_loss /= len(eval_loader)
    return eval_loss


################################################################################
loss_rec, loss_hr_rec, eval_loss_rec, lr_rec = [], [], [], []

begin_epoch = 1
epoch_num = 70

scheduler = MultiStepLR(optimizer, milestones=[30, 60], gamma=0.5)

for epoch in range(begin_epoch, epoch_num + 1):
    # if epoch > 20:
    #     train_dataset.transform = transforms.Compose([resize, toTensor])
    #     train_dataset.VerticalFlip = False
    #
    #     train_loader = DataLoader(train_dataset, batch_size=batch_size_num,
    #                               shuffle=True, num_workers=2)

    # Train
    lo, lohr = net_train()
    loss_rec.append(lo)
    loss_hr_rec.append(lohr)
    print("[" + time.ctime(), end="] ")
    print('Training... Epoch: {:.0f}, Loss: {:.4f}, Loss_HR: {:.4f}'.format(epoch, lo, lohr))

    l_r = optimizer.state_dict()['param_groups'][0]['lr']
    lr_rec.append(l_r)
    print(" " * 26, end=" ")
    print('            Epoch: {:.0f}, Learning Rate: {:.4f}'.format(epoch, l_r))

    # Evaluation
    ev_lo = net_eval()
    eval_loss_rec.append(ev_lo)
    print("[" + time.ctime(), end="] ")
    print('Validating... Epoch: {:.0f}, Loss_HR: {:.4f}'.format(epoch, ev_lo))

    # Schedule
    scheduler.step()

    torch.cuda.empty_cache()

timestamp_str = str(round(time.time()))

torch.save(net, "./hr_model_cuda_" + timestamp_str + ".pt")
torch.save(net.state_dict(), "./hr_model_state_dict_cuda_" + timestamp_str + ".pt")
print("[" + time.ctime(), end="] ")
print("Completed training, model saved")

wf = open("./model_loss_cuda_" + timestamp_str + ".txt", mode='w')
wf.write(str(loss_rec))
wf.close()

wf = open("./model_loss_hr_cuda_" + timestamp_str + ".txt", mode='w')
wf.write(str(loss_hr_rec))
wf.close()

wf = open("./model_eval_loss_cuda_" + timestamp_str + ".txt", mode='w')
wf.write(str(eval_loss_rec))
wf.close()

wf = open("./model_learning_rates_cuda_" + timestamp_str + ".txt", mode='w')
wf.write(str(lr_rec))
wf.close()

print("[" + time.ctime(), end="] ")
print("Saved statistics")
