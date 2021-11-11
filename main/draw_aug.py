'''
Author: JunjieHan
Date: 2021-09-06 19:24:38
LastEditTime: 2021-11-10 15:20:35
Description: read data file
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
#set aug file path
'''
path_S = '/Users/hjj/Documents/HJJ/Master_1/aug_ion_trp/augo'
aug_file_S = path_S + '/HKST-GEC-5.aug'
path_I = '/Users/hjj/Documents/HJJ/Master_1/aug_ion_trp/cliento'
aug_file_I = path_I + '/HKST-GEC-I.aug'
'''

path_S = '/Users/hjj/Documents/HJJ/Master_1/0924_WH/server/client'
aug_file_S = path_S + '/WUDA-GEC-5.aug'
path_I = '/Users/hjj/Documents/HJJ/Master_1/0924_WH/server/client_UPD'
aug_file_I = path_I + '/WUDA-GEC-5.aug'

#save_fig_path = '/Users/hjj/Documents/HJJ/Master_1/0924_WH/server/client/'
save_fig_path = '/Users/hjj/Desktop/'
test = [[],[]]
test[0].append(12)
test[1].append(34)
mean = np.mean(test[0])
#read aug file
time_G_S = []
aug_G_S = []
ref_G_S = []
[time_G_S,aug_G_S,ref_G_S] = rf.open_aug_file(aug_file_S)
time_E_S = []
aug_E_S = []
ref_E_S = []
[time_E_S,aug_E_S,ref_E_S] = rf.open_aug_file(aug_file_S,'E')
time_C_S = []
aug_C_S = []
ref_C_S = []
[time_C_S,aug_C_S,ref_C_S] = rf.open_aug_file(aug_file_S,'C')
#read aug_I file
time_G_I = []
aug_G_I = []
ref_G_I = []
[time_G_I,aug_G_I,ref_G_I] = rf.open_aug_file(aug_file_I)
time_E_I = []
aug_E_I = []
ref_E_I = []
[time_E_I,aug_E_I,ref_E_I] = rf.open_aug_file(aug_file_I,'E')
time_C_I = []
aug_C_I = []
ref_C_I = []
[time_C_I,aug_C_I,ref_C_I] = rf.open_aug_file(aug_file_I,'C')
#prepare aug data


[time_G,aug_G] = dp.pre_aug(time_G_S,aug_G_S,time_G_I,aug_G_I,ref_G_I)
[time_E,aug_E] = dp.pre_aug(time_E_S,aug_E_S,time_E_I,aug_E_I,ref_E_I)
[time_C,aug_C] = dp.pre_aug(time_C_S,aug_C_S,time_C_I,aug_C_I,ref_C_I)

dr.plot_aug_GEC(time_G,aug_G,time_E,aug_E,time_C,aug_C,'P',save_fig_path)
dr.plot_aug_GEC(time_G,aug_G,time_E,aug_E,time_C,aug_C,'L',save_fig_path)
dr.plot_aug_GEC(time_G,aug_G,time_E,aug_E,time_C,aug_C,'ion',save_fig_path)
dr.plot_aug_GEC(time_G,aug_G,time_E,aug_E,time_C,aug_C,'trp',save_fig_path)



