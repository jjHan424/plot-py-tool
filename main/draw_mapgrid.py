'''
Author: your name
Date: 2022-03-07 10:03:20
LastEditTime: 2022-08-25 21:09:04
LastEditors: HanJunjie HanJunjie@whu.edu.cn
Description: 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
FilePath: /plot-py-tool/main/draw_mapgrid.py
'''
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
import imgkit

def get_angel(blh1,blh2):
    blh = [blh2[0] - blh1[0],blh2[1] - blh1[1]]
    deg_tan = math.atan2(blh[0],blh[1]) / glv.deg
    if deg_tan < 0:
        deg_tan = deg_tan + 360
    return deg_tan
def isintriangle(grid_blh,site_3):
    p_1,p_2,p_3=site_3[0],site_3[1],site_3[2]
    S_site_3 = 0.5 * abs(p_1[0]*p_3[1]+p_2[0]*p_1[1]+p_3[0]*p_2[1]-p_1[0]*p_2[1]-p_2[0]*p_3[1]-p_3[0]*p_1[1])
    p_1,p_2,p_3=grid_blh,site_3[1],site_3[2]
    S_1 = 0.5 * abs(p_1[0]*p_3[1]+p_2[0]*p_1[1]+p_3[0]*p_2[1]-p_1[0]*p_2[1]-p_2[0]*p_3[1]-p_3[0]*p_1[1])
    p_1,p_2,p_3=site_3[0],grid_blh,site_3[2]
    S_2 = 0.5 * abs(p_1[0]*p_3[1]+p_2[0]*p_1[1]+p_3[0]*p_2[1]-p_1[0]*p_2[1]-p_2[0]*p_3[1]-p_3[0]*p_1[1])
    p_1,p_2,p_3=site_3[0],site_3[1],grid_blh
    S_3 = 0.5 * abs(p_1[0]*p_3[1]+p_2[0]*p_1[1]+p_3[0]*p_2[1]-p_1[0]*p_2[1]-p_2[0]*p_3[1]-p_3[0]*p_1[1])
    if abs(S_1 + S_2 +S_3 - S_site_3) < 1e-8:
        return 1
    else:
        return 0

def evenlyangle(grid_blh,site_3):
    x,y = site_3[0],site_3[1]
    p_a,p_b = [0,1],[0,1]
    p_a[0] = x[0] - grid_blh[0]
    p_a[1] = x[1] - grid_blh[1]
    p_b[0] = y[0] - grid_blh[0]
    p_b[1] = y[1] - grid_blh[1]
    angle1 = math.acos((p_a[0]*p_b[0]+p_a[1]*p_b[1])/(math.sqrt(p_a[0]*p_a[0] + p_a[1]*p_a[1])*math.sqrt(p_b[0]*p_b[0] + p_b[1]*p_b[1])))
    if angle1 > math.pi:
        angle1 = 2*math.pi-angle1
    x,y = site_3[0],site_3[2]
    p_a[0] = x[0] - grid_blh[0]
    p_a[1] = x[1] - grid_blh[1]
    p_b[0] = y[0] - grid_blh[0]
    p_b[1] = y[1] - grid_blh[1]
    angle2 = math.acos((p_a[0]*p_b[0]+p_a[1]*p_b[1])/(math.sqrt(p_a[0]*p_a[0] + p_a[1]*p_a[1])*math.sqrt(p_b[0]*p_b[0] + p_b[1]*p_b[1])))
    if angle2 >  math.pi:
        angle2 = 2*math.pi-angle2
    x,y = site_3[2],site_3[1]
    p_a[0] = x[0] - grid_blh[0]
    p_a[1] = x[1] - grid_blh[1]
    p_b[0] = y[0] - grid_blh[0]
    p_b[1] = y[1] - grid_blh[1]
    angle3 = math.acos((p_a[0]*p_b[0]+p_a[1]*p_b[1])/(math.sqrt(p_a[0]*p_a[0] + p_a[1]*p_a[1])*math.sqrt(p_b[0]*p_b[0] + p_b[1]*p_b[1])))
    if angle3 >  math.pi:
        angle3 = 2*math.pi-angle3
    angle_list = [angle1,angle2,angle3]
    if (abs(angle1 + angle2 + angle3 - 2*math.pi) < 1e-8):
        for i in range(len(angle_list)):
            angle_list[i] = abs(120/180*math.pi-angle_list[i])
        return np.mean(angle_list)
    else:
        max_angle = np.max(angle_list)
        return abs(math.pi-max_angle) + 120/180*math.pi

# all_truexyz = {
#          'WHXZ':[-2299689.3404, 4975638.9432, 3250284.4043], 'N062':[-2193162.1236, 4996265.6098, 3291753.9553],
#          'XGXN':[-2220831.1149, 5007544.3002, 3256075.5112], 'N010':[-2281398.4103, 5046329.8462, 3153471.3945],
#          'WUH2':[-2267750.2235, 5009154.6154, 3221294.4463], 'EZEC':[-2309234.0914, 4998958.4771, 3207719.1538],
#          'WHHN':[-2231642.4830, 5043039.9490, 3193690.4178], 'WHHP':[-2252813.6974, 4973121.8328, 3286531.2550],
#          'WHJA':[-2261952.7388, 5002588.1770, 3235442.2840], 'WHJX':[-2277732.7767, 5031747.7124, 3179072.7467],
#          'N032':[-2141843.9874, 5071953.5632, 3209315.6167], 'E033':[-2340806.3005, 4922578.8973, 3302011.7872],
#          'N004':[-2334707.5142, 5037347.5891, 3128918.7477], 'N028':[-2191056.9238, 5053129.9326, 3205815.9701],
#          'N047':[-2350716.9401, 4955782.5397, 3244265.6251], 'N068':[-2222210.0722, 4963941.9412, 3320986.9551],
#          'HKOH':[-2423817.5949, 5386056.8004, 2399883.0702], 'HKSL':[-2393383.0549, 5393860.7885, 2412592.0789],
#          'HKST':[-2417143.5093, 5382345.0913, 2415036.6168], 'HKTK':[-2418093.0437, 5374658.0011, 2430428.8781]
#          }

# all_trueblh = {}

# sites = all_truexyz.keys()

# m = folium.Map(location=[30, 114], zoom_start=8, tiles='Stamen Terrain')

# tooltip = "click"

# for k in sites:
#     if k == 'WUH2':
#         continue
#     xyz = all_truexyz[k]
#     blh = tr.xyz2blh(xyz[0],xyz[1],xyz[2])
#     print(blh[0] / glv.deg)
#     print(blh[1] / glv.deg)
#     print(blh[2])
#     all_trueblh[k] = [blh[0] / glv.deg, blh[1] / glv.deg]
#     folium.Marker(
#         [blh[0] / glv.deg, blh[1] / glv.deg], popup=folium.Popup("<b> " + k + " </b>", show=True), tooltip=tooltip,
#         icon=folium.Icon(color='red')
#     ).add_to(m)

# folium.PolyLine(smooth_factor=10,locations=[[22.3952,114.1842],[22.5465,114.2232]],dash_array='20',color="red",tooltip="灰色线条",weight=5).add_to(m)

# m.save('/Users/hjj/Desktop/example.html')
# webbrowser.open('example.html')

nbin=16
# cmap4 = ['red', 'blue', 'green', 'purple', 'orange', 'darkred', 'lightred', 'beige', 'darkblue', 'darkgreen', 'cadetblue', 'darkpurple', 'white', 'pink', 'lightblue', 'lightgreen', 'gray', 'black', 'lightgray']
cmap4 = ['red','cyan','blue','purple','yellow','lime','magenta','orange','green','black','red','cyan','blue','purple','yellow','lime','magenta','orange','green','black']
center_bl = [22.320048,114.1733] #HK
grid_space = [0.1,0.1]
# grid_count = [10,10]

# mark_point_xyz = {
#          'WHXZ':[-2299689.3404, 4975638.9432, 3250284.4043], 'N062':[-2193162.1236, 4996265.6098, 3291753.9553],
#          'XGXN':[-2220831.1149, 5007544.3002, 3256075.5112], 'N010':[-2281398.4103, 5046329.8462, 3153471.3945],
#          'WUH2':[-2267750.2235, 5009154.6154, 3221294.4463], 'EZEC':[-2309234.0914, 4998958.4771, 3207719.1538],
#          'WHHN':[-2231642.4830, 5043039.9490, 3193690.4178], 'WHHP':[-2252813.6974, 4973121.8328, 3286531.2550],
#          'WHJA':[-2261952.7388, 5002588.1770, 3235442.2840], 'WHJX':[-2277732.7767, 5031747.7124, 3179072.7467],
#          'N032':[-2141843.9874, 5071953.5632, 3209315.6167], 'E033':[-2340806.3005, 4922578.8973, 3302011.7872],
#          'N004':[-2334707.5142, 5037347.5891, 3128918.7477], 'N028':[-2191056.9238, 5053129.9326, 3205815.9701],
#          'N047':[-2350716.9401, 4955782.5397, 3244265.6251], 'N068':[-2222210.0722, 4963941.9412, 3320986.9551]   
#          }

mark_point_xyz = {'HKCL':[-2392740.9396,5397563.0493,2404757.8653],
              'HKFN':[-2411012.8949,5380268.2632,2425129.0941],
              'HKKS':[-2429525.8966,5377816.6360,2412152.7354],
              'HKKT':[-2405143.8990,5385195.2549,2420032.5440],
              'HKLM':[-2414045.9447,5391602.3519,2396878.8893],
              'HKLT':[-2399062.7358,5389237.8430,2417327.0568],
              'HKMW':[-2402484.1093,5395262.4383,2400726.9555],
              'HKNP':[-2392360.2537,5400226.2534,2400094.4576],
              'HKOH':[-2423816.8997,5386057.0931,2399883.3709],
              'HKPC':[-2405183.0015,5392541.8294,2403645.7303],
              #'HKQT':[-2421567.8916,5384910.5631,2404264.3943],
              'HKSC':[-2414266.9197,5386768.9868,2407460.0314],
              'HKSL':[-2393382.4157,5393861.1745,2412592.4105],
              'HKSS':[-2424425.1013,5377188.1768,2418617.7454],
              'HKST':[-2417142.8718,5382345.4730,2415036.9459],
              'HKTK':[-2418092.3728,5374658.3417,2430429.1904],
              'HKWS':[-2430579.0108,5374285.6738,2418956.3331],
              'KYC1':[-2408855.2574,5391043.2386,2403591.1306],
              'T430':[-2411015.2264,5380265.7133,2425132.7008]
                }



#sixtens

# mark_point_xyz = {'A003':[-2392740.9396,5397563.0493,2404757.8653],
#               'A007':[-2411012.8949,5380268.2632,2425129.0941],
#               'A008':[-2429525.8966,5377816.6360,2412152.7354],
#               'A010':[-2405143.8990,5385195.2549,2420032.5440],
#               'A013':[-2414045.9447,5391602.3519,2396878.8893],
#               'A014':[-2399062.7358,5389237.8430,2417327.0568],
#               'A017':[-2402484.1093,5395262.4383,2400726.9555],
#               'A018':[-2392360.2537,5400226.2534,2400094.4576],
#               'A019':[-2423816.8997,5386057.0931,2399883.3709],
#               'A022':[-2405183.0015,5392541.8294,2403645.7303],
#               'HKQT':[-2421567.8916,5384910.5631,2404264.3943],
#               'HKSC':[-2414266.9197,5386768.9868,2407460.0314],
#               'HKSL':[-2393382.4157,5393861.1745,2412592.4105],
#               'HKSS':[-2424425.1013,5377188.1768,2418617.7454],
#               'HKST':[-2417142.8718,5382345.4730,2415036.9459],
#               'HKTK':[-2418092.3728,5374658.3417,2430429.1904],
#               'HKWS':[-2430579.0108,5374285.6738,2418956.3331],
#               #'KYC1':[-2408855.2574,5391043.2386,2403591.1306],
#               'T430':[-2411015.2264,5380265.7133,2425132.7008]
#                 }

# mark_point_xyz = rf.open_crd_gridmap(r"E:\1Master_2\Paper_Grid\crd\AUG_HK_xml.crd")
# space_set = 0.1
# savedir = r'E:\1Master_2\Paper_Grid\crd'
site_list = ["HKTK","T430","HKLT","HKKT","HKSS","HKWS","HKSL","HKST","HKKS","HKCL","HKSC","HKPC","HKNP","HKMW","HKLM","HKOH"]
# # site_list = ["AUG-HK2"]
# site_user = "HKSC"
mark_point_xyz = rf.open_crd_gridmap(r"E:\1Master_2\3-IUGG\crd\AUG_HK_xml.crd")
space_set = 0.1
site_user = "HKSC"
# mark_point_xyz = rf.open_crd_gridmap(r"E:\1Master_2\Paper_Grid\crd\2021\AUG_WH.crd")
# space_set = 0.5
# savedir = r'E:\1Master_2\Paper_Grid\crd'
# site_list = ["WHYJ","WHXZ","WHDS","WHSP","N028","N047","N068","XGXN","WUDA"]
# site_user = "WUDA"
# mark_point_xyz = rf.open_crd_gridmap(r"E:\1Master_2\Paper_Grid\crd\2021\AUG_WH.crd")
# site_user = "WUDA"
# space_set = 0.3
# savedir = r'E:\1Master_2\Paper_Grid\crd'
# site_list = ["H035","H038","H053","H055","H068","H074","H139"]

#----LX---#
# mark_point_xyz = rf.open_crd_gridmap(r"E:\0Project\LX\data\AUG.crd")
# space_set = 0.5
# savedir = r'E:\1Master_2\Paper_Grid\crd'
# site_list = ["R293","EZEC","WHHN","WHHP"]

# mark_point_xyz = rf.open_crd_gridmap(r"E:\1Master_2\Paper_Grid\1-Paper_word\Image-3\AUG_HB.crd")
# space_set = 0.8
# savedir = r'E:\1Master_2\Paper_Grid\crd'
# site_list = ["K042","K057","K059","K101","A010","V092","K070"]
# site_list = ["HB01","HB02","HB03","HB04","HB05","HB06","HB07"]
# site_user = "HB04"
# site_list = ["Aug-WH2"]
# Lines_xyz1 = rf.open_flt_pvtflt_file(r"E:\1Master_2\Paper_Grid\Res_FromServer_New\Client_Dynamic-2\client-Grid_Ele-310-01\SEPT-GEC.flt")
# Lines_xyz1 = rf.open_pos_ref_IE(r"E:\1Master_2\Paper_Grid\Dynamic\2021310_WH\Ref.txt")
# Lines_xyz1 = rf.open_gpgga_file("/Volumes/H_GREAT/2Project/Allystar/2022_0726_Dynamic/novatel.txt",year=2022,mon=7,day=26)

#Lines_xyz2 = rf.open_flt_pvtflt_file("/Users/hjj/Documents/HJJ/Master_1/IonoGrid/Dynamic/20211205/Result/client-comp/SEPT-GEC.flt")
#Lines_xyz2 = rf.open_flt_pvtflt_file("/Users/hjj/Documents/HJJ/Master_1/IonoGrid/Dynamic/20211205/Result/client-comp/SEPT-GEC.flt")
# mark_point_xyz = {'2006':[-2430340.3590,5359921.7657,2450575.0220],
#               '2010':[-2419056.7812,5364365.3435,2452055.3961],
#               '2017':[-2424178.5320,5365092.3806,2445506.8814],
#               '2014':[-2384904.1935,5383810.3345,2442958.7433],
#               "2008":[-2400517.6908,5373926.9125,2449368.0968],
#               "2022":[-2401355.6901,5379177.7051,2437245.3320]
#                 }
# title='Stamen Terrain'
# title='https://wprd01.is.autonavi.com/appmaptile?x={x}&y={y}&z={z}&lang=zh_cn&size=1&scl=1&style=8&ltype=11' #街道图
# title='http://webrd02.is.autonavi.com/appmaptile?lang=en&size=1&scale=1&style=7&x={x}&y={y}&z={z}'#高德
title='https://webrd02.is.autonavi.com/appmaptile?lang=en&size=1&scale=1&style=8&x={x}&y={y}&z={z}' #常规英文
# title='https://webst02.is.autonavi.com/appmaptile?style=6&x={x}&y={y}&z={z}' #卫星
# title='https://mt.google.com/vt/lyrs=h&x={x}&y={y}&z={z}' # google 地图
# title='https://mt.google.com/vt/lyrs=s&x={x}&y={y}&z={z}' # google 卫星图
# title = "Stamen Terrain"
# title = "QuadTree"
# m = folium.Map(location=[center_bl[0], center_bl[1]], zoom_start=11.2, tiles=title, attr='default',control_scale = True)
m = folium.Map(location=[center_bl[0], center_bl[1]], zoom_start=11.2, tiles="Stamen Terrain", attr='default',control_scale = True)
# m = folium.Map(location = [center_bl[0], center_bl[1]],zoom_start = 15,control_scale = True)
mark_point_blh={}
points = []
Lines_blh1={}
Lines_blh2={}
minLat = 90
minLon = 180
maxLat = -90
maxLon = -180
#plot Marker
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
    points.append(shapely.geometry.Point(blh[0],blh[1]))
    if site == "HB04":
    # if site == "HKSC":
    # if site == "WUDA":
    # if site == "WHXZ":
        folium.CircleMarker(location=[blh[0],blh[1]],
                            radius=20,   # 圆的半径
                            popup='基站位置',
                            color='red',
                            fill=True,
                            fill_color='red',
                            fill_opacity=1
        ).add_to(m)
    elif site == "HB05" or site == "HB06" or site == "HB02":
    # elif site == "HKST" or site == "HKPC" or site == "HKOH":
    # elif site == "XGXN" or site == "WHXZ" or site == "WHSP":
    # elif site == "WHYJ" or site == "WUDA" or site == "N047":
        folium.CircleMarker(location=[blh[0],blh[1]],
                            radius=20,   # 圆的半径
                            popup='基站位置',
                            color='green',
                            fill=True,
                            fill_color='green',
                            fill_opacity=1
        ).add_to(m)
    else:
        folium.CircleMarker(location=[blh[0],blh[1]],
                            radius=10,   # 圆的半径
                            popup='基站位置',
                            color='blue',
                            fill=True,
                            fill_color='blue',
                            fill_opacity=1
        ).add_to(m)
    folium.Marker(location=[blh[0],blh[1]],popup=folium.Popup(site,show=False),icon=folium.Icon(color='blue', icon="info-sign"),tooltip="click").add_to(m)
    folium.Marker(location=[blh[0],blh[1]], icon=DivIcon(
                icon_size=(150,36),
                icon_anchor=(7,20),
                html='<div style="font-size: 30pt; color : black">'+"{:}".format(site)+'</div>',
                )).add_to(m)

    # if site=="DGXG" or site == "HZHY":
    #     # folium.Marker(location=[blh[0],blh[1]],popup=folium.Popup(site,show=True),icon=folium.Icon(color='green'),tooltip="click").add_to(m)
    #     k=1
    # else:
    #     if site[1:2] == "0" or site[1:2] == "1":
    #         folium.Marker(location=[blh[0],blh[1]],popup=folium.Popup(site,show=True),icon=folium.Icon(color='blue'),tooltip="click").add_to(m)
    #     else:
    #         folium.Marker(location=[blh[0],blh[1]],popup=folium.Popup(site,show=True),icon=folium.Icon(color='red'),tooltip="click").add_to(m)




# for time in Lines_xyz1:
#     blh = tr.xyz2blh(Lines_xyz1[time]["X"],Lines_xyz1[time]["Y"],Lines_xyz1[time]["Z"])
#     blh = [blh[0] / glv.deg,blh[1] / glv.deg,blh[2]]
#     blh_G = tr.wgs84togcj02(blh[0], blh[1])
#     # Lines_blh1[time]=[Lines_xyz1[time]["X"],Lines_xyz1[time]["Y"],Lines_xyz1[time]["Z"]]
#     Lines_blh1[time]=[blh[0],blh[1],blh[2]]

# for time in Lines_xyz2:
#     blh = tr.xyz2blh(Lines_xyz2[time]["X"],Lines_xyz2[time]["Y"],Lines_xyz2[time]["Z"])
#     blh = [blh[0] / glv.deg,blh[1] / glv.deg,blh[2]]
#     Lines_blh2[time]=[blh[0],blh[1],blh[2]]


# minLat = int(minLat)
# minLon = int(minLon)
# maxLat = ceil(maxLat)
# maxLon = ceil(maxLon)
print(maxLat,minLon)
print(minLat,maxLon)
delta = maxLat - minLat
if delta < (maxLon - minLon):
    delta = maxLon-minLon
print(delta)
if delta>10:
    space = delta/5
    # space = 10
    count = 5
else:
    space = space_set
    count = 0
if count==0:
    maxLat = maxLat + space/2
    minLon = minLon - space/2
    # minLat = minLat + space
#maxLat = maxLat + space/2
#minLat = minLat - space/2
#maxLon = maxLon + space/2
#minLon = minLon - space/2

cur_Lat = maxLat
cur_Lon = minLon
# plot grid
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
    folium.PolyLine(locations=[[maxLat,cur_Lon],[maxLat,cur_Lon + space]],color=c,weight=10).add_to(m)
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
    folium.PolyLine(locations=[[cur_Lat,maxLon],[cur_Lat - space,maxLon]],color=c,weight=10).add_to(m)
#---
#   |
#   |
#   |
#---
cur_Lon = cur_Lon + space
cur_Lat = cur_Lat - space
while cur_Lon > minLon:
    
    if i==0:
        c = 'white'
        i=1
    else:
        c = 'black'
        i=0
    folium.PolyLine(locations=[[minLat,cur_Lon-space],[minLat,cur_Lon]],color=c,weight=10).add_to(m)
    cur_Lon = cur_Lon - space
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
    folium.PolyLine(locations=[[cur_Lat,minLon],[cur_Lat + space,minLon]],color=c,weight=10).add_to(m)
    cur_Lat = cur_Lat + space
# text ref
# folium.Marker(location=[maxLat,minLon],popup=folium.Popup("Ref_Lat:{:.1f}\nRef_Lon:{:.1f}\nSpace:{:.1f}".format(maxLat,minLon,space),show=True),icon=folium.Icon(color='red',icon="info-sign"),tooltip="click").add_to(m)
# text only text
# folium.Marker(location=[maxLat,minLon], icon=DivIcon(
#         icon_size=(150,36),
#         icon_anchor=(7,20),
#         html='<div style="font-size: 18pt; color : black">'+"Ref_Lat:{:.1f}\nRef_Lon:{:.1f}\nSpace:{:.1f}".format(maxLat,minLon,space)+'</div>',
#         )).add_to(m)
# plot lines
for time in Lines_blh1:
    folium.Circle(radius=50,location=[Lines_blh1[time][0],Lines_blh1[time][1]],color="red",fill=True,fill_color="#3186cc").add_to(m)
# for time in Lines_blh2:
#     folium.Circle(radius=50,location=[Lines_blh2[time][0],Lines_blh2[time][1]],color="Red",fill=True,fill_color="#DA70D6").add_to(m)

#==================Denauly Triangle===========================#
# multipoint = MultiPoint(points)
# triangles = triangulate(multipoint,tolerance=0.001,edges=False)
# triangle = {}
# for index,t in enumerate(triangles):
#     ell_list = []
#     value = t.wkt.split(",")
#     value[3] = value[3][:len(value[3])-2] + "  " + value[3][len(value[3])-2:len(value[3])]
#     for i in range(len(value)):
#         if i == 0:
#             continue
#         ell_list.append(float(value[i].split(" ")[1]))
#         ell_list.append(float(value[i].split(" ")[2]))
#     triangle[index] = ell_list
# tri_dis = {}
# for index in triangle.keys():
#     cur_tri = []
#     blh1 = [triangle[index][0],triangle[index][1]]
#     blh2 = [triangle[index][2],triangle[index][3]]
#     blh3 = [triangle[index][4],triangle[index][5]]
#     for site in mark_point_blh.keys():
#         if mark_point_blh[site][0] == blh1[0] and mark_point_blh[site][1] == blh1[1] :
#             cur_tri.append(site)
#         if mark_point_blh[site][0] == blh2[0] and mark_point_blh[site][1] == blh2[1] :
#             cur_tri.append(site)
#         if mark_point_blh[site][0] == blh3[0] and mark_point_blh[site][1] == blh3[1] :
#             cur_tri.append(site)
#     c="blue"
#     line1 = cur_tri[0] + cur_tri[1]
#     line2 = cur_tri[1] + cur_tri[0]
#     if line1 not in tri_dis.keys() and line2 not in tri_dis.keys():
#         tri_dis[line1] = 1
#         blh1 = [mark_point_blh[cur_tri[0]][0],mark_point_blh[cur_tri[0]][1]]
#         blh2 = [mark_point_blh[cur_tri[1]][0],mark_point_blh[cur_tri[1]][1]]
#         folium.PolyLine(locations=[[blh1[0],blh1[1]],[blh2[0],blh2[1]]],color=c,weight=1).add_to(m)
#         b=(mark_point_blh[cur_tri[0]][0] + mark_point_blh[cur_tri[1]][0])/2
#         l=(mark_point_blh[cur_tri[0]][1] + mark_point_blh[cur_tri[1]][1])/2
#         dx=mark_point_xyz[cur_tri[0]][0]/1000 - mark_point_xyz[cur_tri[1]][0]/1000
#         dy=mark_point_xyz[cur_tri[0]][1]/1000 - mark_point_xyz[cur_tri[1]][1]/1000
#         dz=mark_point_xyz[cur_tri[0]][2]/1000 - mark_point_xyz[cur_tri[1]][2]/1000
#         dis = math.sqrt(dx*dx+dy*dy+dz*dz)
#         folium.Marker(location=[b,l], icon=DivIcon(
#             icon_size=(150,36),
#             icon_anchor=(7,20),
#             html='<div style="font-size: 10pt; color : red">'+"{:.2f}km".format(dis)+'</div>',
#             )).add_to(m)
#     line1 = cur_tri[0] + cur_tri[2]
#     line2 = cur_tri[2] + cur_tri[0]
#     if line1 not in tri_dis.keys() and line2 not in tri_dis.keys():
#         tri_dis[line1] = 1
#         blh1 = [mark_point_blh[cur_tri[0]][0],mark_point_blh[cur_tri[0]][1]]
#         blh2 = [mark_point_blh[cur_tri[2]][0],mark_point_blh[cur_tri[2]][1]]
#         folium.PolyLine(locations=[[blh1[0],blh1[1]],[blh2[0],blh2[1]]],color=c,weight=1).add_to(m)
#         b=(mark_point_blh[cur_tri[0]][0] + mark_point_blh[cur_tri[2]][0])/2
#         l=(mark_point_blh[cur_tri[0]][1] + mark_point_blh[cur_tri[2]][1])/2
#         dx=mark_point_xyz[cur_tri[0]][0]/1000 - mark_point_xyz[cur_tri[2]][0]/1000
#         dy=mark_point_xyz[cur_tri[0]][1]/1000 - mark_point_xyz[cur_tri[2]][1]/1000
#         dz=mark_point_xyz[cur_tri[0]][2]/1000 - mark_point_xyz[cur_tri[2]][2]/1000
#         dis = math.sqrt(dx*dx+dy*dy+dz*dz)
#         folium.Marker(location=[b,l], icon=DivIcon(
#             icon_size=(150,36),
#             icon_anchor=(7,20),
#             html='<div style="font-size: 10pt; color : red">'+"{:.2f}km".format(dis)+'</div>',
#             )).add_to(m)
#     line1 = cur_tri[1] + cur_tri[2]
#     line2 = cur_tri[2] + cur_tri[1]
#     if line1 not in tri_dis.keys() and line2 not in tri_dis.keys():
#         tri_dis[line1] = 1
#         blh1 = [mark_point_blh[cur_tri[1]][0],mark_point_blh[cur_tri[1]][1]]
#         blh2 = [mark_point_blh[cur_tri[2]][0],mark_point_blh[cur_tri[2]][1]]
#         folium.PolyLine(locations=[[blh1[0],blh1[1]],[blh2[0],blh2[1]]],color=c,weight=1).add_to(m)
#         b=(mark_point_blh[cur_tri[1]][0] + mark_point_blh[cur_tri[2]][0])/2
#         l=(mark_point_blh[cur_tri[1]][1] + mark_point_blh[cur_tri[2]][1])/2
#         dx=mark_point_xyz[cur_tri[1]][0]/1000 - mark_point_xyz[cur_tri[2]][0]/1000
#         dy=mark_point_xyz[cur_tri[1]][1]/1000 - mark_point_xyz[cur_tri[2]][1]/1000
#         dz=mark_point_xyz[cur_tri[1]][2]/1000 - mark_point_xyz[cur_tri[2]][2]/1000
#         dis = math.sqrt(dx*dx+dy*dy+dz*dz)
#         folium.Marker(location=[b,l], icon=DivIcon(
#             icon_size=(150,36),
#             icon_anchor=(7,20),
#             html='<div style="font-size: 10pt; color : red">'+"{:.2f}km".format(dis)+'</div>',
#             )).add_to(m)

#==================Min Distance===========================#
# line_mindis = {}
# line_mindis1 = {}
# for cur_site in mark_point_xyz.keys():
#     for cur_site1 in mark_point_xyz.keys():
#         if cur_site == cur_site1:
#             continue
#         line1 = cur_site + cur_site1
#         line2 = cur_site1 + cur_site
#         dx = mark_point_xyz[cur_site][0] - mark_point_xyz[cur_site1][0]
#         dy = mark_point_xyz[cur_site][1] - mark_point_xyz[cur_site1][1]
#         dz = mark_point_xyz[cur_site][2] - mark_point_xyz[cur_site1][2]
#         dis = math.sqrt(dx*dx+dy*dy+dz*dz) / 1000
#         if cur_site not in line_mindis.keys():
#             line_mindis[cur_site] = {}
#             line_mindis1[cur_site] = []
#         line_mindis[cur_site][dis] = cur_site1
#         line_mindis1[cur_site].append(dis)
# line_mindis2 = {}
# for cur_site in line_mindis1.keys():
#     min_list = sorted(line_mindis1[cur_site])
#     min1,min2,min3 = min_list[0],min_list[1],min_list[2]
#     if cur_site not in line_mindis2.keys():
#         line_mindis2[cur_site] = {}
#     line_mindis2[cur_site][line_mindis[cur_site][min1]] = min1
#     line_mindis2[cur_site][line_mindis[cur_site][min2]] = min2
#     line_mindis2[cur_site][line_mindis[cur_site][min3]] = min3
# line_plot = []
# i = 0
# for cur_site in line_mindis2.keys():
#     c=cmap4[i]
#     i = i+1
#     for cur_site1 in line_mindis2[cur_site].keys():
#         line1 = cur_site + cur_site1
#         line2 = cur_site1 + cur_site
#         blh1 = [mark_point_blh[cur_site][0],mark_point_blh[cur_site][1]]
#         blh2 = [mark_point_blh[cur_site1][0],mark_point_blh[cur_site1][1]]
#         b=(mark_point_blh[cur_site][0] + mark_point_blh[cur_site1][0])/2
#         l=(mark_point_blh[cur_site][1] + mark_point_blh[cur_site1][1])/2
#         if line1 not in line_plot and line2 not in line_plot:
#             line_plot.append(line1)
#             folium.PolyLine(locations=[[blh1[0],blh1[1]],[blh2[0],blh2[1]]],color=c,weight=2).add_to(m)
#             folium.Marker(location=[b,l], icon=DivIcon(
#                 icon_size=(150,36),
#                 icon_anchor=(7,20),
#                 html='<div style="font-size: 10pt; color : red">'+"{:.2f}km".format(line_mindis2[cur_site][cur_site1])+'</div>',
#                 )).add_to(m)
#         else:
#             folium.PolyLine(locations=[[blh1[0],blh1[1]],[b,l]],color=c,weight=2).add_to(m)

# ========================Min Dis Grid ===============#
minDis = 1e16
maxDis = 0
for site_in_list in site_list:
    for cur_site in site_list:
        if cur_site == site_in_list:
            continue
        dx = mark_point_xyz[cur_site][0] - mark_point_xyz[site_in_list][0]
        dy = mark_point_xyz[cur_site][1] - mark_point_xyz[site_in_list][1]
        dz = mark_point_xyz[cur_site][2] - mark_point_xyz[site_in_list][2]
        dis = math.sqrt(dx*dx+dy*dy+dz*dz)
        if dis < minDis:
            minDis = dis
        if dis > maxDis:
            maxDis = dis
print("Min:{:.1f}km,Max:{:.1f}km".format(minDis/1000,maxDis/1000))
line_mindis = {}
line_mindis1 = {}
index_grid = 0
print(range(count_lat))
for site_in_list in site_list:
    line_mindis = {}
    line_mindis1 = {}
    index_grid = 0
    line_mindis3={}
    blh = mark_point_blh[site_in_list]
    delta_Lat = int((maxLat-blh[0])/space)
    delta_Lon = int((blh[1] - minLon)/space)
    index_list = []
    index_list.append('%02d' % (delta_Lat * count_lon + delta_Lon))
    index_list.append('%02d' % (delta_Lat * count_lon + delta_Lon + 1))
    index_list.append('%02d' % ((delta_Lat + 1) * count_lon + delta_Lon))
    index_list.append('%02d' % ((delta_Lat + 1) * count_lon + delta_Lon + 1))
    for i in range(count_lat):
        for j in range(count_lon):
            for cur_site in mark_point_xyz.keys():
                if site_in_list == cur_site:
                    continue
                b=maxLat - i*space
                l=minLon + j*space
                h=0.0
                mark_point_blh['%02d' % (index_grid)] = [b,l,h]
                xyz = tr.blh2xyz(b* glv.deg,l* glv.deg,h)
                line1 = cur_site + '%02d' % (index_grid)
                line2 =  '%02d' % (index_grid) + cur_site
                dx = mark_point_xyz[cur_site][0] - xyz[0]
                dy = mark_point_xyz[cur_site][1] - xyz[1]
                dz = mark_point_xyz[cur_site][2] - xyz[2]
                dis = math.sqrt(dx*dx+dy*dy+dz*dz)
                if '%02d' % (index_grid) not in line_mindis.keys():
                    line_mindis['%02d' % (index_grid)] = {}
                    line_mindis1['%02d' % (index_grid)] = []
                line_mindis['%02d' % (index_grid)][dis] = cur_site
                line_mindis1['%02d' % (index_grid)].append(dis)
            index_grid = index_grid +1
    line_mindis2 = {}
    cofe_grid = []
    for cur_site in line_mindis1.keys():
        min_list = sorted(line_mindis1[cur_site])
        min1,min2,min3 = min_list[0],min_list[1],min_list[2]
        if cur_site not in line_mindis2.keys():
            line_mindis2[cur_site] = {}
        if cur_site not in line_mindis3.keys():
            line_mindis3[cur_site] = [min1,min2,min3]
        line_mindis2[cur_site][line_mindis[cur_site][min1]] = min1
        line_mindis2[cur_site][line_mindis[cur_site][min2]] = min2
        line_mindis2[cur_site][line_mindis[cur_site][min3]] = min3
        cofe_grid.append((min1+min2+min3)/3)
    # m.save(savedir+"\\"+site_in_list+".html")
    mean_index_dis = []
    for cur_index in line_mindis3.keys():
        mean_index_dis.append(np.mean(line_mindis3[cur_index]))
    site_dis_mean = []
    site_dis_mean.append(np.mean(line_mindis3[index_list[0]]))
    site_dis_mean.append(np.mean(line_mindis3[index_list[1]]))
    site_dis_mean.append(np.mean(line_mindis3[index_list[2]]))
    site_dis_mean.append(np.mean(line_mindis3[index_list[3]]))
    dis_site_in_list = []
    for index_grid2 in index_list:
        xyz_site = mark_point_xyz[site_in_list]
        blh_grid = mark_point_blh[index_grid2]
        xyz_grid = tr.blh2xyz(blh_grid[0]* glv.deg,blh_grid[1]* glv.deg,blh_grid[2])
        dx = xyz_site[0] - xyz_grid[0]
        dy = xyz_site[1] - xyz_grid[1]
        dz = xyz_site[2] - xyz_grid[2]
        dis = math.sqrt(dx*dx+dy*dy+dz*dz)
        dis_site_in_list.append(dis)
    dis_mean_wgt = dis_site_in_list[0] / np.sum(dis_site_in_list) * site_dis_mean[0] + dis_site_in_list[1] / np.sum(dis_site_in_list) * site_dis_mean[1] + dis_site_in_list[2] / np.sum(dis_site_in_list) * site_dis_mean[2] + dis_site_in_list[3] / np.sum(dis_site_in_list) * site_dis_mean[3]
    angle = []
    angle_mean = []
    triangle = []
    for index in index_list:
        angle = [1,1,1]
        site_3=[]
        for site_mindis_index in line_mindis2[index].keys():
            blh_grid = mark_point_blh[index]
            blh_site = mark_point_blh[site_mindis_index]
            site_3.append(blh_site)
            deg_tan = get_angel(blh_grid,blh_site)
            if 0<=deg_tan<120:
                angle[0] = angle[0] - 1
            if 120<=deg_tan<240:
                angle[1] = angle[1] - 1
            if 240<=deg_tan<360:
                angle[2] = angle[2] - 1
        angle_mean.append(evenlyangle(mark_point_blh[index],site_3))
        triangle.append(isintriangle(mark_point_blh[index],site_3))
        # if tri == 1:
        #     angle_mean.append(0.5*(np.sum(np.abs(angle))))
        # else:
        #     angle_mean.append(np.sum(np.abs(angle)))
    angle_mean_wgt = dis_site_in_list[0] / np.sum(dis_site_in_list) * angle_mean[0] + dis_site_in_list[1] / np.sum(dis_site_in_list) * angle_mean[1] + dis_site_in_list[2] / np.sum(dis_site_in_list) * angle_mean[2] + dis_site_in_list[3] / np.sum(dis_site_in_list) * angle_mean[3]
    # folium.Marker(location=[mark_point_blh[site_in_list][0],mark_point_blh[site_in_list][1]], icon=DivIcon(
    #             icon_size=(150,36),
    #             icon_anchor=(7,20),
    #             html='<div style="font-size: 15pt; color : black">'+"{:.2f},{:.0f}".format(np.mean(site_dis_mean),np.sum(angle_mean))+'</div>',
    #             )).add_to(m)
    
    print("{} : Mean: {:>10.2f} Wgt_Mean: {:>10.2f} Max3: {:>10.2f} Min: {:>10.2f} 1: {:>10.2f} 2: {:>10.2f} 3: {:>10.2f} 4: {:>10.2f} Mean_ALL: {:>10.2f}  {:.0f}  {:7.2f} {:7.2f}".format(site_in_list,np.mean(site_dis_mean),dis_mean_wgt,np.max(site_dis_mean),np.min(mean_index_dis),dis_site_in_list[0],dis_site_in_list[1],dis_site_in_list[2],dis_site_in_list[3],np.mean(mean_index_dis),np.sum(triangle),np.mean(angle_mean),angle_mean_wgt))

line_mindis = {}
line_mindis1 = {}
index_grid = 0
print(range(count_lat))
for i in range(count_lat):
    for j in range(count_lon):
        for cur_site in mark_point_xyz.keys():
            if "HKTK" == cur_site:
                continue
            b=maxLat - i*space
            l=minLon + j*space
            h=0.0
            mark_point_blh['%02d' % (index_grid)] = [b,l,h]
            xyz = tr.blh2xyz(b* glv.deg,l* glv.deg,h)
            line1 = cur_site + '%02d' % (index_grid)
            line2 =  '%02d' % (index_grid) + cur_site
            dx = mark_point_xyz[cur_site][0] - xyz[0]
            dy = mark_point_xyz[cur_site][1] - xyz[1]
            dz = mark_point_xyz[cur_site][2] - xyz[2]
            dis = math.sqrt(dx*dx+dy*dy+dz*dz)
            if '%02d' % (index_grid) not in line_mindis.keys():
                line_mindis['%02d' % (index_grid)] = {}
                line_mindis1['%02d' % (index_grid)] = []
            line_mindis['%02d' % (index_grid)][dis] = cur_site
            line_mindis1['%02d' % (index_grid)].append(dis)
        index_grid = index_grid +1
line_mindis2 = {}
cofe_grid = []
minDis = 1e16
maxDis = 0
for cur_site in line_mindis1.keys():
    min_list = sorted(line_mindis1[cur_site])
    min1,min2,min3 = min_list[0],min_list[1],min_list[2]
    if cur_site not in line_mindis2.keys():
        line_mindis2[cur_site] = {}
    if cur_site not in line_mindis3.keys():
        line_mindis3[cur_site] = [min1,min2,min3]
    line_mindis2[cur_site][line_mindis[cur_site][min1]] = min1
    line_mindis2[cur_site][line_mindis[cur_site][min2]] = min2
    line_mindis2[cur_site][line_mindis[cur_site][min3]] = min3
    cofe_grid.append((min1+min2+min3)/3)
    diss = (min1+min2+min3)/3
    if diss < minDis:
        minDis = diss
    if diss > maxDis:
        maxDis = diss
    # folium.Marker(location=[mark_point_blh[cur_site][0],mark_point_blh[cur_site][1]], icon=DivIcon(
    #             icon_size=(150,36),
    #             icon_anchor=(7,20),
    #             html='<div style="font-size: 10pt; color : red">'+"{:.2f}".format((min1+min2+min3)/3)+'</div>',
    #             )).add_to(m)
Dis_User = []
for site_in_list in site_list:
    if site_in_list == site_user:
        continue
    xyz_site = mark_point_xyz[site_in_list]
    xyz_grid = mark_point_xyz[site_user]
    dx = xyz_site[0] - xyz_grid[0]
    dy = xyz_site[1] - xyz_grid[1]
    dz = xyz_site[2] - xyz_grid[2]
    dis = math.sqrt(dx*dx+dy*dy+dz*dz)
    Dis_User.append(dis)
print("{}:{:.2f}".format("AUG",np.mean(cofe_grid)))
print("Min:{:.1f}km,Max:{:.1f}km".format(minDis/1000,maxDis/1000))
print("{}:{:.1f}km".format(site_user,np.mean(Dis_User)/1000))
# line_plot = []
# i = 0
# for cur_site in line_mindis2.keys():
#     c='blue'
#     i = i+1
#     for cur_site1 in line_mindis2[cur_site].keys():
#         line1 = cur_site + cur_site1
#         line2 = cur_site1 + cur_site
#         blh1 = [mark_point_blh[cur_site][0],mark_point_blh[cur_site][1]]
#         blh2 = [mark_point_blh[cur_site1][0],mark_point_blh[cur_site1][1]]
#         b=(mark_point_blh[cur_site][0] + mark_point_blh[cur_site1][0])/2
#         l=(mark_point_blh[cur_site][1] + mark_point_blh[cur_site1][1])/2
#         if line1 not in line_plot and line2 not in line_plot:
#             line_plot.append(line1)
#             folium.PolyLine(locations=[[blh1[0],blh1[1]],[blh2[0],blh2[1]]],color=c,weight=2).add_to(m)
#             folium.Marker(location=[b,l], icon=DivIcon(
#                 icon_size=(150,36),
#                 icon_anchor=(7,20),
#                 html='<div style="font-size: 10pt; color : red">'+"{:.2f}km".format(line_mindis2[cur_site][cur_site1])+'</div>',
#                 )).add_to(m)
#         else:
#             folium.PolyLine(locations=[[blh1[0],blh1[1]],[b,l]],color=c,weight=2).add_to(m)
# m.save(savedir+"\\AUG-WH-Dynamic-310.html")
m.save(r"E:\1Master_2\3-IUGG\crd\AUG_HK.html")
 
# path_wkimg = r'D:\Program Files\wkhtmltopdf\bin\wkhtmltoimage.exe'  # 工具路径
# cfg = imgkit.config(wkhtmltoimage=path_wkimg)
# 1、将html文件转为图片
# imgkit.from_file(r'E:\1Master_2\2-UPD_Test\UPD.html', 'helloworld.jpg', config=cfg)
# 2、从url获取html，再转为图片
# imgkit.from_url('https://www.whu.edu.cn/', 'ip.jpg', config=cfg)
# 3、将字符串转为图片
# imgkit.from_string('Hello!','hello.jpg', config=cfg)
# webbrowser.open(r'E:\1Master_2\Paper_Grid\crd\AUG_HK2.html')




