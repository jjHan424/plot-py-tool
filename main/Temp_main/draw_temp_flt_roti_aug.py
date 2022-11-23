'''
Author: HanJunjie HanJunjie@whu.edu.cn
Date: 2022-07-16 14:31:10
LastEditors: HanJunjie HanJunjie@whu.edu.cn
LastEditTime: 2022-08-08 17:48:17
FilePath: /plot-py-tool/main/draw_temp_flt_roti_aug.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
from cProfile import label
import os
import sys
import math
from turtle import color
#from main.draw_flt_static import REF_XYZ
sys.path.insert(0,os.path.dirname(__file__)+'/..')
sys.path.insert(0,os.path.dirname(__file__)+'/../..')
import numpy as np
import readfile as rf
import matplotlib as mpl
mpl.use("TkAgg")
import matplotlib.pyplot as plt
# plt.style.use(['science'])
import dataprocess as dp
import draw as dr
import seaborn as sns
import trans as tr
#path set
# path_flt = "/Volumes/H_GREAT/WangBo_Paper/2021305/test/Frequency2_UPD_HK_GBM/HKSC-GEC-AR-2.flt"
path_flt = r"G:\WangBo_Paper\2021305\HKSC-GC-AR-2.flt"
path_roti = r"G:\WangBo_Paper\ROTI_GF\ISRM209-309\HKSC2021305_GEC.ismr"
path_aug_I = r"E:\1Master_2\Paper_Grid\Res_FromServer_New\Client-New\client-Aug-305\HKSC-GEC-I.aug"
path_aug_S = r"E:\1Master_2\Paper_Grid\Res_FromServer_New\Server\2021305\HKSC-GEC.aug"
figP,axP = plt.subplots(3,1,figsize=(19,10),sharey=False,sharex=True)
#Time
time="UTC"
starttime=8
year = 2021
mon=11
day=1
LastT=10
deltaT=2
all=False
colormap = sns.color_palette(['xkcd:green','xkcd:blue','xkcd:red', 'xkcd:brown', 'xkcd:pink', 'xkcd:purple'],100)
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
    cur_Str_X = '%d' % (starttime % 24) 
    XLabel.append(cur_Str_X)
    XTick.append(int(starttime))       
while starttime < math.ceil(end_Time):
    starttime = starttime + deltaT
    cur_Str_X = '%d' % (starttime % 24)
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
axP[0].scatter(time1,dataE,s=ss,color=colormap[0])
axP[0].scatter(time1,dataN,s=ss,color=colormap[1])
axP[0].scatter(time1,dataU,s=ss,color=colormap[2])
font2 = {'family' : 'Arial',
            'weight' : 600,
            'size'   : 20,
                }
axP[0].set_ylabel("Positioning errors(m)",font2)
font2 = {'family' : 'Times new roman',
            'weight' : 600,
            'size'   : 20,
                }

axP[0].set_xticks(XTick)
axP[0].set_xticklabels(XLabel)
# axP[0].set_yticks([-1.00,-0.75,-0.50,-0.25,0.00,0.25,0.50,0.75,1.00])
# axP[0].set_yticklabels(["-1.00","","-0.50","","0.00","","0.50","","1.00"],fontsize=25)
axP[0].set_yticks([-1.00,0.00,1.00])
axP[0].set_yticklabels(["-1.00","0.00","1.00"],fontsize=20)
axP[0].legend(["East direction","North direction","Up direction"],markerscale=2,prop=font2,loc=1,ncol=3)
axP[0].set_xlim(8,18)
axP[1].set_xlim(8,18)
axP[2].set_xlim(8,18)


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
        axP[1].scatter(time_G[i],data_G[i],s=1,color=colormap[i])
    if E:
        axP[1].scatter(time_E[i],data_E[i],s=1,color=colormap[i])
    if C:
        axP[1].scatter(time_C[i],data_C[i],s=1,color=colormap[i])
font2 = {'family' : 'Arial',
            'weight' : 600,
            'size'   : 20,
                }
axP[1].set_ylabel("ROTI(TECU/min)",font2)
axP[1].set_xticks(XTick)
# axP[2].set_yticklabels([-0.2,-0.1,0,0.1,0.2],fontsize="x-large")
axP[1].set_ylim(0,2)
axP[1].set_yticks([0,1,2])
# axP[1].set_yticks([0,0.25,0.50,0.75,1])
axP[1].set_yticklabels(["0.00","1.00","2.00"],fontsize=20)
###-------------AUG-GEC--------------###
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
# sys_type["C"] = "L2"
# sys_type["G"] = "L1"
# sys_type["E"] = "L1"  
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
    # E=False

    # G,E=False,False
    # C=True
    if G:
        axP[2].scatter(time_G[i],data_G[i],s=1)
    if E:
        axP[2].scatter(time_E[i],data_E[i],s=1)
    if C:
        axP[2].scatter(time_C[0],data_C[0],s=1)
font2 = {'family' : 'Arial',
            'weight' : 600,
            'size'   : 20,
                }
axP[2].set_ylabel("Ionosphere errors(m)",font2)
axP[2].set_xticks(XTick)
axP[2].set_xticklabels(XLabel,fontsize=20)
axP[2].set_yticks([-0.2,0,0.2])
axP[2].set_yticklabels(["-0.20","0.00","0.20"],fontsize=20)
axP[2].set_ylim(-0.2,0.2)
# axP[2].set_yticklabels(["2.400","2.425","2.450","2.475","2.500","2.525","2.550","2.575","2.600"],fontsize=20)
# axP.set_title("GEC",font2)
font2 = {'family' : 'Arial',
            'weight' : 600,
            'size'   : 25,
                }
axP[2].set_xlabel("Time(h)",font2)
axP[0].grid(False)
axP[1].grid(False)
axP[2].grid(False)

###-------------AUG-C--------------###
# [head_I,data_I] = rf.open_aug_file_new(path_aug_I)
# [head_S,data_S] = rf.open_aug_file_new(path_aug_S)
# data = dp.pre_aug_new(head_I,data_I,data_S)
# sys_type={}
# time_G = [[] for i in range(100)]
# time_R = [[] for i in range(100)]
# time_E = [[] for i in range(100)]
# time_C = [[] for i in range(100)]
# time_TRP = []
# data_G = [[] for i in range(100)]
# data_R = [[] for i in range(100)]
# data_E = [[] for i in range(100)]
# data_C = [[] for i in range(100)]
# sys_type["C"] = "TRP1"
# sys_type["G"] = "TRP1"
# sys_type["E"] = "TRP1"  
# for time in data_I.keys():
#     plot_time = (time - cov_Time) / 3600
#     if (plot_time > begT and plot_time < begT + LastT):
#         for sat in data_I[time].keys():
#             prn = int(sat[1:3])
#             if sys_type[sat[0]] not in data_I[time][sat].keys():
#                 continue
#             if abs(data_I[time][sat][sys_type[sat[0]]]) > -1:
#                 data_C[0].append(data_I[time][sat][sys_type[sat[0]]])
#                 time_C[0].append(plot_time)
#                 break
#                 # if sat[0] == "C" and sys_type[sat[0]] in data_I[time][sat].keys():
#                 #     data_C[prn-1].append(data_I[time][sat][sys_type[sat[0]]])
#                 #     time_C[prn-1].append(plot_time)
#                 # if sat[0] == "G" and sys_type[sat[0]] in data_I[time][sat].keys():
#                 #     data_G[prn-1].append(data_I[time][sat][sys_type[sat[0]]])
#                 #     time_G[prn-1].append(plot_time)
#                 # if sat[0] == "E" and sys_type[sat[0]] in data_I[time][sat].keys():
#                 #     data_E[prn-1].append(data_I[time][sat][sys_type[sat[0]]])
#                 #     time_E[prn-1].append(plot_time)
# for i in range(100):
#     G,E,C = True,True,True
#     num = len(time_G[i])
#     if num < 1:
#         G = False
#     num = len(time_E[i])
#     if num < 1:
#         E = False
#     num = len(time_C[i])
#     if num < 1:
#         C = False
#     E=False

#     G,E=False,False
#     C=True
#     if G:
#         axP[2].scatter(time_G[i],data_G[i],s=1)
#     if E:
#         axP[2].scatter(time_E[i],data_E[i],s=1)
#     if C:
#         axP[1].scatter(time_C[0],data_C[0],s=1)
# font2 = {'family' : 'Arial',
#             'weight' : 600,
#             'size'   : 25,
#                 }
# axP[1].set_ylabel("ZTD(m)",font2)
# axP[1].set_xticks(XTick)
# axP[1].set_xticklabels(XLabel,fontsize=25)
# # axP[2].set_yticklabels([-0.2,-0.1,0,0.1,0.2],fontsize="x-large")
# axP[1].set_ylim(2.40,2.60)
# axP[1].set_yticks([2.400,2.425,2.450,2.475,2.500,2.525,2.550,2.575,2.600])
# axP[1].set_yticklabels(["2.400","2.425","2.450","2.475","2.500","2.525","2.550","2.575","2.600"],fontsize=20)
# axP[1].set_xlabel("UTC",font2)
# axP[1].set_title("C",font2)
# axP[1].grid(False)
# axP[1].grid(False)
# axP[1].grid(False)
plt.savefig("E:\\0Project\\Review\\HKSC_GC_PPPRTK_ROTI_AUG.pdf")
plt.show()