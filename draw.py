'''
Author: Junjie Han
Date: 2021-09-23 10:14:18
LastEditTime: 2021-11-10 17:12:54
LastEditors: Please set LastEditors
Description: In User Settings Edit
FilePath: /plot-toolkit-master/jjHan_py_plot/draw.py
'''

import numpy as np
import matplotlib as mpl
mpl.use("TkAgg")
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from numpy.core.fromnumeric import shape, size
import dataprocess as dp
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
        ymin = -0.2
        ymax = 0.2
        col = 2
    elif mode == 'ion':
        f1=4
        ymin = -0.1
        ymax = 0.1
        col = 1
        figP,axP = plt.subplots(3,1,figsize=(20,10),sharey=True,sharex=True)
    elif mode == 'trp':
        f1=6
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

def plot_tec_GREC(all_data = {},savedir='save_fig_path',station = 'hjj',show = False):
    RMS_G,MEAN_G,STD_G = [[],[]],[[],[]],[[],[]]
    RMS_E,MEAN_E,STD_E = [[],[]],[[],[]],[[],[]]
    RMS_C,MEAN_C,STD_C = [[],[]],[[],[]],[[],[]]
    RMS_R,MEAN_R,STD_R = [[],[]],[[],[]],[[],[]]
    G_L,E_L,C_L,R_L = [],[],[],[]
    figP,axP = plt.subplots(2,2,figsize=(20,10),sharey=False,sharex=True)
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
    plt.savefig(savedir)
    if show:
        plt.show()