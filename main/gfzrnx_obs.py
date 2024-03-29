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

obs_path = r"/Users/hanjunjie/Master_3/Data/2021/OBS_EPN/311/"
select_site_file = r"E:\1Master_2\2-UPD_Test\EPN_SITE\EPN_AUG_GER_SITE.txt"

out_crd_path = r"/Users/hanjunjie/Master_3/1-IUGG/CRDSITE/EPN_ALL_2021311.crd"
is_crd_out = True
out_xml_path = r"/Users/hanjunjie/Master_3/1-IUGG/CRDSITE/EPN_ALL_2021311.xml"
is_xml_out = True
obs_list = os.listdir(obs_path)

all_data,select_site = {},[]
# with open(select_site_file,'rt') as f:
#     for line in f:
#         select_site.append(line[0:4])

#readfile
for cur_obs in obs_list:
    cur_path = os.path.join(obs_path, cur_obs)
    cur_marker = ""
    cur_obs_num = 0
    with open(cur_path,'rt') as f:
        for line in f:
            if "END OF HEADER" in line:
                break
            if "MARKER NAME" in line and cur_marker == "" and line[0] != " ":
                value = line.split(" ")
                cur_marker = value[0][0:4]
                all_data[value[0][0:4]] = {}
                select_site.append(value[0][0:4])
            if "APPROX POSITION XYZ" in line and cur_marker != "" and "COMMENT" not in line:
                value = line.split()
                all_data[cur_marker]["X"] = float(value[0])
                all_data[cur_marker]["Y"] = float(value[1])
                all_data[cur_marker]["Z"] = float(value[2])
            if "SYS / # / OBS TYPES" in line and cur_obs_num == 0:
                sys_type = []
                value = line.split()
                sys_type.append(value[0])
                cur_obs_num = int(value[1])
                for cur_type in value:
                    if "SYS" != cur_type and "/" != cur_type and "#" != cur_type and "OBS" != cur_type and "TYPES" != cur_type and len(cur_type) == 3:
                        sys_type.append(cur_type[0:2])
                while cur_obs_num - 13 > 0:
                    cur_obs_num = cur_obs_num - 13
                    line = next(f)
                    value = line.split()
                    for cur_type in value:
                        if "SYS" != cur_type and "/" != cur_type and "#" != cur_type and "OBS" != cur_type and "TYPES" != cur_type and len(cur_type) == 3:
                            sys_type.append(cur_type[0:2])
                cur_obs_num = 0
                all_data[cur_marker][sys_type[0]] = sys_type[1:len(sys_type)]
#write crd file
if is_crd_out:
    for cur_site in all_data.keys():
        G,E,C2,C3 = False,False,False,False
        with open(out_crd_path,'a') as file:
            str_write = ""
            str_write = str_write + "{:<8}{:>15.4f}{:>15.4f}{:>15.4f}".format(cur_site,all_data[cur_site]["X"],all_data[cur_site]["Y"],all_data[cur_site]["Z"])
            # file.write("{:<8}{:>15.4f}{:>15.4f}{:>15.4f}".format(cur_site,all_data[cur_site]["X"],all_data[cur_site]["Y"],all_data[cur_site]["Z"]))
            if "G" in all_data[cur_site].keys():
                if "L1" in all_data[cur_site]["G"] and "L2" in all_data[cur_site]["G"]:
                    # file.write("    {} ".format("G"))
                    str_write = str_write + "    {} ".format("G")
                    G = True
                else:
                    # file.write("      ")
                    str_write = str_write + "      "
            else:
                # file.write("      ")
                str_write = str_write + "      "
            if "E" in all_data[cur_site].keys():
                if "L1" in all_data[cur_site]["E"] and "L5" in all_data[cur_site]["E"]:
                    # file.write("    {} ".format("E"))
                    str_write = str_write + "    {} ".format("E")
                    E = True
                else:
                    # file.write("      ")
                    str_write = str_write + "      "
            else:
                # file.write("      ")
                str_write = str_write + "      "
            if "C" in all_data[cur_site].keys():
                if "L2" in all_data[cur_site]["C"] and "L6" in all_data[cur_site]["C"]:
                    # file.write("    {}".format("C3"))
                    str_write = str_write + "    {}".format("C3")
                    C3 = True
                    C2 = True
                else:
                    # file.write("      ")
                    str_write = str_write + "      "
            else:
                # file.write("      ")
                str_write = str_write + "      "
            if "C" in all_data[cur_site].keys():
                if "L2" in all_data[cur_site]["C"] and "L7" in all_data[cur_site]["C"]:
                    # file.write("    {}".format("C2"))
                    str_write = str_write + "    {}".format("C2")
                    C2 = True
                else:
                    # file.write("      ")
                    str_write = str_write + "      "
            else:
                # file.write("      ")
                str_write = str_write + "      "
            # if (G and E and C2 and C3):
            if True:
                file.write(str_write)
                if cur_site in select_site:
                    file.write("  True\n")
                else:
                    file.write("  False\n")
#write xml file
if is_xml_out:
    for cur_site in all_data.keys():
        G,E,C2,C3 = False,False,False,False
        with open(out_xml_path,'a') as file:
            str_write = "<rec X=\"{:.4f}\" Y=\"{:.4f}\" Z=\"{:.4f}\" id = \"{}\" />\n".format(all_data[cur_site]["X"],all_data[cur_site]["Y"],all_data[cur_site]["Z"],cur_site)
            if cur_site in select_site:
                file.write(str_write)
    for cur_site in all_data.keys():
        G,E,C2,C3 = False,False,False,False
        with open(out_xml_path,'a') as file:
            str_write = "<STA ID=\"{}\" sigCLK=\"9000\" sigPOS=\"0.1_0.1_0.1\" sigSION=\"9000\" sigTropPd=\"0.015\" sigZTD=\"0.201\" />\n".format(cur_site)
            if cur_site in select_site:
                file.write(str_write)

