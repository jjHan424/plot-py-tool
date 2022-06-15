#!/usr/bin/python
# author: zhShen
# date: 20190520
import glv
from math import *
import numpy as np



def blh2xyz(B,L,H):
    sB = sin(B)
    cB = cos(B)
    sL = sin(L)
    cL = cos(L)
    N = glv.a/sqrt(1-glv.e2*sB**2)
    X = (N+H)*cB*cL
    Y = (N+H)*cB*sL
    Z = (N*(1-glv.e2)+H)*sB
    return np.array([X,Y,Z])

def xyz2blh(X,Y,Z):
    bell = glv.a*(1.0-1.0/glv.f)                          
    ss = sqrt(X*X+Y*Y)   
    zps   = Z/ss
    theta = atan( (Z*glv.a) / (ss*glv.b) )
    sin3  = sin(theta) * sin(theta) * sin(theta)
    cos3  = cos(theta) * cos(theta) * cos(theta)
    
    #Closed formula
    B = atan((Z + glv.ep2 * glv.b * sin3) / (ss - glv.e2 * glv.a * cos3))
    L = atan2(Y,X)
    nn = glv.a/sqrt(1.0-glv.e2*sin(B)*sin(L))
    H = ss/cos(B) - nn

    i=0
    while i<=100:
        nn = glv.a/sqrt(1.0-glv.e2*sin(B)*sin(B))
        hOld = H
        phiOld = B
        H = ss/cos(B)-nn
        B = atan(zps/(1.0-glv.e2*nn/(nn+H)))
        if abs(phiOld-B) <= 1.0e-8 and abs(hOld-H) <= 1.0e-3:
            # always convert longitude to 0-360
            if L < 0.0 :
                L += 2 * pi
            break

        i+=1

    return np.array([B,L,H])


def xyz2enu(XYZ=[],XYZ_Ref=[]):

    [b,l,h]=xyz2blh(XYZ[0],XYZ[1],XYZ[2])

    r=[XYZ[0]-XYZ_Ref[0], XYZ[1]-XYZ_Ref[1], XYZ[2]-XYZ_Ref[2]]


    sinPhi = sin(b)
    cosPhi = cos(b)
    sinLam = sin(l)
    cosLam = cos(l)

    N = -sinPhi * cosLam * r[0] - sinPhi * sinLam * r[1] + cosPhi * r[2]
    E = -sinLam * r[0] + cosLam * r[1]
    U = +cosPhi * cosLam * r[0] + cosPhi * sinLam * r[1] + sinPhi * r[2]

    return np.array([E,N,U])

def Cne(B,L):
    res=np.mat(np.zeros((3,3)))

    slat = np.sin(B) 
    clat = np.cos(B)
    slon = np.sin(L) 
    clon = np.cos(L)
    res = np.matrix([[ -slon,clon,0 ],
          [ -slat*clon, -slat*slon, clat],
          [  clat*clon,  clat*slon, slat]])
    return res


def Cnb(pitch,roll,yaw):
    sp = np.sin(pitch)
    cp = np.cos(pitch)
    sr = np.sin(roll)
    cr = np.cos(roll)
    sy = np.sin(yaw)
    cy = np.cos(yaw)
    res=np.matrix([[cy*cr - sy*sp*sr, -sy*cp, cy*sr + sy*sp*cr],
                    [sy*cr + cy*sp*sr, cy*cp, sy*sr - cy*sp*cr],
                    [-cp*sr, sp, cp*cr]])
    return res

def rad2dms(rad):
    deg=rad/glv.deg
    int_d=int(deg)
    m=(deg-int(deg))*60
    int_m=int(m)
    s=(m-int(m))*60
    return str(int_d)+str(int_m)+str(s)


def ymd2gpst(year,month,day,hour,minute,second):
    if month <= 2:
        year = year - 1
        month = month + 12
    JD = floor(365.25*year) + int(30.6001*(month+1)) + day + \
        (hour + minute/60 + second/3600) / 24 + 1720981.5
    w = floor((JD-2444244.5)/7)
    sow = ((JD - 2444244.5)*3600*24 - w * 3600 * 24 * 7)
    
    if abs(sow - round(sow)) < 1e-2:
        sow = round(sow)
    return (w,sow)
    
def mjd2gpst(day,sec):
    w = floor((day - 44244) / 7)
    sow = sec + ((day - 44244) / 7 - w) * 86400
    return(w,sow)

def ymd2doy(year,month,day,hour,minute,second):
    doy = floor(month*275/9)-floor((month+9)/12)*(floor((year-4*floor(year/4)+2)/3)+1)+day-30
    return doy

def transformlat(lng, lat):
    PI = 3.1415926535897932384626
    ret = -100.0 + 2.0 * lng + 3.0 * lat + 0.2 * lat * \
          lat + 0.1 * lng * lat + 0.2 * sqrt(abs(lng))
    ret += (20.0 * sin(6.0 * lng * PI) + 20.0 *
            sin(2.0 * lng * PI)) * 2.0 / 3.0
    ret += (20.0 * sin(lat * PI) + 40.0 *
            sin(lat / 3.0 * PI)) * 2.0 / 3.0
    ret += (160.0 * sin(lat / 12.0 * PI) + 320 *
            sin(lat * PI / 30.0)) * 2.0 / 3.0
    return ret
def transformlng(lng, lat):
    PI = 3.1415926535897932384626
    ret = 300.0 + lng + 2.0 * lat + 0.1 * lng * lng + \
          0.1 * lng * lat + 0.1 * sqrt(abs(lng))
    ret += (20.0 * sin(6.0 * lng * PI) + 20.0 *
            sin(2.0 * lng * PI)) * 2.0 / 3.0
    ret += (20.0 * sin(lng * PI) + 40.0 *
            sin(lng / 3.0 * PI)) * 2.0 / 3.0
    ret += (150.0 * sin(lng / 12.0 * PI) + 300.0 *
            sin(lng / 30.0 * PI)) * 2.0 / 3.0
    return ret

def wgs84togcj02(lng, lat):
    PI = 3.1415926535897932384626
    ee = 0.00669342162296594323
    a = 6378245.0
    dlat = transformlat(lng - 105.0, lat - 35.0)
    dlng = transformlng(lng - 105.0, lat - 35.0)
    radlat = lat / 180.0 * PI
    magic = sin(radlat)
    magic = 1 - ee * magic * magic
    sqrtmagic = sqrt(magic)
    dlat = (dlat * 180.0) / ((a * (1 - ee)) / (magic * sqrtmagic) * PI)
    dlng = (dlng * 180.0) / (a / sqrtmagic * cos(radlat) * PI)
    mglat = lat + dlat
    mglng = lng + dlng
    return [mglng, mglat]
