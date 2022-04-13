'''
Author: your name
Date: 2022-04-13 21:37:11
LastEditTime: 2022-04-13 22:33:09
LastEditors: Please set LastEditors
Description: 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
FilePath: /plot-py-tool/main/draw_bias.py
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

path = "/Users/hjj/Documents/HJJ/Master_1/IonoGrid/2021100/serverBias/GREAT-GEC-NONE.bias"
alldata = rf.open_bias_file_grid(path)
dr.plot_bias_grid(data = alldata,type = ["G","E","C"],mode=["HKNP","HKOH"],ylim = 1,starttime = 0,begT=8,LastT=24,time="UTC+8")
