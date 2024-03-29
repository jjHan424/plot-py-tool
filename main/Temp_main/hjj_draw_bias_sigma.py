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
font_title = {'family' : 'Arial', 'weight' : 300, 'size' : 35}
font_label = {'family' : 'Arial', 'weight' : 300, 'size' : 6}
font_tick = {'family' : 'Arial', 'weight' : 300, 'size' : 6}
font_legend = {'family' : 'Arial', 'weight' : 300, 'size' : 5}
# font_legend = {'family' : 'Times New Roman', 'weight' : 600, 'size' : 15}
font_text = {'family' : 'Arial','weight' : 300,'size'   : 28}
xtick_size = 5

path = "/Users/hanjunjie/Master_3/1-IUGG/AUG2GRID/2021311/HK_MINSIGMA.log"
data_plot,time_plot,data_sys = {},{},{}
ref_site = "HKLM"
# start_time,end_time = 23 + 22/60, 23 + 25/60
start_time,end_time = 2, 24
with open(path) as f:
    for line in f:
        value = line.split()
        if (value[0] == "SAT"):
            cur_site = (value[5].split("-"))[0]
            if cur_site!=ref_site:
                continue
            year,month,day = int(value[3].split("-")[0]),int(value[3].split("-")[1]),int(value[3].split("-")[2])
            hour,minute,second = int(value[4].split(":")[0]),int(value[4].split(":")[1]),int(value[4].split(":")[2][0:2])
            hourinday = hour+minute/60+second/3600
            if (hourinday < start_time):
                continue
            if (hourinday > end_time):
                break
            cur_site = (value[5].split("-"))[1]
            if cur_site not in data_plot.keys():
                data_plot[cur_site],time_plot[cur_site] = {},{}
            if value[6] not in data_plot[cur_site].keys():
                data_plot[cur_site][value[6]],time_plot[cur_site][value[6]] = [],[]
            if hourinday not in data_sys.keys():
                data_sys[hourinday] = {}
            if value[6][0] not in data_sys[hourinday].keys():
                data_sys[hourinday][value[6][0]] = []
            if (float(value[7]) > 0.35):
                continue
            data_sys[hourinday][value[6][0]].append(float(value[7]))
            data_plot[cur_site][value[6]].append(float(value[7]))
            time_plot[cur_site][value[6]].append(hourinday)
barplot_data = {}
for cur_time in data_sys.keys():
    for cur_sys in data_sys[cur_time].keys():
        if cur_sys not in barplot_data.keys():
            barplot_data[cur_sys] = []
        data_temp = data_sys[cur_time][cur_sys]
        data_temp.sort()
        data_sort = data_temp
        up,low = int(len(data_sort) * 0.75),int(len(data_sort) * 0.25)
        witdth = data_sort[up] - data_sort[low]
        up_limit = witdth*4 + data_sort[up]
        # if (data_sort[-1] > up_limit):
        #     print("{},{}".format(cur_sys,cur_time*3600))
        barplot_data[cur_sys].append(data_temp)


figP,axP = plt.subplots(3,1,figsize=(17,8),sharey=False,sharex=True)
axP_index = {"G":0,"E":1,"C":2}
for cur_site in data_plot.keys():
    for cur_sat in data_plot[cur_site].keys():
        axP[axP_index[cur_sat[0]]].scatter(time_plot[cur_site][cur_sat],data_plot[cur_site][cur_sat],s=3)
# for cur_sys in barplot_data.keys():
#     axP[axP_index[cur_sys]].boxplot(barplot_data[cur_sys])
plt.show()
