'''
Author: your name
Date: 2021-11-12 09:38:43
LastEditTime: 2022-08-30 16:11:56
LastEditors: HanJunjie HanJunjie@whu.edu.cn
Description: 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
FilePath: /plot-py-tool/main/draw_aug.py
'''
import os
import sys
sys.path.insert(0,os.path.dirname(__file__)+'/..')
import numpy as np
import readfile as rf
import matplotlib as mpl
mpl.use("TkAgg")
import matplotlib.pyplot as plt
import dataprocess as dp
import draw as dr

Y=2023
M=9
D=10
#all 
S=17 #21
L=7
#open
# S=8+43/60 #21
# L=8/60
#tree
# S=6+46/60
# L=14/60
#building
# S=8+57/60
# L=34/60

mode_list = ["WH","GZ"]
# mode_list = ["Server1","Server2","Server3","Client"]

file_list = [
# r"E:\0Project\ZHD_Data\20230910_Data_Test\BDS2\ppprtk\ES43_20230910_SGG_CLK06_K_GEC.aug",
r"E:\0Project\ZHD_Data\20230910_Data_Test\BDS2\aug_rt\SGG__20230910_SGG_CLK06_S_GEC.aug",
r"E:\0Project\ZHD_Data\20230910_Data_Test\BDS2\aug_rt\GZLH_20230910_SGG_CLK06_S_GEC.augi",
r"E:\0Project\ZHD_Data\20230910_Data_Test\BDS2\aug_rt\ES42_20230910_SGG_CLK06_S_GEC.aug",
r"E:\0Project\EXSUN_Data\20230909_Data_Test\BDS2\ppprtk\ES43_20230909_SGG_CLK06_K_GEC.aug",
]
data_all = {}
for i in range(len(mode_list)):
    [head,data] = rf.open_aug_file_rtppp(file_list[i])
    # [head,data] = rf.open_aug_file_new(file_list[i])
    # data = rf.open_epo_file_rtppp(file_list[i])
    data_all[mode_list[i]] = data

dr.plot_aug_NSAT(data_all,mode_list,type = "NSAT",freq = 1,starttime = S,time = "UTC+8",show = True,deltaT=1,ylim=0.5,LastT=L,year = Y,mon=M,day=D,deltaData=5)