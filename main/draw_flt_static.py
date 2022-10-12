'''
Author: HanJunjie
Date: 2021-11-29 21:26:38
LastEditTime: 2022-09-02 11:04:15
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
           "2008":[-2400517.6874,5373926.9119,2449368.0923],
           "WUDA":[-2267761.1226,5009370.8398,3220970.5620],
           "E033":[-2340806.3769,4922578.9320,3302011.8419],
           "N047":[-2350716.9401,4955782.5397,3244265.6251],
           "2017":[-2424178.5320,5365092.3806,2445506.8814],
           '2010':[-2419056.7812,5364365.3435,2452055.3961],
           "SGGW":[ -2267804.6138,5009342.3946,3220991.8459],
           "N032":[-2141844.0708,5071953.6039,3209315.6304],
           "HKMW":[-2402484.8351,5395262.2062,2400726.7172]}
ENU_ALL = {}
#mode_list = ["HKLM","HKSC","HKTK"]
#mode_list = ["GEC","G","E","C","GE"]#,"4 Sites Grid","3 Sites MLCM"]
# mode_list = ["MLCM","Grid","Grid-Self","Grid-2"]#,"Omc","Rank"]
mode_list = ["MLCM","Grid","Grid-Self","Grid-Ele"]
# mode_list = ["Grid","Grid-Self","Grid-2"]
#mode_list = ["GRID"]#,"Omc","Rank"]
#site_list = ["HKLM","HKSC","HKTK"]
#site_list = ["WUDA","WUDA","WUDA"]
site = "N032"
site_list = [site,"E033","WUDA"]
#site_list = "HKSC"
Y=2021
M=12
D=5
S=2
L=22
# S=9
# L=3
# WUHAN
# Direct1=r"E:\1Master_2\Paper_Grid\Res_FromServer\AUG_vs_Grid_2021339\client-Wgt-WUDA"
# Direct2=r"E:\1Master_2\Paper_Grid\Res_FromServer\AUG_vs_Grid_2021339\client-Wgt-WHDS-WHXZ"
# Direct3=r"E:\1Master_2\Paper_Grid\Res_FromServer\AUG_vs_Grid_2021339\client-WH-Grid-SigWgt"
# Direct4=r"E:\1Master_2\Paper_Grid\Res_FromServer\AUG_vs_Grid_2021339\client-WH-Aug"
# HongKong
Direct1=r"E:\1Master_2\Paper_Grid\Res_FromServer\AUG_vs_Grid_2021339\client-WH-Aug"
Direct2=r"E:\1Master_2\Paper_Grid\Res_FromServer\Grid_Wgt_dIon\client-Grid-WH"
# Direct1=r"E:\1Master_2\Paper_Grid\Res_FromServer\AUG_vs_Wgt_2021339_HK\client-Aug"
# Direct2=r"E:\1Master_2\Paper_Grid\Res_FromServer\Grid_Wgt_dIon\client-Grid-HK"
Direct3=r"E:\1Master_2\Paper_Grid\Res_FromServer\Grid_Sig_Wgt_dIon_New\client-Wgt-N032"
Direct4=r"E:\1Master_2\Paper_Grid\Res_FromServer\Grid_Sig_Ele_Ave\client-Wgt-N032"
# Direct5=r"E:\1Master_2\Paper_Grid\Res_FromServer\Gird_Wgt_dIon\client-Wgt-HKSC-phase"
# Direct6=r"E:\1Master_2\Paper_Grid\Res_FromServer\Gird_Wgt_dIon\client-Wgt-WHDS-WHXZ-phase"

# filename_list = [
#                 Direct1 + "\\" + site + "-GEC-near.flt",
#                 # Direct2 + "\\" + site + "-GEC-5-5.flt",
#                 Direct3 + "\\" + site + "-GEC.flt",
#                 Direct4 + "\\" + site +"-GEC.flt",
#                 Direct5 + "\\" + site +"-GEC.flt"
#                 # Direct6 + "\\" + site +"-GEC.flt"
#                 ]

filename_list = [
                Direct1 + "\\" + site + "-GEC-5-5.flt",
                Direct2 + "\\" + site + "-GEC.flt",
                Direct3 + "\\" + site + "-GEC.flt",
                Direct4 + "\\" + site +"-GEC.flt",
                # Direct5 + "\\" + site +"-GEC.flt"
                # r"E:\1Master_2\Paper_Grid\Pro_20211205-339\client\WUDA-GEC.flt"
                # Direct6 + "\\" + site +"-GEC.flt"
                ]
# China
# filename_list = [
#                 #Direct3 + "/client-comp/"  + "E033-GEC.flt",
#                 #"/Users/hjj/Documents/HJJ/Master_1/IonoGrid/Dynamic/20211205/client/WUDA-GEC.flt",
#                 Direct3 + "/client-grid/"  + "E033-GEC.flt",
#                 Direct3 + "/client-grid-corObs002/"  + "E033-GEC.flt",
#                 Direct3 + "/client-grid/"  + "E033-GEC.flt"
#                 ]
# filename_list = [
#     r"E:\1Master_2\Paper_Grid\Pro_20211205-339\client\HKSC-GEC.flt",
#     r"E:\1Master_2\Paper_Grid\Pro_20211205-339\client\HKSC-GEC_com.flt",
#                  r"E:\1Master_2\Paper_Grid\Pro_20211205-339\client\HKSC-GEC_code.flt",
#                  r"E:\1Master_2\Paper_Grid\Pro_20211205-339\client\HKSC-GEC_phase.flt"]
                 
# filename_list = [
#                 #"/Users/hjj/Documents/HJJ/Master_1/IonoGrid/2021100/clientHKTK/5.flt",
#                 #"/Users/hjj/Documents/HJJ/Master_1/IonoGrid/2021100/clientHKTK/6.flt",
#                 "/Users/hjj/Documents/HJJ/Master_1/IonoGrid/2021100/clientHKTK/3.flt"
#                  ]
for i in range(len(mode_list)):
    data_Raw = rf.open_flt_pvtflt_file(filename_list[i])
    # data_Raw = rf.open_flt_ppplsq_file(filename_list[i])
    data_ENU = dp.XYZ2ENU_const(XYZ = data_Raw,REF_XYZ = REF_XYZ,site = site_list[0])
    ENU_ALL[mode_list[i]] = data_ENU
    
# path_I = "/Users/hjj/Documents/HJJ/Master_1/IonoGrid/2021100/clientHKLM/5-MW.aug"
# path_S = "/Users/hjj/Documents/HJJ/Master_1/IonoGrid/2021100/server_ion/HKLM-GEC-S.aug"
# [head_I,data_I] = rf.open_aug_file_new(path_I)
# [head_S,data_S] = rf.open_aug_file_new(path_S)
# data = dp.pre_aug_new(head_I,data_I,data_S)
# ENU_ALL["ION"] = data
#begTime = 10
# while (S <= 23):
dr.plot_e_n_u(data = ENU_ALL,type = ["E","N","U"],mode = mode_list,ylim = 0.2,starttime=S,LastT=L,deltaT=1,time = "UTC+8",all=False,Fixed=True,delta_data = 5,year = Y,mon=M,day=D,Sigma=3,Sigma_num=1)
    # print("Time:%d",S+1)
    # S = S + 1

