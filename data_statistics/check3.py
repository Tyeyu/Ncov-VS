import csv
import datetime
import pandas as pd
import numpy as np
import tkinter as tk
from tkinter import filedialog
file_name='map.csv'
root = tk.Tk()
root.withdraw()
file_name = filedialog.askopenfilename()
csv_data = pd.read_csv(file_name,keep_default_na=False)
time_dict={}
postion_dict={}
country_dict={}
new_day=csv_data['公开时间'][len(csv_data)-1]
print(new_day)
for e_row in range(0,len(csv_data)):
    print(e_row)
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
    ab=[0,0,0]
    if (csv_data['累积确诊'][e_row] != ''):
        ab[0]=int(csv_data['累积确诊'][e_row])
    if(csv_data['累积出院'][e_row] != ''):
        ab[1] = int(csv_data['累积出院'][e_row])
    if(csv_data['累积死亡'][e_row] != ''):
        ab[2] = int(csv_data['累积死亡'][e_row])

    if csv_data['省份'][e_row]=='北京':
        print(ab)
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
            time_dict[e_time][c] = [0, 0, 0, 0, 0, 0]
        if (b == '地区级'):
            if (e != ''):
                #print(e)
                time_dict[e_time][c][0] += e
            if (f != ''):
                time_dict[e_time][c][1] += f
            if (g != ''):
                time_dict[e_time][c][2] += g
        elif (b == '省级'):
            if (e != ''):
                time_dict[e_time][c][3] = e
            if (f != ''):
                time_dict[e_time][c][4] = f
            if (g != ''):
                time_dict[e_time][c][5] = g

        if (c not in postion_dict):
            postion_dict[c] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # 后一位是省的核减和
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
            postion_dict[c][7] =ab[0]
            postion_dict[c][8] = ab[1]
            postion_dict[c][9] = ab[2]


# print(country_dict)
# print(time_dict)
# print(postion_dict)
name=datetime.datetime.now()
txt_name='acummulatedValueCheckResult_'+str(name.month)+'月'+str(name.day)+'日'+str(name.hour)+'时'+str(name.minute)+'分'
origin_data=[]
a=['确诊时间','省份','累计确诊','卫健委累计确诊','是否一致','累计出院','卫健委累计出院','是否一致','累计死亡','卫健委累计死亡','是否一致']
origin_data.append(a)
postion_keys=list(postion_dict.keys())
for i in range(0,len(postion_dict)):
    b=postion_dict[postion_keys[i]]
    # if postion_keys[i] == None:
    #     postion_keys[i]='无数据'
    # if a[0]!=a[3]:
    #     error_inf=postion_keys[i] + ',各地区新增确诊病例累积'+str(int(a[0]))+',省级新增'+str(int(a[3]))
    #     print(error_inf)
    # if a[1]!=a[4]:
    #     error_inf = postion_keys[i] + ',各地区新增治愈出院数累积' + str(int(a[1])) + ',省级新增' + str(int(a[4]))
    #     print(error_inf)
    # if a[2] != a[5]:
    #     error_inf = postion_keys[i] + ',各地区新增死亡数累积' + str(int(a[2])) + ',省级新增' + str(int(a[5]))
    #     print(error_inf)
    # ans=postion_keys[i]+',最新日期:'+new_day+',省级累计'+str(int(a[3]+a[6]))+',累积出院'+str(int(a[4]))+',累积死亡'+str(int(a[5]))+'(核减'+str(int(a[6]))+')'
    a=[]
    a.append(new_day)
    a.append(postion_keys[i])
    a.append(str(int(b[3] + b[6])))
    a.append(str(int(b[7])))
    if (b[3]+b[6])!=b[7]:
        a.append('否')
    else:
        a.append('是')
    a.append(str(int(b[4])))
    a.append(str(int(b[8])))
    if b[4]!=b[8]:
        a.append('否')
    else:
        a.append('是')
    a.append(str(int(b[5])))
    a.append(str(int(b[9])))
    if b[5]!=b[9]:
        a.append('否')
    else:
        a.append('是')
    origin_data.append(a)
with open(txt_name+".csv", "a+", newline='',encoding='utf-8-sig') as csvfile:
    writer  = csv.writer(csvfile)
    for row in origin_data:
        writer.writerow(row)
csvfile.close()
print('done')
