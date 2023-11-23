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
           "HKSC":[-2414267.6526,5386768.7552,2407459.7917],
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
            "BADH":[4042497.5636,612081.6986,4879251.2225],
            "BRUX":[4027881.6391,306998.8005,4919499.3955],
            "DELF":[3924687.7039,301132.7618,5001910.7712],
            "DENT":[4020711.7179,238851.4245,4928950.3991],
            "DIEP":[3842152.8194,563402.1377,5042888.5867],
            "DILL":[4132892.1702,485479.4981,4817740.6139],
            "DOUR":[4086778.3935,328452.3169,4869783.3870],
            "EIJS":[4023086.0249,400395.3758,4916655.7120],
            "EUSK":[4022105.9954,477011.3699,4910840.9268],
            "FFMJ":[4053455.6499,617729.9464,4869395.9060],
            "GOET":[3918911.7424,687523.9507,4968545.6780],
            "HOBU":[3778219.5479,698635.7113,5074054.4133],
            "IJMU":[3882052.7532,309346.7073,5034330.5815],
            "KARL":[4146524.1416,613138.3553,4791517.3758],
            "KLOP":[4041875.2299,620655.5809,4878637.0344],
            "KOS1":[3899613.5202,397362.1355,5014739.1067],
            "PTBB":[3844059.7256,709661.5969,5023129.7564],
            "REDU":[4091423.1164,368380.8753,4863179.9673],
            "TERS":[3798580.3535,346994.3397,5094781.1592],
            "TIT2":[3993787.0655,450204.1920,4936131.8827],
            "VLIS":[3975804.7213,249950.5991,4964446.4537],
            "WARE":[4031947.2820,370151.3545,4911906.5505],
            "WSRT":[3828735.8359,443305.2549,5064885.1890],
            "ES32":[-2232659.2519,5029348.8036,3214426.9336],
            "ES38":[-2253351.9081,5027804.0855,3202439.2626],
            # "ES43":[-2260116.4546,4991192.4489,3254167.3558],#CLK01
            "ES43":[-2260116.5742,4991192.4669,3254167.3800],
            "AHAQ":[-2502023.7806,4895810.7927,3222095.0954],
            "GZLH":[-2342399.0698,5388187.6595,2473904.3069],
            "JFNG":[-2279829.2449,5004706.4642,3219777.3940],
            "WUH2":[-2267750.3355,5009154.6262,3221294.4506],
            "SPT0":[3328984.3188,761910.5194,5369033.9330],
            "SPT7":[3328988.1263,761918.2170,5369031.8796],
            "TRO1":[2102928.1650,721619.6044,5958196.3742],
            "VARS":[1844608.5317,1109720.2844,5983941.4368],
           }
ENU_ALL = {}
# site_list = ["TERS","IJMU","DENT","WSRT","KOS1","BRUX","DOUR","WARE","REDU","EIJS","TIT2","EUSK","DILL","DIEP","BADH","KLOP","FFMJ","KARL","HOBU","PTBB","GOET"]
# site_list = ["HKTK","T430","HKLT","HKKT","HKSS","HKWS","HKSL","HKST","HKKS","HKCL","HKSC","HKPC","HKNP","HKMW","HKLM","HKOH"]
# site_list = ["EIJS","WSRT","BADH","KLOP","FFMJ"]
site_list = ["TRO1","VARS"]
# mode_list = ["Grid-1-1","Grid-5-5","Grid-5-1","Grid-Auto"]
# mode_list = ["1-1","2-1","3-1","4-1","5-1","6-1","7-1","8-1","5-5","Auto"]
# mode_list = ["FLOAT","FIXED","CORR","VIRTUAL"]
# mode_list = ["FLOAT","FIXED","IONO_CON"]
mode_list = ["PPP","IONO_CON"]
Sig = 0
# SavePath=r"D:\1Master_2\Paper_Grid\Res_FromServer_New\Fig\Pos-Trp\Aug"
SavePath=r"E:\1Master_2\3-IUGG\Result_Server\Client_20230704_5S\RES_30S_10"
S=0
if (not os.path.exists(SavePath)):
    os.mkdir(SavePath)
# for j in range(len(site_list)):
#     SavePathSite = SavePath + "\\" + site_list[j] + "-Sigma-"+"{:0>1}".format(Sig) + "-{:0>2}".format(S)+".txt"
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
    Y=2023
    M=1
    D=29
    L=4
    S=22
    DDD = 60/60
    count = 1
    # Direct = r"E:\1Master_2\3-IUGG\Result_Server\Client_20230629"
    Direct = r"E:\1Master_2\3-IUGG\Result_Server\Client_20230704_5S"
    while count > 0:
        
        doy = tr.ymd2doy(Y,M,D,0,0,00)
        # if doy == 313:
        #     D = D + 1
        #     count = count - 1
        #     continue
        cdoy = "{:0>3}".format(doy)
        cur_file_path = os.path.join(Direct,"{:0>4}{:0>3}_FLT".format(Y,doy))
        filename_list = [
            os.path.join(cur_file_path,Site+"-GEC"+"-Grid"+"-10-10.flt"),
            os.path.join(cur_file_path,Site+"-GEC"+"-Grid"+"-20-10.flt"),
            # os.path.join(cur_file_path,Site+"-GEC"+"-Grid"+"-30-10.flt"),
            # os.path.join(cur_file_path,Site+"-GEC"+"-Grid"+"-40-10.flt"),
            # os.path.join(cur_file_path,Site+"-GEC"+"-Grid"+"-50-10.flt"),
            # os.path.join(cur_file_path,Site+"-GEC"+"-Grid"+"-60-10.flt"),
            # os.path.join(cur_file_path,Site+"-GEC"+"-Grid"+"-70-10.flt"),
            # os.path.join(cur_file_path,Site+"-GEC"+"-Grid"+"-80-10.flt"),
            # os.path.join(cur_file_path,Site+"-GEC"+"-Grid"+"-50-50.flt"),
            os.path.join(cur_file_path,Site+"-GEC"+"-CROSS"+"-10-10.flt"),
                        ]
        filename_list = [
            # os.path.join(r"E:\1Master_3\2_ZTD\2021310\ShortBaseLine_RND_RECON",Site+"-GEC-FLOAT.flt"),
            # os.path.join(r"E:\1Master_3\2_ZTD\2021310\ShortBaseLine_RND_RECON",Site+"-GEC-FIXED.flt"),
            # os.path.join(r"E:\1Master_3\2_ZTD\2021310\ShortBaseLine_RND_RECON",Site+"-GEC-GRID-VIRTUAL.flt"),
            r"E:\1Master_3\2_ZTD\2023029\upd\TRO1-GEC-F.flt",
            r"E:\1Master_3\2_ZTD\2023029\upd\VARS-GEC-F.flt",
                        ]
        for i in range(len(mode_list)):
            # Site = site_list[0]
            if i <= 1:
                data_Raw = rf.open_flt_ppplsq_file(filename_list[i])
            else:
                data_Raw = rf.open_flt_pvtflt_file(filename_list[i])
                # data_Raw = rf.open_flt_pos_rtpppfile(filename_list[i])
                # data_Raw = rf.open_ppprtk_rtpppfile(filename_list[i])
                # data_Raw = rf.open_flt_ppp_rtpppfile(filename_list[i])
            
            data_ENU = dp.XYZ2ENU_const(XYZ = data_Raw,REF_XYZ = REF_XYZ,site = Site)
            ENU_ALL[mode_list[i]] = data_ENU
        # if doy != 305: 
        print(Site)   
        dr.plot_e_n_u(site =Site, data = ENU_ALL,type = ["E","N","U"],mode = mode_list,ylim = 0.5,starttime=S,LastT=L,deltaT=DDD,time = "UTC",all=False,Fixed=False,delta_data = 30,year = Y,mon=M,day=D,Sigma=3,Sigma_num=Sig,save=SavePath,show=True,recovergence=3600)
        
        # dr.plot_en_u(site =Site, data = ENU_ALL,type = ["EN","U"],mode = mode_list,ylim = 1,starttime=S,LastT=L,deltaT=DDD,time = "UTC",all=False,Fixed=True,delta_data = 5,year = Y,mon=M,day=D,Sigma=3,Sigma_num=Sig,save=SavePath,show=True,recovergence=3600)
        D = D + 1
        count = count - 1
        # if (count == 0 and M!=12):
        #     count = 1
        #     M=12
        #     D=5
        if (D > 31):
            D = 1
            M = M + 1
