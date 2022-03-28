'''
Author: HanJunjie
Date: 2021-11-29 21:26:38
LastEditTime: 2022-03-28 14:07:16
LastEditors: Please set LastEditors
Description: 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
FilePath: /plot-py-tool/main/draw_flt.py
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
import seaborn as sns
import trans as tr

REF_XYZ = {"HKLM":[-2414046.6433,5391602.1169,2396878.6436],
           "HKSC":[-2414267.6255,5386768.7774,2407459.7930],
           "HKTK":[-2418093.0695,5374658.0963,2430428.9388]}
ENU_ALL = {}
#mode_list = ["HKLM","HKSC","HKTK"]
mode_list = ["HKTK"]
site_list = ["HKLM","HKSC","HKTK"]
filename_list = ["/Users/hjj/Documents/HJJ/Master_1/IonoGrid/2021100/client/HKLM-GEC-ion.flt",
                 "/Users/hjj/Documents/HJJ/Master_1/IonoGrid/2021100/client/HKSC-GEC-ion.flt",
                 "/Users/hjj/Documents/HJJ/Master_1/IonoGrid/2021100/client/HKTK-GEC-ion.flt"]
for i in range(len(mode_list)):
    data_Raw = rf.open_flt_pvtflt_file(filename_list[i])
    data_ENU = dp.XYZ2ENU_const(XYZ = data_Raw,REF_XYZ = REF_XYZ,site = site_list[i])
    ENU_ALL[mode_list[i]] = data_ENU
    
path_I = "/Users/hjj/Documents/HJJ/Master_1/IonoGrid/2021100/client/HKTK-GEC-I-ion.aug"
path_S = "/Users/hjj/Documents/HJJ/Master_1/IonoGrid/2021100/server_ion/HKTK-GEC-S.aug"
[head_I,data_I] = rf.open_aug_file_new(path_I)
[head_S,data_S] = rf.open_aug_file_new(path_S)
data = dp.pre_aug_new(head_I,data_I,data_S)
ENU_ALL["ION"] = data

dr.plot_enu(data = ENU_ALL,type = ["ION","E","N","U"],mode = mode_list,ylim = 0.2,starttime=2,begT=10,LastT=21,deltaT=2,time = "UTC+8",Fixed=True,delta_data = 30)

