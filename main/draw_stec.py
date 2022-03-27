'''
Author: HanJunjie
Date: 2021-11-10 15:26:45
LastEditTime: 2022-03-04 10:29:46
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



IPP_file1 = '/Users/hjj/Documents/HJJ/Master_1/IonoTest2.0to2.1/GREAT_IonoPre_v2.1_PPP固定解提取STEC/ResultProject/IPP_PPP/yar30100_Fixed_GEC.20IPP'
IPP_file2 = '/Users/hjj/Documents/HJJ/Master_1/IonoTest2.0to2.1/GREAT_IonoPre_v2.1_PPP固定解提取STEC/ResultProject/IPP_PPP/yarr0100_Fixed_GEC.20IPP'
# IPP_file1 = '/Users/hjj/Documents/HJJ/Master_1/IonoTest2.0to2.1/2.0/IPP_PPP/yar30100_Fixed_GEC.20IPP'
# IPP_file2 = '/Users/hjj/Documents/HJJ/Master_1/IonoTest2.0to2.1/2.0/IPP_PPP/yarr0100_Fixed_GEC.20IPP'

# IPP_file1 = '/Users/hjj/Documents/HJJ/Master_1/ionofile_test/20200108_30h/cod24h/IPP_PPP/yarr0090_Fixed.20IPP'
# IPP_file2 = '/Users/hjj/Documents/HJJ/Master_1/ionofile_test/20200108_30h/cod24h/IPP_PPP/wtzz0100_Fixed.20IPP'

# IPP_file1 = '/Users/hjj/Documents/HJJ/Master_1/ionofile_test/2020010/IPP_PL/wtza0100.20IPP'
# IPP_file2 = '/Users/hjj/Documents/HJJ/Master_1/ionofile_test/2020010/IPP_PL/wtza0100_Float.20IPP'

# IPP_file1 = '/Users/hjj/Documents/HJJ/Master_1/ionofile_test/2020010/IPP_PL/wtzz0100.20IPP'
# IPP_file2 = '/Users/hjj/Documents/HJJ/Master_1/ionofile_test/2020010/IPP_PL/wtza0100.20IPP'

# IPP_file2 = '/Users/hjj/Documents/HJJ/Master_1/ionofile_test/2020010/wtza0100-PPPAR-G.20IPP'
# #IPP_file2 = '/Users/hjj/Documents/HJJ/Master_1/ionofile_test/2020010/wtzz0100-PPPAR-G.20IPP'
# IPP_file1 = '/Users/hjj/Documents/HJJ/Master_1/ionofile_test/2020010/IPP_PPP/wtza0100.20IPP'

# IPP_data1 = rf.open_ipp_file(IPP_file1,0,30)
# IPP_data2 = rf.open_ipp_file(IPP_file2,0,30)

IPP_data1 = rf.open_ipp_file(IPP_file1,0,24)
IPP_data2 = rf.open_ipp_file(IPP_file2,0,24)

pre_data = dp.pre_tec(IPP_data1,IPP_data2)
#pre_data = dp.pre_tec_PPPAR(IPP_data1,IPP_data2)
dr.plot_tec_GREC(pre_data,'/Users/hjj/Desktop/ZIM2-ZIM3-PL.png','YAR3-YARR',True)
#dr.plot_tec_MIX(pre_data,'/Users/hjj/Desktop/YARR-YAR3-P.png','YAR3','G',True)
#dr.plot_tec_compare(IPP_data1,IPP_data2,'/Users/hjj/Desktop/YARR-YAR3-PL-R.png','YARR-YAR3','G10',True)
