'''
Author: HanJunjie HanJunjie@whu.edu.cn
Date: 2022-07-16 14:31:10
LastEditors: HanJunjie HanJunjie@whu.edu.cn
LastEditTime: 2022-07-22 11:47:36
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
font_title = {'family' : 'Arial', 'weight' : 300, 'size' : 35}
font_label = {'family' : 'Arial', 'weight' : 300, 'size' : 32}
font_tick = {'family' : 'Arial', 'weight' : 300, 'size' : 35}
font_legend = {'family' : 'Arial', 'weight' : 300, 'size' : 20}
# font_legend = {'family' : 'Times New Roman', 'weight' : 600, 'size' : 15}
font_text = {'family' : 'Arial','weight' : 300,'size'   : 28}

xtick_size = 28
#path set
path_list = [#r"E:\1Master_2\Paper_Grid\Res_FromServer\ROTI\2021339\E0332021339_GEC.ismr",
# r"E:\1Master_2\Paper_Grid\Res_FromServer\ROTI\2021339\HKCL2021339_GEC.ismr",
# r"E:\1Master_2\Paper_Grid\Res_FromServer\ROTI\2021339\HKFN2021339_GEC.ismr",
r"E:\1Master_2\Paper_Grid\Res_FromServer\ROTI\2021339\HKKS2021339_GEC.ismr",
# r"E:\1Master_2\Paper_Grid\Res_FromServer\ROTI\2021339\HKKT2021339_GEC.ismr",
# r"E:\1Master_2\Paper_Grid\Res_FromServer\ROTI\2021339\HKLM2021339_GEC.ismr",
# r"E:\1Master_2\Paper_Grid\Res_FromServer\ROTI\2021339\HKLT2021339_GEC.ismr",
# r"E:\1Master_2\Paper_Grid\Res_FromServer\ROTI\2021339\HKMW2021339_GEC.ismr",
# r"E:\1Master_2\Paper_Grid\Res_FromServer\ROTI\2021339\HKNP2021339_GEC.ismr",
# r"E:\1Master_2\Paper_Grid\Res_FromServer\ROTI\2021339\HKOH2021339_GEC.ismr",
# r"E:\1Master_2\Paper_Grid\Res_FromServer\ROTI\2021339\HKPC2021339_GEC.ismr",
# r"E:\1Master_2\Paper_Grid\Res_FromServer\ROTI\2021339\HKSC2021339_GEC.ismr",
# r"E:\1Master_2\Paper_Grid\Res_FromServer\ROTI\2021339\HKSL2021339_GEC.ismr",
# r"E:\1Master_2\Paper_Grid\Res_FromServer\ROTI\2021339\HKSS2021339_GEC.ismr",
# r"E:\1Master_2\Paper_Grid\Res_FromServer\ROTI\2021339\HKST2021339_GEC.ismr",
# r"E:\1Master_2\Paper_Grid\Res_FromServer\ROTI\2021339\HKTK2021339_GEC.ismr",
# r"E:\1Master_2\Paper_Grid\Res_FromServer\ROTI\2021339\HKWS2021339_GEC.ismr",
# r"E:\1Master_2\Paper_Grid\Res_FromServer\ROTI\2021339\N0042021339_GEC.ismr",
# r"E:\1Master_2\Paper_Grid\Res_FromServer\ROTI\2021339\N0102021339_GEC.ismr",
# r"E:\1Master_2\Paper_Grid\Res_FromServer\ROTI\2021339\N0282021339_GEC.ismr",
# r"E:\1Master_2\Paper_Grid\Res_FromServer\ROTI\2021339\N0322021339_GEC.ismr",
# r"E:\1Master_2\Paper_Grid\Res_FromServer\ROTI\2021339\N0472021339_GEC.ismr",
# r"E:\1Master_2\Paper_Grid\Res_FromServer\ROTI\2021339\N0622021339_GEC.ismr",
# r"E:\1Master_2\Paper_Grid\Res_FromServer\ROTI\2021339\N0682021339_GEC.ismr",
# r"E:\1Master_2\Paper_Grid\Res_FromServer\ROTI\2021339\T4302021339_GEC.ismr",
# r"E:\1Master_2\Paper_Grid\Res_FromServer\ROTI\2021339\WHDS2021339_GEC.ismr",
# r"E:\1Master_2\Paper_Grid\Res_FromServer\ROTI\2021339\WHSP2021339_GEC.ismr",
# r"E:\1Master_2\Paper_Grid\Res_FromServer\ROTI\2021339\WHXZ2021339_GEC.ismr",
# r"E:\1Master_2\Paper_Grid\Res_FromServer\ROTI\2021339\WHYJ2021339_GEC.ismr",
# r"E:\1Master_2\Paper_Grid\Res_FromServer\ROTI\2021339\WUDA2021339_GEC.ismr",
r"E:\1Master_2\Paper_Grid\Res_FromServer\ROTI\2021339\XGXN2021339_GEC.ismr",]
# path_list = [r"E:\1Master_2\Paper_Grid\Pro_20211205-339\roti\WHYJ2021339_GEC.ismr"]
path_list = [r"E:\1Master_2\Paper_Grid\Res_FromServer_New\ROTI\2021305\HKSC2021305_GEC.ismr"]
site_list = ["HKKS","HKKT","HKSS","HKWS","HKSL","HKST","HKKS","HKCL","HKSC","HKPC","HKNP","HKMW","HKLM","HKOH"]
# site_list = ["HKSC"]
# site_list = ["TERS","IJMU","DELF","VLIS","DENT","WSRT","KOS1","BRUX","DOUR","WARE","REDU","EIJS","TIT2","EUSK","DILL","DIEP","BADH","KLOP","FFMJ","KARL","HOBU","PTBB","GOET"]
# sitestring = "TRO1 VARS HETT OVE6 ROM2 OST6 OLK2 PYHA LEK6 METG LOV6 IRBE NOR7 SPT7 VAIN HAS6 RANT REDZ LAMA HELG GELL LDB2 GOML GOET BRTS LEIJ WARE INVR ARIS TLL1 SNEO WTZZ AUBG BUTE BACA MIKL POLV COMO EGLT SWAS MARS ZADA AJAC SCOA ACOR ALME MMET ORID IZMI NICO SAVU SUN6 MNSK TER2 SMLA IJMU DYNG DEVA MALL MAH1 LODZ ZYWI AUTN ENTZ VILL"
# site_list = sitestring.split()
# site_list = ["TERS","IJMU","DELF","VLIS","DENT","WSRT","KOS1","BRUX","DOUR","WARE","REDU","EIJS","TIT2","EUSK","DILL","DIEP","BADH","KLOP","FFMJ","KARL","HOBU","PTBB","GOET"]
count = 1
Year,Mon,Day,Hour,LastT,deltaT = 2021,11,1,6,12,1
while count > 0:
    doy = tr.ymd2doy(Year,Mon,Day,0,00,00)
    cdoy = "{:0>3}".format(doy)
    for i in range(len(site_list)):
        cur_site = site_list[i]
        
        path_roti = r"E:\1Master_2\3-IUGG\Result_Server\ROTI" + "\\" +"{:0>4}".format(Year) + cdoy+"\\"+ cur_site + "{:0>4}".format(Year) + cdoy + "_GEC.ismr"
        save_dir = r"E:\1Master_2\3-IUGG\Result_Server\ROTI\Fig" + "\\" + "{:0>4}".format(Year) + cdoy
        path_roti = r"E:\1Master_2\Paper_Grid\Res_FromServer_New\ROTI-30\2021305"+"\\"+ cur_site + "{:0>4}".format(Year) + cdoy + "_GEC.ismr"
        if (not os.path.exists(save_dir)):
            os.mkdir(save_dir)
        # path_roti = r"D:\GREAT\GREAT_Project\Allystar\ROTI_20220722\30s\DGCA2022203_GEC.ismr"
        # path_roti = r"D:\GREAT\GREAT_Project\Allystar\ROTI_20220722\30s\SWHF2022203_GEC.ismr"

        figP,axP = plt.subplots(3,1,figsize=(8,10),sharey=False,sharex=True)
        #Time
        time="UTC"
        t=time
        starttime=8
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
        secow_start = tr.ymd2gpst(Year,Mon,Day,starttime,00,00)
        cov_Time = secow_start[1] - delta_Time * 3600
        end_Time = begT + LastT
        delta_X = math.ceil((LastT)/deltaT)
        XLabel = []
        XTick = []
        starttime = begT - deltaT
        for i in range(delta_X):
            starttime = starttime + deltaT
            cur_Str_X = '%02d' % (starttime % 24)
            XLabel.append(cur_Str_X)
            XTick.append(int(starttime))       
        while starttime < math.ceil(end_Time):
            starttime = starttime + deltaT
            cur_Str_X = '%02d' % (starttime % 24)
            XLabel.append(cur_Str_X)
            XTick.append(int(starttime))

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
        for time in data.keys():
            plot_time = (time - cov_Time) / 3600
            if (plot_time > begT and plot_time < begT + LastT) or all:
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
                    # if sat == "G03":
                    #     data_G[prn-1].append(data[time][sat])
                    #     time_G[prn-1].append(plot_time)
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
            #!!!
            # E=False
            if G:
                # axP.scatter(time_G[i],data_G[i],s=1,color=colormap[i])
                axP[0].scatter(time_G[i], data_G[i], s=1)
            if E:
                # axP.scatter(time_E[i],data_E[i],s=1,color=colormap[i])
                axP[1].scatter(time_E[i], data_E[i], s=1)
            if C:
                # axP.scatter(time_C[i],data_C[i],s=1,color=colormap[i])
                axP[2].scatter(time_C[i], data_C[i], s=1)

        # font2 = {'family' : 'Arial',
        #             'weight' : 600,
        #             'size'   : 25,
        #                 }
        font3 = { 'weight' : 500,
                'size'   : 15, }

        axP[2].set_xlabel("Time("+t+')',font_label)
        axP[1].set_ylabel("ROTI(TECU/min)",font_label)

        axP[0].set_title('GPS',font_label)
        axP[1].set_title('GAL',font_label)
        axP[2].set_title('BDS',font_label)

        axP[0].set_xticks(XTick)
        axP[1].set_xticks(XTick)
        axP[2].set_xticks(XTick)
        axP[2].set_xticklabels(XLabel)

        axP[0].tick_params(axis='both', colors='black', direction='in', labelsize=15, width=1, length=3, pad=5)
        axP[1].tick_params(axis='both', colors='black', direction='in', labelsize=15, width=1, length=3, pad=5)
        axP[2].tick_params(axis='both', colors='black', direction='in', labelsize=15, width=1, length=3, pad=5)

        axP[0].set_ylim(0,1)
        axP[1].set_ylim(0,1)
        axP[2].set_ylim(0,1)

        axP[0].grid(False)
        axP[1].grid(False)
        axP[2].grid(False)

        labels = axP[0].get_yticklabels() + axP[1].get_yticklabels() + axP[2].get_yticklabels() + axP[2].get_xticklabels()
        [label.set_fontsize(xtick_size) for label in labels]
        [label.set_fontname('Arial') for label in labels]

        # plt.savefig(save_dir+"\\"+cur_site+'.png')
        plt.show()
    Day = Day + 1
    count = count - 1
    if (Day > 31):
        Day = 1
        Mon = Mon + 1