# -*- coding: utf-8 -*-
"""
Created on Thu Dec 22 10:51:16 2022

@author: Admin
"""



# -*- coding: utf-8 -*-
"""
Created on Wed Dec 14 10:00:06 2022

@author: admin
"""

import psycopg2
import time
import pandas as pd
from io import StringIO
import re
from datetime import date
st=time.time()
conn = psycopg2.connect(database="BankNiftydb",
						user='postgres', password='swancap123',
						host='swandatabase.cfehmk2wtejq.ap-south-1.rds.amazonaws.com', port='5432'
)

conn.autocommit = True
cursor = conn.cursor()




date = date(2023,1,18)                 ## to be changed daily
day = date.strftime('%d')
nummonth=date.strftime("%m")
year=date.strftime('%Y')
datestr=str(year)+"-"+str(nummonth)+"-"+str(day)
print(datestr)

for i in range(1,4):
    if(i==1):
        numberstring="I"
        schema="BankNiftyMonthlyI"
        infotable="BANKNIFTYMONTHLY-Iinfo"
    if(i==2):
        numberstring="II"
        schema="BankNiftyMonthlyII"
        infotable="BANKNIFTYMONTHLY-IIinfo"
    if(i==3):
        numberstring="III"
        schema="BankNiftyMonthlyIII"
        infotable="BANKNIFTYMONTHLY-IIIinfo"
        
    bndf=pd.read_csv("C:\\Users\\admin\\Desktop\\Pyspark\\Banknifty-"+numberstring+".csv")
    df=bndf.groupby(['Ticker'])
   
    for name,group in df:
        print(name)
    
        sql2='''CREATE TABLE IF NOT EXISTS "'''+schema+'''"."'''+name+'''"(Ticker varchar(50) NOT NULL,Date Date NOT NULL,Time time NOT NULL,Open float NOT NULL,High float NOT NULL,Low float NOT NULL,Close float NOT NULL,Volume float NOT NULL,"Open Int" float NOT NULL);'''
        cursor.execute(sql2)
        conn.commit()
        noofrows=group.shape[0]
        print(noofrows)
        buffer = StringIO()
        group.to_csv(buffer, index = False)
        buffer.seek(0)
        sql = "COPY %s FROM STDIN WITH CSV HEADER DELIMITER AS ','"
        table='"'+schema+'"."'+name+'"'
        with conn.cursor() as cur:
            #cur.execute("truncate " + table + ";")
            cur.copy_expert(sql=sql % table, file=buffer)
            conn.commit()
    
        cursor = conn.cursor()
        s='''Select 1 from "'''+schema+'''"."'''+infotable+'''" where ticker=\''''+name+'''\';'''
        cursor.execute(s)
        k=cursor.fetchall()
        print(k)
        #z=k[0]
        #print(z[0])
        if(k==[]):
            num=re.findall(r"[-+]?(?:\d*\.*\d+)", name)
            strike=num[0]
            typecepe=name[-2:]
            sql3 ='''INSERT INTO "'''+schema+'''"."'''+infotable+'''"(Ticker,Strike,Type)VALUES (%s,%s,%s)'''
            record_to_insert = (name,strike,typecepe)
            cursor.execute(sql3, record_to_insert)
            conn.commit()
    
        sql4='''Select count(*) from "'''+schema+'''"."'''+name+'''" where date=\''''+datestr+'''\';'''
        cursor.execute(sql4)
        r=cursor.fetchall()
        print(r[0][0])
        if(r[0][0]!=noofrows):
            print("numberofrows not matching")
            break
conn.close()
print("sql done")
et=time.time()

elapsed_time=et-st;
print("elapsed_time:",elapsed_time)
