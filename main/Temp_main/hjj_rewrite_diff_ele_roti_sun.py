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
import math
import glv

#input
Year,Mon,Day,Hour,lastT,DeltaT = 2022,3,1,2,22,2
site_list = ["IJMU","DENT","DOUR","WARE","EIJS","TIT2","EUSK","DILL","DIEP","BADH","KLOP","TERS","KARL","HOBU","PTBB","GOET"]
# site_list = ["IJMU"]
count = 15
site_dis = {"HKCL":10935.17,"HKKS":12728.06,"HKKT":12461.86,"HKLM":13558.71,"HKLT":13013.04,"HKMW":10929.05,"HKNP":13522.67,"HKOH":15347.92,"HKPC":11151.37,"HKSC":12022.27,"HKSL":12271.93,"HKSS":10709.62,"HKST":11528.54,"HKTK":15593.17,"HKWS":13806.22,"T430":12750.27}
# site_dis = {"N028":103250.46,
# "N047":91724.72,
# "N068":99345.21,
# "WHDS":63685.77,
# "WHSP":77501.56,
# "WHXZ":60809.10,
# "WHYJ":67798.80,
# "WUDA":56650.12,
# "XGXN":70440.29}
# site_dis = {"IJMU":144496.30,
# "KOS1":123953.19,
# "TIT2":95951.65,
# "DENT":130343.12,
# "BRUX":82249.78,
# "WARE":69038.59,
# "EIJS":71149.77,
# "EUSK":101645.88,
# "DOUR":86893.12,
# "REDU":89436.22,
# "BADH":93593.72,
# "DIEP":152990.58,
# "DILL":147646.35,
# "FFMJ":93005.28,
# "GOET":154343.77,
# "HOBU":200718.35,
# "KARL":148918.15,
# "KLOP":94998.27,
# "PTBB":170254.53,
# "TERS":170406.50,
# "WSRT":136628.15}
out_list = []
while count > 0:
    doy = tr.ymd2doy(Year,Mon,Day,0,0,00)
    # ele_sun = dp.ele_of_sun(31.6,113.4,Year,Mon,Day,Hour,lastT,5)
    ele_sun = dp.ele_of_sun(22.58,113.86,Year,Mon,Day,Hour,lastT,5)
    # ele_sun = dp.ele_of_sun(53.44,3.19,Year,Mon,Day,Hour,lastT,30)
    [week,sow]=tr.ymd2gpst(Year,Mon,Day,0,0,00)
    max_ele,max_time = 0,0
    for cur_time in ele_sun:
        if ele_sun[cur_time] > max_ele:
            max_ele = ele_sun[cur_time]
            max_time = cur_time
    for cur_site in site_dis.keys():
        
        diff_path = "/Users/hanjunjie/Master_3/1-IUGG/ResFromServer/Diff_Static_5S/{}{:0>3}/{}-GEC2-5.diff".format(Year,doy,cur_site)
        aug_path = "/Users/hanjunjie/Master_3/Data/{}/AUG_5S/{:0>3}/{}-GEC2-FIXED-5.aug".format(Year,doy,cur_site)
        roti_path = "/Users/hanjunjie/Master_3/1-IUGG/ResFromServer/ROTI_5S/{}{}{:0>3}_GEC.ismr".format(cur_site,Year,doy)
        if not os.path.exists(diff_path) or not os.path.exists(roti_path):
            continue
        # if not os.path.exists(aug_path):
        #     aug_path = "/Users/hanjunjie/Master_3/Data/{}/AUG/{:0>3}/{}-GEC.aug".format(Year,doy,cur_site)
        print("{}-{}".format(cur_site,doy))
        [head_I,diff] = rf.open_aug_file_new(diff_path)
        [head_I,aug] = rf.open_aug_file_new(aug_path)
        roti_data = rf.open_ismr(roti_path)
        for cur_time in diff.keys():
            if cur_time not in aug.keys() or cur_time not in roti_data.keys():
                continue
            for cur_sat in diff[cur_time].keys():
                if cur_sat not in aug[cur_time].keys() or cur_sat not in roti_data[cur_time].keys():
                    continue
                if diff[cur_time][cur_sat]["dION1"] == 0.0:
                    continue
                out_path = "/Users/hanjunjie/Master_3/1-IUGG/ResFromServer/Diff_Static_5S/HK_ION_ELE_ROTI_SUN_{}_5S.txt".format(cur_sat[0])
                # if out_path not in out_list:
                #     out_list.append(out_path)
                #     out_str = "PRN,IONDiff,EleSat,Roti,EleSun,Time,DisSite,DOY"
                #     with open(out_path,'a') as file:
                #         file.write(out_str + "\n")
                out_str = "{},{:>10.5f},{:>10.5f},{:>10.5f},{:>10.5f},{:>15},{:>15.5f},{:0>3}".format(cur_sat,diff[cur_time][cur_sat]["dION1"],aug[cur_time][cur_sat]["ELE"],roti_data[cur_time][cur_sat],ele_sun[cur_time],cur_time-sow,site_dis[cur_site],doy)
                with open(out_path,'a') as file:
                    file.write(out_str + "\n")
    count = count - 1
    Day = Day + 1      