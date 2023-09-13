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
import trans as tr
#--------DOUBLE---------#
# diff_path_1 = r"E:\1Master_2\3-IUGG\Pro_2023001_Aug2Grid\Grid_Cross_REC_CRD\BADH-GEC-30.diff"
# diff_path_2 = r"E:\1Master_2\3-IUGG\Pro_2023001_Aug2Grid\Grid_Cross_REC_CRD\KLOP-GEC-30.diff"

# aug_path_1 = r"E:\1Master_2\3-IUGG\Pro_2023001_Aug2Grid\server\BADH-GEC.aug"
# aug_path_2 = r"E:\1Master_2\3-IUGG\Pro_2023001_Aug2Grid\server\KLOP-GEC.aug"
# outdir = r"E:\1Master_2\3-IUGG\Pro_2023001_Aug2Grid\Grid_BADH_KLOP_WARE_EIJS\Test"

# [head_1,data_1] = rf.open_aug_file_new(diff_path_1)
# [head_1,aug_1] = rf.open_aug_file_new(aug_path_1)
# [head_2,data_2] = rf.open_aug_file_new(diff_path_2)
# [head_2,aug_2] = rf.open_aug_file_new(aug_path_2)
# [week,sow]=tr.ymd2gpst(2023,1,1,0,0,00)

# sys_dIon = {"C":"dION2","E":"dION1","G":"dION1"}
# for cur_time in data_1.keys():
#     if cur_time not in data_2.keys():
#         continue
#     if cur_time >= 86130:
#         break
#     delta_sow = cur_time - sow
#     cur_hour = int (delta_sow / 3600)
#     cur_min = int ((delta_sow - cur_hour*3600) / 60)
#     cur_sec = int ((delta_sow - cur_hour*3600 - 60 * cur_min))
#     for cur_sat in data_1[cur_time].keys():
#         write_string = "{:0>2d} {:0>2d} {:0>2d}   ".format(cur_hour,cur_min,cur_sec)
#         if cur_sat not in data_2[cur_time].keys():
#             continue
#         # write_string = write_string + "{:.4f}   {:.4f}\n".format(data_1[cur_time][cur_sat][sys_dIon[cur_sat[0]]],data_2[cur_time][cur_sat][sys_dIon[cur_sat[0]]])
#         write_string = write_string + "{:.4f} {:.4f} {:.4f} {:.4f} {:.4f}   {:.4f} {:.4f} {:.4f} {:.4f} {:.4f}\n".format(aug_1[cur_time][cur_sat]["ELE"],aug_1[cur_time][cur_sat]["AZI"],aug_1[cur_time][cur_sat]["IPP_LAT"],aug_1[cur_time][cur_sat]["IPP_LON"],data_1[cur_time][cur_sat][sys_dIon[cur_sat[0]]],aug_2[cur_time][cur_sat]["ELE"],aug_2[cur_time][cur_sat]["AZI"],aug_2[cur_time][cur_sat]["IPP_LAT"],aug_2[cur_time][cur_sat]["IPP_LON"],data_2[cur_time][cur_sat][sys_dIon[cur_sat[0]]])
#         with open(outdir+"-"+cur_sat,'a') as file:
#             file.write(write_string)

##-------------ALL----------##
# site_list = ["TERS","IJMU","DELF","VLIS","DENT","WSRT","KOS1","BRUX","DOUR","WARE","REDU","EIJS","TIT2","EUSK","DILL","DIEP","BADH","KLOP","FFMJ","KARL","HOBU","PTBB","GOET"]
# site_list = ["FFMJ","GOET","HOBU","REDU","TERS","TIT2","VLIS"]
# site_list = ["N028","N047","N068","WHDS","WHSP","WHXZ","WHYJ","WUDA","XGXN"]
site_list = ["HKTK","T430","HKLT","HKKT","HKSS","HKWS","HKSL","HKST","HKKS","HKCL","HKSC","HKPC","HKNP","HKMW","HKLM","HKOH"]
reference_site = "HKSC"
# site_list = ["TERS","IJMU","DELF"]
diff_all,aug_all = {},{}
[week,sow]=tr.ymd2gpst(2021,11,6,0,0,00)
for cur_site in site_list:
    
    diff_path = r"E:\1Master_2\3-IUGG\Pro_2021310_Aug2Grid\Grid_Cross_HK" + "\\" + cur_site + "-GEC-5.diff"
    aug_path = r"E:\1Master_2\3-IUGG\Pro_2021310_Aug2Grid\server_BDS2" + "\\" + cur_site + "-GEC.aug"
    [head,data] = rf.open_aug_file_new(diff_path)
    [head,aug] = rf.open_aug_file_new(aug_path)
    diff_all[cur_site] = data
    aug_all[cur_site] = aug
outdir = r"E:\1Master_2\3-IUGG\Pro_2021310_Aug2Grid\Grid_Cross_HK\ALL"
sys_dIon = {"C":"dION2","E":"dION1","G":"dION1"}
for cur_time in diff_all[reference_site]:
    same_time,same_sat = True,True
    for cur_site in site_list:
        if cur_time not in diff_all[cur_site].keys():
            same_time = False
            break
        if cur_time not in aug_all[cur_site].keys():
            same_time = False
            break
    delta_sow = cur_time - sow
    if delta_sow >= 86130:
        break
    if not same_time:
        continue
    
    cur_hour = int (delta_sow / 3600)
    cur_min = int ((delta_sow - cur_hour*3600) / 60)
    cur_sec = int ((delta_sow - cur_hour*3600 - 60 * cur_min))
    for cur_sat in diff_all[reference_site][cur_time]:
        same_sat = True
        for cur_site in site_list:
            if cur_sat not in diff_all[cur_site][cur_time].keys():
                same_sat = False
                break
            if cur_sat not in aug_all[cur_site][cur_time].keys():
                same_sat = False
                break
        if not same_sat:
            continue
        write_string = "{:0>2d} {:0>2d} {:0>2d}".format(cur_hour,cur_min,cur_sec)
        for cur_site in site_list:
            write_string = write_string + "    {:.4f} {:.4f} {:.4f} {:.4f} {:.4f}".format(aug_all[cur_site][cur_time][cur_sat]["ELE"],aug_all[cur_site][cur_time][cur_sat]["AZI"],aug_all[cur_site][cur_time][cur_sat]["IPP_LAT"],aug_all[cur_site][cur_time][cur_sat]["IPP_LON"],diff_all[cur_site][cur_time][cur_sat][sys_dIon[cur_sat[0]]])
        with open(outdir+"-"+cur_sat,'a') as file:
            file.write(write_string + "\n")

# for cur_time in data_1.keys():
#     if cur_time not in data_2.keys():
#         continue
#     if cur_time >= 86130:
#         break
#     delta_sow = cur_time - sow
#     cur_hour = int (delta_sow / 3600)
#     cur_min = int ((delta_sow - cur_hour*3600) / 60)
#     cur_sec = int ((delta_sow - cur_hour*3600 - 60 * cur_min))
#     for cur_sat in data_1[cur_time].keys():
#         write_string = "{:0>2d} {:0>2d} {:0>2d}   ".format(cur_hour,cur_min,cur_sec)
#         if cur_sat not in data_2[cur_time].keys():
#             continue
#         # write_string = write_string + "{:.4f}   {:.4f}\n".format(data_1[cur_time][cur_sat][sys_dIon[cur_sat[0]]],data_2[cur_time][cur_sat][sys_dIon[cur_sat[0]]])
#         write_string = write_string + "{:.4f} {:.4f} {:.4f} {:.4f} {:.4f}   {:.4f} {:.4f} {:.4f} {:.4f} {:.4f}\n".format(aug_1[cur_time][cur_sat]["ELE"],aug_1[cur_time][cur_sat]["AZI"],aug_1[cur_time][cur_sat]["IPP_LAT"],aug_1[cur_time][cur_sat]["IPP_LON"],data_1[cur_time][cur_sat][sys_dIon[cur_sat[0]]],aug_2[cur_time][cur_sat]["ELE"],aug_2[cur_time][cur_sat]["AZI"],aug_2[cur_time][cur_sat]["IPP_LAT"],aug_2[cur_time][cur_sat]["IPP_LON"],data_2[cur_time][cur_sat][sys_dIon[cur_sat[0]]])
#         with open(outdir+"-"+cur_sat,'a') as file:
#             file.write(write_string)