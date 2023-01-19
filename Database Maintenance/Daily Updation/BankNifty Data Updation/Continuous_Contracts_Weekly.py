# -*- coding: utf-8 -*-
"""
Created on Fri Jan  6 11:29:38 2023

@author: admin
"""

import pyspark
import numpy as np
import pandas as pd
import os
from os import walk
from pyspark.sql import SparkSession
from pyspark.sql import Row
from pyspark.sql.functions import regexp_replace
from pyspark.sql.functions import array_contains
from pyspark.sql.functions import *
import time
from pyspark.sql.functions import date_format
from datetime import date
from datetime import datetime
import datetime

folpath = r"C:\users\admin\desktop\\Pyspark_Contracts\\Weekly_Data\\"
sym = 'BANKNIFTY'

date = date(2023,1,18)
day = date.strftime('%d')
nummonth=date.strftime("%m")
year=date.strftime('%Y')
tablename="r"+str(day)+str(nummonth)+str(year)
print(tablename)

st=time.time()
spark = SparkSession.builder.config("spark.jars", "C:\\Users\\admin\\Downloads\\postgresql-42.5.0.jar") \
    .master("local").appName("PySpark_Postgres_test").getOrCreate()
#spark.sparkContext.setLogLevel("WARN")

df = spark.read.format("jdbc").option("url", "jdbc:postgresql://swandatabase.cfehmk2wtejq.ap-south-1.rds.amazonaws.com/RawDataBase").option("user","postgres").option("password","swancap123")\
    .option("driver", "org.postgresql.Driver").option("dbtable", tablename)\
    .option("user", "postgres").option("password", "swancap123").load()

## GETTING ONLY TIME IN TIME COLUMN
q = df.withColumn('Time',date_format('Time', 'HH:mm:ss'))
#print(q.show())

## FILTERING BANK NIFTY DATA
bndata = q.filter(q.ticker.contains('BANKNIFTY') & (q.ticker.endswith('E.NFO')))

## REPLACING .NFO IN TICKER
bndata = bndata.withColumn('ticker',regexp_replace('ticker','.NFO',''))
#print(bndata.show())

## CONVERTING PYSPARK DATAFRAME TO PANDAS DATAFRAME
bndata=bndata.toPandas()

df = bndata

## READING WEEKLY EXPIRY FILES
exp_df = pd.read_csv(r"C:\Users\admin\Downloads\WeeklyExpiry.csv",parse_dates = ["date"],dayfirst =True,usecols= ['date', 'Week_number'])
exp_date = pd.read_excel(r'C:\users\admin\desktop\Expiry_DT.xlsx',parse_dates = ['Exp_DT'],usecols = ['MonthYear','Exp_DT'])


## SETTING LAST BAR AS 15:29:59
expiry_time = datetime.datetime.strptime('15:29:59', '%H:%M:%S').time()
df['date'] = pd.to_datetime(df['date'])
df['Time'] = df['Time'].str.replace(' 15:00:59','15:00:59')
df['Time'] = df['Time'].str.replace(' 9:','09:',regex=True)
df['Time'] = pd.to_datetime(df['Time']).dt.time
df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
df = df[df['Time'] <= expiry_time]
df = df.rename(columns={'Date' : 'date'})
df['EXPIRY_DT'] = df['ticker'].str[9:16]
df['EXPIRY_DT'] = pd.to_datetime(df['EXPIRY_DT'],dayfirst=True)
df['OPTION_TYP'] = df['ticker'].str[-2:]
df['STRIKE_PR'] = np.where(df['ticker'].str.len()==23,df['ticker'].str[-7:-2],df['ticker'].str[-7:-2])
df['Month'] = df['ticker'].str[11:14]
df['Year'] = np.where(df['ticker'].str.len()==23,df['ticker'].str[14:16],df['ticker'].str[9:11])
df['MonthYear'] = df['Month'] + df['Year']
df = df.rename(columns={'EXPIRY_DT' : 'expiry_date'})

## MERGING WITH EXPIRY SHEET TO GET EXPIRY DATE
df1 = pd.merge(df,exp_df,on='date',how='left')
df1 = df1.drop_duplicates()
df1 = pd.merge(df1,exp_date,on='MonthYear',how='left')
df1 = df1.drop(['Month','Year','MonthYear'],axis=1)

## GETTING THE EXPIRY DATES FOR MONTHLY CONTRACTS
df1['expiry_date'] = np.where(df1['ticker'].str.len()>21,df1['expiry_date'],df1['Exp_DT'])

df1 = df1.drop(['Exp_DT'],axis=1)

exp_df = pd.read_csv(r"C:\Users\admin\Downloads\WeeklyExpiry.csv",parse_dates = ["Weekly_Expiry_Date"],dayfirst =True,usecols= ['Weekly_Expiry_Date', 'Expiry_Week_number'])

exp_df = exp_df.dropna()

exp_df = exp_df.rename(columns = {'Weekly_Expiry_Date': 'expiry_date'})

df2 = pd.merge(df1, exp_df, on ='expiry_date', how ='left')

df2 = df2.drop_duplicates()

df2['week_diff'] = df2['Expiry_Week_number'] - df2['Week_number']

df2['week_diff'] = df2['Expiry_Week_number'] - df2['Week_number']

final_df = df2[(df2["OPTION_TYP"] == "CE") | (df2["OPTION_TYP"] == "PE") ]

final_df["week_diff"] = final_df['week_diff'].replace(np.nan,10000)

agb = final_df.groupby(["week_diff"])
unique_val_list_a = list(final_df["week_diff"].unique())
unique_val_list_a = sorted([a for a in unique_val_list_a if a>=0])[0:12]
print(unique_val_list_a)

## CREATING -I,-II AND SO ON BASED ON THE WEEK DIFFERENCES

if os.path.exists(folpath+sym+'_Weekly-I.csv'):
    os.remove(folpath+sym+'_Weekly-I.csv')
if os.path.exists(folpath+sym+'_Weekly-II.csv'):
    os.remove(folpath+sym+'_Weekly-II.csv')
if os.path.exists(folpath+sym+'_Weekly-III.csv'):
    os.remove(folpath+sym+'_Weekly-III.csv')
if os.path.exists(folpath+sym+'_Weekly-IV.csv'):
    os.remove(folpath+sym+'_Weekly-IV.csv')
if os.path.exists(folpath+sym+'_Weekly-V.csv'):
    os.remove(folpath+sym+'_Weekly-V.csv')
if os.path.exists(folpath+sym+'_Weekly-VI.csv'):
    os.remove(folpath+sym+'_Weekly-VI.csv')
if os.path.exists(folpath+sym+'_Weekly-VII.csv'):
    os.remove(folpath+sym+'_Weekly-VII.csv')
if os.path.exists(folpath+sym+'_Weekly-VIII.csv'):
    os.remove(folpath+sym+'_Weekly-VIII.csv')
if os.path.exists(folpath+sym+'_Weekly-IX.csv'):
    os.remove(folpath+sym+'_Weekly-IX.csv')
if os.path.exists(folpath+sym+'_Weekly-X.csv'):
    os.remove(folpath+sym+'_Weekly-X.csv')
if os.path.exists(folpath+sym+'_Weekly-XI.csv'):
    os.remove(folpath+sym+'_Weekly-XI.csv')
if os.path.exists(folpath+sym+'_Weekly-XII.csv'):
    os.remove(folpath+sym+'_Weekly-XII.csv')    
    


for i in sorted(unique_val_list_a):

    temp_df = agb.get_group(i)

    if i == 0:
        if not os.path.isfile(folpath + sym + '_Weekly-I.csv'):
            temp_df.to_csv(folpath + sym + '_Weekly-I.csv', index=False)
        else: # else it exists so append without writing the header
            temp_df.to_csv(folpath + sym + '_Weekly-I.csv', mode='a', header=False, index=False)

    if i == 1:
        if not os.path.isfile(folpath + sym + '_Weekly-II.csv'):
            temp_df.to_csv(folpath + sym + '_Weekly-II.csv', index=False)
        else: # else it exists so append without writing the header
            temp_df.to_csv(folpath + sym + '_Weekly-II.csv', mode='a', header=False, index=False)

    if i == 2:
        if not os.path.isfile(folpath + sym + '_Weekly-III.csv'):
            temp_df.to_csv(folpath + sym + '_Weekly-III.csv', index=False)
        else: # else it exists so append without writing the header
            temp_df.to_csv(folpath + sym + '_Weekly-III.csv', mode='a', header=False, index=False)

    if i == 3:
        if not os.path.isfile(folpath + sym + '_Weekly-IV.csv'):
            temp_df.to_csv(folpath + sym + '_Weekly-IV.csv', index=False)
        else: # else it exists so append without writing the header
            temp_df.to_csv(folpath + sym + '_Weekly-IV.csv', mode='a', header=False, index=False)

    if i == 4:
        if not os.path.isfile(folpath + sym + '_Weekly-V.csv'):
            temp_df.to_csv(folpath + sym + '_Weekly-V.csv', index=False)
        else: # else it exists so append without writing the header
            temp_df.to_csv(folpath + sym + '_Weekly-V.csv', mode='a', header=False, index=False)

    if i == 5:
        if not os.path.isfile(folpath + sym + '_Weekly-VI.csv'):
            temp_df.to_csv(folpath + sym + '_Weekly-VI.csv', index=False)
        else: # else it exists so append without writing the header
            temp_df.to_csv(folpath + sym + '_Weekly-VI.csv', mode='a', header=False, index=False)

    if i == 6:
        if not os.path.isfile(folpath + sym + '_Weekly-VII.csv'):
            temp_df.to_csv(folpath + sym + '_Weekly-VII.csv', index=False)
        else: # else it exists so append without writing the header
            temp_df.to_csv(folpath + sym + '_Weekly-VII.csv', mode='a', header=False, index=False)

    if i == 7:
        if not os.path.isfile(folpath + sym + '_Weekly-VIII.csv'):
            temp_df.to_csv(folpath + sym + '_Weekly-VIII.csv', index=False)
        else: # else it exists so append without writing the header
            temp_df.to_csv(folpath + sym + '_Weekly-VIII.csv', mode='a', header=False, index=False)
            
    if i == 8:
        if not os.path.isfile(folpath + sym + '_Weekly-IX.csv'):
            temp_df.to_csv(folpath + sym + '_Weekly-IX.csv', index=False)
        else: # else it exists so append without writing the header
            temp_df.to_csv(folpath + sym + '_Weekly-IX.csv', mode='a', header=False, index=False)
    
    if i == 9:
        if not os.path.isfile(folpath + sym + '_Weekly-X.csv'):
            temp_df.to_csv(folpath + sym + '_Weekly-X.csv', index=False)
        else: # else it exists so append without writing the header
            temp_df.to_csv(folpath + sym + '_Weekly-X.csv', mode='a', header=False, index=False)
    
    if i == 10:
        if not os.path.isfile(folpath + sym + '_Weekly-XI.csv'):
            temp_df.to_csv(folpath + sym + '_Weekly-XI.csv', index=False)
        else: # else it exists so append without writing the header
            temp_df.to_csv(folpath + sym + '_Weekly-XI.csv', mode='a', header=False, index=False)
    
    if i == 11:
        if not os.path.isfile(folpath + sym + '_Weekly-XII.csv'):
            temp_df.to_csv(folpath + sym + '_Weekly-XII.csv', index=False)
        else: # else it exists so append without writing the header
            temp_df.to_csv(folpath + sym + '_Weekly-XII.csv', mode='a', header=False, index=False)

## CREATING THE TICKER AND REMOVING ADDITIONAL COLUMNS
if os.path.exists(r'C:\users\admin\desktop\Pyspark\Weekly\Banknifty-I.csv'):
    os.remove(r'C:\users\admin\desktop\Pyspark\Weekly\Banknifty-I.csv')
if os.path.exists(r'C:\Users\admin\Desktop\Pyspark_Contracts\Weekly_Data\BANKNIFTY_Weekly-I.csv'):    
    test = pd.read_csv(r"C:\Users\admin\Desktop\Pyspark_Contracts\Weekly_Data\BANKNIFTY_Weekly-I.csv")
    test['ticker'] = test['ticker'].str[:9]
    test['NewSymbol'] = test['ticker'] + 'WEEKLY' + '-I' + test['STRIKE_PR'].astype(int).astype(str) + test['OPTION_TYP']
    test['ticker'] = test['NewSymbol']
    test = test.drop(test.columns[9:18],axis=1)
    test = test.rename(columns = {'date':'Date','ticker':'Ticker'})
    test.to_csv(r'C:\users\admin\desktop\Pyspark\Weekly\Banknifty-I.csv',index=False)

if os.path.exists(r'C:\users\admin\desktop\Pyspark\Weekly\Banknifty-II.csv'):
    os.remove(r'C:\users\admin\desktop\Pyspark\Weekly\Banknifty-II.csv')
if os.path.exists(r'C:\Users\admin\Desktop\Pyspark_Contracts\Weekly_Data\BANKNIFTY_Weekly-II.csv'):    
    test = pd.read_csv(r"C:\Users\admin\Desktop\Pyspark_Contracts\Weekly_Data\BANKNIFTY_Weekly-II.csv")
    test['ticker'] = test['ticker'].str[:9]
    test['NewSymbol'] = test['ticker'] + 'WEEKLY' + '-II' + test['STRIKE_PR'].astype(int).astype(str) + test['OPTION_TYP']
    test['ticker'] = test['NewSymbol']
    test = test.drop(test.columns[9:18],axis=1)
    test = test.rename(columns = {'date':'Date','ticker':'Ticker'})
    test.to_csv(r'C:\users\admin\desktop\Pyspark\Weekly\Banknifty-II.csv',index=False)

if os.path.exists(r'C:\users\admin\desktop\Pyspark\Weekly\Banknifty-III.csv'):
    os.remove(r'C:\users\admin\desktop\Pyspark\Weekly\Banknifty-III.csv')
if os.path.exists(r'C:\Users\admin\Desktop\Pyspark_Contracts\Weekly_Data\BANKNIFTY_Weekly-III.csv'):    
    test = pd.read_csv(r"C:\Users\admin\Desktop\Pyspark_Contracts\Weekly_Data\BANKNIFTY_Weekly-III.csv")
    test['ticker'] = test['ticker'].str[:9]
    test['NewSymbol'] = test['ticker'] + 'WEEKLY' + '-III' + test['STRIKE_PR'].astype(int).astype(str) + test['OPTION_TYP']
    test['ticker'] = test['NewSymbol']
    test = test.drop(test.columns[9:18],axis=1)
    test = test.rename(columns = {'date':'Date','ticker':'Ticker'})
    test.to_csv(r'C:\users\admin\desktop\Pyspark\Weekly\Banknifty-III.csv',index=False)

if os.path.exists(r'C:\users\admin\desktop\Pyspark\Weekly\Banknifty-IV.csv'):
    os.remove(r'C:\users\admin\desktop\Pyspark\Weekly\Banknifty-IV.csv')
if os.path.exists(r'C:\Users\admin\Desktop\Pyspark_Contracts\Weekly_Data\BANKNIFTY_Weekly-IV.csv'):    
    test = pd.read_csv(r"C:\Users\admin\Desktop\Pyspark_Contracts\Weekly_Data\BANKNIFTY_Weekly-IV.csv")
    test['ticker'] = test['ticker'].str[:9]
    test['NewSymbol'] = test['ticker'] + 'WEEKLY' + '-IV' + test['STRIKE_PR'].astype(int).astype(str) + test['OPTION_TYP']
    test['ticker'] = test['NewSymbol']
    test = test.drop(test.columns[9:18],axis=1)
    test = test.rename(columns = {'date':'Date','ticker':'Ticker'})
    test.to_csv(r'C:\users\admin\desktop\Pyspark\Weekly\Banknifty-IV.csv',index=False)

if os.path.exists(r'C:\users\admin\desktop\Pyspark\Weekly\Banknifty-V.csv'):
    os.remove(r'C:\users\admin\desktop\Pyspark\Weekly\Banknifty-V.csv')
if os.path.exists(r'C:\Users\admin\Desktop\Pyspark_Contracts\Weekly_Data\BANKNIFTY_Weekly-V.csv'):    
    test = pd.read_csv(r"C:\Users\admin\Desktop\Pyspark_Contracts\Weekly_Data\BANKNIFTY_Weekly-V.csv")
    test['ticker'] = test['ticker'].str[:9]
    test['NewSymbol'] = test['ticker'] + 'WEEKLY' + '-V' + test['STRIKE_PR'].astype(int).astype(str) + test['OPTION_TYP']
    test['ticker'] = test['NewSymbol']
    test = test.drop(test.columns[9:18],axis=1)
    test = test.rename(columns = {'date':'Date','ticker':'Ticker'})
    test.to_csv(r'C:\users\admin\desktop\Pyspark\Weekly\Banknifty-V.csv',index=False)

if os.path.exists(r'C:\users\admin\desktop\Pyspark\Weekly\Banknifty-VI.csv'):
    os.remove(r'C:\users\admin\desktop\Pyspark\Weekly\Banknifty-VI.csv')
if os.path.exists(r'C:\Users\admin\Desktop\Pyspark_Contracts\Weekly_Data\BANKNIFTY_Weekly-VI.csv'):    
    test = pd.read_csv(r"C:\Users\admin\Desktop\Pyspark_Contracts\Weekly_Data\BANKNIFTY_Weekly-VI.csv")
    test['ticker'] = test['ticker'].str[:9]
    test['NewSymbol'] = test['ticker'] + 'WEEKLY' + '-VI' + test['STRIKE_PR'].astype(int).astype(str) + test['OPTION_TYP']
    test['ticker'] = test['NewSymbol']
    test = test.drop(test.columns[9:18],axis=1)
    test = test.rename(columns = {'date':'Date','ticker':'Ticker'})
    test.to_csv(r'C:\users\admin\desktop\Pyspark\Weekly\Banknifty-VI.csv',index=False)

if os.path.exists(r'C:\users\admin\desktop\Pyspark\Weekly\Banknifty-VII.csv'):
    os.remove(r'C:\users\admin\desktop\Pyspark\Weekly\Banknifty-VII.csv')
if os.path.exists(r'C:\Users\admin\Desktop\Pyspark_Contracts\Weekly_Data\BANKNIFTY_Weekly-VII.csv'):
    test = pd.read_csv(r"C:\Users\admin\Desktop\Pyspark_Contracts\Weekly_Data\BANKNIFTY_Weekly-VII.csv")
    test['ticker'] = test['ticker'].str[:9]
    test['NewSymbol'] = test['ticker'] + 'WEEKLY' + '-VII' + test['STRIKE_PR'].astype(int).astype(str) + test['OPTION_TYP']
    test['ticker'] = test['NewSymbol']
    test = test.drop(test.columns[9:18],axis=1)
    test = test.rename(columns = {'date':'Date','ticker':'Ticker'})
    test.to_csv(r'C:\users\admin\desktop\Pyspark\Weekly\Banknifty-VII.csv',index=False)

if os.path.exists(r'C:\users\admin\desktop\Pyspark\Weekly\Banknifty-VIII.csv'):
    os.remove(r'C:\users\admin\desktop\Pyspark\Weekly\Banknifty-VIII.csv')
if os.path.exists(r'C:\Users\admin\Desktop\Pyspark_Contracts\Weekly_Data\BANKNIFTY_Weekly-VIII.csv'):
    test = pd.read_csv(r"C:\Users\admin\Desktop\Pyspark_Contracts\Weekly_Data\BANKNIFTY_Weekly-VIII.csv")
    test['ticker'] = test['ticker'].str[:9]
    test['NewSymbol'] = test['ticker'] + 'WEEKLY' + '-VIII' + test['STRIKE_PR'].astype(int).astype(str) + test['OPTION_TYP']
    test['ticker'] = test['NewSymbol']
    test = test.drop(test.columns[9:18],axis=1)
    test = test.rename(columns = {'date':'Date','ticker':'Ticker'})
    test.to_csv(r'C:\users\admin\desktop\Pyspark\Weekly\Banknifty-VIII.csv',index=False)

if os.path.exists(r'C:\users\admin\desktop\Pyspark\Weekly\Banknifty-IX.csv'):
    os.remove(r'C:\users\admin\desktop\Pyspark\Weekly\Banknifty-IX.csv')
if os.path.exists(r'C:\Users\admin\Desktop\Pyspark_Contracts\Weekly_Data\BANKNIFTY_Weekly-IX.csv'):    
    test = pd.read_csv(r"C:\Users\admin\Desktop\Pyspark_Contracts\Weekly_Data\BANKNIFTY_Weekly-IX.csv")
    test['ticker'] = test['ticker'].str[:9]
    test['NewSymbol'] = test['ticker'] + 'WEEKLY' + '-IX' + test['STRIKE_PR'].astype(int).astype(str) + test['OPTION_TYP']
    test['ticker'] = test['NewSymbol']
    test = test.drop(test.columns[9:18],axis=1)
    test = test.rename(columns = {'date':'Date','ticker':'Ticker'})
    test.to_csv(r'C:\users\admin\desktop\Pyspark\Weekly\Banknifty-IX.csv',index=False)

if os.path.exists(r'C:\users\admin\desktop\Pyspark\Weekly\Banknifty-X.csv'):
    os.remove(r'C:\users\admin\desktop\Pyspark\Weekly\Banknifty-X.csv')
if os.path.exists(r'C:\Users\admin\Desktop\Pyspark_Contracts\Weekly_Data\BANKNIFTY_Weekly-X.csv'):    
    test = pd.read_csv(r"C:\Users\admin\Desktop\Pyspark_Contracts\Weekly_Data\BANKNIFTY_Weekly-X.csv")
    test['ticker'] = test['ticker'].str[:9]
    test['NewSymbol'] = test['ticker'] + 'WEEKLY' + '-X' + test['STRIKE_PR'].astype(int).astype(str) + test['OPTION_TYP']
    test['ticker'] = test['NewSymbol']
    test = test.drop(test.columns[9:18],axis=1)
    test = test.rename(columns = {'date':'Date','ticker':'Ticker'})
    test.to_csv(r'C:\users\admin\desktop\Pyspark\Weekly\Banknifty-X.csv',index=False)

if os.path.exists(r'C:\users\admin\desktop\Pyspark\Weekly\Banknifty-XI.csv'):
    os.remove(r'C:\users\admin\desktop\Pyspark\Weekly\Banknifty-XI.csv')
if os.path.exists(r'C:\Users\admin\Desktop\Pyspark_Contracts\Weekly_Data\BANKNIFTY_Weekly-XI.csv'):    
    test = pd.read_csv(r"C:\Users\admin\Desktop\Pyspark_Contracts\Weekly_Data\BANKNIFTY_Weekly-XI.csv")
    test['ticker'] = test['ticker'].str[:9]
    test['NewSymbol'] = test['ticker'] + 'WEEKLY' + '-XI' + test['STRIKE_PR'].astype(int).astype(str) + test['OPTION_TYP']
    test['ticker'] = test['NewSymbol']
    test = test.drop(test.columns[9:18],axis=1)
    test = test.rename(columns = {'date':'Date','ticker':'Ticker'})
    test.to_csv(r'C:\users\admin\desktop\Pyspark\Weekly\Banknifty-XI.csv',index=False)

if os.path.exists(r'C:\users\admin\desktop\Pyspark\Weekly\Banknifty-XII.csv'):
    os.remove(r'C:\users\admin\desktop\Pyspark\Weekly\Banknifty-XII.csv')
if os.path.exists(r'C:\Users\admin\Desktop\Pyspark_Contracts\Weekly_Data\BANKNIFTY_Weekly-XII.csv'):    
    test = pd.read_csv(r"C:\Users\admin\Desktop\Pyspark_Contracts\Weekly_Data\BANKNIFTY_Weekly-XII.csv")
    test['ticker'] = test['ticker'].str[:9]
    test['NewSymbol'] = test['ticker'] + 'WEEKLY' + '-XII' + test['STRIKE_PR'].astype(int).astype(str) + test['OPTION_TYP']
    test['ticker'] = test['NewSymbol']
    test = test.drop(test.columns[9:18],axis=1)
    test = test.rename(columns = {'date':'Date','ticker':'Ticker'})
    test.to_csv(r'C:\users\admin\desktop\Pyspark\Weekly\Banknifty-XII.csv',index=False)

print("!!!Process Completed!!!")