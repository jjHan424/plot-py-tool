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
time,year,mon,day,starttime,LastT,deltaT = "UTC",2023,1,26,16,132,8


font_title = {'family' : 'Arial', 'weight' : 500, 'size' : 35}
font_label = {'family' : 'Arial', 'weight' : 300, 'size' : 30}
font_tick = {'family' : 'Arial', 'weight' : 300, 'size' : 35}
font_legend = {'family' : 'Arial', 'weight' : 300, 'size' : 30}
# font_legend = {'family' : 'Times New Roman', 'weight' : 600, 'size' : 15}
font_text = {'family' : 'Arial','weight' : 300,'size'   : 28}
xtick_size = 30
color_list = sns.color_palette("Set1")
Site = "SPT0"
# filename_list = [
#             os.path.join(r"E:\1Master_3\2_ZTD\2021310\RECON",Site+"-GEC-FLOAT.flt"),
#             os.path.join(r"E:\1Master_3\2_ZTD\2021310\RECON",Site+"-GEC-FIXED.flt"),
#             os.path.join(r"E:\1Master_3\2_ZTD\2021310\RECON",Site+"-GEC-GRID-VIRTUAL.flt")
#                 ]
filename_list = [
            # os.path.join(r"E:\1Master_3\2_ZTD\2021310\ShortBaseLine_RND","SPT0"+"-GEC-FLOAT.flt"),
            # os.path.join(r"E:\1Master_3\2_ZTD\2021310\ShortBaseLine_RND","SPT0"+"-GEC-FIXED.flt"),
            # os.path.join(r"E:\1Master_3\2_ZTD\2021310\ShortBaseLine_RND","SPT0"+"-GEC-FIXED.flt"),
            # os.path.join(r"E:\1Master_3\2_ZTD\2021310\ShortBaseLine_RND","SPT0"+"-GEC-GRID-VIRTUAL.flt"),
            # os.path.join(r"E:\1Master_3\2_ZTD\2021310\Test","SPT0"+"-GEC-PPPRTK-CROSS-PART-RE-1000-REFAMB.flt"),
            # os.path.join(r"E:\1Master_3\2_ZTD\2021310\Test","SPT0"+"-GEC-PPPRTK-CROSS-PART-RE-AUTO-REFAMB.flt"),
            # os.path.join(r"E:\1Master_3\2_ZTD\2021310\Test","SPT0"+"-GEC-PPPRTK-CROSS-ALL-01-500-REFAMB.flt"),
            # os.path.join(r"E:\1Master_3\2_ZTD\2021310\Test","SPT0"+"-GEC-PPPRTK-CROSS-ALL-EQUAL-500-REFAMB.flt"),
            # os.path.join(r"E:\1Master_3\2_ZTD\2021310\FLT","FFMJ"+"-GEC-GRID-VIRTUAL.flt")
            r"E:\1Master_3\2_ZTD\Result_From_Server\Days_Test\PTBB-GFZ-KIN-86400.flt",
            r"E:\1Master_3\2_ZTD\Result_From_Server\Days_Test\PTBB-GFZ-KIN.flt",
                ]
# mode_list = ["FLOAT","FIXED","IONO_ALL","IONO_PART"]
# mode_list = ["PTBB","TRO1","VARS","WSRT"]
mode_list = ["FIXED","PPPRTK"]
site = Site
#---readfiles for .tro---#
all_data_ref = {}
plot_data_ref = []
ref_file = r"E:\1Master_3\2_ZTD\ref_zpd\spt03100.21zpd"
epoch_flag = False
with open(ref_file) as f:
    for line in f:
        if line == "+TROP/SOLUTION\n":
            epoch_flag = True
        value = line.split()
        if epoch_flag and value[0] == Site:
            if value[0][0:4] not in all_data_ref.keys():
                all_data_ref[value[0][0:4]] = []
            time_value = value[1].split(":")
            cur_time = float(time_value[2])/3600
            all_data_ref[value[0][0:4]].append(float(value[2]))
            if cur_time not in plot_data_ref:
                plot_data_ref.append(cur_time)
#---readfiles for .flt---#
all_data,all_amb = {},{}
for i in range(len(mode_list)):
    soweek_last = 0
    w_last = 0
    filepath = filename_list[i]
    all_data[mode_list[i]],all_amb[mode_list[i]] = {},{}
    head_end,epoch_flag = False,False
    with open(filepath,'rt') as f:
        for line in f:
            if "#" not in line:
                value=line.split()
                soweek = float(value[0])
                if (soweek + w_last*604800 < soweek_last):
                    w_last = w_last + 1
                soweek = soweek + w_last*604800
                soweek_last = soweek
                if soweek not in all_data.keys():
                    all_data[mode_list[i]][soweek]=float(value[len(value)-2])
                    all_amb[mode_list[i]][soweek] = value[8]

#---readfiles for .ztd---#
# all_data,all_amb = {},{}
# for i in range(len(filename_list)):
#     filepath = filename_list[i]
#     all_data[mode_list[i]],all_amb[mode_list[i]] = {},{}
#     head_end,epoch_flag = False,False
#     with open(filepath,'rt') as f:
#         for line in f:
#             if "END OF HEADER" in line:
#                 head_end = True
#             if ">" in line and head_end:
#                 value=line.split()
#                 year=(float(value[1]))
#                 month=(float(value[2]))
#                 day=(float(value[3]))
#                 hour=(float(value[4]))
#                 minute=(float(value[5]))
#                 second=(float(value[6]))
#                 ztd = (float(value[7]))
#                 [w,soweek] = tr.ymd2gpst(year,month,day,hour,minute,second)
#                 if (not epoch_flag):
#                     min_sow = soweek
#                 if (soweek < min_sow):
#                     soweek = soweek + 604800
#                 epoch_flag = True
#                 if soweek not in all_data.keys():
#                     all_data[mode_list[i]][soweek]=ztd
#                     all_amb[mode_list[i]][soweek] = value[8]


#data convert
[XLabel,XTick,cov_Time,begT,LastT]=dr.xtick(time,year,mon,day,starttime,LastT,deltaT)
time_plot,data_plot = {},{}
time_float,data_float = {},{}
for cur_mode in all_data.keys():
    time_plot[cur_mode],data_plot[cur_mode],time_float[cur_mode],data_float[cur_mode] = [],[],[],[]
    for cur_time in all_data[cur_mode].keys():
        plot_time = (cur_time - cov_Time) / 3600
        if (plot_time >= begT and plot_time <= begT + LastT):
            time_plot[cur_mode].append(plot_time)
            data_plot[cur_mode].append(all_data[cur_mode][cur_time])
            if (all_amb[cur_mode][cur_time] == "Float"):
                time_float[cur_mode].append(plot_time)
                data_float[cur_mode].append(all_data[cur_mode][cur_time])
#plot
figP,axP = plt.subplots(1,1,figsize=(17,8),sharey=True,sharex=True)
for i in range(len(mode_list)):
    axP.scatter(time_plot[mode_list[i]],data_plot[mode_list[i]],color = color_list[i%9],s=8)
    #  axP.plot(time_plot[mode_list[i]],data_plot[mode_list[i]],color = color_list[i%9],linewidth = 3)
# for i in range(len(mode_list)):
#     axP.scatter(time_float[mode_list[i]],data_float[mode_list[i]],color = color_list[1],s=5)
axP.set_xticks(XTick)
axP.set_xticklabels(XLabel)
axP.set_title(site,font_title)
axP.legend(mode_list,prop=font_legend,
            framealpha=0,facecolor='none',numpoints=5,markerscale=4, 
            borderaxespad=0) 
# axP.legend(["Fixed","Float"],prop=font_legend,
#             framealpha=0,facecolor='none',numpoints=5,markerscale=4, 
#             borderaxespad=0) 
axP.set_xlabel("Time (GPST)",font_label)
axP.set_ylabel("Zenith Troposphere Delay (mm)",font_label)
# axP.set_ylim(2320,2380)
labels = axP.get_yticklabels() + axP.get_xticklabels()
[label.set_fontsize(xtick_size) for label in labels]
[label.set_fontname('Arial') for label in labels]
# axP.scatter(plot_data_ref,all_data_ref[site],marker = "*",color = color_list[4],s=150)
plt.show()