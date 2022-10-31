'''
Author: Han Junjie
Date: 2021-12-18 15:26:38
LastEditTime: 2021-12-22 21:13:48
LastEditors: Please set LastEditors
Description: 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
FilePath: /plot-py-tool/main/std_stec.py
'''

import os
import sys
sys.path.insert(0,os.path.dirname(__file__)+'/..')
import numpy as np
import readfile as rf
import matplotlib.pyplot as plt
import dataprocess as dp
import draw as dr


IPP_dir = "/Users/hjj/Documents/HJJ/Master_1/ionofile_test/20200108_30h/gfz24h/IPP_PL/"
yyyy = "2020"
site = ["wtzr","wtzs","areg","areq","irkj","irkm","yarr","yar3"]
#site = ["gold","gol2"]
mode = ""
std_all = {}
std_all["G"] = []
std_all["R"] = []
std_all["E"] = []
std_all["C"] = []
max_all = {}
max_all["G"] = []
max_all["R"] = []
max_all["E"] = []
max_all["C"] = []
num_site = len(site)/2
while (num_site):
    day = 7
    count = 5
    while (count):
        IPP1 = IPP_dir + site[int(2*num_site - 2)] + "{0:03}".format(day) + "0" + mode + "." + yyyy[2:] + "IPP"
        IPP2 = IPP_dir + site[int(2*num_site - 1)] + "{0:03}".format(day) + "0" + mode + "." + yyyy[2:] + "IPP"
        IPPdata1 = rf.open_ipp_file(IPP1,0,22)
        IPPdata2 = rf.open_ipp_file(IPP2,0,22)
        cur_std = dp.std_stec(IPPdata1,IPPdata2)
        cur_max = dp.max_stec(IPPdata1,IPPdata2)
        std_all["G"].append(cur_std["G"])
        std_all["R"].append(cur_std["R"])
        std_all["E"].append(cur_std["E"])
        std_all["C"].append(cur_std["C"])

        max_all["G"].append(cur_max["G"])
        max_all["R"].append(cur_max["R"])
        max_all["E"].append(cur_max["E"])
        max_all["C"].append(cur_max["C"])
        count = count - 1
        day = day + 1
    num_site = num_site - 1
print(site)
for Gsys in std_all.keys():
    str = "%s:%f"%(Gsys,np.nanmean(std_all[Gsys]))
    print(str)
    
for Gsys in std_all.keys():
    str = "%s:%f"%(Gsys,np.nanmean(max_all[Gsys]))
    print(str)