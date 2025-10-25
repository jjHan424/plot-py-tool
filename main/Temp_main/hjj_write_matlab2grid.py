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

year,month,day = 2022,3,13
count = 1
while count > 0:
    doy = tr.ymd2doy(year,month,day,0,0,00)
    file_path = "/Users/hanjunjie/Master_3/1-IUGG/GRID_PREDICT/{}{:0>3}/HK_6Site_30_40_ARIMA_122/".format(year,doy)
    ref_file = "/Users/hanjunjie/Master_3/1-IUGG/AUG2GRID/{}{:0>3}/CHNHK16-R-C-HKST-HKLT/GREAT-GEC2-30.grid".format(year,doy)
    [grid_ref,lat,lon] = rf.open_grid_file(ref_file)
    [head_str,res_num] = rf.get_gridhead(ref_file)
    i = range(20)
    for i in range(1,21):
        cur_file = os.path.join(file_path,"{}".format(i))
        all_data = {}
        time_all = []
        with open(cur_file,"rt") as f:
            for line in f:
                value = line.split()
                sod = int(value[1])
                if sod not in all_data.keys():
                    all_data[sod] = {}
                    time_all.append(sod)
                if value[0] not in all_data[sod].keys():
                    all_data[sod][value[0]] = {}
                all_data[sod][value[0]]["C00"] = float(value[2])
                all_data[sod][value[0]]["C10"] = float(value[3])
                all_data[sod][value[0]]["C01"] = float(value[4])
                all_data[sod][value[0]]["C11"] = float(value[5])
        save_file = cur_file + ".grid"
        time_all = sorted(time_all)
        outstr = head_str
        with open(save_file,'a') as file:
            file.write(outstr)
        gweek,sow = tr.ymd2gpst(year,month,day,0,0,0)
        for cur_time in time_all:
            if cur_time not in grid_ref.keys():
                continue
            cur_time_temp = cur_time - sow
            hour = math.floor((cur_time_temp)/3600)
            min = math.floor(((cur_time_temp/3600) - hour) * 60)
            sec = cur_time_temp - hour * 3600 - min * 60
            outstr = ">{:>5}{:>3} {:0>2} {:0>2} {:0>2} {:>10.7f}{:>15}\n".format(year,month,day,hour,min,sec,len(all_data[cur_time]))
            
            outstr = outstr + "{:>3}{:>18.8f}{:>18.8f}{:>18.8f}{:>18.8f}{:>18.8f}{:>18.8f}".format("TRP",grid_ref[cur_time]["TRP"][0],grid_ref[cur_time]["TRP"][1],grid_ref[cur_time]["TRP"][2],grid_ref[cur_time]["TRP"][3],grid_ref[cur_time]["TRP"][4],grid_ref[cur_time]["TRP"][5])
            for j in range(res_num):
                outstr = outstr + "{:>15.4f}".format(grid_ref[cur_time]["TRP"][6+j])
            outstr = outstr + "\n"
            for cur_sat in all_data[cur_time].keys():
                if all_data[cur_time][cur_sat]["C00"] == 0.0:# or all_data[cur_time][cur_sat]["C01"] == 0.0 or all_data[cur_time][cur_sat]["C10"] == 0.0 or all_data[cur_time][cur_sat]["C11"] == 0.0:
                    continue
                outstr = outstr + "{:>3}{:>18.8f}{:>18.8f}{:>18.8f}{:>18.8f}{:>18.8f}{:>18.8f}".\
                format(cur_sat,all_data[cur_time][cur_sat]["C00"],all_data[cur_time][cur_sat]["C10"],all_data[cur_time][cur_sat]["C01"],all_data[cur_time][cur_sat]["C11"],0,0)
                for j in range(res_num):
                    outstr = outstr + "{:>15.4f}".format(0.0)
                outstr = outstr + "\n"
            with open(save_file,'a') as file:
                file.write(outstr)
    count = count -1
    day = day + 1


            

