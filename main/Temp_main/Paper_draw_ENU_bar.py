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

# site_list = ["WUDA","WHYJ","N028","HKSC","HKMW","HKTK"]
site_list = ["WUDA","WHYJ","HKSC","HKMW","HKTK"]
site_list_plot = site_list

com_mode = "MLCM"
Site = "WUDA"
Direct7 = r"E:\1Master_2\Paper_Grid\Res_FromServer_New\Fig\Pos4-New-7_Sigma"
Direct8 = r"E:\1Master_2\Paper_Grid\Res_FromServer_New\Fig\Pos4-New-8_Sigma"
Direct9 = r"E:\1Master_2\Paper_Grid\Res_FromServer_New\Fig\Pos4-New-9_Sigma"
Direct10 = r"E:\1Master_2\Paper_Grid\Res_FromServer_New\Fig\Pos4-New-10_Sigma"
Direct11 = r"E:\1Master_2\Paper_Grid\Res_FromServer_New\Fig\Pos4-New-11_Sigma"

site_num = len(site_list)

data_save = {}
for i in range(site_num):
    cur_site = site_list[i]
    # file_path = Direct1 + "\\" + cur_site + "-Sigma-1.txt"
    if cur_site not in data_save.keys():
        data_save[cur_site] = {}
    data_save[cur_site]["MLCM"] = rf.H_open_rms(Direct7 + "\\" + cur_site + "-Sigma-1.txt",1)
    data_save[cur_site]["Grid"] = rf.H_open_rms(Direct7 + "\\" + cur_site + "-Sigma-1.txt",2)
    data_save[cur_site]["Grid-Chk"] = rf.H_open_rms(Direct7 + "\\" + cur_site + "-Sigma-1.txt",3)
    # data_save[cur_site]["Grid-Ele7"] = rf.H_open_rms(Direct7 + "\\" + cur_site + "-Sigma-1.txt",4)
    # data_save[cur_site]["Grid-Ele8"] = rf.H_open_rms(Direct8 + "\\" + cur_site + "-Sigma-1.txt",4)
    # data_save[cur_site]["Grid-Ele9"] = rf.H_open_rms(Direct9 + "\\" + cur_site + "-Sigma-1.txt",4)
    # data_save[cur_site]["Grid-Ele10"] = rf.H_open_rms(Direct10 + "\\" + cur_site + "-Sigma-1.txt",4)
    # data_save[cur_site]["Grid-Ele11"] = rf.H_open_rms(Direct11 + "\\" + cur_site + "-Sigma-1.txt",4)

#===========Day============#
# for Site in site_list_plot:
#     if Site not in data_save.keys():
#         print("No Data")
#     else:
#         cur_site = Site
#         W=0.8/len(data_save[site_list_plot[0]].keys())
#         figP,axP = plt.subplots(4,1,figsize=(14,9.3),sharey=False,sharex=True)
#         mode_list = []
#         imode = 0
#         mode_num = len(data_save[cur_site].keys())
#         for mode in data_save[cur_site].keys():
#             compare_data_E,compare_data_N,compare_data_U,compare_data_3D=[],[],[],[]
#             if mode == com_mode:
#                 for cdoy in data_save[cur_site][mode]:
#                     compare_data_E.append(data_save[cur_site][mode][cdoy]["E"])
#                     compare_data_N.append(data_save[cur_site][mode][cdoy]["N"])
#                     compare_data_U.append(data_save[cur_site][mode][cdoy]["U"])
#                     compare_data_3D.append(math.sqrt(math.pow(data_save[cur_site][mode][cdoy]["E"],2)+math.pow(data_save[cur_site][mode][cdoy]["N"],2)+math.pow(data_save[cur_site][mode][cdoy]["U"],2)))
#                 compare_data_E = np.array(compare_data_E)
#                 compare_data_N = np.array(compare_data_N)
#                 compare_data_U = np.array(compare_data_U)
#                 compare_data_3D = np.array(compare_data_3D)
#                 break
#         for mode in data_save[cur_site].keys():
#             X_all = list(range(len(data_save[cur_site][mode].keys())))
#             mode_list.append(mode)
#             barplot_data_E,percent_E = [],[]
#             barplot_data_N,percent_N = [],[]
#             barplot_data_U,percent_U = [],[]
#             barplot_data_3D,percent_3D = [],[]
#             barplot_name = []
#             x = []
#             j=0
#             for cdoy in data_save[cur_site][mode]:
#                 barplot_data_E.append(data_save[cur_site][mode][cdoy]["E"])
#                 barplot_data_N.append(data_save[cur_site][mode][cdoy]["N"])
#                 barplot_data_U.append(data_save[cur_site][mode][cdoy]["U"])
#                 barplot_data_3D.append(math.sqrt(math.pow(data_save[cur_site][mode][cdoy]["E"],2)+math.pow(data_save[cur_site][mode][cdoy]["N"],2)+math.pow(data_save[cur_site][mode][cdoy]["U"],2)))
#                 barplot_name.append(cdoy)
#                 x.append(X_all[j])
#                 j=j+1
#             if mode != com_mode:
#                 percent_E=(compare_data_E-np.array(barplot_data_E))/compare_data_E *100
#                 percent_N=(compare_data_N-np.array(barplot_data_N))/compare_data_N*100
#                 percent_U=(compare_data_U-np.array(barplot_data_U))/compare_data_U*100
#                 percent_3D=(compare_data_3D-np.array(barplot_data_3D))/compare_data_3D*100
#             for j in range(len(x)):
#                 x[j] = x[j] + W*imode - W*(mode_num-1)/2
#             imode = imode + 1
#             font_text = {'family' : 'Times new roman','weight' : 300,'size'   : 10}
#             axP[0].bar(x,barplot_data_E,width = W,label='value')
#             axP[1].bar(x,barplot_data_N,width = W,label='value')
#             axP[2].bar(x,barplot_data_U,width = W,label='value')
#             axP[3].bar(x,barplot_data_3D,width = W,label='value')
#             if mode != com_mode:
#                 for i in range(len(x)):
#                     axP[0].text(x[i] - W/2,barplot_data_E[i],'{:.0f}%'.format(percent_E[i]),font_text)
#                     axP[1].text(x[i] - W/2,barplot_data_N[i],'{:.0f}%'.format(percent_N[i]),font_text)
#                     axP[2].text(x[i] - W/2,barplot_data_U[i],'{:.0f}%'.format(percent_U[i]),font_text)
#                     axP[3].text(x[i] - W/2,barplot_data_3D[i],'{:.0f}%'.format(percent_3D[i]),font_text)

#         num_mode = len(mode_list)
#         font_text = {'family' : 'Times new roman','weight' : 300,'size'   : 12}
#         axP[3].set_xticks(X_all)
#         axP[3].set_xticklabels(barplot_name)
#         axP[0].legend(mode_list,prop=font_text,ncol=2,bbox_to_anchor=(1,1.5),loc=1)
#         font_text = {'family' : 'Times new roman','weight' : 300,'size'   : 20}
#         axP[3].set_xlabel("Day of Year",font_text)
#         axP[0].set_ylabel("E(cm)",font_text)
#         axP[1].set_ylabel("N(cm)",font_text)
#         axP[2].set_ylabel("U(cm)",font_text)
#         axP[3].set_ylabel("3D(cm)",font_text)
#         # axP[0].set_ylim(0,10)
#         # axP[1].set_ylim(0,10)
#         # axP[2].set_ylim(0,20)
#         font_text = {'family' : 'Times new roman','weight' : 500,'size'   : 25}
#         axP[0].set_title(Site+"-RMS",font_text)
#         plt.show()

#===========Site============#
figP,axP = plt.subplots(4,1,figsize=(15,9.5),sharey=False,sharex=True)
for Site in site_list_plot:
    if Site not in data_save.keys():
        print("No Data")
    else:
        cur_site = Site
        W=0.2
        mode_list = []
        imode = -1
    
    for mode in data_save[cur_site].keys():
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
        data_save[cur_site][mode]["mean"] = {}
        data_save[cur_site][mode]["mean"]["E"] = np.mean(barplot_data_E)
        data_save[cur_site][mode]["mean"]["N"] = np.mean(barplot_data_N)
        data_save[cur_site][mode]["mean"]["U"] = np.mean(barplot_data_U)
        
site_list = []
imode = 0
mode_num = len(data_save[cur_site].keys())
for mode in data_save[cur_site].keys():
    compare_data_E,compare_data_N,compare_data_U,compare_data_3D=[],[],[],[]
    if mode == com_mode:
        for site in data_save.keys():
            cur_site = site
            compare_data_E.append(data_save[cur_site][mode]["mean"]["E"])
            compare_data_N.append(data_save[cur_site][mode]["mean"]["N"])
            compare_data_U.append(data_save[cur_site][mode]["mean"]["U"])
            compare_data_3D.append(math.sqrt(math.pow(data_save[cur_site][mode]["mean"]["E"],2)+math.pow(data_save[cur_site][mode]["mean"]["N"],2)+math.pow(data_save[cur_site][mode]["mean"]["U"],2)))
        compare_data_E = np.array(compare_data_E)
        compare_data_N = np.array(compare_data_N)
        compare_data_U = np.array(compare_data_U)
        compare_data_3D = np.array(compare_data_3D)
        break

for mode in data_save[site_list_plot[0]].keys():
    X_all = list(range(len(data_save.keys())))
    mode_list.append(mode)
    barplot_data_E = []
    barplot_data_N = []
    barplot_data_U = []
    barplot_data_3D = []
    barplot_name = []
    x = []
    j=0
    W=0.8/len(data_save[site_list_plot[0]].keys())
    for site in data_save.keys():
        cur_site = site
        barplot_data_E.append(data_save[cur_site][mode]["mean"]["E"])
        barplot_data_N.append(data_save[cur_site][mode]["mean"]["N"])
        barplot_data_U.append(data_save[cur_site][mode]["mean"]["U"])
        barplot_data_3D.append(math.sqrt(math.pow(data_save[cur_site][mode]["mean"]["E"],2)+math.pow(data_save[cur_site][mode]["mean"]["N"],2)+math.pow(data_save[cur_site][mode]["mean"]["U"],2)))
        barplot_name.append(site)
        x.append(X_all[j])
        j=j+1
    for j in range(len(x)):
        x[j] = x[j] + W*imode - W*(mode_num-1)/2
    imode = imode + 1
    if mode != com_mode:
        percent_E=(compare_data_E-np.array(barplot_data_E))/compare_data_E *100
        percent_N=(compare_data_N-np.array(barplot_data_N))/compare_data_N*100
        percent_U=(compare_data_U-np.array(barplot_data_U))/compare_data_U*100
        percent_3D=(compare_data_3D-np.array(barplot_data_3D))/compare_data_3D*100
    
    axP[0].bar(x,barplot_data_E,width = W,label='value')
    axP[1].bar(x,barplot_data_N,width = W,label='value')
    axP[2].bar(x,barplot_data_U,width = W,label='value')
    axP[3].bar(x,barplot_data_3D,width = W,label='value')
    font_text = {'family' : 'Times new roman','weight' : 300,'size'   : 10}
    if mode != com_mode:
        for i in range(len(x)):
            axP[0].text(x[i] - W/2,barplot_data_E[i],'{:.2f}%'.format(percent_E[i]),font_text)
            axP[1].text(x[i] - W/2,barplot_data_N[i],'{:.2f}%'.format(percent_N[i]),font_text)
            axP[2].text(x[i] - W/2,barplot_data_U[i],'{:.2f}%'.format(percent_U[i]),font_text)
            axP[3].text(x[i] - W/2,barplot_data_3D[i],'{:.2f}%'.format(percent_3D[i]),font_text)
    

font_text = {'family' : 'Times new roman','weight' : 300,'size'   : 15}
axP[3].set_xticks(X_all)
axP[3].set_xticklabels(barplot_name)
axP[0].legend(mode_list,prop=font_text,ncol=2,bbox_to_anchor=(1,1.5),loc=1)
font_text = {'family' : 'Times new roman','weight' : 300,'size'   : 20}
axP[3].set_xlabel("Site",font_text)
axP[0].set_ylabel("E(cm)",font_text)
axP[1].set_ylabel("N(cm)",font_text)
axP[2].set_ylabel("U(cm)",font_text)
axP[3].set_ylabel("3D(cm)",font_text)
# axP[0].set_ylim(0,10)
# axP[1].set_ylim(0,10)
# axP[2].set_ylim(0,20)
font_text = {'family' : 'Times new roman','weight' : 500,'size'   : 25}
axP[0].set_title("RMS",font_text)
plt.show()
    

