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

all_data = {}
file_NL = r"E:\1Master_2\2-UPD_Test\Pro_2023001\data\upd_nl_2023001_GEC"
file_WL = r"E:\1Master_2\2-UPD_Test\Pro_2023001\data\upd_wl_2023001_GEC"
rf.open_upd_great(file_NL,all_data)
rf.open_upd_great(file_WL,all_data)

Y,M,D = 2023,1,1
S,L,DDD = 0,24,4
dr.plot_upd(mode = ["upd_WL"], data = all_data,type = ["G","E","C"],ylim = 1,starttime=S,LastT=L,deltaT=DDD,time = "UTC",all=False,year = Y,mon=M,day=D,show=True)