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
from adjustText import adjust_text
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
font_text = {'family' : 'Arial','weight' : 300,'size'   : 16}
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

position_errors = {
                        "T430":	[3.085339051060677	,2.318900784854755],
                        "HKLT":	[3.7734460762014344,	1.991374613175532],
                        "HKKT":	[3.112608579632203	,2.119309458290601],
                        "HKSS":	[2.4029383304612706,	2.4613777645863304],
                        "HKWS":	[2.5652507187407627,	2.1814579207493323],
                        "HKSL":	[28.0266427946695,	2.206130254540742],
                        "HKST":	[3.087963056773834,	2.4744343474822683],
                        "HKKS":	[3.58909455294786,	2.214384178502005],
                        "HKCL":	[3.868073692421074	,2.9175056143904845],
                        "HKPC":	[11.398936470566015,	3.366433009878557],
                        "HKNP":	[17.70973470749915	,4.259145244060127],
                        "HKMW":	[14.694818784864276,	2.5890255580044013],
                        "HKLM":	[10.765460222860888,	3.1688301611162437],
                        "HKOH":	[3.89325913085682,	2.9943829013671577]
                  }

crd_file = r"/Users/hanjunjie/Master_3/1-IUGG/CRDSITE/CHN_HK_16.crd"
space = 0.1 # Grid space deg
#read crd file
crd_data,B,L = {},[],[]
with open(crd_file,'rt') as f:
    for line in f:
        value = line.split()
        if value[len(value)-1] == "False":
            continue
        if value[0] not in position_errors.keys():
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



#---Heat_Map---###
Dir_Diff = r"E:\1Master_2\3-IUGG\Result_Server\Diff\2021305"
grid_diff_file = r"E:\1Master_2\3-IUGG\Result_Server\Diff\2021305\GREAT-GEC-30.grid"
x = np.linspace(113.851, 114.349,200)
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

fig = plt.figure(figsize=(15,6))
# plt.subplots_adjust(left=0.1,right=0.9,top=0.9,bottom=0.1)
count = 1
# grid_diff_file = "/Users/hanjunjie/Master_3/1-IUGG/AUG2GRID/2021279/GREAT-GEC2-30.grid"
## 331 ##
plt.subplot(1,3,1)
# box = ax.get_position()
# ax.set_position([box.x0, box.y0 + box.y0*0.9, box.width, box.height])
year,mon,day,hour,min,sec,Delta = 2021,11,1,13,25,0,300
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
    row = int(((-y[i] + 22.6) / 0.1))
    for j in range(len(x)):
        dis_diff = []
        col = int(((x[j] - 113.85) / 0.1))
        grid_index_1 = row * 6 + col
        dB = 22.6 - row * 0.1 - y[i]
        dL = 113.85 + col * 0.1 - x[j]
        dis_diff.append(1/math.sqrt(math.pow(dB,2) + math.pow(dL,2)))
        grid_index_2 = grid_index_1 + 1
        dB = 22.6 - row * 0.1 - y[i]
        dL = 113.85 + col * 0.1 - x[j] + 0.1
        dis_diff.append(1/math.sqrt(math.pow(dB,2) + math.pow(dL,2)))
        grid_index_3 = (row+1) * 6 + col
        dB = 22.6 - row * 0.1 - y[i] - 0.1
        dL = 113.85 + col * 0.1 - x[j]
        dis_diff.append(1/math.sqrt(math.pow(dB,2) + math.pow(dL,2)))
        grid_index_4 = grid_index_3 + 1    
        dB = 22.6 - row * 0.1 - y[i] - 0.1
        dL = 113.85 + col * 0.1 - x[j] + 0.1
        dis_diff.append(1/math.sqrt(math.pow(dB,2) + math.pow(dL,2)))
        diff = [grid_diff[grid_index_1],grid_diff[grid_index_2],grid_diff[grid_index_3],grid_diff[grid_index_4]]
        p = np.array(dis_diff)/np.sum(np.array(dis_diff))
        cur_diff = np.array(diff) * p
        cur_diff_list.append(cur_diff.sum() * 100)
    data_diff.append(cur_diff_list)
data_diff = np.array(data_diff)
map = Basemap(llcrnrlon=113.85, llcrnrlat=22.2, urcrnrlon=114.35, urcrnrlat=22.6, resolution='c',projection='cyl')
map.drawparallels(circles=np.linspace(22.2, 22.6, 5),labels=[0, 0, 0, 0], color='gray',fontsize = tick_size,linewidth=0.5)
map.drawmeridians(meridians=np.linspace(113.85, 114.35, 6),labels=[0, 0, 0, 0], color='gray',fontsize = tick_size,linewidth=0.5)
texts=[]
for cur_site in crd_data:
    map.scatter(crd_data[cur_site]["BLH"][1],crd_data[cur_site]["BLH"][0],marker='o',s=100,facecolor='k',edgecolor='k', linewidth=0.3)
    texts.append(plt.text(crd_data[cur_site]["BLH"][1],crd_data[cur_site]["BLH"][0],cur_site,fontdict=font_text))
adjust_text(texts)
ylabellon = [22.2,22.4,22.6]
ylabeltext = []
for i in ylabellon:
    ylabeltext.append('%.1f$^\circ$N'%(i))
plt.yticks(ylabellon,ylabeltext,size = tick_size)
xlabellon = [113.9,114.1,114.3]
xlabeltext = []
for i in xlabellon:
    xlabeltext.append('%.1f$^\circ$E'%(i))
plt.xticks(xlabellon,xlabeltext,size = tick_size)
# plt.title("{:0>4}-{:0>2}-{:0>2} {:0>2}:{:0>2}:{:0>2} (GPST)".format(int(year),int(mon),int(day),int(hour),int(min),int(sec)),font_title)
map.readshapefile(r'/Users/hanjunjie/Master_3/1-IUGG/CRDSITE/shp/gadm36_CHN_shp/gadm36_CHN_0','states',drawbounds=True)
map.readshapefile(r'/Users/hanjunjie/Master_3/1-IUGG/CRDSITE/shp/gadm36_HKG_shp/gadm36_HKG_0','states',drawbounds=True)
map.pcolormesh(x, y, data_diff, cmap='jet', zorder=0,vmin = 0,vmax = 3)
cbax = plt.axes([0.08,0.12,0.28,0.015]) #left down width height
cp = plt.colorbar(cax=cbax,shrink=2,format = "%.0f",ticks = [0,1,2,3],pad = 0.1,orientation = "horizontal")
cp.set_label('IONO errors (cm)',fontdict = font_label)
cp.set_ticklabels((0,1,2,3),fontsize = 20)

plt.subplot(1,3,2)
# box = ax.get_position()
# ax.set_position([box.x0, box.y0 + box.y0*0.9, box.width, box.height])

list_all_postion = []
for cur_site in position_errors.keys():
    list_all_postion.append(position_errors[cur_site][0])
    list_all_postion.append(position_errors[cur_site][1])
min_position = np.min(np.array(list_all_postion))
max_position = np.max(np.array(list_all_postion))

year,mon,day,hour,min,sec,Delta = 2021,11,1,13,25,0,300
doy = tr.ymd2doy(year,mon,day,0,0,00)
grid_diff_file = os.path.join("/Users/hanjunjie/Master_3/1-IUGG/ResFromServer/GRID_ForHeat","{}{:0>3}".format(year,doy),"GREAT-GEC-30.grid")
sec = sec + Delta
if sec >= 60:
    min = min + sec/60
    sec = 0
if min >= 60:
    hour = hour + min/60
    min = 0
map = Basemap(llcrnrlon=113.85, llcrnrlat=22.2, urcrnrlon=114.35, urcrnrlat=22.6, resolution='c',projection='cyl')
map.drawparallels(circles=np.linspace(22.2, 22.6, 5),labels=[0, 0, 0, 0], color='gray',fontsize = tick_size,linewidth=0.5)
map.drawmeridians(meridians=np.linspace(113.85, 114.35, 6),labels=[0, 0, 0, 0], color='gray',fontsize = tick_size,linewidth=0.5)
texts=[]
for cur_site in crd_data:
    heat_value = position_errors[cur_site][0]
    norm_heat_value =(heat_value - min_position)/(max_position - min_position)
    heat_color = plt.cm.jet(norm_heat_value)
    map.scatter(crd_data[cur_site]["BLH"][1],crd_data[cur_site]["BLH"][0],marker='o',s=100,facecolor=heat_color,edgecolor=heat_color, linewidth=0.3)
    texts.append(plt.text(crd_data[cur_site]["BLH"][1],crd_data[cur_site]["BLH"][0],cur_site,fontdict=font_text))
adjust_text(texts)
xlabellon = [113.9,114.1,114.3]
xlabeltext = []
for i in xlabellon:
    xlabeltext.append('%.1f$^\circ$E'%(i))
plt.xticks(xlabellon,xlabeltext,size = tick_size)
map.readshapefile(r'/Users/hanjunjie/Master_3/1-IUGG/CRDSITE/shp/gadm36_CHN_shp/gadm36_CHN_0','states',drawbounds=True)
map.readshapefile(r'/Users/hanjunjie/Master_3/1-IUGG/CRDSITE/shp/gadm36_HKG_shp/gadm36_HKG_0','states',drawbounds=True)
# map.pcolormesh(x, y, data_diff, cmap='jet', zorder=0,vmin = 0,vmax = 3)


plt.subplot(1,3,3)
# box = ax.get_position()
# ax.set_position([box.x0, box.y0 + box.y0*0.9, box.width, box.height])
year,mon,day,hour,min,sec,Delta = 2021,11,1,13,25,0,300
doy = tr.ymd2doy(year,mon,day,0,0,00)
grid_diff_file = os.path.join("/Users/hanjunjie/Master_3/1-IUGG/ResFromServer/GRID_ForHeat","{}{:0>3}".format(year,doy),"GREAT-GEC-30.grid")
sec = sec + Delta
if sec >= 60:
    min = min + sec/60
    sec = 0
if min >= 60:
    hour = hour + min/60
    min = 0
map = Basemap(llcrnrlon=113.85, llcrnrlat=22.2, urcrnrlon=114.35, urcrnrlat=22.6, resolution='c',projection='cyl')
map.drawparallels(circles=np.linspace(22.2, 22.6, 5),labels=[0, 0, 0, 0], color='gray',fontsize = tick_size,linewidth=0.5)
map.drawmeridians(meridians=np.linspace(113.85, 114.35, 6),labels=[0, 0, 0, 0], color='gray',fontsize = tick_size,linewidth=0.5)
texts=[]
for cur_site in crd_data:
    heat_value = position_errors[cur_site][1]
    norm_heat_value =(heat_value - min_position)/(max_position - min_position)
    heat_color = plt.cm.jet(norm_heat_value)
    map.scatter(crd_data[cur_site]["BLH"][1],crd_data[cur_site]["BLH"][0],marker='o',s=100,facecolor=heat_color,edgecolor=heat_color, linewidth=0.3)
    texts.append(plt.text(crd_data[cur_site]["BLH"][1],crd_data[cur_site]["BLH"][0],cur_site,fontdict=font_text))
adjust_text(texts)
xlabellon = [113.9,114.1,114.3]
xlabeltext = []
for i in xlabellon:
    xlabeltext.append('%.1f$^\circ$E'%(i))
plt.xticks(xlabellon,xlabeltext,size = tick_size)
map.readshapefile(r'/Users/hanjunjie/Master_3/1-IUGG/CRDSITE/shp/gadm36_CHN_shp/gadm36_CHN_0','states',drawbounds=True)
map.readshapefile(r'/Users/hanjunjie/Master_3/1-IUGG/CRDSITE/shp/gadm36_HKG_shp/gadm36_HKG_0','states',drawbounds=True)
# map.pcolormesh(x, y, data_diff, cmap='jet', zorder=0,vmin = 0,vmax = 3)
norm = Normalize(vmin = 0,vmax=max_position)
cbax = plt.axes([0.40,0.12,0.56,0.015]) #left down width height
# cb = plt.colorbar(cax=cbax,shrink=2,format = "%.0f",ticks = [0,5,10,15,20,25],pad = 0.1,orientation = "horizontal")
cb = ColorbarBase(cbax,cmap = plt.cm.jet,norm=norm,orientation='horizontal')
cb.set_label('3D positioning errors (cm)',fontsize=20,fontname="Arial")
cb.set_ticklabels([0,5,10,15,20,25],fontsize=20,fontname="Arial")

# ## 334 ##
# plt.subplot(3,3,4)
# year,mon,day,hour,min,sec,Delta = 2021,11,1,6,25,0,300
# doy = tr.ymd2doy(year,mon,day,0,0,00)
# grid_diff_file = os.path.join("/Users/hanjunjie/Master_3/1-IUGG/ResFromServer/GRID_ForHeat","{}{:0>3}".format(year,doy),"GREAT-GEC-30.grid")
# sec = sec + Delta
# if sec >= 60:
#     min = min + sec/60
#     sec = 0
# if min >= 60:
#     hour = hour + min/60
#     min = 0
# grid_diff = rf.H_open_grid_file_for_heat(grid_diff_file,year,mon,day,hour,min,sec,0)
# data_diff = []
# for i in range(len(y)):
#     cur_diff_list = []
#     row = int(((-y[i] + 22.6) / 0.1))
#     for j in range(len(x)):
#         dis_diff = []
#         col = int(((x[j] - 113.85) / 0.1))
#         grid_index_1 = row * 6 + col
#         dB = 22.6 - row * 0.1 - y[i]
#         dL = 113.85 + col * 0.1 - x[j]
#         dis_diff.append(1/math.sqrt(math.pow(dB,2) + math.pow(dL,2)))
#         grid_index_2 = grid_index_1 + 1
#         dB = 22.6 - row * 0.1 - y[i]
#         dL = 113.85 + col * 0.1 - x[j] + 0.1
#         dis_diff.append(1/math.sqrt(math.pow(dB,2) + math.pow(dL,2)))
#         grid_index_3 = (row+1) * 6 + col
#         dB = 22.6 - row * 0.1 - y[i] - 0.1
#         dL = 113.85 + col * 0.1 - x[j]
#         dis_diff.append(1/math.sqrt(math.pow(dB,2) + math.pow(dL,2)))
#         grid_index_4 = grid_index_3 + 1    
#         dB = 22.6 - row * 0.1 - y[i] - 0.1
#         dL = 113.85 + col * 0.1 - x[j] + 0.1
#         dis_diff.append(1/math.sqrt(math.pow(dB,2) + math.pow(dL,2)))
#         diff = [grid_diff[grid_index_1],grid_diff[grid_index_2],grid_diff[grid_index_3],grid_diff[grid_index_4]]
#         p = np.array(dis_diff)/np.sum(np.array(dis_diff))
#         cur_diff = np.array(diff) * p
#         cur_diff_list.append(cur_diff.sum() * 100)
#     data_diff.append(cur_diff_list)
# data_diff = np.array(data_diff)
# map = Basemap(llcrnrlon=113.85, llcrnrlat=22.2, urcrnrlon=114.35, urcrnrlat=22.6, resolution='c',projection='cyl')
# map.drawparallels(circles=np.linspace(22.2, 22.6, 5),labels=[0, 0, 0, 0], color='gray',fontsize = tick_size,linewidth=0.5)
# map.drawmeridians(meridians=np.linspace(113.85, 114.35, 6),labels=[0, 0, 0, 0], color='gray',fontsize = tick_size,linewidth=0.5)
# # xlabellon = [113.95,114.15,114.35]
# # xlabeltext = []
# # for i in xlabellon:
# #     xlabeltext.append('%.1f$^\circ$E'%(i))
# # plt.xticks(xlabellon,xlabeltext,size = tick_size)
# ylabellon = [22.2,22.4,22.6]
# ylabeltext = []
# for i in ylabellon:
#     ylabeltext.append('%.1f$^\circ$N'%(i))
# plt.yticks(ylabellon,ylabeltext,size = tick_size)
# map.readshapefile(r'/Users/hanjunjie/Master_3/1-IUGG/CRDSITE/shp/gadm36_CHN_shp/gadm36_CHN_0','states',drawbounds=True)
# map.readshapefile(r'/Users/hanjunjie/Master_3/1-IUGG/CRDSITE/shp/gadm36_HKG_shp/gadm36_HKG_0','states',drawbounds=True)
# map.pcolormesh(x, y, data_diff, cmap='jet', zorder=0,vmin = 0,vmax = 3)
# # cp = plt.colorbar(shrink=0.94,format = "%.0f",ticks = [0,1,2,3],pad = 0.01)
# # cp.set_label('Iono Error (cm)',fontdict = font_label)
# # cp.set_ticklabels((0,1,2,3),fontsize = tick_size)
# plt.title("{:0>4}-{:0>2}-{:0>2} {:0>2}:{:0>2}:{:0>2} (GPST)".format(int(year),int(mon),int(day),int(hour),int(min),int(sec)),font_title)

# ## 337 ##
# plt.subplot(3,3,7)
# year,mon,day,hour,min,sec,Delta = 2021,11,2,6,25,0,300
# doy = tr.ymd2doy(year,mon,day,0,0,00)
# grid_diff_file = os.path.join("/Users/hanjunjie/Master_3/1-IUGG/ResFromServer/GRID_ForHeat","{}{:0>3}".format(year,doy),"GREAT-GEC-30.grid")
# sec = sec + Delta
# if sec >= 60:
#     min = min + sec/60
#     sec = 0
# if min >= 60:
#     hour = hour + min/60
#     min = 0
# grid_diff = rf.H_open_grid_file_for_heat(grid_diff_file,year,mon,day,hour,min,sec,0)
# data_diff = []
# for i in range(len(y)):
#     cur_diff_list = []
#     row = int(((-y[i] + 22.6) / 0.1))
#     for j in range(len(x)):
#         dis_diff = []
#         col = int(((x[j] - 113.85) / 0.1))
#         grid_index_1 = row * 6 + col
#         dB = 22.6 - row * 0.1 - y[i]
#         dL = 113.85 + col * 0.1 - x[j]
#         dis_diff.append(1/math.sqrt(math.pow(dB,2) + math.pow(dL,2)))
#         grid_index_2 = grid_index_1 + 1
#         dB = 22.6 - row * 0.1 - y[i]
#         dL = 113.85 + col * 0.1 - x[j] + 0.1
#         dis_diff.append(1/math.sqrt(math.pow(dB,2) + math.pow(dL,2)))
#         grid_index_3 = (row+1) * 6 + col
#         dB = 22.6 - row * 0.1 - y[i] - 0.1
#         dL = 113.85 + col * 0.1 - x[j]
#         dis_diff.append(1/math.sqrt(math.pow(dB,2) + math.pow(dL,2)))
#         grid_index_4 = grid_index_3 + 1    
#         dB = 22.6 - row * 0.1 - y[i] - 0.1
#         dL = 113.85 + col * 0.1 - x[j] + 0.1
#         dis_diff.append(1/math.sqrt(math.pow(dB,2) + math.pow(dL,2)))
#         diff = [grid_diff[grid_index_1],grid_diff[grid_index_2],grid_diff[grid_index_3],grid_diff[grid_index_4]]
#         p = np.array(dis_diff)/np.sum(np.array(dis_diff))
#         cur_diff = np.array(diff) * p
#         cur_diff_list.append(cur_diff.sum() * 100)
#     data_diff.append(cur_diff_list)
# data_diff = np.array(data_diff)
# map = Basemap(llcrnrlon=113.85, llcrnrlat=22.2, urcrnrlon=114.35, urcrnrlat=22.6, resolution='c',projection='cyl')
# map.drawparallels(circles=np.linspace(22.2, 22.6, 5),labels=[0, 0, 0, 0], color='gray',fontsize = tick_size,linewidth=0.5)
# map.drawmeridians(meridians=np.linspace(113.85, 114.35, 6),labels=[0, 0, 0, 0], color='gray',fontsize = tick_size,linewidth=0.5)
# xlabellon = [113.9,114.1,114.3]
# xlabeltext = []
# for i in xlabellon:
#     xlabeltext.append('%.1f$^\circ$E'%(i))
# plt.xticks(xlabellon,xlabeltext,size = tick_size)
# ylabellon = [22.2,22.4,22.6]
# ylabeltext = []
# for i in ylabellon:
#     ylabeltext.append('%.1f$^\circ$N'%(i))
# plt.yticks(ylabellon,ylabeltext,size = tick_size)
# map.readshapefile(r'/Users/hanjunjie/Master_3/1-IUGG/CRDSITE/shp/gadm36_CHN_shp/gadm36_CHN_0','states',drawbounds=True)
# map.readshapefile(r'/Users/hanjunjie/Master_3/1-IUGG/CRDSITE/shp/gadm36_HKG_shp/gadm36_HKG_0','states',drawbounds=True)
# map.pcolormesh(x, y, data_diff, cmap='jet', zorder=0,vmin = 0,vmax = 3)
# # cp = plt.colorbar(shrink=0.94,format = "%.0f",ticks = [0,1,2,3],pad = 0.01)
# # cp.set_label('Iono Error (cm)',fontdict = font_label)
# # cp.set_ticklabels((0,1,2,3),fontsize = tick_size)
# plt.title("{:0>4}-{:0>2}-{:0>2} {:0>2}:{:0>2}:{:0>2} (GPST)".format(int(year),int(mon),int(day),int(hour),int(min),int(sec)),font_title)

# ## 332 ##
# plt.subplot(3,3,2)
# year,mon,day,hour,min,sec,Delta = 2021,10,31,13,25,0,300
# doy = tr.ymd2doy(year,mon,day,0,0,00)
# grid_diff_file = os.path.join("/Users/hanjunjie/Master_3/1-IUGG/ResFromServer/GRID_ForHeat","{}{:0>3}".format(year,doy),"GREAT-GEC-30.grid")
# sec = sec + Delta
# if sec >= 60:
#     min = min + sec/60
#     sec = 0
# if min >= 60:
#     hour = hour + min/60
#     min = 0
# grid_diff = rf.H_open_grid_file_for_heat(grid_diff_file,year,mon,day,hour,min,sec,0)
# data_diff = []
# for i in range(len(y)):
#     cur_diff_list = []
#     row = int(((-y[i] + 22.6) / 0.1))
#     for j in range(len(x)):
#         dis_diff = []
#         col = int(((x[j] - 113.85) / 0.1))
#         grid_index_1 = row * 6 + col
#         dB = 22.6 - row * 0.1 - y[i]
#         dL = 113.85 + col * 0.1 - x[j]
#         dis_diff.append(1/math.sqrt(math.pow(dB,2) + math.pow(dL,2)))
#         grid_index_2 = grid_index_1 + 1
#         dB = 22.6 - row * 0.1 - y[i]
#         dL = 113.85 + col * 0.1 - x[j] + 0.1
#         dis_diff.append(1/math.sqrt(math.pow(dB,2) + math.pow(dL,2)))
#         grid_index_3 = (row+1) * 6 + col
#         dB = 22.6 - row * 0.1 - y[i] - 0.1
#         dL = 113.85 + col * 0.1 - x[j]
#         dis_diff.append(1/math.sqrt(math.pow(dB,2) + math.pow(dL,2)))
#         grid_index_4 = grid_index_3 + 1    
#         dB = 22.6 - row * 0.1 - y[i] - 0.1
#         dL = 113.85 + col * 0.1 - x[j] + 0.1
#         dis_diff.append(1/math.sqrt(math.pow(dB,2) + math.pow(dL,2)))
#         diff = [grid_diff[grid_index_1],grid_diff[grid_index_2],grid_diff[grid_index_3],grid_diff[grid_index_4]]
#         p = np.array(dis_diff)/np.sum(np.array(dis_diff))
#         cur_diff = np.array(diff) * p
#         cur_diff_list.append(cur_diff.sum() * 100)
#     data_diff.append(cur_diff_list)
# data_diff = np.array(data_diff)
# map = Basemap(llcrnrlon=113.85, llcrnrlat=22.2, urcrnrlon=114.35, urcrnrlat=22.6, resolution='c',projection='cyl')
# map.drawparallels(circles=np.linspace(22.2, 22.6, 5),labels=[0, 0, 0, 0], color='gray',fontsize = tick_size,linewidth=0.5)
# map.drawmeridians(meridians=np.linspace(113.85, 114.35, 6),labels=[0, 0, 0, 0], color='gray',fontsize = tick_size,linewidth=0.5)
# # xlabellon = [113.95,114.15,114.35]
# # xlabeltext = []
# # for i in xlabellon:
# #     xlabeltext.append('%.1f$^\circ$E'%(i))
# # plt.xticks(xlabellon,xlabeltext,size = tick_size)
# map.readshapefile(r'/Users/hanjunjie/Master_3/1-IUGG/CRDSITE/shp/gadm36_CHN_shp/gadm36_CHN_0','states',drawbounds=True)
# map.readshapefile(r'/Users/hanjunjie/Master_3/1-IUGG/CRDSITE/shp/gadm36_HKG_shp/gadm36_HKG_0','states',drawbounds=True)
# map.pcolormesh(x, y, data_diff, cmap='jet', zorder=0,vmin = 0,vmax = 3)
# # cp = plt.colorbar(shrink=0.94,format = "%.0f",ticks = [0,1,2,3],pad = 0.01)
# # cp.set_label('Iono Error (cm)',fontdict = font_label)
# # cp.set_ticklabels((0,1,2,3),fontsize = tick_size)
# plt.title("{:0>4}-{:0>2}-{:0>2} {:0>2}:{:0>2}:{:0>2} (GPST)".format(int(year),int(mon),int(day),int(hour),int(min),int(sec)),font_title)

# ## 335 ##
# plt.subplot(3,3,5)
# year,mon,day,hour,min,sec,Delta = 2021,11,1,13,25,0,300
# doy = tr.ymd2doy(year,mon,day,0,0,00)
# grid_diff_file = os.path.join("/Users/hanjunjie/Master_3/1-IUGG/ResFromServer/GRID_ForHeat","{}{:0>3}".format(year,doy),"GREAT-GEC-30.grid")
# sec = sec + Delta
# if sec >= 60:
#     min = min + sec/60
#     sec = 0
# if min >= 60:
#     hour = hour + min/60
#     min = 0
# grid_diff = rf.H_open_grid_file_for_heat(grid_diff_file,year,mon,day,hour,min,sec,0)
# data_diff = []
# for i in range(len(y)):
#     cur_diff_list = []
#     row = int(((-y[i] + 22.6) / 0.1))
#     for j in range(len(x)):
#         dis_diff = []
#         col = int(((x[j] - 113.85) / 0.1))
#         grid_index_1 = row * 6 + col
#         dB = 22.6 - row * 0.1 - y[i]
#         dL = 113.85 + col * 0.1 - x[j]
#         dis_diff.append(1/math.sqrt(math.pow(dB,2) + math.pow(dL,2)))
#         grid_index_2 = grid_index_1 + 1
#         dB = 22.6 - row * 0.1 - y[i]
#         dL = 113.85 + col * 0.1 - x[j] + 0.1
#         dis_diff.append(1/math.sqrt(math.pow(dB,2) + math.pow(dL,2)))
#         grid_index_3 = (row+1) * 6 + col
#         dB = 22.6 - row * 0.1 - y[i] - 0.1
#         dL = 113.85 + col * 0.1 - x[j]
#         dis_diff.append(1/math.sqrt(math.pow(dB,2) + math.pow(dL,2)))
#         grid_index_4 = grid_index_3 + 1    
#         dB = 22.6 - row * 0.1 - y[i] - 0.1
#         dL = 113.85 + col * 0.1 - x[j] + 0.1
#         dis_diff.append(1/math.sqrt(math.pow(dB,2) + math.pow(dL,2)))
#         diff = [grid_diff[grid_index_1],grid_diff[grid_index_2],grid_diff[grid_index_3],grid_diff[grid_index_4]]
#         p = np.array(dis_diff)/np.sum(np.array(dis_diff))
#         cur_diff = np.array(diff) * p
#         cur_diff_list.append(cur_diff.sum() * 100)
#     data_diff.append(cur_diff_list)
# data_diff = np.array(data_diff)
# map = Basemap(llcrnrlon=113.85, llcrnrlat=22.2, urcrnrlon=114.35, urcrnrlat=22.6, resolution='c',projection='cyl')
# map.drawparallels(circles=np.linspace(22.2, 22.6, 5),labels=[0, 0, 0, 0], color='gray',fontsize = tick_size,linewidth=0.5)
# map.drawmeridians(meridians=np.linspace(113.85, 114.35, 6),labels=[0, 0, 0, 0], color='gray',fontsize = tick_size,linewidth=0.5)
# # xlabellon = [113.95,114.15,114.35]
# # xlabeltext = []
# # for i in xlabellon:
# #     xlabeltext.append('%.1f$^\circ$E'%(i))
# # plt.xticks(xlabellon,xlabeltext,size = tick_size)
# map.readshapefile(r'/Users/hanjunjie/Master_3/1-IUGG/CRDSITE/shp/gadm36_CHN_shp/gadm36_CHN_0','states',drawbounds=True)
# map.readshapefile(r'/Users/hanjunjie/Master_3/1-IUGG/CRDSITE/shp/gadm36_HKG_shp/gadm36_HKG_0','states',drawbounds=True)
# map.pcolormesh(x, y, data_diff, cmap='jet', zorder=0,vmin = 0,vmax = 3)
# # cp = plt.colorbar(shrink=0.94,format = "%.0f",ticks = [0,1,2,3],pad = 0.01)
# # cp.set_label('Iono Error (cm)',fontdict = font_label)
# # cp.set_ticklabels((0,1,2,3),fontsize = tick_size)
# plt.title("{:0>4}-{:0>2}-{:0>2} {:0>2}:{:0>2}:{:0>2} (GPST)".format(int(year),int(mon),int(day),int(hour),int(min),int(sec)),font_title)

# ## 335 ##
# plt.subplot(3,3,8)
# year,mon,day,hour,min,sec,Delta = 2021,11,2,13,25,0,300
# doy = tr.ymd2doy(year,mon,day,0,0,00)
# grid_diff_file = os.path.join("/Users/hanjunjie/Master_3/1-IUGG/ResFromServer/GRID_ForHeat","{}{:0>3}".format(year,doy),"GREAT-GEC-30.grid")
# sec = sec + Delta
# if sec >= 60:
#     min = min + sec/60
#     sec = 0
# if min >= 60:
#     hour = hour + min/60
#     min = 0
# grid_diff = rf.H_open_grid_file_for_heat(grid_diff_file,year,mon,day,hour,min,sec,0)
# data_diff = []
# for i in range(len(y)):
#     cur_diff_list = []
#     row = int(((-y[i] + 22.6) / 0.1))
#     for j in range(len(x)):
#         dis_diff = []
#         col = int(((x[j] - 113.85) / 0.1))
#         grid_index_1 = row * 6 + col
#         dB = 22.6 - row * 0.1 - y[i]
#         dL = 113.85 + col * 0.1 - x[j]
#         dis_diff.append(1/math.sqrt(math.pow(dB,2) + math.pow(dL,2)))
#         grid_index_2 = grid_index_1 + 1
#         dB = 22.6 - row * 0.1 - y[i]
#         dL = 113.85 + col * 0.1 - x[j] + 0.1
#         dis_diff.append(1/math.sqrt(math.pow(dB,2) + math.pow(dL,2)))
#         grid_index_3 = (row+1) * 6 + col
#         dB = 22.6 - row * 0.1 - y[i] - 0.1
#         dL = 113.85 + col * 0.1 - x[j]
#         dis_diff.append(1/math.sqrt(math.pow(dB,2) + math.pow(dL,2)))
#         grid_index_4 = grid_index_3 + 1    
#         dB = 22.6 - row * 0.1 - y[i] - 0.1
#         dL = 113.85 + col * 0.1 - x[j] + 0.1
#         dis_diff.append(1/math.sqrt(math.pow(dB,2) + math.pow(dL,2)))
#         diff = [grid_diff[grid_index_1],grid_diff[grid_index_2],grid_diff[grid_index_3],grid_diff[grid_index_4]]
#         p = np.array(dis_diff)/np.sum(np.array(dis_diff))
#         cur_diff = np.array(diff) * p
#         cur_diff_list.append(cur_diff.sum() * 100)
#     data_diff.append(cur_diff_list)
# data_diff = np.array(data_diff)
# map = Basemap(llcrnrlon=113.85, llcrnrlat=22.2, urcrnrlon=114.35, urcrnrlat=22.6, resolution='c',projection='cyl')
# map.drawparallels(circles=np.linspace(22.2, 22.6, 5),labels=[0, 0, 0, 0], color='gray',fontsize = tick_size,linewidth=0.5)
# map.drawmeridians(meridians=np.linspace(113.85, 114.35, 6),labels=[0, 0, 0, 0], color='gray',fontsize = tick_size,linewidth=0.5)
# xlabellon = [113.9,114.1,114.3]
# xlabeltext = []
# for i in xlabellon:
#     xlabeltext.append('%.1f$^\circ$E'%(i))
# plt.xticks(xlabellon,xlabeltext,size = tick_size)
# map.readshapefile(r'/Users/hanjunjie/Master_3/1-IUGG/CRDSITE/shp/gadm36_CHN_shp/gadm36_CHN_0','states',drawbounds=True)
# map.readshapefile(r'/Users/hanjunjie/Master_3/1-IUGG/CRDSITE/shp/gadm36_HKG_shp/gadm36_HKG_0','states',drawbounds=True)
# map.pcolormesh(x, y, data_diff, cmap='jet', zorder=0,vmin = 0,vmax = 3)
# # cp = plt.colorbar(shrink=1,format = "%.0f",ticks = [0,1,2,3],pad = 0.1,orientation = "horizontal")
# # cp.set_label('IONO errors (cm)',fontdict = font_label)
# # cp.set_ticklabels((0,1,2,3),fontsize = tick_size)
# plt.title("{:0>4}-{:0>2}-{:0>2} {:0>2}:{:0>2}:{:0>2} (GPST)".format(int(year),int(mon),int(day),int(hour),int(min),int(sec)),font_title)
# # cax = plt.axes([1,1,0.5,0.02]) #left down width height
# # norm = Normalize(vmin = 0,vmax=3)
# # cb = ColorbarBase(cax,cmap = plt.cm.jet,norm=norm,orientation='horizontal')
# # cb.set_label('Residuals after polynomial fitting (cm)',fontsize=15,fontname="Arial")
# # cb.set_ticklabels([0,1,2,3],fontsize=15,fontname="Arial")

# ## 332 ##
# plt.subplot(3,3,3)
# year,mon,day,hour,min,sec,Delta = 2021,10,31,20,25,0,300
# doy = tr.ymd2doy(year,mon,day,0,0,00)
# grid_diff_file = os.path.join("/Users/hanjunjie/Master_3/1-IUGG/ResFromServer/GRID_ForHeat","{}{:0>3}".format(year,doy),"GREAT-GEC-30.grid")
# sec = sec + Delta
# if sec >= 60:
#     min = min + sec/60
#     sec = 0
# if min >= 60:
#     hour = hour + min/60
#     min = 0
# grid_diff = rf.H_open_grid_file_for_heat(grid_diff_file,year,mon,day,hour,min,sec,0)
# data_diff = []
# for i in range(len(y)):
#     cur_diff_list = []
#     row = int(((-y[i] + 22.6) / 0.1))
#     for j in range(len(x)):
#         dis_diff = []
#         col = int(((x[j] - 113.85) / 0.1))
#         grid_index_1 = row * 6 + col
#         dB = 22.6 - row * 0.1 - y[i]
#         dL = 113.85 + col * 0.1 - x[j]
#         dis_diff.append(1/math.sqrt(math.pow(dB,2) + math.pow(dL,2)))
#         grid_index_2 = grid_index_1 + 1
#         dB = 22.6 - row * 0.1 - y[i]
#         dL = 113.85 + col * 0.1 - x[j] + 0.1
#         dis_diff.append(1/math.sqrt(math.pow(dB,2) + math.pow(dL,2)))
#         grid_index_3 = (row+1) * 6 + col
#         dB = 22.6 - row * 0.1 - y[i] - 0.1
#         dL = 113.85 + col * 0.1 - x[j]
#         dis_diff.append(1/math.sqrt(math.pow(dB,2) + math.pow(dL,2)))
#         grid_index_4 = grid_index_3 + 1    
#         dB = 22.6 - row * 0.1 - y[i] - 0.1
#         dL = 113.85 + col * 0.1 - x[j] + 0.1
#         dis_diff.append(1/math.sqrt(math.pow(dB,2) + math.pow(dL,2)))
#         diff = [grid_diff[grid_index_1],grid_diff[grid_index_2],grid_diff[grid_index_3],grid_diff[grid_index_4]]
#         p = np.array(dis_diff)/np.sum(np.array(dis_diff))
#         cur_diff = np.array(diff) * p
#         cur_diff_list.append(cur_diff.sum() * 100)
#     data_diff.append(cur_diff_list)
# data_diff = np.array(data_diff)
# map = Basemap(llcrnrlon=113.85, llcrnrlat=22.2, urcrnrlon=114.35, urcrnrlat=22.6, resolution='c',projection='cyl')
# map.drawparallels(circles=np.linspace(22.2, 22.6, 5),labels=[0, 0, 0, 0], color='gray',fontsize = tick_size,linewidth=0.5)
# map.drawmeridians(meridians=np.linspace(113.85, 114.35, 6),labels=[0, 0, 0, 0], color='gray',fontsize = tick_size,linewidth=0.5)
# # xlabellon = [113.95,114.15,114.35]
# # xlabeltext = []
# # for i in xlabellon:
# #     xlabeltext.append('%.1f$^\circ$E'%(i))
# # plt.xticks(xlabellon,xlabeltext,size = tick_size)
# map.readshapefile(r'/Users/hanjunjie/Master_3/1-IUGG/CRDSITE/shp/gadm36_CHN_shp/gadm36_CHN_0','states',drawbounds=True)
# map.readshapefile(r'/Users/hanjunjie/Master_3/1-IUGG/CRDSITE/shp/gadm36_HKG_shp/gadm36_HKG_0','states',drawbounds=True)
# map.pcolormesh(x, y, data_diff, cmap='jet', zorder=0,vmin = 0,vmax = 3)
# # cp = plt.colorbar(shrink=0.94,format = "%.0f",ticks = [0,1,2,3],pad = 0.01)
# # cp.set_label('Iono Error (cm)',fontdict = font_label)
# # cp.set_ticklabels((0,1,2,3),fontsize = tick_size)
# plt.title("{:0>4}-{:0>2}-{:0>2} {:0>2}:{:0>2}:{:0>2} (GPST)".format(int(year),int(mon),int(day),int(hour),int(min),int(sec)),font_title)

# ## 335 ##
# plt.subplot(3,3,6)
# year,mon,day,hour,min,sec,Delta = 2021,11,1,20,25,0,300
# doy = tr.ymd2doy(year,mon,day,0,0,00)
# grid_diff_file = os.path.join("/Users/hanjunjie/Master_3/1-IUGG/ResFromServer/GRID_ForHeat","{}{:0>3}".format(year,doy),"GREAT-GEC-30.grid")
# sec = sec + Delta
# if sec >= 60:
#     min = min + sec/60
#     sec = 0
# if min >= 60:
#     hour = hour + min/60
#     min = 0
# grid_diff = rf.H_open_grid_file_for_heat(grid_diff_file,year,mon,day,hour,min,sec,0)
# data_diff = []
# for i in range(len(y)):
#     cur_diff_list = []
#     row = int(((-y[i] + 22.6) / 0.1))
#     for j in range(len(x)):
#         dis_diff = []
#         col = int(((x[j] - 113.85) / 0.1))
#         grid_index_1 = row * 6 + col
#         dB = 22.6 - row * 0.1 - y[i]
#         dL = 113.85 + col * 0.1 - x[j]
#         dis_diff.append(1/math.sqrt(math.pow(dB,2) + math.pow(dL,2)))
#         grid_index_2 = grid_index_1 + 1
#         dB = 22.6 - row * 0.1 - y[i]
#         dL = 113.85 + col * 0.1 - x[j] + 0.1
#         dis_diff.append(1/math.sqrt(math.pow(dB,2) + math.pow(dL,2)))
#         grid_index_3 = (row+1) * 6 + col
#         dB = 22.6 - row * 0.1 - y[i] - 0.1
#         dL = 113.85 + col * 0.1 - x[j]
#         dis_diff.append(1/math.sqrt(math.pow(dB,2) + math.pow(dL,2)))
#         grid_index_4 = grid_index_3 + 1    
#         dB = 22.6 - row * 0.1 - y[i] - 0.1
#         dL = 113.85 + col * 0.1 - x[j] + 0.1
#         dis_diff.append(1/math.sqrt(math.pow(dB,2) + math.pow(dL,2)))
#         diff = [grid_diff[grid_index_1],grid_diff[grid_index_2],grid_diff[grid_index_3],grid_diff[grid_index_4]]
#         p = np.array(dis_diff)/np.sum(np.array(dis_diff))
#         cur_diff = np.array(diff) * p
#         cur_diff_list.append(cur_diff.sum() * 100)
#     data_diff.append(cur_diff_list)
# data_diff = np.array(data_diff)
# map = Basemap(llcrnrlon=113.85, llcrnrlat=22.2, urcrnrlon=114.35, urcrnrlat=22.6, resolution='c',projection='cyl')
# map.drawparallels(circles=np.linspace(22.2, 22.6, 5),labels=[0, 0, 0, 0], color='gray',fontsize = tick_size,linewidth=0.5)
# map.drawmeridians(meridians=np.linspace(113.85, 114.35, 6),labels=[0, 0, 0, 0], color='gray',fontsize = tick_size,linewidth=0.5)
# # xlabellon = [113.95,114.15,114.35]
# # xlabeltext = []
# # for i in xlabellon:
# #     xlabeltext.append('%.1f$^\circ$E'%(i))
# # plt.xticks(xlabellon,xlabeltext,size = tick_size)
# map.readshapefile(r'/Users/hanjunjie/Master_3/1-IUGG/CRDSITE/shp/gadm36_CHN_shp/gadm36_CHN_0','states',drawbounds=True)
# map.readshapefile(r'/Users/hanjunjie/Master_3/1-IUGG/CRDSITE/shp/gadm36_HKG_shp/gadm36_HKG_0','states',drawbounds=True)
# map.pcolormesh(x, y, data_diff, cmap='jet', zorder=0,vmin = 0,vmax = 3)
# # cp = plt.colorbar(shrink=1,format = "%.0f",ticks = [0,1,2,3],pad = 0.1,orientation = "vertical")
# # cp.set_label('IONO errors (cm)',fontdict = font_label)
# # cp.set_ticklabels((0,1,2,3),fontsize = tick_size)
# plt.title("{:0>4}-{:0>2}-{:0>2} {:0>2}:{:0>2}:{:0>2} (GPST)".format(int(year),int(mon),int(day),int(hour),int(min),int(sec)),font_title)

# ## 335 ##
# plt.subplot(3,3,9)
# year,mon,day,hour,min,sec,Delta = 2021,11,2,20,25,0,300
# doy = tr.ymd2doy(year,mon,day,0,0,00)
# grid_diff_file = os.path.join("/Users/hanjunjie/Master_3/1-IUGG/ResFromServer/GRID_ForHeat","{}{:0>3}".format(year,doy),"GREAT-GEC-30.grid")
# sec = sec + Delta
# if sec >= 60:
#     min = min + sec/60
#     sec = 0
# if min >= 60:
#     hour = hour + min/60
#     min = 0
# grid_diff = rf.H_open_grid_file_for_heat(grid_diff_file,year,mon,day,hour,min,sec,0)
# data_diff = []
# for i in range(len(y)):
#     cur_diff_list = []
#     row = int(((-y[i] + 22.6) / 0.1))
#     for j in range(len(x)):
#         dis_diff = []
#         col = int(((x[j] - 113.85) / 0.1))
#         grid_index_1 = row * 6 + col
#         dB = 22.6 - row * 0.1 - y[i]
#         dL = 113.85 + col * 0.1 - x[j]
#         dis_diff.append(1/math.sqrt(math.pow(dB,2) + math.pow(dL,2)))
#         grid_index_2 = grid_index_1 + 1
#         dB = 22.6 - row * 0.1 - y[i]
#         dL = 113.85 + col * 0.1 - x[j] + 0.1
#         dis_diff.append(1/math.sqrt(math.pow(dB,2) + math.pow(dL,2)))
#         grid_index_3 = (row+1) * 6 + col
#         dB = 22.6 - row * 0.1 - y[i] - 0.1
#         dL = 113.85 + col * 0.1 - x[j]
#         dis_diff.append(1/math.sqrt(math.pow(dB,2) + math.pow(dL,2)))
#         grid_index_4 = grid_index_3 + 1    
#         dB = 22.6 - row * 0.1 - y[i] - 0.1
#         dL = 113.85 + col * 0.1 - x[j] + 0.1
#         dis_diff.append(1/math.sqrt(math.pow(dB,2) + math.pow(dL,2)))
#         diff = [grid_diff[grid_index_1],grid_diff[grid_index_2],grid_diff[grid_index_3],grid_diff[grid_index_4]]
#         p = np.array(dis_diff)/np.sum(np.array(dis_diff))
#         cur_diff = np.array(diff) * p
#         cur_diff_list.append(cur_diff.sum() * 100)
#     data_diff.append(cur_diff_list)
# data_diff = np.array(data_diff)
# map = Basemap(llcrnrlon=113.85, llcrnrlat=22.2, urcrnrlon=114.35, urcrnrlat=22.6, resolution='c',projection='cyl')
# map.drawparallels(circles=np.linspace(22.2, 22.6, 5),labels=[0, 0, 0, 0], color='gray',fontsize = tick_size,linewidth=0.5)
# map.drawmeridians(meridians=np.linspace(113.85, 114.35, 6),labels=[0, 0, 0, 0], color='gray',fontsize = tick_size,linewidth=0.5)
# xlabellon = [113.9,114.1,114.3]
# xlabeltext = []
# for i in xlabellon:
#     xlabeltext.append('%.1f$^\circ$E'%(i))
# plt.xticks(xlabellon,xlabeltext,size = tick_size)
# map.readshapefile(r'/Users/hanjunjie/Master_3/1-IUGG/CRDSITE/shp/gadm36_CHN_shp/gadm36_CHN_0','states',drawbounds=True)
# map.readshapefile(r'/Users/hanjunjie/Master_3/1-IUGG/CRDSITE/shp/gadm36_HKG_shp/gadm36_HKG_0','states',drawbounds=True)
# map.pcolormesh(x, y, data_diff, cmap='jet', zorder=0,vmin = 0,vmax = 3)
# # cp = plt.colorbar(shrink=0.94,format = "%.0f",ticks = [0,1,2,3],pad = 0.01)
# # cp.set_label('Iono Error (cm)',fontdict = font_label)
# # cp.set_ticklabels((0,1,2,3),fontsize = tick_size)
# plt.title("{:0>4}-{:0>2}-{:0>2} {:0>2}:{:0>2}:{:0>2} (GPST)".format(int(year),int(mon),int(day),int(hour),int(min),int(sec)),font_title)

# # im = ax.imshow()
# plt.subplot(3,3,8)
# cbax = plt.axes([0.11,0.07,0.8,0.015]) #left down width height
# cp = plt.colorbar(cax=cbax,shrink=2,format = "%.0f",ticks = [0,1,2,3],pad = 0.1,orientation = "horizontal")
# cp.set_label('IONO errors (cm)',fontdict = font_label)
# cp.set_ticklabels((0,1,2,3),fontsize = 25)
plt.tight_layout()
# # save_path = "E:\\1Master_2\\3-IUGG\\Result_Server\\Heat_Save\\{:0>4}{:0>3}_GEC\\{:0>2}{:0>2}{:0>2}.jpg".format(int(year),int(doy),int(hour),int(min),int(sec))
# plt.savefig("/Users/hanjunjie/Desktop/Image-1/HK_DIFF_POSITION.jpg",dpi=300)

plt.show()
# plt.clf()