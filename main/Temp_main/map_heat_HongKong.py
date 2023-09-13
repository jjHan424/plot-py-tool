from math import ceil
import os
import sys
from turtle import width
from numpy import size
sys.path.insert(0,os.path.dirname(__file__)+'/..')
sys.path.insert(0,os.path.dirname(__file__)+'/../..')
import folium
from folium.features import DivIcon
import matplotlib.pyplot as plt
import webbrowser
import trans as tr
import glv
import readfile as rf
from shapely.ops import triangulate
from shapely import wkt
import math
import matplotlib as mpl
import numpy as np
from folium.plugins import HeatMap
import seaborn as sns
from mpl_toolkits.basemap import Basemap
font_title = {'family' : 'Arial', 'weight' : 300, 'size' : 10}
font_label = {'family' : 'Arial', 'weight' : 300, 'size' : 5}
font_tick = {'family' : 'Arial', 'weight' : 300, 'size' : 35}
font_legend = {'family' : 'Arial', 'weight' : 300, 'size' : 30}
# font_legend = {'family' : 'Times New Roman', 'weight' : 600, 'size' : 15}
font_text = {'family' : 'Arial','weight' : 300,'size'   : 28}
tick_size = 5

def cal_dis_interpolation(client_server,crd_data):
    for cur_site in client_server:
        client_site = cur_site[0:4]
        if client_site not in crd_data.keys():
            continue
        client_crd = crd_data[client_site]["XYZ"]
        print("CLIENT: {}".format(client_site))
        all_dis = []
        for server_site in client_server[cur_site]:
            if server_site not in crd_data.keys():
                continue
            cur_server = crd_data[server_site]["XYZ"]
            delta_xyz = np.array(crd_data[client_site]["XYZ"]) - np.array(crd_data[server_site]["XYZ"])
            dis = math.sqrt(np.sum(delta_xyz*delta_xyz))/1000
            all_dis.append(dis)
            print("{}-{}: {:.2f} km".format(client_site,server_site,dis))
        print("{}-{}: {:.2f} km".format(client_site,"MEAN",np.mean(np.array(all_dis))))

def cal_dis_Grid(client_server,crd_data):
    all_site_dis = {}
    for cur_site in client_server:
        client_site = cur_site[0:4]
        if client_site not in crd_data.keys():
            continue
        all_dis = []
        for server_site in crd_data.keys():
            if server_site == client_site:
                continue
            delta_xyz = np.array(crd_data[client_site]["XYZ"]) - np.array(crd_data[server_site]["XYZ"])
            dis = math.sqrt(np.sum(delta_xyz*delta_xyz))/1000
            all_dis.append(dis)
            # print("{}-{}: {:.2f} km".format(client_site,server_site,dis))
        all_site_dis[cur_site] = all_dis
        # print("{}: {:.2f} km".format(client_site,np.mean(np.array(all_dis))))
    mean_length = 3
    dis_site = {}
    site_dis = {}
    for cur_site in all_site_dis.keys():
        cur_dis = all_site_dis[cur_site]
        cur_dis.sort()
        if mean_length > len(cur_dis):
            mean_length = len(cur_dis)
        # print("{}: {:.2f} km".format(cur_site,np.mean(np.array(cur_dis[0:mean_length-1]))))
        dis_site[np.mean(np.array(cur_dis[0:mean_length-1]))] = cur_site
        site_dis[cur_site] = np.mean(np.array(cur_dis[0:mean_length-1]))
    dis_sort = sorted(dis_site)
    dis_site_new = {}
    for cur_dis in dis_sort:
        print("{}: {:.2f} km".format(dis_site[cur_dis],cur_dis))
        dis_site_new[cur_dis] = dis_site[cur_dis]
    return site_dis
    

crd_file = r"E:\1Master_2\3-IUGG\crd\AUG_HK.crd"
space = 0.1 # Grid space deg
#read crd file
crd_data,B,L = {},[],[]
with open(crd_file,'rt') as f:
    for line in f:
        value = line.split()
        if value[len(value)-1] == "False":
            continue
        crd_data[value[0]] = {}
        xyz = [float(value[1]),float(value[2]),float(value[3])]
        crd_data[value[0]]["XYZ"] = xyz
        blh = tr.xyz2blh(xyz[0],xyz[1],xyz[2])
        blh = [blh[0] / glv.deg,blh[1] / glv.deg,blh[2]]
        if blh[1] > 180:
            blh = [blh[0],blh[1] - 360,blh[2]]
        crd_data[value[0]]["BLH"] = blh
        B.append(blh[0])
        L.append(blh[1])
        crd_data[value[0]]["SYS"] = ""
        for i in range(len(value)-1):
            if i >= 4:
                crd_data[value[0]]["SYS"] = crd_data[value[0]]["SYS"] + value[i]
        crd_data[value[0]]["VALUE"] = value[len(value)-1]
mean_bl = [np.mean(B),np.mean(L)] 

# ##---Marker---##
# for cur_site in crd_data:
#     map.scatter(crd_data[cur_site]["BLH"][1],crd_data[cur_site]["BLH"][0],marker='v',s=10,facecolor='#00BFFF',edgecolor='k', linewidth=0.3)


#---Heat_Map---###
Dir_Diff = r"E:\1Master_2\3-IUGG\Result_Server\Diff\2021305"
grid_diff_file = r"E:\1Master_2\3-IUGG\Result_Server\Diff\2021305\GREAT-GEC-30.grid"
x = np.linspace(113.801, 114.299,200)
y = np.linspace(22.201, 22.599,300)
data_diff = []
X, Y = np.meshgrid(x,y)
p_list = []
# for i in range(len(y)):
#     cur_p_list = []
#     for j in range(len(x)):
#         p = []
#         p_sum = 0
#         for cur_site in crd_data.keys():
#             dL = crd_data[cur_site]["BLH"][1] - x[j]
#             dB = crd_data[cur_site]["BLH"][0] - y[i]
#             cur_p = 1/math.sqrt(math.pow(dL,2)+math.pow(dB,2))
#             p.append(cur_p)
#             p_sum = p_sum + cur_p
#         p = np.array(p) / p_sum
#         cur_p_list.append(p)
#     p_list.append(cur_p_list)

plt.figure(figsize=(2.5,2.1),dpi=600)
year,mon,day,hour,min,sec,Delta = 2021,10,31,1,55,0,300
count = 1
grid_diff_file = r"E:\1Master_2\3-IUGG\Result_Server\Diff\2021310\GREAT-GEC-30.grid"
for i in range(count):
    hour,min,sec = 1,55,0
    day = day + i
    doy = tr.ymd2doy(year,mon,day,0,0,00)
    grid_diff_file = r"E:\1Master_2\3-IUGG\Result_Server\Diff" + "\\" + "{:0>4}{:0>3}".format(int(year),int(doy)) + "\\GREAT-GEC-30.grid"
    while hour<24:
        plt.gcf().set_size_inches(2.5,1.8)
        plt.gcf().set_dpi(600)
        sec = sec + Delta
        if sec >= 60:
            min = min + sec/60
            sec = 0
        if min >= 60:
            hour = hour + min/60
            min = 0
        if hour == 24:
            continue
        ##--From Site--##
        # Diff_all_Site = {}
        # for cur_site in crd_data:
        #     diff_path = os.path.join(Dir_Diff,cur_site+"-GEC-30.diff")
        #     Diff_all_Site[cur_site] = rf.H_open_aug_file_for_heat(diff_path,year,mon,day,hour,min,sec,300)
        #     # print("{}-{:.2f}".format(cur_site,Diff_all_Site[cur_site]*100))
        # Diff_mean_Site = {}
        # for cur_site in Diff_all_Site:
        #     Diff_all_Site[cur_site].remove(np.min(Diff_all_Site[cur_site]))
        #     Diff_all_Site[cur_site].remove(np.max(Diff_all_Site[cur_site]))
        #     Diff_all_Site[cur_site].remove(np.min(Diff_all_Site[cur_site]))
        #     Diff_all_Site[cur_site].remove(np.max(Diff_all_Site[cur_site]))
        #     Diff_all_Site[cur_site].remove(np.min(Diff_all_Site[cur_site]))
        #     Diff_all_Site[cur_site].remove(np.max(Diff_all_Site[cur_site]))
        #     Diff_all_Site[cur_site].remove(np.min(Diff_all_Site[cur_site]))
        #     Diff_all_Site[cur_site].remove(np.max(Diff_all_Site[cur_site]))
        #     Diff_all_Site[cur_site].remove(np.min(Diff_all_Site[cur_site]))
        #     Diff_all_Site[cur_site].remove(np.max(Diff_all_Site[cur_site]))
        #     cur_mean = np.mean(Diff_all_Site[cur_site])
        #     Diff_mean_Site[cur_site] = cur_mean * 100

        # data_diff = []
        # for i in range(len(y)):
        #     cur_diff_list = []
        #     for j in range(len(x)):
        #         diff = []
        #         for cur_site in Diff_all_Site.keys():
        #             diff.append(Diff_mean_Site[cur_site])
        #         cur_diff = np.array(diff) * p_list[i][j]
        #         cur_diff_list.append(cur_diff.sum())
        #     data_diff.append(cur_diff_list)
        # data_diff = np.array(data_diff)


        grid_diff = rf.H_open_grid_file_for_heat(grid_diff_file,year,mon,day,hour,min,sec,0)
        data_diff = []
        for i in range(len(y)):
            cur_diff_list = []
            row = int(((-y[i] + 22.6) / 0.1))
            for j in range(len(x)):
                dis_diff = []
                col = int(((x[j] - 113.8) / 0.1))
                grid_index_1 = row * 6 + col
                dB = 22.6 - row * 0.1 - y[i]
                dL = 113.8 + col * 0.1 - x[j]
                dis_diff.append(1/math.sqrt(math.pow(dB,2) + math.pow(dL,2)))
                grid_index_2 = grid_index_1 + 1
                dB = 22.6 - row * 0.1 - y[i]
                dL = 113.8 + col * 0.1 - x[j] + 0.1
                dis_diff.append(1/math.sqrt(math.pow(dB,2) + math.pow(dL,2)))
                grid_index_3 = (row+1) * 6 + col
                dB = 22.6 - row * 0.1 - y[i] - 0.1
                dL = 113.8 + col * 0.1 - x[j]
                dis_diff.append(1/math.sqrt(math.pow(dB,2) + math.pow(dL,2)))
                grid_index_4 = grid_index_3 + 1    
                dB = 22.6 - row * 0.1 - y[i] - 0.1
                dL = 113.8 + col * 0.1 - x[j] + 0.1
                dis_diff.append(1/math.sqrt(math.pow(dB,2) + math.pow(dL,2)))
                diff = [grid_diff[grid_index_1],grid_diff[grid_index_2],grid_diff[grid_index_3],grid_diff[grid_index_4]]
                p = np.array(dis_diff)/np.sum(np.array(dis_diff))
                cur_diff = np.array(diff) * p
                cur_diff_list.append(cur_diff.sum() * 100)
            data_diff.append(cur_diff_list)
        data_diff = np.array(data_diff)

        
        map = Basemap(llcrnrlon=113.8, llcrnrlat=22.2, urcrnrlon=114.3, urcrnrlat=22.6, resolution='c',projection='cyl')
        map.drawparallels(circles=np.linspace(22.2, 22.6, 5),labels=[1, 0, 0, 0], color='gray',fontsize = tick_size,linewidth=0.5)
        map.drawmeridians(meridians=np.linspace(113.8, 114.3, 6),labels=[0, 0, 0, 1], color='gray',fontsize = tick_size,linewidth=0.5)

        map.readshapefile(r'D:\Tools\gadm36_CHN_shp\gadm36_CHN_0','states',drawbounds=True)
        map.readshapefile(r'D:\Tools\gadm36_HKG_shp\gadm36_HKG_0','states',drawbounds=True)
        map.pcolormesh(x, y, data_diff, cmap='jet', zorder=0,vmin = 0,vmax = 3)
        cp = plt.colorbar(shrink=0.94,format = "%.0f",ticks = [0,1,2,3],pad = 0.01)
        cp.set_label('Iono Error (cm)',fontdict = font_label)
        cp.set_ticklabels((0,1,2,3),fontsize = tick_size)
        plt.title("{:0>4}-{:0>2}-{:0>2} {:0>2}:{:0>2}:{:0>2}".format(int(year),int(mon),int(day),int(hour),int(min),int(sec)),font_title)
        plt.title("{:0>4}-{:0>2}-{:0>2} {:0>2}:{:0>2}:{:0>2}".format(int(year),int(mon),int(day),int(hour),int(min),int(sec)),font_title)
        save_dir = "E:\\1Master_2\\3-IUGG\\Result_Server\\Heat_Save\\{:0>4}{:0>3}_GEC".format(int(year),int(doy))
        if not os.path.exists(save_dir):
            os.mkdir(save_dir)
        save_path = "E:\\1Master_2\\3-IUGG\\Result_Server\\Heat_Save\\{:0>4}{:0>3}_GEC\\{:0>2}{:0>2}{:0>2}.jpg".format(int(year),int(doy),int(hour),int(min),int(sec))
        plt.savefig(save_path)
        # plt.show()
        plt.clf()