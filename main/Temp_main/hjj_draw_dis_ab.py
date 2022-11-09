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

area = "HK"
filename = r"E:\1Master_2\Paper_Grid\Res_FromServer_New\Fig\Ele_Wgt-New\HongKong-0.8-30.txt"
dis = {}
coff = {}
site_list = []
a_G,b_G,a_E,b_E,a_C,b_C,r_G,r_E,r_C=[],[],[],[],[],[],[],[],[]
with open(filename,'rt') as f:
    for line in f:
        value = line.split()
        if len(value) > 5:
            if (value[0] not in coff.keys()):
                coff[value[0]]=[]
            site_list.append(value[0])
            a_G.append(float(value[1]))
            b_G.append(float(value[2]))
            r_G.append(float(value[3]))
            a_E.append(float(value[4]))
            b_E.append(float(value[5]))
            r_E.append(float(value[6]))
            a_C.append(float(value[7]))
            b_C.append(float(value[8]))
            r_C.append(float(value[9]))
            coff[value[0]].append(float(value[1]))
            coff[value[0]].append(float(value[2]))
            coff[value[0]].append(float(value[4]))
            coff[value[0]].append(float(value[5]))
            coff[value[0]].append(float(value[7]))
            coff[value[0]].append(float(value[8]))
        if 0<len(value) <= 5:
            dis[value[0]] = float(value[2])
dis_plot=[]
for cur_site in site_list:
    dis_plot.append(dis[cur_site])
figP,axP = plt.subplots(4,1,figsize=(14,9.3),sharey=False,sharex=True)
W=0.8/3
x = []
for j in range(len(site_list)):
    x.append(j-W)
axP[0].bar(x,a_G,width = W,label='value')
axP[1].bar(x,b_G,width = W,label='value')
axP[2].bar(x,r_G,width = W,label='value')

for j in range(len(site_list)):
    x[j] = x[j] + W
axP[0].bar(x,a_E,width = W,label='value')
axP[1].bar(x,b_E,width = W,label='value')
axP[2].bar(x,r_E,width = W,label='value')
axP[3].bar(x,dis_plot,width = W,label='value')

for j in range(len(site_list)):
    x[j] = x[j] + W
axP[0].bar(x,a_C,width = W,label='value')
axP[1].bar(x,b_C,width = W,label='value')
axP[2].bar(x,r_C,width = W,label='value')



x = []
for j in range(len(site_list)):
    x.append(j)
font_text = {'family' : 'Times new roman','weight' : 300,'size'   : 12}
axP[0].legend(["G","E","C"],prop=font_text,ncol=3,loc=1)
axP[0].set_xticks(x)
axP[0].set_xticklabels(site_list)
axP[1].set_xticks(x)
axP[1].set_xticklabels(site_list)
axP[2].set_xticks(x)
axP[2].set_xticklabels(site_list)


plt.show()


