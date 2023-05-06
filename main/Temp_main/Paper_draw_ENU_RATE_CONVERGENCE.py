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
font_title = {'family' : 'Times New Roman', 'weight' : 700, 'size' : 45}
font_label = {'family' : 'Times New Roman', 'weight' : 600, 'size' : 27}
font_tick = {'family' : 'Times New Roman', 'weight' : 400, 'size' : 35}
font_legend = {'family' : 'Times New Roman', 'weight' : 600, 'size' : 30}
# font_legend = {'family' : 'Times New Roman', 'weight' : 600, 'size' : 15}
font_text = {'family' : 'Times new roman','weight' : 500,'size'   : 28}
xtick_size = 25
color_list = sns.color_palette("Set1")

plt.figure(figsize=(14,9))
X_Inter = [-0.2,0.8,1.8]
X_Grid = [0.2,1.2,2.2]
W = 0.4
X_Tick = [0,1,2]
X_TickLable = ["Net. A","Net. B","Net. C"]
#E
axP = plt.subplot(2,3,1)
axP.set_ylim(0,5)
E_Inter = [1.56,1.58,3.13]
E_Grid = [1.34,1.03,2.20]
axP.bar(X_Inter,E_Inter,width=W,color = color_list[0])
axP.bar(X_Grid,E_Grid,width=W,color = color_list[1])
axP.set_xticks(X_Tick)
axP.set_xticklabels(X_TickLable)
labels = axP.get_yticklabels() + axP.get_xticklabels()
[label.set_fontsize(xtick_size) for label in labels]
[label.set_fontname('Times New Roman') for label in labels]
axP.set_ylabel("East Errors(cm)",font_label)
box = axP.get_position()
axP.set_position([box.x0 - 0.02279, box.y0, box.width, box.height])
#N
axP = plt.subplot(2,3,2)
axP.set_ylim(0,5)
E_Inter = [1.11,1.62,4.07]
E_Grid = [0.85,1.13,2.34]
axP.bar(X_Inter,E_Inter,width=W,color = color_list[0])
axP.bar(X_Grid,E_Grid,width=W,color = color_list[1])
axP.set_xticks(X_Tick)
axP.set_xticklabels(X_TickLable)
labels = axP.get_yticklabels() + axP.get_xticklabels()
[label.set_fontsize(xtick_size) for label in labels]
[label.set_fontname('Times New Roman') for label in labels]
axP.set_ylabel("North Errors(cm)",font_label)
box = axP.get_position()
axP.set_position([box.x0 + 0.02279, box.y0, box.width, box.height])
#U
axP = plt.subplot(2,3,3)
axP.set_ylim(0,14)
E_Inter = [6.34,11.03,12.85]
E_Grid = [3.90,4.62,8.87]
axP.bar(X_Inter,E_Inter,width=W,color = color_list[0])
axP.bar(X_Grid,E_Grid,width=W,color = color_list[1])
axP.set_xticks(X_Tick)
axP.set_xticklabels(X_TickLable)
labels = axP.get_yticklabels() + axP.get_xticklabels()
[label.set_fontsize(xtick_size) for label in labels]
[label.set_fontname('Times New Roman') for label in labels]
axP.set_ylabel("Up Errors(cm)",font_label)
axP.legend(["Interpolation","Grid"],prop=font_legend,
            framealpha=1,facecolor='w',ncol=2,numpoints=5, markerscale=5, 
            bbox_to_anchor=(1,1.31),loc=1,borderaxespad=0)
box = axP.get_position()
axP.set_position([box.x0 + 0.02279 * 3,box.y0, box.width, box.height])
#Fixing Rate
axP = plt.subplot(2,3,4)
axP.set_ylim(80,100)
E_Inter = [93.06,92.19,84.12]
E_Grid = [96.77,94.42,91.03]
axP.bar(X_Inter,E_Inter,width=W,color = color_list[0])
axP.bar(X_Grid,E_Grid,width=W,color = color_list[1])
axP.set_xticks(X_Tick)
axP.set_xticklabels(X_TickLable)
axP.set_yticks([80,85,90,95,100])
axP.set_yticklabels(["80%","85%","90%","95%","100%"])
labels = axP.get_yticklabels() + axP.get_xticklabels()
[label.set_fontsize(xtick_size) for label in labels]
[label.set_fontname('Times New Roman') for label in labels]
axP.set_ylabel("Fixing Rate",font_label)
box = axP.get_position()
axP.set_position([box.x0 - 0.02279, box.y0, box.width, box.height])
#Horizonal
# axP = plt.subplot(3,3,5)
# axP.set_ylim(67,100)
# E_Inter = [98.51,96.63,78.44]
# E_Grid = [99.54,99.20,89.80]
# axP.bar(X_Inter,E_Inter,width=W,color = color_list[0])
# axP.bar(X_Grid,E_Grid,width=W,color = color_list[1])
# axP.set_xticks(X_Tick)
# axP.set_xticklabels(X_TickLable)
# labels = axP.get_yticklabels() + axP.get_xticklabels()
# axP.set_yticks([70,80,90,100])
# axP.set_yticklabels(["70%","80%","90%","100%"])
# [label.set_fontsize(xtick_size) for label in labels]
# [label.set_fontname('Times New Roman') for label in labels]
# axP.set_ylabel("Horizontal <5cm",font_label)
# box = axP.get_position()
# axP.set_position([box.x0, box.y0, box.width*0.9, box.height])
# #Vertical
# axP = plt.subplot(3,3,6)
# axP.set_ylim(67,100)
# E_Inter = [95.38,80.20,69.21]
# E_Grid = [97.89,96.16,80.86]
# axP.bar(X_Inter,E_Inter,width=W,color = color_list[0])
# axP.bar(X_Grid,E_Grid,width=W,color = color_list[1])
# axP.set_xticks(X_Tick)
# axP.set_xticklabels(X_TickLable)
# axP.set_yticks([70,80,90,100])
# axP.set_yticklabels(["70%","80%","90%","100%"])
# labels = axP.get_yticklabels() + axP.get_xticklabels()
# [label.set_fontsize(xtick_size) for label in labels]
# [label.set_fontname('Times New Roman') for label in labels]
# axP.set_ylabel("Vertical <10cm",font_label)
# box = axP.get_position()
# axP.set_position([box.x0 + box.width*0.1, box.y0, box.width*0.9, box.height])
#Horizontal Convergence
axP = plt.subplot(2,3,5)
axP.set_ylim(0,45)
E_Inter = [5.44,13.69,44.43]
E_Grid = [0.40,0.61,24.88]
axP.bar(X_Inter,E_Inter,width=W,color = color_list[0])
axP.bar(X_Grid,E_Grid,width=W,color = color_list[1])
axP.set_xticks(X_Tick)
axP.set_xticklabels(X_TickLable)
# axP.set_yticks([80,85,90,95,100])
# axP.set_yticklabels(["80%","85%","90%","95%","100%"])
labels = axP.get_yticklabels() + axP.get_xticklabels()
[label.set_fontsize(xtick_size) for label in labels]
[label.set_fontname('Times New Roman') for label in labels]
axP.set_ylabel("Horizontal\nConvergence Time(s)",font_label)
box = axP.get_position()
axP.set_position([box.x0 + 0.02279, box.y0, box.width, box.height])
#Horizontal Convergence
axP = plt.subplot(2,3,6)
axP.set_ylim(15,80)
E_Inter = [50.31,69.93,77.85]
E_Grid = [16.28,49.45,64.88]
axP.bar(X_Inter,E_Inter,width=W,color = color_list[0])
axP.bar(X_Grid,E_Grid,width=W,color = color_list[1])
axP.set_xticks(X_Tick)
axP.set_xticklabels(X_TickLable)
# axP.set_yticks([80,85,90,95,100])
# axP.set_yticklabels(["80%","85%","90%","95%","100%"])
labels = axP.get_yticklabels() + axP.get_xticklabels()
[label.set_fontsize(xtick_size) for label in labels]
[label.set_fontname('Times New Roman') for label in labels]
axP.set_ylabel("Vertical\nConvergence Time(s)",font_label)
box = axP.get_position()
axP.set_position([box.x0 + 0.02279 * 3, box.y0 , box.width, box.height])
plt.savefig(r"E:\1Master_2\Paper_Grid\1-Paper_word\Image-3\2-3-ENU-Fix-Convergence.png",dpi=600)
plt.savefig(r"E:\1Master_2\Paper_Grid\1-Paper_word\Image-3\2-3-ENU-Fix-Convergence.svg")  
plt.show()