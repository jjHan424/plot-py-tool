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

def ele_of_sun(lat,lon,year,mon,day,hour,lastT,step):
    doy = tr.ymd2doy(year,mon,day,0,0,0)
    N0 = 79.6764+0.2422*(year-1985) - int((year-1985)/4)
    t = doy-N0
    theta = 2*math.pi*t/365.2422
    ED = 0.3723+23.2567*math.sin(theta)+0.1149*math.sin(2*theta) - 0.1712*math.sin(3*theta) - 0.758*math.cos(theta) + 0.3656*math.cos(2*theta) + 0.0201*math.cos(3*theta)
    cur_hour = hour
    hour_int = hour
    second,minute = 0,0
    [w,soweek] = tr.ymd2gpst(year,mon,day,hour_int,minute,second)
    all_data = {}
    while cur_hour < hour + lastT:
        sin_h = math.sin(lat*glv.deg) * math.sin(ED*glv.deg) + math.cos(lat*glv.deg) * math.cos(ED*glv.deg) * math.cos((-180+15*(cur_hour+lon/15))*glv.deg)
        H_sun = math.asin(sin_h)
        if H_sun < 0:
            # cur_hour = cur_hour + step/3600
            H_sun = 0
            # continue
        
        all_data[soweek] = H_sun/glv.deg
        cur_hour = cur_hour + step/3600
        soweek = soweek + step
    return all_data
Year,Mon,Day,Hour,lastT,DeltaT,step = 2021,11,14,2,22,2,30
count = 1
while count > 0:
    doy = tr.ymd2doy(Year,Mon,Day,0,0,00)
    #input
    grid_path = "/Users/hanjunjie/Master_3/1-IUGG/AUG2GRID/{}{:0>3}/CHNHK16-R-C-HKST-HKLT/GREAT-GEC2-30.grid".format(Year,doy)
    gridinfo_path = "/Users/hanjunjie/Master_3/1-IUGG/AUG2GRID/{}{:0>3}/CHNHK16-R-C-HKST-HKLT/GREAT-GEC2-30.info".format(Year,doy)
    roti_path = "/Users/hanjunjie/Master_3/Data/2021/ROTI/HKST{}{:0>3}_GEC.ismr".format(Year,doy)
    delay = 30*30
    #output
    out_path = "/Users/hanjunjie/Master_3/1-IUGG/CSV_for_Pre/{}{:0>3}/HK_4Poly_6Site_LSTM_{}{:0>3}".format(Year,doy,Year,doy)
    if not os.path.exists(out_path):
        os.mkdir(out_path)
    out_put_sys_sat = ["G","E","C"]
    # out_put_sys_sat = ["C06","C07","E07"]
    #Time
    # Year,Mon,Day,Hour,lastT,DeltaT,step = 2021,11,1,2,22,2,30
    #ReadFile
    [head_Info,Grid_Info] = rf.open_aug_file_new(gridinfo_path)
    grid_data,ref_lat,ref_lon = rf.open_grid_file(grid_path)
    roti_data = rf.open_ismr(roti_path)
    ele_sun = ele_of_sun(ref_lat,ref_lon,Year,Mon,Day,Hour,lastT,step)
    #WriteFile
    [XLabel,XTick,cov_Time,begT,LastT]=dr.xtick("UTC",Year,Mon,Day,Hour,lastT,DeltaT)
    done_sat = []
    zero_num,no_zero_num = {},{}
    max_zero_num,min_no_zero_num = 20,30

    intval = 30
    max_delay = 90 - intval
    for cur_time in Grid_Info.keys():
        if cur_time not in grid_data.keys():
            continue
        plot_time = (cur_time - cov_Time) / 3600
        if plot_time < begT:
            continue
        if plot_time > begT + LastT:
            break
        for cur_sat in Grid_Info[cur_time].keys():
            cur_delay = delay
            out_str = ""
            # if cur_sat not in grid_data[cur_time].keys():
            #     continue
            if cur_sat in out_put_sys_sat or cur_sat[0] in out_put_sys_sat:
                save_file = os.path.join(out_path,cur_sat + ".csv")
                if cur_sat not in done_sat:
                    with open(save_file,'a') as file:
                        file.write("{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}".format("sow","C00","C10","C01","C11","ele","azi","ipplat","ipplon","elesun","meanB","meanL","meanH","numSite","roti") + "\n")
                    no_zero_num[cur_sat] = 0
                    done_sat.append(cur_sat)
                if cur_sat in grid_data[cur_time].keys():
                    if cur_sat in roti_data[cur_time].keys():
                        cur_roti = roti_data[cur_time][cur_sat]
                    else:
                        cur_roti = 0.0
                    # cur_roti = 0.0
                    out_str = "{},{:.8f},{:.8f},{:.8f},{:.8f},".format(cur_time,grid_data[cur_time][cur_sat][0],grid_data[cur_time][cur_sat][1],grid_data[cur_time][cur_sat][2],grid_data[cur_time][cur_sat][3])
                    out_str = out_str + "{:.4f},{:.4f},{:.4f},{:.4f},{:.4f},{:.4f},{:.4f},{:.4f},{:.4f},{:.4f}".format(Grid_Info[cur_time][cur_sat]["ELE"],Grid_Info[cur_time][cur_sat]["AZI"],Grid_Info[cur_time][cur_sat]["IPPLAT"],Grid_Info[cur_time][cur_sat]["IPPLON"],ele_sun[cur_time],Grid_Info[cur_time][cur_sat]["MB"],Grid_Info[cur_time][cur_sat]["ML"],Grid_Info[cur_time][cur_sat]["MH"],Grid_Info[cur_time][cur_sat]["NUMSite"],cur_roti)
                    no_zero_num[cur_sat] = no_zero_num[cur_sat] + 1
                    with open(save_file,'a') as file:
                        if (len(out_str) > 1):
                            file.write(out_str + "\n")
                else:
                    # if (zero_num[cur_sat] == max_zero_num):
                    #     no_zero_num[cur_sat],zero_num[cur_sat] = 0,0
                    cur_delay = max_delay
                    while cur_delay > 0:
                        if cur_time + cur_delay in grid_data.keys():
                            if cur_sat in grid_data[cur_time + cur_delay].keys():
                                break
                        cur_delay = cur_delay - intval
                    if cur_delay <= 0:
                        if (no_zero_num[cur_sat] < min_no_zero_num):
                            continue
                        else:
                            for i in range(max_zero_num):
                                if cur_time + i * 30 in Grid_Info.keys():
                                    if cur_sat in Grid_Info[cur_time + i * 30].keys():
                                        if cur_sat in roti_data[cur_time + i * 30].keys():
                                            cur_roti = roti_data[cur_time + i * 30][cur_sat]
                                        else:
                                            cur_roti = 0.0
                                        # cur_roti = 0.0
                                        cur_zero_time = cur_time + i * 30
                                        out_str = "{},{:.8f},{:.8f},{:.8f},{:.8f},".format(cur_zero_time,0,0,0,0)
                                        out_str = out_str + "{:.4f},{:.4f},{:.4f},{:.4f},{:.4f},{:.4f},{:.4f},{:.4f},{:.4f},{:.4f}".format(Grid_Info[cur_zero_time][cur_sat]["ELE"],Grid_Info[cur_zero_time][cur_sat]["AZI"],Grid_Info[cur_zero_time][cur_sat]["IPPLAT"],Grid_Info[cur_zero_time][cur_sat]["IPPLON"],ele_sun[cur_zero_time],Grid_Info[cur_zero_time][cur_sat]["MB"],Grid_Info[cur_zero_time][cur_sat]["ML"],Grid_Info[cur_zero_time][cur_sat]["MH"],Grid_Info[cur_zero_time][cur_sat]["NUMSite"],cur_roti)
                                        with open(save_file,'a') as file:
                                            if (len(out_str) > 1):
                                                file.write(out_str + "\n")
                        no_zero_num[cur_sat] = 0
            else:
                continue
    count = count - 1
    Day = Day + 1


