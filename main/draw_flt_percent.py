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
# site_list = ["HKTK","T430","HKLT","HKKT","HKSS","HKWS","HKSL","HKST","HKKS","HKCL","HKSC","HKPC","HKNP","HKMW","HKLM","HKOH"]
site_list = ["K057"]
# site_list = ["A010","V092","K059","K101"]
# site_list = ["K042","K057","N068","N028","N047"]
# site_list = ["WHSP","XGXN","WHXZ","WHYJ","WUDA","WHDS"]
# site_list = ["HKMW","HKLM","HKSC","HKPC","HKST","HKKT","HKSS","HKWS","T430","HKTK","HKLT","HKSL","HKKS","HKCL","HKNP","HKOH"]
# site_list = ["WUDA","WHYJ"]
# mode_list = ["Interpolation","Grid"]
mode_list = ["Interpolation-2","Interpolation-4","Interpolation-6","Grid"]
for cur_mode in mode_list:
    ENU_ALL[cur_mode] = {}
    for cur_site in site_list:
        ENU_ALL[cur_mode][cur_site]={}
DirectI=r"E:\1Master_2\Paper_Grid\Res_FromServer_New\Client-IonoWhite"
Direct=r"E:\1Master_2\Paper_Grid\Res_FromServer_New\Client-All"
DirectT=r"E:\1Master_2\Paper_Grid\Res_FromServer_New\Client-Trp"
# DirectCon = r"D:\A-paper\Project\Res_FromServer\Client_convergence"
# DirectCon = r"E:\1Master_2\Paper_Grid\Res_FromServer_New\Client_convergence-Site\Trp-0"
DirectCon = r"E:\1Master_2\Paper_Grid\Res_FromServer_New\Client_convergence-1s\Trp-2"
S=2
for Site in site_list:
    Y=2021
    M=10
    D=29
    L=6/60
    DDD = 1
    count = 6
    while count > 0:
        doy = tr.ymd2doy(Y,M,D,0,0,00)
        cdoy = "{:0>3}".format(doy)
        filename_list = [
            # r"E:\1Master_2\Paper_Grid\Pro_20211205-339\client\WUDA.flt",
            # r"E:\1Master_2\Paper_Grid\Pro_20211205-339\client\WUDA-Chk.flt",
            # r"E:\1Master_2\Paper_Grid\Pro_20211205-339\client\WUDA-Coef.flt",
            # DirectT + "\\client-Aug-" + cdoy + "-02" + "\\" + Site + "-GEC.flt",
            DirectCon + "\\client-Aug-" + cdoy + "-02" + "\\" + Site + "-GEC.flt",
            DirectCon + "\\client-Aug-" + cdoy + "-04" + "\\" + Site + "-GEC.flt",
            DirectCon + "\\client-Aug-" + cdoy + "-06" + "\\" + Site + "-GEC.flt",
            # DirectT + "\\client-Grid-" + cdoy + "-08" + "\\" + Site + "-GEC.flt",
            # Direct + "\\client-Grid-" + cdoy + "-10" + "\\" + Site + "-GEC.flt",
            # Direct + "\\client-Grid_Ele-" + cdoy + "-01" + "\\" + Site + "-GEC.flt",
            # Direct + "\\client-Grid_Ele-" + cdoy + "-02" + "\\" + Site + "-GEC.flt",
            # Direct + "\\client-Grid_Ele-" + cdoy + "-03" + "\\" + Site + "-GEC.flt",
            # Direct + "\\client-Grid_Ele_R-" + cdoy + "-01" + "\\" + Site + "-GEC.flt",
            # Direct + "\\client-Grid_Ele_R-" + cdoy + "-02" + "\\" + Site + "-GEC.flt",
            # Direct + "\\client-Trp-" + cdoy + "-02" + "\\" + Site + "-GEC.flt",
            DirectCon + "\\client-Grid_Ele_R-" + cdoy + "-01" + "\\" + Site + "-GEC.flt",
            # DirectT + "\\client-Grid_Chk-" + cdoy + "-01" + "\\" + Site + "-GEC.flt",
            # DirectT + "\\client-Grid_Ele_R-" + cdoy + "-01" + "\\" + Site + "-GEC.flt",
            ]
        # filename_list = [
        #     DirectCon + "\\filter" +  "\\client-Aug-" + cdoy + "-02" + "\\" + Site + "-GEC.flt",
        #     DirectCon + "\\filter" +  "\\client-Grid_Ele_R-" + cdoy + "-01" + "\\" + Site + "-GEC.flt",
        #     # DirectCon + "\\Trp-0"+ "\\client-Grid_Ele_R-" + cdoy + "-01" + "\\" + Site + "-GEC.flt",
        #                 ]
        S_Temp = S
        if cdoy != "308":
            while S_Temp < 24:
                for i in range(len(mode_list)):
                    data_Raw = rf.open_flt_pvtflt_file_percent(filename_list[i],Year=Y,Mon=M,Day=D,Hour=S_Temp,Last=L)
                    # data_Raw = rf.open_flt_ppplsq_file(filename_list[i])
                    data_ENU = dp.XYZ2ENU_const(XYZ = data_Raw,REF_XYZ = REF_XYZ,site = Site)
                    ENU_ALL[mode_list[i]][Site][cdoy+"{:0>2}".format(S_Temp)] = data_ENU
                S_Temp = S_Temp + 1
        D = D + 1
        count = count - 1
        # if (count == 0 and M!=12):
        #     count = 1
        #     M=12
        #     D=5
        if (D > 31):
            D = 1
            M = M + 1

dr.plot_e_n_u_percent(site ="10km", data = ENU_ALL,type = ["Position"],modelist = mode_list,sitelist = site_list,ylim = 0.25,starttime=S,LastT=L,deltaT=DDD,time = "UTC",all=False,Fixed=True,delta_data = 1,year = Y,mon=M,day=D,percent=0.7,show=True)
# dr.plot_e_n_u_percent(site ="10km", data = ENU_ALL,type = ["Horizontal","Vertical"],modelist = mode_list,sitelist = site_list,ylim = 0.5,starttime=S,LastT=L,deltaT=DDD,time = "UTC",all=False,Fixed=True,delta_data = 5,year = Y,mon=M,day=D,percent=0.6,show=True)