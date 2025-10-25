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
# time,year,mon,day,starttime,LastT,deltaT = "UTC",2022,4,10,4,96,4


font_title = {'family' : 'Arial', 'weight' : 500, 'size' : 35}
font_label = {'family' : 'Arial', 'weight' : 300, 'size' : 30}
font_tick = {'family' : 'Arial', 'weight' : 300, 'size' : 35}
font_legend = {'family' : 'Arial', 'weight' : 300, 'size' : 30}
# font_legend = {'family' : 'Times New Roman', 'weight' : 600, 'size' : 15}
font_text = {'family' : 'Arial','weight' : 300,'size'   : 28}
xtick_size = 30
color_list = sns.color_palette("Set1")

beg_year,beg_mon,beg_day,beg_hour,beg_min,beg_sec = 2023,1,29,21,0,0
end_year,end_mon,end_day,end_hour,end_min,end_sec = 2023,1,30,3,0,0
[beg_week,beg_sow] = tr.ymd2gpst(beg_year,beg_mon,beg_day,beg_hour,beg_min,beg_sec)
[end_week,end_sow] = tr.ymd2gpst(end_year,end_mon,end_day,end_hour,end_min,end_sec)
file_list1 = []
beg_dow = int(beg_sow/3600/24)
end_dow = int(end_sow/3600/24)
last_Day = (end_week-beg_week) * 7 + (end_dow - beg_dow)
file_week,file_dow = beg_week,beg_dow
while last_Day >= 0:
    file_list1.append(os.path.join(r"E:\1Master_3\2_ZTD\2023029\Data\SP3","gfz{:0>4}{:0>1}.sp3".format(file_week,file_dow)))
    file_dow = file_dow + 1
    if (file_dow == 7):
        file_dow = 0
        file_week = file_week + 1
    last_Day = last_Day - 1

data_delta = 30
plot_sat = ["G","E","C"]
# READ .sp3
data_raw_x,data_raw_y,data_raw_z = {},{},{}

LastT = ((end_week-beg_week) * 604800 + (end_sow - beg_sow)) / 3600
w_last, soweek_last = 0,0
for cur_file in file_list1:
    epoch_flag = False
    with open(cur_file,'rt') as f:
        for line in f:
            value  = line.split()
            if value[0] == "*":
                cur_year,cur_mon,cur_day,cur_hour,cur_min,cur_sec = int(value[1]),int(value[2]),int(value[3]),int(value[4]),int(value[5]),float(value[6])
                [cur_week,cur_sow] = tr.ymd2gpst(cur_year,cur_mon,cur_day,cur_hour,cur_min,cur_sec)
                if cur_week < beg_week or cur_week > end_week:
                    continue
                if cur_week == beg_week and cur_sow < beg_sow:
                    continue
                if cur_week == end_week and cur_sow > end_sow:
                    continue
                epoch_flag = True
                if (cur_sow + w_last*604800 < soweek_last):
                    w_last = w_last + 1
                cur_sow = cur_sow + w_last*604800
                soweek_last = cur_sow
            if value[0][0] == "P" and epoch_flag == True:
                cur_sat = value[0][1:4]
                if "ALL" in plot_sat or cur_sat in plot_sat or cur_sat[0] in plot_sat:
                    if cur_sat not in data_raw_x.keys():
                        data_raw_x[cur_sat],data_raw_y[cur_sat],data_raw_z[cur_sat] = {},{},{}
                    data_raw_x[cur_sat][cur_sow] = float(value[1]) * 1000
                    data_raw_y[cur_sat][cur_sow] = float(value[2]) * 1000
                    data_raw_z[cur_sat][cur_sow] = float(value[3]) * 1000
                    

# DATA_CONVERT
data_plot_x,data_plot_y,data_plot_z,time_plot = {},{},{},{}
[XLabel,XTick,cov_Time,begT,LastT]=dr.xtick("UTC",beg_year,beg_mon,beg_day,beg_hour,LastT,1)
for cur_sat in data_raw_x:
    if "ALL" in plot_sat or cur_sat in plot_sat or cur_sat[0] in plot_sat:
        if cur_sat not in data_plot_x:
            data_plot_x[cur_sat],data_plot_y[cur_sat],data_plot_z[cur_sat] = [],[],[]
            time_plot[cur_sat] = []
        for cur_time in data_raw_x[cur_sat].keys():
            plot_time = (cur_time - cov_Time) / 3600
            if (plot_time >= begT and plot_time <= begT + LastT):
                if cur_time + 300 in data_raw_x[cur_sat].keys():
                    # data_plot[cur_sat].append(2 * data_raw[cur_sat][cur_time+30] - data_raw[cur_sat][cur_time] - data_raw[cur_sat][cur_time+60])
                    data_plot_x[cur_sat].append(data_raw_x[cur_sat][cur_time+300] - data_raw_x[cur_sat][cur_time])
                    data_plot_y[cur_sat].append(data_raw_y[cur_sat][cur_time+300] - data_raw_y[cur_sat][cur_time])
                    data_plot_z[cur_sat].append(data_raw_z[cur_sat][cur_time+300] - data_raw_z[cur_sat][cur_time])
                    # data_plot[cur_sat].append(data_raw[cur_sat][cur_time+30])
                    time_plot[cur_sat].append(plot_time + 300/3600)

# PLOT

for cur_sat in data_plot_x.keys():
    figP,axP = plt.subplots(3,1,figsize=(17,8),sharey=False,sharex=True)
    axP[0].scatter(time_plot[cur_sat],data_plot_x[cur_sat])
    axP[1].scatter(time_plot[cur_sat],data_plot_y[cur_sat])
    axP[2].scatter(time_plot[cur_sat],data_plot_z[cur_sat])
    axP[2].set_xticks(XTick)
    axP[2].set_xticklabels(XLabel)
    axP[2].set_xlabel("Time (GPST)",font_label)
    axP[0].set_ylabel("Difference between epoch",font_label)
    labels = axP[0].get_yticklabels() + axP[1].get_yticklabels() + axP[2].get_yticklabels() + axP[2].get_xticklabels()
    [label.set_fontsize(xtick_size) for label in labels]
    [label.set_fontname('Arial') for label in labels]
    # plt.savefig(r"E:\1Master_3\2_ZTD\Result_From_Server\Fig\BNC_DELTA_{}.png".format(cur_sat))
    plt.show()