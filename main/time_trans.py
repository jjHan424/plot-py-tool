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
import glv

<<<<<<< HEAD
year=2022
mon=4
day=20
=======
year=2021
mon=12
day=10
>>>>>>> fed472eb8e6f4f892e4f6111e52851e4b931b0d4

print("GPST(Week Sow): ",tr.ymd2gpst(year,mon,day,0,0,0))
print("Day of Year: ",tr.ymd2doy(year,mon,day,0,0,00))
[week,sow]=tr.ymd2gpst(year,mon,day,0,0,00)
print("GPST(Day of Week): ",sow/3600/24)
print(tr.mjd2gpst(60051,0))
xyz = [-2380216.3373,5375749.9006,2465024.2995]
print(tr.xyz2blh(xyz[0],xyz[1],xyz[2]))
blh = tr.xyz2blh(xyz[0],xyz[1],xyz[2])
print(blh[0] / glv.deg,blh[1] / glv.deg)
ref_xyz = [-2380216.3373,5375749.9006,2465024.2995]
enu = tr.xyz2enu(xyz,ref_xyz)
print(enu)
