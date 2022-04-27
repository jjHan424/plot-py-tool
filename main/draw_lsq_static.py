'''
Author: HanJunjie
Date: 2021-11-29 21:26:38
LastEditTime: 2022-04-27 10:19:31
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
#import seaborn as sns
import trans as tr

REF_XYZ = {"HKLM":[-2414046.6433,5391602.1169,2396878.6436],
           "HKSC":[-2414267.6255,5386768.7774,2407459.7930],
           "HKTK":[-2418093.0695,5374658.0963,2430428.9388],
           "HKSL":[-2393383.0432,5393860.9504,2412592.1881]}
ENU_ALL = {}
#mode_list = ["HKLM","HKSC","HKTK"]
#mode_list = ["GEC","G","E","C","GE"]#,"4 Sites Grid","3 Sites MLCM"]
mode_list = ["PC-10000","Server-10000"]
#site_list = ["HKLM","HKSC","HKTK"]
#site_list = ["HKSC","HKSC","HKLM"]
site_list = "HKSL"
Direct = "/Users/hjj/Documents/HJJ/Master_1/IonoGrid/2021100/Bias"
filename_list = [
                "/Users/hjj/Documents/HJJ/Master_1/IonoGrid/2021100/serverTest/HKSL-GEC-ALL-10000.flt",
                "/Users/hjj/Documents/HJJ/Master_1/IonoGrid/2021100/compare/HKSL-GEC-ALL-10000.flt",
                "/Users/hjj/Documents/HJJ/Master_1/IonoGrid/2021100/compare/HKSL-GEC-ALL-100000.flt",
                Direct + "/" + "client/" + "HKSC-GEC.flt",
                Direct + "/" + "client/" + "HKSC-GEC.flt",
                Direct + "/" + "client-NONE/" + "HKLM-E.flt",
                Direct + "/" + "client-NONE/" + "HKLM-C.flt",
                Direct + "/" + "client-NONE/" + "HKLM-GE.flt",
                Direct + "/" + "client-NONE0/" + "HKSC-GEC.flt",
                Direct + "/" + "client-NONE2/" + "HKSC-GEC.flt",
                Direct + "/" + "client-HKST/" + "HKSC-GEC.flt",
                Direct + "/" + "client-HKST0/" + "HKSC-GEC.flt",
                Direct + "/" + "client-HKST2/" + "HKSC-GEC.flt"
                ]
#filename_list = ["/Users/hjj/Documents/HJJ/Master_1/IonoGrid/2021100/clientHKTK/3.flt"]
                 
# filename_list = [
#                 #"/Users/hjj/Documents/HJJ/Master_1/IonoGrid/2021100/clientHKTK/5.flt",
#                 #"/Users/hjj/Documents/HJJ/Master_1/IonoGrid/2021100/clientHKTK/6.flt",
#                 "/Users/hjj/Documents/HJJ/Master_1/IonoGrid/2021100/clientHKTK/3.flt"
#                  ]
for i in range(len(mode_list)):
    data_Raw = rf.open_flt_ppplsq_file(filename_list[i])
    data_ENU = dp.XYZ2ENU_const(XYZ = data_Raw,REF_XYZ = REF_XYZ,site = site_list)
    ENU_ALL[mode_list[i]] = data_ENU
    
# path_I = "/Users/hjj/Documents/HJJ/Master_1/IonoGrid/2021100/clientHKLM/5-MW.aug"
# path_S = "/Users/hjj/Documents/HJJ/Master_1/IonoGrid/2021100/server_ion/HKLM-GEC-S.aug"
# [head_I,data_I] = rf.open_aug_file_new(path_I)
# [head_S,data_S] = rf.open_aug_file_new(path_S)
# data = dp.pre_aug_new(head_I,data_I,data_S)
# ENU_ALL["ION"] = data
#begTime = 10
#while (begTime < 31):
dr.plot_e_n_u(data = ENU_ALL,type = ["E","N","U"],mode = mode_list,ylim = 0.2,starttime=0,begT=0,LastT=24,deltaT=2,time = "UTC",Fixed=False,delta_data = 30)
    #begTime = begTime + 2

