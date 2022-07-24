'''
Author: your name
Date: 2021-11-12 09:38:43
LastEditTime: 2022-07-24 14:37:06
LastEditors: HanJunjie HanJunjie@whu.edu.cn
Description: 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
FilePath: /plot-py-tool/main/draw_aug.py
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

mode_list = ["DGDC","DGCA","SZYT","HZAD","SWHF"]
# mode_list = ["SZYT","SWHF"]
file_list = ["/Volumes/H_GREAT/2Project/Allystar/2022_0723SZ_SZK/DGDC_20220723_SGG_CLK06_S_GEC.aug",
            "/Volumes/H_GREAT/2Project/Allystar/2022_0723SZ_SZK/DGCA_20220723_SGG_CLK06_S_GEC.aug",
            "/Volumes/H_GREAT/2Project/Allystar/2022_0723SZ_SZK/SZYT_20220723_SGG_CLK06_S_GEC.aug",
            "/Volumes/H_GREAT/2Project/Allystar/2022_0723SZ_SZK/HZAD_20220723_SGG_CLK06_S_GEC.aug",
            "/Volumes/H_GREAT/2Project/Allystar/2022_0723SZ_SZK/SWHF_20220723_SGG_CLK06_S_GEC.aug"]
data_all = {}
for i in range(len(mode_list)):
    [head,data] = rf.open_aug_file_rtppp(file_list[i])
    data_all[mode_list[i]] = data

dr.plot_aug_NSAT(data_all,mode_list,type = "NSAT",freq = 1,starttime = 0,time = "UTC+8",show = True,deltaT=1,ylim=0.5,LastT=24,year = 2022,mon=7,day=23,deltaData=5)