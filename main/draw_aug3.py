'''
Author: your name
Date: 2021-11-12 09:38:43
LastEditTime: 2022-08-30 16:11:56
LastEditors: HanJunjie HanJunjie@whu.edu.cn
Description: 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
FilePath: /plot-py-tool/main/draw_aug.py
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

Y=2021
M=11
D=6
#all 
S=2 #21
L=14
#open
# S=8+43/60 #21
# L=8/60
#tree
# S=6+46/60
# L=14/60
#building
# S=8+57/60
# L=34/60

# mode_list = ["DGDC","DGCA","SZYT","HZAD","SWHF"]
mode_list = ["MLCM","Grid"]
# file_list = [
#             r"E:\0Project\NORINCO\0Project\3_20220924_0925(414-Novatel3-302-Trimble2)\20220923AUG_GRT3_414_CLK06\res\20220924\GRT3_20220924_SGG_CLK06_S_GEC.aug",
#             r"E:\0Project\NORINCO\0Project\3_20220924_0925(414-Novatel3-302-Trimble2)\20220923AUG_GRT3_414_CLK06\res\20220924\N004_20220924_SGG_CLK06_S_GEC.aug",
#             r"E:\0Project\NORINCO\0Project\3_20220924_0925(414-Novatel3-302-Trimble2)\20220923AUG_GRT3_414_CLK06\res\20220924\N047_20220924_SGG_CLK06_S_GEC.aug",
#             r"E:\0Project\NORINCO\0Project\20220923AUG_GRT3_414_CLK06\res\20220925\N004_20220925_SGG_CLK06_S_GEC.aug"
# ]
# file_list = [
#             # r"E:\1Master_2\Paper_Grid\Res_FromServer\Grid_Sig_Wgt_dIon_New\client-Wgt-WUDA\WUDA-GEC-I.aug",
#             r"E:\0Project\NORINCO\0Project\AUG_Fig\N004_20221008_SGG_CLK01_S_GEC.aug",
#             r"E:\0Project\NORINCO\0Project\AUG_Fig\N047_20221008_SGG_CLK01_S_GEC.aug",
#             r"E:\0Project\NORINCO\0Project\AUG_Fig\GRT1_20221008_SGG_CLK01_S_GEC.aug"
#             # r"E:\0Project\NORINCO\0Project\CLK06\PPPRTK-WUH2\20220926\WUH2_20220926_SGG_CLK06_K_GEC.aug"
# ]

file_list = [
    r"E:\1Master_2\Paper_Grid\Res_FromServer_New\Client\client-Aug-310\WUDA-GEC-I.aug",
    r"E:\1Master_2\Paper_Grid\Res_FromServer_New\Client\client-Grid-310\WUDA-GEC-I.aug"
]
data_all = {}
for i in range(len(mode_list)):
    # [head,data] = rf.open_aug_file_rtppp(file_list[i])
    [head,data] = rf.open_aug_file_new(file_list[i])
    # data = rf.open_epo_file_rtppp(file_list[i])
    data_all[mode_list[i]] = data

dr.plot_aug_NSAT(data_all,mode_list,type = "NSAT",freq = 1,starttime = S,time = "UTC+8",show = True,deltaT=2,ylim=0.5,LastT=L,year = Y,mon=M,day=D,deltaData=5)