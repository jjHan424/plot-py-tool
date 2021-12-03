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
        if abs(phiOld-B) <= 1.0e-11 and abs(hOld-H) <= 1.0e-5:
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
