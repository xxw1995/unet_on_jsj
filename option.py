# -*- coding: utf-8 -*-
"""
Created on Tue Mar  5 19:34:46 2019

@author: zhxsking
"""

import torch

class Option():
    """定义网络的参数及其他"""
    def __init__(self):
        self.depth = 3 # 图片深度
        self.epochs = 20
        self.batchsize = 1
        self.lr = 1e-3
        self.weight_decay = 0.000
        self.workers = 0 # 多进程，可能会卡程序
        self.dir_img_train = r"E:\pic\jiansanjiang\contrast\RGB\data\train\img" # 训练集
        self.dir_mask_train = r"E:\pic\jiansanjiang\contrast\RGB\data\train\mask"
        self.dir_img_val = r"E:\pic\jiansanjiang\contrast\RGB\data\val\img" # 验证集
        self.dir_mask_val = r"E:\pic\jiansanjiang\contrast\RGB\data\val\mask"
        self.pretrained = False
        self.pretrained_net_path = r"checkpoint\best-cnn.pkl"
        
        
        self.block_size = 1280 # 一次处理block_size*block_size个像素大小的块
        self.threshold = -0.7 # 阈值,ln(0.5)=-0.69
#        self.net_path = r"checkpoint\best-cnn.pkl"
#        self.net_path = r"checkpoint\best-unet.pkl"
        self.test_img_path = r"E:\pic\baidu\all-band-linear5-norm.tif"
        
        self.flag = 4 # 调参用，预测哪种模型，1为玉米，2为大豆，3为水稻，4为背景
        
        self.device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")