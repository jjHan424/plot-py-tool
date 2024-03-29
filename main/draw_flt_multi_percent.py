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
            "BADH":[4042497.5659,612081.7044,4879251.2303],
            "BRUX":[4027881.3392,306998.7821,4919499.0337],
            "DENT":[4020711.2694,238851.3971,4928949.8416],
            "DIEP":[3842152.8088,563402.1405,5042888.5845],
            "DILL":[4132892.1699,485479.4990,4817740.6194],
            "DOUR":[4086777.9038,328452.2746,4869782.8018],
            "EIJS":[4023086.0205,400395.3754,4916655.7137],
            "EUSK":[4022105.9791,477011.3654,4910840.9136],
            "FFMJ":[4053455.6195,617729.9429,4869395.8771],
            "GOET":[3918911.7136,687523.9448,4968545.6512],
            "HOBU":[3778219.5166,698635.7021,5074054.3750],
            "IJMU":[3882052.7400,309346.7059,5034330.5759],
            "KARL":[4146524.1169,613138.3527,4791517.3498],
            "KLOP":[4041875.1891,620655.5731,4878636.9929],
            "KOS1":[3899613.4338,397362.1268,5014739.0067],
            "PTBB":[3844059.6900,709661.5900,5023129.7146],
            "REDU":[4091423.1110,368380.8769,4863179.9641],
            "TERS":[3798580.3478,346994.3368,5094781.1586],
            "TIT2":[3993787.0349,450204.1864,4936131.8507],
            "WARE":[4031946.9452,370151.3253,4911906.1508],
            "WSRT":[3828735.5991,443305.2281,5064884.8827]
           }
ENU_ALL = {}
site_list = ["TERS","IJMU","DENT","WSRT","KOS1","BRUX","DOUR","WARE","REDU","EIJS","TIT2","EUSK","DILL","DIEP","BADH","KLOP","FFMJ","KARL","HOBU","PTBB","GOET"]
site_list = ["KARL","IJMU","DENT","KOS1","BRUX","DOUR","WARE","REDU","EIJS","TIT2","EUSK","DILL","DIEP","BADH","KLOP","FFMJ","PTBB","GOET"]
site_list1 = ["BRUX","DOUR","WARE","REDU","EIJS","BADH","FFMJ","KLOP"]
site_list2 = ["KOS1","DENT","WSRT","TIT2","DIEP","EUSK"]
site_list3 = ["KARL","TERS","IJMU","HOBU","DILL","PTBB","GOET"]
# site_list = site_list1
# site_list = ["TERS","IJMU","DENT","WSRT","KOS1","BRUX","DOUR","WARE","REDU","EIJS","TIT2","EUSK","DILL"]
# site_list = ["TERS","IJMU","DENT"]
# site_list_string = "EIJS WARE EUSK TIT2 BRUX REDU DOUR KOS1 BADH KLOP FFMJ DILL DENT IJMU DIEP GOET WSRT PTBB HOBU"
# site_list = site_list_string.split(" ")
# site_list = ["HKTK","T430","HKLT","HKKT","HKSS","HKWS","HKSL","HKST","HKKS","HKCL","HKSC","HKPC","HKNP","HKMW","HKLM","HKOH"]
# site_list = ["WHYJ","WHXZ","WHDS","WHSP","N028","N047","N068","XGXN","WUDA"]
# mode_list = ["1-1","5-5","5-1","Auto"]
mode_list = ["PPP-AR","Fixed","Semiempirical","Auto"]
for cur_mode in mode_list:
    ENU_ALL[cur_mode] = {}
    for cur_site in site_list:
        ENU_ALL[cur_mode][cur_site]={}
S=2
for Site in site_list:
    # Site = site_list[j]
    Y=2021
    M=11
    D=7
    L=1
    DDD = 10
    count = 13
    Direct = r"/Users/hanjunjie/Master_3/1-IUGG/ResFromServer/CLIENT"
    while count > 0:
        doy = tr.ymd2doy(Y,M,D,0,0,00)
        cdoy = "{:0>3}".format(doy)
        cur_file_path = os.path.join(Direct,"{:0>4}{:0>3}_FLT".format(Y,doy))
        filename_list = [
            os.path.join(Direct,"FLT_PPPAR",  "{}{:0>3}".format(Y,doy),"{}-GEC3-FIXED-0-30-3600.flt".format(Site)),
            os.path.join(Direct,"FLT_CON",  "{}{:0>3}".format(Y,doy),"{}-GEC3-FIXED-0-30-3600.flt".format(Site)),
            os.path.join(Direct,"FLT_COEF", "{}{:0>3}".format(Y,doy),"{}-GEC3-FIXED-0-30-3600.flt".format(Site)),
            os.path.join(Direct,"FLT_CROSS","{}{:0>3}".format(Y,doy),"{}-GEC3-FIXED-0-30-3600.flt".format(Site)),
                        ]
        if not os.path.exists(os.path.join(Direct,"FLT_COEF", "{}{:0>3}".format(Y,doy),"{}-GEC3-FIXED-0-30-3600.flt".format(Site))):
            D = D + 1
            count = count - 1
            continue
        S_Temp = S
        while S_Temp < 24:
            for i in range(len(mode_list)):
                data_Raw = rf.open_flt_pvtflt_file_percent(filename_list[i],Year=Y,Mon=M,Day=D,Hour=S_Temp,Last=L)
                data_ENU = dp.XYZ2ENU_const(XYZ = data_Raw,REF_XYZ = REF_XYZ,site = Site)
                ENU_ALL[mode_list[i]][Site][cdoy+"{:0>2}".format(S_Temp)] = data_ENU
            S_Temp = S_Temp + 1
            if S_Temp == 8:
                S_Temp = 17
        D = D + 1
        count = count - 1
        # if (count == 0 and M!=12):
        #     count = 1
        #     M=12
        #     D=5
        if (D > 31):
            D = 1
            M = M + 1

dr.plot_e_n_u_multi_percent(site ="10km", data = ENU_ALL,type = ["Horizontal","Vertical"],modelist = mode_list,sitelist = site_list,ylim = 25,starttime=S,LastT=L,deltaT=DDD,time = "UTC",all=False,Fixed=False,delta_data = 30,year = Y,mon=M,day=D,percent=0.9,show=True)
# dr.plot_e_n_u_percent(site ="10km", data = ENU_ALL,type = ["Horizontal","Vertical"],modelist = mode_list,sitelist = site_list,ylim = 0.5,starttime=S,LastT=L,deltaT=DDD,time = "UTC",all=False,Fixed=True,delta_data = 5,year = Y,mon=M,day=D,percent=0.6,show=True)