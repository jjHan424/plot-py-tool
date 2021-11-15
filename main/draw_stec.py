'''
Author: HanJunjie
Date: 2021-11-10 15:26:45
LastEditTime: 2021-11-15 17:35:33
LastEditors: Please set LastEditors
FilePath: /plot-toolkit-master/jjHan_py_plot/main/draw_stec.py
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

IPP_file1 = '/Users/hjj/Documents/HJJ/Master_1/ionofile_test/IPP_PPP/yarr0010.20IPP'
IPP_file2 = '/Users/hjj/Documents/HJJ/Master_1/ionofile_test/IPP_PPP/yar30010.20IPP'
IPP_data1 = rf.open_ipp_file(IPP_file1)
IPP_data2 = rf.open_ipp_file(IPP_file2)
pre_data = dp.pre_tec(IPP_data1,IPP_data2)
#dr.plot_tec_GREC(pre_data,'/Users/hjj/Desktop/YARR-YAR3-P.png','ARR-YAR3',True)

dr.plot_tec_MIX(pre_data,'/Users/hjj/Desktop/YARR-YAR3-PPP-E.png','ARR-YAR3','E',True)
