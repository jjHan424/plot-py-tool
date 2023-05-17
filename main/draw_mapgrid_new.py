from math import ceil
import os
import sys
from turtle import width

from numpy import size
sys.path.insert(0,os.path.dirname(__file__)+'/..')
import folium
from folium.features import DivIcon
import webbrowser
import trans as tr
import glv
import readfile as rf
from shapely.ops import triangulate
from shapely import wkt
from shapely.geometry import MultiPoint
import shapely.geometry
import math
import matplotlib as mpl
import numpy as np

def draw_grid(minLon,maxLat,maxLon,minLat,space,m):
    lat_split = 12
    lon_split = 20
    #----- Plot Grid -----#
    print("Top Left Corner : ({:>.4f},{:>.4f})".format(minLon,maxLat))
    print("Lower Right Corner : ({:>.4f},{:>.4f})".format(maxLon,minLat))
    maxLat = maxLat + space/2
    minLon = minLon - space/2
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
    while cur_Lon > minLon:
        if (cur_Lon-space) < minLon:
            break
        if i==0:
            c = 'white'
            i=1
        else:
            c = 'black'
            i=0
        # folium.PolyLine(locations=[[minLat,cur_Lon-space],[minLat,cur_Lon]],color=c,weight=10).add_to(m)
        folium.Polygon(locations=[[minLat,cur_Lon],[minLat,cur_Lon-space],[minLat - space / lon_split,cur_Lon - space],[minLat - space / lon_split,cur_Lon]]
                       ,color = 'black',fill = True,fill_color = c, fill_opacity=1,weight = 3).add_to(m)
        cur_Lon = cur_Lon - space
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
            i=1
        else:
            c = 'black'
            i=0
        if cur_Lat + space > maxLat:
            break
        # folium.PolyLine(locations=[[cur_Lat,minLon],[cur_Lat + space,minLon]],color=c,weight=10).add_to(m)
        folium.Polygon(locations=[[cur_Lat,minLon],[cur_Lat + space,minLon],[cur_Lat + space,minLon - space / lat_split],[cur_Lat,minLon- space / lat_split]]
                       ,color = 'black',fill = True,fill_color = c, fill_opacity=1,weight = 3).add_to(m)
        cur_Lat = cur_Lat + space

crd_file = r"E:\1Master_2\2-UPD_Test\EPN_SITE\GER_AUG.crd"
space = 1.5 # Grid space deg
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
title='https://webrd02.is.autonavi.com/appmaptile?lang=en&size=1&scale=1&style=8&x={x}&y={y}&z={z}' #常规英文      
m = folium.Map(location=[mean_bl[0], mean_bl[1]], zoom_start=5, tiles=title, attr='default',control_scale = True)
# m = folium.Map(location=[mean_bl[0], mean_bl[1]], zoom_start=5, tiles="Stamen Toner", attr='default',control_scale = True)
#-----mark site-----#
cmap4 = ['red','cyan','blue','purple','yellow','lime','magenta','orange','green','black','red','cyan','blue','purple','yellow','lime','magenta','orange','green','black']
color_set = {}
# color_set["G"],color_set["GE"],color_set["GEC2"],color_set["GEC3C2"],color_set["GC3C2"] = 'purple','green','blue','red','yellow'
color_set["G"],color_set["GC2"],color_set["GEC2"],color_set["GEC3C2"],color_set["GC3C2"] = 'purple','green','blue','red','yellow'
minLat = 90
minLon = 180
maxLat = -90
maxLon = -180
for cur_site in crd_data:
    # Circle
    folium.CircleMarker(location=[crd_data[cur_site]["BLH"][0],crd_data[cur_site]["BLH"][1]],
                            radius=10,   # 圆的半径
                            popup=cur_site,
                            color='black',
                            fill=True,
                            fill_color=color_set[crd_data[cur_site]["SYS"]],
                            fill_opacity=1
                       ).add_to(m)
    # Name
    folium.Marker(location=[crd_data[cur_site]["BLH"][0],crd_data[cur_site]["BLH"][1]],
                icon=DivIcon(
                icon_size=(150,36),
                icon_anchor=(7,20),
                html='<div style="font-size: 18pt; color : black">'+"{:}".format(cur_site)+'</div>',
                )).add_to(m)
    # Find Max and Min
    if crd_data[cur_site]["BLH"][0] < minLat:
        minLat = crd_data[cur_site]["BLH"][0]
    if crd_data[cur_site]["BLH"][1] < minLon:
        minLon = crd_data[cur_site]["BLH"][1]
    if crd_data[cur_site]["BLH"][0] > maxLat:
        maxLat = crd_data[cur_site]["BLH"][0]
    if crd_data[cur_site]["BLH"][1] > maxLon:
        maxLon = crd_data[cur_site]["BLH"][1]
draw_grid(minLon,maxLat,maxLon,minLat,space,m)
# m.add_child(folium.ClickForMarker(popup="marker"))
m.save(r"E:\1Master_2\2-UPD_Test\EPN_SITE\GER_AUG.html")