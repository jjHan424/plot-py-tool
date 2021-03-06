'''
Author: HanJunjie HanJunjie@whu.edu.cn
Date: 2022-05-11 11:08:04
LastEditors: HanJunjie HanJunjie@whu.edu.cn
LastEditTime: 2022-07-26 20:33:37
FilePath: /plot-py-tool/main/time_trans.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
import os
import sys
sys.path.insert(0,os.path.dirname(__file__)+'/..')

import trans as tr

year=2022
mon=7
day=26

print("GPST(Week Sow): ",tr.ymd2gpst(year,mon,day,2,46,4))
print("Day of Year: ",tr.ymd2doy(year,mon,day,0,0,00))
[week,sow]=tr.ymd2gpst(year,mon,day,0,0,00)
print("GPST(Day of Week): ",sow/3600/24)
#print(tr.mjd2gpst(59729,0))