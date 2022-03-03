'''
Author: 韩俊杰
Date: 2021-09-15 14:13:07
LastEditTime: 2021-12-22 21:06:14
LastEditors: Please set LastEditors
Description: In User Settings Edit
FilePath: /plot-toolkit-master/jjHan_py_plot/dataprocess.py
'''
import sys
import numpy as np
import math
from numpy.core.fromnumeric import shape
from numpy.core.numeric import NaN

from numpy.lib.function_base import append


def pre_aug(Self_time = [], Self_aug = [], Inte_time = [], Inte_aug = [], ref = []):
    P1,P2,L1,L2 = [[] for i in range(33)],[[] for i in range(33)],[[] for i in range(33)],[[] for i in range(33)]
    ion1,ion2,trp = [[] for i in range(33)],[[] for i in range(33)],[[] for i in range(33)]
    time = [[] for i in range(33)]
    for ref_time in ref:
        I_prn_index = find_sat_index(Inte_time,ref_time)
        S_prn_index = find_sat_index(Self_time,ref_time)
        commont_sat = find_common_sat(I_prn_index,S_prn_index)
        if len(commont_sat) <= 1:
            continue
        else:
            ref_sat = commont_sat[0]
            ref_P1 = Self_aug[ref_sat[0]-1][0][ref_sat[2]] - Inte_aug[ref_sat[0]-1][0][ref_sat[1]]
            ref_P2 = Self_aug[ref_sat[0]-1][1][ref_sat[2]] - Inte_aug[ref_sat[0]-1][1][ref_sat[1]]
            ref_L1 = Self_aug[ref_sat[0]-1][2][ref_sat[2]] - Inte_aug[ref_sat[0]-1][2][ref_sat[1]]
            ref_L2 = Self_aug[ref_sat[0]-1][3][ref_sat[2]] - Inte_aug[ref_sat[0]-1][3][ref_sat[1]]
            if shape(Self_aug[0])[0] > 4:
                ref_ion1 = Self_aug[ref_sat[0]-1][4][ref_sat[2]] - Inte_aug[ref_sat[0]-1][4][ref_sat[1]]
                ref_ion2 = Self_aug[ref_sat[0]-1][5][ref_sat[2]] - Inte_aug[ref_sat[0]-1][5][ref_sat[1]]
                ref_trp = Self_aug[ref_sat[0]-1][6][ref_sat[2]] - Inte_aug[ref_sat[0]-1][6][ref_sat[1]]
            
            for sat in commont_sat:
                if sat[0] == ref_sat[0]:
                    continue
                time[sat[0]-1].append(ref_time[1] / 3600)
                temp = Self_aug[sat[0]-1][0][sat[2]] - Inte_aug[sat[0]-1][0][sat[1]]
                P1[sat[0]-1].append(temp - ref_P1)
                #P1[sat[0]-1].append(temp )

                temp = Self_aug[sat[0]-1][1][sat[2]] - Inte_aug[sat[0]-1][1][sat[1]]
                P2[sat[0]-1].append(temp - ref_P2)
                #P2[sat[0]-1].append(temp)
                
                temp = Self_aug[sat[0]-1][2][sat[2]] - Inte_aug[sat[0]-1][2][sat[1]]
                L1[sat[0]-1].append(temp - ref_L1)
                #L1[sat[0]-1].append(temp)

                temp = Self_aug[sat[0]-1][3][sat[2]] - Inte_aug[sat[0]-1][3][sat[1]]
                L2[sat[0]-1].append(temp - ref_L2)
                #L2[sat[0]-1].append(temp)
                if shape(Self_aug[0])[0] > 4:
                    temp = Self_aug[sat[0]-1][4][sat[2]] - Inte_aug[sat[0]-1][4][sat[1]]
                    ion1[sat[0]-1].append(temp - ref_ion1)
                    #ion1[sat[0]-1].append(temp)

                    temp = Self_aug[sat[0]-1][5][sat[2]] - Inte_aug[sat[0]-1][5][sat[1]]
                    ion2[sat[0]-1].append(temp - ref_ion2)

                    temp = Self_aug[sat[0]-1][6][sat[2]] - Inte_aug[sat[0]-1][6][sat[1]]
                    trp[sat[0]-1].append(temp)
    if shape(Self_aug[0])[0] > 4:
        aug = np.array([P1,P2,L1,L2,ion1,ion2,trp]).T
    else:
        aug = np.array([P1,P2,L1,L2]).T 
    return (time,aug)        

def find_common_sat(I_prn_index = [],S_prn_index = []):
    common_sat = []
    index_I = []
    index_S = []
    for Inte in I_prn_index:
        for Self in S_prn_index:
            if Inte[0] == Self[0]:
                common_sat.append(Inte[0])
                index_I.append(Inte[1])
                index_S.append(Self[1])
    common = np.array([common_sat,index_I,index_S]).T
    return common

def find_sat_index(raw_time = [], target_time = []):
    prn,index = [],[]
    sat = 0
    for sat_time in raw_time:
        sat = sat + 1
        low,high = 0, len(sat_time[0]) - 1
        while low < high:
            mid = int((low+high)/2)
            if sat_time[0][mid] < target_time[0]:
                low = mid + 1
            else:
                if sat_time[0][mid] > target_time[0]:
                    high = mid
                if sat_time[0][mid] == target_time[0]:
                    if abs(sat_time[1][mid] - target_time[1]) < 0.01:
                        prn.append(sat)
                        index.append(mid)
                        break
                    if sat_time[1][mid] < target_time[1]:
                        low = mid + 1
                    if sat_time[1][mid] > target_time[1]:
                        high = mid
    prn_index = np.array([prn,index]).T     
    return prn_index

def rms(data = []):
    size = len(data)
    sum = 0
    for i in range(size):
        sum = sum + data[i] * data[i]
    return math.sqrt(sum / size)
    
def std_stec(IPP_data1 = {},IPP_data2 = {}):
    predata = pre_tec(IPP_data1,IPP_data2)

    data_G = []
    data_R = []
    data_E = []
    data_C = []
    std = {}
    for time in predata:
        for sat in predata[time]:
            prn = int(sat[1:3])
            if (sat[0]=='G' and predata[time][sat]['TEC'] != 0):
                data_G.append(predata[time][sat]['TEC'])
            if (sat[0]=='R' and predata[time][sat]['TEC'] != 0):
                data_R.append(predata[time][sat]['TEC'])
            if (sat[0]=='E' and predata[time][sat]['TEC'] != 0):
                data_E.append(predata[time][sat]['TEC'])
            if (sat[0]=='C' and predata[time][sat]['TEC'] != 0):
                data_C.append(predata[time][sat]['TEC'])
    std["G"] = np.std(data_G)
    std["R"] = np.std(data_R)
    std["E"] = np.std(data_E)
    std["C"] = np.std(data_C)

    return std

def max_stec(IPP_data1 = {},IPP_data2 = {}):
    predata = pre_tec_PPPAR(IPP_data1,IPP_data2)

    data_G = []
    data_R = []
    data_E = []
    data_C = []
    std = {}
    for time in predata:
        for sat in predata[time]:
            prn = int(sat[1:3])
            if (sat[0]=='G' and predata[time][sat]['TEC'] != 0):
                data_G.append(np.abs(predata[time][sat]['TEC']))
            if (sat[0]=='R' and predata[time][sat]['TEC'] != 0):
                data_R.append(np.abs(predata[time][sat]['TEC']))
            if (sat[0]=='E' and predata[time][sat]['TEC'] != 0):
                data_E.append(np.abs(predata[time][sat]['TEC']))
            if (sat[0]=='C' and predata[time][sat]['TEC'] != 0):
                data_C.append(np.abs(predata[time][sat]['TEC']))
    
    std["G"] = NaN
    std["R"] = NaN
    std["E"] = NaN
    std["C"] = NaN
    if (len(data_G) != 0):
        std["G"] = np.max(data_G)
    if (len(data_R) != 0):
        std["R"] = np.max(data_R)
    if (len(data_E) != 0):
        std["E"] = np.max(data_E)
    if (len(data_C) != 0):
        std["C"] = np.max(data_C)

    return std

def pre_tec(IPP_data1={},IPP_data2={}):
    all_data={}
    for sod in IPP_data1:
        if sod in IPP_data2.keys():
            all_data[sod]={}
            for sat in IPP_data1[sod].keys():
                if sat in IPP_data2[sod].keys():
                    all_data[sod][sat]={}
                    all_data[sod][sat]['TEC'] = IPP_data1[sod][sat]['TEC'] - IPP_data2[sod][sat]['TEC']
    return all_data

def pre_tec_PPPAR(IPP_data1={},IPP_data2={}):
    all_data={}
    for sod in IPP_data1:
        if sod in IPP_data2.keys():
            all_data[sod]={}
            for sat in IPP_data1[sod].keys():
                if sat in IPP_data2[sod].keys():
                    all_data[sod][sat]={}
                    all_data[sod][sat]['TEC'] = IPP_data1[sod][sat]['TEC'] - IPP_data2[sod][sat]['TEC']
    all_data1={}
    for sod in all_data:
        G_sat,E_sat,R_sat,C_sat = "","","",""
        all_data1[sod]={}
        for sat in all_data[sod].keys():
            all_data1[sod][sat]={}
            if G_sat == "" and 'G' in sat:
                G_sat = sat
            if R_sat == "" and 'R' in sat:
                R_sat = sat
            if E_sat == "" and 'E' in sat:
                E_sat = sat
            if C_sat == "" and 'C' in sat:
                C_sat = sat
            if 'G' in sat:
                all_data1[sod][sat]['TEC'] = all_data[sod][sat]['TEC'] - all_data[sod][G_sat]['TEC']
            if 'R' in sat:
                all_data1[sod][sat]['TEC'] = all_data[sod][sat]['TEC'] - all_data[sod][R_sat]['TEC']
            if 'E' in sat:
                all_data1[sod][sat]['TEC'] = all_data[sod][sat]['TEC'] - all_data[sod][E_sat]['TEC']
            if 'C' in sat:
                all_data1[sod][sat]['TEC'] = all_data[sod][sat]['TEC'] - all_data[sod][C_sat]['TEC']

    return all_data1