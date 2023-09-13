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
plt.style.use(['science','no-latex'])
import dataprocess as dp
import draw as dr
import seaborn as sns
import trans as tr
import glv as glv
import seaborn as sns

font_title = {'family' : 'Times New Roman', 'weight' : 700, 'size' : 30}
font_label = {'family' : 'Times New Roman', 'weight' : 600, 'size' : 38}
font_tick = {'family' : 'Times New Roman', 'weight' : 400, 'size' : 30}
font_legend = {'family' : 'Times New Roman', 'weight' : 600, 'size' : 22}
font_text = {'family' : 'Times new roman','weight' : 600,'size'   : 20}
xtick_size = 35
color_list = sns.color_palette("Set1")

#Diff-ROTI  "Scatter plot and polynomial fit of water vapor density with altitude (upper for 45,004, middle for 59,280, and lower for 59,316, respectively)."
# abc = [0.05474,0.07856,-0.111289]
# filename = r"E:\1Master_2\Paper_Grid\Res_FromServer_New\Fig\Ele_Wgt-New\Roti.txt"
# Diff,Roti = [],[]
# with open(filename,'rt') as f:
#     for line in f:
#         value = line.split()
#         Diff.append(float(value[4]))
#         Roti.append(float(value[6]))

# figP,axP = plt.subplots(1,1,figsize=(13,8),sharey=True,sharex=True)

# axP.scatter(Roti,Diff,s=40,c="black")
# x=np.linspace(0.95,1.75,1000)
# y=abc[0]*x*x + abc[1]*x + abc[2]
# axP.plot(x,y,linewidth=8.0,linestyle='--')
# font = {'family': 'Times new roman','weight': 600,'size': 23}
# # axP.legend(["Scatter","Polynomial Fit"],prop=font,
# # framealpha=1,facecolor='none',ncol=4,numpoints=5,markerscale=3, 
# #             borderaxespad=0,bbox_to_anchor=(1,1.085),loc=1)
# axP.set_xlim(0,2)
# axP.set_ylim(0,0.2)
# axP.set_xlabel("ROTI(TECU/min)",font_label)
# axP.set_xticks([0.25,0.50,0.75,1.00,1.25,1.50,1.75,2.00])
# axP.set_xticklabels(["0.25","0.50","0.75","1.00","1.25","1.50","1.75","2.00"])
# axP.set_ylabel("Ionospheric errors(m)",font_label)
# axP.set_yticks([0.000,0.025,0.050,0.075,0.100,0.125,0.150,0.175,0.200])
# axP.set_yticklabels(["0","0.025","0.050","0.075","0.100","0.125","0.150","0.175","0.200"])
# labels = axP.get_yticklabels() + axP.get_xticklabels()
# [label.set_fontsize(xtick_size) for label in labels]
# [label.set_fontname('Times New Roman') for label in labels]
# # plt.savefig(r"E:\1Master_2\Paper_Grid\1-Paper_word\Image-3\Errors-Roti-Polynomial.svg")
# # plt.savefig(r"E:\1Master_2\Paper_Grid\1-Paper_word\Image-3\Errors-Roti-Polynomial.png",dpi=600)
# plt.show()

#Diff-Ele
filename = r"E:\1Master_2\Paper_Grid\Res_FromServer_New\Fig\Ele_Wgt-New\diff-meanele.txt"
Diff,Ele = [],[]
ab=[0.0003479,0.004675]
with open(filename,'rt') as f:
    for line in f:
        value = line.split()
        if value[0] == "NaN":
            continue
        Diff.append(float(value[0]))
        Ele.append(float(value[1]))

figP,axP = plt.subplots(1,1,figsize=(13,8),sharey=True,sharex=True)

axP.scatter(Ele,Diff,s=40,c="black")
x=np.linspace(7,75,1000)
y=ab[0]/(np.sin(x*glv.deg) * np.sin(x*glv.deg)) + ab[1]
axP.plot(x,y,linewidth=8.0,linestyle='--')
font = {'family': 'Times new roman','weight': 600,'size': 23}
# axP.legend(["Scatter","Polynomial Fit"],prop=font,
# framealpha=1,facecolor='none',ncol=4,numpoints=5,markerscale=3, 
#             borderaxespad=0,bbox_to_anchor=(1,1.085),loc=1)
axP.set_ylim(0,0.030)
axP.set_xlim(5,75)
axP.set_xlabel("Elevation(deg)",font_label)
axP.set_xticks([5,15,25,35,45,55,65,75])
axP.set_xticklabels(["5","15","25","35","45","55","65","75"])
axP.set_ylabel("Ionospheric errors(m)",font_label)
axP.set_yticks([0.000,0.005,0.010,0.015,0.020,0.025,0.030])
axP.set_yticklabels(["0.000","0.005","0.010","0.015","0.020","0.025","0.030"])
labels = axP.get_yticklabels() + axP.get_xticklabels()
[label.set_fontsize(xtick_size) for label in labels]
[label.set_fontname('Times New Roman') for label in labels]
# plt.savefig(r"E:\1Master_2\Paper_Grid\1-Paper_word\Image-3\Errors-Ele-Polynomial.svg")
# plt.savefig(r"E:\1Master_2\Paper_Grid\1-Paper_word\Image-3\Errors-Ele-Polynomial.png",dpi=600)
plt.show()