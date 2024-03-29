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
import scienceplots
plt.style.use(['science','no-latex'])
import dataprocess as dp
import draw as dr
import seaborn as sns
import trans as tr
import glv as glv
import seaborn as sns

font_title = {'family' : 'Arial', 'weight' : 300, 'size' : 30}
font_label = {'family' : 'Arial', 'weight' : 300, 'size' : 20}
font_tick = {'family' : 'Arial', 'weight' : 300, 'size' : 30}
font_legend = {'family' : 'Arial', 'weight' : 300, 'size' : 20}
font_text = {'family' : 'Times new roman','weight' : 300,'size'   : 20}
xtick_size = 15
color_list = sns.color_palette("Set1")

#Diff-EleSun
file_list = ["/Users/hanjunjie/Master_3/1-IUGG/ResFromServer/PLOT_EPN_TIME_ELESUN_IONO.txt",
             "/Users/hanjunjie/Master_3/1-IUGG/ResFromServer/PLOT_WH_TIME_ELESUN_IONO.txt",
             "/Users/hanjunjie/Master_3/1-IUGG/ResFromServer/PLOT_HK_TIME_ELESUN_IONO.txt"]
mode_list = ["Net. A","Net. B","Net. C"]
# filename = r"E:\1Master_2\Paper_Grid\Res_FromServer_New\Fig\Ele_Wgt-New\diff-meanele.txt"
Diff,Ele,Time,Time_ele = {},{},{},{}
ab=[0.0003479,0.004675]
for i in range(len(file_list)):
    filename = file_list[i]
    if mode_list[i] not in Diff.keys():
        Diff[mode_list[i]],Ele[mode_list[i]],Time[mode_list[i]],Time_ele[mode_list[i]] = [],[],[],[]
    with open(filename,'rt') as f:
        for line in f:
            value = line.split()
            if value[0] == "NaN":
                continue

            Diff[mode_list[i]].append(float(value[2])*100)
            
            if mode_list[i] == "Net. A":
                cur_time = float(value[0])+3600
            else:
                cur_time = float(value[0])+8*3600
            if cur_time>86400:
                cur_time = cur_time-86400
            Time[mode_list[i]].append(cur_time/3600)
            # print(cur_time%1800)
            # if cur_time%1785 == 0:
            Ele[mode_list[i]].append(float(value[1]))
            Time_ele[mode_list[i]].append(cur_time/3600)
a,b,c,d=[0.183551,-0.04425],[-0.422462,-0.005197],[0.248225,0.04779],[-0.009081,0.0002749]
j=0
for i in Time[mode_list[0]]:
    if (i)*3600-3600 == 21885:
        start = j
    if (i)*3600-3600 == 58035:
        end = j
        break
    j=j+1
figP,axP = plt.subplots(3,1,figsize=(6,8),sharey=False,sharex=True)
for i in range(len(file_list)):
    if i == 0:
        x=np.array(Time[mode_list[i]][start:end])
        delta_y = np.min(Diff[mode_list[i]][start:end])
        min_x = np.min(x)
        max_x = np.max(x)
        x=np.array(Time[mode_list[i]][start+50:end+100])
        x = (x-min_x)/(max_x-min_x)
        y=(a[i]*x*x*x+b[i]*x*x+c[i]*x+d[i])*100+delta_y
        # print(np.min(np.array(Diff[mode_list[i]])))
        x=np.array(Time[mode_list[i]][start+50:end+100])
        axP[i].plot(x[y>1.2],y[y>1.2],linewidth=3.0,linestyle='--',c='k')
        axP[i].set_ylim(0,6)
    axP[i].scatter(Time[mode_list[i]],Diff[mode_list[i]],s=5,c="#0099E5")
    axP2 = axP[i].twinx()
    axP2.scatter(Time_ele[mode_list[i]],Ele[mode_list[i]],c="#34BF49",marker='.',s=1)
    axP2.grid(False)
    if i == 0:
        axP2.set_ylim(0,20)
        axP2.set_yticks([0,5,10,15,20])
    elif i== 2:
        axP2.set_ylim(0,60)
        axP2.set_yticks([0,15,30,45,60])
    else:
        axP2.set_ylim(0,44)
        axP2.set_yticks([0,11,22,33,44])
    if i==2:
        
        # axP[i].set_yticks([0,1.5,3,4.5,6])
        axP[i].set_yticks([0,0.3,0.6,0.9,1.2])
        axP[i].set_ylim(0,1.2)
    elif i==1:
        axP[i].set_yticks([0,1,2,3,4])
        axP[i].set_yticklabels(["0.0","1.0","2.0","3.0","4.0"])
        zz = axP2.set_ylabel("Elevation of Sun (deg)",font_label)
        zz.set_color("#34BF49")
    else:
        axP[i].set_yticks([0,1.5,3,4.5,6])
    axP[i].set_xticks([0,6,12,18,24])
    axP[i].set_xlim(0,24)
    labels = axP2.get_yticklabels()+axP[i].get_yticklabels()+axP[i].get_xticklabels()
    [label.set_fontsize(xtick_size) for label in labels]
    [label.set_fontname('Arial') for label in labels]
    axP2.spines['right'].set(color = "#34BF49",linewidth = 2,linestyle = "-")
    axP2.tick_params(axis = 'y',length=6, width=2, color="#34BF49", labelcolor="#34BF49")
    labels = axP2.get_yticklabels()
    # labels.set_color("#34BF49")
    # [label.set_color("#34BF49") for label in labels]
    axP[i].spines['left'].set(color = "#0099E5",linewidth = 2,linestyle = "-")
    axP[i].spines['left'].set_color("#0099E5")
    axP[i].tick_params(axis = 'y',length=6, width=2, color="#0099E5", labelcolor="#0099E5")
    
j=0
time_array = np.array(Time[mode_list[1]])
index = (time_array*3600 == 66555)
for i in Time[mode_list[1]]:
    if (i) == 5.5:
        start = j
    if (i)*3600 == 66555:
        end = j
        break
    j=j+1
# start = j-1267
for i in range(len(file_list)):
    if i == 1:
        index_1 = (21345 < time_array*3600)
        index_2 = 66555 > time_array*3600
        index = index_1 & index_2
        x=np.array(Time[mode_list[i]])[index]
        delta_y = np.min(Diff[mode_list[i]][start:end])
        min_x = np.min(x)
        max_x = np.max(x)
        x=np.array(Time[mode_list[i]])[index]
        x = (x-min_x)/(max_x-min_x)
        x = np.sort(x)
        y=(a[i]*x*x*x+b[i]*x*x+c[i]*x+d[i])*100+delta_y
        # print(np.min(np.array(Diff[mode_list[i]])))
        x=np.array(Time[mode_list[i]])[index]
        x = np.sort(x)
        axP[i].plot(x,y,linewidth=3.0,linestyle='--',c='k')
        axP[i].set_ylim(0,4)
for i in range(3):
    ax_range = axP[i].axis()
    axP[i].text(ax_range[0],ax_range[3],mode_list[i],font_label)
axP[2].set_ylim(0,1.2)
zz = axP[1].set_ylabel("Ionospheric errors (cm)",font_label,labelpad = 7)
zz.set_color("#0099E5")
axP[2].set_xlabel("Local time (hour)",font_label)
axP[0].legend([r"$y = a{x^3} + b{x^2} + cx + d$"],prop=font_legend,
        framealpha=1,facecolor='w',numpoints=5, frameon=False,bbox_to_anchor=(1,1.24),loc=1,
        borderaxespad=0)
leg = axP[0].get_legend()
for legobj in leg.legendHandles:
    legobj.set_linewidth(3)
    # legobj.set_linelength(10)
    legobj.set_color("black")
    legobj.set_linestyle("--")
plt.savefig("/Users/hanjunjie/Desktop/Image-1/Diff_VS_EleSun.jpg",dpi=300)
plt.show()