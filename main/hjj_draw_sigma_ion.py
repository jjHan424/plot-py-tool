'''
Author: HanJunjie HanJunjie@whu.edu.cn
Date: 2022-05-13 12:56:14
LastEditors: HanJunjie HanJunjie@whu.edu.cn
LastEditTime: 2022-06-06 12:15:03
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

path_G = "/Users/hjj/Documents/HJJ/Master_1/IonoGrid/Dynamic/20211205/Result/client-grid/GPS.txt"
sigma_G= rf.H_open_sigma_grid(path_G)
path_E = "/Users/hjj/Documents/HJJ/Master_1/IonoGrid/Dynamic/20211205/Result/client-grid/GAL.txt" 
sigma_E= rf.H_open_sigma_grid(path_E)
path_C = "/Users/hjj/Documents/HJJ/Master_1/IonoGrid/Dynamic/20211205/Result/client-grid/BDS.txt" 
sigma_C= rf.H_open_sigma_grid(path_C)

all_data = {}
all_data["GPS"] = sigma_G
all_data["GAL"] = sigma_E
all_data["BDS"] = sigma_C

begT=8
for time in sigma_G:
    begsow = time
    break
convtime = time-8*3600


#plot
boxG,boxE,boxC=[],[],[]
satG,satE,satC=[],[],[]
dataG,dataE,dataC=[[] for i in range(60)],[[] for i in range(60)],[[] for i in range(60)]

timeG,timeE,timeC=[[] for i in range(60)],[[] for i in range(60)],[[] for i in range(60)]
#data_convert
for time in sigma_G:
    for sat in sigma_G[time]:
        prn = int(sat[1:3])
        timeG[prn].append((time-convtime)/3600)
        dataG[prn].append(sigma_G[time][sat])
for time in sigma_E:
    for sat in sigma_E[time]:
        prn = int(sat[1:3])
        timeE[prn].append((time-convtime)/3600)
        dataE[prn].append(sigma_E[time][sat])
for time in sigma_C:
    for sat in sigma_C[time]:
        prn = int(sat[1:3])
        timeC[prn].append((time-convtime)/3600)
        dataC[prn].append(sigma_C[time][sat])
#scatter
figP,axP = plt.subplots(3,1,figsize=(12,10),sharey=False,sharex=False)
axP[2].set_xlabel('PRN')
axP[1].set_ylabel('Sigma of DCB observation/m')
axP[0].set_title('G')
axP[1].set_title('E')
axP[2].set_title('C')
# axP[0].set_ylim(0,0.08)
# axP[1].set_ylim(0,0.06)
# axP[2].set_ylim(0,0.07)
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
        #axP[0].scatter(timeG[i],dataG[i],s=1)
    if E:
        boxE.append(dataE[i])
        sat = 'E'+'%02d' % (i)
        satE.append(sat)
    if C:
        boxC.append(dataC[i])
        sat = 'C'+'%02d' % (i)
        satC.append(sat)
axP[0].boxplot(boxG,labels=satG,meanline=True,showmeans=True,showfliers=False)
axP[1].boxplot(boxE,labels=satE,meanline=True,showmeans=True,showfliers=False)
axP[2].boxplot(boxC,labels=satC,meanline=True,showmeans=True,showfliers=False)

plt.show()


