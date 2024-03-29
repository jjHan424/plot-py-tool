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
# from shapely.ops import triangulate
# from shapely import wkt
import math
import matplotlib as mpl
import numpy as np
from folium.plugins import HeatMap
import seaborn as sns
# sns.set_style("whitegrid")
from mpl_toolkits.basemap import Basemap
from matplotlib.colorbar import ColorbarBase
from matplotlib.colors import Normalize
font_title = {'family' : 'Arial', 'weight' : 300, 'size' : 20}
font_label = {'family' : 'Arial', 'weight' : 300, 'size' : 20}
font_tick = {'family' : 'Arial', 'weight' : 300, 'size' : 35}
font_legend = {'family' : 'Arial', 'weight' : 300, 'size' : 30}
# font_legend = {'family' : 'Times New Roman', 'weight' : 600, 'size' : 15}
font_text = {'family' : 'Arial','weight' : 300,'size'   : 28}
tick_size = 20

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
    

crd_file = r"/Users/hanjunjie/Master_3/1-IUGG/CRDSITE/EPN_GER_21.crd"
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
# x = np.linspace(113.851, 114.349,200)
# y = np.linspace(22.201, 22.599,300)
x = np.linspace(3.21,10.69,200)
y = np.linspace(48.91,53.39,300)
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

fig = plt.figure(figsize=(16.5,5))
# plt.subplots_adjust(left=0.1,right=0.9,top=0.9,bottom=0.1)
count = 1
# grid_diff_file = "/Users/hanjunjie/Master_3/1-IUGG/AUG2GRID/2021279/GREAT-GEC2-30.grid"
## 331 ##
plt.subplot(1,3,1)
# box = ax.get_position()
# ax.set_position([box.x0, box.y0 + box.y0*0.9, box.width, box.height])
year,mon,day,hour,min,sec,Delta = 2021,11,16,3,20,0,300
doy = tr.ymd2doy(year,mon,day,0,0,00)
grid_diff_file = os.path.join("/Users/hanjunjie/Master_3/1-IUGG/ResFromServer/GRID_ForHeat","{}{:0>3}".format(year,doy),"GREAT-GEC-30.grid")
sec = sec + Delta
if sec >= 60:
    min = min + sec/60
    sec = 0
if min >= 60:
    hour = hour + min/60
    min = 0
grid_diff = rf.H_open_grid_file_for_heat(grid_diff_file,year,mon,day,hour,min,sec,0)
data_diff = []
for i in range(len(y)):
    cur_diff_list = []
    row = int(((-y[i] + 53.4) / 1.5))
    for j in range(len(x)):
        dis_diff = []
        col = int(((x[j] - 3.2) / 1.5))
        grid_index_1 = row * 6 + col
        dB = 53.4 - row * 1.5 - y[i]
        dL = 3.2 + col * 1.5 - x[j]
        dis_diff.append(1/math.sqrt(math.pow(dB,2) + math.pow(dL,2)))
        grid_index_2 = grid_index_1 + 1
        dB = 53.4 - row * 1.5 - y[i]
        dL = 3.2 + col * 1.5 - x[j] + 1.5
        dis_diff.append(1/math.sqrt(math.pow(dB,2) + math.pow(dL,2)))
        grid_index_3 = (row+1) * 6 + col
        dB = 53.4 - row * 1.5 - y[i] - 1.5
        dL = 3.2 + col * 1.5 - x[j]
        dis_diff.append(1/math.sqrt(math.pow(dB,2) + math.pow(dL,2)))
        grid_index_4 = grid_index_3 + 1    
        dB = 53.4 - row * 1.5 - y[i] - 1.5
        dL = 3.2 + col * 1.5 - x[j] + 1.5
        dis_diff.append(1/math.sqrt(math.pow(dB,2) + math.pow(dL,2)))
        diff = [grid_diff[grid_index_1],grid_diff[grid_index_2],grid_diff[grid_index_3],grid_diff[grid_index_4]]
        p = np.array(dis_diff)/np.sum(np.array(dis_diff))
        cur_diff = np.array(diff) * p
        cur_diff_list.append(cur_diff.sum() * 100)
    data_diff.append(cur_diff_list)
data_diff = np.array(data_diff)
map = Basemap(llcrnrlon=3.2, llcrnrlat=48.9, urcrnrlon=10.7, urcrnrlat=53.4, resolution='c',projection='cyl')
map.drawparallels(circles=np.linspace(48.9, 53.4, 4),labels=[1, 0, 0, 0], color='gray',fontsize = tick_size,linewidth=0.5)
map.drawmeridians(meridians=np.linspace(3.2, 10.7, 6),labels=[0, 0, 0, 0], color='gray',fontsize = tick_size,linewidth=0.5)
xlabellon = [4.7,7.7,10.7]
xlabeltext = []
for i in xlabellon:
    xlabeltext.append('%.1f$^\circ$E'%(i))
plt.xticks(xlabellon,xlabeltext,size = tick_size)
map.readshapefile('/Users/hanjunjie/Master_3/1-IUGG/CRDSITE/shp/gadm36_DEU_shp/gadm36_DEU_0','states',drawbounds=True)
map.readshapefile('/Users/hanjunjie/Master_3/1-IUGG/CRDSITE/shp/gadm36_FRA_shp/gadm36_FRA_0','states',drawbounds=True)
map.readshapefile('/Users/hanjunjie/Master_3/1-IUGG/CRDSITE/shp/gadm36_NLD_shp/gadm36_NLD_0','states',drawbounds=True)
map.readshapefile('/Users/hanjunjie/Master_3/1-IUGG/CRDSITE/shp/gadm36_BEL_shp/gadm36_BEL_0','states',drawbounds=True)
map.pcolormesh(x, y, data_diff, cmap='jet', zorder=0,vmin = 0,vmax = 5)
# cp = plt.colorbar(shrink=0.94,format = "%.0f",ticks = [0,1,2,3],pad = 0.01)
# cp.set_label('Iono Error (cm)',fontdict = font_label)
# cp.set_ticklabels((0,1,2,3),fontsize = tick_size)
plt.title("{:0>4}-{:0>2}-{:0>2} {:0>2}:{:0>2}:{:0>2} (GPST)".format(int(year),int(mon),int(day),int(hour),int(min),int(sec)),font_title)

## 334 ##
plt.subplot(1,3,2)
year,mon,day,hour,min,sec,Delta = 2021,11,16,11,45,0,300
doy = tr.ymd2doy(year,mon,day,0,0,00)
grid_diff_file = os.path.join("/Users/hanjunjie/Master_3/1-IUGG/ResFromServer/GRID_ForHeat","{}{:0>3}".format(year,doy),"GREAT-GEC-30.grid")
sec = sec + Delta
if sec >= 60:
    min = min + sec/60
    sec = 0
if min >= 60:
    hour = hour + min/60
    min = 0
grid_diff = rf.H_open_grid_file_for_heat(grid_diff_file,year,mon,day,hour,min,sec,0)
data_diff = []
for i in range(len(y)):
    cur_diff_list = []
    row = int(((-y[i] + 53.4) / 1.5))
    for j in range(len(x)):
        dis_diff = []
        col = int(((x[j] - 3.2) / 1.5))
        grid_index_1 = row * 6 + col
        dB = 53.4 - row * 1.5 - y[i]
        dL = 3.2 + col * 1.5 - x[j]
        dis_diff.append(1/math.sqrt(math.pow(dB,2) + math.pow(dL,2)))
        grid_index_2 = grid_index_1 + 1
        dB = 53.4 - row * 1.5 - y[i]
        dL = 3.2 + col * 1.5 - x[j] + 1.5
        dis_diff.append(1/math.sqrt(math.pow(dB,2) + math.pow(dL,2)))
        grid_index_3 = (row+1) * 6 + col
        dB = 53.4 - row * 1.5 - y[i] - 1.5
        dL = 3.2 + col * 1.5 - x[j]
        dis_diff.append(1/math.sqrt(math.pow(dB,2) + math.pow(dL,2)))
        grid_index_4 = grid_index_3 + 1    
        dB = 53.4 - row * 1.5 - y[i] - 1.5
        dL = 3.2 + col * 1.5 - x[j] + 1.5
        dis_diff.append(1/math.sqrt(math.pow(dB,2) + math.pow(dL,2)))
        diff = [grid_diff[grid_index_1],grid_diff[grid_index_2],grid_diff[grid_index_3],grid_diff[grid_index_4]]
        p = np.array(dis_diff)/np.sum(np.array(dis_diff))
        cur_diff = np.array(diff) * p
        cur_diff_list.append(cur_diff.sum() * 100)
    data_diff.append(cur_diff_list)
data_diff = np.array(data_diff)
map = Basemap(llcrnrlon=3.2, llcrnrlat=48.9, urcrnrlon=10.7, urcrnrlat=53.4, resolution='c',projection='cyl')
map.drawparallels(circles=np.linspace(48.9, 53.4, 4),labels=[0, 0, 0, 0], color='gray',fontsize = tick_size,linewidth=0.5)
map.drawmeridians(meridians=np.linspace(3.2, 10.7, 6),labels=[0, 0, 0, 0], color='gray',fontsize = tick_size,linewidth=0.5)
xlabellon = [4.7,7.7,10.7]
xlabeltext = []
for i in xlabellon:
    xlabeltext.append('%.1f$^\circ$E'%(i))
plt.xticks(xlabellon,xlabeltext,size = tick_size)
map.readshapefile('/Users/hanjunjie/Master_3/1-IUGG/CRDSITE/shp/gadm36_DEU_shp/gadm36_DEU_0','states',drawbounds=True)
map.readshapefile('/Users/hanjunjie/Master_3/1-IUGG/CRDSITE/shp/gadm36_FRA_shp/gadm36_FRA_0','states',drawbounds=True)
map.readshapefile('/Users/hanjunjie/Master_3/1-IUGG/CRDSITE/shp/gadm36_NLD_shp/gadm36_NLD_0','states',drawbounds=True)
map.readshapefile('/Users/hanjunjie/Master_3/1-IUGG/CRDSITE/shp/gadm36_BEL_shp/gadm36_BEL_0','states',drawbounds=True)
map.pcolormesh(x, y, data_diff, cmap='jet', zorder=0,vmin = 0,vmax = 5)
# cp = plt.colorbar(shrink=0.94,format = "%.0f",ticks = [0,1,2,3],pad = 0.01)
# cp.set_label('Iono Error (cm)',fontdict = font_label)
# cp.set_ticklabels((0,1,2,3),fontsize = tick_size)
plt.title("{:0>4}-{:0>2}-{:0>2} {:0>2}:{:0>2}:{:0>2} (GPST)".format(int(year),int(mon),int(day),int(hour),int(min),int(sec)),font_title)

## 337 ##
plt.subplot(1,3,3)
year,mon,day,hour,min,sec,Delta = 2021,11,16,20,20,0,300
doy = tr.ymd2doy(year,mon,day,0,0,00)
grid_diff_file = os.path.join("/Users/hanjunjie/Master_3/1-IUGG/ResFromServer/GRID_ForHeat","{}{:0>3}".format(year,doy),"GREAT-GEC-30.grid")
sec = sec + Delta
if sec >= 60:
    min = min + sec/60
    sec = 0
if min >= 60:
    hour = hour + min/60
    min = 0
grid_diff = rf.H_open_grid_file_for_heat(grid_diff_file,year,mon,day,hour,min,sec,0)
data_diff = []
for i in range(len(y)):
    cur_diff_list = []
    row = int(((-y[i] + 53.4) / 1.5))
    for j in range(len(x)):
        dis_diff = []
        col = int(((x[j] - 3.2) / 1.5))
        grid_index_1 = row * 6 + col
        dB = 53.4 - row * 1.5 - y[i]
        dL = 3.2 + col * 1.5 - x[j]
        dis_diff.append(1/math.sqrt(math.pow(dB,2) + math.pow(dL,2)))
        grid_index_2 = grid_index_1 + 1
        dB = 53.4 - row * 1.5 - y[i]
        dL = 3.2 + col * 1.5 - x[j] + 1.5
        dis_diff.append(1/math.sqrt(math.pow(dB,2) + math.pow(dL,2)))
        grid_index_3 = (row+1) * 6 + col
        dB = 53.4 - row * 1.5 - y[i] - 1.5
        dL = 3.2 + col * 1.5 - x[j]
        dis_diff.append(1/math.sqrt(math.pow(dB,2) + math.pow(dL,2)))
        grid_index_4 = grid_index_3 + 1    
        dB = 53.4 - row * 1.5 - y[i] - 1.5
        dL = 3.2 + col * 1.5 - x[j] + 1.5
        dis_diff.append(1/math.sqrt(math.pow(dB,2) + math.pow(dL,2)))
        diff = [grid_diff[grid_index_1],grid_diff[grid_index_2],grid_diff[grid_index_3],grid_diff[grid_index_4]]
        p = np.array(dis_diff)/np.sum(np.array(dis_diff))
        cur_diff = np.array(diff) * p
        cur_diff_list.append(cur_diff.sum() * 100)
    data_diff.append(cur_diff_list)
data_diff = np.array(data_diff)
map = Basemap(llcrnrlon=3.2, llcrnrlat=48.9, urcrnrlon=10.7, urcrnrlat=53.4, resolution='c',projection='cyl')
map.drawparallels(circles=np.linspace(48.9, 53.4, 4),labels=[0, 0, 0, 0], color='gray',fontsize = tick_size,linewidth=0.5)
map.drawmeridians(meridians=np.linspace(3.2, 10.7, 6),labels=[0, 0, 0, 0], color='gray',fontsize = tick_size,linewidth=0.5)
xlabellon = [4.7,7.7,10.7]
xlabeltext = []
for i in xlabellon:
    xlabeltext.append('%.1f$^\circ$E'%(i))
plt.xticks(xlabellon,xlabeltext,size = tick_size)
map.readshapefile('/Users/hanjunjie/Master_3/1-IUGG/CRDSITE/shp/gadm36_DEU_shp/gadm36_DEU_0','states',drawbounds=True)
map.readshapefile('/Users/hanjunjie/Master_3/1-IUGG/CRDSITE/shp/gadm36_FRA_shp/gadm36_FRA_0','states',drawbounds=True)
map.readshapefile('/Users/hanjunjie/Master_3/1-IUGG/CRDSITE/shp/gadm36_NLD_shp/gadm36_NLD_0','states',drawbounds=True)
map.readshapefile('/Users/hanjunjie/Master_3/1-IUGG/CRDSITE/shp/gadm36_BEL_shp/gadm36_BEL_0','states',drawbounds=True)
map.pcolormesh(x, y, data_diff, cmap='jet', zorder=0,vmin = 0,vmax = 5)
# cp = plt.colorbar(shrink=0.94,format = "%.0f",ticks = [0,1,2,3],pad = 0.01)
# cp.set_label('Iono Error (cm)',fontdict = font_label)
# cp.set_ticklabels((0,1,2,3),fontsize = tick_size)
plt.title("{:0>4}-{:0>2}-{:0>2} {:0>2}:{:0>2}:{:0>2} (GPST)".format(int(year),int(mon),int(day),int(hour),int(min),int(sec)),font_title)

# im = ax.imshow()
plt.subplot(1,3,2)
cbax = plt.axes([0.117,0.15,0.8,0.03]) #left down width height
cp = plt.colorbar(cax=cbax,shrink=2,format = "%.0f",ticks = [0,1,2,3,4,5],pad = 0.1,orientation = "horizontal")
cp.set_label('IONO errors (cm)',fontdict = font_label)
cp.set_ticklabels((0,1,2,3,4,5),fontsize = 25)
# plt.tight_layout()
# save_path = "E:\\1Master_2\\3-IUGG\\Result_Server\\Heat_Save\\{:0>4}{:0>3}_GEC\\{:0>2}{:0>2}{:0>2}.jpg".format(int(year),int(doy),int(hour),int(min),int(sec))
plt.savefig("/Users/hanjunjie/Desktop/Image-1/EPN_GER_DIFF_HEAT.jpg",dpi=300)

# plt.show()
# plt.clf()