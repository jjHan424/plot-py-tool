'''
Author: your name
Date: 2021-11-12 09:38:43
LastEditTime: 2022-08-30 16:09:37
LastEditors: HanJunjie HanJunjie@whu.edu.cn
Description: 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
FilePath: /plot-py-tool/main/draw_aug.py
'''
# '''
# Author: JunjieHan
# Date: 2021-09-06 19:24:38
# LastEditTime: 2022-03-17 22:38:25
# Description: read data file
# '''
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
# #set aug file path
# '''
# path_S = '/Users/hjj/Documents/HJJ/Master_1/aug_ion_trp/augo'
# aug_file_S = path_S + '/HKST-GEC-5.aug'
# path_I = '/Users/hjj/Documents/HJJ/Master_1/Project_MeiTuan/boWang_Master/20211101/1_基站加密/client_Near'
# aug_file_I = path_I + '/HKSC-GEC-I.aug'
# '''

# # path_I = '/Users/hjj/Documents/HJJ/Master_1/Project_MeiTuan/boWang_Master/20211101/1_基站加密/client_Far'
# # aug_file_I = path_I + '/HKSC-GEC-I.aug'
# # path_S = '/Users/hjj/Documents/HJJ/Master_1/Project_MeiTuan/boWang_Master/20211101/1_基站加密/server_Far'
# # aug_file_S = path_S + '/HKSC-GEC-S.aug'

# path_I = '/Users/hjj/Desktop'
# aug_file_I = path_I + '/WUH2_2022006_GEC_UC.aug'
# path_S = '/Users/hjj/Desktop'
# aug_file_S = path_S + '/WUH2_2022006_GEC_UC_client-lsq.aug'

# # path_I = '/Users/hjj/Documents/HJJ/Master_1/IonoGrid/2021305/server'
# # aug_file_I = path_I + '/HKSC-GEC-S.aug'

# #save_fig_path = '/Users/hjj/Documents/HJJ/Master_1/0924_WH/server/client/'
# save_fig_path = '/Users/hjj/Desktop/'
# test = [[],[]]
# test[0].append(12)
# test[1].append(34)
# mean = np.mean(test[0])
# #read aug file
# time_G_S = []
# aug_G_S = []
# ref_G_S = []
# [time_G_S,aug_G_S,ref_G_S] = rf.open_aug_file(aug_file_S)
# time_E_S = []
# aug_E_S = []
# ref_E_S = []
# [time_E_S,aug_E_S,ref_E_S] = rf.open_aug_file(aug_file_S,'E')
# time_C_S = []
# aug_C_S = []
# ref_C_S = []
# [time_C_S,aug_C_S,ref_C_S] = rf.open_aug_file(aug_file_S,'C')
# #read aug_I file
# time_G_I = []
# aug_G_I = []
# ref_G_I = []
# [time_G_I,aug_G_I,ref_G_I] = rf.open_aug_file(aug_file_I)
# time_E_I = []
# aug_E_I = []
# ref_E_I = []
# [time_E_I,aug_E_I,ref_E_I] = rf.open_aug_file(aug_file_I,'E')
# time_C_I = []
# aug_C_I = []
# ref_C_I = []
# [time_C_I,aug_C_I,ref_C_I] = rf.open_aug_file(aug_file_I,'C')
# #prepare aug data


# [time_G,aug_G] = dp.pre_aug(time_G_S,aug_G_S,time_G_I,aug_G_I,ref_G_I)
# [time_E,aug_E] = dp.pre_aug(time_E_S,aug_E_S,time_E_I,aug_E_I,ref_E_I)
# [time_C,aug_C] = dp.pre_aug(time_C_S,aug_C_S,time_C_I,aug_C_I,ref_C_I)

# # dr.plot_aug_GEC(time_G,aug_G,time_E,aug_E,time_C,aug_C,'P',save_fig_path)
# # dr.plot_aug_GEC(time_G,aug_G,time_E,aug_E,time_C,aug_C,'L',save_fig_path)
# dr.plot_aug_GEC(time_G,aug_G,time_E,aug_E,time_C,aug_C,'ion',save_fig_path)
# dr.plot_aug_GEC(time_G,aug_G,time_E,aug_E,time_C,aug_C,'trp',save_fig_path)

# path_S = "/Users/hjj/Documents/HJJ/Master_1/IonoGrid/2021305/Bias/334/server-ion/HKSC-GEC-S.aug"
# path_I = "/Users/hjj/Documents/HJJ/Master_1/IonoGrid/2021305/Bias/334/client-aug/HKSC-GEC-I.aug"

path_S = r"E:\1Master_2\Paper_Grid\Res_FromServer_New\Client_Dynamic-2\WUDA-GEC.aug"   # PPPAR算的改正数
# path_I = r"E:\1Master_2\Paper_Grid\Res_FromServer_New\Client_Dynamic-2\client-Aug-310-02\WUDA-GEC-I.aug"# 内插改正数
path_I = r"E:\1Master_2\Paper_Grid\Res_FromServer_New\Client_Dynamic-2\client-Grid_Ele-310-01\WUDA-GEC-I.aug"# 内插改正数

# path_S = r"G:\Project\data\aug\2021306\K057-GEC.aug"   # PPPAR算的改正数
# path_I = r"D:\A-paper\Project\2021306\client-Grid_Ele_R\From_Server\K057-GEC-I.aug"# 内插改正数

# path_S = "/Volumes/H_GREAT/WangBo_Paper/2021305/test/Frequency2_UPD_HK_GBM/HKSC-GEC-S-2.aug"   # PPPAR算的改正数
# path_I = "/Volumes/H_GREAT/WangBo_Paper/2021305/test/Frequency2_UPD_HK_GBM/HKSC-GEC-I.aug"# 内插改正数

#path_I = "/Users/hjj/Documents/HJJ/Master_1/IonoGrid/2021100/client/HKSC-GEC-I-ion.aug"
# site_list = ["HKCL","HKFN","HKKS","HKKT","HKLM",
#             "HKLT","HKMW","HKNP","HKOH","HK PC",
#             "HKSC","HKSL","HKSS","HKST","HKTK","HKWS"]


# begTime = begTime + 2

# path_I = "/Users/hjj/Documents/HJJ/Master_1/IonoGrid/2021100/clientHKLM/5-MW.aug"
# #path_I = "/Users/hjj/Documents/HJJ/Master_1/IonoGrid/2021100/client/HKLM-GEC-I-ion.aug"
# path_S = "/Users/hjj/Documents/HJJ/Master_1/IonoGrid/2021100/server_ion/HKLM-GEC-S.aug"

# [head_I,data_I] = rf.open_aug_file_rtppp(path_I)
# [head_S,data_S] = rf.open_aug_file_rtppp(path_S)
# [head_I,data_I] = rf.open_aug_file_rtppp(path_I)
# [head_S,data_S] = rf.open_aug_file_rtppp(path_S)


# [head_I,data_I] = rf.open_aug_file_new(path_I)
# [head_S,data_S] = rf.open_aug_file_new(path_S)
# data = dp.pre_aug_new(head_I,data_I,data_S)
#starttime 数据在UTC下的开始时间
#begT 画图起始时间，在time的设置下
#LastT 需要画图的数据长度（小时）
#deltaT 坐标刻度距离
#如下
#starttime = 2,time = "UTC+8",begT=10,LastT=10
#数据在UTC的开始时间为02:00，画图的横坐标时间系统为UTC+8，在UTC+8下从10:00开始画10小时的数据，统计结果为画图的结果
# begTime = 10
# while (begTime < 31):
# dr.plot_aug_G_E_C(data,head_I,type = "P",freq = 1,strttime = 17,time = "UTC",show = True,deltaT=2,ylim=1.5,LastT=7,year = 2022,mon=6,day=20)
# site_list1 = ["WHDS","WHYJ","WHSP","N028","N047","N068","XGXN","WUDA","WHXZ"]
site_list1 = ["WUDA"]
data_site,data_site_S = {},{}
for cur_site in site_list1:
    # path_S = r"E:\1Master_2\Paper_Grid\Res_FromServer_New\Client_Dynamic-2\client-Aug-312-02" + "\\" + cur_site + "-GEC.aug"   # PPPAR算的改正数
    # path_I = r"E:\1Master_2\Paper_Grid\Res_FromServer_New\Client_Dynamic-2\client-Aug-312-02" + "\\" + cur_site + "-GEC-I.aug"   # 内插改正数
    # path_S = r"E:\1Master_2\Paper_Grid\Res_FromServer_New\Client_Dynamic-2\client-Grid_Ele-312-01" + "\\" + cur_site + "-GEC-I.aug"   # Grid改正数a
    # path_S = r"E:\1Master_2\Paper_Grid\2-IUGG\2021310\server\WUDA-GEC.aug"
    path_S = r"E:\1Master_2\Paper_Grid\Res_FromServer_New\Server\2021312\WHYJ-GEC.aug"
    path_I = r"E:\1Master_2\Paper_Grid\Res_FromServer_New\WHYJ-GEC-I.aug"
    # path_I = r"E:\0Project\EXSUN_Data\20230909_Data_Test\BDS3\ppprtk\ES43_20230909_SGG_CLK06_K_GEC.aug"
    # path_I = r"E:\0Project\ZHD_Data\20230910_Data_Test\BDS2\aug_rt\GZLH_20230910_SGG_CLK06_S_GEC.augi"
    # path_S = r"E:\0Project\ZHD_Data\20230910_Data_Test\BDS2\aug_rt\GZLH_20230910_SGG_CLK06_S_GEC.aug"
    # path = r"E:\1Master_2\3-IUGG\Pro_2021311_PPPRTK_GER\client\GOET-GEC-I-GRID-RE3600-TrpVIRTUAL.aug"
    # [head_I,data_I] = rf.open_aug_file_rtppp(path_I)
    # [head_S,data_S] = rf.open_aug_file_rtppp(path_S)
    [head_I,data_I] = rf.open_aug_file_new(path_I)
    [head_S,data_S] = rf.open_aug_file_new(path_S)
    # [head_I,data_site[cur_site]] = rf.open_aug_file_new(path)

    data_site[cur_site] = dp.pre_aug_new(head_I,data_I,data_S)
    # data_site[cur_site] = data_S
    # data_site[cur_site] = data_I
    # data_site_S[cur_site4] = data_S
    print(cur_site)
    # site_list2 = []
    # site_list2.append(cur_site)
    # dr.plot_aug_GEC_new(data_site,head_I,type = "ION",freq = 1,starttime = 2,time = "UTC",show = True,deltaT=60/60,ylim=0.1,LastT=22,year = 2021,mon=10,day=30,site_list=site_list1)
    # dr.plot_aug_G_E_C(data_site,head_I,type = "ION",freq = 1,starttime = 2,time = "UTC",show = True,deltaT=60/60,ylim=0.1,LastT=22,year = 2021,mon=11,day=6,site_list=site_list2)

dr.plot_aug_G_E_C(data_site[cur_site],head_I,type = "ION",freq = 1,starttime = 2,time = "UTC+8",show = True,deltaT=2,ylim=0.2,LastT=22,year = 2021,mon=11,day=8,site_list=site_list1)
# dr.plot_aug_G_E_C(data_site,head_I,type = "NSAT",freq = 1,starttime = 0,time = "UTC",show = True,deltaT=4,ylim=0.04,LastT=24,year = 2021,mon=11,day=6,site_list=site_list1,data_S=data_site_S)


#########
#year mon day starttime 为开始时间
#ylim 为y坐标范围
#time 可以是UTC或者UTC+8等为控制横坐标显示
#type “ION”为电离层，“TRP”为对流层
##########
# dr.plot_aug_GEC_new(data,head_I,type = "TRP",freq = 1,starttime = 2,time = "UTC",show = True,deltaT=2,ylim=0.5,LastT=22,year = 2021,mon=12,day=5)

# begTime = begTime + 2
# dr.plot_aug_GEC_new(data,head_I,type = "TRP",freq = 1,starttime = 2,time = "UTC+8",show = True,deltaT=2,ylim=0.1)



