'''
Author: 韩俊杰
Date: 2021-09-15 14:13:07
LastEditTime: 2022-04-14 20:51:31
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
import trans as tr

def pre_aug(Self_time = [], Self_aug = [], Inte_time = [], Inte_aug = [], ref = []):
    P1,P2,L1,L2 = [[] for i in range(60)],[[] for i in range(60)],[[] for i in range(60)],[[] for i in range(60)]
    ion1,ion2,trp = [[] for i in range(60)],[[] for i in range(60)],[[] for i in range(60)]
    time = [[] for i in range(60)]
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
                #ref_trp = Self_aug[ref_sat[0]-1][6][ref_sat[2]] - Inte_aug[ref_sat[0]-1][6][ref_sat[1]]
            
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

                    # temp = Self_aug[sat[0]-1][6][sat[2]] - Inte_aug[sat[0]-1][6][sat[1]]
                    # trp[sat[0]-1].append(temp)
    if shape(Self_aug)[0] <= 0:
        aug = np.array([P1,P2,L1,L2]).T 
        return (time,aug)
    if shape(Self_aug[0])[0] > 4:
        aug = np.array([P1,P2,L1,L2,ion1,ion2]).T
    else:
        aug = np.array([P1,P2,L1,L2]).T 
    return (time,aug)        

def pre_aug_new(head_I = {}, data_I = {}, data_S = {}):
    head_info = {}
    all_data = {}
    ref_data = {}
    for time in data_I.keys():
        if time not in data_S.keys():
            continue
        if time not in all_data.keys():
            all_data[time] = {}
            ref_data[time] = {}
        for sat in data_I[time].keys():
            if sat not in data_S[time].keys():
                continue
            if sat not in all_data[time].keys() and sat[0] in ref_data[time].keys():
                all_data[time][sat] = {}
            for type in data_I[time][sat].keys():
                sys_type = sat[0] + "_" + type
                if type not in data_S[time][sat].keys():
                    continue               
                if sys_type not in ref_data[time]:   
                    ref_data[time][sat[0]] = 0                
                    ref_data[time][sys_type] = data_I[time][sat][type] - data_S[time][sat][type]
                else:
                    if type == "TRP1":
                        all_data[time][sat][type] = (data_I[time][sat][type] - data_S[time][sat][type])
                    else:
                        all_data[time][sat][type] = (data_I[time][sat][type] - data_S[time][sat][type]) - ref_data[time][sys_type]
    return all_data

def pre_Bias(data = {},INT = 30):
    all_data  = {}

    for soweek in data.keys():
        ref_G,ref_E,ref_C = "NONE","NONE","NONE"
        nextsec = soweek + INT
        while (nextsec not in data.keys()):
            nextsec = nextsec + INT
            if (nextsec >= 2*7*24*3600):
                break
        if (nextsec >= 2*7*24*3600):
                break
        if soweek not in all_data.keys():
            all_data[soweek]={}
            all_data[soweek]["G"] = {}
            all_data[soweek]["E"] = {}
            all_data[soweek]["C"] = {}
        for sys in data[soweek].keys():
            ref_G = "NONE"
            for site in data[soweek][sys].keys():
                if (site not in data[nextsec][sys].keys()):
                    continue
                if ref_G == "NONE":
                    ref_G = site
                    ref = data[nextsec][sys][site] - data[soweek][sys][site]
                    continue
                else:
                    all_data[soweek][sys][site] = data[nextsec][sys][site] - data[soweek][sys][site] - ref
    
    return all_data


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

def XYZ2ENU_const(XYZ = {},REF_XYZ = {},site = "HKLM"):
    all_data = {}
    xyz = []
    ref_xyz = []
    if site not in REF_XYZ.keys():
        return all_data
    else:
        ref_xyz = REF_XYZ[site]

    for time in XYZ.keys():
        if time not in all_data:
            all_data[time] = {}
        for data_type in XYZ[time].keys():
            xyz.append(XYZ[time]["X"])
            xyz.append(XYZ[time]["Y"])
            xyz.append(XYZ[time]["Z"])
            enu = tr.xyz2enu(xyz,ref_xyz)
            xyz.clear()
            all_data[time]["E"] = enu[0]
            all_data[time]["N"] = enu[1]
            all_data[time]["U"] = enu[2]
            all_data[time]["NSAT"] = XYZ[time]["NSAT"]
            all_data[time]["PDOP"] = XYZ[time]["PDOP"]
            all_data[time]["AMB"] = XYZ[time]["AMB"]
    return all_data