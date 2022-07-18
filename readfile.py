'''
Author: JunjieHan
Date: 2021-09-06 19:24:38
LastEditTime: 2022-07-16 15:41:17
Description: read data file
'''
import numpy as np
import math

from pyrsistent import s
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
            if ((value[0][0] == "C" or value[0][0] == "E" or value[0][0] == "G") and epoch_flag):
                if (len(line) <= 4):
                    continue
                sat = value[0]
                if (sat not in all_data[soweek].keys()):
                    all_data[soweek][sat] = {}
                i = 1
                for type in head_info[sat[0]].keys():
                    if 12*i-9 > len(line) - 1 or 12*i+3 > len(line) - 1:
                        break
                    # cur_value = line[12*i-9:12*i+3].strip()
                    cur_value = line[12*i-8:12*i+4].strip()
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
                if value[17] == 'Fixed':
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
                # if value[5] == '1':
                #     all_data[soweek]['AMB'] = 1
                # else:
                #     all_data[soweek]['AMB'] = 0
                if value[15] == 'Fixed':
                    all_data[soweek]['AMB'] = 1
                else:
                    all_data[soweek]['AMB'] = 0
                
    return all_data

def open_bias_file_grid(filename):
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
                    all_data[soweek]["G"] = {}
                    all_data[soweek]["E"] = {}
                    all_data[soweek]["C"] = {}
                continue
            if (epoch_flag):
                if (len(line) <= 4):
                    continue
                site = value[0][0:4]
                i = 1
                for type in  all_data[soweek].keys():
                    if 18*i-1 > len(line) - 1 or 18*i+6 > len(line) - 1:
                        break
                    # cur_value = line[12*i-9:12*i+3].strip()
                    cur_value = line[18*i-1:18*i+6].strip()
                    if (len(cur_value) > 1):
                        all_data[soweek][type][site] = float(cur_value)
                    i = i+1
    return (all_data)

def open_pos_ref_IE(filename):
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
                if value[27] == 'Fixed':
                    all_data[soweek]['AMB'] = 1
                else:
                    all_data[soweek]['AMB'] = 0
                
    return all_data


def open_crd_gridmap(filename):
    all_data={}
    soweek_last = 0
    w_last = 0
    head_end = False
    epoch_flag = True
    with open(filename,'rt') as f:
        for line in f:
            value = line.split()
            
            head_end = True
            if len(value) >= 5:
                if value[4] == "False":
                    head_end = False
            if head_end:
                site = value[0]
                if site not in all_data.keys():
                    all_data[site]=[]
                all_data[site].append(float(value[1]))
                all_data[site].append(float(value[2]))
                all_data[site].append(float(value[3]))
                
    return all_data


def H_open_sigma_grid(filename):
    all_data={}
    soweek_last = 0
    w_last = 0
    head_end = False
    epoch_flag = True
    with open(filename,'rt') as f:
        for line in f:
            value = line.split()
            if (len(value) <= 2):
                continue
            ymd = value[1]
            hms = value[2]
            year = float(ymd[0:4])
            month = float(ymd[5:7])
            day = float(ymd[8:10])
            hour = float(hms[0:2])
            minute = float(hms[3:5])
            second = float(hms[6:8])
            [w,soweek] = tr.ymd2gpst(year,month,day,hour,minute,second)
            if (w_last==0):
                    w_last = w
            soweek = soweek + (w-w_last)*604800
            sat = value[3]
            if soweek not in all_data.keys():
                all_data[soweek]={}
            all_data[soweek][sat] = abs(float(value[4]))
    return all_data

def open_ltt_file(filename,Fixed=True,SPP=True):
    if not SPP:
        if Fixed:
            all_data={}
            soweek_last = 0
            w_last = 0
            head_end = False
            epoch_flag = True
            with open(filename,'rt') as f:
                for line in f:
                    value = line.split()
                    if value[0] != "Week":
                        soweek = float(value[1])
                        if (soweek < soweek_last):
                            w_last = w_last + 1
                        soweek = soweek + w_last*604800
                        soweek_last = soweek
                        #soweek = hour + minute/60.0 + second/3600.0
                        if soweek not in all_data.keys():
                            all_data[soweek]={}
                        all_data[soweek]['X'] = float(value[5])
                        all_data[soweek]['Y'] = float(value[6])
                        all_data[soweek]['Z'] = float(value[7])
                        all_data[soweek]['NSAT'] = float(value[8])
                        all_data[soweek]['PDOP'] = float(value[9])
                        if value[10] == 'Fixed':
                            all_data[soweek]['AMB'] = 1
                        else:
                            all_data[soweek]['AMB'] = 0
        else:
            all_data={}
            soweek_last = 0
            w_last = 0
            head_end = False
            epoch_flag = True
            with open(filename,'rt') as f:
                for line in f:
                    value = line.split()
                    if value[0] != "Week":
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
                        all_data[soweek]['NSAT'] = float(value[8])
                        all_data[soweek]['PDOP'] = float(value[9])
                        all_data[soweek]['AMB'] = 1
    else:
        all_data={}
        soweek_last = 0
        w_last = 0
        head_end = False
        epoch_flag = True
        with open(filename,'rt') as f:
            for line in f:
                value = line.split()
                if value[0] != "Week":
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
                    all_data[soweek]['NSAT'] = float(value[5])
                    all_data[soweek]['PDOP'] = float(value[6])
                    all_data[soweek]['AMB'] = 1           
    return all_data


def open_flt_ppp_rtpppfile(filename):
    all_data={}
    soweek_last = 0
    w_last = 0
    head_end = False
    epoch_flag = True
    with open(filename,'rt') as f:
        for line in f:
            value = line.split()
            if line[0] != "%":
                soweek = float(value[7])
                if (soweek < soweek_last):
                    w_last = w_last + 1
                soweek = soweek + w_last*604800
                soweek_last = soweek
                #soweek = hour + minute/60.0 + second/3600.0
                if soweek not in all_data.keys():
                    all_data[soweek]={}
                all_data[soweek]['X'] = float(value[17])
                all_data[soweek]['Y'] = float(value[18])
                all_data[soweek]['Z'] = float(value[19])
                all_data[soweek]['Q'] = float(value[20])
                all_data[soweek]['NSAT'] = float(value[20])
                all_data[soweek]['PDOP'] = float(value[20])
                all_data[soweek]['AMB'] = 1
                
    return all_data

def open_aug_file_rtppp(filename):
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
            if value[0] == "%" or value[0] == "##" or value[0] == "amb":
                epoch_flag = False
                continue               
            if value[0]=="*":
                value=line.split()
                year=(float(value[1]))
                month=(float(value[2]))
                day=(float(value[3]))
                hour=(float(value[4]))
                minute=(float(value[5]))
                second=(float(value[6]))
                satnum = float(value[7])
                [w,soweek] = tr.ymd2gpst(year,month,day,hour,minute,second)
                if (not epoch_flag):
                    min_sow = soweek
                if (soweek < min_sow):
                    soweek = soweek + 604800
                epoch_flag = True
                if soweek not in all_data.keys():
                    all_data[soweek]={}
            if ((value[0][0] == "C" or value[0][0] == "E" or value[0][0] == "G") and epoch_flag):
                sat = value[0]
                if (sat not in all_data[soweek].keys()):
                    all_data[soweek][sat] = {}
                all_data[soweek][sat]["L1"] = float(value[1])
                all_data[soweek][sat]["P1"] = float(value[2])
                all_data[soweek][sat]["L2"] = float(value[3])
                all_data[soweek][sat]["P2"] = float(value[4])
                all_data[soweek][sat]["TRP1"] = satnum

    head_info["G"]={}
    head_info["G"]["L1"]=1
    head_info["G"]["P1"]=2
    head_info["G"]["L2"]=3
    head_info["G"]["P2"]=4
    head_info["E"]={}
    head_info["E"]["L1"]=1
    head_info["E"]["P1"]=2
    head_info["E"]["L2"]=3
    head_info["E"]["P2"]=4
    head_info["C"]={}
    head_info["C"]["L1"]=1
    head_info["C"]["P1"]=2
    head_info["C"]["L2"]=3
    head_info["C"]["P2"]=4
    return (head_info,all_data)


def open_ppp_float_rtpppfile(filename):
    all_data={}
    soweek_last = 0
    w_last = 0
    head_end = False
    epoch_flag = True
    with open(filename,'rt') as f:
        for line in f:
            value = line.split()
            if line[0] != "%":
                soweek = float(value[7])
                if (soweek < soweek_last):
                    w_last = w_last + 1
                soweek = soweek + w_last*604800
                soweek_last = soweek
                #soweek = hour + minute/60.0 + second/3600.0
                if soweek not in all_data.keys():
                    all_data[soweek]={}
                all_data[soweek]['E'] = float(value[8])
                all_data[soweek]['N'] = float(value[9])
                all_data[soweek]['U'] = float(value[10])
                all_data[soweek]['NSAT'] = float(value[10])
                all_data[soweek]['AMB'] = 1
                
                # if value[15] == 'Fixed':
                #     all_data[soweek]['AMB'] = 1
                # else:
                #     all_data[soweek]['AMB'] = 0
                
    return all_data


def open_pos_ref_GREAT(filename):
    all_data={}
    soweek_last = 0
    w_last = 0
    head_end = False
    epoch_flag = True
    with open(filename,'rt') as f:
        for line in f:
            value = line.split()
            if line[0] != "#":
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
                all_data[soweek]['Q'] = float(value[5])
                all_data[soweek]['NSAT'] = float(value[5])
                all_data[soweek]['PDOP'] = float(value[5])
                if value[19] == 'Fixed':
                    all_data[soweek]['AMB'] = 1
                else:
                    all_data[soweek]['AMB'] = 0
                
    return all_data


def open_flt_ppprtk_rtpppfile(filename):
    all_data={}
    soweek_last = 0
    w_last = 0
    head_end = False
    epoch_flag = True
    with open(filename,'rt') as f:
        for line in f:
            value = line.split()
            if line[0] != "%":
                soweek = float(value[7])
                if (soweek < soweek_last):
                    w_last = w_last + 1
                soweek = soweek + w_last*604800
                soweek_last = soweek
                #soweek = hour + minute/60.0 + second/3600.0
                if soweek not in all_data.keys():
                    all_data[soweek]={}
                all_data[soweek]['X'] = float(value[29])
                all_data[soweek]['Y'] = float(value[30])
                all_data[soweek]['Z'] = float(value[31])
                all_data[soweek]['Q'] = float(value[20])
                all_data[soweek]['NSAT'] = float(value[20])
                all_data[soweek]['PDOP'] = float(value[20])
                all_data[soweek]['AMB'] = 1
                
    return all_data

def open_arinf_rtpppfile(filename,sat = "G15"):
    all_data={}
    soweek_last = 0
    w_last = 0
    head_end = False
    epoch_flag = True
    wr=False
    data1 = []
    time1 = []
    with open(filename,'rt') as f:
        for line in f:
            value = line.split()
            time = value[0].split(':')
            if len(time) > 2:
                year=2022
                mon=6
                day=22
                hour = float(time[0])
                min = float(time[1])
                sec = float(time[2])
                [w,soweek] = tr.ymd2gpst(year,mon,day,hour,min,sec)
                if (w_last == 0):
                    w_last = w
                soweek = soweek + (w - w_last)*7*24*3600
            if value[0] == "WL_INF":
                wr = True
                continue
            elif not wr:
                wr=False
                continue
            if wr and value[0][0] != sat[0]:
                wr=False
            if wr and value[0]==sat:
                data1.append(float(value[1]))
                time1.append(soweek)
                wr = False
  
    return (time1,data1)

def open_ppprtk_rtpppfile(filename):
    all_data={}
    soweek_last = 0
    w_last = 0
    head_end = False
    epoch_flag = True
    with open(filename,'rt') as f:
        for line in f:
            value = line.split()
            if line[0] != "%":
                soweek = float(value[7])
                if (soweek < soweek_last):
                    w_last = w_last + 1
                soweek = soweek + w_last*604800
                soweek_last = soweek
                #soweek = hour + minute/60.0 + second/3600.0
                if soweek not in all_data.keys():
                    all_data[soweek]={}
                all_data[soweek]['X'] = float(value[29])
                all_data[soweek]['Y'] = float(value[30])
                all_data[soweek]['Z'] = float(value[31])
                all_data[soweek]['Q'] = float(value[20])
                all_data[soweek]['NSAT'] = float(value[24])
                # all_data[soweek]['NSAT'] = float(value[12])
                # all_data[soweek]['NSAT'] = float(value[18])
                all_data[soweek]['PDOP'] = float(value[20])
                if (all_data[soweek]['NSAT'] <= 4):
                    all_data[soweek]['AMB'] = 0
                else:
                    all_data[soweek]['AMB'] = 1
                # all_data[soweek]['AMB'] = 1
                
    return all_data


def open_upd_rtpppfile(filename_list,sys="G"):
    all_data = {} 
    for index in filename_list:
        filename = filename_list[index]
        w_last = 0
        with open(filename,'rt') as f:
            for line in f:
                value = line.split()
                if value[0]=='*':
                    if value[7] == "0":
                        continue
                    year=float(value[1])
                    mon=float(value[2])
                    day=float(value[3])
                    hour = float(value[4])
                    min = float(value[5])
                    sec = float(value[6])
                    [w,soweek] = tr.ymd2gpst(year,mon,day,hour,min,sec)
                    if (w_last==0):
                        w_last = w
                    soweek = soweek + (w-w_last)*604800
                    if soweek not in all_data.keys():
                        all_data[soweek]={}
                    w_last = w
                    continue
                
                sat = value[0]
                if 'x' not in sat and sat not in all_data[soweek].keys():
                    all_data[soweek][sat] = (float(value[1]))
                    continue
    return all_data


def open_augc_file_rtppp(filename,sitename):
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
            if value[0]=="*":
                value=line.split()
                year=(float(value[1]))
                month=(float(value[2]))
                day=(float(value[3]))
                hour=(float(value[4]))
                minute=(float(value[5]))
                second=(float(value[6]))
                satnum = float(value[7])
                [w,soweek] = tr.ymd2gpst(year,month,day,hour,minute,second)
                if (not epoch_flag):
                    min_sow = soweek
                if (soweek < min_sow):
                    soweek = soweek + 604800
                epoch_flag = True
                if soweek not in all_data.keys():
                    all_data[soweek]={}
                continue
            all_data[soweek][sitename[int(value[0])-1]] = int(value[1])
            continue

    return (all_data)

def open_ismr(filename):
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
                sat=value[2]
                all_data[soweek][sat] = float(value[9])
    return all_data