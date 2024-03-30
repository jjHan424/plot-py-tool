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

font_title = {'family' : 'Times New Roman', 'weight' : 700, 'size' : 30}
font_label = {'family' : 'Times New Roman', 'weight' : 600, 'size' : 25}
font_tick = {'family' : 'Times New Roman', 'weight' : 400, 'size' : 30}
font_legend = {'family' : 'Times New Roman', 'weight' : 600, 'size' : 22}
font_text = {'family' : 'Times new roman','weight' : 600,'size'   : 20}
xtick_size = 25
color_list = sns.color_palette("Set1")
site_site = ["EIJS","EUSK"]
# site_site = [["TIT2","EUSK"],
#              ["WARE","EIJS"],
#              ["BADH","FFMJ"],
#              ["BADH","KLOP"],
#              ["FFMJ","KLOP"]]
site_site = [
            #  ["DENT","BRUX"],
            #  ["WARE","BRUX"],
             ["FFMJ","KLOP"]
             ]
for cur_site_pair in site_site:
    path_I = r"/Users/hanjunjie/Master_3/1-IUGG/AUG2GRID/2021311/EPNBIG-R-C-CROSS/{}-GEC3-30.diff".format(cur_site_pair[0])
    path_S = r"/Users/hanjunjie/Master_3/1-IUGG/AUG2GRID/2021311/EPNBIG-R-C-CROSS/{}-GEC3-30.diff".format(cur_site_pair[1])
    [head_I,data1] = rf.open_aug_file_new(path_I)
    [head_S,data2] = rf.open_aug_file_new(path_S)

    out_put_sys_sat = ["G","E","C"]
    plot_type = "dION1"
    #Dataconvert
    data_plot = {}
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
                if cur_sat not in data_plot.keys():
                    data_plot[cur_sat] = {}
                    data_plot[cur_sat]["X"],data_plot[cur_sat]["Y"] = [],[]
                data_plot[cur_sat]['X'].append((data1[cur_time][cur_sat][plot_type]*100))
                data_plot[cur_sat]['Y'].append((data2[cur_time][cur_sat][plot_type]*100))

    #Plot
    mean_Coef = {}
    diff_res = {}
    for cur_sat in data_plot.keys():
        if cur_sat[0] not in mean_Coef.keys():
            mean_Coef[cur_sat[0]],diff_res[cur_sat[0]] = [],[]
        figP,axP = plt.subplots(1,1,figsize=(10,10),sharey=True,sharex=True)
        axP.set_xlabel("{} Reduals (cm)".format(cur_site_pair[0]),font_label)
        axP.set_ylabel("{} Reduals (cm)".format(cur_site_pair[1]),font_label)
        axP.scatter(data_plot[cur_sat]['X'],data_plot[cur_sat]['Y'])
        ylim_max = np.max([np.max(data_plot[cur_sat]['X']),np.max(data_plot[cur_sat]['Y'])])
        ylim_min = np.min([np.min(data_plot[cur_sat]['X']),np.min(data_plot[cur_sat]['Y'])])
        axP.set_ylim(ylim_min,ylim_max)
        axP.set_xlim(ylim_min,ylim_max)
        # corr_coef,p_value = pearsonr(np.array(data_plot[cur_sat]['X']),np.array(data_plot[cur_sat]['Y']))
        corr_coef = np.mean(np.array(data_plot[cur_sat]['X']) / np.array(data_plot[cur_sat]['Y']))
        mean_Coef[cur_sat[0]].append(corr_coef)
        temp = dp.rms(np.array(data_plot[cur_sat]['X']) - np.array(data_plot[cur_sat]['Y']))
        diff_res[cur_sat[0]].append(temp)
        axP.set_title("{} Pearson = {:.2f} diff-rms = {:.2f} cm".format(cur_sat,corr_coef,temp),font_title)
        labels = axP.get_yticklabels() + axP.get_xticklabels()
        [label.set_fontsize(xtick_size) for label in labels]
        [label.set_fontname('Arial') for label in labels]
        # plt.show()
        plt.savefig("/Users/hanjunjie/Desktop/Image-1/Site_Site_Aug/{}-{}-{}.jpg".format(cur_site_pair[0],cur_site_pair[1],cur_sat))
        plt.close()
    # for cur_sys in mean_Coef.keys():
    #     print("{} = {:.4f}, {:.4f} cm".format(cur_sys,np.mean(mean_Coef[cur_sys]),np.mean(diff_res[cur_sys])))
    print("{}-{} {:.4f} {:.4f} {:.4f} {:.4f} {:.4f} {:.4f}".format(cur_site_pair[0],cur_site_pair[1],np.mean(mean_Coef["G"]),np.mean(mean_Coef["E"]),np.mean(mean_Coef["C"]),np.mean(diff_res["G"]),np.mean(diff_res["E"]),np.mean(diff_res["C"])))
