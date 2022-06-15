'''
Author: HanJunjie
Date: 2021-11-29 21:26:38
LastEditTime: 2022-06-08 15:41:09
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
           "HKTK":[-2418093.0695,5374658.0963,2430428.9388],
           "2008":[-2400517.6908,5373926.9125,2449368.0968],
           "WUDA":[-2267761.1796,5009370.8535,3220970.6102],
           "E033":[-2340806.3005,4922578.8973,3302011.7872],
           "N047":[-2350716.9401,4955782.5397,3244265.6251],
           "GNSS":[-2162415.18,4394660.91,4072019.31]}
ENU_ALL = {}
#mode_list = ["HKLM","HKSC","HKTK"]
#mode_list = ["GEC","G","E","C","GE"]#,"4 Sites Grid","3 Sites MLCM"]
mode_list = ["Float","Fixed"]#,"Omc","Rank"]
#mode_list = ["GRID"]#,"Omc","Rank"]
#site_list = ["HKLM","HKSC","HKTK"]
#site_list = ["WUDA","WUDA","WUDA"]
site_list = ["GNSS","GNSS","GNSS"]
#site_list = "HKSC"
Y=2020
M=3
D=21
S=7
Direct1 = "/Users/hjj/Documents/HJJ/Master_1/IonoGrid/2021305/Bias/100"
Direct2 = "/Users/hjj/Documents/HJJ/Master_1/IonoGrid/2021305/Bias"
Direct3 = "/Users/hjj/Documents/HJJ/Master_1/IonoGrid/Dynamic/20211205/Result"
# HongKong
# filename_list = [
#                 # "/Users/hjj/Documents/HJJ/Master_1/IonoGrid/2021305/Bias/HKSC-GEC.flt",
#                 # "/Users/hjj/Documents/HJJ/Master_1/IonoGrid/2021305/Bias/HKSC-GEC.flt",
#                 #"/Users/hjj/Documents/HJJ/Master_1/IonoGrid/2021100/client-aug/HKSC-GEC-corObs.flt",
#                 #"/Users/hjj/Documents/HJJ/Master_1/IonoGrid/2021100/client-aug/HKSC-GEC.flt",
#                 #"/Users/hjj/Documents/HJJ/Master_1/IonoGrid/2021100/clientGrid/HKST-HKSC-GEC-corObs.flt",
#                 #"/Users/hjj/Documents/HJJ/Master_1/IonoGrid/2021100/clientGrid/HKST-HKSC-GEC.flt",
#                 #Direct1 + "/client-comp/"  + "HKSC-GEC.flt",
#                 #"/Users/hjj/Documents/HJJ/Master_1/IonoGrid/2021100/client-aug/HKLM-GEC-ion.flt",
#                 #Direct1 + "/client-aug/"  + "HKSC-GEC-corObs.flt",
#                 Direct1 + "/client-rank/"  + "HKSC-GEC-corObs.flt",
#                 Direct1 + "/client-rank/"  + "HKSC-GEC.flt",
#                 #Direct2 + "/" + "client_Rank/" + "HKSC-GEC.flt",
#                 #Direct1 + "/" + "client_2/" + "HKLM-GEC.flt"
#                 ]
# China
filename_list = [
                #Direct3 + "/client-comp/"  + "E033-GEC.flt",
               "/Users/hjj/Documents/HJJ/Master_1/class-2/卫星导航差分与增强系统/zxBaseline/brdc/RTK.txt",
               "/Users/hjj/Documents/HJJ/Master_1/class-2/卫星导航差分与增强系统/zxBaseline/brdc/SPP-GC.txt"
                ]
#filename_list = ["/Users/hjj/Documents/HJJ/Master_1/IonoGrid/2021100/clientHKTK/3.flt"]
                 
# filename_list = [
#                 #"/Users/hjj/Documents/HJJ/Master_1/IonoGrid/2021100/clientHKTK/5.flt",
#                 #"/Users/hjj/Documents/HJJ/Master_1/IonoGrid/2021100/clientHKTK/6.flt",
#                 "/Users/hjj/Documents/HJJ/Master_1/IonoGrid/2021100/clientHKTK/3.flt"
#                  ]
# data_Raw = rf.open_ltt_file(filename_list[1],True,True)
# data_ENU = dp.XYZ2ENU_const(XYZ = data_Raw,REF_XYZ = REF_XYZ,site = site_list[1])
# ENU_ALL[mode_list[0]] = data_ENU
data_Raw = rf.open_ltt_file(filename_list[0],False,False)
data_ENU = dp.XYZ2ENU_const(XYZ = data_Raw,REF_XYZ = REF_XYZ,site = site_list[1])
ENU_ALL[mode_list[0]] = data_ENU  
data_Raw = rf.open_ltt_file(filename_list[0],True,False)
data_ENU = dp.XYZ2ENU_const(XYZ = data_Raw,REF_XYZ = REF_XYZ,site = site_list[1])
ENU_ALL[mode_list[1]] = data_ENU      
# path_I = "/Users/hjj/Documents/HJJ/Master_1/IonoGrid/2021100/clientHKLM/5-MW.aug"
# path_S = "/Users/hjj/Documents/HJJ/Master_1/IonoGrid/2021100/server_ion/HKLM-GEC-S.aug"
# [head_I,data_I] = rf.open_aug_file_new(path_I)
# [head_S,data_S] = rf.open_aug_file_new(path_S)
# data = dp.pre_aug_new(head_I,data_I,data_S)
# ENU_ALL["ION"] = data
#begTime = 10
#while (begTime < 31):
dr.plot_e_n_u(data = ENU_ALL,type = ["NSAT","E","N","U"],mode = mode_list,ylim = 0.5,starttime=S,LastT=1,deltaT=1,time = "UTC",Fixed=True,delta_data = 1,year = Y,mon=M,day=D)
    #begTime = begTime + 2

