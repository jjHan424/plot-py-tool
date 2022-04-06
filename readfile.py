'''
Author: JunjieHan
Date: 2021-09-06 19:24:38
LastEditTime: 2022-04-04 15:08:13
Description: read data file
'''
import numpy as np
import math
import trans as tr
import os

def open_aug_file(filename,sys="G"):
    week,sow=[[] for i in range(60)],[[] for i in range(60)]
    P1,P2,L1,L2 = [[] for i in range(60)],[[] for i in range(60)],[[] for i in range(60)],[[] for i in range(60)]
    ion1,ion2,trp = [[] for i in range(60)],[[] for i in range(60)],[[] for i in range(60)]
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
                    if len(value) <= 5:
                        continue
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
                        #trp[prn-1].append(float(value[7]))
                else:
                    prn=0
                    continue
    if (line_num > 5):
        aug = np.array([P1,P2,L1,L2,ion1,ion2]).T
    else:
        aug = np.array([P1,P2,L1,L2]).T   
    S_time = np.array([week,sow]).T
    all_time = np.array([ref_w,ref_sow]).T
    return (S_time,aug,all_time)

def open_aug_file_new(filename):
    all_data={}
    head_info={}
    soweek_last = 0
    w_last = 0
    head_end = False
    epoch_flag = False
    num_sat = 0
    last_day = 0
    day=0
    file_exist = os.path.exists(filename)
    if (not file_exist):
        return all_data
    with open(filename,'rt') as f:
        for line in f:
            value = line.split()
            if "SYS / # / AUG TYPES" in line:
                head_end = True
                head_index = 1
                for cur_value in value:
                    if (cur_value == "SYS"):
                        break
                    if (len(cur_value) != 1):
                        if line[0] not in head_info.keys():
                            head_info[line[0]]={}
                        head_info[line[0]][cur_value] = head_index
                        head_index = head_index + 1                   
            if ">" in line:
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
                if soweek not in all_data.keys():
                    all_data[soweek]={}
            if ((line[0] == "C" or line[0] == "E" or line[0] == "G") and epoch_flag):
                if (len(line) <= 4):
                    continue
                sat = value[0]
                if (sat not in all_data[soweek].keys()):
                    all_data[soweek][sat] = {}
                i = 1
                for type in head_info[sat[0]].keys():
                    if 12*i-9 > len(line) - 1 or 12*i+3 > len(line) - 1:
                        break
                    cur_value = line[12*i-9:12*i+3].strip()
                    if (len(cur_value) > 1):
                        all_data[soweek][sat][type] = float(cur_value)
                    i = i+1


    return (head_info,all_data)



def open_ipp_file(filename,Nsat = 0,hour_in = 24):
    all_data={}
    soweek_last = 0
    w_last = 0
    head_end = False
    epoch_flag = True
    num_sat = 0
    last_day = 0
    day=0
    
    file_exist = os.path.exists(filename)
    if (not file_exist):
        return all_data
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
                num_sat = (float(value[6]))
                [w,soweek] = tr.ymd2gpst(year,month,day,hour,minute,second)
                if (w_last==0):
                    w_last = w
                if (last_day == 0):
                    last_day = day
                #soweek = soweek + (w-w_last)*604800
                soweek = (day - last_day)*24 + hour + minute/60.0 + second/3600.0
                if (hour_in == 24):
                    soweek = (day - last_day)*24 + hour + minute/60.0 + second/3600.0
                else:
                     if (hour_in < 24 and (hour < (24 - hour_in) / 2)):
                        num_sat = -1
                w_last=w
                if (hour_in > 24 and (day - last_day) != 1):
                    num_sat = -1
                if soweek not in all_data.keys() and num_sat!=-1:
                    all_data[soweek]={}
            if(head_end and (line[0] == 'G' or line[0] == 'R' or line[0] == 'E' or line[0] == 'C') and num_sat >= Nsat):
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

def open_upd_wl_onedayfile(filename_list):
    all_data = {} 
    for index in filename_list:
        filename = filename_list[index]
        w_last = 0
        with open(filename,'rt') as f:
            for line in f:
                value = line.split()
                if value[0] == '%':
                    continue
                if value[0] == "EOF":
                    break
                sat = value[0]
                if sat not in all_data.keys():
                    all_data[sat] = float(value[1])
                    continue
    return all_data

def open_flt_ppplsq_file(filename):
    all_data={}
    soweek_last = 0
    w_last = 0
    head_end = False
    epoch_flag = True
    with open(filename,'rt') as f:
        for line in f:
            value = line.split()
            if line[0] == '%':
                head_end = True
                continue
            if head_end:
                ymd = value[1]
                hms = value[2]
                year = float(ymd[0:4])
                month = float(ymd[5:7])
                day = float(ymd[8:10])
                hour = float(hms[0:2])
                minute = float(hms[3:5])
                second = float(hms[6:12])
                [w,soweek] = tr.ymd2gpst(year,month,day,hour,minute,second)
                if (w_last==0):
                    w_last = w
                soweek = soweek + (w-w_last)*604800
                #soweek = hour + minute/60.0 + second/3600.0
                if soweek not in all_data.keys():
                    all_data[soweek]={}
                all_data[soweek]['X'] = float(value[5])
                all_data[soweek]['Y'] = float(value[6])
                all_data[soweek]['Z'] = float(value[7])
                all_data[soweek]['CLK'] = float(value[11])
                all_data[soweek]['NSAT'] = float(value[13])
                all_data[soweek]['GDOP'] = float(value[15])
                all_data[soweek]['PDOP'] = float(value[16])
                if value[17] == 'Fixed':
                    all_data[soweek]['AMB'] = 1
                else:
                    all_data[soweek]['AMB'] = 0
                
    return all_data

def open_flt_pvtflt_file(filename):
    all_data={}
    soweek_last = 0
    w_last = 0
    head_end = False
    epoch_flag = True
    with open(filename,'rt') as f:
        for line in f:
            value = line.split()
            if line[0] == " ":
                soweek = float(value[0])
                if (soweek < soweek_last):
                    w_last = w_last + 1
                soweek = soweek + w_last*604800
                soweek_last = soweek
                #soweek = hour + minute/60.0 + second/3600.0
                if soweek not in all_data.keys():
                    all_data[soweek]={}
                all_data[soweek]['X'] = float(value[1])
                all_data[soweek]['Y'] = float(value[2])
                all_data[soweek]['Z'] = float(value[3])
                all_data[soweek]['NSAT'] = float(value[13])
                all_data[soweek]['PDOP'] = float(value[14])
                if value[16] == 'Fixed':
                    all_data[soweek]['AMB'] = 1
                else:
                    all_data[soweek]['AMB'] = 0
                
    return all_data

def open_flt_pos_rtpppfile(filename):
    all_data={}
    soweek_last = 0
    w_last = 0
    head_end = False
    epoch_flag = True
    with open(filename,'rt') as f:
        for line in f:
            value = line.split()
            if line[0] != "%":
                soweek = float(value[1])
                if (soweek < soweek_last):
                    w_last = w_last + 1
                soweek = soweek + w_last*604800
                soweek_last = soweek
                #soweek = hour + minute/60.0 + second/3600.0
                if soweek not in all_data.keys():
                    all_data[soweek]={}
                all_data[soweek]['X'] = float(value[2])
                all_data[soweek]['Y'] = float(value[3])
                all_data[soweek]['Z'] = float(value[4])
                all_data[soweek]['Q'] = float(value[5])
                all_data[soweek]['NSAT'] = float(value[5])
                all_data[soweek]['PDOP'] = float(value[5])
                if value[15] == 'Fixed':
                    all_data[soweek]['AMB'] = 1
                else:
                    all_data[soweek]['AMB'] = 0
                
    return all_data