'''
Author: HanJunjie HanJunjie@whu.edu.cn
Date: 2022-06-06 16:50:30
LastEditors: HanJunjie HanJunjie@whu.edu.cn
LastEditTime: 2022-06-06 17:24:37
FilePath: /plot-py-tool/main/draw_satFromAug.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
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
S=3

mode_list = ["MLCM","GRID"]

filename_list = [
                "/Users/hjj/Documents/HJJ/Master_1/IonoGrid/Dynamic/20211205/Result/client-aug/WUDA-GEC-I.aug",
                "/Users/hjj/Documents/HJJ/Master_1/IonoGrid/Dynamic/20211205/Result/client-aug/E033-GEC-I.aug"
                ]
data_ALL={}            
for i in range(len(mode_list)):
    [head_I,data_I] = rf.open_aug_file_new(filename_list[i])
    data_ALL[mode_list[i]] = data_I

dr.plot_SatofAug(data = data_ALL,type = ["NSAT","E","N","U"],mode = mode_list,ylim = 2,starttime=S,LastT=22,deltaT=2,time = "UTC",Fixed=True,delta_data = 1,year = Y,mon=M,day=D)
 