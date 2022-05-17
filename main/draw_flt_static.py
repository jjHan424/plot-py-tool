'''
Author: HanJunjie
Date: 2021-11-29 21:26:38
LastEditTime: 2022-05-17 17:27:12
LastEditors: HanJunjie HanJunjie@whu.edu.cn
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
           "HKTK":[-2418093.0695,5374658.0963,2430428.9388]}
ENU_ALL = {}
#mode_list = ["HKLM","HKSC","HKTK"]
#mode_list = ["GEC","G","E","C","GE"]#,"4 Sites Grid","3 Sites MLCM"]
mode_list = ["HKSC-ALL","TEST"]#,"Omc","Rank"]
#site_list = ["HKLM","HKSC","HKTK"]
site_list = ["HKSC","HKSC","HKTK"]
#site_list = "HKSC"
Direct1 = "/Users/hjj/Documents/HJJ/Master_1/IonoGrid/2021100/Bias"
Direct2 = "/Users/hjj/Documents/HJJ/Master_1/IonoGrid/2021305/Bias"
filename_list = [
                "/Users/hjj/Documents/HJJ/Master_1/IonoGrid/2021305/Bias/HKSC-GEC.flt",
                "/Users/hjj/Documents/HJJ/Master_1/IonoGrid/2021305/Bias/HKSC-GEC.flt",
                Direct2 + "/client-all/"  + "HKSC-GEC.flt",
                #"/Users/hjj/Documents/HJJ/Master_1/IonoGrid/2021100/client-aug/HKLM-GEC-ion.flt",
                Direct2 + "/client-rank/"  + "HKSC-GEC.flt",
                Direct2 + "/client-rank/"  + "HKTK-GEC.flt",
                #Direct2 + "/" + "client_Rank/" + "HKSC-GEC.flt",
                Direct2 + "/" + "client_2/" + "HKLM-GEC.flt"
                ]
#filename_list = ["/Users/hjj/Documents/HJJ/Master_1/IonoGrid/2021100/clientHKTK/3.flt"]
                 
# filename_list = [
#                 #"/Users/hjj/Documents/HJJ/Master_1/IonoGrid/2021100/clientHKTK/5.flt",
#                 #"/Users/hjj/Documents/HJJ/Master_1/IonoGrid/2021100/clientHKTK/6.flt",
#                 "/Users/hjj/Documents/HJJ/Master_1/IonoGrid/2021100/clientHKTK/3.flt"
#                  ]
for i in range(len(mode_list)):
    data_Raw = rf.open_flt_pvtflt_file(filename_list[i])
    data_ENU = dp.XYZ2ENU_const(XYZ = data_Raw,REF_XYZ = REF_XYZ,site = site_list[i])
    ENU_ALL[mode_list[i]] = data_ENU
    
# path_I = "/Users/hjj/Documents/HJJ/Master_1/IonoGrid/2021100/clientHKLM/5-MW.aug"
# path_S = "/Users/hjj/Documents/HJJ/Master_1/IonoGrid/2021100/server_ion/HKLM-GEC-S.aug"
# [head_I,data_I] = rf.open_aug_file_new(path_I)
# [head_S,data_S] = rf.open_aug_file_new(path_S)
# data = dp.pre_aug_new(head_I,data_I,data_S)
# ENU_ALL["ION"] = data
#begTime = 10
#while (begTime < 31):
dr.plot_e_n_u(data = ENU_ALL,type = ["NSAT","E","N","U"],mode = mode_list,ylim = 2,starttime=8,begT=16,LastT=10.2,deltaT=1,time = "UTC+8",Fixed=True,delta_data = 1)
    #begTime = begTime + 2

