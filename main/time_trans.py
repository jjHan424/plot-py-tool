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

year=2021
mon=11
day=6

print("GPST(Week Sow): ",tr.ymd2gpst(year,mon,day,9,31,0))
print("Day of Year: ",tr.ymd2doy(year,mon,day,0,0,00))
[week,sow]=tr.ymd2gpst(year,mon,day,0,0,00)
[week,sow]=tr.ymd2gpst(year,mon,day,16,22,0)
print("GPST(Day of Week): ",sow/3600/24)
print(tr.mjd2gpst(59519,32405))

xyz = [-2141844.0708,5071953.6039,3209315.6304]

blh = tr.xyz2blh(xyz[0],xyz[1],xyz[2])
xyz2 = tr.blh2xyz(blh[0],blh[1],blh[2])
xyz = [-2141844.0708,5071953.6039,3209315.6304]
print(xyz[0]-xyz2[0])
print(xyz[1]-xyz2[1])
print(xyz[2]-xyz2[2])
