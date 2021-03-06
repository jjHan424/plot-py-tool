'''
Author: HanJunjie HanJunjie@whu.edu.cn
Date: 2022-06-01 11:13:42
LastEditors: HanJunjie HanJunjie@whu.edu.cn
LastEditTime: 2022-06-06 16:14:19
FilePath: /plot-py-tool/main/draw_flt_dynamic.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
'''
Author: your name
Date: 2022-04-20 14:13:57
LastEditTime: 2022-04-20 20:36:46
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

import trans as tr
Y=2021
M=12
D=5
S=6+35/60+17/3600

ENU_ALL = {}
#mode_list = ["HKLM","HKSC","HKTK"]
mode_list = ["ION-corObs","ION-virTual"]
#site_list = ["HKLM","HKSC","HKTK"]
site_list = ["SEPT","SEPT","SEPT"]
Direct3 = "/Users/hjj/Documents/HJJ/Master_1/IonoGrid/Dynamic/20211205/Result"
filename_list = [
                #Direct3 + "/client-1.0/"  + "SEPT-GEC.flt",
                # Direct3 + "/client-comp/"  + "SEPT-GEC.flt",
                Direct3 + "/client-aug/"  + "SEPT-GEC.flt",
                Direct3 + "/client-aug/"  + "SEPT-GEC-vir.flt",
                Direct3 + "/client-grid/"  + "SEPT-GEC.flt"
                ]
filename_ref = ["/Users/hjj/Documents/HJJ/Master_1/IonoGrid/Dynamic/20211205_REF/IE/TC_combined_smoothed_ToTrimble.txt",
                 "/Users/hjj/Documents/HJJ/Master_1/文档/PPPRTK综述/综述2.0/20211206/城市道路/TC_combined_smoothed_ToTrimble_city.txt",
                 "/Users/hjj/Documents/HJJ/Master_1/文档/PPPRTK综述/综述2.0/20211206/穿越高架桥/TC_combined_smoothed_ToTrimble_brige.txt"]
                 
# filename_list = [
#                 #"/Users/hjj/Documents/HJJ/Master_1/IonoGrid/2021100/clientHKTK/5.flt",
#                 #"/Users/hjj/Documents/HJJ/Master_1/IonoGrid/2021100/clientHKTK/6.flt",
#                 "/Users/hjj/Documents/HJJ/Master_1/IonoGrid/2021100/clientHKTK/3.flt"
#                  ]
for i in range(len(mode_list)):
    data_Raw = rf.open_flt_pvtflt_file(filename_list[i])
    REF_XYZ = rf.open_pos_ref(filename_ref[0])
    data_ENU = dp.XYZ2ENU_dynamic(XYZ = data_Raw,REF_XYZ = REF_XYZ)
    ENU_ALL[mode_list[i]] = data_ENU


dr.plot_e_n_u(data = ENU_ALL,type = ["NSAT","E","N","U"],mode = mode_list,ylim = 2,starttime=S,LastT=3,deltaT=1,time = "UTC",Fixed=True,delta_data = 1,year = Y,mon=M,day=D,all=True)

