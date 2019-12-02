# -*- coding: utf-8 -*-

import sqlite3 as db
import os
import time
import configparser
import string

currentTime = time.time()
#print(currentTime)


def Dlina_zapisi(fin,pos):
    fin.seek(pos)
    bb = fin.read(1)
    #print(fin.tell(), bb)
    mas=[]
    if bb ==  b'\xc8':
        len_z = fin.read(2)
        #print(len_z)
        len_z = len_z[0] + len_z[1]
        #print(len_z)
        fin.seek(-3, 1)
        zapis_1 = f_in.read(len_z)
        #print(zapis_1)
        fin.seek(pos)
        for i in range(len_z):
            mas.append(ord(fin.read(1)))

    return len_z,mas

def Out_Num(mas,l_num):
    i=0
    s=''
    pos=16
    for i in range(l_num//2):
        pos=i+16
        num = mas[pos]
        s += str((num & 0b11110000) >> 4)
        s += str(num & 0b00001111)
    if l_num%2 ==1:
        pos+=1
        s+=str((mas[pos] & 0b11110000) >> 4)
    #print(s)
    return pos,s


def In_Num(mas,pos):
    #print(pos+1,mas[pos+1])
    i=0
    s=''
    temp=pos+1
    l_num=(mas[temp]>>5)+(mas[temp]&0b00011111)
    temp+=1
    if l_num > 1:
        for i in range(l_num // 2):
            num = mas[temp + i]
            if (num & 0b11110000) >> 4 == 11:
                s+='*'
            elif (num & 0b11110000) >> 4 == 12:
                s+='#'
            else:
                s += str((num & 0b11110000) >> 4)
            if num & 0b00001111 == 11:
                s+='*'
            elif num & 0b00001111 == 12:
                s+='#'
            else:
                s += str(num & 0b00001111)
    if l_num%2 ==1:
        if ((mas[temp+1+i] & 0b11110000) >> 4) == 11:
            s += '*'
        elif ((mas[temp+1+i] & 0b11110000) >> 4)== 12:
            s += '#'
        else:
            s+=str((mas[temp+1+i] & 0b11110000) >> 4)
    pos=temp+l_num//2+l_num%2
    #print(pos,s)
    return pos,s

def Orig_Num(mas,pos):
    #print(pos+1,mas[pos+1])
    i=0
    s=''
    temp=pos+2
    l_num=(mas[temp]>>5)+(mas[temp]&0b00011111)
    temp+=1
    if l_num > 1:
        for i in range(l_num // 2):
            num = mas[temp + i]
            s += str((num & 0b11110000) >> 4)
            s += str(num & 0b00001111)
    if l_num%2 ==1:
        s+=str((mas[temp+1+i] & 0b11110000) >> 4)
    pos=temp+l_num//2+l_num%2
    #print(pos,s)
    return pos,s

def FWD_Number(mas,pos):
    l_num=mas[pos+1]
    snum=''
    l_num = l_num & 0b00011111
    #print( l_num)
    l_num1 = l_num % 2
    l_num = (l_num) // 2
    s=''
    if (l_num+l_num1)!=0:
        pos += 2
        i=0
        for i in range(l_num):
            # print(i)
            num = mas[pos + i]
            s += str((num & 0b11110000) >> 4)
            s += str(num & 0b00001111)
        pos += i
        # print(i,pos)

    snum = s
    #print( snum)
    return  pos,snum

def Date_Time(mas,pos):
    #print(pos,mas[pos:pos+9])
    s_d=''
    s_t=''
    s_d='20'+str(mas[pos+1])+'-'
    if (mas[pos+2])<10: s_d+='0'
    s_d+=str(mas[pos+2])+'-'
    if (mas[pos+3])<10: s_d+='0'
    s_d+=str(mas[pos+3])
    if (mas[pos+4])<10: s_t+='0'
    s_t+=str(mas[pos+4])+':'
    if (mas[pos+5])<10: s_t+='0'
    s_t+=str(mas[pos+5])+':'
    if (mas[pos+6])<10: s_t+='0'
    s_t+=str(mas[pos+6])
    pos+=9

    return s_d, s_t

def Dlit_vyzova(mas,pos):
    dlit=0
    #print('qqqqqqqqqq', pos)
    #print(mas[pos+1],mas[pos+2],mas[pos+3],mas[pos+4])
    dlit=mas[pos+1]*16777216+mas[pos+2]*65536+mas[pos+3]*256+mas[pos+4]
    return dlit

def Trunk(mas,pos):
    trgr=0
    trun=0
    por=0
    chan=0
    trgr=mas[pos+1]*256+mas[pos+2]
    trun=mas[pos+3]*256+mas[pos+4]
    por=mas[pos+6]*256+mas[pos+7]
    chan=mas[pos+8]
    #print(trgr,trun,por,chan)
    return trgr,trun,por,chan

def Create_Tab(name_tab,s):
    #fields_tab=spisok[name_tab].split('|')
    #print(str(len(fields_tab)) ,str(fields_tab))
    column=''
    for i in range(len(s)):
        if i != 0:
            column += ',' + s[i] + ' ' + 'VARCHAR (30) '
        else:
            column += s[i] + ' ' + 'VARCHAR (30) '

    #s='Out_Number,In_Number, Start_Date, Start_time, End_Date, End_Time, Dlit, In_TrGroup, In_Trunk, In_Port, In_Chanel,' \
     # 'Out_TrGr, Out_Trunk, Out_Port, Out_Chanel, Cause, FWD_Number, Origin_Number '
    #print(s)

    sql = " CREATE TABLE if not exists " + name_tab + "(" + s + ");"
    try:
        #print(sql)
        cu.execute(sql)
        sql2="""DELETE FROM """+name_tab+";"
        cu.execute(sql2)
    except db.OperationalError as e:
        print("Error:1 ", e)
    except db.DatabaseError as x:
        print("Error:2 ", x)
    conn.commit()

def Insert_Tab(name_tab,s,st_db):
    strok=''

    for i in range(len(st_db)):
        if st_db[i]=='':
            st_db[i]='""'
        #print('+',st_db[i])
        if( '*' in st_db[i]) or ( '#' in st_db[i]):
            st_db[i]='"'+st_db[i] +'"'
        if i==0:
            strok+=st_db[i]
        else:
            strok+=','+st_db[i]
    #print('--',strok)

    sql="INSERT INTO "+name_tab+" ( "+s+ " )  VALUES ( " + strok + " );"
    #print(sql)
    try:
        cu.execute(sql)
    except db.OperationalError as e:
        print("11111",e)
        print(strok)
    #conn.commit()



conf = configparser.RawConfigParser()
conf.read("transfer.conf")
db_name= conf.get("Config", "DataBase")
print(db_name)
dirname= conf.get("Config", "dirname")
print(dirname)

conn = db.connect(db_name)
cu = conn.cursor()
#column=[]
s_column = 'Out_Number,In_Number, Start_Date, Start_time, End_Date, End_Time, Dlit, In_TrGroup, In_Trunk, In_Port, In_Chanel,' \
    'Out_TrGr, Out_Trunk, Out_Port, Out_Chanel, Cause, FWD_Number, Origin_Number ,Dop_Usluga, Out_In'

tab_name='Taxa'
Create_Tab(tab_name,s_column)
m=[]
files = os.listdir(dirname)
file_start=conf.get("Config", "file_start")
file_end=conf.get("Config", "file_end")

if file_end == '':
    file_end = 'z'

if file_start == '':
    file_start='0'


for ama in files:
    if (ama >= file_start) and (ama<=file_end):
        print(ama)

#print(files)
#ama= filter(lambda x: x.endswith('.ama'), files)
#print(ama)
#f_name='i100020171009003074.ama'

f_out=open('tax9.out','w')

for ama in files:
    #print(ama)
    f_stroka=[]
    if (ama >= file_start) and (ama<=file_end):
        if ama[-4:] == '.ama':
            f_in = open(dirname + '\\' + ama, 'rb')

            # f_in = open(dirname + '\\' + ama, 'rb')
            # f_in=open(f_name,'rb')
            # j = 0
            # f_read = 0

            f_in.seek(0)
            f_m = []
            f_m = f_in.read()
            #print(f_m)
            f_in.seek(0)
            big_pos = 0
            pos_m = 0
            i = 0

            while (big_pos < len(f_m)) & (200 in f_m):
                #print(big_pos, len(f_m))
                while (f_m[big_pos] != 200) & (big_pos < len(f_m)-1):
                    #print(i,big_pos,f_m[big_pos])
                    big_pos += 1
                    #print(big_pos)
                # big_pos = i
                dlina_m = f_m[big_pos + 1] + f_m[big_pos + 2]
                #print(dlina_m)
                m = f_m[big_pos:big_pos + dlina_m]
                #print(m)
                big_pos += dlina_m
                pos_m = 0

                if m[12] != 31:
                    len_num_out = (m[15] >> 5) + (m[15] & 0b00011111)
                    pos_m = 16 + (len_num_out // 2) + (len_num_out % 2)

                    out_in = str(m[12])
                    #print(out_in)

                    out_num_st = ''
                    in_num_st = ''
                    fwd_num_st = ''
                    orig_num_st = ''
                    dop_usluga = ''
                    start_date = ''
                    start_time = ''
                    end_date = ''
                    end_time = ''
                    dlit = 0
                    i_tr_gr = 0
                    i_trunk = 0
                    i_port = 0
                    i_chanel = 0
                    o_tr_gr = 0
                    o_trunk = 0
                    o_port = 0
                    o_chanel = 0
                    cause = 16
                    stroka = ''
                    #out_in = ''
                    s_db = []

                    pos_m, out_num_st = Out_Num(m, len_num_out)
                    if len_num_out != 0 : pos_m += 1
                    # print(pos_m,'---------',m[pos_m])# функция исходящий номер
                    if (m[pos_m] == 100) & (pos_m < len(m)):
                        # print('100', 'Hx64', ama)
                        pos_m, in_num_st = In_Num(m, pos_m)
                    if (m[pos_m] == 101) & (pos_m < len(m)):
                        ##print('101','Hx65')
                        pos_m, fwd_num_st = In_Num(m, pos_m)

                    # конец фиксированной части

                    # Начало переменной части
                    cause=0
                    cause112 =-1

                    while pos_m < len(m):
                        # print('-',pos_m,m[pos_m])

                        if (m[pos_m] == 102) & (pos_m < len(m)):
                            ##print('102','Hx66')
                            start_date, start_time = Date_Time(m, pos_m)
                            pos_m += 9
                        elif (m[pos_m] == 103) & (pos_m < len(m)):
                            ##print('103','Hx67')
                            end_date, end_time = Date_Time(m, pos_m)
                            pos_m += 9
                        elif (m[pos_m] == 104) & (pos_m < len(m)):
                            # print('104','-x68', pos_m, 'кол-во тарифных импульсов')
                            pos_m += 4
                        elif (m[pos_m] == 105) & (pos_m < len(m)):
                            # print('105','Hx69', pos_m,'Базовая услуга')
                            pos_m += 3
                            # print(pos_m)
                        elif (m[pos_m] == 106) & (pos_m < len(m)):
                            # print('106','Hx6A', 'Доп услуга 1 аб.')
                            pos_m += 2
                        elif (m[pos_m] == 107) & (pos_m < len(m)):
                            # print('107','Hx6B',"Доп услуга 2 аб")
                            pos_m += 2
                        elif (m[pos_m] == 108) & (pos_m < len(m)):
                            # print('108','Hx6C',"Адм-е услуги аб-ом")
                            pos_m += 3
                        elif (m[pos_m] == 109) & (pos_m < len(m)):
                            # print('109',ama,'Hx6D',"Последовательность символов")
                            pos_m, dop_usluga = In_Num(m, pos_m)
                            # print(dop_usluga)
                            # pos_m += 3  # +n
                        elif (m[pos_m] == 110) & (pos_m < len(m)):
                            # print('110','Hx6E')
                            pos_m += 2
                        elif (m[pos_m] == 111) & (pos_m < len(m)):
                            # print('111','Hx6F')
                            pos_m += 2
                        elif (m[pos_m] == 112) & (pos_m < len(m)):
                            # print('112','Hx70')
                            cause112 = m[pos_m + 1]
                            #print(cause)
                            pos_m += 2  # Failure Cause
                        elif (m[pos_m] == 113) & (pos_m < len(m)):
                            # print('113','Hx71')
                            i_tr_gr, i_trunk, i_port, i_chanel = Trunk(m, pos_m)
                            pos_m += 9  # Входящая Транк группа, транк, порт, канал
                        elif (m[pos_m] == 114) & (pos_m < len(m)):
                            # print('114','Hx72')
                            o_tr_gr, o_trunk, o_port, o_chanel = Trunk(m, pos_m)
                            pos_m += 9  # Исходящая Транк группа, транк, порт, канал
                        elif (m[pos_m] == 115) & (pos_m < len(m)):
                            # print('115','Hx73')
                            dlit = Dlit_vyzova(m, pos_m)
                            pos_m += 5  # Длительность вызова
                        elif (m[pos_m] == 117) & (pos_m < len(m)):
                            # print('117','Hx75')
                            pos_m += 10
                        elif (m[pos_m] == 118) & (pos_m < len(m)):
                            # print('118','Hx76')
                            pos_m += 3  # +n
                        elif (m[pos_m] == 119) & (pos_m < len(m)):
                            # print('119','Hx77')
                            pos_m, orig_num_st = Orig_Num(m, pos_m)
                            # print(pos_m,m[pos_m])
                            # pos_m += 3 # +n Оригинальный номер вызывающего абонента
                        elif (m[pos_m] == 120) & (pos_m < len(m)):
                            # print('120','Hx78')
                            pos_m += 15
                        elif (m[pos_m] == 121) & (pos_m < len(m)):
                            # print('121','Hx79',pos_m)
                            cause = m[pos_m + 3]
                            #print(cause112,' ///   ',cause)
                            pos_m += 5  # Причина разъединения
                            # print(pos_m)
                        elif (m[pos_m] == 122) & (pos_m < len(m)):
                            # print('122','Hx7A')
                            pos_m += 5
                        elif (m[pos_m] == 123) & (pos_m < len(m)):
                            # print('123','Hx7B')
                            pos_m += 26
                        elif (m[pos_m] == 124) & (pos_m < len(m)):
                            # print('124','Hx7C')
                            pos_m += 10
                        elif (m[pos_m] == 125) & (pos_m < len(m)):
                            # print('125','Hx7D')
                            pos_m += 5
                        elif (m[pos_m] == 126) & (pos_m < len(m)):
                            # print('126','Hx7E')
                            pos_m += 5

                        elif (m[pos_m] == 127) & (pos_m < len(m)):
                            #print('127','Hx7F')
                            #m[pos_m+1]
                            #print(pos_m,m[pos_m+1])
                            pos_m += m[pos_m+1]
                            #print(pos_m)
                        elif (m[pos_m] == 128) & (pos_m < len(m)):
                            #print('128','Hx80',pos_m)
                            pos_m += 13
                        elif (m[pos_m] == 129) & (pos_m < len(m)):
                            #print('129','Hx81')
                            pos_m += 25

                        elif (m[pos_m] == 116) & (pos_m < len(m)):
                            # print('116','Hx74')
                            pos_m += 4
                        else:
                            pos_m += 1

                    # print('%+8s' % out_num_st, '%+15s' % in_num_st, '%+15s' % start_date, '%+9s' % start_time,
                    #      '%+12s' % end_date, '%+9s' % end_time, '%+9s' % dlit,
                    #      '%+9s' % i_tr_gr, '%+9s' % i_trunk, '%+9s' % i_port, '%+9s' % i_chanel,
                    #      '%+9s' % o_tr_gr, '%+9s' % o_trunk, '%+9s' % o_port, '%+9s' % o_chanel,
                    #      '%+9s' % cause, '%+9s' % fwd_num_st, '%+9s' % orig_num_st)

                    # -------------------------------------------------------

                    stroka = '%+8s' % out_num_st + '%+15s' % in_num_st + '%+15s' % start_date + '%+9s' % start_time + \
                             '%+12s' % end_date + '%+9s' % end_time + '%+9s' % dlit + \
                             '%+9s' % i_tr_gr + '%+9s' % i_trunk + '%+9s' % i_port + '%+9s' % i_chanel + \
                             '%+9s' % o_tr_gr + '%+9s' % o_trunk + '%+9s' % o_port + '%+9s' % o_chanel + \
                             '%+9s' % cause + '%+9s' % fwd_num_st + '%+9s' % orig_num_st  + '%+9s' % dop_usluga+ '%+9s' % out_in + '\n'
                    # if fwd_num_st=='':fwd_num_st='0'
                    # if orig_num_st=='':orig_num_st='0'
                    s_db.append(out_num_st)
                    s_db.append(in_num_st)
                    s_db.append('"' + start_date + '"')
                    s_db.append('"' + start_time + '"')
                    s_db.append('"' + end_date + '"')
                    s_db.append('"' + end_time + '"')
                    s_db.append(str(dlit))
                    s_db.append(str(i_tr_gr))
                    s_db.append(str(i_trunk))
                    s_db.append(str(i_port))
                    s_db.append(str(i_chanel))
                    s_db.append(str(o_tr_gr))
                    s_db.append(str(o_trunk))
                    s_db.append(str(o_port))
                    s_db.append(str(o_chanel))
                    s_db.append(str(cause))
                    s_db.append(fwd_num_st)
                    s_db.append(orig_num_st)
                    s_db.append(dop_usluga)
                    s_db.append(out_in)

                    # s_db.append('"'+dop_usluga+'"')
                    # print(s_db)
                    # stroka_db=out_num_st+ ',' + in_num_st+ ','+ start_date+ ',' + '"'+start_time+ '"'+\
                    #      ',' + end_date+ ',' + '"'+ end_time+ '"'+ ',' + str(dlit)+\
                    #     ',' + str(i_tr_gr)+ ',' + str(i_trunk)+ ',' + str(i_port)+ ',' + str(i_chanel)+\
                    #    ',' + str(o_tr_gr)+ ',' + str(o_trunk)+ ',' + str(o_port)+ ',' + str(o_chanel)+\
                    #   ',' + str(cause)+ ',' +'"'+  fwd_num_st+'"'+  ',' +'"'+  orig_num_st+'"'
                    Insert_Tab(tab_name, s_column, s_db)

                    f_stroka.append(stroka)
                    #print(stroka)
            f_in.close()

    f_out.writelines(f_stroka)
    conn.commit()



print(time.time()-currentTime)

#f_in.close()
f_out.close()