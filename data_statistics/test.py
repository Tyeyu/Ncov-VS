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
        if a[0]!=a[3]:
                error_inf=ShengFen[j]+','+time_keys[i]+',地区新增确诊病例累加值为'+str(int(a[0]))+',省级新增'+str(int(a[3]))
                f1.write(error_inf)
                f1.write('\n')
        if a[1]!=a[4]:
                error_inf = ShengFen[j] + ',' + time_keys[i] + ',地区新增治愈出院数累加值为' + str(int(a[1])) + ',省级新增' + str(int(a[4]))
                f1.write(error_inf)
                f1.write('\n')
        if a[2] != a[5]:
                error_inf = ShengFen[j] + ',' + time_keys[i] + ',地区新增死亡数累加值为' + str(int(a[2])) + ',省级新增' + str(int(a[5]))
                f1.write(error_inf)
                f1.write('\n')
f1.write("------------------省级复核，省级所有日期累计值 == 卫健委发布的累计值-----------------\n")
postion_keys=list(postion_dict.keys())
for i in range(0,len(postion_dict)):
    a=postion_dict[postion_keys[i]]
    if (a[3]+a[6])!=a[7]:
        ans = postion_keys[i] + ',最新日期:' + new_day + ',确诊累计值' + str(int(a[3] + a[6])) + ',卫健委累计值' + str(
            int(a[7]))
        f1.write(ans)
        f1.write('\n')
    if a[4]!=a[8]:
        ans = postion_keys[i] + ',最新日期:' + new_day + ',出院累计值' + str(int(a[4])) + ',卫健委累计值' + str(
            int(a[8]))
        f1.write(ans)
        f1.write('\n')
    if a[5]!=a[9]:
        ans = postion_keys[i] + ',最新日期:' + new_day + ',死亡累计值' + str(int(a[5])) + ',卫健委累计值' + str(
            int(a[9]))
        f1.write(ans)
        f1.write('\n')
f1.write("------------------全国级复核，省级累计值 == 全国累计-----------------\n")
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
        error_inf = country_keys[i] + ',各省新增确诊病例累计' + str(int(a['省级总和'][0])) + ',国家级新增' + str(int(a['国家级'][0]))
        f1.write(error_inf)
        f1.write('\n')
    if a['国家级'][1]!=a['省级总和'][1]:
        error_inf = country_keys[i] + ',各省新增治愈出院数累计' + str(int(a['省级总和'][1])) + ',国家级新增' + str(int(a['国家级'][1]))
        f1.write(error_inf)
        f1.write('\n')
    if a['国家级'][2]!=a['省级总和'][2]:
        error_inf = country_keys[i] + ',各省新增死亡数累计' + str(int(a['省级总和'][2])) + ',国家级新增' + str(int(a['国家级'][2]))
        f1.write(error_inf)
        f1.write('\n')
f1.close()
print('done')
