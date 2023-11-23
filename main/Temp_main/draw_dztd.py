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
import seaborn as sns
plt.style.use(['science','grid','no-latex'])
import math
time,year,mon,day,starttime,LastT,deltaT = "UTC",2021,11,6,3,21,1


font_title = {'family' : 'Arial', 'weight' : 500, 'size' : 35}
font_label = {'family' : 'Arial', 'weight' : 300, 'size' : 30}
font_tick = {'family' : 'Arial', 'weight' : 300, 'size' : 35}
font_legend = {'family' : 'Arial', 'weight' : 300, 'size' : 30}
# font_legend = {'family' : 'Times New Roman', 'weight' : 600, 'size' : 15}
font_text = {'family' : 'Arial','weight' : 300,'size'   : 28}
xtick_size = 30
color_list = sns.color_palette("Set1")
site1,site2 = "PTBB","SPT7"
# site1,site2 = "ONS1","IGS"
lon,lat = 9.67,59.19
# site1,site2 = "IGMI","IGM2"
# lon,lat = 10.43,45.76
# site1,site2 = "BOGE","BOGI"
# lon,lat = 20.60,54.53
# site1,site2 = "ONSA","ONS1"
# lon,lat = 9.67,59.19
Site = site1+"-"+site2
# filename_list = [
#             os.path.join(r"E:\1Master_3\2_ZTD\2021310\RECON",Site+"-GEC-FLOAT.flt"),
#             os.path.join(r"E:\1Master_3\2_ZTD\2021310\RECON",Site+"-GEC-FIXED.flt"),
#             os.path.join(r"E:\1Master_3\2_ZTD\2021310\RECON",Site+"-GEC-GRID-VIRTUAL.flt")
#                 ]
filename_list = [
            os.path.join(r"E:\1Master_3\2_ZTD\Result_From_Server\SERVER\server_2021310",site1+"-GE-FLOAT-30-3600.flt"),
            os.path.join(r"E:\1Master_3\2_ZTD\Result_From_Server\SERVER\server_2021310",site1+"-GE-FIXED-30-3600.flt"),
            os.path.join(r"E:\1Master_3\2_ZTD\Result_From_Server\CLIENT\client_2021310",site1+"-GE-FIXED-30-3600.flt"),
            
                ]
# filename_list1 = [
#             os.path.join(r"E:\1Master_3\2_ZTD\2021310\ShortBaseLine_RND_RECON",site2+"-GEC-FLOAT.flt"),
#             os.path.join(r"E:\1Master_3\2_ZTD\2021310\ShortBaseLine_RND_RECON",site2+"-GEC-FIXED.flt"),
#             os.path.join(r"E:\1Master_3\2_ZTD\2021310\Test",site2+"-GEC-PPPRTK-CROSS-ALL-EQUAL-RE-10000-REFAMB.flt"),
#                 ]
filename_list1 = [
            os.path.join(r"E:\1Master_3\2_ZTD\Result_From_Server\REF\310",site1.lower() + "3100.21zpd"),
            os.path.join(r"E:\1Master_3\2_ZTD\Result_From_Server\REF\310",site1.lower() + "3100.21zpd"),
            os.path.join(r"E:\1Master_3\2_ZTD\Result_From_Server\REF\310",site1.lower() + "3100.21zpd"),
            os.path.join(r"E:\1Master_3\2_ZTD\Result_From_Server\REF\310",site1.lower() + "3100.21zpd"),
                ]
# mode_list = ["PPP","PPP-AR","PPPRTK"]
# mode_list = ["KLOP","BADH","FFMJ"]
mode_list = ["FLOAT","FIXED","IONO_CON"]
# mode_list = ["500","10000"]
site = Site


#---readfiles for .flt---#
all_data,all_amb = {},{}
for i in range(len(mode_list)):
    soweek_last = 0
    w_last = 0
    filepath = filename_list[i]
    all_data[mode_list[i]],all_amb[mode_list[i]] = {},{}
    head_end,epoch_flag = False,False
    with open(filepath,'rt') as f:
        for line in f:
            if "#" not in line:
                value=line.split()
                soweek = float(value[0])
                if (soweek < soweek_last):
                    w_last = w_last + 1
                soweek = soweek + w_last*604800
                soweek_last = soweek
                if soweek not in all_data.keys():
                    all_data[mode_list[i]][soweek]=float(value[len(value)-1])
                    all_amb[mode_list[i]][soweek] = value[8]
all_data1,all_amb1 = {},{}
all_data_ref = {}
plot_data_ref = []

for i in range(len(mode_list)):
    epoch_beg = False
    soweek_last = 0
    w_last = 0
    filepath = filename_list1[i]
    all_data1[mode_list[i]],all_amb1[mode_list[i]] = {},{}
    head_end,epoch_flag = False,False
    with open(filepath,'rt') as f:
        if filepath[len(filepath)-3:len(filepath)] == "flt":
            for line in f:
                if "#" not in line:
                    value=line.split()
                    soweek = float(value[0])
                    if (soweek < soweek_last):
                        w_last = w_last + 1
                    soweek = soweek + w_last*604800
                    soweek_last = soweek
                    if soweek not in all_data1.keys():
                        all_data1[mode_list[i]][soweek]=float(value[len(value)-1])
                        all_amb1[mode_list[i]][soweek] = value[8]
        else:
            for line in f:
                if line == "+TROP/SOLUTION\n":
                    epoch_flag = True
                value = line.split()
                if epoch_flag and value[0] == site1:
                    if value[0][0:4] not in all_data_ref.keys():
                        all_data_ref[value[0][0:4]] = {}
                    time_value = value[1].split(":")
                    cur_time = float(time_value[2])/3600
                    
                    all_data_ref[value[0][0:4]][cur_time] = (float(value[2]))
                    if cur_time not in plot_data_ref:
                        plot_data_ref.append(cur_time)

#data convert flt-flt
# [XLabel,XTick,cov_Time,begT,LastT]=dr.xtick(time,year,mon,day,starttime,LastT,deltaT)
# time_plot,data_plot = {},{}
# time_float,data_float = {},{}
# for cur_mode in all_data.keys():
#     time_plot[cur_mode],data_plot[cur_mode],time_float[cur_mode],data_float[cur_mode] = [],[],[],[]
#     for cur_time in all_data[cur_mode].keys():
#         plot_time = (cur_time - cov_Time) / 3600
#         if (plot_time >= begT and plot_time <= begT + LastT) and cur_time in all_data1[cur_mode].keys():
#             time_plot[cur_mode].append(plot_time)
#             data_plot[cur_mode].append((all_data[cur_mode][cur_time]-all_data1[cur_mode][cur_time])*1000)
#             if (all_amb[cur_mode][cur_time] == "Float"):
#                 time_float[cur_mode].append(plot_time)
#                 data_float[cur_mode].append(all_data[cur_mode][cur_time])

#data convert flt-zpd
[XLabel,XTick,cov_Time,begT,LastT]=dr.xtick(time,year,mon,day,starttime,LastT,deltaT)
time_plot,data_plot = {},{}
time_float,data_float = {},{}
for cur_mode in all_data.keys():
    if site1 not in all_data_ref.keys():
        continue
    time_plot[cur_mode],data_plot[cur_mode],time_float[cur_mode],data_float[cur_mode] = [],[],[],[]
    for cur_time in all_data[cur_mode].keys():
        plot_time = (cur_time - cov_Time) / 3600
        # if cur_time % 3600 != 0:
        #     continue
        if (plot_time >= begT and plot_time <= begT + LastT) and plot_time in all_data_ref[site1].keys():
            # if plot_time == 9 or plot_time == 19:
            #     continue
            time_plot[cur_mode].append(plot_time)
            data_plot[cur_mode].append((all_data[cur_mode][cur_time]*1000-all_data_ref[site1][plot_time]))
            if (all_amb[cur_mode][cur_time] == "Float"):
                time_float[cur_mode].append(plot_time)
                data_float[cur_mode].append(all_data[cur_mode][cur_time])

#plot
figP,axP = plt.subplots(1,1,figsize=(17,8),sharey=True,sharex=True)
# axP.set_ylim(-0.02,0.02)
for i in range(len(mode_list)):
    # axP.scatter(time_plot[mode_list[i]],data_plot[mode_list[i]],color = color_list[i%9],s=8)
     axP.plot(time_plot[mode_list[i]],data_plot[mode_list[i]],color = color_list[i%9],linewidth = 3)
# for i in range(len(mode_list)):
#     axP.scatter(time_float[mode_list[i]],data_float[mode_list[i]],color = color_list[1],s=5)
axP.set_xticks(XTick)
axP.set_xticklabels(XLabel)
axP.set_title(site,font_title)
axP.legend(mode_list,prop=font_legend,
            framealpha=0,facecolor='none',numpoints=5,markerscale=4, 
            borderaxespad=0) 
# axP.legend(["Fixed","Float"],prop=font_legend,
#             framealpha=0,facecolor='none',numpoints=5,markerscale=4, 
#             borderaxespad=0) 
axP.set_xlabel("Time (GPST)",font_label)
axP.set_ylabel("Zenith Troposphere Delay (mm)",font_label)
labels = axP.get_yticklabels() + axP.get_xticklabels()
[label.set_fontsize(xtick_size) for label in labels]
[label.set_fontname('Arial') for label in labels]
#PrintOut
for i in range(len(mode_list)):
    str_info = "{} WHT {:<10} RMS {:.1f} mm MEAN {:.1f} mm STD {:.1f} mm".format(site,mode_list[i],dp.rms(data_plot[mode_list[i]]),np.mean(data_plot[mode_list[i]]),np.std(data_plot[mode_list[i]]))
    # with open(r"E:\1Master_3\汇报\Image_20231029"+"\\" + site + "_dZTD_20Hours.txt",'a') as file:
    #     file.write(str_info + "\n")
    print(str_info)

#Plot H Sun

# [H_sun,time_sun] = dp.get_H_sun(year,mon,day,starttime,LastT,30,lat,lon)
# axP2 = axP.twinx()
# axP2.grid(False)
# axP2.plot(time_sun,H_sun,color = color_list[4],linewidth = 5)
# labels = axP2.get_yticklabels() + axP2.get_xticklabels()
# [label.set_fontsize(xtick_size) for label in labels]
# [label.set_fontname('Arial') for label in labels]
# axP2.spines['right'].set(color = color_list[4],linewidth = 2,linestyle = "-")
# axP2.set_ylabel("Elevation of Sun",font_label,color=color_list[4])
# axP2.tick_params(axis = 'y',length=6, width=2, color=color_list[4], labelcolor=color_list[4])

# plt.show()
# plt.savefig(r"E:\1Master_3\汇报\Image_20231029" + "\\" + site + "_WHT_20_Hours.png")

# RECON
con_list = [10,20,50,100]
max_recon_time = 3600
# cont_continue = int(max_recon_time/30)
cont_continue = 4
recovergence = 3600
con_position={}
for cur_mode in mode_list:
    if cur_mode not in con_position.keys():
        con_position[cur_mode] = {}
        for cur_accuracy in con_list:
            con_position[cur_mode][cur_accuracy] = []
for cur_mode in time_plot.keys():
    start_recon = False
    all_epoch = len(time_plot[cur_mode])
    i = 0
    while i < all_epoch:
        time_now = time_plot[cur_mode][i] * 3600
        if time_now % recovergence == 0:
            index_time_now = i
            for cur_accuracy in con_list:
                i = index_time_now
                con_position_num,con_horizontal_num,con_vertical_num = 0,0,0
                while i < all_epoch:
                    cur_time = time_plot[cur_mode][i] * 3600
                    position = abs(data_plot[cur_mode][i])
                    #= position =#
                    if position < cur_accuracy:
                        if con_position_num < cont_continue:
                            con_position_num = con_position_num + 1
                    elif con_position_num < cont_continue:
                        con_position_num = 0
                    if con_position_num == cont_continue:
                        con_position[cur_mode][cur_accuracy].append(time_plot[cur_mode][i-cont_continue+1]*3600 - time_now)
                        con_position_num = 9999999

                    if con_position_num == 9999999:
                        break
                    if cur_time - time_now > max_recon_time:
                        if con_position_num != 9999999:
                            con_position[cur_mode][cur_accuracy].append(max_recon_time)
                        break
                    i = i+1            
        else:
            i=i+1
            continue

for cur_mode in con_position.keys():
    for cur_accuracy in con_position[cur_mode].keys():
        str_recon = "{:<10} {:<3} mm {:.2f}".format(cur_mode,cur_accuracy,np.mean(con_position[cur_mode][cur_accuracy]))
        print(str_recon)

# con_per_hour
# figP,axP = plt.subplots(1,1,figsize=(17,8),sharey=True,sharex=True)
# X_FLOAT,X_FIXED,X_IONO = [],[],[]
# xtick_bar = []
# for i in range(22):
#     X_FLOAT.append(i-0.3)
#     X_FIXED.append(i)
#     X_IONO.append(i+0.3)
#     xtick_bar.append("{:0>2}".format(i+2))
# axP.bar(X_FLOAT,  con_position["FLOAT"][20],color=color_list[0],width=0.3)
# axP.bar(X_FIXED,  con_position["FIXED"][20],color=color_list[1],width=0.3)
# axP.bar(X_IONO,con_position["IONO_CON"][20],color=color_list[2],width=0.3)
# [H_sun,time_sun] = dp.get_H_sun(year,mon,day,starttime,LastT,30,lat,lon)
# axP2 = axP.twinx()
# axP2.grid(False)
# axP2.plot(time_sun,H_sun,color = color_list[4],linewidth = 5)
# labels = axP2.get_yticklabels() + axP2.get_xticklabels()
# [label.set_fontsize(xtick_size) for label in labels]
# [label.set_fontname('Arial') for label in labels]
# axP2.spines['right'].set(color = color_list[4],linewidth = 2,linestyle = "-")
# axP2.set_ylabel("Elevation of Sun",font_label,color=color_list[4])
# axP2.tick_params(axis = 'y',length=6, width=2, color=color_list[4], labelcolor=color_list[4])
# axP.set_xticks(X_FIXED)
# axP.set_xticklabels(xtick_bar)
# axP.set_xlabel("Time (GPST)",font_label)
# axP.set_ylabel("Convergence (s)",font_label)
# labels = axP.get_yticklabels() + axP.get_xticklabels()
# [label.set_fontsize(xtick_size) for label in labels]
# [label.set_fontname('Arial') for label in labels]
# axP.legend(mode_list,prop=font_legend,
#             framealpha=1,facecolor='w',ncol=3,numpoints=5, markerscale=5, 
#             bbox_to_anchor=(1,1.13),loc=1,borderaxespad=0)
plt.show()