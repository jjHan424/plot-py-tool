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
# S=6+35/60+17/3600
S=8

ENU_ALL = {}
#mode_list = ["HKLM","HKSC","HKTK"]
mode_list = ["Interpolation","Grid-1dm","Grid-Auto"]
#site_list = ["HKLM","HKSC","HKTK"]
site_list = ["SEPT","SEPT","SEPT"]
Direct3=r"E:\1Master_2\Paper_Grid\Dynamic"
filename_list = [
                Direct3 + "\\" + "client-Aug-" +  "339" + "-02" + "\\" + site_list[0] + "-GEC.flt",
                Direct3 + "\\" + "client-Grid-" + "339" + "-02" + "\\" + site_list[0] + "-GEC.flt",
                # Direct3 + "\\" + "client-Grid-" + "339" + "-06" + "\\" + site_list[0] + "-GEC.flt",
                # Direct3 + "\\" + "client-Grid-" + "310" + "-06" + "\\" + site_list[0] + "-GEC.flt",
                Direct3 + "\\" + "client-Grid_Ele-" + "339" + "-01" + "\\" + site_list[0] + "-GEC.flt",
                ]
filename_ref = [r"E:\1Master_2\Paper_Grid\Dynamic\2021339_WH\\Ref.txt",
                r"E:\1Master_2\Paper_Grid\Dynamic\2021339_WH\\Ref.txt",
                r"E:\1Master_2\Paper_Grid\Dynamic\2021339_WH\\Ref.txt",]
                 
# filename_list = [
#                 #"/Users/hjj/Documents/HJJ/Master_1/IonoGrid/2021100/clientHKTK/5.flt",
#                 #"/Users/hjj/Documents/HJJ/Master_1/IonoGrid/2021100/clientHKTK/6.flt",
#                 "/Users/hjj/Documents/HJJ/Master_1/IonoGrid/2021100/clientHKTK/3.flt"
#                  ]
for i in range(len(mode_list)):
    data_Raw = rf.open_flt_pvtflt_file(filename_list[i])
    REF_XYZ = rf.open_pos_ref_IE(filename_ref[0])
    data_ENU = dp.XYZ2ENU_dynamic(XYZ = data_Raw,REF_XYZ = REF_XYZ)
    ENU_ALL[mode_list[i]] = data_ENU


dr.plot_e_n_u(data = ENU_ALL,type = ["E","N","U"],mode = mode_list,ylim = 2,starttime=S,LastT=10/60,deltaT=10/60,time = "UTC",Fixed=True,delta_data = 1,Sigma=3,Sigma_num=0,year = Y,mon=M,day=D,show = True,all=False)
# dr.plot_enu(data = ENU_ALL,type = ["NSAT","ENU"],mode = mode_list,ylim = 2,starttime=S,LastT=50/60,deltaT=10/60,time = "UTC",Fixed=True,delta_data = 1,Sigma=3,Sigma_num=0,year = Y,mon=M,day=D,show = True,all=False)

