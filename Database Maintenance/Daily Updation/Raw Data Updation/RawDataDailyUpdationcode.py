# -*- coding: utf-8 -*-
"""
Created on Thu Dec  8 16:20:27 2022

@author: admin
"""


#import the modules
import os
import pandas as pd
import psycopg2
import time
from io import StringIO
from datetime import datetime


from datetime import date
#from datetime import datetime
import calendar

#date = date(2022,10,27) # date.today() #date.today()
date = date.today()

month = calendar.monthcalendar(date.year, date.month)
year=str(date.year)

thrusday = max(month[-1][calendar.THURSDAY], month[-2][calendar.THURSDAY])
print(thrusday)
month=date.strftime('%B')
if(date.day>=thrusday):
    if(month=="December"):
        month="January"
        year=date.year+1
    else:
        month=date.month+1
        month=calendar.month_name[month]

        
day = date.strftime('%d')
nummonth=date.strftime("%m")
print(date)
print(year)
print(month)
print(day)



st=time.time()
conn = psycopg2.connect(database="RawDataBase",
                        user='postgres', password='swancap123',
                        host='swandatabase.cfehmk2wtejq.ap-south-1.rds.amazonaws.com', port='5432'
)

conn.autocommit = True
cursor = conn.cursor()


#read the path
file_path = "//imac2//F//All Databases//Options (Updated as of 24112022)//Index Options//Excel//All Options RawData Files (GDFL)"

csvfile = "NSEFO_" + str(day) + str(nummonth) + str(date.year) + ".csv"
print(csvfile)
file = file_path + '//' + year + '//' + month + ' ' + year 
df_append = pd.DataFrame()
df = pd.read_csv(file + '//' + csvfile)
vname = df.columns[-2]
name = df.columns[-1]
df[vname] = ['{:d}'.format(int(x)) for x in df[vname]]
df[name] = ['{:d}'.format(int(x)) for x in df[name]]
tablename = "r" + csvfile[-12:-4]

print(tablename)
datevalue = csvfile[-12:-4]
Date1 = csvfile[-12:-10] + "-" + csvfile[-10:-8] + "-" + csvfile[-8:-4]
print(Date1)

sql = '''DROP TABLE IF EXISTS ''' + tablename
cursor.execute(sql)

s = '''CREATE TABLE IF NOT EXISTS ''' + tablename + '''(Ticker varchar(50) NOT NULL,Date date,Time time,Open float,High float,Low float,Close float,Volume bigint,"Open Interest" bigint);'''
cursor.execute(s)
conn.commit()
   
buffer = StringIO()
  
    
df.to_csv(buffer, index = False)
buffer.seek(0)

sql = "COPY %s FROM STDIN WITH CSV HEADER DELIMITER AS ','"
with conn.cursor() as cur:
    #cur.execute("truncate " + table + ";")
    cur.copy_expert(sql=sql % tablename, file=buffer)
    conn.commit()

    
    
s = '''Select 1 from rawinfo where name=\'''' + tablename + '''\';'''
cursor.execute(s)
k = cursor.fetchall()
print(k)
#z=k[0]
#print(z[0])
if(k == []):
    sql3 ='''INSERT INTO rawinfo(NAME,Date) VALUES (%s,%s);'''
    record_to_insert = (tablename,Date1)
    cursor.execute(sql3,record_to_insert)

print('Number of rows before committing : ', df.shape[0])
conn.commit()

s = '''Select count(*) from '''+tablename+''';'''
cursor.execute(s)
k=cursor.fetchall()
print('Number of rows after committing : ', k[0][0])


print("sql2 done")
                        
conn.close()
print("sql done")
et=time.time()

elapsed_time=et-st;
print("elapsed_time:",elapsed_time)

