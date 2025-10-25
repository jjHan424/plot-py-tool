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
xtick_size = 25
color_list = sns.color_palette("Set1")
color_list = ["#0099E5","#34BF49","#FF4C4C"]

#PLOT-1-1-1
file_raw = "/Users/hanjunjie/Master_3/1-IUGG/CLIENT_LSTM_SERVER"
file_path_lstm = "/Users/hanjunjie/Master_3/1-IUGG/CLIENT_LSTM_SERVER"
file_path_arima = "/Users/hanjunjie/Master_3/1-IUGG/CLIENT_LSTM_SERVER"

# Read File
data_lstm,data_arima,data_raw = {"G":{},"E":{},"C":{}},{"G":{},"E":{},"C":{}},{"G":{},"E":{},"C":{}}
delay_list = range(1,21)
for i in delay_list:
    cur_file = os.path.join(file_path_lstm,"GER-{}-LSTM-ELE-0-30.txt".format(i))
    if i not in data_lstm.keys():
        data_lstm["G"][i],data_lstm["E"][i],data_lstm["C"][i] = [],[],[]
    with open(cur_file,"rt") as f:
        for line in f:
            value = line.split()
            data_lstm["G"][i].append(np.mean([float(value[0]),float(value[1]),float(value[2])]))
for i in delay_list:
    cur_file = os.path.join(file_path_arima,"GER-{}-ARIMA-ELE-0-30.txt".format(i))
    if i not in data_arima.keys():
        data_arima["G"][i],data_arima["E"][i],data_arima["C"][i] = [],[],[]
    with open(cur_file,"rt") as f:
        for line in f:
            value = line.split()
            data_arima["G"][i].append(np.mean([float(value[0]),float(value[1]),float(value[2])]))
for i in delay_list:
    cur_file = os.path.join(file_path_arima,"GER-{}-RAW-ELE-0-30.txt".format(i))
    if i not in data_raw.keys():
        data_raw["G"][i],data_raw["E"][i],data_raw["C"][i] = [],[],[]
    with open(cur_file,"rt") as f:
        for line in f:
            value = line.split()
            data_raw["G"][i].append(np.mean([float(value[0]),float(value[1]),float(value[2])]))

for i in delay_list:
    cur_file = os.path.join(file_path_lstm,"GER-{}-LSTM-ELE-30-60.txt".format(i))
    if i not in data_lstm.keys():
        data_lstm["E"][i],data_lstm["C"][i] = [],[]
    with open(cur_file,"rt") as f:
        for line in f:
            value = line.split()
            data_lstm["E"][i].append(np.mean([float(value[0]),float(value[1]),float(value[2])]))
for i in delay_list:
    cur_file = os.path.join(file_path_arima,"GER-{}-ARIMA-ELE-30-60.txt".format(i))
    if i not in data_arima.keys():
        data_arima["E"][i],data_arima["C"][i] = [],[]
    with open(cur_file,"rt") as f:
        for line in f:
            value = line.split()
            data_arima["E"][i].append(np.mean([float(value[0]),float(value[1]),float(value[2])]))
for i in delay_list:
    cur_file = os.path.join(file_path_arima,"GER-{}-RAW-ELE-30-60.txt".format(i))
    if i not in data_raw.keys():
        data_raw["E"][i],data_raw["C"][i] = [],[]
    with open(cur_file,"rt") as f:
        for line in f:
            value = line.split()
            data_raw["E"][i].append(np.mean([float(value[0]),float(value[1]),float(value[2])]))

for i in delay_list:
    cur_file = os.path.join(file_path_lstm,"GER-{}-LSTM-ELE-60-90.txt".format(i))
    if i not in data_lstm.keys():
        data_lstm["C"][i] = []
    with open(cur_file,"rt") as f:
        for line in f:
            value = line.split()
            data_lstm["C"][i].append(np.mean([float(value[0]),float(value[1]),float(value[2])]))
for i in delay_list:
    cur_file = os.path.join(file_path_arima,"GER-{}-ARIMA-ELE-60-90.txt".format(i))
    if i not in data_arima.keys():
        data_arima["C"][i] = []
    with open(cur_file,"rt") as f:
        for line in f:
            value = line.split()
            data_arima["C"][i].append(np.mean([float(value[0]),float(value[1]),float(value[2])]))
for i in delay_list:
    cur_file = os.path.join(file_path_arima,"GER-{}-RAW-ELE-60-90.txt".format(i))
    if i not in data_raw.keys():
        data_raw["C"][i] = []
    with open(cur_file,"rt") as f:
        for line in f:
            value = line.split()
            data_raw["C"][i].append(np.mean([float(value[0]),float(value[1]),float(value[2])]))            

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
figP,axP = plt.subplots(1,3,figsize=(12,4),sharey=True,sharex=True)
for i in range(3):
#     for j in range(2):
    axP[i].set_ylim(3,18)
i=-1
W = 0.8/len(data_plot)
for cur_type in data_plot.keys():
    i=i+1
    for cur_sys in data_plot[cur_type].keys():
        axP[sys_axP[cur_sys]].plot(range(1,len(data_plot[cur_type][cur_sys])+1),data_plot[cur_type][cur_sys],color = color_list[i%3],linestyle = "-",marker = "o")
        # axP[sys_axP[cur_sys]].bar([j-0.4+W/2+W*i for j in range(1,21)],data_plot[cur_type][cur_sys],width = W,label = "value",color = color_list[i%9])
        # axP[sys_axP[cur_sys]].set_ylim(3,13)
    for j in range(20):
        if j%2 != 0:
            if (j+1)/2 == 2 or  (j+1)/2 == 4 or (j+1)/2 == 6 or (j+1)/2 == 8 or (j+1)/2 == 10:
                print("G: {:<6}:{:0>2} {:.2f}".format(cur_type,(j+1)/2,np.mean([data_plot[cur_type]["G"][j]])))
                print("E: {:<6}:{:0>2} {:.2f}".format(cur_type,(j+1)/2,np.mean([data_plot[cur_type]["E"][j]])))
                print("C: {:<6}:{:0>2} {:.2f}".format(cur_type,(j+1)/2,np.mean([data_plot[cur_type]["C"][j]])))
            # print("{:.2f}".format(np.mean([data_plot[cur_type]["G"][j],data_plot[cur_type]["E"][j],data_plot[cur_type]["C"][j]])))
axP[2].legend(["RAW","ARIMA","LSTM"],prop=font_legend,
            framealpha=0,facecolor='none',ncol=1,numpoints=1,markerscale=1, 
            borderaxespad=0,bbox_to_anchor=(1,1),loc=1)
i=-1
W = 0.8/len(data_plot)
for cur_type in data_plot.keys():
    i=i+1
    for cur_sys in data_plot[cur_type].keys():
        # axP[sys_axP[cur_sys]].plot([j-0.4+W/2+W*i for j in range(0,20)],[q+1 for q in data_plot[cur_type][cur_sys]],color = color_list[i%9],marker = ".",linestyle="-",markersize=8)
        # axP[sys_axP[cur_sys]].bar([j-0.4+W/2+W*i for j in range(0,20)],data_plot[cur_type][cur_sys],width = W,label = "value",color = color_list[i%9])
        axP[sys_axP[cur_sys]].plot([j for j in range(1,21)],[10 for j in range(1,21)],color = "black",linestyle = "--",linewidth = 2)
    # for cur_sys in data_plot[cur_type].keys():
    break
ax_range = axP[0].axis()
axP[0].text(ax_range[0],ax_range[3],r"$0^\circ$~$30^\circ$",font_title)
ax_range = axP[1].axis()
axP[1].text(ax_range[0],ax_range[3],r"$30^\circ$~$60^\circ$",font_title)
ax_range = axP[2].axis()
axP[2].text(ax_range[0],ax_range[3],r"$60^\circ$~$90^\circ$",font_title)
axP[2].set_xticks(range(0,21,2))
axP[2].set_xticklabels(range(0,11))
labels = axP[0].get_yticklabels() + axP[1].get_yticklabels() + axP[2].get_yticklabels() + axP[0].get_xticklabels() + axP[1].get_xticklabels() + axP[2].get_xticklabels()
[label.set_fontsize(xtick_size) for label in labels]
[label.set_fontname('Arial') for label in labels]
axP[0].set_ylabel('Ionospheric errors (cm)',font_label)
axP[1].set_xlabel('Prediction duration (min)',font_label)
# axP[1][0].set_ylabel('Ionospheric errors (cm)',font_label)
# axP[2][0].set_xlabel('Prediction duration (min)',font_label)
# plt.savefig("/Users/hanjunjie/Desktop/Image-1/GER_DIFFERENT_ELESAT.jpg",dpi = 300)
plt.show()