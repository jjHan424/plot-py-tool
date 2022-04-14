'''
Author: Junjie Han
Date: 2021-09-23 10:14:18
LastEditTime: 2022-04-14 22:23:10
LastEditors: Please set LastEditors
Description: In User Settings Edit
FilePath: /plot-toolkit-master/jjHan_py_plot/draw.py
'''

from matplotlib.markers import MarkerStyle
import numpy as np
import matplotlib as mpl
mpl.use("TkAgg")
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from numpy.core.fromnumeric import shape, size
import dataprocess as dp
import matplotlib.colors as colors
import seaborn as sns
import math
font = {'family' : 'Arial',
		'weight' : 500,
		'size'   : 20,
}


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

def plot_aug_GEC_new(data = {},head = {},type = "ION",freq = 1,ylim = 1,starttime = 0,deltaT = 2,begT = 0,LastT=24,time = "UTC",save='',show = False):
    sys_type = {}
    RMS_G,MEAN_G,STD_G = [[],[]],[[],[]],[[],[]]
    RMS_E,MEAN_E,STD_E = [[],[]],[[],[]],[[],[]]
    RMS_C,MEAN_C,STD_C = [[],[]],[[],[]],[[],[]]
    G_L,E_L,C_L = [],[],[]
    if type == 'P':
        f1=0
        f2=1
        figP,axP = plt.subplots(3,2,figsize=(15,10),sharey=True,sharex=True)
        ymin = -ylim
        ymax = ylim
        col = 2
        
        axP[2][0].set_xlabel('Time' + '(' + time + ')')
        axP[2][1].set_xlabel('Time' + '(' + time + ')')
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
    elif type == 'L':
        f1=2
        f2=3
        figP,axP = plt.subplots(3,2,figsize=(20,10),sharey=True,sharex=True)
        ymin = -ylim
        ymax = ylim
        col = 2
        axP[2][0].set_xlabel('Time' + '(' + time + ')')
        axP[2][1].set_xlabel('Time' + '(' + time + ')')
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
    elif type == 'ION':
        f1=5
        ymin = -ylim
        ymax = ylim
        col = 1
        figP,axP = plt.subplots(3,1,figsize=(20,10),sharey=True,sharex=True)
        axP[2].set_xlabel('Time' + '(' + time + ')')
        axP[1].set_ylabel('Difference of Ionosphere Delay correction/m',font)
        axP[0].set_title('G')
        axP[1].set_title('E')
        axP[2].set_title('C')
        for i in range(3):
                axP[i].grid(linestyle='--',linewidth=0.2, color='black',axis='both')
                # axP[i].set_ylim(ymin,ymax)
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
        figP,axP = plt.subplots(1,1,figsize=(20,10),sharey=True,sharex=True)
        axP.set_xlabel('Time' + '(' + time + ')')
        axP.set_ylabel('Difference of Troposphere Delay correction/m',font)
        axP.grid(linestyle='--',linewidth=0.2, color='black',axis='both')
        axP.set_ylim(ymin,ymax)
        sys_type["C"]="TRP1"
        sys_type["G"]="TRP1"
        sys_type["E"]="TRP1"
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
    if "+" in time:
        end_time = len(time)
        delta_Time = int(time[3:end_time]) + starttime
    else:
        delta_Time = starttime
    for time in data.keys():
        cov_Time = time - delta_Time * 3600
        break
    end_Time = begT + LastT
    delta_X = math.ceil((LastT)/deltaT)
    XLabel = []
    XTick = []
    starttime = begT - deltaT
    for i in range(delta_X):
        starttime = starttime + deltaT
        cur_Str_X = '%02d' % (starttime % 24) + ":00"
        XLabel.append(cur_Str_X)
        XTick.append(starttime)       
    if starttime < end_Time:
        starttime = starttime + deltaT
        cur_Str_X = '%02d' % (starttime % 24) + ":00"
        XLabel.append(cur_Str_X)
        XTick.append(starttime)


    if type == "ION":
        for time in data.keys():
            plot_time = (time - cov_Time) / 3600
            if (plot_time > begT and plot_time < begT + LastT):
                for sat in data[time].keys():
                    prn = int(sat[1:3])
                    if sys_type[sat[0]] not in data[time][sat].keys():
                        continue
                    if abs(data[time][sat][sys_type[sat[0]]]) < 5:
                        if sat[0] == "C" and sys_type[sat[0]] in data[time][sat].keys():
                            data_C[prn-1].append(data[time][sat][sys_type[sat[0]]])
                            time_C[prn-1].append(plot_time)
                        if sat[0] == "G" and sys_type[sat[0]] in data[time][sat].keys():
                            data_G[prn-1].append(data[time][sat][sys_type[sat[0]]])
                            time_G[prn-1].append(plot_time)
                        if sat[0] == "E" and sys_type[sat[0]] in data[time][sat].keys():
                            data_E[prn-1].append(data[time][sat][sys_type[sat[0]]])
                            time_E[prn-1].append(plot_time)
    if type == "TRP":
        for time in data.keys():
            plot_time = (time - cov_Time) / 3600
            if (plot_time > begT and plot_time < begT + LastT):
                for sat in data[time].keys():
                    prn = int(sat[1:3])
                    data_TRP.append(data[time][sat][sys_type[sat[0]]])
                    time_TRP.append(plot_time)
                    break

    if type == "ION":
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
        font_text = {'family' : 'Arial',
		'weight' : 500,
		'size'   : 15,
                }
        font2 = {"size":7}
        ax_range = axP[0].axis()
        axP[0].legend(G_L,prop=font2,
            framealpha=1,facecolor='w',ncol=2,numpoints=5, markerscale=2, 
            bbox_to_anchor=(1.01,1),loc=2,borderaxespad=0)
        axP[0].text(ax_range[0],ax_range[3],r'MEAN={:.4f}cm, RMS={:.4f}cm, STD={:.4f}cm'.format(np.mean(MEAN_G[0])*100, np.mean(RMS_G[0])*100, np.mean(STD_G[0])*100),font_text)
        axP[1].legend(E_L,prop=font2,
            framealpha=1,facecolor='w',ncol=2,numpoints=5, markerscale=2, 
            bbox_to_anchor=(1.01,1),loc=2,borderaxespad=0)
        axP[1].text(ax_range[0],ax_range[3],r'MEAN={:.4f}cm, RMS={:.4f}cm, STD={:.4f}cm'.format(np.mean(MEAN_E[0])*100, np.mean(RMS_E[0])*100, np.mean(STD_E[0])*100),font_text)
        axP[2].legend(C_L,prop=font2,
            framealpha=1,facecolor='w',ncol=2,numpoints=5, markerscale=2, 
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
            
        font2 = {"size":7}
        ax_range = axP.axis()
        axP.text(ax_range[0],ax_range[3],r'MEAN={:.4f}cm, RMS={:.4f}cm, STD={:.4f}cm'.format(np.mean(MEAN_G[0])*100, np.mean(RMS_G[0])*100, np.mean(STD_G[0])*100))
        axP.set_xticks(XTick)
        axP.set_xticklabels(XLabel)


    # figP.suptitle(mode)
    #plt.savefig(savedir)
    if show:
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
    
    figP,axP = plt.subplots(3,1,figsize=(23,15),sharey=False,sharex=True)
    
    axP[2].set_xlabel('Time:Hour of GPS Week(hour)')
    axP[0].set_ylabel(mode+'(Cycles)')
    axP[1].set_ylabel(mode+'(Cycles)')
    axP[2].set_ylabel(mode+'(Cycles)')
    axP[0].set_title('G-NL')
    axP[1].set_title('E-NL')
    axP[2].set_title('C-NL')
    axP[0].set_ylim(0.0,1) 
    axP[1].set_ylim(0.0,1) 
    axP[2].set_ylim(0.0,1) 

    for time in all_data:
        for sat in all_data[time]:
            prn = int(sat[1:3])
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
    colormap = sns.color_palette("colorblind",40)
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
            axP[0].scatter(time_G[i],data_G[i],s=2,marker='D',c = colormap[G_j])
            std_G.append(np.std(data_G[i]))
            prn = '%02d' % (i + 1)
            G_L.append('G'+prn)

        if E:
            axP[1].scatter(time_E[i],data_E[i],s=2,marker='D',c = colormap[E_j])
            prn = '%02d' % (i + 1)
            std_E.append(np.std(data_E[i]))
            E_L.append('E'+prn)

        if C:
            axP[2].scatter(time_C[i],data_C[i],s=2,marker='D',c = colormap[C_j])
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
    axS[0].set_ylim(0,0.1)
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

def plot_enu(data = {},type = ["E","N","U"],mode = ["DEFAULT"],ylim = 1,starttime = 0,deltaT = 2,begT = 0,LastT=24,time = "UTC",save='',show = False,Fixed = False,delta_data = 30):
    N_plot = len(type)
    N_mode = len(mode)
    f1=5
    ymin = -ylim
    ymax = ylim
    figP,axP = plt.subplots(N_plot,1,figsize=(20,10),sharey=False,sharex=True)
    axP[N_plot-1].set_xlabel('Time' + '(' + time + ')')
    font2 = {'family' : 'Arial',
		'weight' : 500,
		'size'   : 13,
            }
    for i in range(N_plot):
        axP[i].set_ylabel(type[i],font2)
        axP[i].grid(linestyle='--',linewidth=0.2, color='black',axis='both')
        if type[i] == "E" or type[i] == "N" or type[i] == "U":
            axP[i].set_ylim(ymin,ymax)
        if type[i] == "E":
            axP[i].set_title("Positioning Errors(m)",font)
        if type[i] == "NSAT":
            axP[i].set_title("Number of Satellite",font)
        if type[i] == "ION":
            axP[i].set_title("Difference of Ionosphere Delay correction/m",font)
            # axP[i].set_ylim(-0.5,0.5)
        if type[i] == "TRP":
            axP[i].set_title("Difference of Tropsphere Delay correction/m",font)
            axP[i].set_ylim(ymin,ymax)
        box = axP[i].get_position()
        if type[i] == "NSAT" or type[i] == "ION" or type[i] == "TRP":
            axP[i].set_position([box.x0, box.y0*1.04, box.width, box.height])
    
    if "+" in time:
        end_time = len(time)
        delta_Time = int(time[3:end_time]) + starttime
    else:
        delta_Time = starttime
    for time in data[mode[0]].keys():
        cov_Time = time - delta_Time * 3600
        break
    end_Time = begT + LastT
    delta_X = math.ceil((LastT)/deltaT)
    XLabel = []
    XTick = []
    starttime = begT - deltaT
    for i in range(delta_X):
        starttime = starttime + deltaT
        cur_Str_X = '%02d' % (starttime % 24) + ":00"
        XLabel.append(cur_Str_X)
        XTick.append(starttime)       
    if starttime < end_Time:
        starttime = starttime + deltaT
        cur_Str_X = '%02d' % (starttime % 24) + ":00"
        XLabel.append(cur_Str_X)
        XTick.append(starttime)


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
            if (plot_time >= begT and plot_time <= (begT + LastT)):
                if data[mode[i]][cur_time]["AMB"] == 0:
                    Float_NUM[i] = Float_NUM[i] + 1
                elif data[mode[i]][cur_time]["AMB"] == 1:
                    Fixed_NUM[i] = Fixed_NUM[i] + 1
                if (Fixed and data[mode[i]][cur_time]["AMB"] == 0):
                    continue
                time[i].append(plot_time)
                data_E[i].append(data[mode[i]][cur_time]["E"])
                data_N[i].append(data[mode[i]][cur_time]["N"])
                data_U[i].append(data[mode[i]][cur_time]["U"])
                data_S[i].append(data[mode[i]][cur_time]["NSAT"])
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

    data_plot["E"] = data_E
    data_plot["N"] = data_N
    data_plot["U"] = data_U
    data_plot["NSAT"] = data_S
    data_plot["TRP"] = data_TRP

    for i in range(N_plot):
        cur_type = type[i]
        RMS_enu[cur_type] = []
        STD_enu[cur_type] = []
        MEAN_enu[cur_type] = []
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
                    axP[i].scatter(time[j],data_plot[cur_type][j],s=1)
                    temp = dp.rms(data_plot[cur_type][j])
                    RMS_enu[cur_type].append(temp)
                    temp = np.std(data_plot[cur_type][j])
                    STD_enu[cur_type].append(temp)
                    temp = np.mean(data_plot[cur_type][j])
                    MEAN_enu[cur_type].append(temp)
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
    for i in range(N_plot):
        cur_type = type[i]
        RMS_str = "RMS:"
        for j in range(N_mode):
            if cur_type == "E" or cur_type == "N" or cur_type == "U":
                RMS_str = RMS_str +'{:.4f}m, '.format(RMS_enu[cur_type][j])
        if cur_type == "E" or cur_type == "N" or cur_type == "U":
            ax_range = axP[i].axis()
            axP[i].text(ax_range[0],ax_range[3],RMS_str[0:8*N_mode+8],font_text)


    axP[N_plot-1].set_xticks(XTick)
    axP[N_plot-1].set_xticklabels(XLabel)
    axP[0].legend(mode,prop=font2,
            framealpha=1,facecolor='w',ncol=1,numpoints=5, markerscale=5, 
            bbox_to_anchor=(1,1),loc=0,borderaxespad=0) 
    for i in range(N_plot):
        cur_type=type[i]
        if cur_type == "E" or cur_type == "N" or cur_type == "U":
            print("\n"+cur_type)
            for j in range(N_mode):
                print(mode[j] + ":")
                print('RMS={:.4f}cm,MEAN={:.4f}cm,STD={:.4f}cm'.format(RMS_enu[cur_type][j]*100,MEAN_enu[cur_type][j]*100,STD_enu[cur_type][j]*100))
    
    print("固定率(Fixed/Fixed+Float):")
    for i in range(N_mode):
        print(mode[i] + ':{:.2f}%'.format(Fixed_NUM[i] / (Fixed_NUM[i] + Float_NUM[i]) * 100))
    print("完整率:")
    for i in range(N_mode):
        print(mode[i] + ':{:.2f}%'.format((Fixed_NUM[i] + Float_NUM[i]) / ALL_NUM[i] * 100))
    print("固定率(Fixed/ALL):")
    for i in range(N_mode):
        print(mode[i] + ':{:.2f}%'.format(Fixed_NUM[i] / (ALL_NUM[i]) * 100))

    plt.show()

def plot_bias_grid(data = {},type = ["G","E","C"],mode = ["HKCL"],ylim = 1,starttime = 0,deltaT = 2,begT = 0,LastT=24,time = "UTC",save='',show = False,Fixed = False,delta_data = 30):
    N_plot = len(type)
    N_mode = len(mode)
    f1=5
    ymin = -ylim
    ymax = ylim
    figP,axP = plt.subplots(N_plot,1,figsize=(20,10),sharey=False,sharex=False)
    if (N_plot>3):
        axP[N_plot-2].set_xlabel('Time' + '(' + time + ')')
    else:
        axP[N_plot-1].set_xlabel('Time' + '(' + time + ')')
    font2 = {'family' : 'Arial',
		'weight' : 500,
		'size'   : 13,
            }
    for i in range(N_plot):
        axP[i].set_ylabel(type[i],font2)
        axP[i].grid(linestyle='--',linewidth=0.2, color='black',axis='both')
        # if type[i] == "G" or type[i] == "E" or type[i] == "C":
        #     axP[i].set_ylim(ymin,ymax)
        if type[i] == "G":
            axP[i].set_title("Difference of Bias(m)",font)
        box = axP[i].get_position()
        if type[i] == "G" or type[i] == "E" or type[i] == "C":
            axP[i].set_position([box.x0, box.y0, box.width*0.9, box.height])
        if type[i] == "RMS" or type[i] == "STD":
            axP[i].set_position([box.x0, box.y0*0.9, box.width, box.height])
    
    if "+" in time:
        end_time = len(time)
        delta_Time = int(time[3:end_time]) + starttime
    else:
        delta_Time = starttime
    for time in data.keys():
        cov_Time = time - delta_Time * 3600
        break
    end_Time = begT + LastT
    delta_X = math.ceil((LastT)/deltaT)
    XLabel = []
    XTick = []
    starttime = begT - deltaT
    for i in range(delta_X):
        starttime = starttime + deltaT
        cur_Str_X = '%02d' % (starttime % 24) + ":00"
        XLabel.append(cur_Str_X)
        XTick.append(starttime)       
    if starttime < end_Time:
        starttime = starttime + deltaT
        cur_Str_X = '%02d' % (starttime % 24) + ":00"
        XLabel.append(cur_Str_X)
        XTick.append(starttime)


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
                    if (cur_type != "RMS" and cur_type != "STD"):
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
    
    
    for i in range(N_plot):
        cur_type = type[i]
        if (cur_type != "RMS" and cur_type != "STD"):
            axP[i].set_xticks(XTick)
            axP[i].set_xticklabels(XLabel)
            axP[i].legend(site_ploted[cur_type],prop=font2,
                    framealpha=1,facecolor='w',ncol=2,numpoints=5, markerscale=5, 
                    bbox_to_anchor=(1,1),loc=0,borderaxespad=0) 
    if ("RMS" in type):
        last_plot = RMS_enu
    elif("STD" in type):
        last_plot = STD_enu
    W = 0.25
    
    for i in range(N_plot):
        cur_type = type[i]
        if (cur_type == "RMS" or cur_type == "STD"):  
            isys=-1         
            for sys in last_plot.keys():
                barplot_data = []
                barplot_name = []
                for site in last_plot[sys].keys():
                    barplot_data.append(last_plot[sys][site])
                    barplot_name.append(site)
                x = list(range(len(barplot_name)))

                for j in range(len(x)):
                    x[j] = x[j] + W*isys
                
                p1 = axP[i].bar(x,barplot_data,width = W)
                isys=isys+1

      
    for sys in last_plot.keys():
        barplot_data = []
        barplot_name = []
        for site in last_plot[sys].keys():
            barplot_name.append(site)
        break
    sys = ["G","E","C"]
    if ('RMS' in type or 'STD' in type):
        x = list(range(len(barplot_name)))
        axP[3].set_xticks(x)
        axP[3].set_xticklabels(barplot_name)
        axP[3].legend(sys)

    # print("固定率:")
    # for i in range(N_mode):
    #     print(mode[i] + ':{:.2f}%'.format(Fixed_NUM[i] / (Fixed_NUM[i] + Float_NUM[i]) * 100))
    # print("完整率:")
    # for i in range(N_mode):
    #     print(mode[i] + ':{:.2f}%'.format((Fixed_NUM[i] + Float_NUM[i]) / ALL_NUM[i] * 100))

    plt.show()