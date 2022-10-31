'''
Author: HanJunjie HanJunjie@whu.edu.cn
Date: 2022-05-13 12:56:14
LastEditors: HanJunjie HanJunjie@whu.edu.cn
LastEditTime: 2022-09-01 20:20:56
FilePath: /plot-py-tool/main/hjj_draw_sigma_ion.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
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

path = r"E:\1Master_2\Paper_Grid\Res_FromServer_New\ResSig\Residual_305.txt"
[Residual,Dis,Num]= rf.H_open_residual_grid(path)

all_data = {}

begT=1
for time in Residual:
    begsow = time
    break
convtime = time-begT*3600

all_data = {}
#plot
boxG,boxE,boxC=[],[],[]
satG,satE,satC=[],[],[]
dataG,dataE,dataC=[[] for i in range(60)],[[] for i in range(60)],[[] for i in range(60)]

timeG,timeE,timeC=[[] for i in range(60)],[[] for i in range(60)],[[] for i in range(60)]
#data_convert
for time in Residual:
    for sat in Residual[time]:
        sys = sat[0:1]
        prn = int(sat[1:3])
        site_site = sat[4:13]
        # if site_site != "N028-XGXN":
        #     continue
        if site_site not in all_data.keys():
            all_data[site_site]={}
            all_data[site_site]["G"] = []
            all_data[site_site]["E"] = []
            all_data[site_site]["C"] = []
        all_data[site_site][sys].append(Residual[time][sat])
        if sys == "G":
            timeG[prn].append((time-convtime)/3600)
            dataG[prn].append(Residual[time][sat])
        if sys == "E":
            timeE[prn].append((time-convtime)/3600)
            dataE[prn].append(Residual[time][sat])
        if sys == "C":
            timeC[prn].append((time-convtime)/3600)
            dataC[prn].append(Residual[time][sat])
Mean = {}
Mean["G"] = []
Mean["E"] = []
Mean["C"] = []
Mean_plot = {}
Mean_plot["G"] = []
Mean_plot["E"] = []
Mean_plot["C"] = []
Dis_plot = {}
Dis_plot["G"] = []
Dis_plot["E"] = []
Dis_plot["C"] = []

Dis_sort = {}
Dis_sort["G"] = []
Dis_sort["E"] = []
Dis_sort["C"] = []
for site_site in all_data:
    for sys in all_data[site_site]:
        if Num[site_site][sys] < 100:
            continue
        Dis_plot[sys].append(Dis[site_site])
        Dis_sort[sys].append(Dis[site_site])
        Mean[sys].append(np.mean(all_data[site_site][sys]))
Dis_sort["G"].sort()
Dis_sort["E"].sort()
Dis_sort["C"].sort()

for sys in Dis_sort:
    for i in range(len(Dis_sort[sys])):
        for j in range(len(Dis_plot[sys])):
            if (Dis_sort[sys][i] == Dis_plot[sys][j]):
                Mean_plot[sys].append(Mean[sys][j])
figP,axP = plt.subplots(3,1,figsize=(12,10),sharey=False,sharex=False)
axP[0].plot(Dis_sort["G"],Mean_plot["G"])
axP[1].plot(Dis_sort["E"],Mean_plot["E"])
axP[2].plot(Dis_sort["C"],Mean_plot["C"])
# axP.legend(["G","E","C"])

#scatter
# figP,axP = plt.subplots(3,1,figsize=(12,10),sharey=False,sharex=False)
# axP[2].set_xlabel('PRN')
# axP[1].set_ylabel('Sigma of DCB observation/m')
# axP[0].set_title('G')
# axP[1].set_title('E')
# axP[2].set_title('C')
# # axP[0].set_ylim(0,0.05)
# # axP[1].set_ylim(0,0.05)
# # axP[2].set_ylim(0,0.05)
# for i in range(3):
#     axP[i].grid(linestyle='--',linewidth=0.2, color='black',axis='both')
#     # axP[i].set_ylim(0,0.06)
#     box = axP[i].get_position()
#     axP[i].set_position([box.x0, box.y0, box.width*0.99, box.height])
# for i in range(60):
#     G,E,C=True,True,True
#     num = len(timeG[i])
#     if num < 1:
#         G = False
#     num = len(timeE[i])
#     if num < 1:
#         E = False
#     num = len(timeC[i])
#     if num < 1:
#         C = False
    
#     if G:
#         boxG.append(dataG[i])
#         sat = 'G'+'%02d' % (i)
#         satG.append(sat)
#         #axP[0].scatter(timeG[i],dataG[i],s=1)
#     if E:
#         boxE.append(dataE[i])
#         sat = 'E'+'%02d' % (i)
#         satE.append(sat)
#     if C:
#         boxC.append(dataC[i])
#         sat = 'C'+'%02d' % (i)
#         satC.append(sat)
# axP[0].boxplot(boxG,labels=satG,meanline=True,showmeans=True,showfliers=False)
# axP[1].boxplot(boxE,labels=satE,meanline=True,showmeans=True,showfliers=False)
# axP[2].boxplot(boxC,labels=satC,meanline=True,showmeans=True,showfliers=False)

plt.show()