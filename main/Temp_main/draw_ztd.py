import os
import sys
sys.path.insert(0,os.path.dirname(__file__)+'/..')
sys.path.insert(0,os.path.dirname(__file__)+'/../..')
import numpy as np
import readfile as rf
import matplotlib as mpl
mpl.use("TkAgg")
import matplotlib.pyplot as plt
import dataprocess as dp
import draw as dr
#import seaborn as sns
import trans as tr
import seaborn as sns
plt.style.use(['science','grid','no-latex'])
import math
time,year,mon,day,starttime,LastT,deltaT = "UTC",2021,10,31,2,22,2


font_title = {'family' : 'Arial', 'weight' : 300, 'size' : 35}
font_label = {'family' : 'Arial', 'weight' : 300, 'size' : 33}
font_tick = {'family' : 'Arial', 'weight' : 300, 'size' : 35}
font_legend = {'family' : 'Arial', 'weight' : 300, 'size' : 30}
# font_legend = {'family' : 'Times New Roman', 'weight' : 600, 'size' : 15}
font_text = {'family' : 'Arial','weight' : 300,'size'   : 28}
xtick_size = 30
color_list = sns.color_palette("Set1")

filename_list = [
            # r"E:\1Master_2\1-ZTD\HK-ZTD-FLT\HKWS-GEC-305-PPP.ztd",
            # r"E:\1Master_2\1-ZTD\HK-ZTD-FLT\HKWS-GEC-305-PPPAR.ztd",
            r"E:\1Master_2\1-ZTD\HK-ZTD-FLT\HKWS-GEC-304-PPPRTK.ztd",
                ]
# mode_list = ["PPP","PPP-AR","PPP-RTK"]
mode_list = ["PPP-RTK"]
site = "HKWS"
#readfiles
all_data,all_amb = {},{}
for i in range(len(filename_list)):
    filepath = filename_list[i]
    all_data[mode_list[i]],all_amb[mode_list[i]] = {},{}
    head_end,epoch_flag = False,False
    with open(filepath,'rt') as f:
        for line in f:
            if "END OF HEADER" in line:
                head_end = True
            if ">" in line and head_end:
                value=line.split()
                year=(float(value[1]))
                month=(float(value[2]))
                day=(float(value[3]))
                hour=(float(value[4]))
                minute=(float(value[5]))
                second=(float(value[6]))
                ztd = (float(value[7]))
                [w,soweek] = tr.ymd2gpst(year,month,day,hour,minute,second)
                if (not epoch_flag):
                    min_sow = soweek
                if (soweek < min_sow):
                    soweek = soweek + 604800
                epoch_flag = True
                if soweek not in all_data.keys():
                    all_data[mode_list[i]][soweek]=ztd
                    all_amb[mode_list[i]][soweek] = value[8]
#data convert
[XLabel,XTick,cov_Time,begT,LastT]=dr.xtick(time,year,mon,day,starttime,LastT,deltaT)
time_plot,data_plot = {},{}
time_float,data_float = {},{}
for cur_mode in all_data.keys():
    time_plot[cur_mode],data_plot[cur_mode],time_float[cur_mode],data_float[cur_mode] = [],[],[],[]
    for cur_time in all_data[cur_mode].keys():
        plot_time = (cur_time - cov_Time) / 3600
        if (plot_time > begT and plot_time < begT + LastT):
            time_plot[cur_mode].append(plot_time)
            data_plot[cur_mode].append(all_data[cur_mode][cur_time])
            if (all_amb[cur_mode][cur_time] == "Float"):
                time_float[cur_mode].append(plot_time)
                data_float[cur_mode].append(all_data[cur_mode][cur_time])
#plot
figP,axP = plt.subplots(1,1,figsize=(16,7),sharey=True,sharex=True)
for i in range(len(mode_list)):
    axP.scatter(time_plot[mode_list[i]],data_plot[mode_list[i]],color = color_list[i%9],s=5)
for i in range(len(mode_list)):
    axP.scatter(time_float[mode_list[i]],data_float[mode_list[i]],color = color_list[1],s=5)
axP.set_xticks(XTick)
axP.set_xticklabels(XLabel)
axP.set_title(site,font_title)
# axP.legend(mode_list,prop=font_legend,
#             framealpha=0,facecolor='none',numpoints=5,markerscale=4, 
#             borderaxespad=0) 
axP.legend(["Fixed","Float"],prop=font_legend,
            framealpha=0,facecolor='none',numpoints=5,markerscale=4, 
            borderaxespad=0) 
labels = axP.get_yticklabels() + axP.get_xticklabels()
[label.set_fontsize(xtick_size) for label in labels]
[label.set_fontname('Arial') for label in labels]
plt.show()