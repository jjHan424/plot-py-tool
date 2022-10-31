'''
Author: your name
Date: 2022-04-20 14:13:57
LastEditTime: 2022-08-06 16:21:03
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
# mode_list = ["AUG1","AUG3","AUG4"]
mode_list = ["CLK01","CLK06"]  
#site_list = ["HKLM","HKSC","HKTK"]
site_list = ["SEPT","NOVA","HKLM"]
filename_list = [#"/Volumes/SAMSUNG USB/2022_0628Dynamic/res/20220628/NOVA_20220628_SGG_CLK01_K_GEC.pppar.pos",
                r"F:\20220930\CLK01\res\20220930\SEPT_20220930_SGG_CLK01_K_GEC.pppar.pos",
                r"F:\20220930\CLK06\res\20220930\SEPT_20220930_SGG_CLK06_K_GEC.pppar.pos",
                 "/Volumes/H_GREAT/2Project/Allystar/20220725-20220726_Data_Report/SZK2_20220726.pos",
                 "/Volumes/H_GREAT/2Project/Allystar/20220725-20220726_Data_Report/SZK3_20220726.pos"]
filename_ref = [r"F:\20220930\IE\TC_ToGNSS.txt",
                 r"F:\20220930\IE\TC_ToGNSS.txt",
                 "/Volumes/H_GREAT/2Project/Allystar/2022_0726_Dynamic/novatel.txt"]
Y=2022
M=9
D=30
#all 
# S=2 #21
# L=10
#open
# S=8+43/60 #21
# L=8/60
#tree
# S=6+46/60
# L=14/60
#building
S=10
L=1.5
# filename_list = [
#                 #"/Users/hjj/Documents/HJJ/Master_1/IonoGrid/2021100/clientHKTK/5.flt",
#                 #"/Users/hjj/Documents/HJJ/Master_1/IonoGrid/2021100/clientHKTK/6.flt",
#                 "/Users/hjj/Documents/HJJ/Master_1/IonoGrid/2021100/clientHKTK/3.flt"
#                  ]
for i in range(len(mode_list)):
    data_Raw = rf.open_flt_pos_rtpppfile(filename_list[i])
    # data_Raw = rf.open_ppprtk_rtpppfile(filename_list[i])
    REF_XYZ = rf.open_pos_ref_IE(filename_ref[i])
    # REF_XYZ = rf.open_pos_ref_HDBD(filename_ref[i])
    # REF_XYZ = rf.open_gpgga_file(filename_ref[i],year=Y,mon=M,day=D)
    data_ENU = dp.XYZ2ENU_dynamic(XYZ = data_Raw,REF_XYZ = REF_XYZ)
    ENU_ALL[mode_list[i]] = data_ENU

dr.plot_e_n_u(data = ENU_ALL,type = ["E","N","U"],mode = mode_list,ylim = 0.5,starttime=S,LastT=L,all=False,deltaT=1,year=Y,mon=M,day=D,time = "UTC+8",Fixed=True,delta_data = 1,Sigma=3,Sigma_num=0)

