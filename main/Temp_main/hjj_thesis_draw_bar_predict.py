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
plt.style.use(['science','grid','no-latex'])
import math
import seaborn as sns
font_title = {'family' : 'Arial', 'weight' : 300, 'size' : 25}
font_label = {'family' : 'Arial', 'weight' : 300, 'size' : 25}
font_tick = {'family' : 'Arial', 'weight' : 300, 'size' : 6}
font_legend = {'family' : 'Arial', 'weight' : 300, 'size' : 25}
# font_legend = {'family' : 'Times New Roman', 'weight' : 600, 'size' : 15}
font_text = {'family' : 'Arial','weight' : 300,'size'   : 28}
xtick_size = 20
color_list = sns.color_palette("Set1")

#PLOT-1-1-1
file_raw = "/Users/hanjunjie/Master_3/1-IUGG/CLIENT_LSTM_SERVER"
file_path_lstm = "/Users/hanjunjie/Master_3/1-IUGG/CLIENT_LSTM_SERVER"
file_path_arima = "/Users/hanjunjie/Master_3/1-IUGG/CLIENT_LSTM_SERVER"

# Read File
data_lstm,data_arima,data_raw = {"G":{},"E":{},"C":{}},{"G":{},"E":{},"C":{}},{"G":{},"E":{},"C":{}}
delay_list = range(1,21)
for i in delay_list:
    cur_file = os.path.join(file_path_lstm,"HK-{}-LSTM-ACTIVE.txt".format(i))
    if i not in data_lstm.keys():
        data_lstm["G"][i],data_lstm["E"][i],data_lstm["C"][i] = [],[],[]
    with open(cur_file,"rt") as f:
        for line in f:
            value = line.split()
            data_lstm["G"][i].append(float(value[0]))
            data_lstm["E"][i].append(float(value[1]))
            data_lstm["C"][i].append(float(value[2]))
for i in delay_list:
    cur_file = os.path.join(file_path_arima,"HK-{}-ARIMA-ACTIVE.txt".format(i))
    if i not in data_arima.keys():
        data_arima["G"][i],data_arima["E"][i],data_arima["C"][i] = [],[],[]
    with open(cur_file,"rt") as f:
        for line in f:
            value = line.split()
            data_arima["G"][i].append(float(value[0]))
            data_arima["E"][i].append(float(value[1]))
            data_arima["C"][i].append(float(value[2]))
for i in delay_list:
    cur_file = os.path.join(file_path_arima,"HK-{}-RAW-ACTIVE.txt".format(i))
    if i not in data_raw.keys():
        data_raw["G"][i],data_raw["E"][i],data_raw["C"][i] = [],[],[]
    with open(cur_file,"rt") as f:
        for line in f:
            value = line.split()
            data_raw["G"][i].append(float(value[0]))
            data_raw["E"][i].append(float(value[1]))
            data_raw["C"][i].append(float(value[2]))

#Data Convert
data_plot = {}
cur_data = data_raw
for cur_sys in cur_data.keys():
    cur_type = "RAW"
    if cur_type not in data_plot.keys():
        data_plot[cur_type] = {}
    if cur_sys not in data_plot[cur_type].keys():
        data_plot[cur_type][cur_sys] = []
    for cur_delay in cur_data[cur_sys].keys():
        data_plot[cur_type][cur_sys].append(np.mean(cur_data[cur_sys][cur_delay]))
cur_data = data_arima
for cur_sys in cur_data.keys():
    cur_type = "ARIMA"
    if cur_type not in data_plot.keys():
        data_plot[cur_type] = {}
    if cur_sys not in data_plot[cur_type].keys():
        data_plot[cur_type][cur_sys] = []
    for cur_delay in cur_data[cur_sys].keys():
        data_plot[cur_type][cur_sys].append(np.mean(cur_data[cur_sys][cur_delay]))
cur_data = data_lstm
for cur_sys in cur_data.keys():
    cur_type = "LSTM"
    if cur_type not in data_plot.keys():
        data_plot[cur_type] = {}
    if cur_sys not in data_plot[cur_type].keys():
        data_plot[cur_type][cur_sys] = []
    for cur_delay in cur_data[cur_sys].keys():
        data_plot[cur_type][cur_sys].append(np.mean(cur_data[cur_sys][cur_delay]))
#Plot based on sys
sys_axP = {"G":0,"E":1,"C":2}
figP,axP = plt.subplots(3,1,figsize=(12,15),sharey=False,sharex=True)
i=-1
W = 0.8/len(data_plot)
for cur_type in data_plot.keys():
    i=i+1
    for cur_sys in data_plot[cur_type].keys():
        # axP[sys_axP[cur_sys]].plot(range(1,len(data_plot[cur_type][cur_sys])+1),data_plot[cur_type][cur_sys],color = color_list[i%9])
        axP[sys_axP[cur_sys]].bar([j-0.4+W/2+W*i for j in range(1,21)],data_plot[cur_type][cur_sys],width = W,label = "value",color = color_list[i%9])
        # axP[sys_axP[cur_sys]].set_ylim(3,13)
    for j in range(20):
        if j%2 != 0:
            print("{:.2f}".format(np.mean([data_plot[cur_type]["G"][j],data_plot[cur_type]["E"][j],data_plot[cur_type]["C"][j]])))
axP[0].legend(["RAW","ARIMA","LSTM"],prop=font_legend,
            framealpha=0,facecolor='none',ncol=3,numpoints=1,markerscale=1, 
            borderaxespad=0,bbox_to_anchor=(1,1.25),loc=1)
i=-1
W = 0.8/len(data_plot)
for cur_type in data_plot.keys():
    i=i+1
    for cur_sys in data_plot[cur_type].keys():
        # axP[sys_axP[cur_sys]].plot([j-0.4+W/2+W*i for j in range(0,20)],[q+1 for q in data_plot[cur_type][cur_sys]],color = color_list[i%9],marker = ".",linestyle="-",markersize=8)
        # axP[sys_axP[cur_sys]].bar([j-0.4+W/2+W*i for j in range(0,20)],data_plot[cur_type][cur_sys],width = W,label = "value",color = color_list[i%9])
        axP[sys_axP[cur_sys]].plot([j for j in range(1,21)],[5 for j in range(1,21)],color = "black",linestyle = "--",linewidth = 2)
    # for cur_sys in data_plot[cur_type].keys():
    break
ax_range = axP[0].axis()
axP[0].text(ax_range[0],ax_range[3],"GPS",font_title)
ax_range = axP[1].axis()
axP[1].text(ax_range[0],ax_range[3],"GAL",font_title)
ax_range = axP[2].axis()
axP[2].text(ax_range[0],ax_range[3],"BDS",font_title)
axP[2].set_xticks(range(0,21,2))
axP[2].set_xticklabels(range(0,11))
labels = axP[0].get_yticklabels() + axP[1].get_yticklabels() + axP[2].get_yticklabels() + axP[0].get_xticklabels() + axP[1].get_xticklabels() + axP[2].get_xticklabels()
[label.set_fontsize(xtick_size) for label in labels]
[label.set_fontname('Arial') for label in labels]
axP[1].set_ylabel('Accuracy of Ionosphere Delay correction/cm',font_label)
axP[2].set_xlabel('Prediction duration/min',font_label)
plt.show()


                                                #======PLOT-2======#
# file_raw = "/Users/hanjunjie/Master_3/1-IUGG/CLIENT_LSTM_SERVER"
# file_path_lstm = "/Users/hanjunjie/Master_3/1-IUGG/CLIENT_LSTM_SERVER"
# file_path_arima = "/Users/hanjunjie/Master_3/1-IUGG/CLIENT_LSTM_SERVER"

# # Read File
# cur_data = {"G":{},"E":{},"C":{},"MEAN":{}}
# delay_list = range(1,21)
# ele_sat = ["QUITE","ACTIVE"]
# for i in delay_list:
#     for cur_ele in ele_sat:
#         cur_file = os.path.join(file_path_lstm,"HK-{}-LSTM-{}.txt".format(i,cur_ele))
#         if cur_ele not in cur_data["G"].keys():
#             cur_data["G"][cur_ele],cur_data["E"][cur_ele],cur_data["C"][cur_ele],cur_data["MEAN"][cur_ele] = {},{},{},{}
#         if i not in cur_data.keys():
#             cur_data["G"][cur_ele][i],cur_data["E"][cur_ele][i],cur_data["C"][cur_ele][i],cur_data["MEAN"][cur_ele][i] = [],[],[],[]
#         with open(cur_file,"rt") as f:
#             for line in f:
#                 value = line.split()
#                 cur_data["G"][cur_ele][i].append(float(value[0]))
#                 cur_data["E"][cur_ele][i].append(float(value[1]))
#                 cur_data["C"][cur_ele][i].append(float(value[2]))
#                 cur_data["MEAN"][cur_ele][i].append(np.mean([float(value[0]),float(value[1]),float(value[2])]))
# data_lstm = cur_data
# cur_data = {"G":{},"E":{},"C":{},"MEAN":{}}
# delay_list = range(1,21)
# ele_sat = ["QUITE","ACTIVE"]
# for i in delay_list:
#     for cur_ele in ele_sat:
#         cur_file = os.path.join(file_path_lstm,"HK-{}-ARIMA-{}.txt".format(i,cur_ele))
#         if cur_ele not in cur_data["G"].keys():
#             cur_data["G"][cur_ele],cur_data["E"][cur_ele],cur_data["C"][cur_ele],cur_data["MEAN"][cur_ele] = {},{},{},{}
#         if i not in cur_data.keys():
#             cur_data["G"][cur_ele][i],cur_data["E"][cur_ele][i],cur_data["C"][cur_ele][i],cur_data["MEAN"][cur_ele][i] = [],[],[],[]
#         with open(cur_file,"rt") as f:
#             for line in f:
#                 value = line.split()
#                 cur_data["G"][cur_ele][i].append(float(value[0]))
#                 cur_data["E"][cur_ele][i].append(float(value[1]))
#                 cur_data["C"][cur_ele][i].append(float(value[2]))
#                 cur_data["MEAN"][cur_ele][i].append(np.mean([float(value[0]),float(value[1]),float(value[2])]))
# data_arima = cur_data
# cur_data = {"G":{},"E":{},"C":{},"MEAN":{}}
# delay_list = range(1,21)
# ele_sat = ["QUITE","ACTIVE"]
# for i in delay_list:
#     for cur_ele in ele_sat:
#         cur_file = os.path.join(file_path_lstm,"HK-{}-RAW-{}.txt".format(i,cur_ele))
#         if cur_ele not in cur_data["G"].keys():
#             cur_data["G"][cur_ele],cur_data["E"][cur_ele],cur_data["C"][cur_ele],cur_data["MEAN"][cur_ele] = {},{},{},{}
#         if i not in cur_data.keys():
#             cur_data["G"][cur_ele][i],cur_data["E"][cur_ele][i],cur_data["C"][cur_ele][i],cur_data["MEAN"][cur_ele][i] = [],[],[],[]
#         with open(cur_file,"rt") as f:
#             for line in f:
#                 value = line.split()
#                 cur_data["G"][cur_ele][i].append(float(value[0]))
#                 cur_data["E"][cur_ele][i].append(float(value[1]))
#                 cur_data["C"][cur_ele][i].append(float(value[2]))
#                 cur_data["MEAN"][cur_ele][i].append(np.mean([float(value[0]),float(value[1]),float(value[2])]))
# data_raw = cur_data

# #Data Convert
# data_plot = {}
# # cur_data = data_raw
# # for cur_sys in cur_data["MEAN"].keys():
# #     cur_type = "RAW"
# #     if cur_type not in data_plot.keys():
# #         data_plot[cur_type] = {}
# #     if cur_sys not in data_plot[cur_type].keys():
# #         data_plot[cur_type][cur_sys] = []
# #     for cur_delay in cur_data["MEAN"][cur_sys].keys():
# #         data_plot[cur_type][cur_sys].append((np.mean(cur_data["MEAN"][cur_sys][cur_delay])))
# cur_data = data_arima
# for cur_sys in cur_data["MEAN"].keys():
#     cur_type = "ARIMA"
#     if cur_type not in data_plot.keys():
#         data_plot[cur_type] = {}
#     if cur_sys not in data_plot[cur_type].keys():
#         data_plot[cur_type][cur_sys] = []
#     for cur_delay in cur_data["MEAN"][cur_sys].keys():
#         data_plot[cur_type][cur_sys].append((np.mean(data_raw["MEAN"][cur_sys][cur_delay]) - np.mean(cur_data["MEAN"][cur_sys][cur_delay]))/np.mean(data_raw["MEAN"][cur_sys][cur_delay])*100)
# cur_data = data_lstm
# for cur_sys in cur_data["MEAN"].keys():
#     cur_type = "LSTM"
#     if cur_type not in data_plot.keys():
#         data_plot[cur_type] = {}
#     if cur_sys not in data_plot[cur_type].keys():
#         data_plot[cur_type][cur_sys] = []
#     for cur_delay in cur_data["MEAN"][cur_sys].keys():
#         data_plot[cur_type][cur_sys].append((np.mean(data_raw["MEAN"][cur_sys][cur_delay]) - np.mean(cur_data["MEAN"][cur_sys][cur_delay]))/np.mean(data_raw["MEAN"][cur_sys][cur_delay])*100)
# #Plot based on sys
# # sys_axP = {"DAY":0,"NIGHT":1,90:2}
# sys_axP = {"RAW":0,"QUITE":0,"ACTIVE":1}
# figP,axP = plt.subplots(1,2,figsize=(18,14),sharey=True,sharex=True)
# i=-1
# W = 0.8/len(data_plot)
# # W = 0.8/2
# for cur_type in data_plot.keys():
#     i=i+1
#     for cur_sys in data_plot[cur_type].keys():
#         # axP[sys_axP[cur_sys]].plot(range(1,len(data_plot[cur_type][cur_sys])+1),data_plot[cur_type][cur_sys],color = color_list[i%9])
#         axP[sys_axP[cur_sys]].bar([j-0.4+W/2+W*i for j in range(1,21)],data_plot[cur_type][cur_sys],width = W,label = "value",color = color_list[(i+1)%9])
#     # i=i+1
#     # axP[sys_axP[cur_type]].bar([j-0.4+W/2+W*i for j in range(1,21)],data_plot[cur_type]["NIGHT"],width = W,label = "value",color = color_list[2])
#         # axP[sys_axP[cur_sys]].set_ylim(3,13)
#     # for j in range(20):
#     #     if j%2 != 0:
#     #         print("{:.2f}".format(np.mean([data_plot[cur_type]["G"][j],data_plot[cur_type]["E"][j],data_plot[cur_type]["C"][j]])))
# axP[1].legend(["ARIMA","LSTM"],prop=font_legend,
#             framealpha=0,facecolor='none',ncol=2,numpoints=1,markerscale=1,
#             borderaxespad=0,bbox_to_anchor=(1,1.18),loc=1)
# i=-1
# W = 0.8/len(data_plot)
# # for cur_type in data_plot.keys():
# #     i=i+1
# #     # for cur_sys in data_plot[cur_type].keys():
# #         # axP[sys_axP[cur_sys]].plot([j-0.4+W/2+W*i for j in range(0,20)],[q+1 for q in data_plot[cur_type][cur_sys]],color = color_list[i%9],marker = ".",linestyle="-",markersize=8)
# #         # axP[sys_axP[cur_sys]].bar([j-0.4+W/2+W*i for j in range(0,20)],data_plot[cur_type][cur_sys],width = W,label = "value",color = color_list[i%9])
# #     axP[sys_axP[cur_type]].plot([j for j in range(1,21)],[10 for j in range(1,21)],color = "black",linestyle = "--",linewidth = 2)
# #     axP[sys_axP[cur_type]].plot([j for j in range(1,21)],[15 for j in range(1,21)],color = "black",linestyle = "--",linewidth = 2)
# #     # for cur_sys in data_plot[cur_type].keys():
# #     # break
# # plt.show()
# ax_range = axP[0].axis()
# axP[0].text(ax_range[0],ax_range[3],"QUITE",font_title)
# ax_range = axP[1].axis()
# axP[1].text(ax_range[0],ax_range[3],"ACTIVE",font_title)
# # ax_range = axP[2].axis()
# # axP[2].text(ax_range[0],ax_range[3],"LSTM",font_title)
# axP[1].set_xticks(range(0,21,2))
# axP[1].set_xticklabels(range(0,11))
# labels = axP[0].get_yticklabels() + axP[1].get_yticklabels() + axP[0].get_xticklabels() + axP[1].get_xticklabels()
# [label.set_fontsize(xtick_size) for label in labels]
# [label.set_fontname('Arial') for label in labels]
# axP[0].set_ylabel('Percentage of improvement/%',font_label)
# axP[1].set_xlabel('Prediction duration/min',font_label)
# axP[0].set_xlabel('Prediction duration/min',font_label)
# plt.show()
