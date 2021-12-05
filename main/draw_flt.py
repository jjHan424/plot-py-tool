'''
Author: HanJunjie
Date: 2021-11-29 21:26:38
LastEditTime: 2021-11-29 21:47:58
LastEditors: Please set LastEditors
Description: 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
FilePath: /plot-py-tool/main/draw_flt.py
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
import seaborn as sns
import trans as tr

filename = '/Users/hjj/Documents/HJJ/Master_1/Project_MeiTuan/NanJing/res_flt/JFNG_2020109_GEC_2.flt'
data = rf.open_flt_ppplsq_file(filename)
data = rf.open_flt_ppplsq_file(filename)