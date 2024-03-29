'''
Author: your name
Date: 2021-11-12 09:38:43
LastEditTime: 2022-08-30 16:09:37
LastEditors: HanJunjie HanJunjie@whu.edu.cn
Description: 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
FilePath: /plot-py-tool/main/draw_aug.py
'''
# '''
# Author: JunjieHan
# Date: 2021-09-06 19:24:38
# LastEditTime: 2022-03-17 22:38:25
# Description: read data file
# '''
import os
import sys
sys.path.insert(0,os.path.dirname(__file__)+'/..')
sys.path.insert(0,os.path.dirname(__file__)+'/../..')
import numpy as np
import readfile as rf
import matplotlib as mpl
mpl.use("TkAgg")
import matplotlib.pyplot as plt
import dataprocess as dp
import draw as dr
import trans as tr
Year,Mon,Day,Hour,lastT,DeltaT = 2021,11,7,2,20,4
count = 1
# site_list1 = ["IJMU","DENT","DOUR","WARE","EIJS","TIT2","EUSK","DILL","DIEP","BADH","KLOP","TERS","KARL","HOBU","PTBB","GOET","KOS1"]
site_list1 = ["DENT","DOUR","WARE","EIJS","TIT2","EUSK","DILL","DIEP","BADH","KLOP","KARL","PTBB","GOET"]
# site_list1 = ["DIEP","TIT2","TERS"]
# site_list1 = ["IJMU","DOUR","WARE","EIJS","TIT2","EUSK","DILL","DIEP","BADH","KLOP","TERS","KARL","HOBU","GOET"]
# site_list1 = ["HKTK","T430","HKKT","HKSS","HKWS","HKSL","HKKS","HKCL","HKPC","HKNP","HKMW","HKLM","HKOH","HKSC"]
# site_list1 = ["FFMJ","REDU","BRUX","KOS1","WSRT"] # EPN_GER
# site_list1 = ["PTBB","TUBO","POPI","BOR1","ARA2"] # EPN_BIG
# site_list1 = ["N028","N047","N068","WHDS","WHSP","WHXZ","XGXN"]
# delay_list = [0,60,120,180,240,300,360,420,480,540,600]
# delay_list = [1,2,4,6,8,10,12,14,16,18,20]
# delay_list = range(1,21)
# delay_list = [2,10,16,20]
delay_list = [20]
# site_list1 = ["REDU","BRUX","KOS1","WSRT"]
# site_list1 = ["KOS1"]
data_site,data_site_S,data_all_aug = {},{},{}
Min_ele,Max_ele,Step_ele = 0,0,30
while count > 0:
    for cur_site in site_list1:
        for cur_delay in delay_list:
            doy = tr.ymd2doy(Year,Mon,Day,0,0,00)
            # print(doy)
            # path_I = r"/Users/hanjunjie/Master_3/1-IUGG/AUG2GRID/{}{:0>3}/EPNGER-R-C-{}/{}-GEC3-30.diff".format(Year,doy,cur_site,cur_site)   # PPPAR算的改正数
            # path_I = r"/Users/hanjunjie/Master_3/1-IUGG/AUG2GRID/{}{:0>3}/EPNGER-R-C-REDU-KOS1-WSRT-BRUX-FFMJ/{}-GEC3-30.respoly".format(Year,doy,cur_site)
            # at(cur_site)# 内插改正数
            # print(cur_site)
            # path_I = r"/Users/hanjunjie/Master_3/1-IUGG/PPPRTK/{}{}/CLIENT_ARIMA/{}-GEC3-FIXED-30-{}.aug".format(Year,doy,cur_site,cur_delay)
            # path_I = r"/Users/hanjunjie/Master_3/1-IUGG/PPPRTK/{}{}/CLIENT_LSTM/{}-GEC3-FIXED-30-10-C00-{}.aug".format(Year,doy,cur_site,cur_delay)
            # path_I = r"/Users/hanjunjie/Master_3/1-IUGG/PPPRTK/{}{}/CLIENT_4_RAW_WITHOUTRES/{}-GEC3-FIXED-30.aug".format(Year,doy,cur_site)
            # path_I = r"/Users/hanjunjie/Master_3/1-IUGG/CLIENT_LSTM_SERVER/CLIENT_{}{:0>3}/{}-GEC2-FIXED-{}-30.aug".format(Year,doy,cur_site,cur_delay)
            # path_S = r"/Users/hanjunjie/Master_3/Data/{}/AUG/{:0>3}/{}-GEC.aug".format(Year,doy,cur_site)
            # path_S = "/Users/hanjunjie/Master_3/Data/2021/AUG/311_EPN_120/{}-GEC3-FIXED-30.aug".format("PTBB")
            # path_res = r"/Users/hanjunjie/Master_3/1-IUGG/PPPRTK/2021310/CLIENT_LSTM/{}-GEC3-FIXED-30-10-30-40-C00-{}.aug".format(cur_site,cur_delay)
            # path_res = r"/Users/hanjunjie/Master_3/1-IUGG/PPPRTK/2021310/CLIENT_ARIMA/{}-GEC3-FIXED-30-122-{}.aug".format(cur_site,cur_delay)
            # path_I = "/Users/hanjunjie/Master_3/1-IUGG/PPPRTK/2021310/TEST/HKLT-CORROBS.aug"
            path_I = "/Users/hanjunjie/Master_3/Data/2021/AUG/311/{}-GEC.aug".format(cur_site)
            if not os.path.exists(path_I):
                continue
            # path_I = path_S
            # path_res = path_I
            # [head_res,data_res] = rf.open_aug_file_new(path_res)
            [head_I,data_I] = rf.open_aug_file_new(path_I)
            # [head_S,data_S] = rf.open_aug_file_new(path_S)
            data_all_aug[cur_site] = data_I
            # data_site["MLCM"] = dp.pre_aug_new(head_I,data_I,data_S)
            # data_site[cur_site] = data_I
            # Min_ele,Max_ele = 0,30
            # while Max_ele <= 90:
                # print("{}-{}".format(Min_ele,Max_ele))
            # dr.plot_aug_G_E_C_Test(data_site[cur_site],head_I,type = "NSAT",freq = 1,starttime = Hour,time = "UTC",show = True,ylim=0,deltaT=DeltaT,LastT=lastT,year = Year,mon=Mon,day=Day,data_S=data_res,min_ele = Min_ele,max_ele = Max_ele,Site = cur_site,Mode = "OLD_DAY",Sun = "ALL")
    # path_I = r"/Users/hanjunjie/Master_3/1-IUGG/AUG2GRID/{}{:0>3}/EPNGER-R-C-{}/{}-GEC3-30.diff".format(Year,doy,cur_site,cur_site)
    # [head_I,data_I] = rf.open_aug_file_new(path_I)
    data_common = dp.find_common_sat_aug(data_all_aug,"DIEP")
    data_site["Without DCB"] = data_common
    grid_path_S = "/Users/hanjunjie/Master_3/1-IUGG/AUG2GRID/{}{:0>3}/EPNGER-R-C-KOS1/GREAT-GEC3-30.grid".format(Year,doy)
    [grid_data_S,lat,lon] = rf.open_grid_file(grid_path_S)
    data_site["With DCB"] = grid_data_S
    dr.plot_aug_NSAT_G_E_C_Sites(data_site,head_I,type = "NSAT",freq = 1,starttime = Hour,time = "GPST",show = False,ylim=0,deltaT=DeltaT,LastT=lastT,year = Year,mon=Mon,day=Day,min_ele = Min_ele,max_ele = Max_ele,Site = cur_site,Mode = "OLD_DAY",Sun = "ALL")
                # Min_ele,Max_ele = Min_ele+Step_ele,Max_ele+Step_ele
    count = count - 1
    Day = Day+1