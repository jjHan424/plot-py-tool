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
# file_NL = r"E:\1Master_2\3-IUGG\data\UPD_New_5S\upd_nl_2021310_GEC"
# file_WL = r"E:\1Master_2\3-IUGG\data\UPD_New_5S\upd_wl_2021310_GEC"
# rf.open_upd_great(file_NL,all_data)
# rf.open_upd_great(file_WL,all_data)
all_data = rf.open_upd_rtpppfile([r"E:\0Project\ZHD_Data\20230914_Data_Test\BDS2\NRTK_20230914_SGG_CLK06_S_GEC.updc"])

Y,M,D = 2021,11,6
S,L,DDD = 0,24,1
dr.plot_upd(mode = ["upd_WL"], data = all_data,type = ["G","E","C"],ylim = 1,starttime=S,LastT=L,deltaT=DDD,time = "UTC+8",all=False,year = Y,mon=M,day=D,show=True)