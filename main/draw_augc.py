'''
Author: HanJunjie HanJunjie@whu.edu.cn
Date: 2022-07-13 16:49:07
LastEditors: HanJunjie HanJunjie@whu.edu.cn
LastEditTime: 2022-07-13 17:17:21
FilePath: /plot-py-tool/main/draw_augc.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
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

site_READ=["DGDC","HCLH","DGCA","SZLX","SZDP"]
path = "/Volumes/H_GREAT/2Project/Allystar/2022_0710DataAnalyse/NRTK_20220713_SGG_CLK01_K_GEC.augc"
site_PLOT=["DGDC","HCLH","DGCA","SZLX","SZDP"]
data = rf.open_augc_file_rtppp(path,site_READ)
dr.plot_augc_NUM(data,site_PLOT,deltaT=1,LastT=24,year=2022,starttime=0,mon=7,day=13,time="UTC",all=True)