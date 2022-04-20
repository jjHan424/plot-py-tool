'''
Author: your name
Date: 2022-04-15 15:01:25
LastEditTime: 2022-04-15 15:30:48
LastEditors: Please set LastEditors
Description: 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
FilePath: /plot-py-tool/main/draw_temp.py
'''
from audioop import bias
from math import sqrt
import os
import sys
from turtle import width
sys.path.insert(0,os.path.dirname(__file__)+'/..')
import numpy as np
import readfile as rf
import matplotlib as mpl
mpl.use("TkAgg")
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import dataprocess as dp
import draw as dr

E1 = [0.80,0.34,0.31,0.75,0.23,0.45,0.46,0.35,0.52,0.27]
N1 = [0.28,0.61,0.35,1.04,0.21,0.52,0.46,0.34,0.75,0.50]
U1 = [1.44,1.40,1.78,3.27,1.24,1.85,2.05,1.30,1.69,1.78]
D1 = []
Fixed1 = [47.7,56.4,66.4,50.2,57.3,45.2,40.3,44.4,48.1,47.7]
IG1 = [57.29,44.5,32.81,64.11,21.92,55.31,60.15,44.62,89.32,95.35]
IE1 = [34.25,39.74,29.16,4.18,13.83,19.94,44.43,22.94,26.11,38.47]

E2 = [2.41,0.16,0.14,0.09,2.40,0.51,0.75,0.42,0.17,0.51]
N2 = [0.80,0.19,0.13,0.11,1.36,0.49,0.66,0.38,0.31,3.68]
U2 = [2.89,0.68,0.82,0.48,1.59,1.90,4.35,2.04,2.89,15.92]
D2 = []
Fixed2 = [46.9,84.7,87.55,95.0,60.6,51.9,33.6,36.5,76.4,48.1]
IG2 = [137.57,65.89,53.45,37.84,68.91,104.16,132.25,124.81,159.53,129.54]
IE2 = [54.86,40.39,5.74,22.17,56.62,144.33,87.92,40.98,65.30,26.57]
BG2 = [5.49,9.43,4.06,7.21,6.56,38.61,25.2,4.06,4.85,18.17]
BE2 = [7.96,4.82,2.75,2.39,6.32,7.70,12.3,4.01,1.55,3.59]

E3 = [2.20,1.16,0.70,0.52,0.67,0.59,4.06,0.71,0.39,0.32]
N3 = [0.64,1.20,1.15,0.39,0.49,0.63,1.30,0.60,0.53,0.34]
U3 = [2.23,3.05,2.44,1.15,3.30,2.59,8.00,2.19,2.88,1.33]
D3 = []
Fixed3 = [54.4,48.6,47.3,64.7,41.9,51.0,43.6,36.9,62.2,53.5]
IG3=[130.42,112.73,103.17,74.99,114.31,125.62,118.29,119.23,166.82,131.86]
IE3=[43.59,113.72,66.75,87.34,94.51,170.47,79.78,45.22,49.15,27.17]
BG3 = [133.2,162.5,34.37,2.42,7.57,13.38,5.33,176.5,213.9,327.1]
BE3 = [5.37,3.44,0.87,1.42,4.48,1.36,1.73,3.16,1.37,2.16]

for i in range(len(E1)):
    D1.append(sqrt(E1[i]*E1[i]+N1[i]*N1[i]+U1[i]*U1[i])*100)
    D2.append(sqrt(E2[i]*E2[i]+N2[i]*N2[i]+U2[i]*U2[i])*100)
    D3.append(sqrt(E3[i]*E3[i]+N3[i]*N3[i]+U3[i]*U3[i])*100)
x=list(range(len(E1)))
xlabel=["10:00-12:00",
        "12:00-14:00",
        "14:00-16:00",
        "16:00-18:00",
        "18:00-20:00",
        "20:00-22:00",
        "22:00-24:00",
        "24:00-02:00",
        "02:00-04:00",
        "04:00-06:00"]
plt.figure
gs=gridspec.GridSpec(4,2)
ax11 = plt.subplot(gs[0,:])
ax11.grid(linestyle='--',linewidth=0.2, color='black',axis='both')
ax21 = plt.subplot(gs[1,:])
ax21.grid(linestyle='--',linewidth=0.2, color='black',axis='both')
ax31 = plt.subplot(gs[2,0])
ax31.grid(linestyle='--',linewidth=0.2, color='black',axis='both')
ax32 = plt.subplot(gs[2,1])
ax32.grid(linestyle='--',linewidth=0.2, color='black',axis='both')
ax41 = plt.subplot(gs[3,0])
ax41.grid(linestyle='--',linewidth=0.2, color='black',axis='both')
ax42 = plt.subplot(gs[3,1])
ax42.grid(linestyle='--',linewidth=0.2, color='black',axis='both')

ax11.set_ylabel("Positioning Errors(cm)")

ax11.plot(x,D2,marker='o',linewidth = 1,markersize = 3)
ax11.plot(x,D3,marker='o',linewidth = 1,markersize = 3)
ax11.plot(x,D1,marker='o',linewidth = 1,markersize = 3)
ax11.set_xticks(x)
ax11.set_xticklabels(xlabel)
ax11.legend(["Bias1","Bias3","NoBias"])

ax21.set_ylabel("Fixed Rate(%)")
W = 0.25
xbar = []
for i in range(len(x)):
    xbar.append(x[i]-W)
ax21.bar(xbar,Fixed2,width = W)
xbar = []
for i in range(len(x)):
    xbar.append(x[i])
ax21.bar(xbar,Fixed3,width = W)
xbar = []
for i in range(len(x)):
    xbar.append(x[i]+W)
ax21.bar(xbar,Fixed1,width = W)
ax21.set_xticks(x)
ax21.set_xticklabels(xlabel)
ax21.legend(["Bias1","Bias3","NoBias"])
x_smale=[0,2,4,6,8]
xlabel=["10:00-12:00",
        
        "14:00-16:00",
        
        "18:00-20:00",
        
        "22:00-24:00",
        
        "02:00-04:00"
        ]
ax31.set_ylabel("GPS:Iono/cm")
ax31.plot(x,IG2,marker='o',linewidth = 1,markersize = 3)
ax31.plot(x,IG3,marker='o',linewidth = 1,markersize = 3)
ax31.plot(x,IG1,marker='o',linewidth = 1,markersize = 3)
ax31.set_xticks(x_smale)
ax31.set_xticklabels(xlabel)
ax41.set_ylabel("GAL:Iono/cm")
ax41.plot(x,IE2,marker='o',linewidth = 1,markersize = 3)
ax41.plot(x,IE3,marker='o',linewidth = 1,markersize = 3)
ax41.plot(x,IE1,marker='o',linewidth = 1,markersize = 3)
ax41.set_xticks(x_smale)
ax41.set_xticklabels(xlabel)

ax32.set_ylabel("GPS:Bias/cm")
ax32.plot(x,BG2,marker='o',linewidth = 1,markersize = 3)
ax32.plot(x,BG3,marker='o',linewidth = 1,markersize = 3)
ax32.set_xticks(x_smale)
ax32.set_xticklabels(xlabel)
ax42.set_ylabel("GAL:Bias/cm")
ax42.plot(x,BE2,marker='o',linewidth = 1,markersize = 3)
ax42.plot(x,BE3,marker='o',linewidth = 1,markersize = 3)
ax42.set_xticks(x_smale)
ax42.set_xticklabels(xlabel)

plt.show()