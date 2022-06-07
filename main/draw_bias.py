'''
Author: your name
Date: 2022-04-13 21:37:11
LastEditTime: 2022-06-06 12:08:04
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
path = "/Users/hjj/Documents/HJJ/Master_1/IonoGrid/Dynamic/20211205/Result/client-grid/GREAT-GEC-5.bias"

site_list = ["HKCL","HKFN","HKKS","HKKT",
            "HKLT","HKMW","HKNP","HKOH",
            "HKPC","HKSL","HKSS","HKST",
            "HKWS"]

site_list = ["2008","2017","2006","2010",
            "2014"]

site_list = ["WHXZ","WHDS","XGXN","N028",
            "N047","N068","WHYJ","WHSP","N062"]
alldata = rf.open_bias_file_grid(path)
data_plot = dp.pre_Bias(alldata,INT = 5)
#begTime = 10
#while (begTime < 31):
dr.plot_bias_grid(data = data_plot,type = ["G","E","C","STD"],mode=site_list,ylim = 0.1,starttime = 2,year=2021,mon=12,day=5,LastT=22,time="UTC")
#begTime = begTime+2
