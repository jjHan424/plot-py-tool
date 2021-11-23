'''
Author: JunjieHan
Date: 2021-09-06 19:24:38
LastEditTime: 2021-11-23 21:05:05
Description: read data file
'''
import numpy as np
import math
import trans as tr

def open_aug_file(filename,sys="G"):
    week,sow=[[] for i in range(33)],[[] for i in range(33)]
    P1,P2,L1,L2 = [[] for i in range(33)],[[] for i in range(33)],[[] for i in range(33)],[[] for i in range(33)]
    ion1,ion2,trp = [[] for i in range(33)],[[] for i in range(33)],[[] for i in range(33)]
    ref = []
    ref_w,ref_sow = [],[]
    epoch_flag = False
    line_num = 0
    min_sow = 0
    with open(filename,'rt') as f:
        for line in f:
            if line[0] == ">":
                value=line.split()
                year=(float(value[1]))
                month=(float(value[2]))
                day=(float(value[3]))
                hour=(float(value[4]))
                minute=(float(value[5]))
                second=(float(value[6]))
                [w,soweek] = tr.ymd2gpst(year,month,day,hour,minute,second)
                if (not epoch_flag):
                    min_sow = soweek
                if (soweek < min_sow):
                    soweek = soweek + 604800
                epoch_flag = True
                ref_w.append(w)
                ref_sow.append(soweek)
            if epoch_flag:             
                if line[0] == sys:
                    value=line.split()
                    prn = int(value[0][1:3])
                    week[prn-1].append(w)
                    sow[prn-1].append(soweek)
                    P1[prn-1].append(float(value[1]))
                    L1[prn-1].append(float(value[2]))
                    P2[prn-1].append(float(value[3]))
                    L2[prn-1].append(float(value[4]))
                    line_num = len(value)
                    if len(value) > 5:
                        ion1[prn-1].append(float(value[5]))
                        ion2[prn-1].append(float(value[6]))
                        trp[prn-1].append(float(value[7]))
                else:
                    prn=0
                    continue
    if (line_num > 5):
        aug = np.array([P1,P2,L1,L2,ion1,ion2,trp]).T
    else:
        aug = np.array([P1,P2,L1,L2]).T   
    S_time = np.array([week,sow]).T
    all_time = np.array([ref_w,ref_sow]).T
    return (S_time,aug,all_time)

def open_ipp_file(filename):
    all_data={}
    soweek_last = 0
    w_last = 0
    head_end = False
    epoch_flag = True
    with open(filename,'rt') as f:
        for line in f:
            value = line.split()
            if value[0] == 'END':
                head_end = True
                continue
            if(head_end and line[0] != 'G' and line[0] != 'R' and line[0] != 'E' and line[0] != 'C' and line[0] != ' '):
                year=(float(value[0]))
                month=(float(value[1]))
                day=(float(value[2]))
                hour=(float(value[3]))
                minute=(float(value[4]))
                second=(float(value[5]))
                [w,soweek] = tr.ymd2gpst(year,month,day,hour,minute,second)
                if (w_last==0):
                    w_last = w
                #soweek = soweek + (w-w_last)*604800
                soweek = hour + minute/60.0 + second/3600.0
                w_last=w
                if soweek not in all_data.keys():
                    all_data[soweek]={}
            if(head_end and (line[0] == 'G' or line[0] == 'R' or line[0] == 'E' or line[0] == 'C')):
                sat = value[0]
                if sat not in all_data[soweek].keys():
                    all_data[soweek][sat]={}
                all_data[soweek][sat]['LAT']=float(value[1])
                all_data[soweek][sat]['LON']=float(value[2])
                all_data[soweek][sat]['ELE']=float(value[3])
                all_data[soweek][sat]['AZI']=float(value[4])
                all_data[soweek][sat]['MPF']=float(value[5])
                all_data[soweek][sat]['TEC']=float(value[6])
    return all_data

def open_upd_nl_file(filename_list,sys="G"):
    all_data = {} 
    for index in filename_list:
        filename = filename_list[index]
        w_last = 0
        with open(filename,'rt') as f:
            for line in f:
                value = line.split()
                if value[0] == '%':
                    if value[4] != 'upd_NL':
                        return 0
                    continue
                if value[0]=='EPOCH-TIME':
                    day = (float(value[1]))
                    sec = (float(value[2]))
                    [w,soweek] = tr.mjd2gpst(day,sec)
                    if (w_last==0):
                        w_last = w
                    soweek = soweek + (w-w_last)*604800
                    if soweek not in all_data.keys():
                        all_data[soweek]={}
                    w_last = w
                    continue
                if value[0] == 'EOF':
                    break
                sat = value[0]
                if 'x' not in sat and sat not in all_data[soweek].keys():
                    all_data[soweek][sat] = (float(value[1]))
                    continue
    return all_data
             