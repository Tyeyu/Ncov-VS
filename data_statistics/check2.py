import csv
import pandas as pd
import datetime
import numpy as np
import tkinter as tk
from tkinter import filedialog
import sys

file_name=sys.argv[1]
# root = tk.Tk()
# root.withdraw()
# file_name = filedialog.askopenfilename()
csv_data = pd.read_csv(file_name,keep_default_na=False)
time_dict={}
postion_dict={}
country_dict={}
cumulative_dict={}
new_day=csv_data['公开时间'][len(csv_data)-1]
#print(new_day)
for e_row in range(0,len(csv_data)):
    #print(e_row)
    a=csv_data['公开时间'][e_row]
    b=csv_data['类别'][e_row]
    c=csv_data['省份'][e_row]
    d=csv_data['城市'][e_row]
    if (csv_data['新增确诊病例'][e_row] != ''):
        e=int(csv_data['新增确诊病例'][e_row])
    else:
        e=0
    if (csv_data['新增治愈出院数'][e_row] != ''):
        f=int(csv_data['新增治愈出院数'][e_row])
    else:
        f=0
    if (csv_data['新增死亡数'][e_row] != ''):
        #print(csv_data['新增死亡数'][e_row])
        g=int(csv_data['新增死亡数'][e_row])
    else:
        g=0
    if (csv_data['核减'][e_row] != ''):
        h=int(csv_data['核减'][e_row])
    else:
        h=0
    e_cumulative=[0,0,0,0]
    if csv_data['累计确诊人数'][e_row]!='':
        e_cumulative[0]=int(csv_data['累计确诊人数'][e_row])
    if csv_data['累计治愈人数'][e_row]!='':
        e_cumulative[1]=int(csv_data['累计治愈人数'][e_row])
    if csv_data['累计死亡人数'][e_row]!='':
        e_cumulative[2]=int(csv_data['累计死亡人数'][e_row])
    if csv_data['累计核减人数'][e_row]!='':
        e_cumulative[3]=int(csv_data['累计核减人数'][e_row])
    # if csv_data['省份'][e_row]=='北京':
    #     print(h)
    if(b==''):
        continue
    if(h==''):
        h=0

    if ((b == '国家级' or b == '省级') and (c != '香港' and c != '澳门' and c != '台湾')):
        e_time = a
        if (e_time not in country_dict):
            country_dict[e_time] = {}
            country_dict[e_time]['省级总和'] = [0, 0, 0]
        if (b == '国家级'):
            country_dict[e_time]['国家级'] = [0, 0, 0]
            if (e != ''):
                country_dict[e_time]['国家级'][0] = e + h
            if (f != ''):
                country_dict[e_time]['国家级'][1] = f
            if (g != ''):
                country_dict[e_time]['国家级'][2] = g
        elif (b == '省级'):
            country_dict[e_time][c] = [0, 0, 0]
            if (e != ''):
                country_dict[e_time][c][0] = e + h
            if (f != ''):
                country_dict[e_time][c][1] = f
            if (g != ''):
                country_dict[e_time][c][2] = g

            if (e != ''):
                country_dict[e_time]['省级总和'][0] += (e + h)
            if (f != ''):
                country_dict[e_time]['省级总和'][1] += f
            if (g != ''):
                country_dict[e_time]['省级总和'][2] += g

    if ((b == '地区级' or b == '省级') and (c != '香港' and c != '澳门' and c != '台湾')):
        e_time = a
        if (e_time not in time_dict):
            time_dict[e_time] = {}
        if (c not in time_dict[e_time]):
            time_dict[e_time][c] = [0, 0, 0, 0, 0, 0, 0, 0]
        if (b == '地区级'):
            if (e != ''):
                #print(e)
                time_dict[e_time][c][0] += e
            if (f != ''):
                time_dict[e_time][c][1] += f
            if (g != ''):
                time_dict[e_time][c][2] += g
            if  (h!=''):
                time_dict[e_time][c][3] += h
        elif (b == '省级'):
            if (e != ''):
                time_dict[e_time][c][4] = e
            if (f != ''):
                time_dict[e_time][c][5] = f
            if (g != ''):
                time_dict[e_time][c][6] = g
            if  (h!=''):
                time_dict[e_time][c][7] = h
        if (c not in postion_dict):
            postion_dict[c] = [0, 0, 0, 0, 0, 0, 0]  # 后一位是省的核减和
        if (b == '地区级'):
            if (e != ''):
                postion_dict[c][0] += e  # 总新增
            if (f != ''):
                postion_dict[c][1] += f
            if (g != ''):
                postion_dict[c][2] += g
        elif (b == '省级'):  # 总新增
            if (e != ''):
                postion_dict[c][3] += e
            if (f != ''):
                postion_dict[c][4] += f
            if (g != ''):
                postion_dict[c][5] += g
            postion_dict[c][6] += h
    if ((b == '省级') and (c != '香港' and c != '澳门' and c != '台湾')):
        if (c not in cumulative_dict):
            cumulative_dict[c] = {}
        if (a not in cumulative_dict[c]):
            cumulative_dict[c][a] = [0, 0, 0, 0, 0, 0, 0, 0]

        if (e != ''):
            cumulative_dict[c][a][0] = e
        if (f != ''):
            cumulative_dict[c][a][1] = f
        if (g != ''):
            cumulative_dict[c][a][2] = g
        if  (h!=''):
            cumulative_dict[c][a][3] = h
        if (e != ''):
            cumulative_dict[c][a][4] = e_cumulative[0]
        if (f != ''):
            cumulative_dict[c][a][5] = e_cumulative[1]
        if (g != ''):
            cumulative_dict[c][a][6] = e_cumulative[2]
        if  (h!=''):
            cumulative_dict[c][a][7] = e_cumulative[3]
#print(cumulative_dict)
# print(country_dict)
# print(time_dict)
# print(postion_dict)
name=datetime.datetime.now()
txt_name='acummulatedValueCheckResult_'+str(name.month)+'月'+str(name.day)+'日'+str(name.hour)+'时'+str(name.minute)+'分.log'
f1 = open(txt_name,'w')

f1.write("------------------省级复核，每天地区新增和 == 省级新增-----------------\n")
time_keys=list(time_dict.keys())
for i in range(0,len(time_dict)):
    ShengFen=list(time_dict[time_keys[i]].keys())
    for j in range(0,len(time_dict[time_keys[i]])):
        a=time_dict[time_keys[i]][ShengFen[j]]
        if ShengFen[j]==None:
                ShengFen[j]='无数据'
        if a[0]!=a[4]:
                error_inf=ShengFen[j]+','+time_keys[i]+',地区新增确诊病例累加值为'+str(int(a[0]))+',省级新增'+str(int(a[4]))
                f1.write(error_inf)
                f1.write('\n')
        if a[1]!=a[5]:
                error_inf = ShengFen[j] + ',' + time_keys[i] + ',地区新增治愈出院数累加值为' + str(int(a[1])) + ',省级新增' + str(int(a[5]))
                f1.write(error_inf)
                f1.write('\n')
        if a[2] != a[6]:
                error_inf = ShengFen[j] + ',' + time_keys[i] + ',地区新增死亡数累加值为' + str(int(a[2])) + ',省级新增' + str(int(a[6]))
                f1.write(error_inf)
                f1.write('\n')
        if a[3] != a[7]:
                error_inf = ShengFen[j] + ',' + time_keys[i] + ',地区新增核减累加值为' + str(int(a[3])) + ',省级新增' + str(int(a[7]))
                f1.write(error_inf)
                f1.write('\n')
f1.write("------------------省级复核，省级所有日期累计值 == 卫健委发布的累计值----------------\n")
cumulative_keys=list(cumulative_dict.keys())
for i in range(0,len(cumulative_dict)):
    cu_time=list(cumulative_dict[cumulative_keys[i]].keys())
    for j in range(0, len(cumulative_dict[cumulative_keys[i]])):
        a=cumulative_dict[cumulative_keys[i]][cu_time[j]]
        dd = cu_time[j]
        dd = datetime.datetime.strptime(dd, "%m月%d日")
        if cu_time[j]=='1月10日':
            if a[0]!=a[4]:
                error_inf=cumulative_keys[i]+',日期:'+cu_time[j]+',确诊累计值'+str(int(a[0]))+',卫健委累计值'+str(int(a[4]))
                f1.write(error_inf)
                f1.write('\n')
            if a[1]!=a[5]:
                error_inf=cumulative_keys[i]+',日期:'+cu_time[j]+',出院累计值'+str(int(a[1]))+',卫健委累计值'+str(int(a[5]))
                f1.write(error_inf)
                f1.write('\n')
            if a[2]!=a[6]:
                error_inf=cumulative_keys[i]+',日期:'+cu_time[j]+',死亡累计值'+str(int(a[2]))+',卫健委累计值'+str(int(a[6]))
                f1.write(error_inf)
                f1.write('\n')
        elif cu_time[j]=='2月1日':
            b=cumulative_dict[cumulative_keys[i]]['1月31日']
            if a[0]+b[4]-a[3]!=a[4]:
                error_inf=cumulative_keys[i]+',日期:'+cu_time[j]+',确诊累计值'+str(int(a[0]+b[4]-a[3]))+',卫健委累计值'+str(int(a[4]))
                f1.write(error_inf)
                f1.write('\n')
            if a[1]!=a[5]:
                error_inf=cumulative_keys[i]+',日期:'+cu_time[j]+',出院累计值'+str(int(a[1]))+',卫健委累计值'+str(int(a[5]))
                f1.write(error_inf)
                f1.write('\n')
            if a[2]!=a[6]:
                error_inf=cumulative_keys[i]+',日期:'+cu_time[j]+',死亡累计值'+str(int(a[2]))+',卫健委累计值'+str(int(a[6]))
                f1.write(error_inf)
                f1.write('\n')
        else:
            aa=str(dd.month)+'月'+str(dd.day-1)+'日'
            b = cumulative_dict[cumulative_keys[i]][aa]
            if a[0]+b[4]-a[3]!=a[4]:
                error_inf=cumulative_keys[i]+',日期:'+cu_time[j]+',确诊累计值'+str(int(a[0]+b[4]-a[3]))+',卫健委累计值'+str(int(a[4]))
                f1.write(error_inf)
                f1.write('\n')
            if a[1]!=a[5]:
                error_inf=cumulative_keys[i]+',日期:'+cu_time[j]+',出院累计值'+str(int(a[1]))+',卫健委累计值'+str(int(a[5]))
                f1.write(error_inf)
                f1.write('\n')
            if a[2]!=a[6]:
                error_inf=cumulative_keys[i]+',日期:'+cu_time[j]+',死亡累计值'+str(int(a[2]))+',卫健委累计值'+str(int(a[6]))
                f1.write(error_inf)
                f1.write('\n')
f1.write("------------------全国级复核：省级累积==全国累积-----------------\n")
country_keys=list(country_dict.keys())
for i in range(0,len(country_dict)):
    a=country_dict[country_keys[i]]
    #print(country_keys[i])
    if '国家级' not in list(a.keys()):
        error_inf = country_keys[i] + '没有统计国家数据'
        f1.write(error_inf)
        f1.write('\n')
        continue
    if a['国家级'][0]!=a['省级总和'][0]:
        error_inf = country_keys[i] + ',各省新增确诊病例累积' + str(int(a['省级总和'][0])) + ',国家级新增' + str(int(a['国家级'][0]))
        f1.write(error_inf)
        f1.write('\n')
    if a['国家级'][1]!=a['省级总和'][1]:
        error_inf = country_keys[i] + ',各省新增治愈出院数累积' + str(int(a['省级总和'][1])) + ',国家级新增' + str(int(a['国家级'][1]))
        f1.write(error_inf)
        f1.write('\n')
    if a['国家级'][2]!=a['省级总和'][2]:
        error_inf = country_keys[i] + ',各省新增死亡数累积' + str(int(a['省级总和'][2])) + ',国家级新增' + str(int(a['国家级'][2]))
        f1.write(error_inf)
        f1.write('\n')
f1.close()
#生成csv文件
name=datetime.datetime.now()
txt_name='acummulatedValueCheckResult_'+str(name.month)+'月'+str(name.day)+'日'+str(name.hour)+'时'+str(name.minute)+'分'
origin_data=[]
e_row=['确诊时间','省份','累计确诊','卫健委累计确诊','是否一致','累计出院','卫健委累计出院','是否一致','累计死亡','卫健委累计死亡','是否一致']
origin_data.append(e_row)
cumulative_key=list(cumulative_dict.keys())
for i in range(0,len(postion_dict)):
    cu_time = list(cumulative_dict[cumulative_keys[i]].keys())
    for j in range(0, len(cumulative_dict[cumulative_keys[i]])):
        a=cumulative_dict[cumulative_keys[i]][cu_time[j]]
        dd = cu_time[j]
        dd = datetime.datetime.strptime(dd, "%m月%d日")
        e_row=[]
        e_row.append(cu_time[j])
        e_row.append(cumulative_key[i])
        if cu_time[j] == '1月10日':
            e_row.append(str(int(a[0])))
            e_row.append(str(int(a[4])))
            if a[0] != a[4]:
                e_row.append('否')
            else:
                e_row.append('是')
        elif cu_time[j] == '2月1日':
            b = cumulative_dict[cumulative_keys[i]]['1月31日']
            e_row.append(str(int(a[0] + b[4] - a[3])))
            e_row.append(str(int(a[4])))
            if (a[0]+b[4]-a[3])!=a[4]:
                e_row.append('否')
            else:
                e_row.append('是')
        else:
            aa=str(dd.month)+'月'+str(dd.day-1)+'日'
            b = cumulative_dict[cumulative_keys[i]][aa]
            e_row.append(str(int(a[0] + b[4] - a[3])))
            e_row.append(str(int(a[4])))
            if (a[0]+b[4]-a[3])!=a[4]:
                e_row.append('否')
            else:
                e_row.append('是')
        a.append(str(int(a[1])))
        a.append(str(int(a[5])))
        if a[1]!=a[5]:
            e_row.append('否')
        else:
            e_row.append('是')
        e_row.append(str(int(a[2])))
        e_row.append(str(int(a[6])))
        if a[2]!=a[6]:
            e_row.append('否')
        else:
            e_row.append('是')
        origin_data.append(e_row)
with open(txt_name+".csv", "a+", newline='',encoding='utf-8-sig') as csvfile:
    writer  = csv.writer(csvfile)
    for row in origin_data:
        writer.writerow(row)
csvfile.close()
print('done')
