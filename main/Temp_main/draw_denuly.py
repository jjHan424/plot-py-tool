from audioop import mul
import imp
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

center_bl = [22.320048,114.1733] #HK
grid_space = [0.1,0.1]
# title='Stamen Terrain'
# title='https://wprd01.is.autonavi.com/appmaptile?x={x}&y={y}&z={z}&lang=zh_cn&size=1&scl=1&style=8&ltype=11' #街道图
title='http://webrd02.is.autonavi.com/appmaptile?lang=zh_cn&size=1&scale=1&style=7&x={x}&y={y}&z={z}'#高德
# title='https://webrd02.is.autonavi.com/appmaptile?lang=en&size=1&scale=1&style=8&x={x}&y={y}&z={z}' #常规英文
# title='https://webst02.is.autonavi.com/appmaptile?style=6&x={x}&y={y}&z={z}' #卫星
m = folium.Map(location=[center_bl[0], center_bl[1]], zoom_start=11.2, tiles=title, attr='高德-卫星影像图')
points = []
mark_point_blh = {}
mark_point_xyz = rf.open_crd_gridmap(r"E:\1Master_2\Paper_Grid\crd\2021\AUG_WH.crd")
minLat = 90
minLon = 180
maxLat = -90
maxLon = -180
for site in mark_point_xyz.keys():
    xyz = mark_point_xyz[site]
    blh = tr.xyz2blh(xyz[0],xyz[1],xyz[2])
    blh = [blh[0] / glv.deg,blh[1] / glv.deg,blh[2]]
    if blh[0] < minLat:
        minLat = blh[0]
    if blh[1] < minLon:
        minLon = blh[1]
    if blh[0] > maxLat:
        maxLat = blh[0]
    if blh[1] > maxLon:
        maxLon = blh[1]
    mark_point_blh[site]=[blh[0],blh[1],blh[2]]
    if site != "HKMW":
        points.append(shapely.geometry.Point(blh[0],blh[1]))
    folium.Marker(location=[blh[0],blh[1]],popup=folium.Popup(site,show=True),icon=folium.Icon(color='blue', icon="info-sign"),tooltip="click").add_to(m)
multipoint = MultiPoint(points)
# print(multipoint)
triangles = triangulate(multipoint,tolerance=0.001,edges=False)
# fnew = open(r"E:\1Master_2\Paper_Grid\crd\AUG_HK.txtt","w")
triangle = {}
for index,t in enumerate(triangles):
    # fnew.write(str(index) + '\t' + str(t.wkt) +"\n")
    ell_list = []
    value = t.wkt.split(",")
    value[3] = value[3][:len(value[3])-2] + "  " + value[3][len(value[3])-2:len(value[3])]
    for i in range(len(value)):
        if i == 0:
            continue
        ell_list.append(float(value[i].split(" ")[1]))
        ell_list.append(float(value[i].split(" ")[2]))
    triangle[index] = ell_list


for index in triangle.keys():
    blh1 = [triangle[index][0],triangle[index][1]]
    blh2 = [triangle[index][2],triangle[index][3]]
    blh3 = [triangle[index][4],triangle[index][5]]
    c="blue"
    folium.PolyLine(locations=[[blh1[0],blh1[1]],[blh2[0],blh2[1]]],color=c,weight=1).add_to(m)
    folium.PolyLine(locations=[[blh3[0],blh3[1]],[blh2[0],blh2[1]]],color=c,weight=1).add_to(m)
    folium.PolyLine(locations=[[blh3[0],blh3[1]],[blh1[0],blh1[1]]],color=c,weight=1).add_to(m)

m.save(r'E:\1Master_2\Paper_Grid\crd\AUG_HK2.html')
webbrowser.open(r'E:\1Master_2\Paper_Grid\crd\AUG_HK2.html')
