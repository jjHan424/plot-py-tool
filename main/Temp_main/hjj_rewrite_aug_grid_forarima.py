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
#import seaborn as sns
import trans as tr
import math
import glv

#input
Year,Mon,Day,Hour,lastT,DeltaT = 2022,3,1,2,22,2
count = 3
while count > 0:
    doy = tr.ymd2doy(Year,Mon,Day,0,0,00)
    grid_path = "/Users/hanjunjie/Master_3/1-IUGG/AUG2GRID/{}{:0>3}/CHNHK16-R-C-HKST-HKLT/GREAT-GEC2-30.grid".format(Year,doy)
    gridinfo_path = "/Users/hanjunjie/Master_3/1-IUGG/AUG2GRID/{}{:0>3}/CHNHK16-R-C-HKST-HKLT/GREAT-GEC2-30.info".format(Year,doy)
    # raw_aug_path = "/Users/hanjunjie/Master_3/Data/2021/AUG/311/REDU-GEC.aug"
    # int_aug_path = "/Users/hanjunjie/Master_3/1-IUGG/PPPRTK/2021311/CLIENT_4_RAW_WITHOUTRES/WSRT-GEC3-FIXED-30.aug"
    # bias_path = "/Users/hanjunjie/Master_3/1-IUGG/AUG2GRID/2021311/HKLT_NEW_4/GREAT-GEC3-30.bias"
    #output
    out_path = "/Users/hanjunjie/Master_3/1-IUGG/CSV_for_Pre/{}{:0>3}".format(Year,doy)
    if not os.path.exists(out_path):
        os.mkdir(out_path)
    out_path = "/Users/hanjunjie/Master_3/1-IUGG/CSV_for_Pre/{}{:0>3}/HK_4Poly_6Site_ARIMA_{}{:0>3}".format(Year,doy,Year,doy)
    if not os.path.exists(out_path):
        os.mkdir(out_path)
    out_put_sys_sat = ["G","E","C"]
    #Time

    #ReadFile
    # [head_I,raw_aug] = rf.open_aug_file_new(raw_aug_path)
    # [head_S,int_aug] = rf.open_aug_file_new(int_aug_path)
    grid_data,ref_lat,ref_lon = rf.open_grid_file(grid_path)
    [head_Info,Grid_Info] = rf.open_aug_file_new(gridinfo_path)
    #WriteFile
    [XLabel,XTick,cov_Time,begT,LastT]=dr.xtick("UTC",Year,Mon,Day,Hour,lastT,DeltaT)
    for cur_time in grid_data.keys():
        plot_time = (cur_time - cov_Time) / 3600
        if plot_time < begT:
            continue
        if plot_time > begT + LastT:
            break
        for cur_sat in grid_data[cur_time].keys():
            if cur_sat in out_put_sys_sat or cur_sat[0] in out_put_sys_sat:
                save_file = os.path.join(out_path,cur_sat)
                out_str = "{:<10}{:<15.8f}{:<15.8f}{:<15.8f}{:<15.8f}".format(cur_time,grid_data[cur_time][cur_sat][0],grid_data[cur_time][cur_sat][1],grid_data[cur_time][cur_sat][2],grid_data[cur_time][cur_sat][3])
                # if cur_time in int_aug.keys():
                #     if cur_sat in int_aug[cur_time].keys():
                #         out_str = out_str + "{:<10.4f}".format(int_aug[cur_time][cur_sat]["ION1"])
                #     else:
                #         out_str = out_str + "{:<10.4f}".format(0.0)
                # else:
                out_str = out_str + "{:<10.4f}".format(0.0)
                    
                if cur_time in Grid_Info.keys():
                    if cur_sat in Grid_Info[cur_time].keys():
                        out_str = out_str + "{:<10.4f}{:<10.4f}".format(0.0,Grid_Info[cur_time][cur_sat]["ELE"])
                    else:
                        out_str = out_str + "{:<10.4f}{:<10.4f}".format(0.0,0.0)
                else:
                    out_str = out_str + "{:<10.4f}{:<10.4f}".format(0.0,0.0)
                with open(save_file,'a') as file:
                    file.write(out_str + "\n")
            else:
                continue
    count = count - 1
    Day = Day + 1


