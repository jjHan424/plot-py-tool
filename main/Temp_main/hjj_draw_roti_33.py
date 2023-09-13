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
plt.style.use(['science','no-latex'])
import dataprocess as dp
import draw as dr
import seaborn as sns
import trans as tr
import seaborn as sns

font_title = {'family' : 'Arial', 'weight' : 300, 'size' : 20}
font_label = {'family' : 'Arial', 'weight' : 300, 'size' : 20}
font_tick = {'family' : 'Arial', 'weight' : 300, 'size' : 20}
font_legend = {'family' : 'Arial', 'weight' : 300, 'size' : 20}
# font_legend = {'family' : 'Times New Roman', 'weight' : 600, 'size' : 15}
font_text = {'family' : 'Arial','weight' : 300,'size'   : 20}
xtick_size = 16
color_list = sns.color_palette("Set1")

site_list = ["HKSC"]
count = 1
# Year,Mon,Day,Hour,LastT,deltaT = 2021,11,1,5,16,4
Year,Mon,Day,Hour,LastT,deltaT = 2021,11,1,3,21,4
time="UTC"

plot_type = "ALL"

while count > 0:
   
    doy = tr.ymd2doy(Year,Mon,Day,0,00,00)
    cdoy = "{:0>3}".format(doy)
    for i in range(len(site_list)):
        cur_site = site_list[i]
        
        # path_roti = r"E:\1Master_2\Paper_Grid\Res_FromServer_New\ROTI" + "\\" +"{:0>4}".format(Year) + cdoy+"\\"+ cur_site + "{:0>4}".format(Year) + cdoy + "_GEC.ismr"
        # save_dir = r"E:\1Master_2\Paper_Grid\Res_FromServer_New\Fig\ROTI-30" + "\\" + "{:0>4}".format(Year) + cdoy
        # diff_dir = r"E:\1Master_2\Paper_Grid\Res_FromServer_New\Diff-New" + "\\" + "{:0>4}{:0>3}".format(Year,doy) + "\\" + cur_site + "-GEC-5.diff"
        # # path_roti = r"G:\Data\Res\ROTI" + "\\" +"{:0>4}".format(Year) + cdoy+"\\"+ cur_site + "{:0>4}".format(Year) + cdoy + "_GEC.ismr"
        # # save_dir = r"G:\Data\Res\ROTI-30" + "\\" + "{:0>4}".format(Year) + cdoy
        # # diff_dir = r"G:\Data\Res\Diff-New" + "\\" + "{:0>4}{:0>3}".format(Year,doy) + "\\" + cur_site + "-GEC-5.diff"
        # [Diff_Head,Diff_Data] = rf.open_aug_file_new(diff_dir)
        # if (not os.path.exists(save_dir)):
        #     os.mkdir(save_dir)
        # # path_roti = r"D:\GREAT\GREAT_Project\Allystar\ROTI_20220722\30s\DGCA2022203_GEC.ismr"
        # # path_roti = r"D:\GREAT\GREAT_Project\Allystar\ROTI_20220722\30s\SWHF2022203_GEC.ismr"

        # figP,axP = plt.subplots(2,3,figsize=(12,8),sharey=False,sharex=True)
        # # figP,axP = plt.subplots(1,3,figsize=(11,5),sharey=False,sharex=True)
        # #Time
        
        # t=time
        # all=False
        # colormap = sns.color_palette(['xkcd:green','xkcd:blue','xkcd:red', 'xkcd:brown', 'xkcd:pink', 'xkcd:purple'],100)
        # ###-------------Time Set in Plot--------------##
        [XLabel,XTick,cov_Time,begT,LastT]=dr.xtick(time,Year,Mon,Day,Hour,LastT,deltaT)

        ##mean_max_roti###
        path_roti = r"E:\1Master_2\Paper_Grid\Res_FromServer_New\ROTI" + "\\" +"{:0>4}".format(Year) + cdoy+"\\"+ cur_site + "{:0>4}".format(Year) + cdoy + "_GEC.ismr"
        ###-------------ROTI-------------###
        data = rf.open_ismr(path_roti)
        # print(data)
        time_G = [[] for i in range(100)]
        time_R = [[] for i in range(100)]
        time_E = [[] for i in range(100)]
        time_C = [[] for i in range(100)]
        time_TRP = []
        data_G = [[] for i in range(100)]
        data_R = [[] for i in range(100)]
        data_E = [[] for i in range(100)]
        data_C = [[] for i in range(100)]
        mean_G,mean_E,mean_C=[],[],[]
        min_G,min_E,min_C=[],[],[]
        meanT_G,meanT_E,meanT_C=[],[],[]
        All_G,All_E,All_C=[],[],[]
        Num_G,Num_E,Num_C=[],[],[]
        for time in data.keys():
            plot_time = (time - cov_Time) / 3600
            # if time not in Diff_Data.keys():
            #     continue
            if (plot_time > begT and plot_time < begT + LastT) or all:
                temp_mean_G,temp_mean_E,temp_mean_C=[],[],[]
                # if time not in Diff_Data.keys():
                #         continue
                for sat in data[time].keys():
                    # if sat not in Diff_Data[time].keys():
                    #     continue
                    if data[time][sat] == 0:
                        continue
                    prn = int(sat[1:3])
                    if sat[0] == "C":
                        if prn < 6:
                            continue
                        data_C[prn-1].append(data[time][sat])
                        temp_mean_C.append(data[time][sat])
                        time_C[prn-1].append(plot_time)
                    if sat[0] == "G":
                        data_G[prn-1].append(data[time][sat])
                        temp_mean_G.append(data[time][sat])
                        time_G[prn-1].append(plot_time)
                    if sat[0] == "E":
                        data_E[prn-1].append(data[time][sat])
                        temp_mean_E.append(data[time][sat])
                        time_E[prn-1].append(plot_time)
                tempNum=0
                if len(temp_mean_G)>3:
                    mean_temp = np.mean(temp_mean_G)
                    if mean_temp > 6:
                        continue
                    mean_G.append(mean_temp)
                    min_G.append(np.min(temp_mean_G))
                    meanT_G.append(plot_time)
                    All_G.append(len(temp_mean_G))
                    for iii in range(len(temp_mean_G)):
                        if temp_mean_G[iii] > mean_temp:
                            tempNum = tempNum + 1
                    Num_G.append(tempNum)
                else:
                    mean_G.append(0)
                    min_G.append(0)
                    meanT_G.append(plot_time)
                    All_G.append(len(temp_mean_G))
                    Num_G.append(len(temp_mean_G))
                tempNum=0
                if len(temp_mean_E)>3:
                    mean_temp = np.mean(temp_mean_E)
                    if mean_temp > 6:
                        continue
                    mean_E.append(mean_temp)
                    min_E.append(np.min(temp_mean_E))
                    meanT_E.append(plot_time)
                    All_E.append(len(temp_mean_E))
                    for iii in range(len(temp_mean_E)):
                        if temp_mean_E[iii] > mean_temp:
                            tempNum = tempNum + 1
                    Num_E.append(tempNum)
                else:
                    mean_E.append(0)
                    min_E.append(0)
                    meanT_E.append(plot_time)
                    All_E.append(len(temp_mean_E))
                    Num_E.append(len(temp_mean_E))
                tempNum=0
                if len(temp_mean_C)>3:
                    mean_temp = np.mean(temp_mean_C)
                    if mean_temp > 6:
                        continue
                    mean_C.append(mean_temp)
                    min_C.append(np.min(temp_mean_C))
                    meanT_C.append(plot_time)
                    All_C.append(len(temp_mean_C))
                    for iii in range(len(temp_mean_C)):
                        if temp_mean_C[iii] > mean_temp:
                            tempNum = tempNum + 1
                    Num_C.append(tempNum)
                else:
                    mean_C.append(0)
                    min_C.append(0)
                    meanT_C.append(plot_time)
                    All_C.append(len(temp_mean_C))
                    Num_C.append(len(temp_mean_C))
                # if (np.mean(temp_mean_E)>9):
                #     print("hjj")
                    # if sat == "G03":
                    #     data_G[prn-1].append(data[time][sat])
                    #     time_G[prn-1].append(plot_time)
        if plot_type == "MEAN":
            axP[1][0].scatter(meanT_G, mean_G,s=1)
            axP[1][1].scatter(meanT_E, mean_E,s=1)
            axP[1][2].scatter(meanT_C, mean_C,s=1)
            axP[1][0].set_ylim(0, 2)
            axP[1][1].set_ylim(0, 2)
            axP[1][2].set_ylim(0, 2)
        
        print("GPS:{:.4f}".format(np.max(np.array(mean_G))))
        print("GAL:{:.4f}".format(np.max(np.array(mean_E))))
        print("BDS:{:.4f}".format(np.max(np.array(mean_C))))
        figP,axP = plt.subplots(3,1,figsize=(11,5),sharey=False,sharex=True)
        axP[0].scatter(meanT_G, mean_G,s=1)
        axP[1].scatter(meanT_E, mean_E,s=1)
        axP[2].scatter(meanT_C, mean_C,s=1)
        axP[2].set_xticks(XTick)
        axP[2].set_xticklabels(XLabel)
        plt.show()

        # axP[0][0].plot(meanT_G, All_G,color = color_list[0])
        # axP[0][1].plot(meanT_E, All_E,color = color_list[0])
        # axP[0][2].plot(meanT_C, All_C,color = color_list[0])

        # axP[0][0].plot(meanT_G, Num_G,color = color_list[1])
        # axP[0][1].plot(meanT_E, Num_E,color = color_list[1])
        # axP[0][2].plot(meanT_C, Num_C,color = color_list[1])
        #----------------------------#

        # axP[0].plot(meanT_G, All_G,color = color_list[0])
        # axP[1].plot(meanT_E, All_E,color = color_list[0])
        # axP[2].plot(meanT_C, All_C,color = color_list[0])

        # axP[0].plot(meanT_G, Num_G,color = color_list[1])
        # axP[1].plot(meanT_E, Num_E,color = color_list[1])
        # axP[2].plot(meanT_C, Num_C,color = color_list[1])

        # axP[2].legend(["All","Scintillating"],prop=font_legend,
        # framealpha=0,facecolor='none',ncol=2,numpoints=5,markerscale=10,
        #             borderaxespad=0,bbox_to_anchor=(1,1.3),loc=1)
        # leg = axP[2].get_legend()
        # for legobj in leg.legendHandles:
        #     legobj.set_linewidth(5)
        # axP[0].set_xticks(XTick)
        # axP[0].set_xticklabels(XLabel)
        # labels = axP[0].get_xticklabels() + axP[1].get_xticklabels() + axP[2].get_xticklabels() + axP[0].get_yticklabels() + axP[1].get_yticklabels() + axP[2].get_yticklabels()
        # [label.set_fontsize(xtick_size) for label in labels]
        # labels = axP[0].get_xticklabels() + axP[1].get_xticklabels() + axP[2].get_xticklabels()
        # [label.set_rotation(30) for label in labels]
        
        # axP[0].set_ylabel("Num of sat",font_label)
        # axP[1].set_xlabel("Time (UTC)",font_label)
        # box = axP[0].get_position()
        # axP[0].set_position([box.x0,box.y0 + box.y0*1, box.width, box.height*0.8])
        # box = axP[1].get_position()
        # axP[1].set_position([box.x0,box.y0 + box.y0*1, box.width, box.height*0.8])
        # box = axP[2].get_position()
        # axP[2].set_position([box.x0,box.y0 + box.y0*1, box.width, box.height*0.8])
        # axP[0].set_title("GPS",font_title)
        # axP[1].set_title("GAL",font_title)
        # axP[2].set_title("BDS",font_title)

        #----------------------------#
        if plot_type == "ALL":
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
                    # axP.scatter(time_G[i],data_G[i],s=1,color=colormap[i])
                    axP[0][0].scatter(time_G[i], data_G[i], s=1,color = color_list[i%9])
                if E:
                    # axP.scatter(time_E[i],data_E[i],s=1,color=colormap[i])
                    axP[0][1].scatter(time_E[i], data_E[i], s=1,color = color_list[i%9])
                if C:
                    # axP.scatter(time_C[i],data_C[i],s=1,color=colormap[i])
                    axP[0][2].scatter(time_C[i], data_C[i], s=1,color = color_list[i%9])

        # font2 = {'family' : 'Arial',
        #             'weight' : 600,
        #             'size'   : 25,
        #                 }
        font3 = { 'weight' : 500,
                'size'   : 15, }

        # axP[2].set_xlabel("Time("+t+')',font3)
        # axP[1].set_ylabel("ROTI(TECU/min)",font3)

        # axP[0].set_title('G',font3)
        # axP[1].set_title('E',font3)
        # axP[2].set_title('C',font3)

        axP[1][0].set_xticks(XTick)
        # axP[2][0].set_xticks(XTick)
        # axP[2][0].set_xticks(XTick)
        # axP[1].set_xticks(XTick)
        # axP[2].set_xticks(XTick)
        axP[1][0].set_xticklabels(XLabel)

        # axP[0].tick_params(axis='both', colors='black', direction='in', labelsize=15, width=1, length=3, pad=5)
        # axP[1].tick_params(axis='both', colors='black', direction='in', labelsize=15, width=1, length=3, pad=5)
        # axP[2].tick_params(axis='both', colors='black', direction='in', labelsize=15, width=1, length=3, pad=5)

        axP[0][0].set_ylim(0,6)
        axP[0][1].set_ylim(0,6)
        axP[0][2].set_ylim(0,6)

        # axP[0].grid(False)
        # axP[1].grid(False)
        # axP[2].grid(False)

        # plt.savefig(save_dir+"\\"+cur_site+'.png')

        time_G = [[] for i in range(100)]
        time_R = [[] for i in range(100)]
        time_E = [[] for i in range(100)]
        time_C = [[] for i in range(100)]
        time_TRP = []
        data_G = [[] for i in range(100)]
        data_R = [[] for i in range(100)]
        data_E = [[] for i in range(100)]
        data_C = [[] for i in range(100)]
        mean_G,mean_E,mean_C=[],[],[]
        min_G,min_E,min_C=[],[],[]
        meanT_G,meanT_E,meanT_C=[],[],[]
        All_G,All_E,All_C=[],[],[]
        Num_G,Num_E,Num_C=[],[],[]
        for time in Diff_Data.keys():
            plot_time = (time - cov_Time) / 3600
            if (plot_time > begT and plot_time < begT + LastT) or all:
                temp_mean_G,temp_mean_E,temp_mean_C=[],[],[]
                for sat in Diff_Data[time].keys():
                    prn = int(sat[1:3])
                    if sat[0] == "C":
                        data_C[prn-1].append(abs(Diff_Data[time][sat]["dION2"]))
                        temp_mean_C.append(abs(Diff_Data[time][sat]["dION2"]))
                        time_C[prn-1].append(plot_time)
                    if sat[0] == "G":
                        data_G[prn-1].append(abs(Diff_Data[time][sat]["dION1"]))
                        temp_mean_G.append(abs(Diff_Data[time][sat]["dION1"]))
                        time_G[prn-1].append(plot_time)
                    if sat[0] == "E":
                        data_E[prn-1].append(abs(Diff_Data[time][sat]["dION1"]))
                        temp_mean_E.append(abs(Diff_Data[time][sat]["dION1"]))
                        time_E[prn-1].append(plot_time)
                tempNum=0
                if len(temp_mean_G)>0:
                    mean_temp = np.mean(temp_mean_G)
                    mean_G.append(mean_temp)
                    min_G.append(np.min(temp_mean_G))
                    meanT_G.append(plot_time)
                    All_G.append(len(temp_mean_G))
                    for iii in range(len(temp_mean_G)):
                        if temp_mean_G[iii] > mean_temp:
                            tempNum = tempNum + 1
                    Num_G.append(tempNum)
                else:
                    mean_G.append(0)
                    min_G.append(0)
                    meanT_G.append(plot_time)
                    All_G.append(len(temp_mean_G))
                    Num_G.append(len(temp_mean_G))
                tempNum=0
                if len(temp_mean_E)>0:
                    mean_temp = np.mean(temp_mean_E)
                    mean_E.append(mean_temp)
                    min_E.append(np.min(temp_mean_E))
                    meanT_E.append(plot_time)
                    All_E.append(len(temp_mean_E))
                    for iii in range(len(temp_mean_E)):
                        if temp_mean_E[iii] > mean_temp:
                            tempNum = tempNum + 1
                    Num_E.append(tempNum)
                else:
                    mean_E.append(0)
                    min_E.append(0)
                    meanT_E.append(plot_time)
                    All_E.append(len(temp_mean_E))
                    Num_E.append(len(temp_mean_E))
                tempNum=0
                if len(temp_mean_C)>0:
                    mean_temp = np.mean(temp_mean_C)
                    mean_C.append(mean_temp)
                    min_C.append(np.min(temp_mean_C))
                    meanT_C.append(plot_time)
                    All_C.append(len(temp_mean_C))
                    for iii in range(len(temp_mean_C)):
                        if temp_mean_C[iii] > mean_temp:
                            tempNum = tempNum + 1
                    Num_C.append(tempNum)
                else:
                    mean_C.append(0)
                    min_C.append(0)
                    meanT_C.append(plot_time)
                    All_C.append(len(temp_mean_C))
                    Num_C.append(len(temp_mean_C))
        if plot_type == "MEAN" :
            axP[2][0].scatter(meanT_G, mean_G,s=1)
            axP[2][1].scatter(meanT_E, mean_E,s=1)
            axP[2][2].scatter(meanT_C, mean_C,s=1)
        if plot_type == "ALL":
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
                    # axP.scatter(time_G[i],data_G[i],s=1,color=colormap[i])
                    axP[1][0].scatter(time_G[i], data_G[i], s=1,color = color_list[i%9])
                if E:
                    # axP.scatter(time_E[i],data_E[i],s=1,color=colormap[i])
                    axP[1][1].scatter(time_E[i], data_E[i], s=1,color = color_list[i%9])
                if C:
                    # axP.scatter(time_C[i],data_C[i],s=1,color=colormap[i])
                    axP[1][2].scatter(time_C[i], data_C[i], s=1,color = color_list[i%9])
        
        axP[1][0].set_xticks(XTick)
        axP[1][0].set_xticklabels(XLabel)
        labels = axP[1][0].get_xticklabels() + axP[1][1].get_xticklabels() + axP[1][2].get_xticklabels()
        [label.set_fontsize(xtick_size) for label in labels]
        [label.set_rotation(30) for label in labels]
        font = {'family': 'Times new roman','weight': 600,'size': 20}
        axP[1][1].set_xlabel("Time(UTC)",font_label)
        axP[1][0].set_ylim(0,0.6)
        axP[1][1].set_ylim(0,0.6)
        axP[1][2].set_ylim(0,0.6)
        y_labels = axP[0][0].get_yticklabels() + axP[1][0].get_yticklabels() + axP[0][1].get_yticklabels() + axP[1][1].get_yticklabels() + axP[0][2].get_yticklabels() + axP[1][2].get_yticklabels()
        [label.set_fontsize(xtick_size) for label in y_labels]
        # axP[0][0].set_ylabel("Num of sat",font_label)
        axP[0][0].set_ylabel("ROTI(TECU/min)",font_label)
        axP[1][0].set_ylabel("IONO errors(m)",font_label)
        font = {'family': 'Times new roman','weight': 600,'size': 23}
        axP[0][0].set_title("GPS",font_title)
        axP[0][1].set_title("GAL",font_title)
        axP[0][2].set_title("BDS",font_title)

        box = axP[0][1].get_position()
        axP[0][1].set_position([box.x0,box.y0 + box.y0*0.08, box.width, box.height])
        box = axP[0][0].get_position()
        axP[0][0].set_position([box.x0,box.y0 + box.y0*0.08, box.width, box.height])
        box = axP[0][2].get_position()
        axP[0][2].set_position([box.x0,box.y0 + box.y0*0.08, box.width, box.height])

        box = axP[1][1].get_position()
        axP[1][1].set_position([box.x0,box.y0 + box.y0*0.5, box.width, box.height])
        box = axP[1][0].get_position()
        axP[1][0].set_position([box.x0,box.y0 + box.y0*0.5, box.width, box.height])
        box = axP[1][2].get_position()
        axP[1][2].set_position([box.x0,box.y0 + box.y0*0.5, box.width, box.height])

        # plt.savefig(r"E:\1Master_2\Paper_Grid\1-Paper_word\Image-3\HKMW-ROTI-ROTI-New.png",dpi=600)
        # plt.savefig(r"E:\1Master_2\Paper_Grid\1-Paper_word\Image-3\HKMW-ROTI-ROTI.svg")
        plt.show()
        Day = Day + 1
        count = count - 1
        if (Day > 31):
            Day = 1
            Mon = Mon + 1