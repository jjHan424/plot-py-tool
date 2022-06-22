'''
Author: your name
Date: 2022-04-20 14:13:57
LastEditTime: 2022-06-21 13:51:06
LastEditors: HanJunjie HanJunjie@whu.edu.cn
Description: 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
FilePath: /plot-py-tool/main/draw_pos_rtppp_dynamic.py
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

import trans as tr

ENU_ALL = {}
#mode_list = ["HKLM","HKSC","HKTK"]
mode_list = ["NOVA-INS"]
#site_list = ["HKLM","HKSC","HKTK"]
site_list = ["SEPT","NOVA","HKLM"]
filename_list = ["/Users/hjj/Desktop/2022_0620Dynamic2/res/20220620/NOVA_20220620_SGG_CLK06_K_GEC.pppar.pos",
                 "/Users/hjj/Desktop/2022_0618Dynamic/res/20220618/NOVA_20220618_SGG_CLK06_K_GEC.ppprtk",
                 "/Users/hjj/Documents/HJJ/Master_1/文档/PPPRTK综述/综述2.0/20211206/穿越高架桥/SEPT_20211206_SGG_CLK06_K_GEC_pppar_brige.pos"]
filename_ref = ["/Users/hjj/Desktop/2022_0620Dynamic2/TC_Forward2GNSS.txt",
                 "/Users/hjj/Downloads/SEPT-GEC-rtkins.ins",
                 "/Users/hjj/Documents/HJJ/Master_1/文档/PPPRTK综述/综述2.0/20211206/穿越高架桥/TC_combined_smoothed_ToTrimble_brige.txt"]
Y=2022
M=6
D=20
S=12+45/60   
# filename_list = [
#                 #"/Users/hjj/Documents/HJJ/Master_1/IonoGrid/2021100/clientHKTK/5.flt",
#                 #"/Users/hjj/Documents/HJJ/Master_1/IonoGrid/2021100/clientHKTK/6.flt",
#                 "/Users/hjj/Documents/HJJ/Master_1/IonoGrid/2021100/clientHKTK/3.flt"
#                  ]
for i in range(len(mode_list)):
    data_Raw = rf.open_flt_pos_rtpppfile(filename_list[i])
    REF_XYZ = rf.open_pos_ref_IE(filename_ref[i])
    data_ENU = dp.XYZ2ENU_dynamic(XYZ = data_Raw,REF_XYZ = REF_XYZ)
    ENU_ALL[mode_list[i]] = data_ENU

dr.plot_e_n_u(data = ENU_ALL,type = ["E","N","U"],mode = mode_list,ylim = 1,starttime=S,LastT=1,all=False,deltaT=1,year=Y,mon=M,day=D,time = "UTC+8",Fixed=True,delta_data = 1)

