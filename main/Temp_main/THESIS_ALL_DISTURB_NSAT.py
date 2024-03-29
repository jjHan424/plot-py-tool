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
Year,Mon,Day,Hour,LastT,deltaT = 2021,11,1,10,6,2
cur_site = site_list[0]
[XLabel,XTick,cov_Time,begT,LastT]=dr.xtick("GPST",Year,Mon,Day,Hour,LastT,deltaT)
doy = tr.ymd2doy(Year,Mon,Day,0,00,00)
cdoy = "{:0>3}".format(doy)
path_roti = os.path.join("/Users/hanjunjie/Master_3/1-IUGG/ResFromServer/ROTI_5S", cur_site + "{:0>4}".format(Year) + cdoy + "_GEC.ismr")
data = rf.open_ismr(path_roti)
data_plot,time_plot = {"Scintillating":{},"All":{}},{"Scintillating":{},"All":{}}
for cur_time in data.keys():
    plot_time = (cur_time - cov_Time) / 3600
        # if time not in Diff_Data.keys():
        #     continue
    if (plot_time > begT and plot_time < begT + LastT):
        Numberall,NumberScin = {"G":0,"E":0,"C":0},{"G":0,"E":0,"C":0}
        for cur_sat in data[cur_time].keys():
            if cur_sat[0] not in data_plot["All"].keys():
                data_plot["All"][cur_sat[0]],data_plot["Scintillating"][cur_sat[0]] = [],[]
                time_plot["All"][cur_sat[0]],time_plot["Scintillating"][cur_sat[0]] = [],[]
            Numberall[cur_sat[0]] = Numberall[cur_sat[0]] + 1
            if data[cur_time][cur_sat] > 0.8:
                NumberScin[cur_sat[0]] = NumberScin[cur_sat[0]] + 1
        for cur_sys in Numberall.keys():
            data_plot["All"][cur_sys].append(Numberall[cur_sys])
            data_plot["Scintillating"][cur_sys].append(NumberScin[cur_sys])
            time_plot["All"][cur_sys].append(plot_time)
            time_plot["Scintillating"][cur_sys].append(plot_time)
figP,axP = plt.subplots(1,3,figsize=(12,4),sharey=True,sharex=True)
# axP[1].set_xlabel('Time' + ' (' + time + ')',font_label)
axP[1].set_xlabel("GPS time (hour)",font_label)
axP[0].set_ylabel('Number of satellites',font_label)
# axP[1].yaxis.set_label_coords(-0.1,0.5)
axP[0].set_title('GPS ({:.1f}%)'.format(np.mean(data_plot["Scintillating"]["G"])/np.mean(data_plot["All"]["G"])*100),font_title)
axP[1].set_title('GAL ({:.1f}%)'.format(np.mean(data_plot["Scintillating"]["E"])/np.mean(data_plot["All"]["E"])*100),font_title)
axP[2].set_title('BDS ({:.1f}%)'.format(np.mean(data_plot["Scintillating"]["C"])/np.mean(data_plot["All"]["C"])*100),font_title)
for i in range(3):
    axP[i].grid(linestyle='--',linewidth=0.2, color='black',axis='both')
    axP[i].set_ylim(0,15)
    box = axP[i].get_position()
    axP[i].set_position([box.x0, box.y0 + box.height*0.15, box.width, box.height*0.8])
sys_axP = {"G":0,"E":1,"C":2}
j=-1
for cur_mode in data_plot.keys():
    j = j + 1
    for cur_sys in data_plot[cur_mode].keys():
        axP[sys_axP[cur_sys]].plot(time_plot[cur_mode][cur_sys],data_plot[cur_mode][cur_sys],color = color_list[j%3])
axP[1].legend(["Scintillating","All"],prop=font_legend,
        framealpha=1,facecolor='w',numpoints=5, markerscale=3, frameon=False,
        loc=0,borderaxespad=0)
leg = axP[1].get_legend()
for legobj in leg.legendHandles:
    legobj.set_linewidth(3)
axP[2].set_xticks(XTick)
axP[1].set_xticks(XTick)
axP[0].set_xticks(XTick)
axP[2].set_xticklabels(XLabel)
labels = axP[0].get_xticklabels() + axP[1].get_xticklabels() + axP[2].get_xticklabels() + axP[0].get_yticklabels()
[label.set_fontsize(xtick_size) for label in labels]
[label.set_fontname('Arial') for label in labels]
plt.savefig("/Users/hanjunjie/Desktop/Image-1/HKLT_NSAT_ROTI.jpg",dpi=300)
plt.show()