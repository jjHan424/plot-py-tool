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
    lat_split = 16*1.3
    lon_split = 16*1.4
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
    while cur_Lon > minLon:
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
    # folium.Marker(location=[minLat - space/5,cur_Lon-space/5],
    #             icon=DivIcon(
    #             icon_size=(150,36),
    #             icon_anchor=(7,20),
    #             html='<div style="font-size: 20pt; color : black">'+"{:.1f}\u00B0E".format(cur_Lon)+'</div>',
    #             )).add_to(m)
    # folium.Polygon(locations=[[minLat,cur_Lon],[minLat,cur_Lon-space / lat_split],[minLat - space / lon_split,cur_Lon - space / lat_split],[minLat - space / lon_split,cur_Lon]]
    #                    ,color = 'black',fill = True,fill_color = c, fill_opacity=1,weight = 3).add_to(m)
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
            if server_site == cur_site:
                continue
            cur_server = crd_data[server_site]["XYZ"]
            delta_xyz = np.array(crd_data[client_site]["XYZ"]) - np.array(crd_data[server_site]["XYZ"])
            dis = math.sqrt(np.sum(delta_xyz*delta_xyz)) / 1000
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
    mean_length = 6
    dis_site = {}
    for cur_site in all_site_dis.keys():
        cur_dis = all_site_dis[cur_site]
        cur_dis.sort()
        if mean_length > len(cur_dis):
            mean_length = len(cur_dis)
        # print("{}: {:.2f} km".format(cur_site,np.mean(np.array(cur_dis[0:mean_length-1]))))
        dis_site[np.mean(np.array(cur_dis[0:mean_length-1]))] = cur_site
    dis_sort = sorted(dis_site)
    for cur_dis in dis_sort:
        print("{}: {:.2f} km".format(dis_site[cur_dis],cur_dis))
    print("{}: {:.2f} km".format("MEAN",np.mean(dis_sort)))
    

crd_file = r"E:\0Project\ZHD_Data\ZHD_html.crd"
# crd_file = r"E:\1Master_2\3-IUGG\crd\AUG_HK_xml.crd"
space = 0.5 # Grid space deg
# client_server = ["TERS","KARL","IJMU","DENT","WSRT","KOS1","BRUX","DOUR","WARE","REDU","EIJS","TIT2","EUSK","DILL","DIEP","BADH","KLOP","FFMJ","HOBU","PTBB","GOET"]
site_list1 = ["BRUX","DOUR","WARE","REDU","EIJS","BADH","FFMJ","KLOP"]
site_list2 = ["KOS1","DENT","WSRT","TIT2","DIEP","EUSK"]
site_list3 = ["KARL","TERS","IJMU","HOBU","DILL","PTBB","GOET"]

# site_list1 = ["KOS1","BRUX","DOUR","WARE","REDU","EIJS","BADH"]
# site_list2 = ["DENT","WSRT","TIT2","DILL","DIEP","KLOP","FFMJ","PTBB"]
# site_list3 = ["KARL","TERS","IJMU","EUSK","HOBU","GOET"]

site_list3 = ["HKTK","T430","HKLT","HKKT","HKSS","HKWS","HKSL","HKST","HKKS","HKCL","HKSC","HKPC","HKNP","HKMW","HKLM","HKOH"]

client_server = {"ES32":["ES32","ES33","ES34","ES35","ES36","ES37","ES38","ES41","ES42","ES43"],
                 "ES33":["ES32","ES33","ES34","ES35","ES36","ES37","ES38","ES41","ES42","ES43"],
                 "ES34":["ES32","ES33","ES34","ES35","ES36","ES37","ES38","ES41","ES42","ES43"],
                 "ES35":["ES32","ES33","ES34","ES35","ES36","ES37","ES38","ES41","ES42","ES43"],
                 "ES36":["ES32","ES33","ES34","ES35","ES36","ES37","ES38","ES41","ES42","ES43"],
                 "ES37":["ES32","ES33","ES34","ES35","ES36","ES37","ES38","ES41","ES42","ES43"],
                 "ES38":["ES32","ES33","ES34","ES35","ES36","ES37","ES38","ES41","ES42","ES43"],
                 "ES41":["ES32","ES33","ES34","ES35","ES36","ES37","ES38","ES41","ES42","ES43"],
                 "ES42":["ES32","ES33","ES34","ES35","ES36","ES37","ES38","ES41","ES42","ES43"],
                 "ES43":["ES32","ES33","ES34","ES35","ES36","ES37","ES38","ES41","ES42","ES43"]}
# client_server = {"ES43":["ES42","ES38","ES35"],
#                  "ES38":["ES43","ES33","ES39"]}
# client_server = {"JFNG":["WHDX"],
#                  }

# client_server = {"DIEP1":["WSRT","HOBU","GOET"],
#                  "DIEP2":["WSRT","HOBU","PTBB"],
#                  "DELF":["IJMU","KOS1","VLIS"],
#                  "EIJS":["TIT2","EUSK","WARE"],
#                  "WARE":["EIJS","BRUX","DOUR"],
#                  "WSRT":["TERS","KOS1","DIEP"],
#                  "BRUX":["DENT","WARE","DOUR"]}
# client_server = {"DIEP1":["WSRT","HOBU","GOET"],
#                  "DELF":["IJMU","KOS1","VLIS"],
#                  "EIJS":["TIT2","EUSK","WARE"],
#                  "WSRT":["TERS","KOS1","DIEP"],
#                  "BRUX":["DENT","WARE","DOUR"]}
# client_server = {"TIT2":["REDU"]}
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
        # print("{}: {:.5f} {:.5f} {:.5f}".format(value[0],blh[0] / glv.deg,blh[1] / glv.deg,blh[2]))
        blh = [blh[0] / glv.deg,blh[1] / glv.deg,blh[2]]
        if blh[1] > 180:
            blh = [blh[0],blh[1] - 360,blh[2]]
        crd_data[value[0]]["BLH"] = blh
        B.append(blh[0])
        L.append(blh[1])
        print("{:.2f},{:.2f}".format(blh[0],blh[1]))
        crd_data[value[0]]["SYS"] = ""
        for i in range(len(value)-1):
            if i >= 4:
                crd_data[value[0]]["SYS"] = crd_data[value[0]]["SYS"] + value[i]
        crd_data[value[0]]["VALUE"] = value[len(value)-1]
mean_bl = [np.mean(B),np.mean(L)] 
title='https://webrd02.is.autonavi.com/appmaptile?lang=en&size=1&scale=1&style=8&x={x}&y={y}&z={z}' #常规英文      
# title = 'http://map.geoq.cn/ArcGIS/rest/services/ChinaOnlineStreetGray/MapServer/tile/{z}/{y}/{x}'
# title = 'Stamen Watercolor'
# title = 'Stamen Toner'
m = folium.Map(location=[mean_bl[0], mean_bl[1]], zoom_start=5, tiles=title, attr='default',control_scale = True)
# m = folium.Map(location=[mean_bl[0], mean_bl[1]], zoom_start=5, attr='default',control_scale = True)
# cal_dis_interpolation(client_server,crd_data)
# cal_dis_Grid(site_list3,crd_data)
#-----mark site-----#
cmap4 = ['red','cyan','blue','purple','yellow','lime','magenta','orange','green','black','red','cyan','blue','purple','yellow','lime','magenta','orange','green','black']
color_set = {}
color_set["G"],color_set["GE"],color_set["GEC3"],color_set["GEC2C3"],color_set["GC2C3"] = 'purple','green','blue','blue','yellow'
# color_set["G"],color_set["GC2"],color_set["GEC3"],color_set["GEC3C2"],color_set["GC3C2"] = 'purple','green','blue','red','yellow'
minLat = 90
minLon = 180
maxLat = -90
maxLon = -180
for cur_site in crd_data:
    # Circle
    if cur_site == "ES44" or cur_site == "ES31":
        folium.CircleMarker(location=[crd_data[cur_site]["BLH"][0],crd_data[cur_site]["BLH"][1]],
                                radius=10,   # 圆的半径
                                popup=cur_site,
                                color='red',
                                fill=True,
                                fill_color=color_set[crd_data[cur_site]["SYS"]],
                                fill_opacity=1
                        ).add_to(m)
    else:
        folium.CircleMarker(location=[crd_data[cur_site]["BLH"][0],crd_data[cur_site]["BLH"][1]],
                            radius=10,   # 圆的半径
                            popup=cur_site,
                            color='blue',
                            fill=True,
                            fill_color=color_set[crd_data[cur_site]["SYS"]],
                            fill_opacity=1
                    ).add_to(m)
    # Name
    folium.Marker(location=[crd_data[cur_site]["BLH"][0]+space/10,crd_data[cur_site]["BLH"][1]],
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
m.save(r"E:\0Project\ZHD_Data\temp.html")



# out_xml_path = r"E:\1Master_2\3-IUGG\crd\AUG_GER_21.xml"
# for cur_site in crd_data.keys():
#     # G,E,C2,C3 = False,False,False,False
#     with open(out_xml_path,'a') as file:
#         str_write = "<rec X=\"{:.4f}\" Y=\"{:.4f}\" Z=\"{:.4f}\" id = \"{}\" />\n".format(crd_data[cur_site]["XYZ"][0],crd_data[cur_site]["XYZ"][1],crd_data[cur_site]["XYZ"][2],cur_site)
#         file.write(str_write)
# for cur_site in crd_data.keys():
#     G,E,C2,C3 = False,False,False,False
#     with open(out_xml_path,'a') as file:
#         str_write = "<STA ID=\"{}\" sigCLK=\"9000\" sigPOS=\"0.1_0.1_0.1\" sigSION=\"9000\" sigTropPd=\"0.015\" sigZTD=\"0.201\" />\n".format(cur_site)
#         file.write(str_write)