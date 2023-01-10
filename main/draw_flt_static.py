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

REF_XYZ = {
           "HKSC":[-2414267.6255,5386768.7774,2407459.7930],
           "HKTK":[-2418093.0695,5374658.0963,2430428.9388],
           "HKMW":[-2402484.8351,5395262.2062,2400726.7172],
           "HKCL":[-2392741.6793,5397562.8528,2404757.6381],
           "HKKS":[-2429526.6128,5377816.4032,2412152.4833],
           "HKKT":[-2405144.6258,5385195.0303,2420032.2957],
           "HKLM":[-2414046.6682,5391602.1234,2396878.6406],
           "HKLT":[-2399063.4601,5389237.6196,2417326.8134],
           "HKNP":[-2392360.9915,5400226.0468,2400094.2194],
           "HKOH":[-2423817.6243,5386056.8703,2399883.1266],
           "HKPC":[-2405183.7237,5392541.5974,2403645.4824],
           "HKSL":[-2393383.1399,5393860.9488,2412592.1665],
           "HKSS":[-2424425.8236,5377187.9503,2418617.5000],
           "HKST":[-2417143.5996,5382345.2556,2415036.7024],
           "HKWS":[-2430579.7341,5374285.4508,2418956.0864],
           "T430":[-2411015.9437,5380265.4823,2425132.4516],
           "WUDA":[-2267761.1226,5009370.8398,3220970.5620],
           "WHYJ":[-2252813.6375,4973121.8230,3286531.2991],
           "N028":[-2191056.9474,5053129.9334,3205815.9843],
           "N004":[-2334707.5108,5037347.5734,3128918.7498],
           "N047":[-2350716.9193,4955782.5391,3244265.6248],
           "N068":[-2222210.0878,4963941.9216,3320986.9437],
           "WHDS":[-2309234.0723,4998958.4644,3207719.1445],
           "WHSP":[-2277732.7853,5031747.7356,3179072.7779],
           "WHXZ":[-2299689.3578,4975638.9471,3250284.4212],
           "XGXN":[-2220831.1399,5007544.3179,3256075.5381],
           "A010":[-2175297.1093,4330326.1005,4133584.2591],
           "K042":[-2132034.8536,4509248.5850,3961882.4343],
           "K057":[-2061539.3542,4485887.5744,4026181.9595],
           "K059":[-2211742.6097,4402276.4734,4037240.8884],
           "K101":[-2044552.7122,4330957.9318,4200451.9052],
           "V092":[-1980661.4288,4556162.0565,3989739.6921],
           "K070":[-2059482.5470,4437621.0251,4080017.7148],
           }
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
# site_list = ["HKSC"]
# Site = "WUDA"
# site_list = ["WUDA","WHYJ","N028","HKSC","HKMW","HKTK"]
# site_list = ["HKSC","HKMW","HKTK"]
# site_list = ["WUDA","HKSC"]
# site_list = ["HKTK","T430","HKLT","HKKT","HKSS","HKWS","HKSL","HKST","HKKS","HKCL","HKSC","HKPC","HKNP","HKMW","HKLM","HKOH","WHYJ","WHXZ","WHDS","WHSP","N028","N047","N068","XGXN","WUDA"]
# site_list = ["WHYJ","WHXZ","WHDS","WHSP","N028","N047","N068","XGXN","WUDA","K042","K057","K059","K101","A010","V092","HKTK","T430","HKLT","HKKT","HKSS","HKWS","HKSL","HKST","HKKS","HKCL","HKSC","HKPC","HKNP","HKMW","HKLM","HKOH"]
# site_list = ["HKTK","T430","HKLT","HKKT","HKSS","HKWS","HKSL","HKST","HKKS","HKCL","HKSC","HKPC","HKNP","HKMW","HKLM","HKOH"]
site_list = ["HKSC"]
mode_list = ["1","2","3"]
# mode_list = ["Aug","Grid-2","Grid-4","Coef","Coef-R","Chk"]
# mode_list = ["Interpolation"]
Sig = 0
# SavePath=r"D:\1Master_2\Paper_Grid\Res_FromServer_New\Fig\Pos-Trp\Aug"
SavePath=r"D:\A-paper\Test-Trp"
S=13
if (not os.path.exists(SavePath)):
    os.mkdir(SavePath)
for j in range(len(site_list)):
    
    SavePathSite = SavePath + "\\" + site_list[j] + "-Sigma-"+"{:0>1}".format(Sig) + "-{:0>2}".format(S)+".txt"
    # with open(SavePathSite,'a') as file:
    #     file.write("Doy    ")
    #     for i in range(len(mode_list)):
    #         file.write("Fix1-{}     ".format(mode_list[i]))
    #     for i in range(len(mode_list)):
    #         file.write("Fix2-{}     ".format(mode_list[i]))
    #     file.write("       ")
    #     for i in range(len(mode_list)):
    #         file.write("E-{}        ".format(mode_list[i]))
    #     for i in range(len(mode_list)):
    #         file.write("N-{}          ".format(mode_list[i]))
    #     for i in range(len(mode_list)):
    #         file.write("U-{}          ".format(mode_list[i]))
    #     file.write("\n")

for j in range(len(site_list)):
    Site = site_list[j]
    Y=2021
    M=11
    D=2
    L=12
    DDD = 1
    count = 1
    DirectI=r"E:\1Master_2\Paper_Grid\Res_FromServer_New\Client-IonoWhite"
    Direct=r"E:\1Master_2\Paper_Grid\Res_FromServer_New\Client-All"
    DirectT=r"E:\1Master_2\Paper_Grid\Res_FromServer_New\Client-Trp"
    DirectCon = r"D:\A-paper\Project\Res_FromServer\Client_convergence"
    
    while count > 0:
        doy = tr.ymd2doy(Y,M,D,0,0,00)
        cdoy = "{:0>3}".format(doy)
        # filename_list = [
        #     # r"E:\1Master_2\Paper_Grid\Pro_20211205-339\client\WUDA.flt",
        #     # r"E:\1Master_2\Paper_Grid\Pro_20211205-339\client\WUDA-Chk.flt",
        #     # r"E:\1Master_2\Paper_Grid\Pro_20211205-339\client\WUDA-Coef.flt",
        #     DirectT + "\\client-Aug-" + cdoy + "-02" + "\\" + Site + "-GEC.flt",
        #     # DirectT + "\\client-Grid_Cor-" + cdoy + "-02" + "\\" + Site + "-GEC.flt",
        #     # DirectT + "\\client-Grid-" + cdoy + "-02" + "\\" + Site + "-GEC.flt",
        #     # DirectT + "\\client-Grid-" + cdoy + "-04" + "\\" + Site + "-GEC.flt",
        #     # DirectT + "\\client-Grid-" + cdoy + "-06" + "\\" + Site + "-GEC.flt",
        #     # DirectT + "\\client-Grid-" + cdoy + "-08" + "\\" + Site + "-GEC.flt",
        #     # Direct + "\\client-Grid-" + cdoy + "-10" + "\\" + Site + "-GEC.flt",
        #     # Direct + "\\client-Grid_Ele-" + cdoy + "-01" + "\\" + Site + "-GEC.flt",
        #     # Direct + "\\client-Grid_Ele-" + cdoy + "-02" + "\\" + Site + "-GEC.flt",
        #     # Direct + "\\client-Grid_Ele-" + cdoy + "-03" + "\\" + Site + "-GEC.flt",
        #     # Direct + "\\client-Grid_Ele_R-" + cdoy + "-01" + "\\" + Site + "-GEC.flt",
        #     # Direct + "\\client-Grid_Ele_R-" + cdoy + "-02" + "\\" + Site + "-GEC.flt",
            
        #     # Direct + "\\client-Trp-" + cdoy + "-02" + "\\" + Site + "-GEC.flt",
        #     # DirectT + "\\client-Grid_Ele_R-" + cdoy + "-01" + "\\" + Site + "-GEC.flt",
        #     # Direct + "\\client-Grid_Ele_R-" + cdoy + "-01" + "\\" + Site + "-GEC-Trp.flt",
        #     # DirectT + "\\client-Grid_Chk-" + cdoy + "-01" + "\\" + Site + "-GEC.flt",
        #     # DirectT + "\\client-Aug-" + cdoy + "-02" + "\\" + Site + "-GEC.flt",
        #     # DirectT + "\\client-Grid_Ele_R-" + cdoy + "-01" + "\\" + Site + "-GEC.flt",
        #                 ]

        filename_list = [
            DirectCon + "\\filter" +  "\\client-Aug-" + cdoy + "-02" + "\\" + Site + "-GEC.flt",
            DirectCon + "\\filter" +  "\\client-Aug-" + cdoy + "-04" + "\\" + Site + "-GEC.flt",
            # DirectCon + "\\filter" +  "\\client-Aug-" + cdoy + "-06" + "\\" + Site + "-GEC.flt",
            DirectCon + "\\filter" +  "\\client-Grid_Ele_R-" + cdoy + "-01" + "\\" + Site + "-GEC.flt",
            # DirectCon + "\\Trp-2" +  "\\client-Aug-" + cdoy + "-02" + "\\" + Site + "-GEC.flt",
            # DirectCon + "\\Trp-2" +  "\\client-Grid_Ele_R-" + cdoy + "-01" + "\\" + Site + "-GEC.flt",
            # r"G:\Data\Res\Client-Trp\client-Grid_Ele_R-306-01\WUDA-GEC.flt",
                        ]
        for i in range(len(mode_list)):
            data_Raw = rf.open_flt_pvtflt_file(filename_list[i])
            # data_Raw = rf.open_flt_ppplsq_file(filename_list[i])
            data_ENU = dp.XYZ2ENU_const(XYZ = data_Raw,REF_XYZ = REF_XYZ,site = Site)
            ENU_ALL[mode_list[i]] = data_ENU
            
        dr.plot_e_n_u(site =Site, data = ENU_ALL,type = ["E","N","U"],mode = mode_list,ylim = 0.5,starttime=S,LastT=L,deltaT=DDD,time = "UTC",all=False,Fixed=False,delta_data = 5,year = Y,mon=M,day=D,Sigma=3,Sigma_num=Sig,save=SavePath,show=True,recovergence=3600)
        D = D + 1
        count = count - 1
        # if (count == 0 and M!=12):
        #     count = 1
        #     M=12
        #     D=5
        if (D > 31):
            D = 1
            M = M + 1
