import csv
import pandas as pd
import datetime
import numpy as np
import sys

def read_data():
    file_name=sys.argv[1]
    csv_data = pd.read_csv(file_name,keep_default_na=False)
    return csv_data

def ex_GAT(name):
    if(name=='香港' or name=='澳门' or name=='台湾'):
        return False
    return True

def judge(data):
    x=0
    try:
        x=float(data)
    except ValueError as e:
        x=0.0
    return x
    
def get_row_data(e_row,row_data):
    a_list=[]
    a_list.append(row_data['数据起始时间'][e_row])
    a_list.append(row_data['数据结束时间'][e_row])
    a_list.append(row_data['类别'][e_row])
    a_list.append(row_data['省份'][e_row])
    a_list.append(row_data['城市'][e_row])
    a_list.append(judge(row_data['新增确诊病例'][e_row]))
    a_list.append(judge(row_data['新增治愈出院数'][e_row]))
    a_list.append(judge(row_data['新增死亡数'][e_row]))
    a_list.append(judge(row_data['核减'][e_row]))
    return a_list

def seg_time(time_str):
    time_list=[]
    flag=False
    time1=''
    time2=''
    for i in time_str:
        if(i==','):
            flag=True
        elif(flag==False):
            time1+=i
        elif(flag==True):
            time2+=i
    time_list.append(time1)
    time_list.append(time2)
    return time_list

def cal_emerge(origin_data):
    country_dict={}
    for e_row in range(0,len(origin_data)):
        row_list=get_row_data(e_row,origin_data)
        st_time=row_list[0]
        ed_time=row_list[1]
        lb=row_list[2]
        sf=row_list[3]
        cs=row_list[4]
        em_qz=row_list[5]
        em_zy=row_list[6]
        em_sw=row_list[7]
        hj=row_list[8]
        
        time_key=st_time+','+ed_time

        if((lb=='国家级' or lb == '省级')and ex_GAT(sf)==True):
            if(time_key not in country_dict):
                country_dict[time_key]={}
            if(lb=='省级'):
                country_dict[time_key][sf]=[0,0,0]
                country_dict[time_key][sf][0]=em_qz+hj
                country_dict[time_key][sf][1]=em_zy
                country_dict[time_key][sf][2]=em_sw

                country_dict[time_key]['省级总和'] = [0, 0, 0]
                country_dict[time_key]['省级总和'][0]+=(em_qz+hj)
                country_dict[time_key]['省级总和'][1]+=em_zy
                country_dict[time_key]['省级总和'][2]+=em_sw
        
            elif(lb=='国家级'):
                country_dict[time_key]['国家级']=[0, 0, 0]
                country_dict[time_key]['国家级'][0]=em_qz+hj
                country_dict[time_key]['国家级'][1]=em_zy
                country_dict[time_key]['国家级'][2]=em_sw
    return country_dict
     
def cal_time(origin_data): #计算新增（地区&省级）
    time_dict={}
    for e_row in range(0,len(origin_data)):
        row_list=get_row_data(e_row,origin_data)
        st_time=row_list[0]
        ed_time=row_list[1]
        lb=row_list[2]
        sf=row_list[3]
        cs=row_list[4]
        em_qz=row_list[5]
        em_zy=row_list[6]
        em_sw=row_list[7]
        hj=row_list[8]

        time_key=st_time+','+ed_time
        if((lb == '地区级' or lb == '省级') and ex_GAT(sf)==True):
            if(time_key not in time_dict):
                time_dict[time_key]={}
            if(sf not in time_dict[time_key]):
                time_dict[time_key][sf]=[0, 0, 0, 0, 0, 0, 0, 0]
            if(lb == '地区级'):
                time_dict[time_key][sf][0]+=em_qz
                time_dict[time_key][sf][1]+=em_zy
                time_dict[time_key][sf][2]+=em_sw
                time_dict[time_key][sf][3]+=hj
            elif(lb=='省级'):
                time_dict[time_key][sf][4]=em_qz
                time_dict[time_key][sf][5]=em_zy
                time_dict[time_key][sf][6]=em_sw
                time_dict[time_key][sf][7]=hj
    return time_dict

def cal_postion(origin_data):
    postion_dict={}
    for e_row in range(0,len(origin_data)):
        row_list=get_row_data(e_row,origin_data)
        st_time=row_list[0]
        ed_time=row_list[1]
        lb=row_list[2]
        sf=row_list[3]
        cs=row_list[4]
        em_qz=row_list[5]
        em_zy=row_list[6]
        em_sw=row_list[7]
        hj=row_list[8]

        if((lb == '地区级' or lb == '省级') and ex_GAT(sf)==True):
            if(sf not in postion_dict):
                postion_dict[sf]=[0, 0, 0, 0, 0, 0, 0]
            if(lb =='地区级'):
                postion_dict[sf][0]+=em_qz
                postion_dict[sf][1]+=em_zy
                postion_dict[sf][2]+=em_sw
            if(lb =='省级'):
                postion_dict[sf][3]+=em_qz
                postion_dict[sf][4]+=em_zy
                postion_dict[sf][5]+=em_sw
                postion_dict[sf][6]+=hj
    return postion_dict

def cal_cumulative(origin_data):
    cumulative_dict={}
    for e_row in range(0,len(origin_data)):
        row_list=get_row_data(e_row,origin_data)
        st_time=row_list[0]
        ed_time=row_list[1]
        lb=row_list[2]
        sf=row_list[3]
        cs=row_list[4]
        em_qz=row_list[5]
        em_zy=row_list[6]
        em_sw=row_list[7]
        hj=row_list[8]
        e_cumulative=[0,0,0]
        e_cumulative[0]=judge(origin_data['累计确诊人数'][e_row])
        e_cumulative[1]=judge(origin_data['累计治愈人数'][e_row])
        e_cumulative[2]=judge(origin_data['累计死亡人数'][e_row])
        time_key=st_time
        if (ex_GAT(sf)==True and lb=='省级'):
            try:
                datet=datetime.datetime.strptime(time_key,'%Y/%m/%d %H:%M')
                the_key=str(datet.month)+'月'+str(datet.day)+'日'

            
                if(sf not in cumulative_dict):
                    cumulative_dict[sf]={}
                if(the_key not in cumulative_dict[sf]):
                    cumulative_dict[sf][the_key]=[0, 0, 0, 0, 0, 0, 0]
                cumulative_dict[sf][the_key][0]=em_qz
                cumulative_dict[sf][the_key][1]=em_zy
                cumulative_dict[sf][the_key][2]=em_sw
                cumulative_dict[sf][the_key][3]=hj
                cumulative_dict[sf][the_key][4]=e_cumulative[0]
                cumulative_dict[sf][the_key][5]=e_cumulative[1]
                cumulative_dict[sf][the_key][6]=e_cumulative[2]
            except:
                mm=1
    return cumulative_dict   

def write_txt_1(time_dict):

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

def write_txt_2(cumulative_dict):
    f1.write("------------------省级复核，省级所有日期累计值 == 卫健委发布的累计值----------------\n")
    cumulative_keys=list(cumulative_dict.keys())
    for i in range(0,len(cumulative_dict)):
        cu_time=list(cumulative_dict[cumulative_keys[i]].keys())
        for j in range(0, len(cumulative_dict[cumulative_keys[i]])):
            a=cumulative_dict[cumulative_keys[i]][cu_time[j]]
            try:
                dd=datetime.datetime.strptime(cu_time[j],"%m月%d日")
            except ValueError as e:
                mm=1
            if cu_time[j]=='2月7日':
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

def write_txt_3(country_dict):
    f1.write("------------------全国级复核：省级累积==全国累积-----------------\n")
    country_keys=list(country_dict.keys())
    for i in range(0,len(country_dict)):
        a=country_dict[country_keys[i]]
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

def write_csv(cumulative_dict,postion_dict):
    name=datetime.datetime.now()
    txt_name='acummulatedValueCheckResult_'+str(name.month)+'月'+str(name.day)+'日'+str(name.hour)+'时'+str(name.minute)+'分'
    origin_data=[]
    e_row=['确诊时间','省份','累计确诊','卫健委累计确诊','是否一致','累计出院','卫健委累计出院','是否一致','累计死亡','卫健委累计死亡','是否一致']
    origin_data.append(e_row)
    cumulative_key=list(cumulative_dict.keys())
    for i in range(0,len(postion_dict)):
        cu_time = list(cumulative_dict[cumulative_key[i]].keys())
        for j in range(0, len(cumulative_dict[cumulative_key[i]])):
            a=cumulative_dict[cumulative_key[i]][cu_time[j]]
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

if __name__ == '__main__':

    origin_data=read_data()
    country_dict=cal_emerge(origin_data)
    time_dict=cal_time(origin_data)
    postion_dict=cal_postion(origin_data)
    cumulative_dict=cal_cumulative(origin_data)

    global f1
    name=datetime.datetime.now()
    txt_name='acummulatedValueCheckResult_'+str(name.month)+'月'+str(name.day)+'日'+str(name.hour)+'时'+str(name.minute)+'分.log'
    f1=open(txt_name,'w')
    write_txt_1(time_dict)
    #write_txt_2(cumulative_dict)
    #write_txt_3(country_dict)
    #write_csv(cumulative_dict,postion_dict)
    
    print('done')