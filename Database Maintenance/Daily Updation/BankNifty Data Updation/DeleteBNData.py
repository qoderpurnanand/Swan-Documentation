# -*- coding: utf-8 -*-
"""
Created on Tue Jan  3 12:50:04 2023

@author: Admin
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



date = date(2022,11,25)         ## date to be entered as an input 
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


    sql2='''select *from "'''+schema+'''".delete_datewisemulti(\''''+datestr+'''\');'''

    cursor.execute(sql2)
    conn.commit()
    print("Deletion from schema "+schema+" done")