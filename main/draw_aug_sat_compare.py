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
import trans as tr
aug_path_1 = [r"E:\1Master_2\3-IUGG\server_AUG_ELE\2021310\New_UC_5S_5S\WHYJ-GEC.aug",
            #   r"E:\1Master_2\3-IUGG\server_AUG_ELE\2021310\New_UC_5S_5S\WUDA-GEC.aug",
            #   r"E:\1Master_2\3-IUGG\server_AUG_ELE\2021310\IGSO_30S_5S\N047-GEC.aug",
            #   r"E:\1Master_2\3-IUGG\server_AUG_ELE\2021310\IGSO_30S_5S\N068-GEC.aug",
            #   r"E:\1Master_2\3-IUGG\server_AUG_ELE\2021310\IGSO_30S_5S\WHDS-GEC.aug",
            #   r"E:\1Master_2\3-IUGG\server_AUG_ELE\2021310\IGSO_30S_5S\WHSP-GEC.aug",
            #   r"E:\1Master_2\3-IUGG\server_AUG_ELE\2021310\IGSO_30S_5S\WHXZ-GEC.aug",
            #   r"E:\1Master_2\3-IUGG\server_AUG_ELE\2021310\IGSO_30S_5S\WHYJ-GEC.aug",
            #   r"E:\1Master_2\3-IUGG\server_AUG_ELE\2021310\IGSO_30S_5S\WUDA-GEC.aug",
            #   r"E:\1Master_2\3-IUGG\server_AUG_ELE\2021310\IGSO_30S_5S\XGXN-GEC.aug",
              ]
aug_path_2 = [r"E:\1Master_2\3-IUGG\server_AUG_ELE\2021310\Old_5S_5S\WHYJ-GEC.aug",
            #   r"E:\1Master_2\3-IUGG\server_AUG_ELE\2021310\Old_5S_5S\N028-GEC.aug",
            #   r"E:\1Master_2\3-IUGG\server_AUG_ELE\2021310\Old_5S_5S\N047-GEC.aug",
            #   r"E:\1Master_2\3-IUGG\server_AUG_ELE\2021310\Old_5S_5S\N068-GEC.aug",
            #   r"E:\1Master_2\3-IUGG\server_AUG_ELE\2021310\Old_5S_5S\WHDS-GEC.aug",
            #   r"E:\1Master_2\3-IUGG\server_AUG_ELE\2021310\Old_5S_5S\WHSP-GEC.aug",
            #   r"E:\1Master_2\3-IUGG\server_AUG_ELE\2021310\Old_5S_5S\WHXZ-GEC.aug",
            #   r"E:\1Master_2\3-IUGG\server_AUG_ELE\2021310\Old_5S_5S\WHYJ-GEC.aug",
            #   r"E:\1Master_2\3-IUGG\server_AUG_ELE\2021310\Old_5S_5S\WUDA-GEC.aug",
            #   r"E:\1Master_2\3-IUGG\server_AUG_ELE\2021310\Old_5S_5S\XGXN-GEC.aug",
              ]

out_path = r"E:\1Master_2\3-IUGG\server_AUG_ELE\2021310\New_UC_5S_5S"

if len(aug_path_1) != len(aug_path_2):
    print("The number of 1 != 2")
    sys.exit()
[week,sow]=tr.ymd2gpst(2021,11,6,0,0,00)
for i in range(len(aug_path_1)):
    [head_1,data_1] = rf.open_aug_file_new(aug_path_1[i])
    [head_2,data_2] = rf.open_aug_file_new(aug_path_2[i])
    site_name = aug_path_2[i].split(".")[0]
    site_name = site_name[len(site_name)-8:len(site_name)-4]
    out_file1 = out_path + "\\" + site_name + "-New-Old.difference"
    out_file2 = out_path + "\\" + site_name + "-Old-New.difference"
    for cur_time in data_1.keys():
        delta_sow = cur_time - sow
        cur_hour = int (delta_sow / 3600)
        cur_min = int ((delta_sow - cur_hour*3600) / 60)
        cur_sec = int ((delta_sow - cur_hour*3600 - 60 * cur_min))
        different_1,different_2 = "{:0>2d} {:0>2d} {:0>2d}".format(cur_hour,cur_min,cur_sec),"{:0>2d} {:0>2d} {:0>2d}".format(cur_hour,cur_min,cur_sec)
        if cur_time not in data_2.keys():
            continue
        for cur_sat in data_1[cur_time].keys():
            if cur_sat not in data_2[cur_time].keys():
                different_1 = different_1 + " " + cur_sat
        with open(out_file1,'a') as file:
            file.write(different_1 + "\n")
        # print(different_1)
        for cur_sat in data_2[cur_time].keys():
            if cur_sat not in data_1[cur_time].keys():
                different_2 = different_2 + " " + cur_sat
        with open(out_file2,'a') as file:
            file.write(different_2 + "\n")