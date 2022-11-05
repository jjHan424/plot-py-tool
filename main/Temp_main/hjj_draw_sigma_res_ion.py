'''
Author: HanJunjie HanJunjie@whu.edu.cn
Date: 2022-05-13 12:56:14
LastEditors: HanJunjie HanJunjie@whu.edu.cn
LastEditTime: 2022-09-01 22:28:07
FilePath: /plot-py-tool/main/hjj_draw_sigma_ion.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
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

path_G = r"E:\1Master_2\Paper_Grid\Res_FromServer_New\ResSig\HKMW-Sigma-312.txt"
[sigma_G,sigma_E,sigma_C]= rf.H_open_sigma_grid(path_G,"G")

all_data = {}
all_data["GPS"] = sigma_G
all_data["GAL"] = sigma_E
all_data["BDS"] = sigma_C
year=2021
mon=11
day=8
starttime=2
LastT=22
deltaT=2
time = "UTC+8"


if "+" in time:
    end_time = len(time)
    delta_Time = int(time[3:end_time]) + starttime
    begT = int(time[3:end_time]) + starttime
else:
    delta_Time = starttime
    begT=starttime
#for time in data[mode[0]].keys():
secow_start = tr.ymd2gpst(year,mon,day,0,00,00)
doy = tr.ymd2doy(year,mon,day,0,00,00)
cov_Time = secow_start[1] - 0 * 3600
if "+" in time:
    cov_Time = secow_start[1] - int(time[3:end_time]) * 3600
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



#plot
boxG,boxE,boxC=[],[],[]
satG,satE,satC=[],[],[]
dataG,dataE,dataC=[[] for i in range(60)],[[] for i in range(60)],[[] for i in range(60)]

timeG,timeE,timeC=[[] for i in range(60)],[[] for i in range(60)],[[] for i in range(60)]
#data_convert
for cur_time in sigma_G:
    plot_time = (cur_time-cov_Time) / 3600
    if ((plot_time >= begT and plot_time <= (begT + LastT))):
        for sat in sigma_G[cur_time]:
            prn = int(sat[1:3])
            timeG[prn].append(plot_time)
            dataG[prn].append(sigma_G[cur_time][sat])
for cur_time in sigma_E:
    plot_time = (cur_time-cov_Time) / 3600
    if ((plot_time >= begT and plot_time <= (begT + LastT))):
        for sat in sigma_E[cur_time]:
            prn = int(sat[1:3])
            timeE[prn].append(plot_time)
            dataE[prn].append(sigma_E[cur_time][sat])
for cur_time in sigma_C:
    plot_time = (cur_time-cov_Time) / 3600
    if ((plot_time >= begT and plot_time <= (begT + LastT))):
        for sat in sigma_C[cur_time]:
            prn = int(sat[1:3])
            timeC[prn].append(plot_time)
            dataC[prn].append(sigma_C[cur_time][sat])
#scatter
figP,axP = plt.subplots(3,1,figsize=(12,10),sharey=False,sharex=True)
axP[2].set_xlabel('Time')
axP[1].set_ylabel('Residual of DCB observation/m')
axP[0].set_title('G')
axP[1].set_title('E')
axP[2].set_title('C')
# axP[0].set_ylim(0,0.05)
# axP[1].set_ylim(0,0.05)
# axP[2].set_ylim(0,0.05)
for i in range(3):
    axP[i].grid(linestyle='--',linewidth=0.2, color='black',axis='both')
    # axP[i].set_ylim(0,0.06)
    box = axP[i].get_position()
    axP[i].set_position([box.x0, box.y0, box.width*0.99, box.height])
for i in range(60):
    G,E,C=True,True,True
    num = len(timeG[i])
    if num < 1:
        G = False
    num = len(timeE[i])
    if num < 1:
        E = False
    num = len(timeC[i])
    if num < 1:
        C = False
    
    if G:
        boxG.append(dataG[i])
        sat = 'G'+'%02d' % (i)
        satG.append(sat)
        axP[0].scatter(timeG[i],dataG[i],s=1)
    if E:
        boxE.append(dataE[i])
        sat = 'E'+'%02d' % (i)
        satE.append(sat)
        axP[1].scatter(timeE[i],dataE[i],s=1)
    if C:
        boxC.append(dataC[i])
        sat = 'C'+'%02d' % (i)
        satC.append(sat)
        axP[2].scatter(timeC[i],dataC[i],s=1)
# axP[0].boxplot(boxG,labels=satG,meanline=True,showmeans=True,showfliers=False)
# axP[1].boxplot(boxE,labels=satE,meanline=True,showmeans=True,showfliers=False)
# axP[2].boxplot(boxC,labels=satC,meanline=True,showmeans=True,showfliers=False)
axP[2].set_xticks(XTick)
axP[2].set_xticklabels(XLabel)
plt.show()


