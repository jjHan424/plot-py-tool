'''
Author: HanJunjie
Date: 2021-11-29 21:26:38
LastEditTime: 2022-09-02 11:04:15
LastEditors: HanJunjie HanJunjie@whu.edu.cn
Description: 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
FilePath: /plot-py-tool/main/draw_flt.py
'''
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

REF_XYZ = {"HKLM":[-2414046.6433,5391602.1169,2396878.6436],
           "HKSC":[-2414267.6255,5386768.7774,2407459.7930],
           "HKTK":[-2418093.0695,5374658.0963,2430428.9388],
           "2008":[-2400517.6874,5373926.9119,2449368.0923],
           "WUDA":[-2267761.1226,5009370.8398,3220970.5620],
           "E033":[-2340806.3769,4922578.9320,3302011.8419],
           "N047":[-2350716.9401,4955782.5397,3244265.6251],
           "2017":[-2424178.5320,5365092.3806,2445506.8814],
           '2010':[-2419056.7812,5364365.3435,2452055.3961],
           "SGGW":[ -2267804.6138,5009342.3946,3220991.8459],
           "N032":[-2141844.0708,5071953.6039,3209315.6304],
           "HKMW":[-2402484.8351,5395262.2062,2400726.7172],
           "WHYJ":[-2252813.6375,4973121.8230,3286531.2991],
           "N028":[-2191056.9474,5053129.9334,3205815.9843]}
ENU_ALL = {}
#mode_list = ["HKLM","HKSC","HKTK"]
#mode_list = ["GEC","G","E","C","GE"]#,"4 Sites Grid","3 Sites MLCM"]
# mode_list = ["MLCM","Grid","Grid-Self","Grid-2"]#,"Omc","Rank"]
# mode_list = ["MLCM","Grid","Grid-Chk","Grid_Ele"]
# mode_list = ["Grid","Wgt-Chk","Ele-Self","Ele-WH"]
# mode_list = ["Grid","Wgt-Chk","Old"]
# mode_list = ["Aug","Grid","Grid_Chk","Ele8","Ele10"]
# mode_list = ["ALL-1","Site-1","ALL-2","Site-2"]
# mode_list = ["MLCM","Grid","Grid-Chk"]
# mode_list = ["Grid","Grid-Self","Grid-2"]
#mode_list = ["GRID"]#,"Omc","Rank"]
# site_list = ["WUDA","WHYJ","N028"]
#site_list = ["WUDA","WUDA","WUDA"]
# Site = "WUDA"
# site_list = ["WUDA","WHYJ","N028","HKSC","HKMW","HKTK"]
mode_list = ["Grid","Chk","Ele-HK","Ele-WH"]
site_list = ["HKMW"]
# site_list = "HKSC"
# Y=2021
# M=10
# D=28
# S=2
# L=22
# count = 11
Sig = 0
SavePath=r"E:\1Master_2\Paper_Grid\Res_FromServer_New\Fig\Pos4-New-11_Sigma"
if (not os.path.exists(SavePath)):
    os.mkdir(SavePath)
# for j in range(len(site_list)):
    
#     SavePathSite = SavePath + "\\" + site_list[j] + "-Sigma-"+"{:0>1}".format(Sig)+".txt"
#     with open(SavePathSite,'a') as file:
#         file.write("Doy    ")
#         for i in range(len(mode_list)):
#             file.write("Fix1-{}     ".format(mode_list[i]))
#         for i in range(len(mode_list)):
#             file.write("Fix2-{}     ".format(mode_list[i]))
#         file.write("       ")
#         for i in range(len(mode_list)):
#             file.write("E-{}        ".format(mode_list[i]))
#         for i in range(len(mode_list)):
#             file.write("N-{}          ".format(mode_list[i]))
#         for i in range(len(mode_list)):
#             file.write("U-{}          ".format(mode_list[i]))
#         file.write("\n")

for j in range(len(site_list)):
    Site = site_list[j]
    Y=2021
    M=11
    D=7
    S=17.5
    L=1.5
    count = 1
    Direct=r"E:\1Master_2\Paper_Grid\Res_FromServer_New\Client-SetRef"
    
    while count > 0:
        D = D + 1
        count = count - 1
        if (D > 31):
            D = 1
            M = M + 1
        doy = tr.ymd2doy(Y,M,D,0,0,00)
        cdoy = "{:0>3}".format(doy)
        # filename_list = [
        #     # Direct + "\\client-Aug-" + cdoy + "\\" + Site + "-GEC.flt",
        #     Direct + "\\client-Grid-" + cdoy + "\\" + Site + "-GEC.flt", 
        #     Direct + "\\client-Grid_Chk-" + cdoy + "\\" + Site + "-GEC.flt",
        #     Direct + "\\client-Grid_Ele-8-" + cdoy + "\\" + Site + "-GEC.flt",
        #     # Direct + "\\client-Grid_Ele-9-" + cdoy + "\\" + Site + "-GEC.flt",
        #     Direct + "\\client-Grid_Ele-10-" + cdoy + "\\" + Site + "-GEC.flt",
        #     # Direct + "\\client-Grid_Ele-6-" + cdoy + "\\" + Site + "-GEC.flt",
        #     # Direct + "\\client-Grid_Ele-7-" + cdoy + "\\" + Site + "-GEC.flt",
        #     # Direct + "\\client-Grid_Ele-8-" + cdoy + "\\" + Site + "-GEC.flt"
        #     # Direct + "\\client-New-Grid-" + cdoy + "\\" + Site + "-GEC.flt", 
        #     # Direct + "\\client-New-Grid_Chk-" + cdoy + "\\" + Site + "-GEC.flt",
        #     # Direct + "\\client-New-Grid_Ele-" + cdoy + "\\" + Site + "-GEC.flt"
        #     # r"E:\1Master_2\Paper_Grid\Pro_20211205-339\client\HKSC-GEC-1.flt",
        #                 ]
        filename_list = [
            r"E:\1Master_2\Paper_Grid\Pro_20211107-312\client_SetRef\HKMW-GEC-Grid.flt",
            r"E:\1Master_2\Paper_Grid\Pro_20211107-312\client_SetRef\HKMW-GEC-Chk.flt",
            r"E:\1Master_2\Paper_Grid\Pro_20211107-312\client_SetRef\HKMW-GEC-ELE-HKMW.flt",
            r"E:\1Master_2\Paper_Grid\Pro_20211107-312\client_SetRef\HKMW-GEC-ELE-N028.flt",
                        ]
        for i in range(len(mode_list)):
            data_Raw = rf.open_flt_pvtflt_file(filename_list[i])
            # data_Raw = rf.open_flt_ppplsq_file(filename_list[i])
            data_ENU = dp.XYZ2ENU_const(XYZ = data_Raw,REF_XYZ = REF_XYZ,site = Site)
            ENU_ALL[mode_list[i]] = data_ENU
            
        dr.plot_e_n_u(site =Site, data = ENU_ALL,type = ["E","N","U"],mode = mode_list,ylim = 1,starttime=S,LastT=L,deltaT=0.25,time = "UTC",all=False,Fixed=False,delta_data = 5,year = Y,mon=M,day=D,Sigma=3,Sigma_num=Sig,save=SavePath,show=True)
        # if (count == 0 and M!=12):
        #     count = 1
        #     M=12
        #     D=4
