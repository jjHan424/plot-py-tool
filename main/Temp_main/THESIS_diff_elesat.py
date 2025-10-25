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
import glv as glv
import seaborn as sns

font_title = {'family' : 'Arial', 'weight' : 300, 'size' : 30}
font_label = {'family' : 'Arial', 'weight' : 300, 'size' : 20}
font_tick = {'family' : 'Arial', 'weight' : 300, 'size' : 30}
font_legend = {'family' : 'Arial', 'weight' : 300, 'size' : 20}
font_text = {'family' : 'Times new roman','weight' : 300,'size'   : 20}
xtick_size = 15
color_list = sns.color_palette("Set1")

#Diff-EleSun
file_list = ["/Users/hanjunjie/Master_3/1-IUGG/ResFromServer/PLOT_EPN_ELE_IONO.txt"]
mode_list = ["Net. A","Net. B","Net. C"]
# filename = r"E:\1Master_2\Paper_Grid\Res_FromServer_New\Fig\Ele_Wgt-New\diff-meanele.txt"
Diff,Ele,Time,Time_ele = {},{},{},{}
abc=[-0.009162,0.001741,0.015485]
for i in range(len(file_list)):
    filename = file_list[i]
    if mode_list[i] not in Diff.keys():
        Diff[mode_list[i]],Ele[mode_list[i]],Time[mode_list[i]],Time_ele[mode_list[i]] = [],[],[],[]
    with open(filename,'rt') as f:
        for line in f:
            value = line.split()
            if value[0] == "NaN":
                continue
            Diff[mode_list[i]].append(float(value[1])*100)
            Ele[mode_list[i]].append(float(value[0]))

figP,axP = plt.subplots(1,1,figsize=(6,3.5),sharey=False,sharex=True,frameon = False)
i=0
x = np.array(Ele[mode_list[i]])*glv.deg
y = (abc[0]*np.sin(x)+abc[1]/np.sin(x)+abc[2])*100
axP.plot(Ele[mode_list[i]],y,linewidth=3.0,linestyle='--',c='k')
# axP.legend([r"$y = a \times \sin (x) + \frac{b}{{\sin (x)}} + c$"],prop = font_label)
axP.legend([r"$y = a \times \sin (x) + \frac{b}{{\sin (x)}} + c$"],prop=font_legend,
        framealpha=1,facecolor='w',numpoints=5, markerscale=3, frameon=False,
        borderaxespad=0)
leg = axP.get_legend()
for legobj in leg.legendHandles:
    legobj.set_linewidth(3)
    # legobj.set_linelength(10)
    # legobj.set_color("black")
axP.scatter(Ele[mode_list[i]],Diff[mode_list[i]],s=5,c="#0099E5")

# axP[2].set_ylim(0,1.2)
zz = axP.set_ylabel("Ionospheric errors (cm)",font_label,y=0.4)
labels = axP.get_yticklabels()+axP.get_xticklabels()
[label.set_fontsize(xtick_size) for label in labels]
[label.set_fontname('Arial') for label in labels]
axP.set_xlabel("Elevation of Satellite (deg)",font_label)
box = axP.get_position()
# axP.set_position([box.x0, box.y0+box.y0*0.03, box.width, box.height])
axP.set_position([box.x0, box.y0+box.height*0.15, box.width, box.height*0.85])
# plt.savefig("/Users/hanjunjie/Desktop/Image-1/Diff_VS_EleSat.jpg",dpi=300)
plt.show()