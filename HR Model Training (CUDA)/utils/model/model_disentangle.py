import sys

import torch
import torch.nn as nn

sys.path.append('..')

from utils.model.resnet import resnet18, resnet18_part


# 残差块
class ResidualBlock(nn.Module):
    """Residual Block."""

    def __init__(self, dim_in, dim_out):
        super(ResidualBlock, self).__init__()  # self是ResidualBlock类的实例，它调用父类（nn.Module）的init方法
        self.main = nn.Sequential(
            # 卷积层
            nn.Conv2d(dim_in, dim_out, kernel_size=(3, 3), padding=1, bias=False),
            # 批量归一化层
            nn.InstanceNorm2d(dim_out, affine=True),
            # 激活函数
            nn.ReLU(inplace=True),
            # 卷积层
            nn.Conv2d(dim_out, dim_out, kernel_size=(3, 3), padding=1, bias=False),
            # 批量归一化层
            nn.InstanceNorm2d(dim_out, affine=True)
        )

    # 前向传播（“x + (f(x)-x)”）
    # x可跨层更快地向前传播
    def forward(self, x):
        return x + self.main(x)


# Fig. 4(b) the decoder D
class Generator(nn.Module):
    def __init__(self, conv_dim=64, repeat_num=2, img_mode=3, up_time=3):
        super(Generator, self).__init__()

        curr_dim = conv_dim

        # Bottleneck
        # 实际使用repeat_num=1，1个残差块（1层残差网络），即2次3 × 3 conv, 128
        layers = []
        for i in range(repeat_num):
            layers.append(ResidualBlock(dim_in=curr_dim, dim_out=curr_dim))

        # Up-Sampling
        # 3次分别是：
        # 3 × 3 Trans conv, 64, ↑ 2
        # 3 × 3 Trans conv, 32, ↑ 2
        # 3 × 3 Trans conv, 16, ↑ 2
        for i in range(up_time):
            layers.append(
                nn.ConvTranspose2d(
                    curr_dim, curr_dim // 2,
                    kernel_size=(3, 3), stride=(2, 2),
                    padding=(1, 1), output_padding=(1, 1), bias=False
                )
            )
            layers.append(nn.InstanceNorm2d(curr_dim // 2, affine=True))
            layers.append(nn.ReLU(inplace=True))
            curr_dim = curr_dim // 2

        self.main = nn.Sequential(*layers)

        # 7 × 7 conv, 6
        layers = []
        if img_mode == 3:
            layers.append(nn.Conv2d(curr_dim, 6, kernel_size=(7, 7), padding=3, bias=False))
        elif img_mode == 1:
            layers.append(nn.Conv2d(curr_dim, 3, kernel_size=(7, 7), padding=3, bias=False))
        elif img_mode == 4:
            layers.append(nn.Conv2d(curr_dim, 9, kernel_size=(7, 7), padding=3, bias=False))
        elif img_mode == 0:
            layers.append(nn.Conv2d(curr_dim, 3, kernel_size=(7, 7), padding=3, bias=False))

        layers.append(nn.Tanh())
        self.img_reg = nn.Sequential(*layers)

    def forward(self, x):
        features = self.main(x)
        x = self.img_reg(features)
        return x


class HR_estimator_multi_task_STmap(nn.Module):
    def __init__(self):
        super(HR_estimator_multi_task_STmap, self).__init__()

        # Fig. 4(a) the physiological and non-physiological encoder Ep and En
        # 以及Fig. 4(c) the physiological estimator的前半部分和心率估计部分（封装在resnet18中）
        self.extractor = resnet18(pretrained=False, num_classes=1, num_output=34)
        self.extractor.avgpool = nn.AdaptiveAvgPool2d((1, 1))
        self.extractor.conv1 = nn.Conv2d(6, 64, kernel_size=(7, 7), stride=(2, 2), padding=3, bias=False)

    def forward(self, x):
        # feat_out: encoded feature
        # feat: 供rPPG估计的feature
        hr, feat_out, feat = self.extractor(x)

        return hr, feat_out


# 封装encoder和decoder
class HR_disentangle(nn.Module):
    def __init__(self, decov_num=1):
        super(HR_disentangle, self).__init__()

        self.extractor = HR_estimator_multi_task_STmap()

        self.Noise_encoder = resnet18_part()
        self.Noise_encoder.conv1 = nn.Conv2d(
            6, 64, kernel_size=(7, 7), stride=(2, 2), padding=3, bias=False
        )

        self.decoder = Generator(conv_dim=128, repeat_num=decov_num, img_mode=3)

    def forward(self, img):
        hr, feat_hr = self.extractor(img)

        feat_n = self.Noise_encoder(img)

        feat = feat_hr + feat_n
        img = self.decoder(feat)

        return feat_hr, feat_n, hr, img


# 主模型
class HR_disentangle_cross(nn.Module):
    def __init__(self):
        super(HR_disentangle_cross, self).__init__()

        self.encoder_decoder = HR_disentangle(decov_num=1)

    def forward(self, img):
        batch_size = img.size(0)

        feat_hr, feat_n, hr, img_out = self.encoder_decoder(img)

        idx1 = torch.randint(batch_size, (batch_size,))
        idx2 = torch.randint(batch_size, (batch_size,))

        idx1 = idx1.long()
        idx2 = idx2.long()

        feat_hr1 = feat_hr[idx1, :, :, :]
        feat_hr2 = feat_hr[idx2, :, :, :]
        feat_n1 = feat_n[idx1, :, :, :]
        feat_n2 = feat_n[idx2, :, :, :]

        featf1 = feat_hr1 + feat_n2
        featf2 = feat_hr2 + feat_n1

        imgf1 = self.encoder_decoder.decoder(featf1)
        imgf2 = self.encoder_decoder.decoder(featf2)

        feat_hrf1, feat_nf2, hrf1, img_outf1 = self.encoder_decoder(imgf1)
        feat_hrf2, feat_nf1, hrf2, img_outf2 = self.encoder_decoder(imgf2)

        return feat_hr, feat_n, hr, img_out, \
               feat_hrf1, feat_nf1, hrf1, idx1, \
               feat_hrf2, feat_nf2, hrf2, idx2
