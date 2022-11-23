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
import glv

Ele_path = r"E:\1Master_2\Paper_Grid\Res_FromServer_New\Server"
Diff_path = r"E:\1Master_2\Paper_Grid\Res_FromServer_New\Diff-New"
Log_path1 = r"E:\1Master_2\Paper_Grid\Res_FromServer_New\Wgt\Coef-12"
Log_path2 = r"E:\1Master_2\Paper_Grid\Res_FromServer_New\Wgt\Coef-19"
Log_path3 = r"E:\1Master_2\Paper_Grid\Res_FromServer_New\Wgt\Coef-20"
Mean_save = r"E:\1Master_2\Paper_Grid\Res_FromServer_New\Fig\Coef-Compare\Chk-Coef131415.mean"

site_list = ["WUDA","WHYJ","N028","HKSC","HKMW","HKTK"]
site_list = ["WUDA"]
mode_list = ["Chk","IonoWgt","IonoWgt"]
title_list = ["Chk","ROTI","CHK"]
sys_list = ["G","E","C"]
plot_type = ["TimePlot"]
FromEle = False
count = 1
Year_Raw,Mon_Raw,Day_Raw = 2021,11,1
Hour,LastT = 11,2
deltaT = 0.5
dis_Site = {"WUDA":[36340.95, 1.81],"WHYJ":[47022.05, 1.88],"N028":[65481.22, 3.52],
            "HKTK":[13074.23, 3.65],"HKSC":[7122.08, 2.05],"HKMW":[7739.61, 3.14]}

mode_diff = {"G":"dION1","E":"dION1","C":"dION2"}

Year,Mon,Day = Year_Raw,Mon_Raw,Day_Raw
if "Time" in plot_type or "TimePlot" in plot_type:
    while count>0:
        [XLabel,XTick,cov_Time,begT,LastT] = dr.xtick("UTC",Year,Mon,Day,Hour,LastT,deltaT)
        doy = tr.ymd2doy(Year,Mon,Day,0,00,00)
        for site in site_list:
            File_Diff = Diff_path + "\\" + "{:0>4}{:0>3}".format(Year,doy) + "\\" + site + "-GEC-5.diff"
            File_Log1 = Log_path1 + "\\" + "{:0>4}{:0>3}".format(Year,doy) + "\\" + site
            File_Log2 = Log_path2 + "\\" + "{:0>4}{:0>3}".format(Year,doy) + "\\" + site
            # File_Log3 = Log_path3 + "\\" + "{:0>4}{:0>3}".format(Year,doy) + "\\" + site
            File_Ele = Ele_path + "\\" + "{:0>4}{:0>3}".format(Year,doy) + "\\" + site + "-GEC.aug"

            File_Log1 =  r"E:\1Master_2\Paper_Grid\Pro_20211101-305\ROTI.log"
            File_Log2 =  r"E:\1Master_2\Paper_Grid\Pro_20211101-305\Chk.log"

            #Read Data
            [Diff_Head,Diff_Data] = rf.open_aug_file_new(File_Diff)
            if FromEle:
                [Ele_Head,Ele_Data] = rf.open_aug_file_new(File_Ele)
                Log_Data1={}
                for cur_time in Ele_Data.keys():
                    plot_time = (cur_time-cov_Time) / 3600
                    if ((plot_time >= begT and plot_time <= (begT + LastT))):
                        if cur_time not in Log_Data1.keys():
                            Log_Data1[cur_time] = {}
                        for sat in Ele_Data[cur_time].keys():
                            if sat not in Log_Data1[cur_time].keys():
                                Log_Data1[cur_time][sat] = {}
                            #===Coef-10===#
                            Log_Data1[cur_time][sat]["Ele"] =  Ele_Data[cur_time][sat]["ELE"]
                            Elevation = Ele_Data[cur_time][sat]["ELE"]
                            Ele_Adjust = (int((Elevation) * 10) + 0.5) / 10 * math.pi/180
                            a = 4e-8 * dis_Site[site][0]
                            a = a * (1 + 1 / 10 * dis_Site[site][1] / (5 / 3 * math.pi))
                            b = 3.8e-7 * dis_Site[site][0] + 0.0012
                            b = b * (1 + 1 / 10 * dis_Site[site][1] / (5 / 3 * math.pi))
                            Log_Data1[cur_time][sat]["IonoFac1"] = a*math.pow(math.sin(Ele_Adjust),-2) + b
            else:
                Log_Data1 = rf.H_open_log_ppprtk_client_wgt(File_Log1,100)
                Log_Data2 = rf.H_open_log_ppprtk_client_wgt(File_Log2,100)
                # Log_Data3 = rf.H_open_log_ppprtk_client_wgt(File_Log3,100)
            #Data Conv
            data,time={},{}
            data["G"],data["E"],data["C"] = [[[] for i in range((50))] for i in range(len(mode_list))],[[[] for i in range((50))] for i in range(len(mode_list))],[[[] for i in range((50))] for i in range(len(mode_list))]
            time["G"],time["E"],time["C"] = [[[] for i in range((50))] for i in range(len(mode_list))],[[[] for i in range((50))] for i in range(len(mode_list))],[[[] for i in range((50))] for i in range(len(mode_list))]
            for cur_time in Log_Data1.keys():
                plot_time = (cur_time-cov_Time) / 3600
                if ((plot_time >= begT and plot_time <= (begT + LastT))):
                    for sat in Log_Data1[cur_time].keys():
                        prn_index = int(sat[1:3]) - 1
                        data[sat[0]][1][prn_index].append(Log_Data1[cur_time][sat][mode_list[1]])
                        time[sat[0]][1][prn_index].append(plot_time)
                        if cur_time in Diff_Data.keys():
                            if sat in Diff_Data[cur_time].keys():
                                if abs(Diff_Data[cur_time][sat][mode_diff[sat[0]]]) == 0.0:
                                    continue
                                Wgt = math.pow(abs(Diff_Data[cur_time][sat][mode_diff[sat[0]]])/Log_Data1[cur_time][sat]["BaseFac"],2)*Log_Data1[cur_time][sat]["BaseWgt"]
                                data[sat[0]][0][prn_index].append(abs(Diff_Data[cur_time][sat][mode_diff[sat[0]]]))
                                # data[sat[0]][0][prn_index].append(Wgt)
                                time[sat[0]][0][prn_index].append(plot_time)
                        
                        if cur_time in Log_Data2.keys():
                            if sat in Log_Data2[cur_time].keys():
                                # if (abs(Log_Data2[cur_time][sat][mode_list[2]]) > 1):
                                #     Log_Data2[cur_time][sat][mode_list[2]] = 1
                                data[sat[0]][2][prn_index].append(math.pow(Log_Data2[cur_time][sat][mode_list[2]],1))
                                time[sat[0]][2][prn_index].append(plot_time)
                        # if cur_time in Diff_Data.keys():
                        #     if sat in Diff_Data[cur_time].keys():
                        #         if abs(Diff_Data[cur_time][sat][mode_diff[sat[0]]]) == 0.0:
                        #             continue
                        #         data[sat[0]][3][prn_index].append(Log_Data3[cur_time][sat][mode_list[3]])
                        #         time[sat[0]][3][prn_index].append(plot_time)
            #Data Plot && mean_Cal
            if  "TimePlot" in plot_type:
                figP,axP = plt.subplots(len(mode_list),len(sys_list),figsize=(14,9.3),sharey=False,sharex=True)
            mode_Num,sys_num = len(mode_list),len(sys_list)
            mean = {}
            mean["G"],mean["E"],mean["C"] = [[] for i in range(len(mode_list))],[[] for i in range(len(mode_list))],[[] for i in range(len(mode_list))]
            mean["GEC"] = [{} for i in range(len(mode_list))]
            for i in range(mode_Num):
                for j in range(sys_num):
                    for sat in range(50):
                        if sys_num == 1 and mode_Num>1 and "TimePlot" in plot_type:
                            axP[i].scatter(time[sys_list[j]][i][sat],data[sys_list[j]][i][sat],s=1)
                        elif mode_Num == 1 and sys_num>1 and "TimePlot" in plot_type:
                            axP[j].scatter(time[sys_list[j]][i][sat],data[sys_list[j]][i][sat],s=1)
                        elif mode_Num>1 and sys_num>1 and "TimePlot" in plot_type:
                            axP[i][j].scatter(time[sys_list[j]][i][sat],data[sys_list[j]][i][sat],s=1)
                        if len(time[sys_list[j]][i][sat]) > 0:
                            mean[sys_list[j]][i].append(np.mean(data[sys_list[j]][i][sat]))
                            mean["GEC"][i][sys_list[j]+'{:0>2}'.format(sat+1)]=(np.mean(data[sys_list[j]][i][sat]))
            #Plot Set
            
            
            #Mean Set && plot
            Mean = {}
            Mean["G"],Mean["E"],Mean["C"] = [],[],[]
            for sys_index in range(sys_num):
                for mode_index in range(mode_Num):
                    Mean[sys_list[sys_index]].append(np.mean(mean[sys_list[sys_index]][mode_index]))
                    mean["GEC"][mode_index][sys_list[sys_index]+"-ALL"]=(np.mean(mean[sys_list[sys_index]][mode_index]))
            if  "TimePlot" in plot_type:
                for i in range(mode_Num):
                    for j in range(sys_num):
                        if sys_num == 1 and mode_Num>1:
                            axP[i].set_xticks(XTick)
                            axP[i].set_xticklabels(XLabel)
                        elif mode_Num == 1 and sys_num>1:
                            axP[j].set_xticks(XTick)
                            axP[j].set_xticklabels(XLabel)
                        elif mode_Num>1 and sys_num>1:
                            axP[i][j].set_xticks(XTick)
                            axP[i][j].set_xticklabels(XLabel)
                            axP[i][j].set_title(site + "-" + sys_list[j]+"-"+title_list[i])
                            # axP[i][j].set_ylim(0,Mean[sys_list[j]][0]*2)
                plt.show()
            with open(Mean_save,'a') as file1:
                for sat in mean["GEC"][0].keys():
                    file1.write('{:0>3}   {}    {}    '.format(doy,sat,site))
                    for mode in range(len(mean["GEC"])):
                        file1.write('{:.4f}    '.format(mean["GEC"][mode][sat]*100))
                    file1.write('\n')

        Day = Day + 1
        if (Day > 31):
            Day = 1
            Mon = Mon + 1
        count = count - 1
Year,Mon,Day = Year_Raw,Mon_Raw,Day_Raw
if "Bar-ALL" in plot_type:
    Mean_Data = {}
    Mean_Data["Chk"] = rf.H_open_mean_ppprtk_client_wgt(Mean_save,1)
    Mean_Data["Coef"] = rf.H_open_mean_ppprtk_client_wgt(Mean_save,2)
    Width = 0.8/len(Mean_Data.keys())
    
    Doy_len = 12
    for cur_site in site_list:
        FixP,axP = plt.subplots(len(sys_list),1,figsize=(14,9.3),sharey=False,sharex=True)
        mode_index = -1
        mode_legend=[]
        for mode in Mean_Data.keys():
            mode_index = mode_index + 1
            mode_legend.append(mode)
            for sys_index in range(len(sys_list)):
                data_plot = []
                X = []
                x = 0
                X_Doy = []
                for doy in Mean_Data[mode][cur_site].keys():
                    data_plot.append(Mean_Data[mode][cur_site][doy][sys_list[sys_index]+"-ALL"])
                    X.append(x - (len(Mean_Data.keys())-1)/2*Width + mode_index*Width)
                    x = x+1
                    X_Doy.append(doy)
                axP[sys_index].bar(X,data_plot,width = Width,label='value')
        for sys_index in range(len(sys_list)):
            axP[sys_index].set_title(sys_list[sys_index]+"-"+cur_site)
            axP[sys_index].set_xticks([0,1,2,3,4,5,6,7,8,9,10,11])
            axP[sys_index].set_xticklabels(X_Doy)
            axP[sys_index].set_xlabel("Doy")
            axP[sys_index].set_ylabel("dIon(cm)")
        axP[0].legend(mode_legend)
        plt.show()
Year,Mon,Day = Year_Raw,Mon_Raw,Day_Raw
if "Bar-SAT" in plot_type:
    Mean_Data = {}
    Mean_Data["Chk"] = rf.H_open_mean_ppprtk_client_wgt(Mean_save,1)
    Mean_Data["Coef"] = rf.H_open_mean_ppprtk_client_wgt(Mean_save,2)
    Width = 0.8/len(Mean_Data.keys())

    doy = tr.ymd2doy(Year,Mon,Day,0,00,00)
    Doy_len = 12
    for cur_site in site_list:
        FixP,axP = plt.subplots(len(sys_list),1,figsize=(14,9.3),sharey=False,sharex=False)
        mode_index = -1
        mode_legend=[]
        for mode in Mean_Data.keys():
            mode_index = mode_index + 1
            mode_legend.append(mode)
            for sys_index in range(len(sys_list)):
                data_plot = []
                X = []
                X_tick = []
                x = 0
                X_Doy = []
                for sat in Mean_Data[mode][cur_site][doy].keys():
                    if sat[0] == sys_list[sys_index]:
                        data_plot.append(Mean_Data[mode][cur_site][doy][sat])
                        X.append(x - (len(Mean_Data.keys())-1)/2*Width + mode_index*Width)
                        X_tick.append(x)
                        x = x+1
                        X_Doy.append(sat)
                axP[sys_index].bar(X,data_plot,width = Width,label='value')
                axP[sys_index].set_title(sys_list[sys_index]+"-"+cur_site+"-{:0>3}".format(doy))
                axP[sys_index].set_xticks(X_tick)
                axP[sys_index].set_xticklabels(X_Doy)

        for sys_index in range(len(sys_list)):
            axP[sys_index].set_ylabel("dIon(cm)")
        axP[0].legend(mode_legend)
        axP[len(sys_list)-1].set_xlabel("Doy")
        plt.show()



