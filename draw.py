'''
Author: Junjie Han
Date: 2021-09-23 10:14:18
LastEditTime: 2022-08-30 20:26:43
LastEditors: HanJunjie HanJunjie@whu.edu.cn
Description: In User Settings Edit
FilePath: /plot-toolkit-master/jjHan_py_plot/draw.py
'''

from asyncore import write
from matplotlib.markers import MarkerStyle
import numpy as np
import matplotlib as mpl
mpl.use("TkAgg")
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
plt.style.use(['science','grid','no-latex'])
from numpy.core.fromnumeric import shape, size
import dataprocess as dp
import matplotlib.colors as colors
from matplotlib.pyplot import MultipleLocator
import seaborn as sns
import math
import trans as tr
font = {'family' : 'Arial',
		'weight' : 500,
		'size'   : 20,
}

font_title = {'family' : 'Times New Roman', 'weight' : 700, 'size' : 45}
font_label = {'family' : 'Times New Roman', 'weight' : 600, 'size' : 29}
font_tick = {'family' : 'Times New Roman', 'weight' : 400, 'size' : 30}
# font_legend = {'family' : 'Times New Roman', 'weight' : 600, 'size' : 22}
font_legend = {'family' : 'Times New Roman', 'weight' : 600, 'size' : 15}
font_text = {'family' : 'Times new roman','weight' : 500,'size'   : 28}
xtick_size = 26
color_list = sns.color_palette("Set1")

def xtick(time,year,mon,day,starttime,LastT,deltaT):
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

    # for i in range(delta_X):
    #     starttime = starttime + deltaT
    #     cur_Str_X = '%02d' % (starttime % 24) + ":{:0>2}".format(int((starttime-int(starttime))*60))
    #     XLabel.append(cur_Str_X)
    #     XTick.append((starttime))       
    
    while starttime < end_Time:
        starttime = starttime + deltaT
        if (starttime >= end_Time):
            cur_Str_X = '%02d' % (end_Time % 24) + ":{:0>2}".format(round((end_Time-int(end_Time))*60))
            XLabel.append(cur_Str_X)
            XTick.append((end_Time))
            break
        cur_Str_X = '%02d' % (starttime % 24) + ":{:0>2}".format(round((starttime-int(starttime))*60))
        XLabel.append(cur_Str_X)
        XTick.append((starttime))
    
    return (XLabel,XTick,cov_Time,begT,LastT)


def plot_aug_GEC(time_G = [], aug_G = [], time_E = [], aug_E = [], time_C = [], aug_C = [],mode = 'P' ,save='save_fig_path', show = False):
    RMS_G,MEAN_G,STD_G = [[],[]],[[],[]],[[],[]]
    RMS_E,MEAN_E,STD_E = [[],[]],[[],[]],[[],[]]
    RMS_C,MEAN_C,STD_C = [[],[]],[[],[]],[[],[]]
    if mode == 'P':
        f1=0
        f2=1
        figP,axP = plt.subplots(3,2,figsize=(20,10),sharey=True,sharex=True)
        ymin = -2
        ymax = 2
        col = 2
    elif mode == 'L':
        f1=2
        f2=3
        figP,axP = plt.subplots(3,2,figsize=(20,10),sharey=True,sharex=True)
        ymin = -2
        ymax = 2
        col = 2
    elif mode == 'ion':
        f1=5
        ymin = -0.1
        ymax = 0.1
        col = 1
        figP,axP = plt.subplots(3,1,figsize=(20,10),sharey=True,sharex=True)
    elif mode == 'trp':
        f1=4
        ymin = -0.2
        ymax = 0.2
        col = 1
        figP,axP = plt.subplots(3,1,figsize=(20,10),sharey=True,sharex=True)
    else:
        print("Wrong mode")
    savedir = save + mode + '.png'
    G_L,E_L,C_L = [],[],[]

    if mode == 'P' or mode == 'L':
        axP[2][0].set_xlabel('Time(Hours of GPS Week)')
        axP[2][1].set_xlabel('Time(Hours of GPS Week)')
        axP[1][0].set_ylabel('Difference of augmentation correction/m',font)
        axP[0][0].set_title('G')
        axP[0][1].set_title('G')
        axP[1][0].set_title('E')
        axP[1][1].set_title('E')
        axP[2][0].set_title('C')
        axP[2][1].set_title('C')
        for i in range(3):
            for j in range(2):
                axP[i][j].grid(linestyle='--',linewidth=0.2, color='black',axis='both')
                axP[i][j].set_ylim(ymin,ymax)
    else:
        axP[2].set_xlabel('Time(Hours of GPS Week)')
        axP[1].set_ylabel('Difference of augmentation correction/m',font)
        axP[0].set_title('G')
        axP[1].set_title('E')
        axP[2].set_title('C')
        for i in range(3):
                axP[i].grid(linestyle='--',linewidth=0.2, color='black',axis='both')
                axP[i].set_ylim(ymin,ymax)
                box = axP[i].get_position()
                axP[i].set_position([box.x0, box.y0, box.width*0.99, box.height])
            

    
    if mode == 'P' or mode == 'L':
        for i in range(33):
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
            if G:
                axP[0][0].scatter(time_G[i],aug_G[i][f1],s=1)
                axP[0][1].scatter(time_G[i],aug_G[i][f2],s=1)
                prn = '%02d' % i
                G_L.append('G'+prn)
                temp = dp.rms(aug_G[i][f1])
                RMS_G[0].append(temp)
                temp = np.std(aug_G[i][f1])
                STD_G[0].append(temp)
                temp = np.mean(aug_G[i][f1])
                MEAN_G[0].append(temp)

                temp = dp.rms(aug_G[i][f2])
                RMS_G[1].append(temp)
                temp = np.std(aug_G[i][f2])
                STD_G[1].append(temp)
                temp = np.mean(aug_G[i][f2])
                MEAN_G[1].append(temp)
            if E:
                axP[1][0].scatter(time_E[i],aug_E[i][f1],s=1)
                axP[1][1].scatter(time_E[i],aug_E[i][f2],s=1)
                prn = '%02d' % i
                E_L.append('E'+prn)
                temp = dp.rms(aug_E[i][f1])
                RMS_E[0].append(temp)
                temp = np.std(aug_E[i][f1])
                STD_E[0].append(temp)
                temp = np.mean(aug_E[i][f1])
                MEAN_E[0].append(temp)

                temp = dp.rms(aug_E[i][f2])
                RMS_E[1].append(temp)
                temp = np.std(aug_E[i][f2])
                STD_E[1].append(temp)
                temp = np.mean(aug_E[i][f2])
                MEAN_E[1].append(temp)
            if C:
                axP[2][0].scatter(time_C[i],aug_C[i][f1],s=1)
                axP[2][1].scatter(time_C[i],aug_C[i][f2],s=1)
                prn = '%02d' % i
                C_L.append('C'+prn)
                temp = dp.rms(aug_C[i][f1])
                RMS_C[0].append(temp)
                temp = np.std(aug_C[i][f1])
                STD_C[0].append(temp)
                temp = np.mean(aug_C[i][f1])
                MEAN_C[0].append(temp)

                temp = dp.rms(aug_C[i][f2])
                RMS_C[1].append(temp)
                temp = np.std(aug_C[i][f2])
                STD_C[1].append(temp)
                temp = np.mean(aug_C[i][f2])
                MEAN_C[1].append(temp)
        
        font2 = {"size":7}
        ax_range = axP[0][0].axis()
        axP[0][1].legend(G_L,prop=font2,
            framealpha=1,facecolor='w',ncol=3,numpoints=5, markerscale=2, 
            bbox_to_anchor=(1.01,1),loc=2,borderaxespad=0)
        axP[1][1].legend(E_L,prop=font2,
            framealpha=1,facecolor='w',ncol=3,numpoints=5, markerscale=2, 
            bbox_to_anchor=(1.01,1),loc=2,borderaxespad=0)
        axP[2][1].legend(C_L,prop=font2,
            framealpha=1,facecolor='w',ncol=3,numpoints=5, markerscale=2, 
            bbox_to_anchor=(1.01,1),loc=2,borderaxespad=0)

        axP[0][0].text(ax_range[0],ax_range[3],r'MEAN={:.4f}cm, RMS={:.4f}cm, STD={:.4f}cm'.format(np.mean(MEAN_G[0])*100, np.mean(RMS_G[0])*100, np.mean(STD_G[0])*100))
        axP[0][1].text(ax_range[0],ax_range[3],r'MEAN={:.4f}cm, RMS={:.4f}cm, STD={:.4f}cm'.format(np.mean(MEAN_G[1])*100, np.mean(RMS_G[1])*100, np.mean(STD_G[1])*100))

        axP[1][0].text(ax_range[0],ax_range[3],r'MEAN={:.4f}cm, RMS={:.4f}cm, STD={:.4f}cm'.format(np.mean(MEAN_E[0])*100, np.mean(RMS_E[0])*100, np.mean(STD_E[0])*100))
        axP[1][1].text(ax_range[0],ax_range[3],r'MEAN={:.4f}cm, RMS={:.4f}cm, STD={:.4f}cm'.format(np.mean(MEAN_E[1])*100, np.mean(RMS_E[1])*100, np.mean(STD_E[1])*100))

        axP[2][0].text(ax_range[0],ax_range[3],r'MEAN={:.4f}cm, RMS={:.4f}cm, STD={:.4f}cm'.format(np.mean(MEAN_C[0])*100, np.mean(RMS_C[0])*100, np.mean(STD_C[0])*100))
        axP[2][1].text(ax_range[0],ax_range[3],r'MEAN={:.4f}cm, RMS={:.4f}cm, STD={:.4f}cm'.format(np.mean(MEAN_C[1])*100, np.mean(RMS_C[1])*100, np.mean(STD_C[1])*100))
    else:
        for i in range(33):
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
            if G:
                axP[0].scatter(time_G[i],aug_G[i][f1],s=1)
                prn = '%02d' % i
                G_L.append('G'+prn)
                temp = dp.rms(aug_G[i][f1])
                RMS_G[0].append(temp)
                temp = np.std(aug_G[i][f1])
                STD_G[0].append(temp)
                temp = np.mean(aug_G[i][f1])
                MEAN_G[0].append(temp)
            if E:
                axP[1].scatter(time_E[i],aug_E[i][f1],s=1)
                prn = '%02d' % i
                E_L.append('E'+prn)
                temp = dp.rms(aug_E[i][f1])
                RMS_E[0].append(temp)
                temp = np.std(aug_E[i][f1])
                STD_E[0].append(temp)
                temp = np.mean(aug_E[i][f1])
                MEAN_E[0].append(temp)
            if C:
                axP[2].scatter(time_C[i],aug_C[i][f1],s=1)
                prn = '%02d' % i
                C_L.append('C'+prn)
                temp = dp.rms(aug_C[i][f1])
                RMS_C[0].append(temp)
                temp = np.std(aug_C[i][f1])
                STD_C[0].append(temp)
                temp = np.mean(aug_C[i][f1])
                MEAN_C[0].append(temp)
        
        font2 = {"size":7}
        ax_range = axP[0].axis()
        axP[0].legend(G_L,prop=font2,
            framealpha=1,facecolor='w',ncol=3,numpoints=5, markerscale=2, 
            bbox_to_anchor=(1.01,1),loc=2,borderaxespad=0)
        axP[0].text(ax_range[0],ax_range[3],r'MEAN={:.4f}cm, RMS={:.4f}cm, STD={:.4f}cm'.format(np.mean(MEAN_G[0])*100, np.mean(RMS_G[0])*100, np.mean(STD_G[0])*100))
        axP[1].legend(E_L,prop=font2,
            framealpha=1,facecolor='w',ncol=3,numpoints=5, markerscale=2, 
            bbox_to_anchor=(1.01,1),loc=2,borderaxespad=0)
        axP[1].text(ax_range[0],ax_range[3],r'MEAN={:.4f}cm, RMS={:.4f}cm, STD={:.4f}cm'.format(np.mean(MEAN_E[0])*100, np.mean(RMS_E[0])*100, np.mean(STD_E[0])*100))
        axP[2].legend(C_L,prop=font2,
            framealpha=1,facecolor='w',ncol=3,numpoints=5, markerscale=2, 
            bbox_to_anchor=(1.01,1),loc=2,borderaxespad=0)
        axP[2].text(ax_range[0],ax_range[3],r'MEAN={:.4f}cm, RMS={:.4f}cm, STD={:.4f}cm'.format(np.mean(MEAN_C[0])*100, np.mean(RMS_C[0])*100, np.mean(STD_C[0])*100))
        

        
    figP.suptitle(mode)
    plt.savefig(savedir)
    if show:
        plt.show()

def plot_aug_G_E_C(data = {},head = {},type = "ION",freq = 1,ylim = 1,starttime = 0,deltaT = 2,LastT=24,time = "UTC",save='',show = False,year = 2021,mon=11,day=1):
    sys_type = {}
    RMS_G,MEAN_G,STD_G = [[],[]],[[],[]],[[],[]]
    RMS_E,MEAN_E,STD_E = [[],[]],[[],[]],[[],[]]
    RMS_C,MEAN_C,STD_C = [[],[]],[[],[]],[[],[]]

    RMS_G1,MEAN_G1,STD_G1 = [[],[]],[[],[]],[[],[]]
    RMS_E1,MEAN_E1,STD_E1 = [[],[]],[[],[]],[[],[]]
    RMS_C1,MEAN_C1,STD_C1 = [[],[]],[[],[]],[[],[]]
    G_L,E_L,C_L = [],[],[]
    if type == 'P':
        f1=0
        f2=1
        figP,axP = plt.subplots(3,2,figsize=(13,8),sharey=True,sharex=True)
        ymin = -ylim
        ymax = ylim
        col = 2
        
        axP[2][0].set_xlabel('Time' + '(' + time + ')')
        axP[2][1].set_xlabel('Time' + '(' + time + ')')
        axP[1][0].set_ylabel('Difference of augmentation correction/m',font)
        axP[0][0].set_title('G-P1')
        axP[0][1].set_title('G-P2')
        axP[1][0].set_title('E-P1')
        axP[1][1].set_title('E-P2')
        axP[2][0].set_title('C-P1')
        axP[2][1].set_title('C-P2')
        for i in range(3):
            for j in range(2):
                axP[i][j].grid(linestyle='--',linewidth=0.2, color='black',axis='both')
                axP[i][j].set_ylim(ymin,ymax)
        type1="P1"
        type2="P2"
        sys_type["C"]["1"] = "P2"
        sys_type["G"]["1"] = "P1"
        sys_type["E"]["1"] = "P1"  
        sys_type["C"]["2"]  = "P7"
        sys_type["G"]["2"]  = "P2"
        sys_type["E"]["2"]  = "P7" 
    elif type == 'L':
        f1=2
        f2=3
        figP,axP = plt.subplots(3,2,figsize=(15,10),sharey=True,sharex=True)
        ymin = -ylim
        ymax = ylim
        col = 2
        axP[2][0].set_xlabel('Time' + '(' + time + ')')
        axP[2][1].set_xlabel('Time' + '(' + time + ')')
        axP[1][0].set_ylabel('Difference of augmentation correction/m',font)
        axP[0][0].set_title('G-L1')
        axP[0][1].set_title('G-L2')
        axP[1][0].set_title('E-L1')
        axP[1][1].set_title('E-L2')
        axP[2][0].set_title('C-L1')
        axP[2][1].set_title('C-L2')
        for i in range(3):
            for j in range(2):
                axP[i][j].grid(linestyle='--',linewidth=0.2, color='black',axis='both')
                # axP[i][j].set_ylim(ymin,ymax)
        sys_type["C"] = {}
        sys_type["G"] = {}
        sys_type["E"] = {}
        sys_type["C"]["1"] = "L2"
        sys_type["G"]["1"] = "L1"
        sys_type["E"]["1"] = "L1"  
        sys_type["C"]["2"]  = "L7"
        sys_type["G"]["2"]  = "L2"
        sys_type["E"]["2"]  = "L7" 
        # sys_type["C"]["1"] = "L1"
        # sys_type["G"]["1"] = "L1"
        # sys_type["E"]["1"] = "L1"  
        # sys_type["C"]["2"]  = "L2"
        # sys_type["G"]["2"]  = "L2"
        # sys_type["E"]["2"]  = "L2" 
    elif type == 'ION':
        f1=5
        ymin = -ylim
        ymax = ylim
        col = 1
        figP,axP = plt.subplots(3,1,figsize=(15,8),sharey=True,sharex=True)
        axP[2].set_xlabel('Time' + '(' + time + ')',font)
        axP[1].set_ylabel('Difference of Ionosphere Delay correction/m',font)
        axP[0].set_title('G',font)
        axP[1].set_title('E',font)
        axP[2].set_title('C',font)
        for i in range(3):
                axP[i].grid(linestyle='--',linewidth=0.2, color='black',axis='both')
                axP[i].set_ylim(ymin,ymax)
                box = axP[i].get_position()
                axP[i].set_position([box.x0, box.y0, box.width*0.99, box.height])
        if freq==1:
            sys_type["C"] = "ION2"
            sys_type["G"] = "ION1"
            sys_type["E"] = "ION1"  
        else:
            sys_type["C"] = "ION7"
            sys_type["G"] = "ION2"
            sys_type["E"] = "ION5" 
    elif type == 'TRP':
        f1=4
        ymin = -ylim
        ymax = ylim
        col = 1
        figP,axP = plt.subplots(1,1,figsize=(12,10),sharey=True,sharex=True)
        axP.set_xlabel('Time' + '(' + time + ')',font)
        axP.set_ylabel('Difference of Troposphere Delay correction/m',font)
        axP.grid(linestyle='--',linewidth=0.2, color='black',axis='both')
        axP.set_ylim(ymin,ymax)
        sys_type["C"]="TRP1"
        sys_type["G"]="TRP1"
        sys_type["E"]="TRP1"
    elif type == 'NSAT':
        f1=4
        ymin = -ylim
        ymax = ylim
        col = 1
        figP,axP = plt.subplots(3,1,figsize=(12,10),sharey=True,sharex=True)
        axP[2].set_xlabel('Time' + '(' + time + ')')
        axP[1].set_ylabel('Number of Sat',font)
        axP[0].set_title('G')
        axP[1].set_title('E')
        axP[2].set_title('C')
        # axP.set_xlabel('Time' + '(' + time + ')')
    elif type == "diffIon":
        f1=5
        ymin = -ylim
        ymax = ylim
        col = 1
        figP,axP = plt.subplots(3,1,figsize=(12,10),sharey=True,sharex=True)
        axP[2].set_xlabel('Time' + '(' + time + ')')
        axP[1].set_ylabel('Difference of Ionosphere Delay correction/m',font)
        axP[0].set_title('G')
        axP[1].set_title('E')
        axP[2].set_title('C')
        for i in range(3):
                axP[i].grid(linestyle='--',linewidth=0.2, color='black',axis='both')
                axP[i].set_ylim(ymin,ymax)
                box = axP[i].get_position()
                axP[i].set_position([box.x0, box.y0, box.width*0.99, box.height])
        if freq==1:
            sys_type["C"] = "dION2"
            sys_type["G"] = "dION1"
            sys_type["E"] = "dION1"  
        
    else:
        print("Wrong mode")
    
    time_G = [[] for i in range(100)]
    time_R = [[] for i in range(100)]
    time_E = [[] for i in range(100)]
    time_C = [[] for i in range(100)]
    time_TRP = []
    data_G = [[] for i in range(100)]
    data_R = [[] for i in range(100)]
    data_E = [[] for i in range(100)]
    data_C = [[] for i in range(100)]
    data_TRP = []
    data_G1 = [[] for i in range(100)]
    data_R1 = [[] for i in range(100)]
    data_E1 = [[] for i in range(100)]
    data_C1 = [[] for i in range(100)]
    
    [XLabel,XTick,cov_Time,begT,LastT]=xtick(time,year,mon,day,starttime,LastT,deltaT)
    if type == "L" or type == "P":
        for time in data.keys():
            plot_time = (time - cov_Time) / 3600
            if (plot_time > begT and plot_time < begT + LastT):
                for sat in data[time].keys():
                    prn = int(sat[1:3])
                    # if abs(data[time][sat][sys_type[sat[0]]]) > -1:
                    if sat[0] == "C":
                        data_C[prn-1].append(data[time][sat][sys_type[sat[0]]["1"]])
                        data_C1[prn-1].append(data[time][sat][sys_type[sat[0]]["2"]])
                        time_C[prn-1].append(plot_time)
                    if sat[0] == "G":
                        data_G[prn-1].append(data[time][sat][sys_type[sat[0]]["1"]])
                        data_G1[prn-1].append(data[time][sat][sys_type[sat[0]]["2"]])
                        time_G[prn-1].append(plot_time)
                    if sat[0] == "E":
                        data_E[prn-1].append(data[time][sat][sys_type[sat[0]]["1"]])
                        data_E1[prn-1].append(data[time][sat][sys_type[sat[0]]["2"]])
                        time_E[prn-1].append(plot_time)
    
    if type == "ION" or type == "diffIon":
        for time in data.keys():
            plot_time = (time - cov_Time) / 3600
            if (plot_time > begT and plot_time < begT + LastT):
                for sat in data[time].keys():
                    prn = int(sat[1:3])
                    if sys_type[sat[0]] not in data[time][sat].keys():
                        continue
                    if abs(data[time][sat][sys_type[sat[0]]]) == 0:
                        continue
                    if abs(data[time][sat][sys_type[sat[0]]]) < 0.1:
                        if sat[0] == "C" and sys_type[sat[0]] in data[time][sat].keys():
                            data_C[prn-1].append(data[time][sat][sys_type[sat[0]]])
                            time_C[prn-1].append(plot_time)
                        if sat[0] == "G" and sys_type[sat[0]] in data[time][sat].keys():
                            data_G[prn-1].append(data[time][sat][sys_type[sat[0]]])
                            time_G[prn-1].append(plot_time)
                        if sat[0] == "E" and sys_type[sat[0]] in data[time][sat].keys():
                            data_E[prn-1].append(data[time][sat][sys_type[sat[0]]])
                            time_E[prn-1].append(plot_time)
    if type == "NSAT":
        for time in data.keys():
            num_C,num_G,num_E = 0,0,0
            plot_time = (time - cov_Time) / 3600
            if (plot_time > begT and plot_time < begT + LastT):
                for sat in data[time].keys():
                    prn = int(sat[1:3])
                    if sat[0] == "C":
                        num_C = num_C + 1
                    if sat[0] == "G":
                        num_G = num_G + 1
                    if sat[0] == "E":
                        num_E = num_E + 1
                
                data_C[0].append(num_C)
                time_C[0].append(plot_time)
                data_G[0].append(num_G)
                time_G[0].append(plot_time)
                data_E[0].append(num_E)
                time_E[0].append(plot_time)
    if type == "TRP":
        for time in data.keys():
            plot_time = (time - cov_Time) / 3600
            if (plot_time > begT and plot_time < begT + LastT):
                for sat in data[time].keys():
                    prn = int(sat[1:3])
                    data_TRP.append(data[time][sat][sys_type[sat[0]]])
                    time_TRP.append(plot_time)
                    break
    if type == "NSAT":
        axP[0].scatter(time_G[0],data_G[0])
        axP[1].scatter(time_E[0],data_E[0])
        axP[2].scatter(time_C[0],data_C[0])
        font_text = {'family' : 'Arial',
		'weight' : 500,
		'size'   : 15,
                }
        mean_Sat_G=np.mean(data_G[0])
        mean_Sat_E=np.mean(data_E[0])
        mean_Sat_C=np.mean(data_C[0])
        axP[2].set_xticks(XTick)
        axP[1].set_xticks(XTick)
        axP[0].set_xticks(XTick)
        axP[2].set_xticklabels(XLabel)
    if type == "ION" or type == "diffIon":
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
                if G:
                    axP[0].scatter(time_G[i],data_G[i],s=1)
                    prn = '%02d' % (i + 1)
                    G_L.append('G'+prn)
                    temp = dp.rms(data_G[i])
                    RMS_G[0].append(temp)
                    temp = np.std(data_G[i])
                    STD_G[0].append(temp)
                    temp = np.mean(data_G[i])
                    MEAN_G[0].append(temp)
                if E:
                    axP[1].scatter(time_E[i],data_E[i],s=1)
                    prn = '%02d' % (i + 1)
                    E_L.append('E'+prn)
                    temp = dp.rms(data_E[i])
                    RMS_E[0].append(temp)
                    temp = np.std(data_E[i])
                    STD_E[0].append(temp)
                    temp = np.mean(data_E[i])
                    MEAN_E[0].append(temp)
                if C:
                    axP[2].scatter(time_C[i],data_C[i],s=1)
                    prn = '%02d' % (i + 1)
                    C_L.append('C'+prn)
                    temp = dp.rms(data_C[i])
                    RMS_C[0].append(temp)
                    temp = np.std(data_C[i])
                    STD_C[0].append(temp)
                    temp = np.mean(data_C[i])
                    MEAN_C[0].append(temp)
        
        font_text = {'family' : 'Times New Roman',
		'weight' : 500,
		'size'   : 18,
                }
        font2 = {'family' : 'Times New Roman',
		'weight' : 400,
		'size'   : 12,
                }
        ax_range = axP[0].axis()
        axP[0].legend(G_L,prop=font2,
            framealpha=1,facecolor='w',ncol=1,numpoints=5, markerscale=5, 
            bbox_to_anchor=(1.01,1),loc=2,borderaxespad=0)
        axP[0].text(ax_range[0],ax_range[3],r'MEAN={:.4f}cm, RMS={:.4f}cm, STD={:.4f}cm'.format(np.mean(MEAN_G[0])*100, np.mean(RMS_G[0])*100, np.mean(STD_G[0])*100),font_text)
        axP[1].legend(E_L,prop=font2,
            framealpha=1,facecolor='w',ncol=1,numpoints=5, markerscale=5, 
            bbox_to_anchor=(1.01,1),loc=2,borderaxespad=0)
        axP[1].text(ax_range[0],ax_range[3],r'MEAN={:.4f}cm, RMS={:.4f}cm, STD={:.4f}cm'.format(np.mean(MEAN_E[0])*100, np.mean(RMS_E[0])*100, np.mean(STD_E[0])*100),font_text)
        axP[2].legend(C_L,prop=font2,
            framealpha=1,facecolor='w',ncol=1,numpoints=5, markerscale=5, 
            bbox_to_anchor=(1.01,1),loc=2,borderaxespad=0)
        axP[2].text(ax_range[0],ax_range[3],r'MEAN={:.4f}cm, RMS={:.4f}cm, STD={:.4f}cm'.format(np.mean(MEAN_C[0])*100, np.mean(RMS_C[0])*100, np.mean(STD_C[0])*100),font_text)
        axP[2].set_xticks(XTick)
        axP[1].set_xticks(XTick)
        axP[0].set_xticks(XTick)
        axP[2].set_xticklabels(XLabel)
    
    if type == "TRP":
        axP.scatter(time_TRP,data_TRP,s=1)
        temp = dp.rms(data_TRP)
        RMS_G[0].append(temp)
        temp = np.std(data_TRP)
        STD_G[0].append(temp)
        temp = np.mean(data_TRP)
        MEAN_G[0].append(temp)
        font_text = {'family' : 'Times New Roman',
		'weight' : 500,
		'size'   : 18,
                }    
        font2 = {"size":7}
        ax_range = axP.axis()
        axP.text(ax_range[0],ax_range[3],r'MEAN={:.4f}cm, RMS={:.4f}cm, STD={:.4f}cm'.format(np.mean(MEAN_G[0])*100, np.mean(RMS_G[0])*100, np.mean(STD_G[0])*100),font_text)
        axP.set_xticks(XTick)
        axP.set_xticklabels(XLabel)
    if type == "NSAT":
        ax_range = axP[0].axis()
        font2 = {"size":20}
        axP[0].text(ax_range[0],ax_range[3],r'ALL: {:.1f}, G: {:.1f}, E: {:.1f}, C: {:.1f}'.format(mean_Sat_C+mean_Sat_E+mean_Sat_G,mean_Sat_G,mean_Sat_E,mean_Sat_C),font2)
    if type == "L" or type=="P":
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
                if G:
                    axP[0][0].scatter(time_G[i],data_G[i],s=1)
                    axP[0][1].scatter(time_G[i],data_G1[i],s=1)
                    prn = '%02d' % (i + 1)
                    G_L.append('G'+prn)
                    temp = dp.rms(data_G[i])
                    RMS_G[0].append(temp)
                    temp = dp.rms(data_G1[i])
                    RMS_G1[0].append(temp)
                    temp = np.std(data_G[i])
                    STD_G[0].append(temp)
                    temp = np.mean(data_G[i])
                    MEAN_G[0].append(temp)
                if E:
                    axP[1][0].scatter(time_E[i],data_E[i],s=1)
                    axP[1][1].scatter(time_E[i],data_E1[i],s=1)
                    prn = '%02d' % (i + 1)
                    E_L.append('E'+prn)
                    temp = dp.rms(data_E[i])
                    RMS_E[0].append(temp)
                    temp = dp.rms(data_E1[i])
                    RMS_E1[0].append(temp)
                    temp = np.std(data_E[i])
                    STD_E[0].append(temp)
                    temp = np.mean(data_E[i])
                    MEAN_E[0].append(temp)
                if C:
                    axP[2][0].scatter(time_C[i],data_C[i],s=1)
                    axP[2][1].scatter(time_C[i],data_C1[i],s=1)
                    prn = '%02d' % (i + 1)
                    C_L.append('C'+prn)
                    temp = dp.rms(data_C[i])
                    RMS_C[0].append(temp)
                    temp = dp.rms(data_C1[i])
                    RMS_C1[0].append(temp)
                    temp = np.std(data_C[i])
                    STD_C[0].append(temp)
                    temp = np.mean(data_C[i])
                    MEAN_C[0].append(temp)
        font_text = {'family' : 'Arial',
		'weight' : 500,
		'size'   : 15,
                }
        font2 = {"size":7}
        axP[0][1].legend(G_L,prop=font2,
            framealpha=1,facecolor='w',ncol=2,numpoints=5, markerscale=2, 
            bbox_to_anchor=(1.01,1),loc=2,borderaxespad=0)
        ax_range = axP[0][0].axis()
        axP[0][0].text(ax_range[0],ax_range[3],r'RMS={:.4f}cm'.format(np.mean(RMS_G[0])*100),font_text)
        ax_range = axP[0][1].axis()
        axP[0][1].text(ax_range[0],ax_range[3],r'RMS={:.4f}cm'.format(np.mean(RMS_G1[0])*100),font_text)
        axP[1][1].legend(E_L,prop=font2,
            framealpha=1,facecolor='w',ncol=2,numpoints=5, markerscale=2, 
            bbox_to_anchor=(1.01,1),loc=2,borderaxespad=0)
        ax_range = axP[1][0].axis()
        axP[1][0].text(ax_range[0],ax_range[3],r'RMS={:.4f}cm'.format(np.mean(RMS_E[0])*100),font_text)
        ax_range = axP[1][1].axis()
        axP[1][1].text(ax_range[0],ax_range[3],r'RMS={:.4f}cm'.format(np.mean(RMS_E1[0])*100),font_text)
        axP[2][1].legend(C_L,prop=font2,
            framealpha=1,facecolor='w',ncol=2,numpoints=5, markerscale=2, 
            bbox_to_anchor=(1.01,1),loc=2,borderaxespad=0)
        ax_range = axP[2][0].axis()
        axP[2][0].text(ax_range[0],ax_range[3],r'RMS={:.4f}cm'.format(np.mean(RMS_C[0])*100),font_text)
        ax_range = axP[2][1].axis()
        axP[2][1].text(ax_range[0],ax_range[3],r'RMS={:.4f}cm'.format(np.mean(RMS_C1[0])*100),font_text)
        axP[0][1].set_xticks(XTick)
        axP[0][0].set_xticks(XTick)
        axP[1][1].set_xticks(XTick)
        axP[1][0].set_xticks(XTick)
        axP[2][1].set_xticks(XTick)
        axP[2][0].set_xticks(XTick)
        axP[2][0].set_xticklabels(XLabel)
        axP[2][1].set_xticklabels(XLabel)
    
    # figP.suptitle(mode)
    # savedir = save + ".jpg"
    plt.savefig(r"D:\A-paper\Fig_and_Res\K070-Grid.png")
    if type == "ION":
        labels = axP[0].get_xticklabels() + axP[0].get_yticklabels() + axP[1].get_xticklabels() + axP[1].get_yticklabels() + axP[2].get_xticklabels() + axP[2].get_yticklabels()
        [label.set_fontsize(15) for label in labels]
    if type == "TRP":
        labels = axP.get_xticklabels() + axP.get_yticklabels()
        [label.set_fontsize(15) for label in labels]
    if show:
        plt.show()  

def plot_augc_NUM(data={},sitename=[],deltaT=2,LastT=24,starttime=0,year=2022,mon=1,day=1,time="UTC",all=False):
    f1=4
    col = 1
    figP,axP = plt.subplots(1,1,figsize=(12,10),sharey=True,sharex=True)
    axP.set_xlabel('Time' + '(' + time + ')')
    axP.set_ylabel('Number of Sat',font)

    #Time set
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

    Sitenum = len(sitename)
    dataplot={}
    timeplot={}
   
    for time in data.keys():
        plot_time = (time - cov_Time) / 3600
        if (plot_time > begT and plot_time < begT + LastT or all):
            for oneSite in data[time].keys():
                if oneSite not in sitename:
                    continue
                if oneSite not in dataplot.keys():
                    dataplot[oneSite]=[]
                    timeplot[oneSite]=[]
                dataplot[oneSite].append(data[time][oneSite])
                timeplot[oneSite].append(plot_time)
    legd=[]
    Mean_Sat={}
    # ss=600
    for oneSite in dataplot.keys():
        axP.scatter(timeplot[oneSite],dataplot[oneSite])
        Mean_Sat[oneSite]=np.mean(dataplot[oneSite])
        # ss=ss-100
        legd.append(oneSite)
    print(Mean_Sat)
    axP.legend(legd)
    if not all:
        axP.set_xticks(XTick)
        axP.set_xticklabels(XLabel)
    plt.show()
    
    

    


def plot_tec_GREC(all_data = {},savedir='save_fig_path',station = 'hjj',show = False):
    RMS_G,MEAN_G,STD_G = [[],[]],[[],[]],[[],[]]
    RMS_E,MEAN_E,STD_E = [[],[]],[[],[]],[[],[]]
    RMS_C,MEAN_C,STD_C = [[],[]],[[],[]],[[],[]]
    RMS_R,MEAN_R,STD_R = [[],[]],[[],[]],[[],[]]
    G_L,E_L,C_L,R_L = [],[],[],[]
    figP,axP = plt.subplots(2,2,figsize=(20,10),sharey=False,sharex=True)
    #figX,axX = plt.subplots(2,2,figsize=(20,10),sharey=False,sharex=True)
    axP[1][0].set_xlabel('Time:UT(h)')
    axP[1][1].set_xlabel('Time:UT(h)')
    axP[0][0].set_ylabel(station+'(TECU)')
    axP[0][1].set_ylabel(station+'(TECU)')
    axP[1][0].set_ylabel(station+'(TECU)')
    axP[1][1].set_ylabel(station+'(TECU)')
    axP[0][0].set_title('G')
    axP[0][1].set_title('R')
    axP[1][0].set_title('E')
    axP[1][1].set_title('C')
    time_G = [[] for i in range(60)]
    time_R = [[] for i in range(60)]
    time_E = [[] for i in range(60)]
    time_C = [[] for i in range(60)]

    data_G = [[] for i in range(60)]
    data_R = [[] for i in range(60)]
    data_E = [[] for i in range(60)]
    data_C = [[] for i in range(60)]

    for time in all_data:
        for sat in all_data[time]:
            prn = int(sat[1:3])
            if (sat[0]=='G'):
                time_G[prn-1].append(time)
                data_G[prn-1].append(all_data[time][sat]['TEC'])
            if (sat[0]=='R'):
                time_R[prn-1].append(time)
                data_R[prn-1].append(all_data[time][sat]['TEC'])
            if (sat[0]=='E'):
                time_E[prn-1].append(time)
                data_E[prn-1].append(all_data[time][sat]['TEC'])
            if (sat[0]=='C'):
                time_C[prn-1].append(time)
                data_C[prn-1].append(all_data[time][sat]['TEC'])
    
    for i in range(33):
        G,R,E,C = True,True,True,True
        num = len(time_G[i])
        if num < 1:
            G = False
        num = len(time_E[i])
        if num < 1:
            E = False
        num = len(time_C[i])
        if num < 1:
            C = False
        num = len(time_R[i])
        if num < 1:
            R = False
        R = False
        if G:
            axP[0][0].scatter(time_G[i],data_G[i],s=1)
            prn = '%02d' % (i + 1)
            G_L.append('G'+prn)
            temp = dp.rms(data_G[i])
            RMS_G[0].append(temp)
            temp = np.std(data_G[i])
            STD_G[0].append(temp)
            temp = np.mean(data_G[i])
            MEAN_G[0].append(temp)
        if R:
            axP[0][1].scatter(time_R[i],data_R[i],s=1)
            prn = '%02d' % (i + 1)
            R_L.append('R'+prn)
            temp = dp.rms(data_R[i])
            RMS_R[0].append(temp)
            temp = np.std(data_R[i])
            STD_R[0].append(temp)
            temp = np.mean(data_R[i])
            MEAN_R[0].append(temp)
        if E:
            axP[1][0].scatter(time_E[i],data_E[i],s=1)
            prn = '%02d' % (i + 1)
            E_L.append('E'+prn)
            temp = dp.rms(data_E[i])
            RMS_E[0].append(temp)
            temp = np.std(data_E[i])
            STD_E[0].append(temp)
            temp = np.mean(data_E[i])
            MEAN_E[0].append(temp)
        if C:
            axP[1][1].scatter(time_C[i],data_C[i],s=1)
            prn = '%02d' % (i + 1)
            C_L.append('C'+prn)
            temp = dp.rms(data_C[i])
            RMS_C[0].append(temp)
            temp = np.std(data_C[i])
            STD_C[0].append(temp)
            temp = np.mean(data_C[i])
            MEAN_C[0].append(temp)


    font2 = {"size":7}
    ax_range = axP[0][0].get_position()
    axP[0][0].set_position([ax_range.x0, ax_range.y0, ax_range.width*0.8, ax_range.height])
    ax_range = axP[0][1].get_position()
    axP[0][1].set_position([ax_range.x0, ax_range.y0, ax_range.width*0.8, ax_range.height])
    ax_range = axP[1][0].get_position()
    axP[1][0].set_position([ax_range.x0, ax_range.y0, ax_range.width*0.8, ax_range.height])
    ax_range = axP[1][1].get_position()
    axP[1][1].set_position([ax_range.x0, ax_range.y0, ax_range.width*0.8, ax_range.height])
    axP[0][0].legend(G_L,prop=font2,
        framealpha=1,facecolor='w',ncol=3,numpoints=5, markerscale=2, 
        bbox_to_anchor=(1.01,1),loc=2,borderaxespad=0)
    axP[0][1].legend(R_L,prop=font2,
        framealpha=1,facecolor='w',ncol=3,numpoints=5, markerscale=2, 
        bbox_to_anchor=(1.01,1),loc=2,borderaxespad=0)
    axP[1][0].legend(E_L,prop=font2,
        framealpha=1,facecolor='w',ncol=3,numpoints=5, markerscale=2, 
        bbox_to_anchor=(1.01,1),loc=2,borderaxespad=0)
    axP[1][1].legend(C_L,prop=font2,
        framealpha=1,facecolor='w',ncol=3,numpoints=5, markerscale=2, 
        bbox_to_anchor=(1.01,1),loc=2,borderaxespad=0)
    #axP[0][0].text(ax_range[0],ax_range[3],r'MEAN={:.4f}cm, RMS={:.4f}cm, STD={:.4f}cm'.format(np.mean(MEAN_G[0])*100, np.mean(RMS_G[0])*100, np.mean(STD_G[0])*100))
    axP[0][0].grid()
    axP[0][1].grid()
    axP[1][0].grid()
    axP[1][1].grid()

    # axP[0][0].set_ylim(-11,-5)
    # axP[0][1].set_ylim(-33,-16)
    # axP[1][0].set_ylim(-22,-10)
    # axP[1][1].set_ylim(-24,-8)
    #plt.savefig(savedir)
    if show:
        plt.show()

def plot_tec_GREC_delta(all_data = {},savedir='save_fig_path',station = 'hjj',show = False):
    RMS_G,MEAN_G,STD_G = [[],[]],[[],[]],[[],[]]
    RMS_E,MEAN_E,STD_E = [[],[]],[[],[]],[[],[]]
    RMS_C,MEAN_C,STD_C = [[],[]],[[],[]],[[],[]]
    RMS_R,MEAN_R,STD_R = [[],[]],[[],[]],[[],[]]
    G_L,E_L,C_L,R_L = [],[],[],[]
    figP,axP = plt.subplots(2,2,figsize=(20,10),sharey=False,sharex=True)
    figX,axX = plt.subplots(2,2,figsize=(20,10),sharey=False,sharex=True)
    axP[1][0].set_xlabel('Time:UT(h)')
    axP[1][1].set_xlabel('Time:UT(h)')
    axP[0][0].set_ylabel(station+'(TECU)')
    axP[0][1].set_ylabel(station+'(TECU)')
    axP[1][0].set_ylabel(station+'(TECU)')
    axP[1][1].set_ylabel(station+'(TECU)')
    axP[0][0].set_title('G')
    axP[0][1].set_title('R')
    axP[1][0].set_title('E')
    axP[1][1].set_title('C')
    time_G = [[] for i in range(60)]
    time_R = [[] for i in range(60)]
    time_E = [[] for i in range(60)]
    time_C = [[] for i in range(60)]

    data_G = [[] for i in range(60)]
    data_R = [[] for i in range(60)]
    data_E = [[] for i in range(60)]
    data_C = [[] for i in range(60)]

    for time in all_data:
        G_data,R_data,E_data,C_data = 0.0,0.0,0.0,0.0
        for sat in all_data[time]:
            prn = int(sat[1:3])
            if (sat[0]=='G'):
                if G_data == 0.0:
                    G_data = all_data[time][sat]['TEC']
                else:
                    time_G[prn-1].append(time)
                    data_G[prn-1].append(all_data[time][sat]['TEC'] - G_data)
            if (sat[0]=='R'):
                if R_data == 0.0:
                    R_data = all_data[time][sat]['TEC']
                else:
                    time_R[prn-1].append(time)
                    data_R[prn-1].append(all_data[time][sat]['TEC'] - R_data)
            if (sat[0]=='E'):
                if E_data == 0.0:
                    E_data = all_data[time][sat]['TEC']
                else:
                    time_E[prn-1].append(time)
                    data_E[prn-1].append(all_data[time][sat]['TEC'] - E_data)
            if (sat[0]=='C'):
                if C_data == 0.0:
                    C_data = all_data[time][sat]['TEC']
                else:
                    time_C[prn-1].append(time)
                    data_C[prn-1].append(all_data[time][sat]['TEC'] - C_data)
    
    for i in range(33):
        G,R,E,C = True,True,True,True
        num = len(time_G[i])
        if num < 1:
            G = False
        num = len(time_E[i])
        if num < 1:
            E = False
        num = len(time_C[i])
        if num < 1:
            C = False
        num = len(time_R[i])
        if num < 1:
            R = False

        if G:
            axP[0][0].scatter(time_G[i],data_G[i],s=1)
            prn = '%02d' % (i + 1)
            G_L.append('G'+prn)
            temp = dp.rms(data_G[i])
            RMS_G[0].append(temp)
            temp = np.std(data_G[i])
            STD_G[0].append(temp)
            temp = np.mean(data_G[i])
            MEAN_G[0].append(temp)
        if R:
            axP[0][1].scatter(time_R[i],data_R[i],s=1)
            prn = '%02d' % (i + 1)
            R_L.append('R'+prn)
            temp = dp.rms(data_R[i])
            RMS_R[0].append(temp)
            temp = np.std(data_R[i])
            STD_R[0].append(temp)
            temp = np.mean(data_R[i])
            MEAN_R[0].append(temp)
        if E:
            axP[1][0].scatter(time_E[i],data_E[i],s=1)
            prn = '%02d' % (i + 1)
            E_L.append('E'+prn)
            temp = dp.rms(data_E[i])
            RMS_E[0].append(temp)
            temp = np.std(data_E[i])
            STD_E[0].append(temp)
            temp = np.mean(data_E[i])
            MEAN_E[0].append(temp)
        if C:
            axP[1][1].scatter(time_C[i],data_C[i],s=1)
            prn = '%02d' % (i + 1)
            C_L.append('C'+prn)
            temp = dp.rms(data_C[i])
            RMS_C[0].append(temp)
            temp = np.std(data_C[i])
            STD_C[0].append(temp)
            temp = np.mean(data_C[i])
            MEAN_C[0].append(temp)


    font2 = {"size":7}
    ax_range = axP[0][0].get_position()
    axP[0][0].set_position([ax_range.x0, ax_range.y0, ax_range.width*0.8, ax_range.height])
    ax_range = axP[0][1].get_position()
    axP[0][1].set_position([ax_range.x0, ax_range.y0, ax_range.width*0.8, ax_range.height])
    ax_range = axP[1][0].get_position()
    axP[1][0].set_position([ax_range.x0, ax_range.y0, ax_range.width*0.8, ax_range.height])
    ax_range = axP[1][1].get_position()
    axP[1][1].set_position([ax_range.x0, ax_range.y0, ax_range.width*0.8, ax_range.height])
    axP[0][0].legend(G_L,prop=font2,
        framealpha=1,facecolor='w',ncol=3,numpoints=5, markerscale=2, 
        bbox_to_anchor=(1.01,1),loc=2,borderaxespad=0)
    axP[0][1].legend(R_L,prop=font2,
        framealpha=1,facecolor='w',ncol=3,numpoints=5, markerscale=2, 
        bbox_to_anchor=(1.01,1),loc=2,borderaxespad=0)
    axP[1][0].legend(E_L,prop=font2,
        framealpha=1,facecolor='w',ncol=3,numpoints=5, markerscale=2, 
        bbox_to_anchor=(1.01,1),loc=2,borderaxespad=0)
    axP[1][1].legend(C_L,prop=font2,
        framealpha=1,facecolor='w',ncol=3,numpoints=5, markerscale=2, 
        bbox_to_anchor=(1.01,1),loc=2,borderaxespad=0)
    #axP[0][0].text(ax_range[0],ax_range[3],r'MEAN={:.4f}cm, RMS={:.4f}cm, STD={:.4f}cm'.format(np.mean(MEAN_G[0])*100, np.mean(RMS_G[0])*100, np.mean(STD_G[0])*100))
    axP[0][0].grid()
    axP[0][1].grid()
    axP[1][0].grid()
    axP[1][1].grid()
    #axP[0][0].set_ylim(-0.5,0.6)
    #axP[0][1].set_ylim(-4,4)
    #axP[1][0].set_ylim(-0.4,0.4)
    #axP[1][1].set_ylim(-2,2)
    plt.savefig(savedir)
    if show:
        plt.show()

def plot_tec_MIX(all_data = {},savedir='save_fig_path',station = 'hjj',Gsys = 'GREC',show = False):
    RMS_G,MEAN_G,STD_G = [[],[]],[[],[]],[[],[]]
    RMS_E,MEAN_E,STD_E = [[],[]],[[],[]],[[],[]]
    RMS_C,MEAN_C,STD_C = [[],[]],[[],[]],[[],[]]
    RMS_R,MEAN_R,STD_R = [[],[]],[[],[]],[[],[]]
    G_L,E_L,C_L,R_L = [],[],[],[]
    figP,axP = plt.subplots(figsize=(20,10),sharey=False,sharex=True)
    figX,axX = plt.subplots(2,2,figsize=(20,10),sharey=False,sharex=True)
    axP.set_xlabel('Time:UT(h)',fontsize = 20)
    axP.set_ylabel(station+'(TECU)',fontsize = 20)
    axP.tick_params(labelsize=15)
    time_G = [[] for i in range(60)]
    time_R = [[] for i in range(60)]
    time_E = [[] for i in range(60)]
    time_C = [[] for i in range(60)]

    data_G = [[] for i in range(60)]
    data_R = [[] for i in range(60)]
    data_E = [[] for i in range(60)]
    data_C = [[] for i in range(60)]

    for time in all_data:
        for sat in all_data[time]:
            prn = int(sat[1:3])
            if (sat[0]=='G' and all_data[time][sat]['TEC'] != 0):
                time_G[prn-1].append(time)
                data_G[prn-1].append(all_data[time][sat]['TEC'])
            if (sat[0]=='R' and all_data[time][sat]['TEC'] != 0):
                time_R[prn-1].append(time)
                data_R[prn-1].append(all_data[time][sat]['TEC'])
            if (sat[0]=='E' and all_data[time][sat]['TEC'] != 0):
                time_E[prn-1].append(time)
                data_E[prn-1].append(all_data[time][sat]['TEC'])
            if (sat[0]=='C' and all_data[time][sat]['TEC'] != 0):
                time_C[prn-1].append(time)
                data_C[prn-1].append(all_data[time][sat]['TEC'])
    
    for i in range(33):
        G,R,E,C = True,True,True,True
        num = len(time_G[i])
        if (num < 1 or 'G' not in Gsys):
            G = False
        num = len(time_E[i])
        if (num < 1 or 'E' not in Gsys):
            E = False
        num = len(time_C[i])
        if (num < 1 or 'C' not in Gsys):
            C = False
        num = len(time_R[i])
        if (num < 1 or 'R' not in Gsys):
            R = False
        # if i != 23:
        #     G = False
        if G:
            axP.scatter(time_G[i],data_G[i],s=1)
            prn = '%02d' % (i + 1)
            G_L.append('G'+prn)
            temp = dp.rms(data_G[i])
            RMS_G[0].append(temp)
            temp = np.std(data_G[i])
            STD_G[0].append(temp)
            temp = np.mean(data_G[i])
            MEAN_G[0].append(temp)
        if R:
            axP.scatter(time_R[i],data_R[i],s=1)
            prn = '%02d' % (i + 1)
            G_L.append('R'+prn)
            temp = dp.rms(data_R[i])
            RMS_R[0].append(temp)
            temp = np.std(data_R[i])
            STD_R[0].append(temp)
            temp = np.mean(data_R[i])
            MEAN_R[0].append(temp)
        if E:
            axP.scatter(time_E[i],data_E[i],s=1)
            prn = '%02d' % (i + 1)
            G_L.append('E'+prn)
            temp = dp.rms(data_E[i])
            RMS_E[0].append(temp)
            temp = np.std(data_E[i])
            STD_E[0].append(temp)
            temp = np.mean(data_E[i])
            MEAN_E[0].append(temp)
        if C:
            axP.scatter(time_C[i],data_C[i],s=1)
            prn = '%02d' % (i + 1)
            G_L.append('C'+prn)
            temp = dp.rms(data_C[i])
            RMS_C[0].append(temp)
            temp = np.std(data_C[i])
            STD_C[0].append(temp)
            temp = np.mean(data_C[i])
            MEAN_C[0].append(temp)


    font2 = {"size":10}
    ax_range = axP.get_position()
    axP.set_position([ax_range.x0, ax_range.y0, ax_range.width*0.9, ax_range.height])
    
    axP.legend(G_L,prop=font2,
        framealpha=1,facecolor='w',ncol=3,numpoints=5, markerscale=2, 
        bbox_to_anchor=(1.01,1),loc=2,borderaxespad=0)
    #axP.set_ylim(8,9)
    #axP[0][0].text(ax_range[0],ax_range[3],r'MEAN={:.4f}cm, RMS={:.4f}cm, STD={:.4f}cm'.format(np.mean(MEAN_G[0])*100, np.mean(RMS_G[0])*100, np.mean(STD_G[0])*100))
    axP.grid()
    plt.savefig(savedir)
    if show:
        plt.show()


def plot_tec_compare(all_data1 = {},all_data2 = {},savedir='save_fig_path',station = 'hjj',Gsys = 'GREC',show = False):
    RMS_G,MEAN_G,STD_G = [[],[]],[[],[]],[[],[]]
    RMS_E,MEAN_E,STD_E = [[],[]],[[],[]],[[],[]]
    RMS_C,MEAN_C,STD_C = [[],[]],[[],[]],[[],[]]
    RMS_R,MEAN_R,STD_R = [[],[]],[[],[]],[[],[]]
    G_L,E_L,C_L,R_L = [],[],[],[]
    figP,axP = plt.subplots(figsize=(20,10),sharey=False,sharex=True)
    axP.set_xlabel('Time:UT(h)',fontsize = 20)
    axP.set_ylabel(station+'(TECU)',fontsize = 20)
    axP.tick_params(labelsize=15)
    time_G = [[] for i in range(60)]
    time_R = [[] for i in range(60)]
    time_E = [[] for i in range(60)]
    time_C = [[] for i in range(60)]

    data_G = [[] for i in range(60)]
    data_R = [[] for i in range(60)]
    data_E = [[] for i in range(60)]
    data_C = [[] for i in range(60)]

    for time in all_data1:
        for sat in all_data1[time]:
            prn = int(sat[1:3])
            if (sat[0]=='G'):
                time_G[prn-1].append(time)
                data_G[prn-1].append(all_data1[time][sat]['TEC'])
            if (sat[0]=='R'):
                time_R[prn-1].append(time)
                data_R[prn-1].append(all_data1[time][sat]['TEC'])
            if (sat[0]=='E'):
                time_E[prn-1].append(time)
                data_E[prn-1].append(all_data1[time][sat]['TEC'])
            if (sat[0]=='C'):
                time_C[prn-1].append(time)
                data_C[prn-1].append(all_data1[time][sat]['TEC'])
    
    for i in range(33):
        G,R,E,C = True,True,True,True
        num = len(time_G[i])
        prn = 'G' + '%02d' % (i + 1)
        if (num < 1 or prn not in Gsys):
            G = False
        num = len(time_E[i])
        prn = 'E' + '%02d' % (i + 1)
        if (num < 1 or prn not in Gsys):
            E = False
        num = len(time_C[i])
        prn = 'C' + '%02d' % (i + 1)
        if (num < 1 or prn not in Gsys):
            C = False
        num = len(time_R[i])
        prn = 'R' + '%02d' % (i + 1)
        if (num < 1 or prn not in Gsys):
            R = False

        if G:
            axP.scatter(time_G[i],data_G[i],s=1,c='#00CED1',label='PPP')
            prn = '%02d' % (i + 1)
            G_L.append('mode1')
            temp = dp.rms(data_G[i])
            RMS_G[0].append(temp)
            temp = np.std(data_G[i])
            STD_G[0].append(temp)
            temp = np.mean(data_G[i])
            MEAN_G[0].append(temp)
        if R:
            axP.scatter(time_R[i],data_R[i],s=1)
            prn = '%02d' % (i + 1)
            G_L.append('mode1')
            temp = dp.rms(data_R[i])
            RMS_R[0].append(temp)
            temp = np.std(data_R[i])
            STD_R[0].append(temp)
            temp = np.mean(data_R[i])
            MEAN_R[0].append(temp)
        if E:
            axP.scatter(time_E[i],data_E[i],s=1)
            prn = '%02d' % (i + 1)
            G_L.append('mode1')
            temp = dp.rms(data_E[i])
            RMS_E[0].append(temp)
            temp = np.std(data_E[i])
            STD_E[0].append(temp)
            temp = np.mean(data_E[i])
            MEAN_E[0].append(temp)
        if C:
            axP.scatter(time_C[i],data_C[i],s=1)
            prn = '%02d' % (i + 1)
            G_L.append('mode1')
            temp = dp.rms(data_C[i])
            RMS_C[0].append(temp)
            temp = np.std(data_C[i])
            STD_C[0].append(temp)
            temp = np.mean(data_C[i])
            MEAN_C[0].append(temp)
    time_G = [[] for i in range(60)]
    time_R = [[] for i in range(60)]
    time_E = [[] for i in range(60)]
    time_C = [[] for i in range(60)]

    data_G = [[] for i in range(60)]
    data_R = [[] for i in range(60)]
    data_E = [[] for i in range(60)]
    data_C = [[] for i in range(60)]
    for time in all_data2:
        for sat in all_data2[time]:
            prn = int(sat[1:3])
            if (sat[0]=='G'):
                time_G[prn-1].append(time)
                data_G[prn-1].append(all_data2[time][sat]['TEC'])
            if (sat[0]=='R'):
                time_R[prn-1].append(time)
                data_R[prn-1].append(all_data2[time][sat]['TEC'])
            if (sat[0]=='E'):
                time_E[prn-1].append(time)
                data_E[prn-1].append(all_data2[time][sat]['TEC'])
            if (sat[0]=='C'):
                time_C[prn-1].append(time)
                data_C[prn-1].append(all_data2[time][sat]['TEC'])
    
    for i in range(33):
        G,R,E,C = True,True,True,True
        num = len(time_G[i])
        prn = 'G' + '%02d' % (i + 1)
        if (num < 1 or prn not in Gsys):
            G = False
        num = len(time_E[i])
        prn = 'E' + '%02d' % (i + 1)
        if (num < 1 or prn not in Gsys):
            E = False
        num = len(time_C[i])
        prn = 'C' + '%02d' % (i + 1)
        if (num < 1 or prn not in Gsys):
            C = False
        num = len(time_R[i])
        prn = 'R' + '%02d' % (i + 1)
        if (num < 1 or prn not in Gsys):
            R = False
        #G,R,E,C = False,False,False,False
        if G:
            axP.scatter(time_G[i],data_G[i],s=1,c='#DC143C',label='SION')
            prn = '%02d' % (i + 1)
            G_L.append('mode2')
            temp = dp.rms(data_G[i])
            RMS_G[0].append(temp)
            temp = np.std(data_G[i])
            STD_G[0].append(temp)
            temp = np.mean(data_G[i])
            MEAN_G[0].append(temp)
        if R:
            axP.scatter(time_R[i],data_R[i],s=1)
            prn = '%02d' % (i + 1)
            G_L.append('mode2')
            temp = dp.rms(data_R[i])
            RMS_R[0].append(temp)
            temp = np.std(data_R[i])
            STD_R[0].append(temp)
            temp = np.mean(data_R[i])
            MEAN_R[0].append(temp)
        if E:
            axP.scatter(time_E[i],data_E[i],s=1)
            prn = '%02d' % (i + 1)
            G_L.append('mode2')
            temp = dp.rms(data_E[i])
            RMS_E[0].append(temp)
            temp = np.std(data_E[i])
            STD_E[0].append(temp)
            temp = np.mean(data_E[i])
            MEAN_E[0].append(temp)
        if C:
            axP.scatter(time_C[i],data_C[i],s=1)
            prn = '%02d' % (i + 1)
            G_L.append('mode2')
            temp = dp.rms(data_C[i])
            RMS_C[0].append(temp)
            temp = np.std(data_C[i])
            STD_C[0].append(temp)
            temp = np.mean(data_C[i])
            MEAN_C[0].append(temp)


    font2 = {"size":10}
    ax_range = axP.get_position()
    axP.set_position([ax_range.x0, ax_range.y0, ax_range.width, ax_range.height])
    
    axP.legend(prop=font2,
        framealpha=1,facecolor='w', markerscale=3)
    #axP.set_ylim(16,32)
    #axP[0][0].text(ax_range[0],ax_range[3],r'MEAN={:.4f}cm, RMS={:.4f}cm, STD={:.4f}cm'.format(np.mean(MEAN_G[0])*100, np.mean(RMS_G[0])*100, np.mean(STD_G[0])*100))
    axP.grid()
    plt.savefig(savedir)
    if show:
        plt.show()

def plot_upd_nl_GEC(all_data={},savedir='save_fig_path',mode = 'upd_nl',show = False):
    time_G = [[] for i in range(60)]
    time_E = [[] for i in range(60)]
    time_C = [[] for i in range(60)]

    data_G = [[] for i in range(60)]
    data_E = [[] for i in range(60)]
    data_C = [[] for i in range(60)]
    std_G,std_E,std_C = [],[],[]
    G_L,E_L,C_L = [],[],[]
    
    figP,axP = plt.subplots(3,1,figsize=(12,9),sharey=False,sharex=True)
    
    axP[2].set_xlabel('Time:Hour of GPS Week(hour)')
    axP[0].set_ylabel(mode+'(Cycles)')
    axP[1].set_ylabel(mode+'(Cycles)')
    axP[2].set_ylabel(mode+'(Cycles)')
    if "WL" in mode:
        axP[0].set_title('G-WL')
        axP[1].set_title('E-WL')
        axP[2].set_title('C-WL')
    else:
        axP[0].set_title('G-NL')
        axP[1].set_title('E-NL')
        axP[2].set_title('C-NL')
    # axP[0].set_ylim(0.0,1) 
    # axP[1].set_ylim(0.0,1) 
    # axP[2].set_ylim(0.0,1) 

    for time in all_data:
        for sat in all_data[time]:
            prn = int(sat[1:3])
            if (all_data[time][sat] != 999.9999):
                if (sat[0]=='G'):
                    time_G[prn-1].append(time / 3600)
                    data_G[prn-1].append(all_data[time][sat])
                    continue
                if (sat[0]=='E'):
                    time_E[prn-1].append(time / 3600)
                    data_E[prn-1].append(all_data[time][sat])
                    continue
                if (sat[0]=='C'):
                    time_C[prn-1].append(time / 3600)
                    data_C[prn-1].append(all_data[time][sat])
                    continue
    #colormap = sns.color_palette("colorblind",40)
    G_j,E_j,C_j = 0,0,0
    for i in range(40):
        G,R,E,C = True,True,True,True
        num = len(time_G[i])
        if num < 1:
            G = False
        else:
            G_j = G_j+1
        num = len(time_E[i])
        if num < 1:
            E = False
        else:
            E_j = E_j+1
        num = len(time_C[i])
        if num < 1:
            C = False
        else:
            C_j = C_j+1
        
        if G:
            axP[0].scatter(time_G[i],data_G[i],s=2,marker='D')
            std_G.append(np.std(data_G[i]))
            prn = '%02d' % (i + 1)
            G_L.append('G'+prn)

        if E:
            axP[1].scatter(time_E[i],data_E[i],s=2,marker='D')
            prn = '%02d' % (i + 1)
            std_E.append(np.std(data_E[i]))
            E_L.append('E'+prn)

        if C:
            axP[2].scatter(time_C[i],data_C[i],s=2,marker='D')
            prn = '%02d' % (i + 1)
            std_C.append(np.std(data_C[i]))
            C_L.append('C'+prn)

    font2 = {"size":7}
    axP[0].legend(G_L,prop=font2,
        framealpha=1,facecolor='w',ncol=3,numpoints=5, markerscale=2, 
        bbox_to_anchor=(1.01,1),loc=2,borderaxespad=0)
    axP[1].legend(E_L,prop=font2,
        framealpha=1,facecolor='w',ncol=3,numpoints=5, markerscale=2, 
        bbox_to_anchor=(1.01,1),loc=2,borderaxespad=0)
    axP[2].legend(C_L,prop=font2,
        framealpha=1,facecolor='w',ncol=3,numpoints=5, markerscale=2, 
        bbox_to_anchor=(1.01,1),loc=2,borderaxespad=0) 
    axP[0].grid()
    axP[1].grid()
    axP[2].grid()

    savedir1 = savedir + mode + ".png" 
    plt.savefig(savedir1)
    figS,axS = plt.subplots(3,1,figsize=(20,15),sharey=True,sharex=False)
    axS[0].set_ylabel('UPD STD(Cycles)')
    axS[1].set_ylabel('UPD STD(Cycles)')
    axS[2].set_ylabel('UPD STD(Cycles)')
    axS[0].set_title('G-STD-NL')
    axS[1].set_title('E-STD-NL')
    axS[2].set_title('C-STD-NL')
    axS[0].set_ylim(0,0.5)
    axS[0].bar(range(len(std_G)),std_G,tick_label=G_L)
    axS[1].bar(range(len(std_E)),std_E,tick_label=E_L)
    axS[2].bar(range(len(std_C)),std_C,tick_label=C_L)
    axS[0].grid(axis = "y")
    axS[1].grid(axis = "y")
    axS[2].grid(axis = "y")
    axS[0].set_axisbelow(True)
    axS[1].set_axisbelow(True)
    axS[2].set_axisbelow(True)
    savedir2 = savedir + mode + "std.png" 
    plt.savefig(savedir2)
    if show:
        plt.show()

def plot_upd_wl_oneday_GEC(all_data={},savedir='save_fig_path',mode = 'upd_wl',show = False):
    figS,axS = plt.subplots(3,1,figsize=(20,15),sharey=True,sharex=False)
    axS[0].set_ylabel('UPD WL(Cycles)')
    axS[1].set_ylabel('UPD WL(Cycles)')
    axS[2].set_ylabel('UPD WL(Cycles)')
    axS[0].set_title('G-WL')
    axS[1].set_title('E-WL')
    axS[2].set_title('C-WL')
    GL,EL,CL = [],[],[]
    G_j,E_j,C_j = -1,-1,-1
    for sat in all_data:
        if 'G' in sat:
            G_j = G_j + 1
            GL.append(sat)
            axS[0].bar(G_j,all_data[sat])
        if 'E' in sat:
            E_j = E_j + 1
            EL.append(sat)
            axS[1].bar(E_j,all_data[sat])
        if 'C' in sat:
            C_j = C_j + 1
            CL.append(sat)
            axS[2].bar(C_j,all_data[sat])
    
    axS[0].set_xticks(range(G_j+1))
    axS[0].set_xticklabels(GL)
    axS[1].set_xticks(range(E_j+1))
    axS[1].set_xticklabels(EL)
    axS[2].set_xticks(range(C_j+1))
    axS[2].set_xticklabels(CL)
    savedir = savedir + mode + '.png'
    plt.savefig(savedir)
    if show:
        plt.show()

def plot_e_n_u(site = "Default",data = {},type = ["E","N","U"],mode = ["DEFAULT"],ylim = 1,starttime = 0,deltaT = 2,LastT=24,time = "UTC",save='../',show = False,Fixed = False,delta_data = 30,year=2021,mon=4,day=10,all=False,Sigma=3,Sigma_num=1,recovergence = 0):
    # #=== plot_e_n_u ===# #
    N_plot = len(type)
    N_mode = len(mode)
    f1=5
    ymin = -ylim
    ymax = ylim
    ##=== Plot set ===##
    figP,axP = plt.subplots(N_plot,1,figsize=(13.7,11),sharey=False,sharex=True)
    axP[N_plot - 1].set_xlabel('Time' + '(' + time + ')',font_label)
    ## Only ENU
    if N_plot == 3:
        for i in range(N_plot):
            if type[i] == "E":
                axP[i].set_ylabel("East errors(m)",font_label)
            if type[i] == "N":
                axP[i].set_ylabel("North errors(m)",font_label)
            if type[i] == "U":
                axP[i].set_ylabel("Up errors(m)",font_label)
            if type[i] == "NSAT":
                axP[i].set_ylabel("Number of Sat",font_label)
    ## with NSAT
    elif N_plot == 4 and "NSAT" in type:
        axP[0].set_ylabel("Number of Sat",font_label)
        axP[2].set_ylabel("Position errors(m)",font_label)
    for i in range(N_plot):
        if type[i] != "NSAT":
            axP[i].set_ylim(ymin,ymax)
        else:
            box = axP[i].get_position()
            axP[i].set_position([box.x0, box.y0, box.width, box.height*1.3])
            axP2 = axP[i].twinx()
            box = axP2.get_position()
            axP2.set_position([box.x0, box.y0, box.width, box.height*1.3])
            

        
        
    ##=== Save set ===##
    doy = tr.ymd2doy(year,mon,day,0,00,00)
    SaveTextFile = save + "\\" + site + "-" "Sigma-" + "{:0>1}".format(Sigma_num) + "-{:0>2}".format(starttime) + ".txt"
    if not show:
        with open(SaveTextFile,'a') as file:
            file.write("{:0>3}    ".format(doy))
    ##=== Time Xtick set ===##
    [XLabel,XTick,cov_Time,begT,LastT]=xtick(time,year,mon,day,starttime,LastT,deltaT)
    ##=== Data convert && convergence time ===##
    time_plot,data_plot,fixed_num,float_num,all_num,RMS_enu,STD_enu,MEAN_enu = {},{},{},{},{},{},{},{}
    type_list = ["E","N","U","NSAT","PDOP","AMB"]
    type_enu = ["E","N","U"]
    for cur_mode in mode:
        if cur_mode not in time_plot:
            time_plot[cur_mode] = []
            data_plot[cur_mode] = {}
            RMS_enu[cur_mode],STD_enu[cur_mode],MEAN_enu[cur_mode] = {},{},{}
            fixed_num[cur_mode],float_num[cur_mode],all_num[cur_mode] = 0,0,(LastT*3600) / delta_data + 1
            for cur_type in type_list:
                data_plot[cur_mode][cur_type] = []
    for cur_mode in mode:
        for cur_time in data[cur_mode].keys():
            plot_time = (cur_time-cov_Time) / 3600
            if ((plot_time >= begT and plot_time <= (begT + LastT)) or all):
                if data[cur_mode][cur_time]["AMB"] == 0:
                    float_num[cur_mode] = float_num[cur_mode] + 1
                else:
                    fixed_num[cur_mode] = fixed_num[cur_mode] + 1
                if (Fixed and data[cur_mode][cur_time]["AMB"] == 0):
                    continue
                time_plot[cur_mode].append(plot_time)
                for cur_type in type_list:
                    data_plot[cur_mode][cur_type].append(data[cur_mode][cur_time][cur_type])
    ##=== Convergence time ===##
    # con_list = [20,10,5]
    con_list = [10]
    cont_continue = 10
    con_horizontal,con_vertical,con_position = {},{},{}
    for cur_mode in mode:
        if cur_mode not in con_horizontal.keys():
            con_horizontal[cur_mode],con_vertical[cur_mode],con_position[cur_mode] = {},{},{}
            for cur_accuracy in con_list:
                con_horizontal[cur_mode][cur_accuracy] = []
                con_vertical[cur_mode][cur_accuracy] = []
                con_position[cur_mode][cur_accuracy] = []
    if recovergence != 0:
        for cur_mode in time_plot.keys():
            start_recon = False
            all_epoch = len(time_plot[cur_mode])
            i = 0
            while i < all_epoch:
                time_now = time_plot[cur_mode][i] * 3600
                if time_now % recovergence == 0:
                    index_time_now = i
                    for cur_accuracy in con_list:
                        i = index_time_now
                        con_position_num,con_horizontal_num,con_vertical_num = 0,0,0
                        while i < all_epoch:
                            cur_time = time_plot[cur_mode][i] * 3600
                            horizontal = math.sqrt(math.pow(data_plot[cur_mode]["E"][i],2) + math.pow(data_plot[cur_mode]["N"][i],2))*100
                            vertical = abs(data_plot[cur_mode]["U"][i])*100
                            position = math.sqrt(math.pow(data_plot[cur_mode]["E"][i],2) + math.pow(data_plot[cur_mode]["N"][i],2) +  math.pow(data_plot[cur_mode]["U"][i],2))*100
                            #= position =#
                            if position < cur_accuracy:
                                if con_position_num < cont_continue:
                                    con_position_num = con_position_num + 1
                            elif con_position_num < cont_continue:
                                con_position_num = 0
                            if con_position_num == cont_continue:
                                con_position[cur_mode][cur_accuracy].append(time_plot[cur_mode][i-cont_continue+1]*3600 - time_now)
                                con_position_num = 99
                            #= horizontal =#
                            if horizontal < cur_accuracy:
                                if con_horizontal_num < cont_continue:
                                    con_horizontal_num = con_horizontal_num + 1
                            elif con_horizontal_num < cont_continue:
                                con_horizontal_num = 0
                            if con_horizontal_num == cont_continue:
                                con_horizontal[cur_mode][cur_accuracy].append(time_plot[cur_mode][i-cont_continue+1]*3600 - time_now)
                                con_horizontal_num = 99
                            #= vertical =#
                            if vertical < cur_accuracy:
                                if con_vertical_num < cont_continue:
                                    con_vertical_num = con_vertical_num + 1
                            elif con_vertical_num < cont_continue:
                                con_vertical_num = 0
                            if con_vertical_num == cont_continue:
                                con_vertical[cur_mode][cur_accuracy].append(time_plot[cur_mode][i-cont_continue+1]*3600 - time_now)
                                con_vertical_num = 99
                            if con_horizontal_num == 99 and con_vertical_num == 99 and con_position_num == 99:
                                break
                            if cur_time - time_now > 15*60:
                                if con_horizontal_num != 99:
                                    con_horizontal[cur_mode][cur_accuracy].append(900)
                                if con_position_num != 99:
                                    con_position[cur_mode][cur_accuracy].append(900)
                                if con_vertical_num != 99:
                                    con_vertical[cur_mode][cur_accuracy].append(900)
                                break
                            i = i+1
                            
                else:
                    i=i+1
                    continue
                    

    ##=== Sigma Edit ===##
    if Sigma > 0:
        for cur_mode in mode:
            Sigma_num_temp = Sigma_num
            after_sig = len(time_plot[cur_mode])
            for cur_type in type_enu:
                MEAN_enu[cur_mode][cur_type] = np.mean(data_plot[cur_mode][cur_type])
                STD_enu[cur_mode][cur_type] = np.std(data_plot[cur_mode][cur_type])
                RMS_enu[cur_mode][cur_type] = dp.rms(data_plot[cur_mode][cur_type])
            while Sigma_num_temp >= 1:
                before_sig = len(time_plot[cur_mode])
                index_rm = []
                for cur_type in type_enu:
                    for i in range(before_sig):
                        if abs(data_plot[cur_mode][cur_type][i] - MEAN_enu[cur_mode][cur_type]) > Sigma * STD_enu[cur_mode][cur_type] and i not in index_rm:
                            index_rm.append(i)
                for cur_type in type_list:
                    data_plot[cur_mode][cur_type] = np.delete(data_plot[cur_mode][cur_type],index_rm)
                    MEAN_enu[cur_mode][cur_type] = np.mean(data_plot[cur_mode][cur_type])
                    STD_enu[cur_mode][cur_type] = np.std(data_plot[cur_mode][cur_type])
                    RMS_enu[cur_mode][cur_type] = dp.rms(data_plot[cur_mode][cur_type])
                time_plot[cur_mode] = np.delete(time_plot[cur_mode],index_rm)
                after_sig = len(time_plot[cur_mode])
                print("{}-{}:{:0>2}-{:0>5},{:0>5}".format(cur_mode,"Sig",Sigma_num_temp,before_sig,after_sig))
                Sigma_num_temp = Sigma_num_temp - 1
            #== -MEAN ==#
            # for cur_type in type_enu:
            #     MEAN_enu[cur_mode][cur_type] = np.mean(data_plot[cur_mode][cur_type])
            #     data_plot[cur_mode][cur_type] = data_plot[cur_mode][cur_type] - MEAN_enu[cur_mode][cur_type]
            #     STD_enu[cur_mode][cur_type] = np.std(data_plot[cur_mode][cur_type])
            #     RMS_enu[cur_mode][cur_type] = dp.rms(data_plot[cur_mode][cur_type])    
            #== Distribution ==#
            num_5_en,num_10_en,num_10_u,num_15_u = 0,0,0,0
            for i in range(after_sig):
                if math.sqrt(math.pow(data_plot[cur_mode]["E"][i],2) + math.pow(data_plot[cur_mode]["N"][i],2)) < 0.05:
                    num_5_en = num_5_en + 1
                if math.sqrt(math.pow(data_plot[cur_mode]["E"][i],2) + math.pow(data_plot[cur_mode]["N"][i],2)) < 0.10:
                    num_10_en = num_10_en + 1
                if abs(data_plot[cur_mode]["U"][i]) < 0.10:
                    num_10_u = num_10_u + 1
                if abs(data_plot[cur_mode]["U"][i]) < 0.15:
                    num_15_u = num_15_u + 1
            print(cur_mode)
            print("Horizon(<5cm)    " + '{:.2f}%'.format(num_5_en/after_sig*100))
            print("Horizon(<10cm)    " + '{:.2f}%'.format(num_10_en/after_sig*100))
            print("Altitude(<10cm)   " + '{:.2f}%'.format(num_10_u/after_sig*100))
            print("Altitude(<15cm)  " + '{:.2f}%'.format(num_15_u/after_sig*100))
    ##=== Plot Data ===##
    if 1:
        for i in range(N_plot):
            for j in range(N_mode):
                axP[i].scatter(time_plot[mode[j]],data_plot[mode[j]][type[i]],color = color_list[j%9],s=13)
    else:
        for i in range(N_plot):
            for j in range(N_mode):
                if type[i] != "NSAT":
                    axP[i].scatter(time_plot[mode[j]],data_plot[mode[j]][type[i]],color = color_list[j%9],s=13)
        axP[0].plot(time_plot[mode[0]],data_plot[mode[0]]["NSAT"],color = color_list[3],ls = '-',linewidth = 3)
        axP[0].plot(time_plot[mode[1]],data_plot[mode[1]]["NSAT"],color = color_list[3],ls=':',linewidth = 3)
        axP[0].set_ylabel("Num of Sat",font_label,color = color_list[3])
        axP[0].spines['left'].set(color = color_list[3],linewidth = 2,linestyle = "-")
        axP[0].tick_params(length=6, width=2, color=color_list[3], labelcolor=color_list[3])
        axP[0].legend(["Interpolation","Grid"],prop=font_legend,
            framealpha=1,facecolor='none',ncol=4,numpoints=5,markerscale=3, 
            borderaxespad=0,bbox_to_anchor=(1,1.2),loc=1,frameon = False) 
        leg = axP[0].get_legend()
        for legobj in leg.legendHandles:
            legobj.set_linewidth(5)
            legobj.set_color("black")
        
        axP2.grid(False)
        axP2.plot(time_plot[mode[0]],data_plot[mode[0]]["PDOP"],color = color_list[4],ls = '-',linewidth = 3)
        axP2.plot(time_plot[mode[1]],data_plot[mode[1]]["PDOP"],color = color_list[4],ls = ':',linewidth = 3)
        axP2.set_ylabel("PDOP",font_label,color = color_list[4])
        axP2.spines['right'].set(color = color_list[4],linewidth = 2,linestyle = "-")
        axP2.tick_params(length=6, width=2, color=color_list[4], labelcolor=color_list[4])
        labels = axP2.get_yticklabels() + axP2.get_xticklabels()
        [label.set_fontsize(xtick_size) for label in labels]
        [label.set_fontname('Times New Roman') for label in labels]

    i=-1
    for cur_type in type:
        i = i+1
        RMS_str = "RMS:"
        MEAN_str = "MEAN:"
        for cur_mode in mode:
            if cur_type in type_enu:
                RMS_str = RMS_str +'{:.4f}m, '.format(RMS_enu[cur_mode][cur_type])
            if cur_type == "NSAT":
                MEAN_str = MEAN_str +'{:.2f}, '.format(MEAN_enu[cur_mode][cur_type])
        if cur_type in type_enu:
            ax_range = axP[i].axis()
            # axP[i].text(ax_range[0],ax_range[3]+ylim/15,RMS_str[0:9*N_mode+2],font_text)
            # if cur_type == "E":
            #     axP[i].text(ax_range[0],ax_range[3]-ylim/2,"East",font_title)
            # if cur_type == "N":
            #     axP[i].text(ax_range[0],ax_range[3]-ylim/2,"North",font_title)
            # if cur_type == "U":
            #     axP[i].text(ax_range[0],ax_range[3]-ylim/2,"Up",font_title)
        if cur_type == "NSAT":
            ax_range = axP[i].axis()
            # axP[i].text(ax_range[0],ax_range[3]+ylim/15,MEAN_str[0:7*N_mode+3],font_text)
    labels = axP[0].get_yticklabels() + axP[0].get_xticklabels()
    for i in range(N_plot):
        labels = labels + axP[i].get_yticklabels() + axP[i].get_xticklabels()
    [label.set_fontsize(xtick_size) for label in labels]
    [label.set_fontname('Times New Roman') for label in labels]
    if not all:
        axP[N_plot-1].set_xticks(XTick)
        axP[N_plot-1].set_xticklabels(XLabel)
    E_str=""
    for i in range(N_plot):
        cur_type=type[i]
        # if not all:
        #     axP[i].set_xticks(XTick)
        ax_range = axP[i].axis()
        if (N_plot==3 and i == 0):
            axP[i].legend(mode,prop=font_legend,
            framealpha=1,facecolor='none',ncol=4,numpoints=5,markerscale=4, 
            borderaxespad=0,bbox_to_anchor=(1,1.3),loc=1) 
        if (N_plot==4 and i == 1):
            axP[i].legend(mode,prop=font_legend,
            framealpha=0,facecolor='none',ncol=4,numpoints=5, markerscale=4,
            borderaxespad=0,bbox_to_anchor=(1,1.22),loc=1) 
        #axP[i].autoscale(tight=True)
        if cur_type == "E" or cur_type == "N" or cur_type == "U":
            print("\n"+cur_type)
            for cur_mode in mode:
                # E_str = E_str + "             ###{}-{}###       \n".format(cur_type,mode[j])
                # E_str = E_str + 'RMS={:.4f}cm,MEAN={:.4f}cm,STD={:.4f}cm\n'.format(RMS_enu[cur_type][j]*100,MEAN_enu[cur_type][j]*100,STD_enu[cur_type][j]*100)
                E_str = E_str + '{:.4f}           '.format(RMS_enu[cur_mode][cur_type]*100)
                print(cur_mode + ":")
                print('RMS={:.4f}cm,MEAN={:.4f}cm,STD={:.4f}cm'.format(RMS_enu[cur_mode][cur_type]*100,MEAN_enu[cur_mode][cur_type]*100,STD_enu[cur_mode][cur_type]*100))
    
    print("固定率(Fixed/Fixed+Float):")
    for cur_mode in mode:
        if (fixed_num[cur_mode] == 0):
            print(cur_mode + ':{:.2f}%'.format(0))
        else:
            print(cur_mode + ':{:.2f}%'.format(fixed_num[cur_mode] / (fixed_num[cur_mode] + float_num[cur_mode]) * 100))        
    print("固定率(Fixed_Sigma/Fixed+Float):")
    for cur_mode in mode:
        if (fixed_num[cur_mode] == 0):
            print(cur_mode + ':{:.2f}%'.format(0))
        else:
            print(cur_mode + ':{:.2f}%'.format(len(time_plot[cur_mode]) / (fixed_num[cur_mode] + float_num[cur_mode]) * 100))
    print("完整率:")
    for cur_mode in mode:
        print(cur_mode + ':{:.2f}%'.format((fixed_num[cur_mode] + float_num[cur_mode]) / all_num[cur_mode] * 100))
    print("固定率(Fixed/ALL):")
    for cur_mode in mode:
        print(cur_mode + ':{:.2f}%'.format(fixed_num[cur_mode] / (all_num[cur_mode]) * 100))
    print("3D收敛时间(s):")
    for cur_accuracy in con_list:
        print('{:.0f}cm'.format(cur_accuracy))
        for cur_mode in con_position.keys():
            print('{}:{:.2f}s'.format(cur_mode,np.mean(con_position[cur_mode][cur_accuracy])))
    print("垂直收敛时间(s):")
    for cur_accuracy in con_list:
        print('{:.0f}cm'.format(cur_accuracy))
        for cur_mode in con_position.keys():
            print('{}:{:.2f}s'.format(cur_mode,np.mean(con_vertical[cur_mode][cur_accuracy])))
    print("水平收敛时间(s):")
    for cur_accuracy in con_list:
        print('{:.0f}cm'.format(cur_accuracy))
        for cur_mode in con_position.keys():
            print('{}:{:.2f}s'.format(cur_mode,np.mean(con_horizontal[cur_mode][cur_accuracy])))

    if show:
        plt.savefig(r"D:\A-paper\Fig_and_Res\HKPC-305-IONO.png",dpi=600)
        plt.savefig(r"D:\A-paper\Fig_and_Res\HKPC-305-IONO.svg")
        plt.show()
    else:
        SaveFigFile = save + "\\" + site + "-" + "{:0>3}".format(doy) + "-" "Sigma-" + "{:0>1}".format(Sigma_num) + ".png"
        plt.savefig(SaveFigFile)
        with open(SaveTextFile,'a') as file:
            # file.write("       ###"+"Fixed/Fixed+Float"+"###       \n")
            for i in range(N_mode):
                if ((fixed_num[mode[i]]) == 0):
                    file.write('{:>.2f}%           '.format(mode[i],0))
                else:
                    file.write('{:>.2f}%           '.format(fixed_num[mode[i]] / (all_num[mode[i]]) * 100))
            for i in range(N_mode):
                if ((fixed_num[mode[i]]) == 0):
                    file.write('{:>.2f}%           '.format(mode[i],0))
                else:
                    file.write('{:>.2f}%           '.format(len(time_plot[mode[i]]) / (fixed_num[mode[i]] + float_num[mode[i]]) * 100))
            file.write(E_str+'\n')
            # file.write("=========================="+"{:0>3}".format(doy)+"==========================\n")
            # file.write("==========="+"{:0>3}".format(doy)+"===========\n")
            # file1.write('%04f' % abs(data_Diff[time][sat][sys_type[sat[0]]]) + "   " + '%04f' % data_Ele[time][sat]["ELE"] + "   " + '%04f' % data_ROTI[time][sat] + "\n")


def plot_enu(site = "Default",data = {},type = ["E","N","U"],mode = ["DEFAULT"],ylim = 1,starttime = 0,deltaT = 2,LastT=24,time = "UTC",save='',show = False,Fixed = False,delta_data = 30,year=2021,mon=4,day=10,all=False,Sigma=3,Sigma_num=1):
    N_mode = len(mode)
    if "NSAT" in type:
        figP,axP = plt.subplots(N_mode+1,1,figsize=(15,11),sharey=False,sharex=True)
    else:
        figP,axP = plt.subplots(N_mode,1,figsize=(15,11),sharey=False,sharex=False)
    [XLabel,XTick,cov_Time,begT,LastT]=xtick(time,year,mon,day,starttime,LastT,deltaT)
    data_plot = {}
    time_plot = {}
    #data convert
    for cur_mode in mode:
        if cur_mode not in data_plot.keys():
            data_plot[cur_mode] = {}
            time_plot[cur_mode] = []
            data_plot[cur_mode]["E"] = []
            data_plot[cur_mode]["N"] = []
            data_plot[cur_mode]["U"] = []
            data_plot[cur_mode]["NSAT"] = []
            data_plot[cur_mode]["PDOP"] = []
    indexx = 0
    for cur_mode in mode:
        for cur_time in data[cur_mode].keys():
            plot_time = (cur_time-cov_Time) / 3600
            if ((plot_time >= begT and plot_time <= (begT + LastT)) or all):
                if (Fixed and data[cur_mode][cur_time]["AMB"] == 0):
                    continue
                if (data[cur_mode][cur_time]["PDOP"] > 5):
                    continue
                data_plot[cur_mode]["E"].append(data[cur_mode][cur_time]["E"])
                data_plot[cur_mode]["N"].append(data[cur_mode][cur_time]["N"])
                data_plot[cur_mode]["U"].append(data[cur_mode][cur_time]["U"])
                data_plot[cur_mode]["NSAT"].append(data[cur_mode][cur_time]["NSAT"])
                data_plot[cur_mode]["PDOP"].append(data[cur_mode][cur_time]["PDOP"])
                time_plot[cur_mode].append(plot_time)
                indexx = indexx + 1
                # if (plot_time - 10+37.5) < 5/3600:
                #     print(indexx)
                # if (plot_time - 10+47.5) < 5/3600:
                #     print(indexx)
    #Sigma
    RMS_enu,STD_enu,MEAN_enu={},{},{}
    if Sigma > 0:
        cur_type = "E"
        RMS_enu[cur_type] = []
        STD_enu[cur_type] = []
        MEAN_enu[cur_type] = []
        cur_type = "N"
        RMS_enu[cur_type] = []
        STD_enu[cur_type] = []
        MEAN_enu[cur_type] = []
        cur_type = "U"
        RMS_enu[cur_type] = []
        STD_enu[cur_type] = []
        MEAN_enu[cur_type] = []
        for cur_mode in mode:
            Sigma_num_temp = Sigma_num
            mean_E = np.mean(data_plot[cur_mode]["E"])
            mean_N = np.mean(data_plot[cur_mode]["N"])
            mean_U = np.mean(data_plot[cur_mode]["U"])
            std_E = np.std(data_plot[cur_mode]["E"])
            std_N = np.std(data_plot[cur_mode]["N"])
            std_U = np.std(data_plot[cur_mode]["U"])
            rms_E = dp.rms(data_plot[cur_mode]["E"])
            rms_N = dp.rms(data_plot[cur_mode]["N"])
            rms_U = dp.rms(data_plot[cur_mode]["U"])
            while Sigma_num_temp >= 1:
                indexs = []
                mean_E = np.mean(data_plot[cur_mode]["E"])
                mean_N = np.mean(data_plot[cur_mode]["N"])
                mean_U = np.mean(data_plot[cur_mode]["U"])
                std_E = np.std(data_plot[cur_mode]["E"])
                std_N = np.std(data_plot[cur_mode]["N"])
                std_U = np.std(data_plot[cur_mode]["U"])
                rms_E = dp.rms(data_plot[cur_mode]["E"])
                rms_N = dp.rms(data_plot[cur_mode]["N"])
                rms_U = dp.rms(data_plot[cur_mode]["U"])
                for ii in range(len(time_plot[cur_mode])):
                    if abs(data_plot[cur_mode]["E"][ii] - mean_E) > Sigma * std_E or abs(data_plot[cur_mode]["N"][ii] - mean_N) >  Sigma * std_N or abs(data_plot[cur_mode]["U"][ii] - mean_U) >  Sigma * std_U:
                        indexs.append(ii)
                data_plot[cur_mode]["E"] = np.delete(data_plot[cur_mode]["E"],indexs)
                data_plot[cur_mode]["N"] = np.delete(data_plot[cur_mode]["N"],indexs)
                data_plot[cur_mode]["U"] = np.delete(data_plot[cur_mode]["U"],indexs)
                data_plot[cur_mode]["NSAT"] = np.delete(data_plot[cur_mode]["NSAT"],indexs)
                data_plot[cur_mode]["PDOP"] = np.delete(data_plot[cur_mode]["PDOP"],indexs)
                time_plot[cur_mode] = np.delete(time_plot[cur_mode],indexs)
                Sigma_num_temp = Sigma_num_temp - 1
    #plot
    font = {'family': 'Times new roman','weight': 500,'size': 20}
    for i in range(N_mode):
        if N_mode < len(axP):
            plus_index = 1
        else:
            plus_index = 0
        data_plot[mode[i]]["E"] = data_plot[mode[i]]["E"] - np.mean(data_plot[mode[i]]["E"])
        data_plot[mode[i]]["N"] = data_plot[mode[i]]["N"] - np.mean(data_plot[mode[i]]["N"])
        data_plot[mode[i]]["U"] = data_plot[mode[i]]["U"] - np.mean(data_plot[mode[i]]["U"])
        axP[i+plus_index].scatter(time_plot[mode[i]],data_plot[mode[i]]["E"],s=5.5)
        axP[i+plus_index].scatter(time_plot[mode[i]],data_plot[mode[i]]["N"],s=5.5)
        axP[i+plus_index].scatter(time_plot[mode[i]],data_plot[mode[i]]["U"],s=5.5)
        axP[i+plus_index].set_ylim(-0.5,0.5)
        axP[i+plus_index].set_title(mode[i],font,loc = "left")
        axP[i+plus_index].fill_between(time_plot["Interpolation"][1000:1100],-0.5,0.5,facecolor = "gray",alpha=0.3)
        
    
    axP[0+plus_index].legend(["East direction","North direction","Up direction"],prop=font,
            framealpha=1,facecolor='none',ncol=4,numpoints=5,markerscale=3, 
            borderaxespad=0,bbox_to_anchor=(1,1.2),loc=1,frameon = False) 
    if N_mode < len(axP):
        colormap = sns.color_palette("muted",10)
        axP[0].grid(False)
        axP[0].plot(time_plot[mode[0]],data_plot[mode[0]]["NSAT"],color = colormap[0],ls = '-',linewidth = 1.5)
        axP[0].plot(time_plot[mode[1]],data_plot[mode[1]]["NSAT"],color = colormap[0],ls=':',linewidth = 1.5)
        font = {'family': 'Times new roman','weight': 600,'size': 23}
        axP[0].set_ylabel("Num of Sat",font,color = colormap[0])
        axP[0].spines['left'].set(color = colormap[0],linewidth = 2,linestyle = "-")
        axP[0].tick_params(length=6, width=2, color=colormap[0], labelcolor=colormap[0])
        font = {'family': 'Times new roman','weight': 500,'size': 20}
        axP[0].legend(["Interpolation","Grid"],prop=font,
            framealpha=1,facecolor='none',ncol=4,numpoints=5,markerscale=3, 
            borderaxespad=0,bbox_to_anchor=(1,1.2),loc=1,frameon = False) 
        leg = axP[0].get_legend()
        for legobj in leg.legendHandles:
            legobj.set_linewidth(3)
            legobj.set_color("black")
        font = {'family': 'Times new roman','weight': 600,'size': 23}
        axP2 = axP[0].twinx()
        axP2.grid(False)
        axP2.plot(time_plot[mode[0]],data_plot[mode[0]]["PDOP"],color = colormap[2],ls = '-',linewidth = 1.5)
        axP2.plot(time_plot[mode[1]],data_plot[mode[1]]["PDOP"],color = colormap[2],ls = ':',linewidth = 1.5)
        axP2.set_ylabel("PDOP",font,color = colormap[2])
        axP2.spines['right'].set(color = colormap[2],linewidth = 2,linestyle = "-")
        axP2.tick_params(length=6, width=2, color=colormap[2], labelcolor=colormap[2])
        labels = axP[0].get_xticklabels() + axP[0].get_yticklabels() + axP2.get_xticklabels() + axP2.get_yticklabels()
        [label.set_fontsize(18) for label in labels]
        [label.set_fontname('Times New Roman') for label in labels]

    axP[1+plus_index].set_ylabel("Position errors(m)",font)
    axP[2+plus_index].set_xlabel("Time(UTC)",font)
    axP[2+plus_index].set_xticks(XTick)
    axP[2+plus_index].set_xticklabels(XLabel)

    for i in range(N_mode):
        labels = labels + axP[i+plus_index].get_xticklabels() + axP[i+plus_index].get_yticklabels()
    [label.set_fontsize(18) for label in labels]
    [label.set_fontname('Times New Roman') for label in labels]
    
    # plt.savefig(r"E:\1Master_2\Paper_Grid\1-Paper_word\Image-1\SEPT-Dynamic-310.svg")
    # plt.savefig(r"E:\1Master_2\Paper_Grid\1-Paper_word\Image-1\SEPT-Dynamic-310.png",dpi=600)
    plt.show()
    
    
        

    

def plot_bias_grid(data = {},type = ["G","E","C"],mode = ["HKCL"],ylim = 1,starttime = 0,deltaT = 2,LastT=24,time = "UTC",save='',show = False,Fixed = False,delta_data = 30,year=2021,mon=4,day=10):
    N_plot = len(type)
    N_mode = len(mode)
    f1=5
    ymin = -ylim
    ymax = ylim
    figP,axP = plt.subplots(N_plot,1,figsize=(18,11),sharey=False,sharex=False)
    font = {'family': 'Times new roman','weight': 600,'size': 23}
    if (N_plot>3):
        axP[N_plot-2].set_xlabel('Time' + '(' + time + ')',font_label)
    else:
        axP[N_plot-1].set_xlabel('Time' + '(' + time + ')',font_label)
    font2 = {'family' : 'Arial',
		'weight' : 500,
		'size'   : 13,
            }
    
    for i in range(N_plot):
        font = {'family': 'Times new roman','weight': 600,'size': 23}
        axP[1].set_ylabel("Receiver DCB(m)",font_label)
        axP[i].grid(linestyle='--',linewidth=0.2, color='black',axis='both')
        if type[i] == "G" or type[i] == "E" or type[i] == "C":
            #  axP[i].set_ylim(ymin,ymax)
             font = {'family': 'Times new roman','weight': 600,'size': 20}
             axP[i].set_title(type[i],font_title)
        box = axP[i].get_position()
        if type[i] == "G" or type[i] == "E" or type[i] == "C":
            axP[i].set_position([box.x0, box.y0, box.width*0.9, box.height])
        box = axP[0].get_position()
        axP[0].set_position([box.x0, box.y0*1.023, box.width, box.height])
        box = axP[2].get_position()
        axP[2].set_position([box.x0, box.y0-0.015, box.width, box.height])
        # if type[i] == "RMS" or type[i] == "STD":
            # axP[i].set_position([box.x0, box.y0*0.9, box.width, box.height])
            #axP[i].set_ylim(0,0.6)

    [XLabel,XTick,cov_Time,begT,LastT]=xtick(time,year,mon,day,starttime,LastT,deltaT)

    time_G = [[] for i in range(N_mode)]
    time_E = [[] for i in range(N_mode)]
    time_C = [[] for i in range(N_mode)]
    data_plot = {}
    time_plot = {}
    data_G = [[] for i in range(N_mode)]
    data_E = [[] for i in range(N_mode)]
    data_C = [[] for i in range(N_mode)]
    data_S = [[] for i in range(N_mode)]
    Fixed_NUM = [[] for i in range(N_mode)]
    Float_NUM = [[] for i in range(N_mode)]
    ALL_NUM = [[] for i in range(N_mode)]

    for i in range(N_mode):
        Fixed_NUM[i] = 0
        Float_NUM[i] = 0
        ALL_NUM[i] = (LastT*3600) / delta_data + 1

    RMS_enu,STD_enu,MEAN_enu = {},{},{}
    
    time_sG = [[] for i in range(100)]
    time_sE = [[] for i in range(100)]
    time_sC = [[] for i in range(100)]
    time_TRP = []
    data_sG = [[] for i in range(100)]
    data_sE = [[] for i in range(100)]
    data_sC = [[] for i in range(100)]
    data_TRP = []

    for i in range(N_mode):
        for cur_time in data.keys():
            plot_time = (cur_time-cov_Time) / 3600
            if (plot_time >= begT and plot_time <= (begT + LastT)):
                if (mode[i] in data[cur_time]["G"].keys()):
                    data_G[i].append(data[cur_time]["G"][mode[i]])
                    time_G[i].append(plot_time) 
                if (mode[i] in data[cur_time]["E"].keys()):
                    data_E[i].append(data[cur_time]["E"][mode[i]])
                    time_E[i].append(plot_time) 
                if (mode[i] in data[cur_time]["C"].keys()):
                    data_C[i].append(data[cur_time]["C"][mode[i]])
                    time_C[i].append(plot_time) 
                if "ION" in type and cur_time in data["ION"].keys():
                    for sat in data["ION"][cur_time].keys():
                        prn = int(sat[1:3])
                        if sat[0] == "C":
                            data_sC[prn-1].append(data["ION"][cur_time][sat]["ION2"])
                            time_sC[prn-1].append(plot_time)
                        if sat[0] == "G":
                            data_sG[prn-1].append(data["ION"][cur_time][sat]["ION1"])
                            time_sG[prn-1].append(plot_time)
                        if sat[0] == "E":
                            data_sE[prn-1].append(data["ION"][cur_time][sat]["ION1"])
                            time_sE[prn-1].append(plot_time)
                if "TRP" in type and cur_time in data["ION"].keys():
                    for sat in data["ION"][cur_time].keys():
                        prn = int(sat[1:3])
                        data_TRP.append(data["ION"][cur_time][sat]["TRP1"])
                        time_TRP.append(plot_time)
                        break

    data_plot["G"] = data_G
    data_plot["E"] = data_E
    data_plot["C"] = data_C

    time_plot["G"] = time_G
    time_plot["E"] = time_E
    time_plot["C"] = time_C

    site_ploted={}
    site_ploted["G"] = []
    site_ploted["E"] = []
    site_ploted["C"] = []

    for i in range(N_plot):
        cur_type = type[i]
        RMS_enu[cur_type] = {}
        STD_enu[cur_type] = {}
        MEAN_enu[cur_type] = {}
        if (cur_type != "ION"):
            for j in range(N_mode):
                if cur_type == "TRP":
                    axP[i].scatter(time_TRP,data_plot[cur_type],s=1)
                    temp = dp.rms(data_plot[cur_type])
                    RMS_enu[cur_type].append(temp)
                    temp = np.std(data_plot[cur_type])
                    STD_enu[cur_type].append(temp)
                    temp = np.mean(data_plot[cur_type])
                    MEAN_enu[cur_type].append(temp)
                else:
                    if (cur_type != "RMS" and cur_type != "STD" and cur_type != "BOX" and cur_type != "BOX3"):
                        if (len(time_plot[cur_type][j]) > 0):
                            axP[i].scatter(time_plot[cur_type][j],data_plot[cur_type][j],s=1)
                            temp = dp.rms(data_plot[cur_type][j])
                            RMS_enu[cur_type][mode[j]] = (temp)
                            temp = np.std(data_plot[cur_type][j])
                            STD_enu[cur_type][mode[j]] = (temp)
                            temp = np.mean(data_plot[cur_type][j])
                            MEAN_enu[cur_type][mode[j]] = (temp)
                            if mode[j] not in site_ploted[cur_type]:
                                site_ploted[cur_type].append(mode[j])

        if (cur_type == "ION"):
            for sat_i in range(100):
                G,E,C = True,True,True
                num = len(time_sG[sat_i])
                if num < 1:
                    G = False
                num = len(time_sE[sat_i])
                if num < 1:
                    E = False
                num = len(time_sC[sat_i])
                if num < 1:
                    C = False
                if G:
                    axP[i].scatter(time_sG[sat_i],data_sG[sat_i],s=1)
                if E:
                    axP[i].scatter(time_sE[sat_i],data_sE[sat_i],s=1)
                if C:
                    axP[i].scatter(time_sC[sat_i],data_sC[sat_i],s=1)
    font_text = {'family' : 'Arial',
		'weight' : 500,
		'size'   : 15,
                }
    
    font = {'family': 'Times new roman','weight': 600,'size': 20}
    for i in range(N_plot):
        cur_type = type[i]
        if (cur_type != "RMS" and cur_type != "STD" and cur_type != "BOX3"):
            axP[i].set_xticks(XTick)
            axP[i].set_xticklabels(XLabel,fontsize = 18)
    axP[1].legend(site_ploted["G"],prop=font_legend,
                    framealpha=1,facecolor='none',ncol=1,numpoints=5, markerscale=10, 
                    bbox_to_anchor=(1.02,1.2),loc=0,borderaxespad=0) 
    # plt.tick_params(labelsize = 18)
    labels = axP[0].get_yticklabels() + axP[0].get_xticklabels() + axP[1].get_yticklabels() + axP[1].get_xticklabels() + axP[2].get_yticklabels() + axP[2].get_xticklabels()
    [label.set_fontsize(xtick_size) for label in labels]
    [label.set_fontname('Times New Roman') for label in labels]
    if ("RMS" in type or "BOX3" in type):
        last_plot = RMS_enu
    elif("STD" in type):
        last_plot = STD_enu
    #plot bar
    X_all = list(range(len(mode)))
    
    W = 0.25
    for i in range(N_plot):
        cur_type = type[i]
        if (cur_type == "RMS" or cur_type == "STD"):  
            isys=-1         
            for sys in last_plot.keys():
                barplot_data = []
                barplot_name = []
                x = []
                j=0
                for site in mode:
                    if site in last_plot[sys].keys():
                        barplot_data.append(last_plot[sys][site])
                        barplot_name.append(site)
                        x.append(X_all[j])
                    j=j+1

                for j in range(len(x)):
                    x[j] = x[j] + W*isys
                
                p1 = axP[i].bar(x,barplot_data,width = W,label='value')
                print(sys)
                print(np.mean(barplot_data))
                #axP[i].bar_label(p1,label_type='edge')
                isys=isys+1

    for i in range(N_plot):
        cur_type = type[i]
        if (cur_type == "BOX3"):  
            isys=-1         
            for sys in ["G"]:
                barplot_data = []
                barplot_name = []
                x = []
                j=0
                for j in range(N_mode):
                    if mode[j] in last_plot[sys].keys():
                        barplot_data.append(data_plot[sys][j])
                        barplot_name.append(mode[j])
                        x.append(X_all[j])

                for j in range(len(x)):
                    x[j] = x[j] + W*isys
                
                p1 = axP[i].boxplot(barplot_data)
                # print(sys)
                # print(np.mean(barplot_data))
                #axP[i].bar_label(p1,label_type='edge')
                isys=isys+1
    if ("RMS" in type or "BOX3" in type or "STD" in type):
        for sys in last_plot.keys():
            barplot_data = []
            barplot_name = []
            for site in last_plot[sys].keys():
                barplot_name.append(site)
            break
        sys = ["G","E","C"]
        if ('RMS' in type or 'STD' in type):
            axP[3].set_xticks(X_all)
            axP[3].set_xticklabels(mode)
            axP[3].legend(sys)
            axP[3].set_xlim(-0.5,len(mode)+0.5)
    # print("固定率:")
    # for i in range(N_mode):
    #     print(mode[i] + ':{:.2f}%'.format(Fixed_NUM[i] / (Fixed_NUM[i] + Float_NUM[i]) * 100))
    # print("完整率:")
    # for i in range(N_mode):
    #     print(mode[i] + ':{:.2f}%'.format((Fixed_NUM[i] + Float_NUM[i]) / ALL_NUM[i] * 100))

    labels = axP[0].get_yticklabels() + axP[0].get_xticklabels() + axP[1].get_yticklabels() + axP[1].get_xticklabels() + axP[2].get_yticklabels() + axP[2].get_xticklabels()
    plt.savefig(r"D:\A-paper\Fig_and_Res\HB-306-RDCB.png",dpi=600)
    plt.savefig(r"D:\A-paper\Fig_and_Res\HB-306-RDCB.svg")
    plt.show()

def plot_SatofAug(data = {},type = ["E","N","U"],mode = ["DEFAULT"],ylim = 1,starttime = 0,deltaT = 2,LastT=24,time = "UTC",save='',show = False,Fixed = False,delta_data = 30,year=2021,mon=4,day=10,all=False):
    #with plt.style.context("science","grid"):
        N_plot = 1
        N_mode = len(mode)
        f1=5
        ymin = -ylim
        ymax = ylim
        
        figP,axP = plt.subplots(N_plot,1,figsize=(12,10),sharey=False,sharex=True)
        axP.set_xlabel('Time' + '(' + time + ')')
        font2 = {'family' : 'Times new roman',
            'weight' : 600,
            'size'   : 15,
                }
        axP.set_title("Number of Satellite",font)
        
        if "+" in time:
            end_time = len(time)
            delta_Time = int(time[3:end_time]) + starttime
            begT = int(time[3:end_time]) + starttime
        else:
            delta_Time = starttime
            begT=starttime
        #for time in data[mode[0]].keys():
        secow_start = tr.ymd2gpst(year,mon,day,0,00,00)
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


        time = [[] for i in range(N_mode)]
        data_plot = {}
        data_E = [[] for i in range(N_mode)]
        data_N = [[] for i in range(N_mode)]
        data_U = [[] for i in range(N_mode)]
        data_S = [[] for i in range(N_mode)]
        Fixed_NUM = [[] for i in range(N_mode)]
        Float_NUM = [[] for i in range(N_mode)]
        ALL_NUM = [[] for i in range(N_mode)]

        for i in range(N_mode):
            Fixed_NUM[i] = 0
            Float_NUM[i] = 0
            ALL_NUM[i] = (LastT*3600) / delta_data + 1

        RMS_enu,STD_enu,MEAN_enu = {},{},{}
        
        time_sG = [[] for i in range(100)]
        time_sE = [[] for i in range(100)]
        time_sC = [[] for i in range(100)]
        time_TRP = []
        data_sG = [[] for i in range(100)]
        data_sE = [[] for i in range(100)]
        data_sC = [[] for i in range(100)]
        data_TRP = []

        for i in range(N_mode):
            for cur_time in data[mode[i]].keys():
                plot_time = (cur_time-cov_Time) / 3600
                if ((plot_time >= begT and plot_time <= (begT + LastT)) or all):
                    time[i].append(plot_time)
                    data_E[i].append(len(data[mode[i]][cur_time]))

        data_plot["E"] = data_E

        for i in range(N_plot):
            cur_type = "E"
            RMS_enu[cur_type] = []
            STD_enu[cur_type] = []
            MEAN_enu[cur_type] = []
            if (cur_type != "ION"):
                for j in range(N_mode):
                    temp = np.mean(data_plot[cur_type][j])
                    MEAN_enu[cur_type].append(temp)
                    # data_plot[cur_type][j] = data_plot[cur_type][j]-temp
                    axP.scatter(time[j],data_plot[cur_type][j])
                    temp = dp.rms(data_plot[cur_type][j])
                    RMS_enu[cur_type].append(temp)
                    temp = np.std(data_plot[cur_type][j])
                    STD_enu[cur_type].append(temp)
                        
            
        font_text = {'family' : 'Times new roman',
            'weight' : 600,
            'size'   : 15,
                    }
        for i in range(N_plot):
            cur_type = "E"
            RMS_str = "RMS:"
            MEAN_str = "MEAN:"
            for j in range(N_mode):
                if cur_type == "E":
                    MEAN_str = MEAN_str +'{:.2f}, '.format(MEAN_enu[cur_type][j])
            if cur_type == "E":
                ax_range = axP.axis()
                #print(len(RMS_str))
                #RMS_str[len(RMS_str)-2:len(RMS_str)] = ""
                axP.text(ax_range[0],ax_range[3]+ylim/15,MEAN_str[0:7*N_mode+3],font_text)


        axP.set_xticks(XTick)
        axP.set_xticklabels(XLabel)
        # axP[0].legend(mode,
        #         framealpha=1,facecolor='w',ncol=1,numpoints=5, markerscale=5, 
        #         bbox_to_anchor=(1,1),loc=0,borderaxespad=0) 
        
            
        for i in range(N_plot):
            cur_type="E"
            axP.set_xticks(XTick)
            ax_range = axP.axis()
            
            axP.legend(mode,prop=font_text,
            framealpha=1,facecolor='none',ncol=4,numpoints=5, markerscale=1.3, 
            borderaxespad=0,bbox_to_anchor=(1,1.12),loc=1) 
            #axP[i].autoscale(tight=True)
            if cur_type == "E" or cur_type == "N" or cur_type == "U":
                print("\n"+cur_type)
                for j in range(N_mode):
                    print(mode[j] + ":")
                    print('RMS={:.4f}cm,MEAN={:.4f}cm,STD={:.4f}cm'.format(RMS_enu[cur_type][j]*100,MEAN_enu[cur_type][j]*100,STD_enu[cur_type][j]*100))

        plt.show()


def plot_aug_NSAT(data = {},mode = {},type = "NSAT",freq = 1,ylim = 1,starttime = 0,deltaT = 2,LastT=24,time = "UTC",save='',show = False,year = 2021,mon=11,day=1,deltaData=5):
    sys_type = {}
    RMS_G,MEAN_G,STD_G = [[],[]],[[],[]],[[],[]]
    RMS_E,MEAN_E,STD_E = [[],[]],[[],[]],[[],[]]
    RMS_C,MEAN_C,STD_C = [[],[]],[[],[]],[[],[]]

    RMS_G1,MEAN_G1,STD_G1 = [[],[]],[[],[]],[[],[]]
    RMS_E1,MEAN_E1,STD_E1 = [[],[]],[[],[]],[[],[]]
    RMS_C1,MEAN_C1,STD_C1 = [[],[]],[[],[]],[[],[]]
    num_plot = len(mode)
    G_L,E_L,C_L = [],[],[]
    if type == 'NSAT':
        f1=0
        f2=1
        num_mode = len(mode)
        figP,axP = plt.subplots(num_mode,1,figsize=(12,8),sharey=True,sharex=True)
        ymin = -ylim
        ymax = ylim
        col = 2
        for i in range(num_mode):
            axP[i].set_xlabel('Time' + '(' + time + ')')
            # axP[i].set_ylabel('Num of Fixed Sat',font)
            axP[i].set_ylabel('Num of Obs Sat',font)
            axP[i].set_title(mode[i])
            axP[i].grid(linestyle='--',linewidth=0.2, color='black',axis='both')
    else:
        print("Wrong mode")
    
    time_G = [[] for i in range(100)]
    time_R = [[] for i in range(100)]
    time_E = [[] for i in range(100)]
    time_C = [[] for i in range(100)]
    time_TRP = []
    data_G = [[] for i in range(100)]
    data_R = [[] for i in range(100)]
    data_E = [[] for i in range(100)]
    data_C = [[] for i in range(100)]
    data_TRP = []
    data_G1 = [[] for i in range(100)]
    data_R1 = [[] for i in range(100)]
    data_E1 = [[] for i in range(100)]
    data_C1 = [[] for i in range(100)]
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
   
    if type == "NSAT":
        for j in range(num_mode):
            start = False
            time_last = 0
            for time in data[mode[j]].keys():
                num_C,num_G,num_E = 0,0,0
                plot_time = (time - cov_Time) / 3600
                # if ((time - time_last) > deltaData and start):
                #     data_C[j].append(0)
                #     time_C[j].append(plot_time)
                #     data_G[j].append(0)
                #     time_G[j].append(plot_time)
                #     data_E[j].append(0)
                #     time_E[j].append(0)
                #     data_R[j].append(0)
                #     time_R[j].append(plot_time)
                time_last = time
                if (plot_time > begT and plot_time < begT + LastT):
                    start = True
                    for sat in data[mode[j]][time].keys():
                        prn = int(sat[1:3])
                        if sat[0] == "C":
                            num_C = num_C + 1
                        if sat[0] == "G":
                            num_G = num_G + 1
                        if sat[0] == "E":
                            num_E = num_E + 1
                    data_C[j].append(num_C)
                    time_C[j].append(plot_time)
                    data_G[j].append(num_G)
                    time_G[j].append(plot_time)
                    data_E[j].append(num_E)
                    time_E[j].append(plot_time)
                    data_R[j].append(num_C+num_G+num_E)
                    time_R[j].append(plot_time)
    mean_Sat_C,mean_Sat_E,mean_Sat_G,mean_Sat_R={},{},{},{}
    if type == "NSAT":
        for j in range(num_mode):
            # axP[j].plot(time_R[j],data_R[j])
            axP[j].scatter(time_R[j],data_R[j])
            axP[j].set_xticks(XTick)
            mean_Sat_G[mode[j]]=np.mean(data_G[j])
            mean_Sat_E[mode[j]]=np.mean(data_E[j])
            mean_Sat_C[mode[j]]=np.mean(data_C[j])
            mean_Sat_R[mode[j]]=np.mean(data_R[j])
        
        font_text = {'family' : 'Arial',
		'weight' : 500,
		'size'   : 15,
                }
        axP[j].set_xticklabels(XLabel)
    
    
    
    if type == "NSAT":
        for j in range(num_mode):      
            ax_range = axP[j].axis()
            font2 = {"size":20}
            axP[j].text(ax_range[0],ax_range[3],r'ALL: {:.1f}, G: {:.1f}, E: {:.1f}, C: {:.1f}'.format(mean_Sat_R[mode[j]],mean_Sat_G[mode[j]],mean_Sat_E[mode[j]],mean_Sat_C[mode[j]]),font2)
    
    # figP.suptitle(mode)
    #plt.savefig(savedir)
    if show:
        plt.show()  


def plot_e_n_u_percent(site = "Default",data = {},type = ["Horizontal","Vertical","Position"],modelist = ["DEFAULT"],sitelist = ["HJJ"],ylim = 1,starttime = 0,deltaT = 2,LastT=24,time = "UTC",save='',show = False,Fixed = False,delta_data = 30,year=2021,mon=4,day=10,all=False,percent=90):
    N_plot = len(type)
    N_mode = len(modelist)
    f1=5
    ymin = 0.0
    ymax = ylim
    figP,axP = plt.subplots(1,N_plot,figsize=(9,9),sharey=False,sharex=True)
    font = {'family' : 'Times New Roman',
		'weight' : 500,
		'size'   : 20,
        }
    for i in range(N_plot):
        if N_plot == 1:
            axP.set_ylim(ymin,ymax)
            font2 = {'family' : 'Times new roman','weight' : 600,'size'   : 23}
            axP.set_ylabel("3D " + type[i] + " Errors(m)",font2)
            axP.set_xlabel("Time(min)",font2)
            axP.set_title(site.format(percent*100),font2)
            if type[i] != "Horizontal" and type[i] != "Vertical" and type[i] != "Position":
                return
        else:
            axP[i].set_ylim(ymin,ymax)
            font2 = {'family' : 'Times new roman','weight' : 300,'size'   : 22}
            axP[i].set_ylabel(type[i] + " Diff/m",font2)
            axP[i].set_title("{:.0f}-Percent".format(percent*100),font2)
            if type[i] != "Horizontal" and type[i] != "Vertical" and type[i] != "Position":
                return
    
    data_plot = {}
    time_plot = {}
    end_secs = LastT * 3600
    Sec_Start = 0
    XLabel,XTick = [],[]
    tick_temp = 0
    while tick_temp <= LastT * 60:
        XTick.append(tick_temp)
        XLabel.append("{:0>2d}".format(tick_temp))
        tick_temp = tick_temp + deltaT
    while Sec_Start < end_secs:
        for mode in data:
            Horizon_temp,Vertical_temp,Position_temp = [],[],[]
            if mode not in data_plot.keys():
                data_plot[mode] = {}
                data_plot[mode]["Horizontal"],data_plot[mode]["Vertical"],data_plot[mode]["Position"] = [],[],[]
                time_plot[mode] = []
            for cur_site in sitelist:
                if cur_site in data[mode].keys():
                    for cur_doy in data[mode][cur_site].keys():
                        if Sec_Start in data[mode][cur_site][cur_doy].keys():
                            if data[mode][cur_site][cur_doy][Sec_Start]["AMB"] == 0:
                                continue
                            Vertical_temp.append(abs(data[mode][cur_site][cur_doy][Sec_Start]["U"]))
                            Horizon_temp.append(math.sqrt(math.pow(data[mode][cur_site][cur_doy][Sec_Start]["E"],2)+math.pow(data[mode][cur_site][cur_doy][Sec_Start]["N"],2)))
                            Position_temp.append(math.sqrt(math.pow(data[mode][cur_site][cur_doy][Sec_Start]["E"],2)+math.pow(data[mode][cur_site][cur_doy][Sec_Start]["N"],2)+math.pow(data[mode][cur_site][cur_doy][Sec_Start]["U"],2)))
                        else:
                            continue
                else:
                    continue
            size_data = len(Vertical_temp)
            if size_data>=1:
                time_plot[mode].append(Sec_Start/60)
                Vertical_temp.sort()
                Horizon_temp.sort()
                Position_temp.sort()
                percent_size = int(size_data * percent)
                # data_plot[mode]["Horizontal"].append(np.mean(Horizon_temp[0:percent_size]))
                # data_plot[mode]["Vertical"].append(np.mean(Vertical_temp[0:percent_size]))
                # data_plot[mode]["Position"].append(np.mean(Position_temp[0:percent_size]))
                # data_plot[mode]["Horizontal"].append((Horizon_temp[percent_size]))
                # data_plot[mode]["Vertical"].append((Vertical_temp[percent_size]))
                # data_plot[mode]["Position"].append((Position_temp[percent_size]))
                data_plot[mode]["Horizontal"].append(np.mean(Horizon_temp))
                data_plot[mode]["Vertical"].append(np.mean(Vertical_temp))
                data_plot[mode]["Position"].append(np.mean(Position_temp))
        Sec_Start = Sec_Start + delta_data
    
    for cur_mode in data_plot.keys():
        count_20,count_10,count_5 = 0,0,0
        bool_20,bool_10,bool_5 = False,False,False
        for i in range(len(data_plot[cur_mode]["Position"])):
            if data_plot[cur_mode]["Position"][i] > 0.05:
                 count_5 = 0
            if data_plot[cur_mode]["Position"][i] > 0.1:
                 count_10,count_5 = 0,0 
            if data_plot[cur_mode]["Position"][i] > 0.2:
                 count_20,count_10,count_5 = 0,0,0    
            if data_plot[cur_mode]["Position"][i] <= 0.2:
                count_20 = count_20 + 1
            if data_plot[cur_mode]["Position"][i] <= 0.1:
                count_10 = count_10 + 1
            if data_plot[cur_mode]["Position"][i] <= 0.05:
                count_5 = count_5 + 1
            if count_20 == 10 and not bool_20:
                print("{},20-{:.1f}".format(cur_mode,time_plot[cur_mode][i]*60/delta_data - 9))
                bool_20 = True
            if count_10 == 10 and not bool_10:
                print("{},10-{:.1f}".format(cur_mode,time_plot[cur_mode][i]*60/delta_data - 9))
                bool_10 = True
            if count_5 == 10 and not bool_5:
                print("{}, 5-{:.1f}".format(cur_mode,time_plot[cur_mode][i]*60/delta_data - 9))
                bool_5 = True

    for i in range(N_plot):
        if N_plot == 1:
            for cur_mode in data_plot.keys():
                axP.plot(time_plot[cur_mode],data_plot[cur_mode][type[i]],linewidth =2)
            font = {'family': 'Times new roman','weight': 600,'size': 20}
            axP.legend(modelist,prop=font,
                framealpha=1,facecolor='none',ncol=1,numpoints=5,markerscale=5, 
                borderaxespad=0,loc=1)
            leg = axP.get_legend()
            for legobj in leg.legendHandles:
                legobj.set_linewidth(5)
            axP.grid(False)
            axP.set_xticks(XTick)
            axP.set_xticklabels(XLabel)
            labels = axP.get_xticklabels() + axP.get_yticklabels()
            [label.set_fontsize(18) for label in labels]
            [label.set_fontname('Times New Roman') for label in labels]
        else:
            for cur_mode in data_plot.keys():
                axP[i].scatter(time_plot[mode],data_plot[cur_mode][type[i]],s=1)
            axP[i].legend(modelist,prop=font2,markerscale=5)
            axP[i].grid(False)
    plt.axhline(0.20,color='gray',ls="--")
    plt.axhline(0.10,color='gray',ls="--")
    # plt.axhline(0.05,color='gray',ls="--")
    # plt.savefig(r"E:\1Master_2\Paper_Grid\1-Paper_word\Image-1"+"\\"+site+"-Percent.svg")
    # plt.savefig(r"E:\1Master_2\Paper_Grid\1-Paper_word\Image-1"+"\\"+site+"-Percent.png",dpi=600)
    plt.show()

def plot_aug_GEC_new(data = {},head = {},type = "ION",freq = 1,ylim = 1,starttime = 0,deltaT = 2,LastT=24,time = "UTC",save='',show = False,year = 2021,mon=11,day=1):
    sys_type = {}
    RMS_G,MEAN_G,STD_G = [[],[]],[[],[]],[[],[]]
    RMS_E,MEAN_E,STD_E = [[],[]],[[],[]],[[],[]]
    RMS_C,MEAN_C,STD_C = [[],[]],[[],[]],[[],[]]

    RMS_G1,MEAN_G1,STD_G1 = [[],[]],[[],[]],[[],[]]
    RMS_E1,MEAN_E1,STD_E1 = [[],[]],[[],[]],[[],[]]
    RMS_C1,MEAN_C1,STD_C1 = [[],[]],[[],[]],[[],[]]
    G_L,E_L,C_L = [],[],[]
    if type == 'ION':
        f1=5
        ymin = -ylim
        ymax = ylim
        col = 1
        figP,axP = plt.subplots(1,1,figsize=(15,9),sharey=True,sharex=True)
        axP.set_xlabel('Time' + '(' + time + ')',font_label)
        axP.set_ylabel('Difference of Ionosphere Delay correction/m',font_label)
        axP.grid(linestyle='--',linewidth=0.2, color='black',axis='both')
        axP.set_ylim(ymin,ymax)
        box = axP.get_position()
        axP.set_position([box.x0, box.y0, box.width*0.88, box.height])
        if freq==1:
            sys_type["C"] = "ION2"
            sys_type["G"] = "ION1"
            sys_type["E"] = "ION1"  
        else:
            sys_type["C"] = "ION7"
            sys_type["G"] = "ION2"
            sys_type["E"] = "ION5" 
    
    time_G = [[] for i in range(100)]
    time_R = [[] for i in range(100)]
    time_E = [[] for i in range(100)]
    time_C = [[] for i in range(100)]
    time_TRP = []
    data_G = [[] for i in range(100)]
    data_R = [[] for i in range(100)]
    data_E = [[] for i in range(100)]
    data_C = [[] for i in range(100)]
    data_TRP = []
    data_G1 = [[] for i in range(100)]
    data_R1 = [[] for i in range(100)]
    data_E1 = [[] for i in range(100)]
    data_C1 = [[] for i in range(100)]
    
    [XLabel,XTick,cov_Time,begT,LastT]=xtick(time,year,mon,day,starttime,LastT,deltaT)
    if type == "L" or type == "P":
        for time in data.keys():
            plot_time = (time - cov_Time) / 3600
            if (plot_time > begT and plot_time < begT + LastT):
                for sat in data[time].keys():
                    prn = int(sat[1:3])
                    # if abs(data[time][sat][sys_type[sat[0]]]) > -1:
                    if sat[0] == "C":
                        data_C[prn-1].append(data[time][sat][sys_type[sat[0]]["1"]])
                        data_C1[prn-1].append(data[time][sat][sys_type[sat[0]]["2"]])
                        time_C[prn-1].append(plot_time)
                    if sat[0] == "G":
                        data_G[prn-1].append(data[time][sat][sys_type[sat[0]]["1"]])
                        data_G1[prn-1].append(data[time][sat][sys_type[sat[0]]["2"]])
                        time_G[prn-1].append(plot_time)
                    if sat[0] == "E":
                        data_E[prn-1].append(data[time][sat][sys_type[sat[0]]["1"]])
                        data_E1[prn-1].append(data[time][sat][sys_type[sat[0]]["2"]])
                        time_E[prn-1].append(plot_time)
    
    if type == "ION" or type == "diffIon":
        for time in data.keys():
            plot_time = (time - cov_Time) / 3600
            if (plot_time > begT and plot_time < begT + LastT):
                for sat in data[time].keys():
                    prn = int(sat[1:3])
                    if sys_type[sat[0]] not in data[time][sat].keys():
                        continue
                    if abs(data[time][sat][sys_type[sat[0]]]) == 0:
                        continue
                    if abs(data[time][sat][sys_type[sat[0]]]) < 0.1:
                        if sat[0] == "C" and sys_type[sat[0]] in data[time][sat].keys():
                            data_C[prn-1].append(data[time][sat][sys_type[sat[0]]])
                            time_C[prn-1].append(plot_time)
                        if sat[0] == "G" and sys_type[sat[0]] in data[time][sat].keys():
                            data_G[prn-1].append(data[time][sat][sys_type[sat[0]]])
                            time_G[prn-1].append(plot_time)
                        if sat[0] == "E" and sys_type[sat[0]] in data[time][sat].keys():
                            data_E[prn-1].append(data[time][sat][sys_type[sat[0]]])
                            time_E[prn-1].append(plot_time)
    if type == "NSAT":
        for time in data.keys():
            num_C,num_G,num_E = 0,0,0
            plot_time = (time - cov_Time) / 3600
            if (plot_time > begT and plot_time < begT + LastT):
                for sat in data[time].keys():
                    prn = int(sat[1:3])
                    if sat[0] == "C":
                        num_C = num_C + 1
                    if sat[0] == "G":
                        num_G = num_G + 1
                    if sat[0] == "E":
                        num_E = num_E + 1
                
                data_C[0].append(num_C)
                time_C[0].append(plot_time)
                data_G[0].append(num_G)
                time_G[0].append(plot_time)
                data_E[0].append(num_E)
                time_E[0].append(plot_time)
    if type == "TRP":
        for time in data.keys():
            plot_time = (time - cov_Time) / 3600
            if (plot_time > begT and plot_time < begT + LastT):
                for sat in data[time].keys():
                    prn = int(sat[1:3])
                    data_TRP.append(data[time][sat][sys_type[sat[0]]])
                    time_TRP.append(plot_time)
                    break
    if type == "NSAT":
        axP[0].scatter(time_G[0],data_G[0])
        axP[1].scatter(time_E[0],data_E[0])
        axP[2].scatter(time_C[0],data_C[0])
        mean_Sat_G=np.mean(data_G[0])
        mean_Sat_E=np.mean(data_E[0])
        mean_Sat_C=np.mean(data_C[0])
        axP[2].set_xticks(XTick)
        axP[1].set_xticks(XTick)
        axP[0].set_xticks(XTick)
        axP[2].set_xticklabels(XLabel)
    if type == "ION" or type == "diffIon":
        for i in range (100):
            if len(time_G[i]) > 1:
                axP.scatter(time_G[i],data_G[i],s=1)
                prn = '%02d' % (i + 1)
                G_L.append('G'+prn)
                temp = dp.rms(data_G[i])
                RMS_G[0].append(temp)
                temp = np.std(data_G[i])
                STD_G[0].append(temp)
                temp = np.mean(data_G[i])
                MEAN_G[0].append(temp)
        for i in range (100):
            if len(time_E[i]) > 1:
                axP.scatter(time_E[i],data_E[i],s=1)
                prn = '%02d' % (i + 1)
                G_L.append('E'+prn)
                temp = dp.rms(data_E[i])
                RMS_G[0].append(temp)
                temp = np.std(data_E[i])
                STD_G[0].append(temp)
                temp = np.mean(data_E[i])
                MEAN_G[0].append(temp)
        for i in range (100):
            if len(time_C[i]) > 1:
                axP.scatter(time_C[i],data_C[i],s=1)
                prn = '%02d' % (i + 1)
                G_L.append('C'+prn)
                temp = dp.rms(data_C[i])
                RMS_G[0].append(temp)
                temp = np.std(data_C[i])
                STD_G[0].append(temp)
                temp = np.mean(data_C[i])
                MEAN_G[0].append(temp)
        
       
        font2 = {'family' : 'Times New Roman',
		'weight' : 400,
		'size'   : 12,
                }
        ax_range = axP.axis()
        axP.legend(G_L,prop=font_legend,
            framealpha=1,facecolor='w',ncol=2,numpoints=5, markerscale=10, 
            bbox_to_anchor=(1.01,1),loc=2,borderaxespad=0)
        axP.text(ax_range[0],ax_range[3],r'MEAN={:.4f}cm, RMS={:.4f}cm, STD={:.4f}cm'.format(np.mean(MEAN_G[0])*100, np.mean(RMS_G[0])*100, np.mean(STD_G[0])*100),font_text)
        axP.text(ax_range[0],0.08,'Interpolation',font_title)
        axP.set_xticks(XTick)
        axP.set_xticklabels(XLabel)
    
    if type == "TRP":
        axP.scatter(time_TRP,data_TRP,s=1)
        temp = dp.rms(data_TRP)
        RMS_G[0].append(temp)
        temp = np.std(data_TRP)
        STD_G[0].append(temp)
        temp = np.mean(data_TRP)
        MEAN_G[0].append(temp)   
        font2 = {"size":7}
        ax_range = axP.axis()
        axP.text(ax_range[0],ax_range[3],r'MEAN={:.4f}cm, RMS={:.4f}cm, STD={:.4f}cm'.format(np.mean(MEAN_G[0])*100, np.mean(RMS_G[0])*100, np.mean(STD_G[0])*100),font_text)
        axP.set_xticks(XTick)
        axP.set_xticklabels(XLabel)
    if type == "NSAT":
        ax_range = axP[0].axis()
        font2 = {"size":20}
        axP[0].text(ax_range[0],ax_range[3],r'ALL: {:.1f}, G: {:.1f}, E: {:.1f}, C: {:.1f}'.format(mean_Sat_C+mean_Sat_E+mean_Sat_G,mean_Sat_G,mean_Sat_E,mean_Sat_C),font2)
    if type == "L" or type=="P":
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
                if G:
                    axP[0][0].scatter(time_G[i],data_G[i],s=1)
                    axP[0][1].scatter(time_G[i],data_G1[i],s=1)
                    prn = '%02d' % (i + 1)
                    G_L.append('G'+prn)
                    temp = dp.rms(data_G[i])
                    RMS_G[0].append(temp)
                    temp = dp.rms(data_G1[i])
                    RMS_G1[0].append(temp)
                    temp = np.std(data_G[i])
                    STD_G[0].append(temp)
                    temp = np.mean(data_G[i])
                    MEAN_G[0].append(temp)
                if E:
                    axP[1][0].scatter(time_E[i],data_E[i],s=1)
                    axP[1][1].scatter(time_E[i],data_E1[i],s=1)
                    prn = '%02d' % (i + 1)
                    E_L.append('E'+prn)
                    temp = dp.rms(data_E[i])
                    RMS_E[0].append(temp)
                    temp = dp.rms(data_E1[i])
                    RMS_E1[0].append(temp)
                    temp = np.std(data_E[i])
                    STD_E[0].append(temp)
                    temp = np.mean(data_E[i])
                    MEAN_E[0].append(temp)
                if C:
                    axP[2][0].scatter(time_C[i],data_C[i],s=1)
                    axP[2][1].scatter(time_C[i],data_C1[i],s=1)
                    prn = '%02d' % (i + 1)
                    C_L.append('C'+prn)
                    temp = dp.rms(data_C[i])
                    RMS_C[0].append(temp)
                    temp = dp.rms(data_C1[i])
                    RMS_C1[0].append(temp)
                    temp = np.std(data_C[i])
                    STD_C[0].append(temp)
                    temp = np.mean(data_C[i])
                    MEAN_C[0].append(temp)
        font2 = {"size":7}
        axP[0][1].legend(G_L,prop=font2,
            framealpha=1,facecolor='w',ncol=2,numpoints=5, markerscale=2, 
            bbox_to_anchor=(1.01,1),loc=2,borderaxespad=0)
        ax_range = axP[0][0].axis()
        axP[0][0].text(ax_range[0],ax_range[3],r'RMS={:.4f}cm'.format(np.mean(RMS_G[0])*100),font_text)
        ax_range = axP[0][1].axis()
        axP[0][1].text(ax_range[0],ax_range[3],r'RMS={:.4f}cm'.format(np.mean(RMS_G1[0])*100),font_text)
        axP[1][1].legend(E_L,prop=font2,
            framealpha=1,facecolor='w',ncol=2,numpoints=5, markerscale=2, 
            bbox_to_anchor=(1.01,1),loc=2,borderaxespad=0)
        ax_range = axP[1][0].axis()
        axP[1][0].text(ax_range[0],ax_range[3],r'RMS={:.4f}cm'.format(np.mean(RMS_E[0])*100),font_text)
        ax_range = axP[1][1].axis()
        axP[1][1].text(ax_range[0],ax_range[3],r'RMS={:.4f}cm'.format(np.mean(RMS_E1[0])*100),font_text)
        axP[2][1].legend(C_L,prop=font2,
            framealpha=1,facecolor='w',ncol=2,numpoints=5, markerscale=2, 
            bbox_to_anchor=(1.01,1),loc=2,borderaxespad=0)
        ax_range = axP[2][0].axis()
        axP[2][0].text(ax_range[0],ax_range[3],r'RMS={:.4f}cm'.format(np.mean(RMS_C[0])*100),font_text)
        ax_range = axP[2][1].axis()
        axP[2][1].text(ax_range[0],ax_range[3],r'RMS={:.4f}cm'.format(np.mean(RMS_C1[0])*100),font_text)
        axP[0][1].set_xticks(XTick)
        axP[0][0].set_xticks(XTick)
        axP[1][1].set_xticks(XTick)
        axP[1][0].set_xticks(XTick)
        axP[2][1].set_xticks(XTick)
        axP[2][0].set_xticks(XTick)
        axP[2][0].set_xticklabels(XLabel)
        axP[2][1].set_xticklabels(XLabel)
    
    # figP.suptitle(mode)
    # savedir = save + ".jpg"
    plt.savefig(r"D:\A-paper\Fig_and_Res\K070-Grid.png")
    if type == "ION":
        labels = axP.get_xticklabels() + axP.get_yticklabels()
        [label.set_fontsize(xtick_size) for label in labels]
    if type == "TRP":
        labels = axP.get_xticklabels() + axP.get_yticklabels()
        [label.set_fontsize(15) for label in labels]
    if show:
        plt.savefig(r"D:\A-paper\Fig_and_Res\K070-306-AUG-Interpolation.png",dpi=600)
        plt.show()  