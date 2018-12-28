# -*- coding: utf-8 -*-
"""
Created on Mon Oct 29 10:03:56 2018
@author: zhxsking
可视化loss变化，用于调参
单独窗口显示 %matplotlib qt5
"""

import torch
import torch.nn as nn
from torch.utils.data import DataLoader
import torch.nn.functional as F
import torchvision
from jsj_dataset import JsjDataset
from unet import UNet
import matplotlib.pyplot as plt
from os.path import join
import sys
import time

class Option():
    """超参数定义类"""
    def __init__(self):
        self.epochs = 50
        self.batchsize = 1
        self.lr = 1e-5
        self.in_dim = 3 # 图片按rgb输入还是按灰度输入，可选1,3
        self.scale = 0.5 # 图片缩放
        self.workers = 2 # 多进程读取data
        self.dir_img = r"E:\pic\jiansanjiang\contrast\RGB\data\train\img"
        self.dir_mask = r"E:\pic\jiansanjiang\contrast\RGB\data\train\mask"
        self.save_path = r"checkpoint"
        self.cuda = False
        if torch.cuda.is_available():
            self.cuda = True
            torch.backends.cudnn.benchmark = True
        self.pretrained = False
        self.net_path = r"checkpoint\unet-epoch26.pkl"


if __name__ == '__main__':
    __spec__ = None
    
    opt = Option()
    
    dataset = JsjDataset(opt.dir_img, opt.dir_mask, scale=opt.scale)
    dataloader = DataLoader(dataset=dataset, batch_size=opt.batchsize, shuffle=True, num_workers=opt.workers)
    
    unet = UNet(in_dim=opt.in_dim)
    loss_func = nn.BCEWithLogitsLoss()
    if opt.cuda:
        unet = unet.cuda()
        loss_func = loss_func.cuda()
    optimizer = torch.optim.Adam(unet.parameters(), lr=opt.lr, weight_decay=0.0005)
    # 加载预训练的参数
    if opt.pretrained:
        state = torch.load(opt.net_path)
        unet.load_state_dict(state['net'])
        optimizer.load_state_dict(state['optimizer'])
    unet.train()
    
    loss_list = []
    loss_list_big = []
    plt.ion()
    plt.show()
    try:
        for epoch in range(opt.epochs):
            local_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            print('epoch {}/{} start... {}'.format(epoch+1, opt.epochs, local_time))
            loss_temp = 0
            
            for cnt, (img, mask) in enumerate(dataloader, 1):
                if opt.cuda:
                    img = img.cuda()
                    mask = mask.cuda()
                out = unet(img)
                out_prob = F.sigmoid(out)
                loss = loss_func(out, mask)
                local_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                print('epoch {}/{}, iter {}/{}, loss {}, {}'.format(epoch+1, opt.epochs, cnt, len(dataloader), loss, local_time))
                loss_temp += loss.item()
                loss_list_big.append(loss.item())
                # 绘制loss曲线
                plt.plot(loss_list_big)
                plt.title('loss {}'.format(loss))
                plt.pause(0.01)
                # 反向传播
                optimizer.zero_grad()
                loss.backward()
                optimizer.step()
            loss_temp /= cnt
            loss_list.append(loss_temp)
            local_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            print('epoch {}/{} done, average loss {}, {}'.format(epoch+1, opt.epochs, loss_temp, local_time))
        plt.ioff()
    except KeyboardInterrupt:
        print('Interrupt!')
        sys.exit(0)
        

            
            
            