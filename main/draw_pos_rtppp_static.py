'''
Author: HanJunjie
Date: 2021-11-29 21:26:38
LastEditTime: 2022-06-22 09:45:17
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

import trans as tr

# REF_XYZ = {"F034":[ -2686347.4938,5087702.2177,2744828.3915],
#            "HKSC":[-2414267.6255,5386768.7774,2407459.7930],
#            "HKTK":[-2418093.0695,5374658.0963,2430428.9388]}

REF_XYZ = {"A010":[ -2175297.0269,4330326.0624,4133584.2257 ],
           "A024":[-2160908.9756,4384024.5574,4084144.5058],
           "HKSC":[-2414267.6255,5386768.7774,2407459.7930],
           "A025":[-2178638.9718,4379452.1998,4079581.9556],
           "09TE":[-2094676.7721,5634981.5854,2123731.7002],
           'JFNG':[-2279829.1055,5004706.4425,3219777.3643],
           "N028":[-2191056.9238,5053129.9326,3205815.9701],
           "107":[-2267808.9738,5009350.0774,3220969.8167],
           "ZHD":[-2267775.3665,5009356.0078,3220980.7585]}
Y=2022
M=6
D=21
S=16
ENU_ALL = {}
#mode_list = ["HKLM","HKSC","HKTK"]
mode_list = ["ZHD"]
#site_list = ["HKLM","HKSC","HKTK"]
site_list = ["ZHD","A010","A025"]
filename_list = ["/Volumes/H_GREAT/2Project/Allystar/rtppp_test/SGG__20220621_SGG_CLK06_K_GEC.pppar.pos",
                 "/Users/hjj/Documents/HJJ/Master_1/Project_MeiTuan/sixtens/TEST-0425/grid_G1G2E1E7B1B3_server_new/client_33sites/result/20220425/A010_20220425_epo_K_GEC.pppar.pos",
                 "/Users/hjj/Documents/HJJ/Master_1/Project_MeiTuan/sixtens/TEST-0425/grid_G1G2E1E7B1B3_user/20220425/A025_20220425_SSRA02SIX0_K_GEC.pppar.pos"]
                 
# filename_list = [
#                 #"/Users/hjj/Documents/HJJ/Master_1/IonoGrid/2021100/clientHKTK/5.flt",
#                 #"/Users/hjj/Documents/HJJ/Master_1/IonoGrid/2021100/clientHKTK/6.flt",
#                 "/Users/hjj/Documents/HJJ/Master_1/IonoGrid/2021100/clientHKTK/3.flt"
#                  ]
for i in range(len(mode_list)):
    # data_Raw = rf.open_flt_pos_rtpppfile(filename_list[i])
    data_Raw = rf.open_flt_pos_rtpppfile(filename_list[i])
    data_ENU = dp.XYZ2ENU_const(XYZ = data_Raw,REF_XYZ = REF_XYZ,site = site_list[i])
    ENU_ALL[mode_list[i]] = data_ENU


dr.plot_e_n_u(data = ENU_ALL,type = ["E","N","U"],mode = mode_list,ylim = 2,starttime=S,LastT=8,all=False,deltaT=1,year=Y,mon=M,day=D,time = "UTC+8",Fixed=True,delta_data = 1)

