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

# grid_path_S = "/Users/hanjunjie/Master_3/1-IUGG/AUG2GRID/2021311/GER_5C_NEW_4/GREAT-GEC3-30.grid"

# delay = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]
# delay = [2,4,6,8,10,12,14,16,18,20]
delay = [20]
Year,Mon,Day,Hour,lastT,DeltaT = 2021,11,7,2,22,2
count = 1
while count > 0:
    doy = tr.ymd2doy(Year,Mon,Day,0,0,00)
    # grid_path_S = "/Users/hanjunjie/Master_3/1-IUGG/AUG2GRID/{}{:0>3}/CHNHK16-R-C-HKST-HKLT/GREAT-GEC2-30.grid".format(Year,doy)
    grid_path_S = "/Users/hanjunjie/Master_3/1-IUGG/AUG2GRID/{}{:0>3}/EPNGER-R-C-KOS1/GREAT-GEC3-30.grid".format(Year,doy)
    [grid_data_S,lat,lon] = rf.open_grid_file(grid_path_S)
    for cur_delay in delay:
        # grid_path_I = "/Users/hanjunjie/Master_3/1-IUGG/AUG2GRID/2021311/GER_5C_NEW_4/GREAT-GEC3-30.grid"
        # grid_path_I = "/Users/hanjunjie/Master_3/1-IUGG/GRID_PREDICT/2021310/HK_6Site_30_120_ARIMA_220/{}.grid".format(cur_delay)
        # [grid_data_I,lat,lon] = rf.open_grid_file(grid_path_I)
        # [grid_data_ref,lat,lon] = rf.open_grid_file(grid_path_ref)
        grid_data_ref = grid_data_S
        # grid_data = dp.pre_grid(grid_data_I,grid_data_S,grid_data_ref)
        dr.plot_grid_GEC_new(grid_data_S,type = "NSAT",freq = 1,starttime = Hour,time = "UTC",show = True,ylim=0,deltaT=DeltaT,LastT=lastT,year = Year,mon=Mon,day=Day)
    count = count - 1
    Day = Day + 1

