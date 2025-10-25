import os
import sys
sys.path.insert(0,os.path.dirname(__file__)+'/..')
sys.path.insert(0,os.path.dirname(__file__)+'/../..')
import numpy as np
import readfile as rf
import matplotlib as mpl
mpl.use("TkAgg")
import matplotlib.pyplot as plt
import dataprocess as dp
import draw as dr
#import seaborn as sns
import trans as tr
import math
import glv

year,month,day = 2021,11,7
hour,length,step = 21,2,30
# lon,lat = 9.67,59.19
lon,lat = 114,30 #WUHAN
lon,lat = 114,22 #HONGKONG

doy = tr.ymd2doy(year,month,day,0,0,00)
N0 = 79.6764+0.2422*(year-1985) - int((year-1985)/4)
t = doy-N0
theta = 2*math.pi*t/365.2422
ED = 0.3723+23.2567*math.sin(theta)+0.1149*math.sin(2*theta) - 0.1712*math.sin(3*theta) - 0.758*math.cos(theta) + 0.3656*math.cos(2*theta) + 0.0201*math.cos(3*theta)
# hour,length,step = 0,24,30
cur_hour = hour
H_sun_list,time_plot = [],[]
while cur_hour < hour + length:
    sin_h = math.sin(lat*glv.deg) * math.sin(ED*glv.deg) + math.cos(lat*glv.deg) * math.cos(ED*glv.deg) * math.cos((-180+15*(cur_hour+lon/15))*glv.deg)
    H_sun = math.asin(sin_h)
    if H_sun < 0:
        cur_hour = cur_hour + step/3600
        continue
    H_sun_list.append(H_sun/glv.deg)
    time_plot.append(cur_hour)
    cur_hour = cur_hour + step/3600
figP,axP = plt.subplots(1,1,figsize=(18,9.5),sharey=False,sharex=True)
axP.plot(time_plot,H_sun_list)

year,month,day = 2021,11,6
hour,length,step = 2,22,30
# lon,lat = 9.67,59.19
lon,lat = 114,30 #WUHAN
# lon,lat = 114,22 #HONGKONG

doy = tr.ymd2doy(year,month,day,0,0,00)
N0 = 79.6764+0.2422*(year-1985) - int((year-1985)/4)
t = doy-N0
theta = 2*math.pi*t/365.2422
ED = 0.3723+23.2567*math.sin(theta)+0.1149*math.sin(2*theta) - 0.1712*math.sin(3*theta) - 0.758*math.cos(theta) + 0.3656*math.cos(2*theta) + 0.0201*math.cos(3*theta)
# hour,length,step = 0,24,30
cur_hour = hour
H_sun_list,time_plot = [],[]
while cur_hour < hour + length:
    sin_h = math.sin(lat*glv.deg) * math.sin(ED*glv.deg) + math.cos(lat*glv.deg) * math.cos(ED*glv.deg) * math.cos((-180+15*(cur_hour+lon/15))*glv.deg)
    H_sun = math.asin(sin_h)
    if H_sun < 0:
        cur_hour = cur_hour + step/3600
        continue
    H_sun_list.append(H_sun/glv.deg)
    time_plot.append(cur_hour)
    cur_hour = cur_hour + step/3600
# figP,axP = plt.subplots(1,1,figsize=(18,9.5),sharey=False,sharex=True)
# axP.plot(time_plot,H_sun_list)

plt.show()

