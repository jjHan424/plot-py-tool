'''
Author: your name
Date: 2022-04-13 21:37:11
LastEditTime: 2022-05-21 13:52:05
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

#path = "/Users/hjj/Documents/HJJ/Master_1/IonoGrid/2021305/Bias/060/client-rank//GREAT-GEC-S.bias"
path = "/Users/hjj/Documents/HJJ/Master_1/Project_MeiTuan/MeiTuan/PPPRTK/2022114-grid/client/GREAT-GEC-S.bias"

site_list = ["HKCL","HKFN","HKKS","HKKT",
            "HKLT","HKMW","HKNP","HKOH",
            "HKPC","HKSL","HKSS","HKST",
            "HKWS"]

site_list = ["2008","2017","2006","2010",
            "2014"]
alldata = rf.open_bias_file_grid(path)
data_plot = dp.pre_Bias(alldata,INT = 5)
#begTime = 10
#while (begTime < 31):
dr.plot_bias_grid(data = data_plot,type = ["G","E","C","STD"],mode=site_list,ylim = 0.1,starttime = 1,year=2022,mon=4,day=24,LastT=15,time="UTC")
#begTime = begTime+2
