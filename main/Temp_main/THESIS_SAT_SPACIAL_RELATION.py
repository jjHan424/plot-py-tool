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
from scipy.stats import pearsonr

font_title = {'family' : 'Arial', 'weight' : 300, 'size' : 25}
font_label = {'family' : 'Arial', 'weight' : 300, 'size' : 25}
font_tick = {'family' : 'Arial', 'weight' : 300, 'size' : 25}
font_legend = {'family' : 'Arial', 'weight' : 300, 'size' : 25}
font_text = {'family' : 'Arial','weight' : 300,'size'   : 25}
xtick_size = 25
color_list = sns.color_palette("Set1")
color_list = ["#0099E5","#34BF49","#FF4C4C"]
site_site = ["EIJS","EUSK"]
# site_site = [["TIT2","EUSK"],
#              ["WARE","EIJS"],
#              ["BADH","FFMJ"],
#              ["BADH","KLOP"],
#              ["FFMJ","KLOP"]]
site_site = [
             ["BADH","KLOP","8.62 km"],["WARE","EIJS","31.87 km"],["WARE","BRUX","63.73 km"]
            
             
             ]
mode_list = []
data_plot = {}
for cur_site_pair in site_site:
    path_I = r"/Users/hanjunjie/Master_3/1-IUGG/AUG2GRID/2021311/EPNBIG-R-C-CROSS/{}-GEC3-30.diff".format(cur_site_pair[0])
    path_S = r"/Users/hanjunjie/Master_3/1-IUGG/AUG2GRID/2021311/EPNBIG-R-C-CROSS/{}-GEC3-30.diff".format(cur_site_pair[1])
    [head_I,data1] = rf.open_aug_file_new(path_I)
    [head_S,data2] = rf.open_aug_file_new(path_S)
    # cur_mode = "{}-{} ({})".format(cur_site_pair[0],cur_site_pair[1],cur_site_pair[2])
    cur_mode = "{}".format(cur_site_pair[2])
    mode_list.append(cur_mode)
    out_put_sys_sat = ["G22","E04","C12"]
    plot_type = "dION1"
    #Dataconvert
    if cur_mode not in data_plot.keys():
        data_plot[cur_mode] = {}
    for cur_time in data1.keys():
        if cur_time not in data2.keys():
            continue
        for cur_sat in data1[cur_time].keys():
            if cur_sat not in data2[cur_time].keys():
                continue
            if cur_sat in out_put_sys_sat or cur_sat[0] in out_put_sys_sat:
                if plot_type not in data1[cur_time][cur_sat].keys():
                    continue
                if data1[cur_time][cur_sat][plot_type] == 0.0 or data2[cur_time][cur_sat][plot_type] == 0.0:
                    continue
                if cur_sat not in data_plot[cur_mode].keys():
                    data_plot[cur_mode][cur_sat] = {}
                    data_plot[cur_mode][cur_sat]["X"],data_plot[cur_mode][cur_sat]["Y"] = [],[]
                data_plot[cur_mode][cur_sat]['X'].append((data1[cur_time][cur_sat][plot_type]*100))
                data_plot[cur_mode][cur_sat]['Y'].append((data2[cur_time][cur_sat][plot_type]*100))

    #Plot
mean_Coef = {}
diff_res = {}
figP,axP = plt.subplots(1,3,figsize=(15,5),sharey=True,sharex=False)
sys_axP = {"G":0,"E":1,"C":2}
j=-1
for cur_mode in data_plot.keys():
    j=j+1
    for cur_sat in  data_plot[cur_mode].keys():
        if cur_sat[0] not in mean_Coef.keys():
            mean_Coef[cur_sat[0]],diff_res[cur_sat[0]] = [],[]
        axP[sys_axP[cur_sat[0]]].set_xlabel("IONO errors (cm)",font_label)
        axP[sys_axP["G"]].set_ylabel("IONO errors (cm)",font_label)
        axP[sys_axP[cur_sat[0]]].scatter( data_plot[cur_mode][cur_sat]['X'], data_plot[cur_mode][cur_sat]['Y'],s=7,color = color_list[j%3])
        ylim_max = np.max([np.max(data_plot[cur_mode][cur_sat]['X']),np.max(data_plot[cur_mode][cur_sat]['Y'])])
        ylim_min = np.min([np.min(data_plot[cur_mode][cur_sat]['X']),np.min(data_plot[cur_mode][cur_sat]['Y'])])
        axP[sys_axP[cur_sat[0]]].set_ylim(0,10)
        axP[sys_axP[cur_sat[0]]].set_xlim(0,10)
        # corr_coef,p_value = pearsonr(np.array(data_plot[cur_sat]['X']),np.array(data_plot[cur_sat]['Y']))
        corr_coef = np.mean(np.array(data_plot[cur_mode][cur_sat]['X']) / np.array(data_plot[cur_mode][cur_sat]['Y']))
        mean_Coef[cur_sat[0]].append(corr_coef)
        temp = dp.rms(np.array(data_plot[cur_mode][cur_sat]['X']) - np.array(data_plot[cur_mode][cur_sat]['Y']))
        diff_res[cur_sat[0]].append(temp)
        axP[sys_axP[cur_sat[0]]].set_title("{}".format(cur_sat),font_title)
        labels = axP[sys_axP[cur_sat[0]]].get_yticklabels() + axP[sys_axP[cur_sat[0]]].get_xticklabels()
        [label.set_fontsize(xtick_size) for label in labels]
        [label.set_fontname('Arial') for label in labels]
axP[2].legend(mode_list,prop=font_legend,
        framealpha=1,facecolor='w',numpoints=5, markerscale=6, frameon=False,ncol = 1,
        loc=0,borderaxespad=0)
for i in range(3):
    box = axP[i].get_position()
    axP[i].set_position([box.x0, box.y0,0.24, 0.72])
plt.savefig("/Users/hanjunjie/Desktop/Image-1/Diff_Relationship.jpg",dpi = 300)
plt.show()
plt.close()
    # for cur_sys in mean_Coef.keys():
    #     print("{} = {:.4f}, {:.4f} cm".format(cur_sys,np.mean(mean_Coef[cur_sys]),np.mean(diff_res[cur_sys])))
    # print("{}-{} {:.4f} {:.4f} {:.4f} {:.4f} {:.4f} {:.4f}".format(cur_site_pair[0],cur_site_pair[1],np.mean(mean_Coef["G"]),np.mean(mean_Coef["E"]),np.mean(mean_Coef["C"]),np.mean(diff_res["G"]),np.mean(diff_res["E"]),np.mean(diff_res["C"])))
