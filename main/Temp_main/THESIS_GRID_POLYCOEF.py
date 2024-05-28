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
font_title = {'family' : 'Arial', 'weight' : 300, 'size' : 20}
font_label = {'family' : 'Arial', 'weight' : 300, 'size' : 20}
font_tick = {'family' : 'Arial', 'weight' : 300, 'size' : 20}
font_legend = {'family' : 'Arial', 'weight' : 300, 'size' : 20}
# font_legend = {'family' : 'Times New Roman', 'weight' : 600, 'size' : 15}
font_text = {'family' : 'Arial','weight' : 300,'size'   : 20}
xtick_size = 20
color_list = sns.color_palette("Set1")
color_list = ["#0099E5","#34BF49","#FF4C4C"]

site_list = ["HKLM"]
count = 1
# Year,Mon,Day,Hour,LastT,deltaT = 2021,11,1,5,16,4
Year,Mon,Day,Hour,LastT,deltaT = 2021,11,7,16,1.5,30/60
cur_site = site_list[0]
[XLabel,XTick,cov_Time,begT,LastT]=dr.xtick_min("GPST",Year,Mon,Day,Hour,LastT,deltaT)
doy = tr.ymd2doy(Year,Mon,Day,0,00,00)
cdoy = "{:0>3}".format(doy)
path_grid = "/Users/hanjunjie/Master_3/1-IUGG/AUG2GRID/2021311/HK_HKLT_NEW_4_6S/GREAT-GEC3-30.grid"
plot_sat = "G22"
[grid_data_S,lat,lon] = rf.open_grid_file(path_grid)
data_plot,time_plot = {},[]
for cur_time in grid_data_S.keys():
    plot_time = (cur_time - cov_Time) / 3600
        # if time not in Diff_Data.keys():
        #     continue
    if (plot_time > begT and plot_time < begT + LastT):
        Numberall,NumberScin = {"G":0,"E":0,"C":0},{"G":0,"E":0,"C":0}
        for cur_sat in grid_data_S[cur_time].keys():
            if cur_sat != plot_sat:
                continue
            for i in range(4):
                if i not in data_plot.keys():
                    data_plot[i] = []
                data_plot[i].append(grid_data_S[cur_time][cur_sat][i])
            time_plot.append(plot_time)
figP,axP = plt.subplots(4,3,figsize=(14,10),sharey=False,sharex=True)
# axP[1].set_xlabel('Time' + ' (' + time + ')',font_label)
axP[3][0].set_xlabel("GPS time (hour)",font_label)
axP[3][1].set_xlabel("GPS time (hour)",font_label)
axP[3][2].set_xlabel("GPS time (hour)",font_label)
axP[0][0].set_ylabel(r'$A_{00}$',font_label)
axP[1][0].set_ylabel(r'$A_{00}$',font_label)
axP[2][0].set_ylabel(r'$A_{00}$',font_label)
axP[3][0].set_ylabel(r'$A_{00}$',font_label)
# axP[1].yaxis.set_label_coords(-0.1,0.5)
axP[0][0].set_title('Raw',font_title)
axP[0][1].set_title('First difference',font_title)
axP[0][2].set_title('Seconde difference',font_title)
# for i in range(3):
#     axP[i].grid(linestyle='--',linewidth=0.2, color='black',axis='both')
#     axP[i].set_ylim(0,15)
#     box = axP[i].get_position()
#     axP[i].set_position([box.x0, box.y0 + box.height*0.15, box.width, box.height*0.8])
sys_axP = {"G":0,"E":1,"C":2}
j=-1
for cur_mode in data_plot.keys():
    axP[cur_mode][0].plot(time_plot,data_plot[cur_mode],color = color_list[0],linestyle = "-",marker = "o",markersize = 5)
    # axP[cur_mode][0].scatter(time_plot,data_plot[cur_mode],color = color_list[0],marker = "o",s=5)
    axP[cur_mode][1].plot(time_plot[:-1],np.diff(data_plot[cur_mode]),color = color_list[0],linestyle = "-",marker = "o",markersize = 5)
    axP[cur_mode][2].plot(time_plot[:-2],np.diff(np.diff(data_plot[cur_mode])),color = color_list[0],linestyle = "-",marker = "o",markersize = 5)
    
# axP[1].legend(["Scintillating","All"],prop=font_legend,
#         framealpha=1,facecolor='w',numpoints=5, markerscale=3, frameon=False,
#         loc=0,borderaxespad=0)
# leg = axP[1].get_legend()
# for legobj in leg.legendHandles:
#     legobj.set_linewidth(3)
axP[3][2].set_xticks(XTick)
axP[3][1].set_xticks(XTick)
axP[3][0].set_xticks(XTick)
axP[3][2].set_xticklabels(XLabel)
labels = axP[0][0].get_xticklabels()
for i in range(4):
    for j in range(3):
        labels = labels+axP[i][j].get_xticklabels() + axP[i][j].get_yticklabels()
[label.set_fontsize(xtick_size) for label in labels]
[label.set_fontname('Arial') for label in labels]
# plt.savefig("/Users/hanjunjie/Desktop/Image-1/KOS1_RAW_ARIMA_LSTM.jpg",dpi=300)
plt.show()