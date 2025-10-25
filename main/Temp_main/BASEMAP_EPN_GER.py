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
# import readfile as rf
# from shapely.ops import triangulate
# from shapely import wkt
import math
import matplotlib as mpl
import numpy as np
from folium.plugins import HeatMap
import seaborn as sns
from mpl_toolkits.basemap import Basemap
from adjustText import adjust_text
from matplotlib.colors import Normalize
from matplotlib.colorbar import ColorbarBase
font_title = {'family' : 'Arial', 'weight' : 300, 'size' : 10}
font_label = {'family' : 'Arial', 'weight' : 300, 'size' : 15}
font_label_new = {'family' : 'Arial', 'size' : 15}
font_tick = {'family' : 'Arial', 'weight' : 300, 'size' : 35}
font_legend = {'family' : 'Arial', 'weight' : 300, 'size' : 30}
# font_legend = {'family' : 'Times New Roman', 'weight' : 600, 'size' : 15}
font_text = {'family' : 'Arial','weight' : 300,'size'   : 15}
tick_size = 15

def draw_grid(minLon,maxLat,maxLon,minLat,space,m):
    lat_split = 16
    lon_split = 16*1.8
    #----- Plot Grid -----#
    print("Top Left Corner : ({:>.4f},{:>.4f})".format(minLon,maxLat))
    print("Lower Right Corner : ({:>.4f},{:>.4f})".format(maxLon,minLat))
    maxLat = maxLat + space/3
    minLon = minLon - 0.07
    cur_Lat = maxLat
    cur_Lon = minLon

    while cur_Lon < maxLon:
        if abs(cur_Lon - maxLon) < 1e-8:
            break
        cur_Lon = cur_Lon + space 
        folium.PolyLine(locations=[[maxLat,cur_Lon],[minLat,cur_Lon]],color='black',weight = 3.5).add_to(m)    
    maxLon = cur_Lon
    while cur_Lat > minLat:
        if abs(cur_Lat - minLat) < 1e-8:
            break
        cur_Lat = cur_Lat - space
        folium.PolyLine(locations=[[cur_Lat,minLon],[cur_Lat,maxLon]],color='black',weight= 3.5).add_to(m)
    minLat = cur_Lat
    cur_Lon = minLon
    while cur_Lon < maxLon:
        cur_Lon = cur_Lon + space
        folium.PolyLine(locations=[[maxLat,cur_Lon],[minLat,cur_Lon]],color='black',weight= 3.5).add_to(m)
    #plot bound
    cur_Lat = maxLat + space
    cur_Lon = minLon - space
    i=0
    # folium.Rectangle
    #---
    deg = True
    count_lon = 1
    while cur_Lon < maxLon - space:
        cur_Lon = cur_Lon + space
        count_lon = count_lon+1
        if i==0:
            # c = 'black'
            c = 'white'
            i=1
        else:
            c = 'black'
            i=0
        # folium.PolyLine(locations=[[maxLat,cur_Lon],[maxLat,cur_Lon + space]],color=c,weight=10).add_to(m)
        folium.Polygon(locations=[[maxLat,cur_Lon],[maxLat,cur_Lon + space],[maxLat - space / lon_split,cur_Lon + space],[maxLat - space / lon_split,cur_Lon]]
                       ,color = 'black',fill = True,fill_color = c, fill_opacity=1,weight = 3).add_to(m)
    #---
    #   |
    #   |
    #   |
    count_lat = 1
    while cur_Lat > minLat + space:
        cur_Lat = cur_Lat - space
        count_lat = count_lat +1
        if i==0:
            c = 'white'
            # c = 'black'
            i=1
        else:
            c = 'black'
            i=0
        # folium.PolyLine(locations=[[cur_Lat,maxLon],[cur_Lat - space,maxLon]],color=c,weight=10).add_to(m)
        folium.Polygon(locations=[[cur_Lat,maxLon],[cur_Lat - space,maxLon],[cur_Lat - space,maxLon - space / lat_split],[cur_Lat,maxLon- space / lat_split]]
                       ,color = 'black',fill = True,fill_color = c, fill_opacity=1,weight = 3).add_to(m)
    #---
    #   |
    #   |
    #   |
    #---
    cur_Lon = cur_Lon + space
    cur_Lat = cur_Lat - space
    while cur_Lon >= minLon:
        # if (cur_Lon-space) < minLon:
        #     break
        if i==0:
            c = 'white'
            # c = 'black'
            i=1
        else:
            c = 'black'
            i=0
        # folium.PolyLine(locations=[[minLat,cur_Lon-space],[minLat,cur_Lon]],color=c,weight=10).add_to(m)
        folium.Polygon(locations=[[minLat,cur_Lon],[minLat,cur_Lon-space],[minLat - space / lon_split,cur_Lon - space],[minLat - space / lon_split,cur_Lon]]
                       ,color = 'black',fill = True,fill_color = c, fill_opacity=1,weight = 3).add_to(m)
        cur_Lon = cur_Lon - space
        folium.Marker(location=[minLat - space/5,cur_Lon+space-space/5],
                icon=DivIcon(
                icon_size=(150,36),
                icon_anchor=(7,20),
                html='<div style="font-size: 20pt; color : black">'+"{:.1f}\u00B0E".format(cur_Lon+space)+'</div>',
                )).add_to(m)
    folium.Marker(location=[minLat - space/5,cur_Lon-space/5],
                icon=DivIcon(
                icon_size=(150,36),
                icon_anchor=(7,20),
                html='<div style="font-size: 20pt; color : black">'+"{:.1f}\u00B0E".format(cur_Lon)+'</div>',
                )).add_to(m)
    folium.Polygon(locations=[[minLat,cur_Lon],[minLat,cur_Lon-space / lat_split],[minLat - space / lon_split,cur_Lon - space / lat_split],[minLat - space / lon_split,cur_Lon]]
                       ,color = 'black',fill = True,fill_color = c, fill_opacity=1,weight = 3).add_to(m)
    # ---
    #|   |
    #|   |
    #|   |
    # ---
    while cur_Lat < maxLat:
        if i==0:
            c = 'white'
            # c = 'black'
            i=1
        else:
            c = 'black'
            i=0
        if cur_Lat + space > maxLat:
            break
        # folium.PolyLine(locations=[[cur_Lat,minLon],[cur_Lat + space,minLon]],color=c,weight=10).add_to(m)
        folium.Polygon(locations=[[cur_Lat,minLon],[cur_Lat + space,minLon],[cur_Lat + space,minLon - space / lat_split],[cur_Lat,minLon- space / lat_split]]
                       ,color = 'black',fill = True,fill_color = c, fill_opacity=1,weight = 3).add_to(m)
        folium.Marker(location=[cur_Lat,minLon-space/1.7],
                icon=DivIcon(
                icon_size=(150,36),
                icon_anchor=(7,20),
                html='<div style="font-size: 20pt; color : black">'+"{:.1f}\u00B0N".format(cur_Lat)+'</div>',
                )).add_to(m)
        cur_Lat = cur_Lat + space
    folium.Marker(location=[cur_Lat,minLon-space/1.7],
            icon=DivIcon(
            icon_size=(150,36),
            icon_anchor=(7,20),
            html='<div style="font-size: 20pt; color : black">'+"{:.1f}\u00B0N".format(cur_Lat)+'</div>',
            )).add_to(m)

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
    
def rgb2hex(RGB):
    a = hex(int(int(RGB)/16))[-1]
    b = hex(int(int(RGB)%16))[-1]
    return (a+b)
fig = plt.figure(figsize=(6.5,4))
# ax = fig.add_subplot(121)
# box = ax.get_position()
# ax.set_position([box.x0, box.y0 + box.y0*0.9, box.width, box.height])
crd_file = "/Users/hanjunjie/Master_3/1-IUGG/CRDSITE/EPN_GER_21.crd"
space = 1.5 # Grid space deg
client_server = ["IJMU","DENT","WSRT","KOS1","BRUX","DOUR","WARE","REDU","EIJS","TIT2","EUSK","DILL","DIEP","BADH","KLOP","FFMJ","HOBU","PTBB","GOET"]
site_list1 = ["BRUX","DOUR","WARE","REDU","EIJS","BADH","FFMJ","KLOP"]
site_list2 = ["KOS1","DENT","WSRT","TIT2","DIEP","EUSK"]
site_list3 = ["KARL","TERS","IJMU","HOBU","DILL","PTBB","GOET"]
site_list = ["IJMU","DENT","DOUR","WARE","EIJS","TIT2","EUSK","DILL","DIEP","BADH","KLOP","TERS","KARL","HOBU","PTBB","GOET"]
#read crd file
crd_data,B,L = {},[],[]
with open(crd_file,'rt') as f:
    for line in f:
        value = line.split()
        if value[len(value)-1] == "False":
            continue
        # if value[0] not in site_list:
        #     continue
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

map = Basemap(llcrnrlon=3.2, llcrnrlat=48.9, urcrnrlon=10.7, urcrnrlat=53.4, resolution='c',projection='cyl')

##---Marker---##
texts=[]
lat_list,long_list = [],[]
for cur_site in crd_data:
    # if cur_site in site_list1:
    #     map.scatter(crd_data[cur_site]["BLH"][1],crd_data[cur_site]["BLH"][0],marker='v',s=100,facecolor='#0099E5',edgecolor='k', linewidth=0.3)
    # elif cur_site in site_list2:
    #     map.scatter(crd_data[cur_site]["BLH"][1],crd_data[cur_site]["BLH"][0],marker='v',s=100,facecolor='#FF4C4C',edgecolor='k', linewidth=0.3)
    # else:
    map.scatter(crd_data[cur_site]["BLH"][1],crd_data[cur_site]["BLH"][0],marker='v',s=100,facecolor='#34BF49',edgecolor='k', linewidth=0.3)
    lat_list.append(crd_data[cur_site]["BLH"][1])
    long_list.append(crd_data[cur_site]["BLH"][0])
    texts.append(plt.text(crd_data[cur_site]["BLH"][1],crd_data[cur_site]["BLH"][0],cur_site,fontdict=font_text))
adjust_text(texts)

map.drawparallels(circles=np.linspace(48.9, 53.4, 4),labels=[1, 0, 0, 0], color='gray',fontsize = tick_size,linewidth=0.5)
map.drawmeridians(meridians=np.linspace(3.2, 10.7, 6),labels=[0, 0, 0, 1], color='gray',fontsize = tick_size,linewidth=0.5)

map.readshapefile('/Users/hanjunjie/Master_3/1-IUGG/CRDSITE/shp/gadm36_DEU_shp/gadm36_DEU_0','states',drawbounds=True)
map.readshapefile('/Users/hanjunjie/Master_3/1-IUGG/CRDSITE/shp/gadm36_FRA_shp/gadm36_FRA_0','states',drawbounds=True)
map.readshapefile('/Users/hanjunjie/Master_3/1-IUGG/CRDSITE/shp/gadm36_NLD_shp/gadm36_NLD_0','states',drawbounds=True)
map.readshapefile('/Users/hanjunjie/Master_3/1-IUGG/CRDSITE/shp/gadm36_BEL_shp/gadm36_BEL_0','states',drawbounds=True)


plt.savefig("/Users/hanjunjie/Desktop/Image-1/EPN_SITE_STOCASTIC.jpg",dpi=300)
plt.show()
# plt.clf()
plt.close()

