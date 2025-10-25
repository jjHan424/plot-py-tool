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
font_text = {'family' : 'Arial','weight' : 300,'size'   : 25}
xtick_size = 25
color_list = sns.color_palette("Set1")
color_list = ["#0099E5","#34BF49","#FF4C4C"]
Direct = r"/Users/hanjunjie/Master_3/1-IUGG/ResFromServer/CLIENT"

Y=2021
M=12
D=10
# S=11
S=8.5
LastT = 3
All = False
Fixed = False
doy = tr.ymd2doy(Y,M,D,0,0,00)
max_error = 20
step = 0.2
START = 0
mode_list = ["Fixed","Semiempirical","Auto"]
filename_list = [
            os.path.join(Direct,"FLT_CON",  "{}{:0>3}".format(Y,doy),"{}-GEC3-FIXED-0-5-1.flt".format("SEPT")),
            os.path.join(Direct,"FLT_COEF", "{}{:0>3}".format(Y,doy),"{}-GEC3-FIXED-0-5-1.flt".format("SEPT")),
            os.path.join(Direct,"FLT_CROSS","{}{:0>3}".format(Y,doy),"{}-GEC3-FIXED-0-5-1.flt".format("SEPT")),
            # os.path.join(Direct,"FLT_CROSS","{}{:0>3}".format(Y,doy),"{}-GEC3-FIXED-0-30-NEW.flt".format("SEPT")),
                ]
filename_ref = [os.path.join("/Users/hanjunjie/Master_3/1-IUGG/ResFromServer/CLIENT/Dynamic_ref","Ref_{:0>3}.txt".format(doy)),
                r"G:\Data\Res\Dynamic\2021310_WH\\Ref.txt",
                r"G:\Data\Res\Dynamic\2021310_WH\\Ref.txt",
                r"G:\Data\Res\Dynamic\2021310_WH\\Ref.txt",]
ENU_ALL = {}
for i in range(len(mode_list)):
    data_Raw = rf.open_flt_pvtflt_file(filename_list[i])
    # data_Raw = rf.open_ppprtk_rtpppfile(filename_list[i])
    REF_XYZ = rf.open_pos_ref_IE(filename_ref[0])
    data_ENU = dp.XYZ2ENU_dynamic(XYZ = data_Raw,REF_XYZ = REF_XYZ)
    ENU_ALL[mode_list[i]] = data_ENU

[XLabel,XTick,cov_Time,begT,LastT]=dr.xtick("GPST",Y,M,D,S,LastT,30)
data_all = {}
for cur_mode in ENU_ALL.keys():
    if cur_mode not in data_all.keys():
        data_all[cur_mode] = {}
        data_all[cur_mode]["E"],data_all[cur_mode]["N"],data_all[cur_mode]["U"] = [],[],[]
    for cur_time in ENU_ALL[cur_mode]:
        plot_time = (cur_time - cov_Time) / 3600
        if (plot_time >= begT and plot_time <= begT+LastT) or All:
            if Fixed and ENU_ALL[cur_mode][cur_time]["AMB"] == 0:
                continue
            e = ENU_ALL[cur_mode][cur_time]["E"]*100
            n = ENU_ALL[cur_mode][cur_time]["N"]*100
            u = ENU_ALL[cur_mode][cur_time]["U"]*100
            data_all[cur_mode]["E"].append(e)
            data_all[cur_mode]["N"].append(n)
            data_all[cur_mode]["U"].append(u)
data_plot,x_plot = {},{}
percent_95 = {}
for cur_mode in data_all.keys():
    if cur_mode not in data_plot.keys():
        data_plot[cur_mode],x_plot[cur_mode] = [],[]
    start = START
    
    e = np.array(data_all[cur_mode]["E"]) - np.mean(np.array(data_all[cur_mode]["E"]))
    n = np.array(data_all[cur_mode]["N"]) - np.mean(np.array(data_all[cur_mode]["N"]))
    u = np.array(data_all[cur_mode]["U"]) - np.mean(np.array(data_all[cur_mode]["U"]))
    # temp_data = np.abs(u)
    temp_data = np.sqrt(np.power(e,2)+np.power(n,2)+np.power(u,2))
    temp_data = np.sort(temp_data)
    all_num = temp_data.size
    print("{}-{}-{:.2f}".format(cur_mode,"68.26",temp_data[int(0.6826*all_num)]))
    print("{}-{}-{:.2f}".format(cur_mode,"95.44",temp_data[int(0.95*all_num)]))
    print("{}-{}-{:.2f}".format(cur_mode,"99.75",temp_data[int(0.9974*all_num)]))
    percent_95[cur_mode] = temp_data[int(0.95*all_num)]
    while start <max_error:
        cur_accuracy = temp_data[(temp_data >= start) & (temp_data < start+step)]
        start = start+step
        data_plot[cur_mode].append(cur_accuracy.size/all_num*100)
        x_plot[cur_mode].append(start)
figP,axP = plt.subplots(1,1,figsize=(8,8),sharey=False,sharex=True)
axP.set_ylim(0,15)
j=-1
for cur_mode in percent_95:
    j=j+1
    xxx = axP.axvline(x=percent_95[cur_mode],color = color_list[j%3],linestyle = "--",linewidth = 3)
# L1 = plt.legend([xxx],["95% Confidence"],prop=font_legend,
#         framealpha=0,facecolor='white',ncol=4,numpoints=5,markerscale=4,frameon = True, 
#         borderaxespad=0,bbox_to_anchor=(0.67,1),loc=1)
# for legobj in L1.legendHandles:
#     legobj.set_linewidth(3)
#     legobj.set_color("black")
# plt.gca().add_artist(L1)
j=-1
for cur_mode in data_all.keys():
    j=j+1
    if j == 1:
        legend2 = axP.bar(x_plot[cur_mode],data_plot[cur_mode],width = step,bottom=data_plot[mode_list[j-1]],label='value',color = color_list[j%9])
    if j == 2:
        legend3 = axP.bar(x_plot[cur_mode],data_plot[cur_mode],width = step,bottom=np.array(data_plot[mode_list[j-1]])+np.array(data_plot[mode_list[j-2]]),label='value',color = color_list[j%3])
    if j == 0:
        legend1 = axP.bar(x_plot[cur_mode],data_plot[cur_mode],width = step,label='value',color = color_list[j%3])
    # axP.bar(np.array(x_plot[cur_mode])+step/3*(j-1),data_plot[cur_mode],width = step/3,label='value',color = color_list[j%3])
    x = np.array(x_plot[cur_mode])
    y = np.array(data_plot[cur_mode])
    # y = y[(x > -0.05)&(x < 0.05)]
    temp = y[x<=5]
    print("{}:{:.2f}".format(cur_mode,temp.sum()))
    temp = y[x>10]
    print("{}:{:.2f}".format(cur_mode,temp.sum()))
axP.legend([legend1,legend2,legend3,xxx],[mode_list[0],mode_list[1],mode_list[2],"95% Confidence"],prop=font_legend,
        framealpha=1,facecolor='w',numpoints=5, markerscale=3, frameon=False,ncol = 2,
        loc=1,borderaxespad=0,bbox_to_anchor=(1.1,1.16))
leg = axP.get_legend()
j=0
for legobj in leg.legendHandles:
    j=j+1
    if j == 4:
        legobj.set_linewidth(3)
        legobj.set_color("black")
# L1 = plt.legend([legend2],[mode_list[1]],prop=font_legend,
#         framealpha=0,facecolor='white',ncol=4,numpoints=5,markerscale=4,frameon = True, 
#         borderaxespad=0,bbox_to_anchor=(0.67,0.93),loc=1)
# plt.gca().add_artist(L1)
# L1 = plt.legend([legend1],[mode_list[0]],prop=font_legend,
#         framealpha=0,facecolor='white',ncol=4,numpoints=5,markerscale=4,frameon = True, 
#         borderaxespad=0,bbox_to_anchor=(0.67,0.87),loc=1)
# plt.gca().add_artist(L1)
# L1 = plt.legend([legend3],[mode_list[2]],prop=font_legend,
#         framealpha=0,facecolor='white',ncol=4,numpoints=5,markerscale=4,frameon = True, 
#         borderaxespad=0,bbox_to_anchor=(0.67,0.81),loc=1)
# plt.gca().add_artist(L1)
j=-1

axP.set_xlabel("3D position errors (cm)",font_label)
axP.set_ylabel("Percentage (%)",font_label)
axP.set_xticks([0,5,10,15,20])
labels = axP.get_xticklabels() + axP.get_yticklabels()
[label.set_fontsize(xtick_size) for label in labels]
[label.set_fontname('Arial') for label in labels]

# plt.savefig("/Users/hanjunjie/Desktop/Image-1/SEPT_20211210_344_Percent.jpg",dpi=300)
plt.show()