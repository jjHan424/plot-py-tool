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
import seaborn as sns
font_title = {'family' : 'Arial', 'weight' : 300, 'size' : 25}
font_label = {'family' : 'Arial', 'weight' : 300, 'size' : 25}
font_tick = {'family' : 'Arial', 'weight' : 300, 'size' : 25}
font_legend = {'family' : 'Arial', 'weight' : 300, 'size' : 25}
# font_legend = {'family' : 'Times New Roman', 'weight' : 600, 'size' : 15}
font_text = {'family' : 'Arial','weight' : 300,'size'   : 20}
xtick_size = 25
color_list = sns.color_palette("Set1")
color_list = ["#0085c3","#7ab800","#71c6c1","#dc5034","#009bbb",
              "#b7295a","#6e2585","#f2af00","#5482ab","#ce1126",
              "#444444","#eeeeee"]
# color_list = ["#ffcc2f","#00acee","#2baf2b","#ef5734","#cecece","#543729"]

site_list = ["HKLT"]
count = 1
# Year,Mon,Day,Hour,LastT,deltaT = 2021,11,1,5,16,4
Year,Mon,Day,Hour,LastT,deltaT = 2021,10,6,8,16,4
cur_site = site_list[0]
[XLabel,XTick,cov_Time,begT,LastT]=dr.xtick("GPST",Year,Mon,Day,Hour,LastT,deltaT)
doy = tr.ymd2doy(Year,Mon,Day,0,00,00)
cdoy = "{:0>3}".format(doy)
path_roti = os.path.join("/Users/hanjunjie/Master_3/1-IUGG/ResFromServer/ROTI", cur_site + "{:0>4}".format(Year) + cdoy + "_GEC.ismr")
path_diff = "/Users/hanjunjie/Master_3/1-IUGG/ResFromServer/Diff_Static_5S/2021279/HKLT-GEC2-5.diff"
[head_res,data_diff] = rf.open_aug_file_new(path_diff)
data = rf.open_ismr(path_roti)
data_plot,time_plot = {"Scintillating":{},"All":{}},{"Scintillating":{},"All":{}}
for cur_time in data_diff.keys():
    if cur_time not in data.keys():
        continue
    plot_time = (cur_time - cov_Time) / 3600
        # if time not in Diff_Data.keys():
        #     continue
    if (plot_time > begT and plot_time < begT + LastT):
        Numberall,NumberScin = {"G":0,"E":0,"C":0},{"G":0,"E":0,"C":0}
        for cur_sat in data_diff[cur_time].keys():
            if cur_sat not in data[cur_time].keys():
                continue
            if data_diff[cur_time][cur_sat]["dION1"] == 0.0:
                continue
            if cur_sat not in data_plot["All"].keys():
                data_plot["All"][cur_sat],data_plot["Scintillating"][cur_sat] = [],[]
                time_plot["All"][cur_sat],time_plot["Scintillating"][cur_sat] = [],[]
            Numberall[cur_sat[0]] = Numberall[cur_sat[0]] + 1
            if cur_sat in data_diff[cur_time].keys():
                data_plot["All"][cur_sat].append(data_diff[cur_time][cur_sat]["dION1"]*100)
                time_plot["All"][cur_sat].append(plot_time)
            # data_plot["All"][cur_sat].append(data_diff[cur_time][cur_sat]["dION1"]*100)
            data_plot["Scintillating"][cur_sat].append(data[cur_time][cur_sat])
            # time_plot["All"][cur_sat].append(plot_time)
            time_plot["Scintillating"][cur_sat].append(plot_time)
figP,axP = plt.subplots(2,3,figsize=(12,8),sharey=False,sharex=True)
# axP[1].set_xlabel('Time' + ' (' + time + ')',font_label)
# for i in range(3):  
axP[1][1].set_xlabel("GPS time (hour)",font_label)

for i in range(2):
    for j in range(3):
        if i == 0:
            axP[i][j].set_ylim(0,1)
        if i == 1:
            axP[i][j].set_ylim(0,40)
            axP[i][j].set_yticks([0,10,20,30,40])
        if j > 0:
            axP[i][j].set_yticklabels([])
axP[0][0].set_ylabel('ROTI (TECU/min)',font_label)
axP[1][0].set_ylabel('IONO errors (cm)',font_label)
# axP[1].yaxis.set_label_coords(-0.1,0.5)
axP[0][0].set_title('GPS',font_title)
axP[0][1].set_title('GAL',font_title)
axP[0][2].set_title('BDS',font_title)
# for i in range(3):
    # axP[i].grid(linestyle='--',linewidth=0.2, color='black',axis='both')
    # axP[i].set_ylim(0,15)
    # box = axP[i].get_position()
    # axP[i].set_position([box.x0, box.y0 + box.height*0.15, box.width, box.height*0.8])
sys_axP = {"G":0,"E":1,"C":2}
mode_axP = {"All":1,"Scintillating":0}

for cur_mode in data_plot.keys():
    sys_color = {"G":-1,"E":-1,"C":-1}
    for cur_sat in data_plot[cur_mode].keys():
        sys_color[cur_sat[0]] = sys_color[cur_sat[0]] + 1
        axP[mode_axP[cur_mode]][sys_axP[cur_sat[0]]].scatter(time_plot[cur_mode][cur_sat],data_plot[cur_mode][cur_sat],s=1,color = color_list[sys_color[cur_sat[0]]%12])
# xxx = axP[0].axvspan(ymin = 0,ymax = 1,xmin = min_sun,xmax = max_sun,alpha = 0.3,color = "gray")
# L1 = plt.legend([xxx],["Scintillating"],prop=font_legend,
#         framealpha=0,facecolor='white',ncol=4,numpoints=5,markerscale=4,frameon = True, 
#         borderaxespad=0,bbox_to_anchor=(1,1),loc=1)
# plt.gca().add_artist(L1)
# axP[1][2].legend(["Scintillating"],prop=font_legend,
#         framealpha=1,facecolor='w',numpoints=5, markerscale=3, frameon=False,
#         loc=0,borderaxespad=0)
        # color = color_list[sys_color[cur_sat[0]]%11]
        # axP[sys_axP[cur_sys]].plot(time_plot[cur_mode][cur_sys],data_plot[cur_mode][cur_sys],color = color_list[j%3])
# axP[1].legend(["Scintillating","All"],prop=font_legend,
#         framealpha=1,facecolor='w',numpoints=5, markerscale=3, frameon=False,
#         loc=0,borderaxespad=0)
# leg = axP[1].get_legend()
# for legobj in leg.legendHandles:
#     legobj.set_linewidth(3)
axP[1][2].set_xticks(XTick)
axP[1][1].set_xticks(XTick)
axP[1][0].set_xticks(XTick)
axP[1][2].set_xticklabels(XLabel)
labels = axP[0][1].get_xticklabels()
for i in range(2):
    for j in range(3):
        labels = labels + axP[i][j].get_xticklabels() + axP[i][j].get_yticklabels()
        xxx = axP[i][j].axvspan(ymin = 0,ymax = 1,xmin = 13,xmax = 17,alpha = 0.3,color = "gray")
L1 = plt.legend([xxx],["Scintillating"],prop=font_legend,
        framealpha=0,facecolor='white',ncol=4,numpoints=5,markerscale=4,frameon = True, 
        borderaxespad=0,bbox_to_anchor=(1,1.19),loc=1)
plt.gca().add_artist(L1)
[label.set_fontsize(xtick_size) for label in labels]
[label.set_fontname('Arial') for label in labels]
# plt.savefig("/Users/hanjunjie/Desktop/Image-1/HKLT_DIFF_ROTI_2021279.jpg",dpi=300)
plt.show()