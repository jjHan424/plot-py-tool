'''
Author: HanJunjie HanJunjie@whu.edu.cn
Date: 2022-05-11 11:08:04
LastEditors: HanJunjie HanJunjie@whu.edu.cn
LastEditTime: 2022-08-30 15:25:27
FilePath: /plot-py-tool/main/time_trans.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
import os
import sys
sys.path.insert(0,os.path.dirname(__file__)+'/..')

import trans as tr
import matplotlib.pyplot as plt

year=2022
mon=4
day=20

print("GPST(Week Sow): ",tr.ymd2gpst(year,mon,day,0,0,0))
print("Day of Year: ",tr.ymd2doy(year,mon,day,0,0,00))
[week,sow]=tr.ymd2gpst(year,mon,day,0,0,00)
print("GPST(Day of Week): ",sow/3600/24)
print(tr.mjd2gpst(60208,0))
xyz =     [3370667.1984,711818.7219,5349787.8726]
ref_xyz = [3370658.8291,711876.9374,5349786.7382]
enu = tr.xyz2enu(xyz,ref_xyz)
print(enu)
