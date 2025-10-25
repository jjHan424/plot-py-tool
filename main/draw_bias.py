'''
Author: your name
Date: 2022-04-13 21:37:11
LastEditTime: 2022-09-03 20:00:02
LastEditors: HanJunjie HanJunjie@whu.edu.cn
Description: 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
FilePath: /plot-py-tool/main/draw_bias.py
'''
from audioop import bias
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

#path = "/Users/hjj/Documents/HJJ/Master_1/IonoGrid/2021305/Bias/060/client-rank//GREAT-GEC-S.bias"


site_list = ["HKTK","T430","HKLT","HKKT","HKSS","HKWS","HKSL","HKST","HKKS","HKCL","HKPC","HKNP","HKMW","HKLM","HKOH","HKSC"]
# site_list = ["IJMU","DENT","WSRT","KOS1","BRUX","DOUR","WARE","REDU","EIJS","TIT2","EUSK","DILL","DIEP","BADH","KLOP","FFMJ","KARL","HOBU","PTBB","GOET"]

# data_plot = dp.pre_Bias(alldata,INT = 5)
#begTime = 10
#while (begTime < 31):
count = 1
Y=2021
M=11
D=7
Hour = 2
L=22
while count > 0:
    doy = tr.ymd2doy(Y,M,D,0,0,00)
    cdoy = "{:0>3}".format(doy)
    # path = r"E:\1Master_2\Paper_Grid\Res_FromServer_New\Server\Bias" + "\\GREAT-GEC-5-HK-" + cdoy + ".bias"
    path = r"/Users/hanjunjie/Master_3/1-IUGG/AUG2GRID/2021311/HK_Test/GREAT-GEC3-30.bias"
    alldata = rf.open_bias_file_grid(path)
    alldata_pre = dp.pre_Bias(alldata,30)
    dr.plot_bias_grid(data = alldata_pre,type = ["G","E","C","STD"],mode=site_list,ylim = 0.1,starttime = Hour,year=Y,mon=M,day=D,LastT=L,time="UTC",deltaT = 2)
    D = D + 1
    count = count - 1
    # if (count == 0 and M!=12):
    #     count = 1
    #     M=12
    #     D=5
    if (D > 31):
        D = 1
        M = M + 1
#begTime = begTime+2
