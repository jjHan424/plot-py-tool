'''
Author: your name
Date: 2022-04-20 14:13:57
LastEditTime: 2022-04-20 14:17:16
LastEditors: Please set LastEditors
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
import seaborn as sns
import trans as tr

REF_XYZ = {"F034":[ -2686347.4938,5087702.2177,2744828.3915],
           "HKSC":[-2414267.6255,5386768.7774,2407459.7930],
           "HKTK":[-2418093.0695,5374658.0963,2430428.9388]}
ENU_ALL = {}
#mode_list = ["HKLM","HKSC","HKTK"]
mode_list = ["F034"]
#site_list = ["HKLM","HKSC","HKTK"]
site_list = ["F034","HKSC","HKLM"]
filename_list = ["/Users/hjj/Documents/HJJ/Master_1/Project_MeiTuan/sixtens/Wuhan-AUG/综合改正数/终端/20220318/F034_20220318_SSRA02SIX0_K_GEC.pppar.pos",
                 "/Users/hjj/Documents/HJJ/Master_1/IonoGrid/2021100/client/HKSC-GEC-ion.flt",
                 "/Users/hjj/Documents/HJJ/Master_1/IonoGrid/2021100/client/HKLM-GEC-ion.flt"]
                 
# filename_list = [
#                 #"/Users/hjj/Documents/HJJ/Master_1/IonoGrid/2021100/clientHKTK/5.flt",
#                 #"/Users/hjj/Documents/HJJ/Master_1/IonoGrid/2021100/clientHKTK/6.flt",
#                 "/Users/hjj/Documents/HJJ/Master_1/IonoGrid/2021100/clientHKTK/3.flt"
#                  ]
for i in range(len(mode_list)):
    data_Raw = rf.open_flt_pos_rtpppfile(filename_list[i])
    data_ENU = dp.XYZ2ENU_const(XYZ = data_Raw,REF_XYZ = REF_XYZ,site = site_list[i])
    ENU_ALL[mode_list[i]] = data_ENU


dr.plot_e_n_u(data = ENU_ALL,type = ["E","N","U"],mode = mode_list,ylim = 2,starttime=0,begT=0,LastT=24,deltaT=2,time = "UTC",Fixed=False,delta_data = 1)

