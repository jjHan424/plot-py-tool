'''
Author: HanJunjie HanJunjie@whu.edu.cn
Date: 2022-07-16 14:31:10
LastEditors: HanJunjie HanJunjie@whu.edu.cn
LastEditTime: 2022-07-16 16:25:57
FilePath: /plot-py-tool/main/draw_temp_flt_roti_aug.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
import os
import sys
import math
#from main.draw_flt_static import REF_XYZ
sys.path.insert(0,os.path.dirname(__file__)+'/..')
import numpy as np
import readfile as rf
import matplotlib as mpl
mpl.use("TkAgg")
import matplotlib.pyplot as plt
plt.style.use(['science','grid'])
import dataprocess as dp
import draw as dr
#import seaborn as sns
import trans as tr
#path set
# path_flt = "/Volumes/H_GREAT/WangBo_Paper/2021305/test/Frequency2_UPD_HK_GBM/HKSC-GEC-AR-2.flt"
path_flt = "/Volumes/H_GREAT/WangBo_Paper/2021305/HKSC-GC-AR-2.flt"
path_roti = "/Volumes/H_GREAT/WangBo_Paper/2021305/test/res/HKSC_GEC_0.15.ismr"
path_aug_I = "/Volumes/H_GREAT/WangBo_Paper/2021305/test/Frequency2_UPD_HK_GBM/IONTRP/HKSC-GEC-I.aug"
path_aug_S = "/Volumes/H_GREAT/WangBo_Paper/2021305/test/Frequency2_UPD_HK_GBM/IONTRP/HKSC-GEC-S-2.aug"
figP,axP = plt.subplots(3,1,figsize=(12,10),sharey=False,sharex=True)
#Time
time="UTC"
starttime=8
year = 2021
mon=11
day=1
LastT=14
deltaT=2
all=False
###-------------Time Set in Plot--------------###
if "+" in time:
    end_time = len(time)
    delta_Time = int(time[3:end_time]) + starttime
    begT = int(time[3:end_time]) + starttime
else:
    delta_Time = starttime
    begT=starttime
secow_start = tr.ymd2gpst(year,mon,day,starttime,00,00)
cov_Time = secow_start[1] - delta_Time * 3600
end_Time = begT + LastT
delta_X = math.ceil((LastT)/deltaT)
XLabel = []
XTick = []
starttime = begT - deltaT
for i in range(delta_X):
    starttime = starttime + deltaT
    cur_Str_X = '%02d' % (starttime % 24) + ":00"
    XLabel.append(cur_Str_X)
    XTick.append(int(starttime))       
while starttime < math.ceil(end_Time):
    starttime = starttime + deltaT
    cur_Str_X = '%02d' % (starttime % 24) + ":00"
    XLabel.append(cur_Str_X)
    XTick.append(int(starttime))
###-------------FLT--------------###
data_Raw = rf.open_flt_pvtflt_file(path_flt)
REF_XYZ={"HKSC":[-2414267.6255,5386768.7774,2407459.7930]}
data_ENU = dp.XYZ2ENU_const(XYZ = data_Raw,REF_XYZ = REF_XYZ,site = "HKSC")
time1,dataE,dataN,dataU=[],[],[],[]
Float_NUM,Fixed_NUM=0,0
for cur_time in data_ENU:
    plot_time = (cur_time-cov_Time) / 3600
    if ((plot_time >= begT and plot_time <= (begT + LastT)) or all):
        if data_ENU[cur_time]["AMB"] == 0:
            Float_NUM = Float_NUM + 1
        elif data_ENU[cur_time]["AMB"] == 1:
            Fixed_NUM = Fixed_NUM + 1
        # if (data_ENU[cur_time]["AMB"] == 0):
        #     continue
        time1.append(plot_time)
        dataE.append(data_ENU[cur_time]["E"])
        dataN.append(data_ENU[cur_time]["N"])
        dataU.append(data_ENU[cur_time]["U"])
ss=10
axP[0].set_ylim(-1,1)
axP[0].scatter(time1,dataE,s=ss)
axP[0].scatter(time1,dataN,s=ss)
axP[0].scatter(time1,dataU,s=ss)
font2 = {'family' : 'Times new roman',
            'weight' : 600,
            'size'   : 15,
                }
axP[0].set_ylabel("Positioning Errors(m)",font2)
font2 = {'family' : 'Times new roman',
            'weight' : 600,
            'size'   : 15,
                }
axP[0].legend(["E","N","U"],markerscale=2,prop=font2)
axP[0].set_xticks(XTick)
axP[0].set_xticklabels(XLabel)


###-------------ROTI-------------###
data = rf.open_ismr(path_roti)
time_G = [[] for i in range(100)]
time_R = [[] for i in range(100)]
time_E = [[] for i in range(100)]
time_C = [[] for i in range(100)]
time_TRP = []
data_G = [[] for i in range(100)]
data_R = [[] for i in range(100)]
data_E = [[] for i in range(100)]
data_C = [[] for i in range(100)]
for time in data.keys():
    plot_time = (time - cov_Time) / 3600
    if (plot_time > begT and plot_time < begT + LastT):
        for sat in data[time].keys():
            prn = int(sat[1:3])
            if sat[0] == "C":
                data_C[prn-1].append(data[time][sat])
                time_C[prn-1].append(plot_time)
            if sat[0] == "G":
                data_G[prn-1].append(data[time][sat])
                time_G[prn-1].append(plot_time)
            if sat[0] == "E":
                data_E[prn-1].append(data[time][sat])
                time_E[prn-1].append(plot_time)
for i in range(100):
    G,E,C = True,True,True
    num = len(time_G[i])
    if num < 1:
        G = False
    num = len(time_E[i])
    if num < 1:
        E = False
    num = len(time_C[i])
    if num < 1:
        C = False
    E=False
    if G:
        axP[1].scatter(time_G[i],data_G[i],s=1)
    if E:
        axP[1].scatter(time_E[i],data_E[i],s=1)
    if C:
        axP[1].scatter(time_C[i],data_C[i],s=1)
font2 = {'family' : 'Times new roman',
            'weight' : 600,
            'size'   : 15,
                }
axP[1].set_ylabel("ROTI(TECU/min)",font2)
axP[1].set_xticks(XTick)
# axP[2].set_yticklabels([-0.2,-0.1,0,0.1,0.2],fontsize="x-large")
axP[1].set_ylim(0,2)
###-------------AUG--------------###
[head_I,data_I] = rf.open_aug_file_new(path_aug_I)
[head_S,data_S] = rf.open_aug_file_new(path_aug_S)
data = dp.pre_aug_new(head_I,data_I,data_S)
sys_type={}
time_G = [[] for i in range(100)]
time_R = [[] for i in range(100)]
time_E = [[] for i in range(100)]
time_C = [[] for i in range(100)]
time_TRP = []
data_G = [[] for i in range(100)]
data_R = [[] for i in range(100)]
data_E = [[] for i in range(100)]
data_C = [[] for i in range(100)]
sys_type["C"] = "ION2"
sys_type["G"] = "ION1"
sys_type["E"] = "ION1"  
for time in data.keys():
    plot_time = (time - cov_Time) / 3600
    if (plot_time > begT and plot_time < begT + LastT):
        for sat in data[time].keys():
            prn = int(sat[1:3])
            if sys_type[sat[0]] not in data[time][sat].keys():
                continue
            if abs(data[time][sat][sys_type[sat[0]]]) > -1:
                if sat[0] == "C" and sys_type[sat[0]] in data[time][sat].keys():
                    data_C[prn-1].append(data[time][sat][sys_type[sat[0]]])
                    time_C[prn-1].append(plot_time)
                if sat[0] == "G" and sys_type[sat[0]] in data[time][sat].keys():
                    data_G[prn-1].append(data[time][sat][sys_type[sat[0]]])
                    time_G[prn-1].append(plot_time)
                if sat[0] == "E" and sys_type[sat[0]] in data[time][sat].keys():
                    data_E[prn-1].append(data[time][sat][sys_type[sat[0]]])
                    time_E[prn-1].append(plot_time)
for i in range(100):
    G,E,C = True,True,True
    num = len(time_G[i])
    if num < 1:
        G = False
    num = len(time_E[i])
    if num < 1:
        E = False
    num = len(time_C[i])
    if num < 1:
        C = False
    E=False
    if G:
        axP[2].scatter(time_G[i],data_G[i],s=1)
    if E:
        axP[2].scatter(time_E[i],data_E[i],s=1)
    if C:
        axP[2].scatter(time_C[i],data_C[i],s=1)
font2 = {'family' : 'Times new roman',
            'weight' : 600,
            'size'   : 15,
                }
axP[2].set_ylabel("Difference of Ionosphere Delay correction(m)",font2)
axP[2].set_xticks(XTick)
axP[2].set_xticklabels(XLabel,fontsize="x-large")
# axP[2].set_yticklabels([-0.2,-0.1,0,0.1,0.2],fontsize="x-large")
axP[2].set_ylim(-0.2,0.2)
plt.show()