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

site_list = ["WUDA","WHYJ","HKSC","HKMW","HKTK"]
site_list_plot = ["WUDA","WHYJ","HKSC","HKMW","HKTK"]
Site = "WUDA"
Direct = r"E:\1Master_2\Paper_Grid\Res_FromServer_New\Fig\Pos4-New-3"

site_num = len(site_list)

data_save = {}
for i in range(site_num):
    cur_site = site_list[i]
    file_path = Direct + "\\" + cur_site + "-Sigma-0.txt"
    if cur_site not in data_save.keys():
        data_save[cur_site] = {}
    data_save[cur_site]["MLCM"] = rf.H_open_rms(file_path,1)
    data_save[cur_site]["Grid"] = rf.H_open_rms(file_path,2)
    data_save[cur_site]["Grid-Chk"] = rf.H_open_rms(file_path,3)
    data_save[cur_site]["Grid-Ele"] = rf.H_open_rms(file_path,4)

#===========Day============#
for Site in site_list_plot:
    if Site not in data_save.keys():
        print("No Data")
    else:
        cur_site = Site
        W=0.2
        figP,axP = plt.subplots(4,1,figsize=(14,9.3),sharey=False,sharex=True)
        mode_list = []
        imode = -1
        for mode in data_save[cur_site].keys():
            X_all = list(range(len(data_save[cur_site][mode].keys())))
            mode_list.append(mode)
            barplot_data_E = []
            barplot_data_N = []
            barplot_data_U = []
            barplot_data_3D = []
            barplot_name = []
            x = []
            j=0
            for cdoy in data_save[cur_site][mode]:
                barplot_data_E.append(data_save[cur_site][mode][cdoy]["E"])
                barplot_data_N.append(data_save[cur_site][mode][cdoy]["N"])
                barplot_data_U.append(data_save[cur_site][mode][cdoy]["U"])
                barplot_data_3D.append(math.sqrt(math.pow(data_save[cur_site][mode][cdoy]["E"],2)+math.pow(data_save[cur_site][mode][cdoy]["N"],2)+math.pow(data_save[cur_site][mode][cdoy]["U"],2)))
                barplot_name.append(cdoy)
                x.append(X_all[j])
                j=j+1
            for j in range(len(x)):
                x[j] = x[j] + W*imode - W/2
            imode = imode + 1
            
            axP[0].bar(x,barplot_data_E,width = 0.2,label='value')
            axP[1].bar(x,barplot_data_N,width = 0.2,label='value')
            axP[2].bar(x,barplot_data_U,width = 0.2,label='value')
            axP[3].bar(x,barplot_data_3D,width = 0.2,label='value')
            
        num_mode = len(mode_list)
        font_text = {'family' : 'Times new roman','weight' : 300,'size'   : 12}
        axP[3].set_xticks(X_all)
        axP[3].set_xticklabels(barplot_name)
        axP[0].legend(mode_list,prop=font_text,ncol=4,bbox_to_anchor=(1,1.32),loc=1)
        font_text = {'family' : 'Times new roman','weight' : 300,'size'   : 20}
        axP[3].set_xlabel("Day of Year",font_text)
        axP[0].set_ylabel("E(cm)",font_text)
        axP[1].set_ylabel("N(cm)",font_text)
        axP[2].set_ylabel("U(cm)",font_text)
        axP[3].set_ylabel("3D(cm)",font_text)
        # axP[0].set_ylim(0,10)
        # axP[1].set_ylim(0,10)
        # axP[2].set_ylim(0,20)
        font_text = {'family' : 'Times new roman','weight' : 500,'size'   : 25}
        axP[0].set_title(Site+"-RMS",font_text)
        plt.show()

#===========Site============#
# figP,axP = plt.subplots(4,1,figsize=(15,9.5),sharey=False,sharex=True)
# for Site in site_list_plot:
#     if Site not in data_save.keys():
#         print("No Data")
#     else:
#         cur_site = Site
#         W=0.2
#         mode_list = []
#         imode = -1
#     for mode in data_save[cur_site].keys():
#         barplot_data_E = []
#         barplot_data_N = []
#         barplot_data_U = []
#         barplot_data_3D = []
#         barplot_name = []
#         x = []
#         j=0
#         for cdoy in data_save[cur_site][mode]:
#             barplot_data_E.append(data_save[cur_site][mode][cdoy]["E"])
#             barplot_data_N.append(data_save[cur_site][mode][cdoy]["N"])
#             barplot_data_U.append(data_save[cur_site][mode][cdoy]["U"])
#         data_save[cur_site][mode]["mean"] = {}
#         data_save[cur_site][mode]["mean"]["E"] = np.mean(barplot_data_E)
#         data_save[cur_site][mode]["mean"]["N"] = np.mean(barplot_data_N)
#         data_save[cur_site][mode]["mean"]["U"] = np.mean(barplot_data_U)
        
# site_list = []
# imode = -1
# for mode in data_save[site_list_plot[0]].keys():
#     X_all = list(range(len(data_save.keys())))
#     mode_list.append(mode)
#     barplot_data_E = []
#     barplot_data_N = []
#     barplot_data_U = []
#     barplot_data_3D = []
#     barplot_name = []
#     x = []
#     j=0
#     W=0.2
#     for site in data_save.keys():
#         cur_site = site
#         barplot_data_E.append(data_save[cur_site][mode]["mean"]["E"])
#         barplot_data_N.append(data_save[cur_site][mode]["mean"]["N"])
#         barplot_data_U.append(data_save[cur_site][mode]["mean"]["U"])
#         barplot_data_3D.append(math.sqrt(math.pow(data_save[cur_site][mode]["mean"]["E"],2)+math.pow(data_save[cur_site][mode]["mean"]["N"],2)+math.pow(data_save[cur_site][mode]["mean"]["U"],2)))
#         barplot_name.append(site)
#         x.append(X_all[j])
#         j=j+1
#     for j in range(len(x)):
#         x[j] = x[j] + W*imode - W/2
#     imode = imode + 1

#     axP[0].bar(x,barplot_data_E,width = 0.2,label='value')
#     axP[1].bar(x,barplot_data_N,width = 0.2,label='value')
#     axP[2].bar(x,barplot_data_U,width = 0.2,label='value')
#     axP[3].bar(x,barplot_data_3D,width = 0.2,label='value')
    

# font_text = {'family' : 'Times new roman','weight' : 300,'size'   : 15}
# axP[3].set_xticks(X_all)
# axP[3].set_xticklabels(barplot_name)
# axP[0].legend(mode_list,prop=font_text,ncol=4,bbox_to_anchor=(1,1.32),loc=1)
# font_text = {'family' : 'Times new roman','weight' : 300,'size'   : 20}
# axP[3].set_xlabel("Site",font_text)
# axP[0].set_ylabel("E(cm)",font_text)
# axP[1].set_ylabel("N(cm)",font_text)
# axP[2].set_ylabel("U(cm)",font_text)
# axP[3].set_ylabel("3D(cm)",font_text)
# # axP[0].set_ylim(0,10)
# # axP[1].set_ylim(0,10)
# # axP[2].set_ylim(0,20)
# font_text = {'family' : 'Times new roman','weight' : 500,'size'   : 25}
# axP[0].set_title("RMS",font_text)
# plt.show()
    

