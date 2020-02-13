#!/usr/bin/python
# -*- coding: UTF-8 -*-
import numpy as np
import operator
from functools import reduce
def readFile(filepath):
    f = open(filepath, "r", encoding='UTF-8-sig')
    Alldata = f.readlines()
    Length = len(Alldata)
    Lables=Alldata[0].strip().split(',')
    data=[]
    for index in range(1,len(Alldata)):
        data.append(Alldata[index].strip())
    #data=Alldata[1:]
    # print()
    return Lables,data
def datedict(Lables,data):
    datedict={}
    dateList=[]
    for Len in data:
        List=Len.split(',')
        lable={}
        
        for index in range(0,len(List)):
            if index>3 and ( List[index]=='' or List[index]==None):
                lable[Lables[index]]='0'
            else:
                lable[Lables[index]]=List[index]
        if datedict.get(List[0])==None:
            datedict[List[0]]=[]
            datedict[List[0]].append(lable)
            dateList.append(List[0])
        else:
            datedict[List[0]].append(lable)
    return datedict,dateList

def prodict(datedict,dateList,Lables):
    prodicts={}
    provins={}
    for key in dateList:
        prodic={}
        for k in datedict.get(key):
            if prodic.get(k[Lables[2]])==None:
                prodic[k[Lables[2]]]=[]
                prodic[k[Lables[2]]].append(k)
            else:
                prodic[k[Lables[2]]].append(k)   
            if provins.get(k[Lables[2]])==None and k[Lables[1]]!='国外':
                 provins[k[Lables[2]]]=0
        prodicts[key]=prodic
    return  prodicts,list(provins.keys())
def computeDay(prodicts,proLists,Lables):
    dateList=list(prodicts.keys())
    compdics={}
    #省级每天核查错误数据
    perrdics={}
    #国家每天核查错误数据
    cerrdics={}
    for datekey in dateList:
        prolist=list(prodicts.get(datekey).keys())
        prodic=prodicts.get(datekey)
        prodic_1={}
        perrdics[datekey]=[]
        #存储某天各省累计信息
        stypesum={}
        for prokey in prolist:
            proArry=prodic.get(prokey)
            protype={}
            types=[]
            typesSum=[]
            for p in proArry:
                if protype.get(p.get(Lables[1]))==None:
                    types.append(p.get(Lables[1]))
                    typesSum.append(p.get(Lables[1])+"累计")
                    protype[p.get(Lables[1])]=[]
                    protype[p.get(Lables[1])].append(p)
                    protype[p.get(Lables[1])+"累计"]={}
                    protype[p.get(Lables[1])+"累计"][Lables[4]]=int(p.get(Lables[4]))
                    protype[p.get(Lables[1])+"累计"][Lables[5]]=int(p.get(Lables[5]))
                    protype[p.get(Lables[1])+"累计"][Lables[6]]=int(p.get(Lables[6]))
                    protype[p.get(Lables[1])+"累计"][Lables[7]]=int(p.get(Lables[7]))
                else:
                    protype[p.get(Lables[1])].append(p)
                    protype[p.get(Lables[1])+"累计"][Lables[4]]+=int(p.get(Lables[4]))
                    protype[p.get(Lables[1])+"累计"][Lables[5]]+=int(p.get(Lables[5]))
                    protype[p.get(Lables[1])+"累计"][Lables[6]]+=int(p.get(Lables[6]))
                    protype[p.get(Lables[1])+"累计"][Lables[7]]+=int(p.get(Lables[7]))
            prodic_1[prokey]=protype
            #========将每个省当天datekey省级与地区的数据放入数组中
            ss=[]
            for i in range(0,len(typesSum)):
                ss.append({typesSum[i] : protype.get(typesSum[i])})
            stypesum[prokey]=ss
            #print(stypesum)
            #====================================================

            #复核每个省每天的数据============================
            if len(types)>1:
               if protype.get(typesSum[0])[Lables[4]]!=protype.get(typesSum[1])[Lables[4]]:
                   perrdics[datekey].append({prokey : {typesSum[0] : protype.get(typesSum[0]), typesSum[1] : protype.get(typesSum[1])}})
               elif protype.get(typesSum[0])[Lables[5]]!=protype.get(typesSum[1])[Lables[5]]:
                    perrdics[datekey].append({prokey : {typesSum[0] : protype.get(typesSum[0]), typesSum[1] : protype.get(typesSum[1])}})
               elif  protype.get(typesSum[0])[Lables[6]]!=protype.get(typesSum[1])[Lables[6]]:
                    perrdics[datekey].append({prokey : {typesSum[0] : protype.get(typesSum[0]), typesSum[1] : protype.get(typesSum[1])}})    
            #===================================================
            #print(types,typesSum)
            #break
        #print(stypesum)
        #===========复核每天各省和全国=====================
        prosum={Lables[4]:0,Lables[5]:0,Lables[6]:0,Lables[7]:0}
        csum=None
        for pro in proLists:
            if pro == '':
                csum = stypesum.get(pro)[0].get('国家级累计')
            if pro !=None or pro != '':
                for p in stypesum.get(pro):
                    d=p.get('省级累计')
                    #print(p)
                    if d!=None:
                        prosum[Lables[4]]+=d[Lables[4]]
                        prosum[Lables[5]] += d[Lables[5]]
                        prosum[Lables[6]] += d[Lables[6]]
                        prosum[Lables[7]] += d[Lables[7]]
        #print(prosum,csum)
        cerrdics[datekey]=[]
        if (prosum[Lables[4]]+prosum[Lables[7]])!=(csum[Lables[4]]+csum[Lables[7]]):
            cerrdics[datekey].append({'省级累计':{Lables[4]:prosum[Lables[4]]+prosum[Lables[7]]},
                               '国家级累计':{Lables[4]:csum[Lables[4]]+csum[Lables[7]]}})
        if prosum[Lables[5]]!=csum[Lables[5]]:
            cerrdics[datekey].append({'省级累计':{Lables[5]:prosum[Lables[5]]},
                               '国家级累计':{Lables[5]:csum[Lables[5]]}})
        if prosum[Lables[6]]!=csum[Lables[6]]:
            cerrdics[datekey].append({'省级累计':{Lables[6]:prosum[Lables[6]]},
                               '国家级累计':{Lables[6]:csum[Lables[6]]}})
        #break
        #===================================================


        #存储每天所有数据
        compdics[datekey]=prodic_1
        #break
    print(perrdics)
    print(cerrdics)
    return compdics

if __name__=='__main__':
    Lables,data=readFile('2_map.csv')
    datedict,dateList=datedict(Lables,data)
    prodicts,proList=prodict(datedict,dateList,Lables)
    computeDay(prodicts,proList,Lables)
    
