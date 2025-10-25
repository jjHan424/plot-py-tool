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

site_list = ["TERS","IJMU","DENT","WSRT","KOS1","BRUX","DOUR","WARE","REDU","EIJS","TIT2","EUSK","DILL","DIEP","BADH","KLOP","FFMJ","KARL","HOBU","PTBB","GOET"]
# site_list = ["TERS"]
site_list1 = ["BRUX","DOUR","WARE","REDU","EIJS","BADH","FFMJ","KLOP"]
site_list2 = ["KOS1","DENT","WSRT","TIT2","DIEP","EUSK"]
site_list3 = ["IJMU","DILL","PTBB","GOET","TERS","HOBU","KARL"] #HOBU TERS KARL
site_list = site_list3
site_list = ["DOUR"]
site_list_plot = site_list
Mode_Plot = "Site"
Fix_mode = "FixRaw"
com_mode = "CON"
Site = "WUDA"
mode_list = ["CON","COEF","GRID"]
DirectAll = "/Users/hanjunjie/Master_3/1-IUGG/ResFromServer/CLIENT/Statistic"
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
        data_save[cur_site][mode_list[i]] = rf.H_open_rms(os.path.join(DirectAll , cur_site + "-Sigma-0-08.txt"),i+1,len(mode_list))

#===========Day============#
if Mode_Plot=="Site":
    for Site in site_list_plot:
        if Site not in data_save.keys():
            print("No Data")
        else:
            cur_site = Site
            W=0.8/len(data_save[site_list_plot[0]].keys())
            if Fix_mode == "FixRaw" or Fix_mode == "FixSig":
                figP,axP = plt.subplots(5,1,figsize=(9.5,9.5),sharey=False,sharex=True)
            else:
                figP,axP = plt.subplots(4,1,figsize=(18,9.5),sharey=False,sharex=True)
            mode_list = []
            imode = 0
            mode_num = len(data_save[cur_site].keys())
            for mode in data_save[cur_site].keys():
                compare_data_Fix,compare_data_E,compare_data_N,compare_data_U,compare_data_3D=[],[],[],[],[]
                if mode == com_mode:
                    for cdoy in data_save[cur_site][mode].keys():
                        if Fix_mode == "FixRaw" or Fix_mode == "FixSig":
                            compare_data_Fix.append(data_save[cur_site][mode][cdoy][Fix_mode])
                        compare_data_E.append(data_save[cur_site][mode][cdoy]["E"])
                        compare_data_N.append(data_save[cur_site][mode][cdoy]["N"])
                        compare_data_U.append(data_save[cur_site][mode][cdoy]["U"])
                        compare_data_3D.append(math.sqrt(math.pow(data_save[cur_site][mode][cdoy]["E"],2)+math.pow(data_save[cur_site][mode][cdoy]["N"],2)+math.pow(data_save[cur_site][mode][cdoy]["U"],2)))
                    compare_data_E = np.array(compare_data_E)
                    compare_data_N = np.array(compare_data_N)
                    compare_data_U = np.array(compare_data_U)
                    compare_data_3D = np.array(compare_data_3D)
                    if Fix_mode == "FixRaw" or Fix_mode == "FixSig":
                        compare_data_Fix = np.array(compare_data_Fix)
                    break
            for mode in data_save[cur_site].keys():
                X_all = list(range(len(data_save[cur_site][mode].keys())))
                mode_list.append(mode)
                bartext_data_Fix,barplot_data_Fix,percent_Fix = [],[],[]
                barplot_data_E,percent_E = [],[]
                barplot_data_N,percent_N = [],[]
                barplot_data_U,percent_U = [],[]
                barplot_data_3D,percent_3D = [],[]
                barplot_name = []
                x = []
                j=0
                for cdoy in data_save[cur_site][mode]:
                    if Fix_mode == "FixRaw" or Fix_mode == "FixSig":
                        if data_save[cur_site][mode][cdoy][Fix_mode] < 80:
                            barplot_data_Fix.append(80)
                        else:
                            barplot_data_Fix.append(data_save[cur_site][mode][cdoy][Fix_mode])
                        bartext_data_Fix.append(data_save[cur_site][mode][cdoy][Fix_mode])
                    barplot_data_E.append(data_save[cur_site][mode][cdoy]["E"])
                    barplot_data_N.append(data_save[cur_site][mode][cdoy]["N"])
                    barplot_data_U.append(data_save[cur_site][mode][cdoy]["U"])
                    barplot_data_3D.append(math.sqrt(math.pow(data_save[cur_site][mode][cdoy]["E"],2)+math.pow(data_save[cur_site][mode][cdoy]["N"],2)+math.pow(data_save[cur_site][mode][cdoy]["U"],2)))
                    barplot_name.append(cdoy)
                    x.append(X_all[j])
                    j=j+1
                if mode != com_mode:
                    if Fix_mode == "FixRaw" or Fix_mode == "FixSig":
                        percent_Fix=np.array(barplot_data_Fix) - compare_data_Fix
                    percent_E=(compare_data_E-np.array(barplot_data_E))/compare_data_E *100
                    percent_N=(compare_data_N-np.array(barplot_data_N))/compare_data_N*100
                    percent_U=(compare_data_U-np.array(barplot_data_U))/compare_data_U*100
                    percent_3D=(compare_data_3D-np.array(barplot_data_3D))/compare_data_3D*100
                for j in range(len(x)):
                    x[j] = x[j] + W*imode - W*(mode_num-1)/2
                imode = imode + 1
                font_text = {'family' : 'Times new roman','weight' : 300,'size'   : 10}
                axP[0].bar(x,barplot_data_E,width = W,label='value')
                axP[1].bar(x,barplot_data_N,width = W,label='value')
                axP[2].bar(x,barplot_data_U,width = W,label='value')
                axP[3].bar(x,barplot_data_3D,width = W,label='value')
                if Fix_mode == "FixRaw" or Fix_mode == "FixSig":
                    axP[4].bar(x,barplot_data_Fix,width = W,label='value')
                if mode != com_mode:
                    font_text = {'family' : 'Times new roman','weight' : 300,'size'   : 10}
                    for i in range(len(x)):
                        if percent_E[i] < 0:
                            axP[0].text(x[i] - W/2,barplot_data_E[i],'{:.2f}%'.format(percent_E[i]),font_text,rotation=45,color="red")
                        else:
                            axP[0].text(x[i] - W/2,barplot_data_E[i],'{:.2f}%'.format(percent_E[i]),font_text,rotation=45,color="green")
                        if percent_N[i] < 0:
                            axP[1].text(x[i] - W/2,barplot_data_N[i],'{:.2f}%'.format(percent_N[i]),font_text,rotation=45,color="red")
                        else:
                            axP[1].text(x[i] - W/2,barplot_data_N[i],'{:.2f}%'.format(percent_N[i]),font_text,rotation=45,color="green")
                        if percent_U[i] < 0:
                            axP[2].text(x[i] - W/2,barplot_data_U[i],'{:.2f}%'.format(percent_U[i]),font_text,rotation=45,color="red")
                        else:
                            axP[2].text(x[i] - W/2,barplot_data_U[i],'{:.2f}%'.format(percent_U[i]),font_text,rotation=45,color="green")
                        if percent_3D[i] < 0:
                            axP[3].text(x[i] - W/2,barplot_data_3D[i],'{:.2f}%'.format(percent_3D[i]),font_text,rotation=45,color="red")
                        else:
                            axP[3].text(x[i] - W/2,barplot_data_3D[i],'{:.2f}%'.format(percent_3D[i]),font_text,rotation=45,color="green")
                if Fix_mode == "FixRaw" or Fix_mode == "FixSig":
                    for i in range(len(x)):
                        axP[4].text(x[i] - W/2,barplot_data_Fix[i],'{:.2f}%'.format(bartext_data_Fix[i]),font_text,rotation=45)

            num_mode = len(mode_list)
            font_text = {'family' : 'Times new roman','weight' : 300,'size'   : 12}
            axP[3].set_xticks(X_all)
            axP[3].set_xticklabels(barplot_name)
            axP[0].legend(mode_list,prop=font_text,ncol=3,bbox_to_anchor=(1,1.55),loc=1)
            font_text = {'family' : 'Times new roman','weight' : 300,'size'   : 20}
            if Fix_mode == "FixRaw" or Fix_mode == "FixSig":
                axP[4].set_xlabel("Day of Year",font_text)
            else:
                axP[3].set_xlabel("Day of Year",font_text)
            axP[0].set_ylabel("E(cm)",font_text)
            axP[1].set_ylabel("N(cm)",font_text)
            axP[2].set_ylabel("U(cm)",font_text)
            axP[3].set_ylabel("3D(cm)",font_text)
            if Fix_mode == "FixRaw" or Fix_mode == "FixSig":
                axP[4].set_ylabel(Fix_mode,font_text)
                axP[4].set_ylim(80,100)
            # axP[0].set_ylim(0,10)
            # axP[1].set_ylim(0,10)
            # axP[2].set_ylim(0,20)
            font_text = {'family' : 'Times new roman','weight' : 500,'size'   : 25}
            axP[0].set_title(Site+"-RMS",font_text)
            if show:
                plt.show()
            else:
                plt.savefig(DirectSave+"\\"+Site+"-Chk-Grid-Coef"+".png",dpi=600)


if Mode_Plot=="Mean":
#===========Site============#
    if Fix_mode == "FixRaw" or Fix_mode == "FixSig":
        mode_Num = 5
    else:
        mode_Num = 4
    figP,axP = plt.subplots(mode_Num,1,figsize=(9.5,9.5),sharey=False,sharex=True)
    for Site in site_list_plot:
        if Site not in data_save.keys():
            print("No Data")
        else:
            cur_site = Site
            W=0.2
            mode_list = []
            imode = -1
        
        for mode in data_save[cur_site].keys():
            barplot_data_Fix = []
            barplot_data_E = []
            barplot_data_N = []
            barplot_data_U = []
            barplot_data_3D = []
            barplot_name = []
            x = []
            j=0
            for cdoy in data_save[cur_site][mode]:
                # if cdoy == 305:
                #     continue
                if mode_Num==5:
                    barplot_data_Fix.append(data_save[cur_site][mode][cdoy][Fix_mode])
                barplot_data_E.append(data_save[cur_site][mode][cdoy]["E"])
                barplot_data_N.append(data_save[cur_site][mode][cdoy]["N"])
                barplot_data_U.append(data_save[cur_site][mode][cdoy]["U"])
            data_save[cur_site][mode]["mean"] = {}
            data_save[cur_site][mode]["mean"]["E"] = np.mean(barplot_data_E)
            data_save[cur_site][mode]["mean"]["N"] = np.mean(barplot_data_N)
            data_save[cur_site][mode]["mean"]["U"] = np.mean(barplot_data_U)
            if mode_Num==5:
                data_save[cur_site][mode]["mean"][Fix_mode] = np.mean(barplot_data_Fix)
            
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
        barplot_data_Fix = []
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
            if mode_Num==5:
                barplot_data_Fix.append(data_save[cur_site][mode]["mean"][Fix_mode])
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
        if mode_Num==5:
            axP[4].bar(x,barplot_data_Fix,width = W,label='value')
        axP[0].bar(x,barplot_data_E,width = W,label='value')
        axP[1].bar(x,barplot_data_N,width = W,label='value')
        axP[2].bar(x,barplot_data_U,width = W,label='value')
        axP[3].bar(x,barplot_data_3D,width = W,label='value')
        font_text = {'family' : 'Times new roman','weight' : 300,'size'   : 10}
        # if mode != com_mode:
        #     for i in range(len(x)):
        #         if percent_E[i] < 0:
        #             axP[0].text(x[i] - W/2,barplot_data_E[i],'{:.2f}%'.format(percent_E[i]),font_text,rotation=45,color="red")
        #         else:
        #             axP[0].text(x[i] - W/2,barplot_data_E[i],'{:.2f}%'.format(percent_E[i]),font_text,rotation=45,color="green")
        #         if percent_N[i] < 0:
        #             axP[1].text(x[i] - W/2,barplot_data_N[i],'{:.2f}%'.format(percent_N[i]),font_text,rotation=45,color="red")
        #         else:
        #             axP[1].text(x[i] - W/2,barplot_data_N[i],'{:.2f}%'.format(percent_N[i]),font_text,rotation=45,color="green")
        #         if percent_U[i] < 0:
        #             axP[2].text(x[i] - W/2,barplot_data_U[i],'{:.2f}%'.format(percent_U[i]),font_text,rotation=45,color="red")
        #         else:
        #             axP[2].text(x[i] - W/2,barplot_data_U[i],'{:.2f}%'.format(percent_U[i]),font_text,rotation=45,color="green")
        #         if percent_3D[i] < 0:
        #             axP[3].text(x[i] - W/2,barplot_data_3D[i],'{:.2f}%'.format(percent_3D[i]),font_text,rotation=45,color="red")
        #         else:
        #             axP[3].text(x[i] - W/2,barplot_data_3D[i],'{:.2f}%'.format(percent_3D[i]),font_text,rotation=45,color="green")
                
        if mode_Num==5:
            for i in range(len(x)):
                # axP[4].text(x[i] - W/2,barplot_data_Fix[i],'{:.2f}%'.format(barplot_data_Fix[i]),font_text,rotation=45)
                print("{:>4}-{}{:>3}:{:<3.4f}cm{:>3}:{:<3.4f}cm{:>3}:{:<3.4f}cm{:>3}:{:<3.4f}cm{:>3}:{:<3.2f}%".format(mode,site_list[i],"E",barplot_data_E[i],"N",barplot_data_N[i],"U",barplot_data_U[i],"3D",barplot_data_3D[i],"Fix",barplot_data_Fix[i]))
            print("{:>4} {:>3}:{:<3.4f}cm{:>3}:{:<3.4f}cm{:>3}:{:<3.4f}cm{:>3}:{:<3.4f}cm{:>3}:{:<3.2f}%".format(mode,"E",np.mean(barplot_data_E),"N",np.mean(barplot_data_N),"U",np.mean(barplot_data_U),"3D",np.mean(barplot_data_3D),"Fix",np.mean(barplot_data_Fix)))

    font_text = {'family' : 'Times new roman','weight' : 300,'size'   : 15}
    axP[mode_Num-1].set_xticks(X_all)
    axP[mode_Num-1].set_xticklabels(barplot_name)
    font = {'family': 'Times new roman','weight': 500,'size': 20}
    axP[0].legend(mode_list,prop=font,
            framealpha=1,facecolor='none',ncol=4,numpoints=5,markerscale=3, 
            borderaxespad=0,bbox_to_anchor=(1,1.4),loc=1,frameon = False) 
    font_text = {'family' : 'Times new roman','weight' : 600,'size'   : 20}
    axP[mode_Num-1].set_xlabel("Site",font_text)
    axP[0].set_ylabel("East(cm)",font_text)
    axP[1].set_ylabel("North(cm)",font_text)
    axP[2].set_ylabel("Up(cm)",font_text)
    axP[3].set_ylabel("3D(cm)",font_text)
    labels = axP[0].get_yticklabels() + axP[1].get_yticklabels() + axP[2].get_yticklabels() + axP[3].get_yticklabels() + axP[4].get_yticklabels() + axP[4].get_xticklabels()
    [label.set_fontsize(18) for label in labels]
    [label.set_fontname('Times New Roman') for label in labels]
    if mode_Num==5:
        # axP[4].set_ylabel(Fix_mode,font_text)
        axP[4].set_ylabel("Fixing rate(%)",font_text)
        axP[4].set_ylim(80,100)
    # axP[0].set_ylim(0,10)
    # axP[1].set_ylim(0,10)
    # axP[2].set_ylim(0,20)
    font_text = {'family' : 'Times new roman','weight' : 500,'size'   : 25}
    # axP[0].set_title("RMS",font_text)
    # plt.savefig(r"E:\1Master_2\Paper_Grid\1-Paper_word\Image-1\4-distance-Position-Bar.svg")
    # plt.savefig(r"E:\1Master_2\Paper_Grid\1-Paper_word\Image-1\4-distance-Position-Bar.png",dpi=600)
    plt.show()
    
    

