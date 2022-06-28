'''
Author: HanJunjie HanJunjie@whu.edu.cn
Date: 2022-06-22 23:09:27
LastEditors: HanJunjie HanJunjie@whu.edu.cn
LastEditTime: 2022-06-23 19:08:06
FilePath: /plot-py-tool/main/draw_arinf.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
from ipaddress import collapse_addresses
import os
import sys
from turtle import color
sys.path.insert(0,os.path.dirname(__file__)+'/..')
import numpy as np
import readfile as rf
import matplotlib as mpl
mpl.use("TkAgg")
import matplotlib.pyplot as plt
import dataprocess as dp
import draw as dr

[time,data] = rf.open_arinf_rtpppfile("/Volumes/H_GREAT/2Project/Allystar/20220622_WH2_ZHD/N004_20220623_SGG_CLK06_S_GEC.arinf",sat="G05")
figP,axP = plt.subplots(1,1,figsize=(12,10),sharey=False,sharex=True)
data_plot = []
for i in range(len(data)-1):
    data_plot.append(data[i+1]-data[i])
axP.scatter(time[1:len(time)],data_plot,s=20,color="blue")


[time1,data1] = rf.open_arinf_rtpppfile("/Volumes/H_GREAT/2Project/Allystar/20220622_WH2_ZHD/N004_20220623_SGG_CLK06_S_GEC.arinf",sat="G11")
data_plot = []
for i in range(len(data1)-1):
    data_plot.append(data1[i+1]-data1[i])
axP.scatter(time1[1:len(time1)],data_plot,s=5,color="green")
plt.show()