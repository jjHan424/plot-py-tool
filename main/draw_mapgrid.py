'''
Author: your name
Date: 2022-03-07 10:03:20
LastEditTime: 2022-03-28 19:26:32
LastEditors: Please set LastEditors
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
import webbrowser
import trans as tr
import glv

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
              'HKQT':[-2421567.8916,5384910.5631,2404264.3943],
              'HKSC':[-2414266.9197,5386768.9868,2407460.0314],
              'HKSL':[-2393382.4157,5393861.1745,2412592.4105],
              'HKSS':[-2424425.1013,5377188.1768,2418617.7454],
              'HKST':[-2417142.8718,5382345.4730,2415036.9459],
              'HKTK':[-2418092.3728,5374658.3417,2430429.1904],
              'HKWS':[-2430579.0108,5374285.6738,2418956.3331],
              #'KYC1':[-2408855.2574,5391043.2386,2403591.1306],
              'T430':[-2411015.2264,5380265.7133,2425132.7008]
                }

# mark_point_xyz = {
#               'HKKT':[-2405143.8990,5385195.2549,2420032.5440],
#               'HKLT':[-2399062.7358,5389237.8430,2417327.0568],
#               'HKMW':[-2402484.1093,5395262.4383,2400726.9555],
#               'HKOH':[-2423816.8997,5386057.0931,2399883.3709],
#               'HKPC':[-2405183.0015,5392541.8294,2403645.7303],
#               'HKQT':[-2421567.8916,5384910.5631,2404264.3943],
#               'HKSC':[-2414266.9197,5386768.9868,2407460.0314],
#               'HKST':[-2417142.8718,5382345.4730,2415036.9459],
#               'T430':[-2411015.2264,5380265.7133,2425132.7008]
#                 }
m = folium.Map(location=[center_bl[0], center_bl[1]], zoom_start=11, tiles='Stamen Terrain')
mark_point_blh={}
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
    if (site == "HKSC"):
        folium.Marker(location=[blh[0],blh[1]],popup=folium.Popup(site,show=True),icon=folium.Icon(color='red'),tooltip="click").add_to(m)
    if (site == "HKTK"):
        folium.Marker(location=[blh[0],blh[1]],popup=folium.Popup(site,show=True),icon=folium.Icon(color='blue'),tooltip="click").add_to(m)
    if (site == "HKLM"):
        folium.Marker(location=[blh[0],blh[1]],popup=folium.Popup(site,show=True),icon=folium.Icon(color='green'),tooltip="click").add_to(m)

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
if delta>2.5:
    space = delta/5
    count = 5
else:
    space = 0.1
    count = 0
if count==0:
    maxLat = maxLat + space/2
    minLon = minLon - space/2
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
    folium.PolyLine(locations=[[maxLat,cur_Lon],[minLat,cur_Lon]],color='black',dash_array='20',weight = 2).add_to(m)    
maxLon = cur_Lon
while cur_Lat > minLat:
    if abs(cur_Lat - minLat) < 1e-8:
        break
    cur_Lat = cur_Lat - space
    folium.PolyLine(locations=[[cur_Lat,minLon],[cur_Lat,maxLon]],color='black',dash_array='20',weight=2).add_to(m)
minLat = cur_Lat
cur_Lon = minLon
while cur_Lon < maxLon:
    cur_Lon = cur_Lon + space
    folium.PolyLine(locations=[[maxLat,cur_Lon],[minLat,cur_Lon]],color='black',dash_array='20',weight=2).add_to(m)
#plot bound
cur_Lat = maxLat + space
cur_Lon = minLon - space
i=0

#---
while cur_Lon < maxLon - space:
    cur_Lon = cur_Lon + space
    if i==0:
        c = 'white'
        i=1
    else:
        c = 'black'
        i=0
    folium.PolyLine(locations=[[maxLat,cur_Lon],[maxLat,cur_Lon + space]],color=c,weight=5).add_to(m)
#---
#   |
#   |
#   |
while cur_Lat > minLat + space:
    cur_Lat = cur_Lat - space
    if i==0:
        c = 'white'
        i=1
    else:
        c = 'black'
        i=0
    folium.PolyLine(locations=[[cur_Lat,maxLon],[cur_Lat - space,maxLon]],color=c,weight=5).add_to(m)
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
    folium.PolyLine(locations=[[minLat,cur_Lon-space],[minLat,cur_Lon]],color=c,weight=5).add_to(m)
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
    folium.PolyLine(locations=[[cur_Lat,minLon],[cur_Lat + space,minLon]],color=c,weight=5).add_to(m)
    cur_Lat = cur_Lat + space
# text ref
folium.Marker(location=[maxLat,minLon],popup=folium.Popup("Ref_Lat:{:.1f}\nRef_Lon:{:.1f}\nSpace:{:.1f}".format(maxLat,minLon,space),show=True),icon=folium.Icon(color='blue'),tooltip="click").add_to(m)
m.save('/Users/hjj/Desktop/PPT.html')
webbrowser.open('/Users/hjj/Desktop/HongKongGridS.html')