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

Y=2021
M=12
D=5
#all 
S=1 #21
L=3
#open
# S=8+43/60 #21
# L=8/60
#tree
# S=6+46/60
# L=14/60
#building
# S=8+57/60
# L=34/60

# mode_list = ["DGDC","DGCA","SZYT","HZAD","SWHF"]
mode_list = ["30","5"]
file_list = ["/Volumes/H_software/1Master_2/Paper-Grid/20211205-339/server-30-new/N028-GEC-5.aug",
            "/Volumes/H_software/1Master_2/Paper-Grid/20211205-339/server-5-new/N028-GEC-5.aug",
            "/Volumes/SAMSUNG USB/NUC/2022_0726Dynamic/CLK01/HZAD_20220726_SGG_CLK01_S_GEC.aug",
            "/Volumes/H_GREAT/2Project/Allystar/2022_0723SZ_SZK/HZAD_20220723_SGG_CLK06_S_GEC.aug",
            "/Volumes/H_GREAT/2Project/Allystar/2022_0723SZ_SZK/SWHF_20220723_SGG_CLK06_S_GEC.aug"]
data_all = {}
for i in range(len(mode_list)):
    # [head,data] = rf.open_aug_file_rtppp(file_list[i])
    [head,data] = rf.open_aug_file_new(file_list[i])
    # data = rf.open_epo_file_rtppp(file_list[i])
    data_all[mode_list[i]] = data

dr.plot_aug_NSAT(data_all,mode_list,type = "NSAT",freq = 1,starttime = S,time = "UTC+8",show = True,deltaT=1,ylim=0.5,LastT=L,year = Y,mon=M,day=D,deltaData=5)