#!/usr/bin/python
# -*- coding: UTF-8 -*-
import numpy as np
import operator
from functools import reduce
from datetime import datetime
import time
import re
def readFile(filepath):
    f = open(filepath, "r", encoding='UTF-8-sig')
    Alldata = f.readlines()
    Length = len(Alldata)
    # print()
    Lables = re.split(',|\\t',Alldata[0].strip())
    data = []
    for index in range(1, len(Alldata)):
        data.append(Alldata[index].strip())
    # data=Alldata[1:]
    # print()
    #Lables为字段名，根据不同字段的位置可以直接修改Lables数组的标号
    return Lables, data


def datedict(Lables, data):
    datedict = {}
    dateList = []
    for Len in data:
        List =re.split(',|\\t',Len)
        lable = {}
        for index in range(0, len(List)):
            if index==0:
                if '-' in List[index]:
                    t=List[index].split(' ')[0].split('-')
                    #
                    List[index]=t[0]+'/'+str(int(t[1]))+'/'+str(int(t[2]))+' 00:00'
            List[index]=List[index].replace('\u3000','')
            if index > 3 and (List[index] == '' or List[index] == None):
                lable[Lables[index]] = '0'
            else:
                lable[Lables[index]] = List[index].replace('.0','')
        if datedict.get(List[0]) == None:
            datedict[List[0]] = []
            datedict[List[0]].append(lable)
            dateList.append(List[0])
        else:
            datedict[List[0]].append(lable)
    return datedict, dateList


def prodict(datedict, dateList, Lables):
    prodicts = {}
    provins = {}
    for key in dateList:
        prodic = {}
        for k in datedict.get(key):
            #print(k)
            #通过正则表达式获取每个省的简称
            k[Lables[2]]=re.split('省|市|(回族)*自治区|特别行政区', k[Lables[2]])[0]
            if prodic.get(k[Lables[2]]) == None:
                prodic[k[Lables[2]]] = []
                prodic[k[Lables[2]]].append(k)
            else:
                prodic[k[Lables[2]]].append(k)
            if provins.get(k[Lables[2]]) == None and k[Lables[1]] != '国外':
                provins[k[Lables[2]]] = 0
        prodicts[key] = prodic
    return prodicts, list(provins.keys())

#每天的地区和省，以及每天的各省和全国的新增是否相等
def computeDay(prodicts, proLists, Lables):
    dateList = list(prodicts.keys())
    compdics = {}
    # 省级每天核查错误数据
    perrdics = {}
    # 国家每天核查错误数据
    cerrdics = {}
    for datekey in dateList:
        prolist = list(prodicts.get(datekey).keys())
        prodic = prodicts.get(datekey)
        prodic_1 = {}
        perrdics[datekey] = []
        # 存储某天各省累计信息
        stypesum = {}
        for prokey in prolist:
            proArry = prodic.get(prokey)
            protype = {}
            types = []
            typesSum = []
            for p in proArry:
                if protype.get(p.get(Lables[1])) == None:
                    types.append(p.get(Lables[1]))
                    typesSum.append(p.get(Lables[1]) + "累计")
                    protype[p.get(Lables[1])] = []
                    protype[p.get(Lables[1])].append(p)
                    protype[p.get(Lables[1]) + "累计"] = {}
                    protype[p.get(Lables[1]) + "累计"][Lables[4]] = int(p.get(Lables[4]))
                    protype[p.get(Lables[1]) + "累计"][Lables[5]] = int(p.get(Lables[5]))
                    #print(Lables[7])
                    protype[p.get(Lables[1]) + "累计"][Lables[6]] = int(p.get(Lables[6]))
                    protype[p.get(Lables[1]) + "累计"][Lables[7]] = int(p.get(Lables[7]))
                else:
                    protype[p.get(Lables[1])].append(p)
                    protype[p.get(Lables[1]) + "累计"][Lables[4]] += int(p.get(Lables[4]))
                    protype[p.get(Lables[1]) + "累计"][Lables[5]] += int(p.get(Lables[5]))
                    protype[p.get(Lables[1]) + "累计"][Lables[6]] += int(p.get(Lables[6]))
                    protype[p.get(Lables[1]) + "累计"][Lables[7]] += int(p.get(Lables[7]))
            prodic_1[prokey] = protype
            # ========将每个省当天datekey省级与地区的数据放入数组中
            ss = []
            for i in range(0, len(typesSum)):
                ss.append({typesSum[i]: protype.get(typesSum[i])})
            stypesum[prokey] = ss
            # print(stypesum)
            # ====================================================

            # 复核每个省每天的数据============================
            if len(types) > 1:
                if protype.get(typesSum[0])[Lables[4]] !=\
                        protype.get(typesSum[1])[Lables[4]]:
                    perrdics[datekey].append(
                        {prokey: {typesSum[0]: {Lables[4]:protype.get(typesSum[0])[Lables[4]]},
                                  typesSum[1]: {Lables[4]:protype.get(typesSum[1])[Lables[4]]}}})
                if protype.get(typesSum[0])[Lables[5]] != protype.get(typesSum[1])[Lables[5]]:
                    perrdics[datekey].append(
                        {prokey: {typesSum[0]:{Lables[5]: protype.get(typesSum[0])[Lables[5]]},
                                  typesSum[1]: {Lables[5]:protype.get(typesSum[1])[Lables[5]]}}})
                if protype.get(typesSum[0])[Lables[6]] != protype.get(typesSum[1])[Lables[6]]:
                    perrdics[datekey].append(
                        {prokey: {typesSum[0]: {Lables[6]:protype.get(typesSum[0])[Lables[6]]},
                                  typesSum[1]: {Lables[6]:protype.get(typesSum[1])[Lables[6]]}}})
                    # ===================================================
            # print(types,typesSum)
            # break
        # print(stypesum)
        # ===========复核每天各省和全国=====================
        prosum = {Lables[4]: 0, Lables[5]: 0, Lables[6]: 0, Lables[7]: 0}
        csum = None
        for pro in proLists:
            if pro == '':
                #print(pro,datekey,stypesum.get(pro))
                if stypesum.get(pro)==None:
                    csum={'新增确诊病例': 0, '新增治愈出院数': 0, '新增死亡数': 0, '核减': 0,'国家缺少':0}
                else:
                    csum = stypesum.get(pro)[0].get('国家级累计')
            elif pro != None or pro != '':
                #print(stypesum.get(pro),pro,datekey)
                if stypesum.get(pro)==None:
                    continue
                for p in stypesum.get(pro):

                    d = p.get('省级累计')
                    # print(p)
                    if d != None:
                        prosum[Lables[4]] += d[Lables[4]]
                        prosum[Lables[5]] += d[Lables[5]]
                        prosum[Lables[6]] += d[Lables[6]]
                        prosum[Lables[7]] += d[Lables[7]]
        # print(prosum,csum)
        cerrdics[datekey] = []
        if (prosum[Lables[4]] ) != (csum[Lables[4]]):
            if csum.get('国家缺少')!=None:
                cerrdics[datekey].append({Lables[4]: {'省级累计': prosum[Lables[4]], '国家级累计': '统计缺失'}})
            else:
                cerrdics[datekey].append({Lables[4]:{'省级累计': prosum[Lables[4]], '国家级累计':  csum[Lables[4]] }})
        if prosum[Lables[5]] != csum[Lables[5]]:
            if csum.get('国家缺少') != None:
                cerrdics[datekey].append({Lables[5]: {'省级累计': prosum[Lables[5]],
                                                      '国家级累计': '统计缺失'}})
            else:
                cerrdics[datekey].append({Lables[5]:{'省级累计':  prosum[Lables[5]],
                                      '国家级累计':  csum[Lables[5]]}})
        if prosum[Lables[6]] != csum[Lables[6]]:
            if csum.get('国家缺少') != None:
                cerrdics[datekey].append({Lables[6]: {'省级累计': prosum[Lables[6]],
                                                      '国家级累计': '统计缺失'}})
            else:
                cerrdics[datekey].append({Lables[6]:{'省级累计': prosum[Lables[6]],
                                      '国家级累计': csum[Lables[6]]}})
        # break
        # ===================================================

        # 存储每天所有数据
        compdics[datekey] = prodic_1
        # break
    # print(perrdics)
    # print(cerrdics)
    return perrdics,cerrdics,compdics

#计算当前某天前面所有天的累加值
def computedS(dateList,compdics,proList,Lables):
    proDic={}
    for pk in proList:
        proDic[pk]=[]
    for datekey in dateList:
        prokeys=list(compdics.get(datekey).keys())
        for pk in prokeys:
            proDic.get(pk).append({datekey:compdics.get(datekey).get(pk)})
    err=[]
    for pk in proList:
        if pk=='':
            continue
        #print(proDic.get(pk))
        index=0
        #last保存前面所有日期的省级累加值
        last={Lables[4]:0,Lables[5]:0,Lables[6]:0}
        #lastnow保存前面最新的卫健委累计数据
        lastnow={Lables[8]:0,Lables[9]:0,Lables[10]:0}
        for d in proDic.get(pk):
            d.get(list(d.keys())[0]).get('省级')
            now={Lables[8]:0,Lables[9]:0,Lables[10]:0}
            if d.get(list(d.keys())[0]).get('省级')==None:
                t=datekey.split(' ')[0].split('/')
                #print(t)
                #nowdate=t[0]+'/'+str(int(t[1]))+'/'+str(int(t[2])+1)+' 00:00'
                nowdate=t[0]
                err.append({pk: {nowdate: {'省级':'缺失'}}})
                continue
            for k in d.get(list(d.keys())[0]).get('省级'):
                datekey=k[Lables[0]]
                last[Lables[4]]+=(int(k.get(Lables[4]))+int(k.get(Lables[7])))
                last[Lables[5]] += int(k.get(Lables[5]))
                last[Lables[6]] += int(k.get(Lables[6]))
                now[Lables[8]]+=int(k.get(Lables[8]))
                now[Lables[9]]+= int(k.get(Lables[9]))
                now[Lables[10]]+= int(k.get(Lables[10]))
            #保存第一天的累计
            if index == 0:
                lastnow=nowTolastnow(lastnow,now,Lables)
                index+=1
            #if pk=='广东':
                #print(now,Lables[8],last,Lables[4])
            #当当前累计值不为0时候核查否则就用lastnow的核查
            if last.get(Lables[4])!=now.get(Lables[8]):
                if now.get(Lables[8])!=0:
                    err.append({pk:{datekey:{Lables[4]:last.get(Lables[4]),Lables[8]:now.get(Lables[8])}}})
                else:
                    if last.get(Lables[4]) != lastnow.get(Lables[8]):
                        err.append({pk: {datekey: {Lables[4]: last.get(Lables[4]), Lables[8]: lastnow.get(Lables[8])}}})
            if last.get(Lables[5])!=now.get(Lables[9]):
                if  now.get(Lables[9])!=0:
                    err.append({pk: {datekey: {Lables[5]: last.get(Lables[5]), Lables[9]: now.get(Lables[9])}}})
                else:
                    if last.get(Lables[5])!=lastnow.get(Lables[9]):
                        err.append({pk: {datekey: {Lables[5]: last.get(Lables[5]), Lables[9]: lastnow.get(Lables[9])}}})
            if last.get(Lables[6])!=now.get(Lables[10]):
                if now.get(Lables[10])!=0:
                    err.append({pk: {datekey: {Lables[6]: last.get(Lables[6]), Lables[10]: now.get(Lables[10])}}})
                else:
                    if last.get(Lables[6])!=lastnow.get(Lables[10]):
                        err.append({pk: {datekey: {Lables[6]: last.get(Lables[6]), Lables[10]: lastnow.get(Lables[10])}}})
            if now.get(Lables[8])!=0 :
                lastnow[Lables[8]]=now.get(Lables[8])
            if now.get(Lables[9])!=0 :
                lastnow[Lables[9]] = now.get(Lables[9])
            if now.get(Lables[10])!=0:
                lastnow[Lables[10]] = now.get(Lables[10])
        #print(err)
        #break
    return err
def nowTolastnow(lastnow,now,Lables):
    lastnow[Lables[8]] = now[Lables[8]]
    lastnow[Lables[9]] = now[Lables[9]]
    lastnow[Lables[10]] = now[Lables[10]]
    return lastnow

def write1(filename,perrdics,dateList):
    fp = open(filename, "a+", encoding="utf-8")
    fp.write('------------------不符合规则省级复核，每天地区新增和 == 省级新增-----------------\n')

    for datekey in dateList:
        wstr = '';
        if len(perrdics.get(datekey))!=0:
            for index in range(0,len(perrdics.get(datekey))):
                prodic=perrdics.get(datekey)[index]
                pro=list(prodic.keys())[0]
                #print(prodic.get(pro))
                prodic.get(pro)['地区级累计']
                type=list(prodic.get(pro)['地区级累计'].keys())[0]
                wstr = pro + ',' + datekey + ',地区级'+type+'累加值为' + str(prodic.get(pro)['地区级累计'].get(type)) + ',' \
                           + '省级新增' + str(prodic.get(pro)['省级累计'].get(type))
                #print(wstr)
                fp.write(wstr+'\n')
    fp.write('\n')
    fp.close()
def write2(filename,err):
    fp = open(filename, "a+", encoding="utf-8")
    fp.write('------------------不符合规则省级复核，省级所有日期累计值 == 卫健委发布的累计值----------------\n')
    for pk in err:
        pro=list(pk.keys())[0]
        dates=list(pk.get(pro).keys())[0]
        g=dates.split('月')

        g[1]=g[1].split('日')[0]
        # print(g)
        if int(g[0])<2:
            continue
        elif int(g[0])>=2 and int(g[1])<13:
            continue
        s=pk.get(pro).get(dates)
        wstr=''
        if s.get('省级')!=None:
            wstr=pro+','+dates+',省级数据缺失'
        else:
            if  '确诊'in list(s.keys())[0]:
                wstr=pro+','+str(dates)+',前面所有日期加当前累计'+list(s.keys())[0]+'值'+str(s.get(list(s.keys())[0]))+\
                     ',卫健委'+list(s.keys())[1]+str(s.get(list(s.keys())[1]))
                fp.write(wstr+'\n')
    fp.write('\n')
    fp.close()

def write3(filename,cerrdics,dateList):
    fp = open(filename, "a+", encoding="utf-8")
    fp.write('------------------不符合规则全国级复核：每天新增 省级累积==全国累积-----------------\n')
    for datekey in dateList:
        wstr = '';
        if len(cerrdics.get(datekey))!=0:
            for index in range(0,len(cerrdics.get(datekey))):
                prodic=cerrdics.get(datekey)[index]
                type=list(prodic.keys())[0]
                wstr = datekey + ',各省当天'+type+'累加值为' + str(prodic.get(type).get('省级累计')) + ',' \
                            + '国家当天新增' + str(prodic.get(type).get('国家级累计'))
                #print(wstr)
                fp.write(wstr+'\n')
    fp.write('\n')
    fp.close()
def writeCSV(filename,err):
    fp = open(filename, "a+", encoding="utf-8-sig")
    fp.write('公开时间,省份,累计确诊,卫健委累计确诊,是否一致,累计出院,卫健委累计出院,是否一致,累计死亡,卫健委累计死亡,是否一致\n')
    for pk in err:
        pro=list(pk.keys())[0]
        dates=list(pk.get(pro).keys())[0]
        s=pk.get(pro).get(dates)
        wstr=''
        #wk={'累计确诊'}
        wstr = dates + ',' + pro
        if s.get('省级')!=None:
            wstr+=',,,否,,,否,,,否'
        else:
            if list(s.keys())[0]=='新增确诊病例':
                wstr+=','+str(s.get(list(s.keys())[0]))+','+str(s.get(list(s.keys())[1]))+',否'
            else:
                wstr+=',0,0,是'
            if list(s.keys())[0]=='新增治愈出院数':
                wstr+=','+str(s.get(list(s.keys())[0]))+','+str(s.get(list(s.keys())[1]))+',否'
            else:
                wstr+=',0,0,是'
            if list(s.keys())[0]=='新增死亡数':
                wstr += ',' + str(s.get(list(s.keys())[0])) + ',' + str(s.get(list(s.keys())[1])) + ',否'
            else:
                wstr += ',0,0,是'
        fp.write(wstr+'\n')
    return None
if __name__ == '__main__':
    filename='MergeData_20200214(6).csv'
    Lables, data = readFile(filename)
    #print(Lables)
    datedict, dateList = datedict(Lables, data)
    #print(dateList)
    prodicts, proList = prodict(datedict, dateList, Lables)
    print(proList)
    perrdics,cerrdics,compdics=computeDay(prodicts, proList, Lables)
    err=computedS(dateList, compdics, proList, Lables)
    # #print(err)
    filename=filename.split('.')[0]+'ErrorReport'+time.strftime("%Y%m%d_%H-%M-%S",time.localtime(time.time()))+'.log'
    write1(filename, perrdics, dateList)
    write2(filename, err)
    write3(filename, cerrdics, dateList)
    filename=filename.replace('.log','.csv')
    print(err)
    writeCSV(filename, err)

