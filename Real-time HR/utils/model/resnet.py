import math

import torch.nn as nn
import torch.utils.model_zoo as model_zoo

__all__ = ['ResNet', 'resnet18', 'resnet18_part']

model_urls = {
    'resnet18': 'https://download.pytorch.org/models/resnet18-5c106cde.pth',
    'resnet34': 'https://download.pytorch.org/models/resnet34-333f7ec4.pth',
    'resnet50': 'https://download.pytorch.org/models/resnet50-19c8e357.pth',
    'resnet101': 'https://download.pytorch.org/models/resnet101-5d3b4d8f.pth',
    'resnet152': 'https://download.pytorch.org/models/resnet152-b121ed2d.pth',
}


# 卷积层
def conv3x3(in_planes, out_planes, stride=(1, 1)):
    """3x3 convolution with padding"""
    return nn.Conv2d(in_planes, out_planes, kernel_size=(3, 3), stride=stride,
                     padding=1, bias=False)


# 残差块
class BasicBlock(nn.Module):
    expansion = 1

    def __init__(self, inplanes, planes, stride=1, downsample=None):
        super(BasicBlock, self).__init__()

        # 卷积层
        self.conv1 = conv3x3(inplanes, planes, stride)
        # 批量归一化层
        self.bn1 = nn.BatchNorm2d(planes)
        # 激活函数
        self.relu = nn.ReLU(inplace=True)
        # 卷积层
        self.conv2 = conv3x3(planes, planes)
        # 批量归一化层
        self.bn2 = nn.BatchNorm2d(planes)

        self.downsample = downsample
        self.stride = stride

    # 前向传播（“x + (f(x)-x)”）
    # “残差”x可跨层更快地向前传播
    def forward(self, x):
        # “残差”x
        residual = x

        # 网络走一遍
        out = self.conv1(x)
        out = self.bn1(out)
        out = self.relu(out)
        out = self.conv2(out)
        out = self.bn2(out)

        # 下采样选项
        if self.downsample is not None:
            residual = self.downsample(x)

        # 前向传播（“x + (f(x)-x)”）
        out += residual
        out = self.relu(out)
        return out


# 瓶颈层
class Bottleneck(nn.Module):
    expansion = 4

    def __init__(self, inplanes, planes, stride=(1, 1), downsample=None):
        super(Bottleneck, self).__init__()

        self.conv1 = nn.Conv2d(inplanes, planes, kernel_size=(1, 1), bias=False)
        self.bn1 = nn.BatchNorm2d(planes)
        self.conv2 = nn.Conv2d(planes, planes, kernel_size=(3, 3), stride=stride, padding=1, bias=False)
        self.bn2 = nn.BatchNorm2d(planes)
        self.conv3 = nn.Conv2d(planes, planes * 4, kernel_size=(1, 1), bias=False)
        self.bn3 = nn.BatchNorm2d(planes * 4)
        self.relu = nn.ReLU(inplace=True)

        self.downsample = downsample
        self.stride = stride

    def forward(self, x):
        residual = x

        out = self.conv1(x)
        out = self.bn1(out)
        out = self.relu(out)
        out = self.conv2(out)
        out = self.bn2(out)
        out = self.relu(out)
        out = self.conv3(out)
        out = self.bn3(out)

        if self.downsample is not None:
            residual = self.downsample(x)

        out += residual
        out = self.relu(out)
        return out


# 输入是STmap，输出是predicted HR
class ResNet(nn.Module):

    def __init__(self, block, layers, num_classes=1000, ave_size=7, num_output=1):
        self.inplanes = 64
        super(ResNet, self).__init__()

        self.conv1 = nn.Conv2d(3, 64, kernel_size=(7, 7), stride=(2, 2), padding=3, bias=False)
        self.bn1 = nn.BatchNorm2d(64)
        self.relu = nn.ReLU(inplace=True)

        self.maxpool = nn.AvgPool2d(kernel_size=3, stride=2, padding=1)

        self.layer1 = self._make_layer(block, 64, layers[0])

        # layer2输出encoded feature
        self.layer2 = self._make_layer(block, 128, layers[1], stride=2)
        # 至此实现Fig. 4(a) the physiological and non-physiological encoder Ep and En

        # layer3输出供生理信息估计的feature
        self.layer3 = self._make_layer(block, 256, layers[2], stride=2)
        # 至此实现Fig. 4(c) the physiological estimator的前半部分

        # 接下来实现Fig. 4(c) the physiological estimator的心率估计部分，输出predicted HR
        self.layer4 = self._make_layer(block, 512, layers[3], stride=2)

        self.avgpool = nn.AvgPool2d(ave_size, stride=1)

        self.fc = nn.Linear(512 * block.expansion, num_classes)
        # 至此实现全部网络结构

        self.num_output = num_output
        for m in self.modules():
            if isinstance(m, nn.Conv2d):
                n = m.kernel_size[0] * m.kernel_size[1] * m.out_channels
                m.weight.data.normal_(0, math.sqrt(2. / n))
            elif isinstance(m, nn.BatchNorm2d):
                m.weight.data.fill_(1)
                m.bias.data.zero_()

    # 封装一层残差网络的结构
    def _make_layer(self, block, planes, blocks, stride=(1, 1)):
        downsample = None
        if stride != 1 or self.inplanes != planes * block.expansion:
            downsample = nn.Sequential(
                nn.Conv2d(
                    self.inplanes, planes * block.expansion,
                    kernel_size=(1, 1), stride=stride, bias=False
                ),
                nn.BatchNorm2d(planes * block.expansion),
            )

        layers = [block(self.inplanes, planes, stride, downsample)]
        self.inplanes = planes * block.expansion
        for i in range(1, blocks):
            layers.append(block(self.inplanes, planes))

        return nn.Sequential(*layers)

    def forward(self, x):
        x = self.conv1(x)
        x = self.bn1(x)
        x = self.relu(x)

        conv1 = self.maxpool(x)

        conv2 = self.layer1(conv1)

        # layer2输出encoded feature
        conv3 = self.layer2(conv2)  # B*128*28*28
        # 至此实现Fig. 4(a) the physiological and non-physiological encoder Ep and En

        # layer3输出供生理信息估计的feature
        conv4 = self.layer3(conv3)  # B*256*14*14
        # 至此实现Fig. 4(c) the physiological estimator的前半部分

        # 继续实现Fig. 4(c) the physiological estimator的心率估计部分
        conv5 = self.layer4(conv4)  # B*512*7*7

        x = self.avgpool(conv5)

        feat = x.view(x.size(0), -1)
        x = self.fc(feat)
        # 至此x为估计的心率

        if self.num_output == 34:
            return x, conv3, conv4
        else:
            return x


def resnet18(pretrained=False, **kwargs):
    """Constructs a ResNet-18 model.
    Args:
        pretrained (bool): If True, returns a model pretrained on ImageNet
    """
    model = ResNet(BasicBlock, [2, 2, 2, 2], **kwargs)
    if pretrained:
        model.load_state_dict(model_zoo.load_url(model_urls['resnet18']))
    return model


# 到ResNet的layer2为止，用作noise encoder，输出encoded feature
class ResNet_part(nn.Module):

    def __init__(self, block, layers):
        self.inplanes = 64
        super(ResNet_part, self).__init__()

        self.conv1 = nn.Conv2d(3, 64, kernel_size=(7, 7), stride=(2, 2), padding=3, bias=False)
        self.bn1 = nn.BatchNorm2d(64)
        self.relu = nn.ReLU(inplace=True)

        self.maxpool = nn.AvgPool2d(kernel_size=3, stride=2, padding=1)

        self.layer1 = self._make_layer(block, 64, layers[0])

        self.layer2 = self._make_layer(block, 128, layers[1], stride=2)

        for m in self.modules():
            if isinstance(m, nn.Conv2d):
                n = m.kernel_size[0] * m.kernel_size[1] * m.out_channels
                m.weight.data.normal_(0, math.sqrt(2. / n))
            elif isinstance(m, nn.BatchNorm2d):
                m.weight.data.fill_(1)
                m.bias.data.zero_()

    def _make_layer(self, block, planes, blocks, stride=(1, 1)):
        downsample = None
        if stride != 1 or self.inplanes != planes * block.expansion:
            downsample = nn.Sequential(
                nn.Conv2d(
                    self.inplanes, planes * block.expansion,
                    kernel_size=(1, 1), stride=stride, bias=False
                ),
                nn.BatchNorm2d(planes * block.expansion),
            )

        layers = [block(self.inplanes, planes, stride, downsample)]
        self.inplanes = planes * block.expansion
        for i in range(1, blocks):
            layers.append(block(self.inplanes, planes))

        return nn.Sequential(*layers)

    def forward(self, x):
        x = self.conv1(x)
        x = self.bn1(x)
        x = self.relu(x)

        conv1 = self.maxpool(x)

        conv2 = self.layer1(conv1)

        conv3 = self.layer2(conv2)

        return conv3


def resnet18_part():
    model = ResNet_part(BasicBlock, [2, 2, 2, 2])

    return model
