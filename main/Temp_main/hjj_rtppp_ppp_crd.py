import os
import sys
sys.path.insert(0,os.path.dirname(__file__)+'/..')
sys.path.insert(0,os.path.dirname(__file__)+'/../..')
import numpy as np
import readfile as rf
import matplotlib as mpl
mpl.use("TkAgg")
import matplotlib.pyplot as plt
import dataprocess as dp
import draw as dr

ppp_path = r"E:\0Project\ZHD_Data\Coordinate\PPP"
obs_path = r"E:\0Project\ZHD_Data\Coordinate\obs_test"
select_site_file = r"E:\1Master_2\2-UPD_Test\EPN_SITE\EPN_AUG_GER_SITE.txt"

out_crd_path = r"E:\0Project\ZHD_Data\ZHD.crd"
is_crd_out = True
out_xml_path = r"E:\1Master_2\2-UPD_Test\EPN_SITE\GER_AUG.xml"
is_xml_out = True
ppp_list = os.listdir(ppp_path)

# site_list = "AHAQ AHBB AHHS AHJA AHXC FJLY FJQZ FJZZ GDLC GDSJ GDSS GDYJ GDZC GDZH GXGG GXHZ GXLB GXQZ GXWZ GZGY GZLH GZST GZZS HBJZ HNAH HNCD HNCZ HNHY HNKF HNZZ HPDS HSMS HZBL HZJJ JXJA JXND JXRJ JXSN JXXS JXYC SCAJ SCBZ SCXC SDDY SDLL SDQD SPZH SYDK WHDX"
# site_list = site_list.split()

all_data,select_site = {},[]
with open(select_site_file,'rt') as f:
    for line in f:
        select_site.append(line[0:4])

#readfile
for cur_ppp in ppp_list:
    cur_path = os.path.join(ppp_path,cur_ppp)
    cur_site = cur_ppp[0:4]
    # if cur_site not in site_list:
    #     continue
    with open(cur_path,'rt') as f:
        last_line = f.readlines()[-1]
    value = last_line.split()
    if len(value) < 1:
        continue
    Num_GPS,Num_GAL,Num_BDS = int(value[13]),int(value[15]),int(value[16])
    # Num_BDS = 0
    # cur_obs = os.path.join(obs_path,cur_site + "2530.23O")
    # with open(cur_obs,'rt') as f:
    #     for line in f:
    #         value_obs = line.split()
    #         if value_obs[0] == "C06":
    #             # value_obs = line.split()
    #             if len(value_obs) == 10:
    #                 Num_BDS = 1
    #             break
    
    if Num_GPS * Num_GAL * Num_BDS == 0:
        continue
    GEC_str = ""
    if Num_GPS > 0:
        GEC_str = GEC_str + "G"
    else:
        GEC_str = GEC_str + "  "
    if Num_GAL > 0:
        GEC_str = GEC_str + " " + "E"
    else:
        GEC_str = GEC_str + "  "
    if Num_BDS > 0:
        GEC_str = GEC_str + " " + "C2 C3"
    else:
        GEC_str = GEC_str + "    "
    with open(out_crd_path,'a') as file:
        str_write = ""
        str_write = str_write + "{:<8}{:>15.4f}{:>15.4f}{:>15.4f}{:>12}  True\n".format(cur_site,float(value[17]),float(value[18]),float(value[19]),GEC_str)
        file.write(str_write)
