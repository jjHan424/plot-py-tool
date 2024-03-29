'''
Author: 韩俊杰
Date: 2021-09-15 14:13:07
LastEditTime: 2022-07-25 19:50:14
LastEditors: HanJunjie HanJunjie@whu.edu.cn
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
import glv

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
        Ele_index,Ele_cur,Ele_sort,ref_sat = {},{},{},{}
        for sat in data_I[time].keys():
            if len(sat) <= 1:
                continue
            if sat not in data_S[time].keys():
                continue
            if sat[0] not in Ele_index.keys():
                Ele_index[sat[0]],Ele_cur[sat[0]],Ele_sort[sat[0]] = [],[],[]
            Ele_index[sat[0]].append(sat)
            Ele_cur[sat[0]].append(data_S[time][sat]["ELE"])
            Ele_sort[sat[0]].append(data_S[time][sat]["ELE"])
        
        for sys_cur in Ele_cur.keys():
            Ele_sort[sys_cur].sort(reverse = True)
            for j in range(len(Ele_sort[sys_cur])):
                for i in range(len(Ele_sort[sys_cur])):
                    if Ele_cur[sys_cur][i] == Ele_sort[sys_cur][j]:
                        ref_sat[sys_cur] = Ele_index[sys_cur][i]
                        break
                if sys_cur in ref_sat.keys():
                    for type in data_I[time][sat].keys():
                        sys_type = ref_sat[sys_cur][0] + "_" + type
                        if type not in data_S[time][ref_sat[sys_cur]].keys():
                            continue    
                        ref_data[time][sys_cur] = 0                
                        ref_data[time][sys_type] = data_I[time][ref_sat[sys_cur]][type] - data_S[time][ref_sat[sys_cur]][type]
                    break

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
                    ref_data[time][sys_type] = data_I[time][ref_sat[sat[0]]][type] - data_S[time][ref_sat[sat[0]]][type]
                    ref_data[time][sys_type] = data_I[time][sat][type] - data_S[time][sat][type]
                else:
                    if "ELE" in data_S[time][sat].keys():
                        all_data[time][sat]["ELE"] = data_S[time][sat]["ELE"]
                    if type == "TRP1":
                        all_data[time][sat][type] = (data_I[time][sat][type] - data_S[time][sat][type])
                    else:
                        # if data_I[time][sat][type] == 0.0 or data_S[time][sat][type] == 0.0:
                        #     continue
                        all_data[time][sat][type] = (data_I[time][sat][type] - data_S[time][sat][type]) - ref_data[time][sys_type]
        for sat in data_I[time].keys():
            if sat not in all_data[time].keys():
                continue
            for type in data_I[time][sat].keys():
                if type[0] != "d":
                    continue
                all_data[time][sat][type] = data_I[time][sat][type]
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
                all_data[soweek][sys][site] = data[nextsec][sys][site] - data[soweek][sys][site]
                # if ref_G == "NONE":
                #     ref_G = site
                #     ref = data[nextsec][sys][site] - data[soweek][sys][site]
                #     continue
                # else:
                #     all_data[soweek][sys][site] = data[nextsec][sys][site] - data[soweek][sys][site] - ref
    
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
    if size == 0:
        return 0
    return math.sqrt(sum / size)

def rms_3sigma(data = [],time_p = [],sig_num = 0,max_data = 0):
    size = 0
    sum = 0
    time_out,data_out = [],[]
    data_mean = np.mean(data)
    data_sigma = np.std(data)
    for i in range(len(data)):
        if abs(data[i]) > max_data and max_data != 0:
            continue
        if abs(data[i]-data_mean) > sig_num*data_sigma and sig_num != 0:
            continue
        sum = sum + data[i] * data[i]
        data_out.append(data[i])
        time_out.append(time_p[i])
        size = size + 1
    if size == 0:
        return 0
    return (time_out,data_out)

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
            # all_data[time]["Q"] = XYZ[time]["Q"]
    return all_data

def XYZ2ENU_dynamic(XYZ = {},REF_XYZ = {}):
    all_data = {}
    xyz = []
    ref_xyz = []
    

    for time in XYZ.keys():
        if time not in all_data and time in REF_XYZ.keys():
            if REF_XYZ[time]["AMB"] != 1:
                continue
            all_data[time] = {}
            xyz.append(XYZ[time]["X"])
            xyz.append(XYZ[time]["Y"])
            xyz.append(XYZ[time]["Z"])
            ref_xyz.append(REF_XYZ[time]["X"])
            ref_xyz.append(REF_XYZ[time]["Y"])
            ref_xyz.append(REF_XYZ[time]["Z"])
            enu = tr.xyz2enu(xyz,ref_xyz)
            xyz.clear()
            ref_xyz.clear()
            all_data[time]["E"] = enu[0]
            all_data[time]["N"] = enu[1]
            all_data[time]["U"] = enu[2]
            all_data[time]["NSAT"] = XYZ[time]["NSAT"]
            all_data[time]["PDOP"] = XYZ[time]["PDOP"]
            all_data[time]["AMB"] = XYZ[time]["AMB"]
    return all_data


def get_H_sun(year,month,day,hour,length,step,lon,lat):
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
        time_plot.append(cur_hour-2)
        cur_hour = cur_hour + step/3600
    return H_sun_list,time_plot

def pre_grid(data_I,data_S,data_ref):
    all_data = {}
    for cur_time in data_ref.keys():
        if cur_time not in data_S.keys():
            continue
        if cur_time not in data_I.keys():
            continue
        if cur_time not in all_data.keys():
            all_data[cur_time] = {}
        for cur_sat in data_ref[cur_time].keys():
            if cur_sat not in data_S[cur_time].keys():
                continue
            if cur_sat not in data_I[cur_time].keys():
                continue
            all_data[cur_time][cur_sat] = []
            for i in range(len(data_I[cur_time][cur_sat])):
                all_data[cur_time][cur_sat].append(data_S[cur_time][cur_sat][i] - data_I[cur_time][cur_sat][i])
    return all_data

def find_common_sat_aug(data={},ref_site = "NONE"):
    all_data = {}
    for cur_time in data[ref_site].keys():
        if cur_time not in all_data.keys():
            all_data[cur_time] = {}
        for cur_sat in data[ref_site][cur_time].keys():
            number = 0
            for cur_site in data.keys():
                if cur_time in data[cur_site].keys():
                    if cur_sat in data[cur_site][cur_time].keys():
                        number = number+1
            if number == len(data):
                all_data[cur_time][cur_sat] = 1
    return all_data
def ele_of_sun(lat,lon,year,mon,day,hour,lastT,step):
    doy = tr.ymd2doy(year,mon,day,0,0,0)
    N0 = 79.6764+0.2422*(year-1985) - int((year-1985)/4)
    t = doy-N0
    theta = 2*math.pi*t/365.2422
    ED = 0.3723+23.2567*math.sin(theta)+0.1149*math.sin(2*theta) - 0.1712*math.sin(3*theta) - 0.758*math.cos(theta) + 0.3656*math.cos(2*theta) + 0.0201*math.cos(3*theta)
    cur_hour = hour
    hour_int = hour
    second,minute = 0,0
    [w,soweek] = tr.ymd2gpst(year,mon,day,hour_int,minute,second)
    all_data = {}
    while cur_hour < hour + lastT:
        sin_h = math.sin(lat*glv.deg) * math.sin(ED*glv.deg) + math.cos(lat*glv.deg) * math.cos(ED*glv.deg) * math.cos((-180+15*(cur_hour+lon/15))*glv.deg)
        H_sun = math.asin(sin_h)
        if H_sun < 0:
            # cur_hour = cur_hour + step/3600
            H_sun = 0
            # continue
        
        all_data[soweek] = H_sun/glv.deg
        cur_hour = cur_hour + step/3600
        soweek = soweek + step
    return all_data