'''
Author: Han Junjie
Date: 2021-11-23 20:07:41
LastEditTime: 2022-08-28 20:58:51
LastEditors: HanJunjie HanJunjie@whu.edu.cn
Description: 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
FilePath: /plot-py-tool/main/draw_upd.py
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
#import seaborn as sns
import trans as tr


file_nl = {}
file_wl = {}
file_nl[0] = r'E:\0Project\Tencent\NRTK_20220829_SGG_CLK06_S_GEC.upd'
# Save_dir = r'E:\0Project\Tencent\'

file_wl[0] = '/Users/hjj/Documents/HJJ/Master_1/Project_MeiTuan/GERAT_UPDLSQ/ambupd/upd_wl_2020001_G_UC'
week,sec = tr.ymd2gpst(2020,9,6,0,0,0)
nl = rf.open_upd_rtpppfile(file_nl)
#wl = rf.open_upd_wl_onedayfile(file_wl)
#dr.plot_upd_wl_oneday_GEC(wl,'/Users/hjj/Desktop/','UPD WL',True)
dr.plot_upd_nl_GEC(nl,"E:\\0Project\\Tencent\\",'UPD NL',True)