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
font_title = {'family' : 'Arial', 'weight' : 300, 'size' : 23}
font_label = {'family' : 'Arial', 'weight' : 300, 'size' : 23}
font_tick = {'family' : 'Arial', 'weight' : 300, 'size' : 23}
font_legend = {'family' : 'Arial', 'weight' : 300, 'size' : 23}
# font_legend = {'family' : 'Times New Roman', 'weight' : 600, 'size' : 15}
font_text = {'family' : 'Arial','weight' : 300,'size'   : 23}
xtick_size = 23
color_list = ["#0099E5","#34BF49","#FF4C4C"]
# site_list = ["KARL","TERS","IJMU","DENT","WSRT","KOS1","BRUX","DOUR","WARE","REDU","EIJS","TIT2","EUSK","DILL","DIEP","BADH","KLOP","FFMJ","HOBU","PTBB","GOET"]
# site_list = ["KARL","IJMU","DENT","KOS1","BRUX","DOUR","WARE","REDU","EIJS","TIT2","EUSK","DILL","DIEP","BADH","KLOP","FFMJ","PTBB","GOET"]
site_list = ["HKTK","T430","HKLT","HKKT","HKSS","HKWS","HKSL","HKST","HKKS","HKCL","HKSC","HKPC","HKNP","HKMW","HKLM","HKOH"]
# site_list = ["KOS1-312","KOS1-313","KOS1-314"]
site_list = ["HKST"]
# site_list = ["HKTK","T430","HKLT","HKKT","HKWS","HKST","HKKS","HKCL","HKSC","HKNP","HKLM"]
# site_list_string = "EIJS WARE EUSK TIT2 BRUX REDU DOUR KOS1 BADH KLOP FFMJ DILL DENT IJMU DIEP GOET WSRT PTBB HOBU"
# site_list = site_list_string.split(" ")
# site_list = ["HKTK","T430","HKLT","HKKT","HKSS","HKWS","HKSL","HKST","HKKS","HKCL","HKSC","HKPC","HKNP","HKMW","HKLM","HKOH"]
# site_list = ["TIT2"]
# site_list1 = ["BRUX","DOUR","WARE","REDU","EIJS","BADH","FFMJ","KLOP"]
# site_list2 = ["KOS1","DENT","WSRT","TIT2","DIEP","EUSK"]
# site_list3 = ["KARL","TERS","IJMU","HOBU","DILL","PTBB","GOET"]
# site_list = site_list1
# site_list = ["site_list1"]
site_list_plot = site_list
Mode_Plot = "Site_Thesis"
Fix_mode = "FixRaw"
com_mode = "CON"
Site = "WUDA"
mode_list = ["No prediction","ARIMA","LSTM"]
# mode_list = ["L","T"]
# mode_list = ["1-1","2-1","3-1","4-1","5-1","6-1","7-1","8-1","5-5","Auto"]
# mode_list = ["1-1","2-1","Auto"]
# plot_list = ["E","N","U","3D","FixSig"]
plot_list = ["2D","U","010-3","FixRaw"]
# plot_list = ["005-H","005-V","005-3","010-H","010-V","010-3","020-H","020-V","020-3"]
# plot_list = ["3D","010-H","010-V","FixRaw"]
# DirectAll = r"E:\1Master_2\3-IUGG\Result_Server\Client_20230704_5S\RES_30S_10"
DirectAll = "/Users/hanjunjie/Master_3/1-IUGG/ResFromServer/CLIENT/Statistic_Prediction"
# DirectAll = r"E:\1Master_2\3-IUGG\Result_Server\Client_20230629\RES_FIX\PNG_HK_305_10_16"
DirectSave = r"E:\1Master_2\3-IUGG\Result_Server\Client_20230629\RES_RE600"
site_num = len(site_list)
show = True
data_save = {}
for i in range(site_num):
    cur_site = site_list[i]
    # file_path = Direct1 + "\\" + cur_site + "-Sigma-1.txt"
    if cur_site not in data_save.keys():
        data_save[cur_site] = {}
    for i in range(len(mode_list)):
        # data_save[cur_site][mode_list[i]] = rf.H_open_rms(DirectAll + "\\" + cur_site + "-Sigma-1-10.txt",i+1,len(mode_list))
        data_save[cur_site][mode_list[i]] = rf.H_open_rms(os.path.join(DirectAll , cur_site + "-Sigma-1-12.txt"),i+1,len(mode_list))


W=0.8/len(mode_list)
bar_plot = {}
data_mean = {}
for cur_site in site_list:
    bar_plot[cur_site],data_mean[cur_site] = {},{}
    ##-------refresh plot data--------##
    for cur_mode in data_save[cur_site].keys():
        if cur_mode not in bar_plot[cur_site].keys():
            bar_plot[cur_site][cur_mode],data_mean[cur_site][cur_mode] = {},{}
        for cur_type in plot_list:
            if cur_type not in bar_plot[cur_site][cur_mode].keys():
                bar_plot[cur_site][cur_mode][cur_type] = []
    
    for cur_mode in data_save[cur_site].keys():
        bar_plot[cur_site]["DOY"] = []
        for cur_doy in data_save[cur_site][cur_mode].keys():
            bar_plot[cur_site]["DOY"].append(cur_doy)
            for cur_type in plot_list:
                bar_plot[cur_site][cur_mode][cur_type].append(data_save[cur_site][cur_mode][cur_doy][cur_type])
    for cur_mode in data_save[cur_site].keys():
        for cur_type in bar_plot[cur_site][cur_mode].keys():
            data_mean[cur_site][cur_mode][cur_type] = np.mean(bar_plot[cur_site][cur_mode][cur_type])
bar_plot_mean = {}
for cur_mode in mode_list:
    if cur_mode not in bar_plot_mean:
        bar_plot_mean[cur_mode] = {}
    for cur_type in plot_list:
        if cur_type not in bar_plot_mean[cur_mode].keys():
            bar_plot_mean[cur_mode][cur_type] = []
        for cur_site in data_mean.keys():
            bar_plot_mean[cur_mode][cur_type].append(data_mean[cur_site][cur_mode][cur_type])

if Mode_Plot == "Site":
    for cur_site in data_save.keys():
        figP,axP = plt.subplots(len(plot_list),1,figsize=(12,12),sharey=False,sharex=True)
        i_mode = 0
        for cur_mode in data_save[cur_site].keys():
            X_all = list(range(len(data_save[cur_site][cur_mode].keys())))
            for i in range(len(X_all)):
                X_all[i] = X_all[i] + W*i_mode - W*(len(mode_list)-1)/2
            for i in range(len(plot_list)):
                axP[i].bar(X_all,bar_plot[cur_site][cur_mode][plot_list[i]],width = W,label='value')
            i_mode = i_mode + 1
        X_all = list(range(len(bar_plot[cur_site]["DOY"])))
        axP[len(axP)-1].set_xticks(X_all)
        axP[len(axP)-1].set_xticklabels(bar_plot[cur_site]["DOY"])
        plt.show()

if Mode_Plot == "Site_Thesis":
    for cur_site in data_save.keys():
        figP,axP = plt.subplots(2,2,figsize=(12,8),sharey=False,sharex=True)
        i_mode = 0
        for cur_mode in data_save[cur_site].keys():
            X_all = list(range(1,len(data_save[cur_site][cur_mode].keys())+1))
            for i in range(len(X_all)):
                X_all[i] = X_all[i] + W*i_mode - W*(len(mode_list)-1)/2
            for i in range(len(plot_list)):
                if plot_list[i] == "2D":
                    axP[0][0].bar(X_all,bar_plot[cur_site][cur_mode][plot_list[i]],width = W,label='value',color = color_list[i_mode%3])
                if plot_list[i] == "U":
                    axP[0][1].bar(X_all,bar_plot[cur_site][cur_mode][plot_list[i]],width = W,label='value',color = color_list[i_mode%3])
                if plot_list[i] == "010-3":
                    axP[1][0].bar(X_all,bar_plot[cur_site][cur_mode][plot_list[i]],width = W,label='value',color = color_list[i_mode%3])
                if plot_list[i] == "FixRaw":
                    axP[1][1].bar(X_all,bar_plot[cur_site][cur_mode][plot_list[i]],width = W,label='value',color = color_list[i_mode%3])
            i_mode = i_mode + 1
        # X_all = list(range(len(bar_plot[cur_site]["DOY"])))
        # axP[len(axP)-1].set_xticks(X_all)
        # axP[len(axP)-1].set_xticklabels(bar_plot[cur_site]["DOY"])
        axP[0][0].set_ylim(0,8)
        axP[0][1].set_ylim(0,8)
        axP[1][0].set_ylim(0,800)
        axP[1][1].set_ylim(85,100)
        axP[0][0].set_yticks([0,2,4,6,8])
        axP[0][1].set_yticks([0,2,4,6,8])
        axP[1][0].set_yticks([0,200,400,600,800])
        axP[1][1].set_yticks([85,90,95,100])
        axP[0][0].set_ylabel("Position errors (cm)",font_label)
        axP[1][0].set_xlabel("Prediction duration (min)",font_label,x=1)
        axP[1][0].set_ylabel("Convergence Time (s)",font_label)
        axP[1][1].set_ylabel("Fixing Rate (%)",font_label)
        ax_range = axP[0][0].axis()
        axP[0][0].text(ax_range[0],ax_range[3]-1,"Horizontal",font_title)
        ax_range = axP[0][1].axis()
        axP[0][1].text(ax_range[0],ax_range[3]-1,"Vertical",font_title)
        labels = axP[0][0].get_yticklabels() + axP[0][0].get_xticklabels()
        axP[0][0].set_xticks([0,2,4,6,8,10,12,14,16,18,20])
        axP[0][0].set_xticklabels([0,1,2,3,4,5,6,7,8,9,10])
        for i in range(2):
            for j in range(2):
                labels = labels + axP[i][j].get_yticklabels() + axP[i][j].get_xticklabels()
        axP[1][1].legend(mode_list,prop=font_legend,
            framealpha=0,facecolor='none',ncol=3,numpoints=5,markerscale=4, 
            borderaxespad=0,bbox_to_anchor=(1,1.19),loc=1)
        box = axP[1][0].get_position()
        axP[1][0].set_position([box.x0 - 0.03, box.y0, box.width, box.height]) 
        box = axP[0][0].get_position()
        axP[0][0].set_position([box.x0 - 0.03, box.y0, box.width, box.height]) 
        [label.set_fontsize(xtick_size) for label in labels]
        [label.set_fontname('Arial') for label in labels]
        axP[0][0].axhline(y=0.91,color = 'k',linestyle = "--",linewidth = 3)
        axP[0][1].axhline(y=3.44,color = 'k',linestyle = "--",linewidth = 3)
        # axP[1][0].axhline(y=3,color = 'k',linestyle = "--",linewidth = 3)
        legend_list = [plt.Line2D([0,20],[0,20],color = 'k',linestyle = "--",linewidth = 3)]
        # axP[1][0].legend(legend_list,["Auto"],prop = font_legend,frameon=False,bbox_to_anchor=(0.4,1.25),loc=1)
        plt.savefig("/Users/hanjunjie/Desktop/Image-1/HKST_2021279_delay1_20.jpg",dpi=300)
        plt.show()

if Mode_Plot == "Site_Mean":
    # for cur_site in data_save.keys():
    figP,axP = plt.subplots(len(plot_list),1,figsize=(12,12),sharey=False,sharex=True)
    i_mode = 0
    for cur_mode in data_save["KOS1-312"].keys():
        X_all = list(range(len(data_save["KOS1-312"][cur_mode].keys())))
        for i in range(len(X_all)):
            X_all[i] = X_all[i] + W*i_mode - W*(len(mode_list)-1)/2
        for i in range(len(plot_list)):
            y = []
            for cur_site in data_save.keys():
                y.append(bar_plot[cur_site][cur_mode][plot_list[i]])
            y = np.mean(np.array(y),0)
            axP[i].bar(X_all,y,width = W,label='value')
        i_mode = i_mode + 1
    X_all = list(range(len(bar_plot[cur_site]["DOY"])))
    axP[len(axP)-1].set_xticks(X_all)
    axP[len(axP)-1].set_xticklabels(bar_plot[cur_site]["DOY"])
    plt.show()



if Mode_Plot == "Mean":
    i_mode = 0
    figP,axP = plt.subplots(len(plot_list),1,figsize=(12,12),sharey=False,sharex=True)
    for cur_mode in bar_plot_mean.keys():
        X_all = list(range(len(site_list)))
        for i in range(len(X_all)):
            X_all[i] = X_all[i] + W*i_mode - W*(len(mode_list)-1)/2
        for i in range(len(plot_list)):
            axP[i].bar(X_all,bar_plot_mean[cur_mode][plot_list[i]],width = W,label='value')
            print("{}-{} {:.2f}".format(cur_mode,plot_list[i],np.mean(bar_plot_mean[cur_mode][plot_list[i]])))
        i_mode = i_mode + 1
        
    X_all = list(range(len(site_list)))
    axP[len(axP)-1].set_xticks(X_all)
    axP[len(axP)-1].set_xticklabels(site_list)
    plt.show()
visible_ticks = {"top":False,"right":False}
if Mode_Plot == "PPT":
    plt.figure(figsize=(1.5,0.75),dpi = 600)

    axP = plt.subplot(2,3,1)
    i_mode = 0
    for cur_mode in data_save[cur_site].keys():
        X_all = list(range(len(data_save[cur_site][cur_mode].keys())))
        for i in range(len(X_all)):
            X_all[i] = X_all[i] + W*i_mode - W*(len(mode_list)-1)/2
        axP.bar(X_all,bar_plot[cur_site][cur_mode]["E"],width = W,label='value')
        i_mode = i_mode + 1
    axP.set_xticks([0,1,2])
    axP.set_xticklabels(["85 km","124 km","162 km"])
    axP.set_ylim(0,6)
    axP.set_yticks([0,1,2,3,4,5])
    axP.set_yticklabels(["0","1","2","3","4","5"])
    labels = axP.get_yticklabels() + axP.get_xticklabels()
    [label.set_fontsize(xtick_size) for label in labels]
    [label.set_fontname('Arial') for label in labels]
    plt.ylabel("East errors (cm)",fontdict=font_label,labelpad=1)
    axP.grid(False)
    box = axP.get_position()
    axP.set_position([box.x0 - box.width / 8,box.y0 + box.height / 6,box.width,box.height])
    axP.spines['right'].set_color("none")
    axP.spines['top'].set_color("none")
    axP.yaxis.set_minor_locator(mpl.ticker.MultipleLocator(1))
    plt.tick_params(axis="both",which = "both",**visible_ticks)
    #####################
    axP = plt.subplot(2,3,2)
    i_mode = 0
    for cur_mode in data_save[cur_site].keys():
        X_all = list(range(len(data_save[cur_site][cur_mode].keys())))
        for i in range(len(X_all)):
            X_all[i] = X_all[i] + W*i_mode - W*(len(mode_list)-1)/2
        axP.bar(X_all,bar_plot[cur_site][cur_mode]["N"],width = W,label='value')
        i_mode = i_mode + 1
    axP.set_xticks([0,1,2])
    axP.set_xticklabels(["85 km","124 km","162 km"])
    axP.set_ylim(0,6)
    axP.set_yticks([0,1,2,3,4,5])
    axP.set_yticklabels(["0","1","2","3","4","5"])
    labels = axP.get_yticklabels() + axP.get_xticklabels()
    [label.set_fontsize(xtick_size) for label in labels]
    [label.set_fontname('Arial') for label in labels]
    plt.ylabel("North errors (cm)",fontdict=font_label,labelpad=1)
    axP.grid(False)
    box = axP.get_position()
    axP.set_position([box.x0,box.y0 + box.height / 6,box.width,box.height])
    axP.spines['right'].set_color("none")
    axP.spines['top'].set_color("none")
    axP.yaxis.set_minor_locator(mpl.ticker.MultipleLocator(1))
    plt.tick_params(axis="both",which = "both",**visible_ticks)
    ############
    axP = plt.subplot(2,3,3)
    i_mode = 0
    for cur_mode in data_save[cur_site].keys():
        X_all = list(range(len(data_save[cur_site][cur_mode].keys())))
        for i in range(len(X_all)):
            X_all[i] = X_all[i] + W*i_mode - W*(len(mode_list)-1)/2
        axP.bar(X_all,bar_plot[cur_site][cur_mode]["U"],width = W,label='value')
        i_mode = i_mode + 1
    axP.set_xticks([0,1,2])
    axP.set_xticklabels(["85 km","124 km","162 km"])
    axP.set_ylim(0,11)
    axP.set_yticks([0,2,4,6,8,10])
    axP.set_yticklabels(["0","2","4","6","8","10"])
    labels = axP.get_yticklabels() + axP.get_xticklabels()
    [label.set_fontsize(xtick_size) for label in labels]
    [label.set_fontname('Arial') for label in labels]
    plt.ylabel("Up errors (cm)",fontdict=font_label,labelpad=1)
    axP.grid(False)
    box = axP.get_position()
    axP.set_position([box.x0 + box.width / 8,box.y0 + box.height / 6,box.width,box.height])
    axP.spines['right'].set_color("none")
    axP.spines['top'].set_color("none")
    axP.yaxis.set_minor_locator(mpl.ticker.MultipleLocator(1))
    plt.tick_params(axis="both",which = "both",**visible_ticks)
    ##### Lengend ########
    axP.legend(mode_list,prop=font_legend,
            framealpha=0,facecolor='none',ncol=4,numpoints=5,markerscale=4, 
            borderaxespad=0,bbox_to_anchor=(1,1.17),loc=1) 
    ###############
    axP = plt.subplot(2,2,3)
    i_mode = 0
    for cur_mode in data_save[cur_site].keys():
        X_all = list(range(len(data_save[cur_site][cur_mode].keys())))
        for i in range(len(X_all)):
            X_all[i] = X_all[i] + W*i_mode - W*(len(mode_list)-1)/2
        axP.bar(X_all,bar_plot[cur_site][cur_mode]["010-3"],width = W,label='value')
        i_mode = i_mode + 1
    axP.set_xticks([0,1,2])
    axP.set_xticklabels(["85 km","124 km","162 km"])
    axP.set_ylim(0,300)
    axP.set_yticks([0,50,100,150,200,250,300])
    axP.set_yticklabels(["0","50","100","150","200","250","300"])
    labels = axP.get_yticklabels() + axP.get_xticklabels()
    [label.set_fontsize(xtick_size) for label in labels]
    [label.set_fontname('Arial') for label in labels]
    plt.ylabel("Convergen time (s)",fontdict=font_label,labelpad=1)
    axP.grid(False)
    box1 = axP.get_position()
    axP.set_position([box1.x0 - box.width / 8,box1.y0,box1.width,box1.height])
    axP.spines['right'].set_color("none")
    axP.spines['top'].set_color("none")
    axP.yaxis.set_minor_locator(mpl.ticker.MultipleLocator(50))
    plt.tick_params(axis="both",which = "both",**visible_ticks)
    ################
    axP = plt.subplot(2,2,4)
    i_mode = 0
    for cur_mode in data_save[cur_site].keys():
        X_all = list(range(len(data_save[cur_site][cur_mode].keys())))
        for i in range(len(X_all)):
            X_all[i] = X_all[i] + W*i_mode - W*(len(mode_list)-1)/2
        axP.bar(X_all,bar_plot[cur_site][cur_mode]["FixSig"],width = W,label='value')
        i_mode = i_mode + 1
    axP.set_xticks([0,1,2])
    axP.set_xticklabels(["85 km","124 km","162 km"])
    axP.set_ylim(95,100)
    axP.set_yticks([95,96,97,98,99,100])
    axP.set_yticklabels(["95","96","97","98","99","100"])
    labels = axP.get_yticklabels() + axP.get_xticklabels()
    [label.set_fontsize(xtick_size) for label in labels]
    [label.set_fontname('Arial') for label in labels]
    plt.ylabel("Fixing rate (%)",fontdict=font_label,labelpad=1)
    axP.grid(False)
    box1 = axP.get_position()
    axP.set_position([box1.x0 + box.width / 8,box1.y0,box1.width,box1.height])
    axP.spines['right'].set_color("none")
    axP.spines['top'].set_color("none")
    axP.yaxis.set_minor_locator(mpl.ticker.MultipleLocator(1))
    plt.tick_params(axis="both",which = "both",**visible_ticks)
    plt.show()

        