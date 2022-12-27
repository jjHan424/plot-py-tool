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

plot_type = "3D"
plot_type = "3D"
step_start = 0
step_in = 0.005
last_end = 0.5
time = "UTC"
Fixed = True
year = 2021
mon = 11
day = 6
starttime = 10
LastT = 50/60
deltaT = 60/60
mode_list = ["Interpolation","Grid-1dm","Grid-Auto"]

# mode_list = ["Interpolation"]
site_list = ["SEPT","SEPT","SEPT"]
ENU_ALL = {}
#-----dynamic-------#
Direct3=r"E:\1Master_2\Paper_Grid\Dynamic"
filename_list = [Direct3 + "\\" + "client-Aug-" +  "310" + "-02" + "\\" + site_list[0] + "-GEC.flt",
                Direct3 + "\\" + "client-Grid-" + "310" + "-02" + "\\" + site_list[0] + "-GEC.flt",
                # Direct3 + "\\" + "client-Grid-" + "339" + "-06" + "\\" + site_list[0] + "-GEC.flt",
                # Direct3 + "\\" + "client-Grid-" + "310" + "-06" + "\\" + site_list[0] + "-GEC.flt",
                Direct3 + "\\" + "client-Grid_Ele-" + "310" + "-01" + "\\" + site_list[0] + "-GEC.flt",
                ]
filename_ref = [r"E:\1Master_2\Paper_Grid\Dynamic\2021310_WH\\Ref.txt",
                r"E:\1Master_2\Paper_Grid\Dynamic\2021339_WH\\Ref.txt",
                r"E:\1Master_2\Paper_Grid\Dynamic\2021339_WH\\Ref.txt",]
for i in range(len(mode_list)):
    data_Raw = rf.open_flt_pvtflt_file(filename_list[i])
    REF_XYZ = rf.open_pos_ref_IE(filename_ref[0])
    data_ENU = dp.XYZ2ENU_dynamic(XYZ = data_Raw,REF_XYZ = REF_XYZ)
    ENU_ALL[mode_list[i]] = data_ENU
#--------static-------#
# REF_XYZ = {
#            "HKSC":[-2414267.6255,5386768.7774,2407459.7930],
#            "HKTK":[-2418093.0695,5374658.0963,2430428.9388],
#            "HKMW":[-2402484.8351,5395262.2062,2400726.7172],
#            "HKCL":[-2392741.6793,5397562.8528,2404757.6381],
#            "HKKS":[-2429526.6128,5377816.4032,2412152.4833],
#            "HKKT":[-2405144.6258,5385195.0303,2420032.2957],
#            "HKLM":[-2414046.6682,5391602.1234,2396878.6406],
#            "HKLT":[-2399063.4601,5389237.6196,2417326.8134],
#            "HKNP":[-2392360.9915,5400226.0468,2400094.2194],
#            "HKOH":[-2423817.6243,5386056.8703,2399883.1266],
#            "HKPC":[-2405183.7237,5392541.5974,2403645.4824],
#            "HKSL":[-2393383.1399,5393860.9488,2412592.1665],
#            "HKSS":[-2424425.8236,5377187.9503,2418617.5000],
#            "HKST":[-2417143.5996,5382345.2556,2415036.7024],
#            "HKWS":[-2430579.7341,5374285.4508,2418956.0864],
#            "T430":[-2411015.9437,5380265.4823,2425132.4516],
#            "WUDA":[-2267761.1226,5009370.8398,3220970.5620],
#            "WHYJ":[-2252813.6375,4973121.8230,3286531.2991],
#            "N028":[-2191056.9474,5053129.9334,3205815.9843],
#            "N004":[-2334707.5108,5037347.5734,3128918.7498],
#            "N047":[-2350716.9193,4955782.5391,3244265.6248],
#            "N068":[-2222210.0878,4963941.9216,3320986.9437],
#            "WHDS":[-2309234.0723,4998958.4644,3207719.1445],
#            "WHSP":[-2277732.7853,5031747.7356,3179072.7779],
#            "WHXZ":[-2299689.3578,4975638.9471,3250284.4212],
#            "XGXN":[-2220831.1399,5007544.3179,3256075.5381],
#            "A010":[-2175297.1093,4330326.1005,4133584.2591],
#            "K042":[-2132034.8536,4509248.5850,3961882.4343],
#            "K057":[-2061539.3542,4485887.5744,4026181.9595],
#            "K059":[-2211742.6097,4402276.4734,4037240.8884],
#            "K101":[-2044552.7122,4330957.9318,4200451.9052],
#            "V092":[-1980661.4288,4556162.0565,3989739.6921],
#            }
# DirectT=r"E:\1Master_2\Paper_Grid\Res_FromServer_New\Client-Trp"
# Site = "HKSC"
# doy = tr.ymd2doy(year,mon,day,0,0,00)
# cdoy = "{:0>3}".format(doy)
# filename_list = [
#             # DirectT + "\\client-Aug-" + cdoy + "-02" + "\\" + Site + "-GEC.flt",
#             DirectT + "\\client-Grid-" + cdoy + "-06" + "\\" + Site + "-GEC.flt",
#             # DirectT + "\\client-Grid_Ele_R-" + cdoy + "-01" + "\\" + Site + "-GEC.flt",
#             ]
# for i in range(len(mode_list)):
#     data_Raw = rf.open_flt_pvtflt_file(filename_list[i])
#     # data_Raw = rf.open_flt_ppplsq_file(filename_list[i])
#     data_ENU = dp.XYZ2ENU_const(XYZ = data_Raw,REF_XYZ = REF_XYZ,site = Site)
#     ENU_ALL[mode_list[i]] = data_ENU


#data_convert
data_all,plot_all,step_plot = {},{},{}
[XLabel,XTick,cov_Time,begT,LastT]=dr.xtick(time,year,mon,day,starttime,LastT,deltaT)
for cur_mode in ENU_ALL.keys():
    if cur_mode not in data_all.keys():
        data_all[cur_mode] = {}
        plot_all[cur_mode] = {}
        step_plot[cur_mode] = {}
        data_all[cur_mode]["3D"],data_all[cur_mode]["U"],data_all[cur_mode]["V"],data_all[cur_mode]["H"] = [],[],[],[]
        plot_all[cur_mode]["3D"],plot_all[cur_mode]["U"],plot_all[cur_mode]["V"],plot_all[cur_mode]["H"] = [],[],[],[]
        step_plot[cur_mode]["3D"],step_plot[cur_mode]["U"],step_plot[cur_mode]["V"],step_plot[cur_mode]["H"] = [],[],[],[]
    for cur_time in ENU_ALL[cur_mode].keys():
        plot_time = (cur_time-cov_Time) / 3600
        if ((plot_time >= begT and plot_time <= (begT + LastT))):
            if (Fixed and ENU_ALL[cur_mode][cur_time]["AMB"] == 0):
                continue
            if (ENU_ALL[cur_mode][cur_time]["PDOP"] > 5):
                continue
            D3 = math.sqrt(ENU_ALL[cur_mode][cur_time]["E"] * ENU_ALL[cur_mode][cur_time]["E"] + ENU_ALL[cur_mode][cur_time]["N"] * ENU_ALL[cur_mode][cur_time]["N"] +ENU_ALL[cur_mode][cur_time]["U"] * ENU_ALL[cur_mode][cur_time]["U"])
            U = abs(ENU_ALL[cur_mode][cur_time]["U"])
            H = math.sqrt(ENU_ALL[cur_mode][cur_time]["E"] * ENU_ALL[cur_mode][cur_time]["E"] + ENU_ALL[cur_mode][cur_time]["N"] * ENU_ALL[cur_mode][cur_time]["N"])
            data_all[cur_mode]["3D"].append(math.sqrt(ENU_ALL[cur_mode][cur_time]["E"] * ENU_ALL[cur_mode][cur_time]["E"] + ENU_ALL[cur_mode][cur_time]["N"] * ENU_ALL[cur_mode][cur_time]["N"] +ENU_ALL[cur_mode][cur_time]["U"] * ENU_ALL[cur_mode][cur_time]["U"]))
            data_all[cur_mode]["U"].append(abs(ENU_ALL[cur_mode][cur_time]["U"]))
            data_all[cur_mode]["H"].append(math.sqrt(ENU_ALL[cur_mode][cur_time]["E"] * ENU_ALL[cur_mode][cur_time]["E"] + ENU_ALL[cur_mode][cur_time]["N"] * ENU_ALL[cur_mode][cur_time]["N"]))

for cur_mode in data_all.keys():
    data_all[cur_mode]["3D"] = abs(data_all[cur_mode]["3D"] - np.mean(data_all[cur_mode]["3D"]))
    data_all[cur_mode]["U"] = abs(data_all[cur_mode]["U"] - np.mean(data_all[cur_mode]["U"]))
    data_all[cur_mode]["H"] = abs(data_all[cur_mode]["H"] - np.mean(data_all[cur_mode]["H"]))

test = []
while step_start < last_end:
    step_end = step_start + step_in
    step_plus = 0
    for cur_mode in data_all.keys():
        all_epoch = len(data_all[cur_mode]["3D"])
        num_epoch_3D,num_epoch_U,num_epoch_H = 0,0,0
        for ii in range(len(data_all[cur_mode]["3D"])):
            if step_start == -1:
                if data_all[cur_mode]["3D"][ii] <= step_end :
                    num_epoch_3D = num_epoch_3D + 1
                if data_all[cur_mode]["U"][ii] <= step_end :
                    num_epoch_U = num_epoch_U + 1
                if data_all[cur_mode]["H"][ii] <= step_end :
                    num_epoch_H = num_epoch_H + 1
            else:
                if data_all[cur_mode]["3D"][ii] > step_start and data_all[cur_mode]["3D"][ii] <= step_end :
                    num_epoch_3D = num_epoch_3D + 1
                if data_all[cur_mode]["U"][ii] > step_start and data_all[cur_mode]["U"][ii] <= step_end :
                    num_epoch_U = num_epoch_U + 1
                if data_all[cur_mode]["H"][ii] > step_start and data_all[cur_mode]["H"][ii] <= step_end :
                    num_epoch_H = num_epoch_H + 1
        # if abs(step_end - last_end)<step_in/100:
        #     num_epoch_3D,num_epoch_U,num_epoch_H = 0,0,0
        #     for ii in range(len(data_all[cur_mode]["3D"])):
        #         if data_all[cur_mode]["3D"][ii] > step_end:
        #             num_epoch_3D = num_epoch_3D + 1
        #         if data_all[cur_mode]["U"][ii] > step_end:
        #             num_epoch_U = num_epoch_U + 1
        #         if data_all[cur_mode]["H"][ii] > step_end:
        #             num_epoch_H = num_epoch_H + 1
        #     plot_all[cur_mode]["3D"].append(num_epoch_3D/all_epoch*100)
        #     plot_all[cur_mode]["U"].append(num_epoch_U/all_epoch*100)
        #     plot_all[cur_mode]["H"].append(num_epoch_H/all_epoch*100)
        #     step_plot[cur_mode]["3D"].append((step_start + step_end)/2+step_plus)
        # else:
        plot_all[cur_mode]["3D"].append(num_epoch_3D/all_epoch*100)
        plot_all[cur_mode]["U"].append(num_epoch_U/all_epoch*100)
        plot_all[cur_mode]["H"].append(num_epoch_H/all_epoch*100)
        step_plot[cur_mode]["3D"].append((step_start + step_end)/2+step_plus)
            # step_plus = step_plus + step_in/3
        step_plus = 0
    step_start = step_start + step_in
D3,U,H = 0,0,0
for cur_mode in plot_all.keys():
    print(np.sum(np.array(plot_all[cur_mode]["3D"][0:10])))
    print(np.sum(np.array(plot_all[cur_mode]["U"])))
    print(np.sum(np.array(plot_all[cur_mode]["H"])))

#plot
bottomm = []
for ii in range(len(plot_all[mode_list[0]]["3D"])):
    bottomm.append(plot_all[mode_list[0]]["3D"][ii]+plot_all[mode_list[1]]["3D"][ii])

if plot_type == "3D":
    figP,axP = plt.subplots(1,1,figsize=(15,8.5),sharey=True,sharex=True)
    for ii in range(len(mode_list)):
        if ii == 1:
            axP.bar(step_plot[mode_list[ii]]["3D"],plot_all[mode_list[ii]]["3D"],width = step_in,bottom=plot_all[mode_list[ii-1]]["3D"],label='value')
        if ii == 2:
            axP.bar(step_plot[mode_list[ii]]["3D"],plot_all[mode_list[ii]]["3D"],width = step_in,bottom=bottomm,label='value')
        if ii == 0:
            axP.bar(step_plot[mode_list[ii]]["3D"],plot_all[mode_list[ii]]["3D"],width = step_in,label='value')
    # for ii in range(len(mode_list)):
    #     axP.plot(step_plot[mode_list[ii]]["3D"],plot_all[mode_list[ii]]["3D"],linewidth = 5)
    font = {'family': 'Times new roman','weight': 600,'size': 23}
    axP.set_ylabel("Percentage(%)",font)
    axP.set_xlabel("Position Errors(m)",font)
    labels = axP.get_xticklabels() + axP.get_yticklabels()
    [label.set_fontsize(18) for label in labels]
    [label.set_fontname('Times New Romam') for label in labels]
    font = {'family': 'Times new roman','weight': 600,'size': 20}
    axP.legend(mode_list,prop=font,
            framealpha=1,facecolor='none',ncol=1,numpoints=5,markerscale=5, 
            borderaxespad=0,loc=1) 



if plot_type == "2D":
    figP,axP = plt.subplots(1,2,figsize=(15,8),sharey=True,sharex=True)
    for cur_mode in plot_all.keys():
        axP[0].bar(step_plot[cur_mode]["3D"],plot_all[cur_mode]["H"],width = step_in,label='value')
        axP[1].bar(step_plot[cur_mode]["3D"],plot_all[cur_mode]["U"],width = step_in,label='value')
# plt.savefig(r"E:\1Master_2\Paper_Grid\1-Paper_word\Image-1\SEPT-Precent-Bar-310.svg")
# plt.savefig(r"E:\1Master_2\Paper_Grid\1-Paper_word\Image-1\SEPT-Precent-Bar-310.png",dpi=600)
plt.show()
print("HJJ")
