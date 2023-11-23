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
time,year,mon,day,starttime,LastT,deltaT = "UTC",2021,11,6,3,22,1


font_title = {'family' : 'Arial', 'weight' : 500, 'size' : 35}
font_label = {'family' : 'Arial', 'weight' : 300, 'size' : 30}
font_tick = {'family' : 'Arial', 'weight' : 300, 'size' : 35}
font_legend = {'family' : 'Arial', 'weight' : 300, 'size' : 30}
# font_legend = {'family' : 'Times New Roman', 'weight' : 600, 'size' : 15}
font_text = {'family' : 'Arial','weight' : 300,'size'   : 28}
xtick_size = 30
color_list = sns.color_palette("Set1")

time,year,mon,day,starttime,LastT,deltaT = "UTC",2021,11,6,2,22,1
aug_self = r"E:\1Master_3\2_ZTD\2021310\Test\SPT0-GEC-PPPRTK-SELF.aug"
aug_cross = r"E:\1Master_3\2_ZTD\2021310\Test\SPT0-GEC-PPPRTK-CROSS.aug"
aug_ele = r"E:\1Master_3\2_ZTD\2021310\Test\SPT0-GEC.aug"
[head,self_aug] = rf.open_aug_file_new(aug_self)
[head,cross_aug] = rf.open_aug_file_new(aug_cross)
[head,ele_aug] = rf.open_aug_file_new(aug_ele)

ref_sat = {}

for cur_time in cross_aug.keys():
    if cur_time not in ele_aug.keys() or cur_time not in self_aug.keys():
        continue
    ref_sat[cur_time] = {}
    ref_sat[cur_time]["cross"],ref_sat[cur_time]["self"],ref_sat[cur_time]["ele"] = {},{},{}
    cur_error = {}
    # CROSS
    cur_error["G"],cur_error["E"],cur_error["C"] = [],[],[]
    cur_forsort = {}
    for cur_sat in cross_aug[cur_time].keys():
        if "dION1" not in cross_aug[cur_time][cur_sat].keys():
            continue
        cur_error[cur_sat[0]].append(cross_aug[cur_time][cur_sat]["dION1"])
        cur_forsort[cross_aug[cur_time][cur_sat]["dION1"]] = cur_sat
    for cur_sys in cur_error.keys():
        if len(cur_error[cur_sys]) <= 0:
            continue
        cur_list_error = sorted(cur_error[cur_sys])
        min_error = cur_list_error[0]
        ref_sat[cur_time]["cross"][cur_sys] = (cur_forsort[min_error])
    # SELF
    cur_error["G"],cur_error["E"],cur_error["C"] = [],[],[]
    cur_forsort = {}
    for cur_sat in self_aug[cur_time].keys():
        if "dION1" not in self_aug[cur_time][cur_sat].keys():
            continue
        cur_error[cur_sat[0]].append(self_aug[cur_time][cur_sat]["dION1"])
        if self_aug[cur_time][cur_sat]["dION1"] == 999.9:
            ref_sat[cur_time]["self"][cur_sat[0]] = cur_sat
    # ELE
    cur_error["G"],cur_error["E"],cur_error["C"] = [],[],[]
    cur_forsort = {}
    for cur_sat in ele_aug[cur_time].keys():
        if "ELE" not in ele_aug[cur_time][cur_sat].keys():
            continue
        cur_error[cur_sat[0]].append(ele_aug[cur_time][cur_sat]["ELE"])
        cur_forsort[ele_aug[cur_time][cur_sat]["ELE"]] = cur_sat
    for cur_sys in cur_error.keys():
        if len(cur_error[cur_sys]) <= 0:
            continue
        cur_list_error = sorted(cur_error[cur_sys])
        min_error = cur_list_error[len(cur_list_error)-1]
        ref_sat[cur_time]["ele"][cur_sys] = (cur_forsort[min_error])

#convert to plot
[XLabel,XTick,cov_Time,begT,LastT]=dr.xtick(time,year,mon,day,starttime,LastT,deltaT)
data_plot,time_plot = {},{}
data_plot["G"],data_plot["E"],time_plot["G"],time_plot["E"] = [],[],[],[]
for cur_time in ref_sat.keys():
    plot_time = (cur_time - cov_Time) / 3600
    if (plot_time >= begT and plot_time <= begT + LastT):
        for cur_sys in data_plot.keys():
            time_plot[cur_sys].append(plot_time)
            if cur_sys not in ref_sat[cur_time]["cross"].keys():
                data_plot[cur_sys].append(5)
                continue
            if cur_sys not in ref_sat[cur_time]["self"].keys():
                data_plot[cur_sys].append(6)
                continue
            if cur_sys not in ref_sat[cur_time]["ele"].keys():
                data_plot[cur_sys].append(7)
                continue
            if ref_sat[cur_time]["cross"][cur_sys] == ref_sat[cur_time]["self"][cur_sys]:
                if ref_sat[cur_time]["self"][cur_sys] == ref_sat[cur_time]["ele"][cur_sys]:
                    data_plot[cur_sys].append(4)
                else:
                    data_plot[cur_sys].append(1)
            else:
                if ref_sat[cur_time]["cross"][cur_sys] == ref_sat[cur_time]["ele"][cur_sys]:
                    data_plot[cur_sys].append(2)
                else:
                    if ref_sat[cur_time]["self"][cur_sys] == ref_sat[cur_time]["ele"][cur_sys]:
                        data_plot[cur_sys].append(3)
                    else:
                        data_plot[cur_sys].append(0)
figP,axP = plt.subplots(2,1,figsize=(17,8),sharey=True,sharex=True)
axP[0].scatter(time_plot["G"],data_plot["G"])
axP[1].scatter(time_plot["E"],data_plot["E"])
plt.show()

        
