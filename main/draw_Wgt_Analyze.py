import os
import sys
sys.path.insert(0,os.path.dirname(__file__)+'/..')
import numpy as np
import readfile as rf
import matplotlib as mpl
mpl.use("TkAgg")
import matplotlib.pyplot as plt
import dataprocess as dp
import draw as dr
#import seaborn as sns
import trans as tr
import math
site_list = ["WHYJ","WHXZ","WHDS","WHSP","N028","N047","N068","XGXN","WUDA","HKTK","T430","HKLT","HKKT","HKSS","HKWS","HKSL","HKST","HKKS","HKCL","HKSC","HKPC","HKNP","HKMW","HKLM","HKOH"]
# site_list = ["HKTK","T430","HKLT","HKKT","HKSS","HKWS","HKSL","HKST","HKKS","HKCL","HKSC","HKPC","HKNP","HKMW","HKLM","HKOH"]
# site_list = ["WHYJ","WHXZ","WHDS","WHSP","N028","N047","N068","XGXN","WUDA"]
# site_list = ["WHYJ","WHXZ","WHDS","WHSP","N004","N010","N028","N047","N062","N068","XGXN","WUDA","N032","E033"]
count = 1
Year,Mon,Day,Hour,LastT,deltaT = 2021,12,4,0,24,2
while count > 0:
    Day = Day + 1
    count = count - 1
    if (Day > 31):
        Day = 1
        Mon = Mon + 1
    for cur_site in site_list:
        doy = tr.ymd2doy(Year,Mon,Day,0,0,00)
        yyyy = "{:0>4}".format(Year)
        cdoy = "{:0>3}".format(doy)
        path_Diff = r"E:\1Master_2\Paper_Grid\Res_FromServer_New\Diff-New"+ "\\" +  yyyy + cdoy + "\\" + cur_site + "-GEC-5.diff"
        path_Ele = r"E:\1Master_2\Paper_Grid\Res_FromServer_New\Server"+ "\\" +  yyyy + cdoy + "\\" + cur_site +"-GEC.aug"
        path_ROTI = r"E:\1Master_2\Paper_Grid\Res_FromServer_New\ROTI"+"\\"+ yyyy + cdoy + "\\" + cur_site + yyyy + cdoy + "_GEC.ismr"
        Save_Dir = r"E:\1Master_2\Paper_Grid\Res_FromServer_New\Ele_Wgt-New"+"\\"+ yyyy + cdoy
        # Save_Dir = r"E:\1Master_2\Paper_Grid\Pro_20211205-339\Ele_Wgt\HK"
        if (not os.path.exists(Save_Dir)):
            os.mkdir(Save_Dir)
        
        [Head_Ele,data_Ele] = rf.open_aug_file_new(path_Ele)
        [Head_Diff,data_Diff] = rf.open_aug_file_new(path_Diff)
        data_ROTI = rf.open_ismr(path_ROTI)
        time = "UTC"
        figP,axP = plt.subplots(2,3,figsize=(12,9),sharey=False,sharex=True)
        ############TIME SET###################
        if "+" in time:
            end_time = len(time)
            delta_Time = int(time[3:end_time]) + Hour
            begT = int(time[3:end_time]) + Hour
        else:

            delta_Time = Hour
            begT=Hour
        #for time in data[mode[0]].keys():
        secow_start = tr.ymd2gpst(Year,Mon,Day,0,00,00)
        cov_Time = secow_start[1] - 0 * 3600
        if "+" in time:
            cov_Time = secow_start[1] - int(time[3:end_time]) * 3600
        end_Time = begT + LastT
        delta_X = math.ceil((LastT)/deltaT)
        XLabel = []
        XTick = []
        starttime = begT - deltaT
        for i in range(delta_X):
            starttime = starttime + deltaT
            cur_Str_X = '%02d' % (starttime % 24) + ":00"
            XLabel.append(cur_Str_X)
            XTick.append(int(starttime))       
        while starttime < math.ceil(end_Time):
            starttime = starttime + deltaT
            cur_Str_X = '%02d' % (starttime % 24) + ":00"
            XLabel.append(cur_Str_X)
            XTick.append(int(starttime))
        sys_type = {}
        sys_type["C"] = "dION2"
        sys_type["G"] = "dION1"
        sys_type["E"] = "dION1"  
        time_G = [[] for i in range(100)]
        time_R = [[] for i in range(100)]
        time_E = [[] for i in range(100)]
        time_C = [[] for i in range(100)]
        Diff_G = [[] for i in range(100)]
        Diff_R = [[] for i in range(100)]
        Diff_E = [[] for i in range(100)]
        Diff_C = [[] for i in range(100)]
        Ele_G = [[] for i in range(100)]
        Ele_R = [[] for i in range(100)]
        Ele_E = [[] for i in range(100)]
        Ele_C = [[] for i in range(100)]

        for time in data_Diff.keys():
            if time not in data_Ele.keys():
                continue
            plot_time = (time - cov_Time) / 3600
            if (plot_time > begT and plot_time < begT + LastT):
                for sat in data_Diff[time].keys():
                    prn = int(sat[1:3])
                    if abs(data_Diff[time][sat][sys_type[sat[0]]]) == 0:
                        continue
                    if sat not in data_Ele[time].keys():
                        continue
                    if sat not in data_ROTI[time].keys():
                        continue
                    if sat[0] == "C":
                        Diff_C[prn-1].append(abs(data_Diff[time][sat][sys_type[sat[0]]]))
                        Ele_C[prn-1].append(data_Ele[time][sat]["ELE"])
                        with open(Save_Dir + "\\" + cur_site + "_" + sat[0] + ".txt",'a') as file1:
                            file1.write('%04f' % abs(data_Diff[time][sat][sys_type[sat[0]]]) + "   " + '%04f' % data_Ele[time][sat]["ELE"] + "   " + '%04f' % data_ROTI[time][sat] + "\n")
                        # with open(Save_Dir + "\\" + sat[0] + "-WH.txt",'a') as file1:
                        #     file1.write('%04f' % abs(data_Diff[time][sat][sys_type[sat[0]]]) + "   " + '%04f' % data_Ele[time][sat]["ELE"] + "   " + '%04f' % data_ROTI[time][sat] + "\n")
                        time_C[prn-1].append(plot_time)
                    if sat[0] == "G":
                        Diff_G[prn-1].append(abs(data_Diff[time][sat][sys_type[sat[0]]]))
                        Ele_G[prn-1].append(data_Ele[time][sat]["ELE"])
                        with open(Save_Dir + "\\" + cur_site + "_" + sat[0] + ".txt",'a') as file2:
                            file2.write('%04f' % abs(data_Diff[time][sat][sys_type[sat[0]]]) + "   " + '%04f' % data_Ele[time][sat]["ELE"] + "   " + '%04f' % data_ROTI[time][sat] + "\n")
                        # with open(Save_Dir + "\\" + sat[0] + "-WH.txt",'a') as file2:
                        #     file2.write('%04f' % abs(data_Diff[time][sat][sys_type[sat[0]]]) + "   " + '%04f' % data_Ele[time][sat]["ELE"] + "   " + '%04f' % data_ROTI[time][sat] + "\n")
                        time_G[prn-1].append(plot_time)
                    if sat[0] == "E":
                        Diff_E[prn-1].append(abs(data_Diff[time][sat][sys_type[sat[0]]]))
                        Ele_E[prn-1].append(data_Ele[time][sat]["ELE"])
                        with open(Save_Dir + "\\" + cur_site + "_" + sat[0] + ".txt",'a') as file3:
                            file3.write('%04f' % abs(data_Diff[time][sat][sys_type[sat[0]]]) + "   " + '%04f' % data_Ele[time][sat]["ELE"] + "   " + '%04f' % data_ROTI[time][sat] + "\n")
                        # with open(Save_Dir + "\\" + sat[0] + "-WH.txt",'a') as file3:
                            # file3.write('%04f' % abs(data_Diff[time][sat][sys_type[sat[0]]]) + "   " + '%04f' % data_Ele[time][sat]["ELE"] + "   " + '%04f' % data_ROTI[time][sat] + "\n")
                        time_E[prn-1].append(plot_time)

        Diff_plot,Ele_plot,Time_plot = {},{},{}
        Diff_plot["G"],Diff_plot["E"],Diff_plot["C"] = Diff_G,Diff_E,Diff_C
        Ele_plot["G"],Ele_plot["E"],Ele_plot["C"] = Ele_G,Ele_E,Ele_C
        Time_plot["G"],Time_plot["E"],Time_plot["C"] = time_G,time_E,time_C
        Plot_index={}
        Plot_index["G"],Plot_index["E"],Plot_index["C"] = 0,1,2
    # for g_sys in Diff_plot.keys():
    #     for i in range(100):
    #         if len(Time_plot[g_sys][i]) == 0:
    #             continue
    #         # axP[0][Plot_index[g_sys]].plot(Time_plot[g_sys][i],Diff_plot[g_sys][i])
    #         # axP[1][Plot_index[g_sys]].plot(Time_plot[g_sys][i],Ele_plot[g_sys][i])
    #         # axP[0][Plot_index[g_sys]].scatter(Time_plot[g_sys][i],Diff_plot[g_sys][i],s=1)
    #         # axP[1][Plot_index[g_sys]].scatter(Time_plot[g_sys][i],Ele_plot[g_sys][i],s=1)
    #         sat = g_sys + '%02d' % (i + 1)
    #         figP1,axP1 = plt.subplots(2,1,figsize=(12,9),sharey=False,sharex=True)
    #         axP1[0].set_title(sat)
    #         savedir = Save_Dir + "\\" +sat + ".jpg"
            
    #         axP1[0].scatter(Time_plot[g_sys][i],Diff_plot[g_sys][i],s=1)
    #         axP1[1].scatter(Time_plot[g_sys][i],Ele_plot[g_sys][i],s=1)

    #         plt.savefig(savedir)
            # plt.show()

    # plt.show()