#!/usr/bin/env python
#-*- coding:utf-8 -*-
import os
import math
import tkinter as tk
import numpy as np
from scipy.interpolate import interp1d
from random import randint
EPSILON=1/10000000000

# 点类
class Point:
    '''包含 点名 数学坐标X 数学坐标Y  高程（z）H'''
    def __init__(self,pointname,x,y,h):
        self.PointName=pointname
        self.X=x
        self.Y=y
        self.H=h
    def Cal_Distans(self,x0,y0):
        d=math.sqrt(math.pow(x0-self.X,2)+math.pow(y0-self.Y,2))
        return d
# 线类
class Line:
    def __init__(self,point_b,point_e):
        self.BeginPoint=point_b
        self.EndPoint=point_e
        self.Belonging_Triangle=[]
    def __eq__(self, other):
        if(self.BeginPoint.PointName==other.EndPoint.PointName and
            self.EndPoint.PointName==other.BeginPoint.PointName):
            return 1
        elif(self.BeginPoint.PointName==other.BeginPoint.PointName and
              self.EndPoint.PointName==other.EndPoint.PointName):
            return 1
        else:
            return 0

# 三角形类
class Triangle:
    def __init__(self,point_b,point_e,point_s):
        self.BaseLine=Line(point_b,point_e)
        self.newLine1=Line(point_b,point_s)
        self.newLine2=Line(point_s,point_e)
    def __eq__(self, other):#重载==
        if(self.BaseLine==other.BaseLine and self.newLine1==other.newLine1 and self.newLine2==other.newLine2):
            return 1
        elif(self.BaseLine==other.BaseLine and self.newLine1==other.newLine2 and self.newLine2==other.newLine1):
            return 1
        elif(self.BaseLine==other.newLine1 and self.newLine1==other.newLine2 and self.newLine2==other.BaseLine):
            return 1
        elif(self.BaseLine==other.newLine1 and self.newLine1==other.BaseLine and self.newLine2==other.newLine2):
            return 1
        elif(self.BaseLine==other.newLine2 and self.newLine1==other.newLine1 and self.newLine2==other.BaseLine):
            return 1
        elif(self.BaseLine==other.newLine2 and self.newLine1==other.BaseLine and self.newLine2==other.newLine1):
            return 1
        else:
            return 0

# 数据读取 将数据组织到已经封装的点类 再用列表将所有点线性连接在一起 方便调用
def ReadDataTXT(Str_Path):
    point_list=[]
    with open(Str_Path) as f:
        for line in f:
            if (line==""):
                break
            str_list=[]
            str_list=line.split()
            if (str_list[4]=="False"):
                continue
            xyz = [float(str_list[1]),float(str_list[2]),float(str_list[3])]
            blh = tr.xyz2blh(xyz[0],xyz[1],xyz[2])
            blh = [blh[0] / glv.deg,blh[1] / glv.deg,blh[2]]
            point=Point(str_list[0],blh[0],blh[1],blh[2])
            point_list.append(point)
            str_list=[]
    return point_list
#
#  生成TIN三角网
#
# 查询数据边界
def XYMinMax(Point_List):
    xmax=EPSILON
    xmin=1/EPSILON
    ymax=EPSILON
    ymin=1/EPSILON
    for point in Point_List:
        if (point.X<xmin):
            xmin=point.X
        elif(point.X>xmax):
            xmax=point.X
        if(point.Y<ymin):
            ymin=point.Y
        elif(point.Y>ymax):
            ymax=point.Y
    return xmin,xmax,ymin,ymax
# 数学坐标系转到屏幕坐标系
# 上下个延伸10% 使屏幕有效率达到86% 数据边界不会丢失
def GaussToScreenCor(XYMinMax_List,Gx,Gy):
    dxmax=(XYMinMax_List[1]-XYMinMax_List[0])*1.2
    dymax=(XYMinMax_List[3]-XYMinMax_List[2])*1.2
    xscale=dxmax/800
    yscale=dymax/600
    Sx=int((Gx-XYMinMax_List[0]+dxmax*0.083)/xscale)
    Sy=int((XYMinMax_List[3]-Gy+dymax*0.083)/yscale)
    return Sx,Sy

# 解算右三角形余弦值
def Solve_Triangle_cos(Triangle):
    c=Triangle.BaseLine.BeginPoint.Cal_Distans(Triangle.BaseLine.EndPoint.X,Triangle.BaseLine.EndPoint.Y)
    b=Triangle.newLine1.EndPoint.Cal_Distans(Triangle.BaseLine.EndPoint.X,Triangle.BaseLine.EndPoint.Y)
    a=Triangle.newLine1.EndPoint.Cal_Distans(Triangle.BaseLine.BeginPoint.X,Triangle.BaseLine.BeginPoint.Y)
    cos=(a*a+b*b-c*c)/(2*a*b)
    return cos

# 与某点距离最近的点
def NearistPoint(Point,Point_list):
    d=1/EPSILON
    index=0
    for i in range(len(Point_list)):
        if(Point_list[i].PointName!=Point.PointName):
            if (Point.Cal_Distans(Point_list[i].X,Point_list[i].Y)<d):
                d=Point.Cal_Distans(Point_list[i].X,Point_list[i].Y)
                index=i
    return index
# 由基线生成三角形
def CreatTRI(Line,Point_List):
     cos=1.1
     cosmin=1.1
     index=''
     for i in range(len(Point_List)):
        if(Point_List[i].PointName==Line.BeginPoint.PointName or Point_List[i].PointName==Line.EndPoint.PointName):
            continue
        if(Judge_Right(Line,Point_List[i])):
            triangle=Triangle(Line.BeginPoint,Line.EndPoint,Point_List[i])
            cos=Solve_Triangle_cos(triangle)
            if(cos<cosmin):
                cosmin=cos
                index=i
     if(index!=''):
         return index

# 判断边是否添加重复，重复则删除并返回0
def Judge_Dup(Line_List):
    line1=Line_List[-1]
    for i in range(0,len(Line_List)-1):
        if(Line_List[i]==line1):
            return 1
# 判断寻找点是否在基线边右侧 是返回true (利用图形学平移旋转变化)
def Judge_Right(BaseLine,Point):
    dx=BaseLine.EndPoint.X-BaseLine.BeginPoint.X
    dy=BaseLine.EndPoint.Y-BaseLine.BeginPoint.Y
    d=math.sqrt(dx*dx+dy*dy)
    cos=dx/d
    sin=dy/d
    #旋转平移变换 三角形顺时针旋转基线方向与X正轴重合
    x=(Point.X-BaseLine.BeginPoint.X)*cos+(Point.Y-BaseLine.BeginPoint.Y)*sin
    y=-(Point.X-BaseLine.BeginPoint.X)*sin+(Point.Y-BaseLine.BeginPoint.Y)*cos
    if(y<0):
        return 1
# 添加边
def AddLine(LineList,BaseStack,line):
    LineList.append(line)
    if(Judge_Dup(LineList)):
        del LineList[-1]
        del BaseStack[-1]
    return LineList,BaseStack
def AddBaseStack(BaseStack,line):
    BaseStack.append(line)
    if(Judge_Dup(BaseStack)):
        del BaseStack[-1]
    return BaseStack
#添加三角形
def AddTriangle(Triangle_List,triangle):
    already=0
    for tri in Triangle_List:
        if(tri==triangle):
            already=1
    if (already==0):
        Triangle_List.append(triangle)
        #三角形存储后 在刚存进的三角形三边上记录该三角形的列表索引号
        Triangle_List[-1].BaseLine.Belonging_Triangle.append(len(Triangle_List)-1)
        Triangle_List[-1].newLine1.Belonging_Triangle.append(len(Triangle_List)-1)
        Triangle_List[-1].newLine2.Belonging_Triangle.append(len(Triangle_List)-1)
    return Triangle_List
# 建立边与三角形间的索引
def EdgeIndexTri(Triangle_List):
    for i in range(0,len(Triangle_List)):
        for j in range(0,len(Triangle_List)):
            if(i==j):
                continue
            else:
                if(Triangle_List[i].BaseLine==Triangle_List[j].BaseLine or Triangle_List[i].BaseLine==Triangle_List[
                    j].newLine1 or Triangle_List[i].BaseLine==Triangle_List[j].newLine2):
                    Triangle_List[i].BaseLine.Belonging_Triangle.append(j)
                if(Triangle_List[i].newLine1==Triangle_List[j].BaseLine or Triangle_List[i].newLine1==Triangle_List[
                    j].newLine1 or Triangle_List[i].newLine1==Triangle_List[j].newLine2):
                    Triangle_List[i].newLine1.Belonging_Triangle.append(j)
                if(Triangle_List[i].newLine2==Triangle_List[j].BaseLine or Triangle_List[i].newLine2==Triangle_List[
                    j].newLine1 or Triangle_List[i].newLine2==Triangle_List[j].newLine2):
                    Triangle_List[i].newLine2.Belonging_Triangle.append(j)
    return Triangle_List
# 生成TIN三角网
def CreatTIN(Point_List):
    point_list=Point_List # copy 一份 备用
    line_list=[] # 存放边的列表
    triangle_list=[] # 存放三角形的列表
    base_stack=[]
    basebegin=randint(0,len(point_list)-1)
    basend=NearistPoint(point_list[basebegin],point_list)
    line_list.append(Line(point_list[basebegin],point_list[basend]))
    base_stack.append(Line(point_list[basebegin],point_list[basend]))
    while(len(base_stack)):
        line=base_stack[-1]
        del base_stack[-1]
        index=CreatTRI(line,point_list)
        if(index==None):
            continue
        elif(index!=None):
            triangle=Triangle(line.BeginPoint,line.EndPoint,point_list[index])
            base_stack=AddBaseStack(base_stack,Line(line.BeginPoint,point_list[index]))
            base_stack=AddBaseStack(base_stack,Line(point_list[index],line.EndPoint))
            [line_list,base_stack]=AddLine(line_list,base_stack,Line(line.BeginPoint,point_list[index]))
            [line_list,base_stack]=AddLine(line_list,base_stack,Line(point_list[index],line.EndPoint))
            triangle_list=AddTriangle(triangle_list,triangle)
    Triangle_list=EdgeIndexTri(triangle_list)
    return line_list,Triangle_list

'''*******************窗体********************'''
# 生成一个窗体界面 命名为window
window=tk.Tk()
window.title('TIN')
window.geometry('1000x750')

# 在窗体上生成一块画布 用于绘制导线图
canvas = tk.Canvas(window,width=800,height=600,bg = 'white')
canvas.place(x=190,y=10)

# 画出数据点
def Draw_Point(Point_List):
    xyminmax=XYMinMax(Point_List)
    for point in Point_List:
        gxgy=GaussToScreenCor(xyminmax,point.X,point.Y)
        oval = canvas.create_oval(gxgy[0]-1, gxgy[1]-1, gxgy[0]+1, gxgy[1]+1)
        #canvas.create_text(gxgy[0]-13,gxgy[1],text=point.PointName)

# 画出TIN网
def Connect_Point(list1,list2,color):
    line = canvas.create_line(list1[0], list1[1],list2[0],list2[1],fill = color)
def Draw_TIN(Point_List,Line_List):
    xyminmax=XYMinMax(Point_List)
    for line in Line_List:
        gxgy1=GaussToScreenCor(xyminmax,line.BeginPoint.X,line.BeginPoint.Y)
        gxgy2=GaussToScreenCor(xyminmax,line.EndPoint.X,line.EndPoint.Y)
        oval = canvas.create_oval(gxgy1[0]-1, gxgy1[1]-1, gxgy1[0]+1, gxgy1[1]+1)
        ova2 = canvas.create_oval(gxgy1[0]-1, gxgy1[1]-1, gxgy1[0]+1, gxgy1[1]+1)
        Connect_Point(gxgy1,gxgy2,'black')

#********调试********
path=r"E:\1Master_2\Paper_Grid\crd\AUG_HK.crd"
point_list=ReadDataTXT(path)
Draw_Point(point_list)
Net=CreatTIN(point_list)
Draw_TIN(point_list,Net[0])
window.mainloop()
'''*******************所有代码在此之上********************'''