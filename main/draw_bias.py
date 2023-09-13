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


# site_list = ["HKTK","T430","HKLT","HKKT","HKSS","HKWS","HKSL","HKST","HKKS","HKCL","HKPC","HKNP","HKMW","HKLM","HKOH"]
site_list = ["WHYJ","WHDS","WHSP","N028","N047","N068","XGXN","WHXZ"]
# site_list = ["HB01","HB02","HB03","HB04","HB05","HB06","HB07"] 
# site_list = ["K042","K057","K059","K101","A010","V092"]

# site_list = ["2008","2017","2006","2010",
#             "2014"]

# site_list = ["WHXZ","WHDS","XGXN","N028",
#             "N047","N068","WHYJ","WHSP","N062"]

# site_list = ["WHXZ","WHDS","WHYJ"]

# data_plot = dp.pre_Bias(alldata,INT = 5)
#begTime = 10
#while (begTime < 31):
count = 1
Y=2021
M=11
D=6
L=24
while count > 0:
    doy = tr.ymd2doy(Y,M,D,0,0,00)
    cdoy = "{:0>3}".format(doy)
    # path = r"E:\1Master_2\Paper_Grid\Res_FromServer_New\Server\Bias" + "\\GREAT-GEC-5-HK-" + cdoy + ".bias"
    path = r"E:\1Master_2\3-IUGG\Pro_2021310_Aug2Grid\Grid_BDS3\GREAT-GEC-5.bias"
    alldata = rf.open_bias_file_grid(path)
    alldata_pre = dp.pre_Bias(alldata,5)
    dr.plot_bias_grid(data = alldata_pre,type = ["G","E","C","STD"],mode=site_list,ylim = 0.1,starttime = 0,year=Y,mon=M,day=D,LastT=L,time="UTC",deltaT = 4)
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
