'''
Author: HanJunjie HanJunjie@whu.edu.cn
Date: 2022-05-11 11:08:04
LastEditors: HanJunjie HanJunjie@whu.edu.cn
LastEditTime: 2022-05-11 14:21:10
FilePath: /plot-py-tool/main/time_trans.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
import os
import sys
sys.path.insert(0,os.path.dirname(__file__)+'/..')

import trans as tr



print(tr.ymd2gpst(2022,4,25,9,36,30))