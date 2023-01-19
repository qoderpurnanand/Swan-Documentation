# -*- coding: utf-8 -*-
"""
Created on Fri Nov 18 10:54:35 2022

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
import datetime

folpath = r"C:\users\admin\desktop\\Pyspark_Contracts\\"
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

ddf = bndata
ddf = ddf.loc[:, ~ddf.columns.str.contains('^Unnamed')]
ddf['date'] = pd.to_datetime(ddf['date'],dayfirst=True)
ddf['Optiontype'] = ddf['ticker'].str[-2:]
ddf['Temp'] = ddf['ticker'].str.replace('BANKNIFTY','')
ddf['Temp'] = ddf['Temp'].str[:-2]
ddf['Length_of_temp'] = np.where(ddf['Temp'].str.len()==12,12,ddf['Temp'].str.len())
ddf['Strike'] = np.where((ddf['Temp'].str.len()==12)|(ddf['Temp'].str.len()==10),ddf['Temp'].str[-5:],
                         ddf['Temp'].str[-4:])
ddf['Exp_year'] = np.where(ddf['Temp'].str.len()==12,ddf['Temp'].str[5:7],ddf['Temp'].str[:2])
ddf['Exp_month'] = ddf['Temp'].str[2:5]

#print(ddf.iloc[0,:])

## READING THE EXPIRY SHEET
exp_file_path = r"C:\Users\admin\Downloads\MonthlyExpiry.csv"
#exp_df = spark.read.options(header='True',inferSchema='True').csv(exp_file_path).dropna()
exp_df = pd.read_csv(exp_file_path,parse_dates=["curr_exp_date","curr_date"],dayfirst=True).dropna()
## CONVERTING TO PANDAS DATAFRAME
#exp_df = exp_df.toPandas()
exp_df.rename({'curr_date': 'New_date'}, axis=1, inplace=True)
exp_df['New_date'] = pd.to_datetime(exp_df['New_date'],dayfirst=True)
#print(exp_df)

exp_date = pd.read_excel(r'C:\users\admin\desktop\Expiry_DT.xlsx')
#print(exp_date)
ddf['Exp_year'] = ddf['Exp_year'].astype('str')
ddf['MonthYear'] = ddf['Exp_month'] + ddf['Exp_year']
merged_df = pd.merge(ddf,exp_date,on='MonthYear')
merged_df = merged_df.drop(['MonthYear','Month','Year'],axis=1)

start_time = datetime.datetime.strptime('09:15:00', '%H:%M:%S').time()
end_time = datetime.datetime.strptime('15:30:00', '%H:%M:%S').time()

merged_df['Length_of_temp'] = merged_df['Length_of_temp'].astype('int64')
df_10 = merged_df[(merged_df['Length_of_temp']==10) | (merged_df['Length_of_temp']==9)]
df_12 = merged_df[merged_df['Length_of_temp']==12]
df_12['DateDate'] = df_12['Temp'].str[:2]
df_12['DateDate'] = df_12['DateDate'].astype('int64')
df_12['Exp_DT'] = pd.to_datetime(merged_df['Exp_DT'],dayfirst=True)
df_12['Exp_Day'] = df_12['Exp_DT'].dt.day

df_12 = df_12[df_12['Exp_Day']==df_12['DateDate']]
df_12 = df_12.drop(['DateDate','Exp_Day'],axis=1)

ddf = df_10.append(df_12,ignore_index=True)
ddf['Time'] = ddf['Time'].str.replace(' 15:00:59','15:00:59')
ddf['Time'] = ddf['Time'].str.replace(' 9:','09:',regex=True)
ddf['Time'] = pd.to_datetime(ddf['Time'], format='%H:%M:%S').dt.time
ddf = ddf[(ddf['Time']>=start_time) & (ddf['Time']<=end_time)]


def add(stri):
    obj = datetime.datetime.strptime(stri, "%b")
    month_number = obj.month
    return month_number

ddf['exp_month_number'] = ddf.apply(lambda row : add(row["Exp_month"]), axis = 1)
#print(ddf)

ddf['New_date'] = date
ddf["New_date"] = pd.to_datetime(ddf["New_date"],dayfirst=True)
ddf["current_month_number"] = ddf['New_date'].dt.month
ddf["difference"] = ddf['exp_month_number'].astype(int) - ddf["current_month_number"].astype(int)
df1 = pd.merge(ddf, 
                 exp_df, 
                 on ='New_date', 
                 how ='left')
df1.drop(df1.filter(regex="Unname"),axis=1, inplace=True)
df1["current_exp_month_number"] = df1['curr_exp_date'].dt.month
df1["Diff_months"] = df1["current_exp_month_number"] - df1["current_month_number"]
df1["Diff_months"] = df1["Diff_months"].astype(int) 
bdf = df1[df1["Diff_months"] == 0]
adf = df1[(df1["Diff_months"] == 1) | (df1["Diff_months"] == -11)]
if bdf.shape[0] + adf.shape[0] == df1.shape[0]:
    print("Sanity Check Success")
else:
    print("Error1")
    
agb = adf.groupby(["difference"])
unique_val_list_a = list(adf["difference"].unique())
bgb = bdf.groupby(["difference"])
unique_val_list_b = list(bdf["difference"].unique())

if os.path.exists(folpath+sym+'-I.csv'):
    os.remove(folpath+sym+'-I.csv')
if os.path.exists(folpath+sym+'-II.csv'):
    os.remove(folpath+sym+'-II.csv')
if os.path.exists(folpath+sym+'-III.csv'):
    os.remove(folpath+sym+'-III.csv')
if os.path.exists(folpath+sym+'misc.csv'):
    os.remove(folpath+sym+'misc.csv')

for i in unique_val_list_b:
    temp_df = bgb.get_group(i)

    if i == 0:
        if not os.path.isfile(folpath + sym + '-I.csv'):
            temp_df.to_csv(folpath + sym + '-I.csv', index=False)
        else: # else it exists so append without writing the header
            temp_df.to_csv(folpath + sym + '-I.csv', mode='a', header=False, index=False)

    elif i == 1 or i == -11:
        if not os.path.isfile(folpath + sym + '-II.csv'):
            temp_df.to_csv(folpath + sym + '-II.csv', index=False)
        else: # else it exists so append without writing the header
            temp_df.to_csv(folpath + sym + '-II.csv', mode='a', header=False, index=False)

    elif i == 2 or i == -10:
        if not os.path.isfile(folpath + sym + '-III.csv'):
            temp_df.to_csv(folpath + sym + '-III.csv', index=False)
        else: # else it exists so append without writing the header
            temp_df.to_csv(folpath + sym + '-III.csv', mode='a', header=False, index=False)

    else:
        if not os.path.isfile(folpath + sym + 'misc.csv'):
            temp_df.to_csv(folpath + sym + 'misc.csv', index=False)
        else: # else it exists so append without writing the header
            temp_df.to_csv(folpath + sym + 'misc.csv', mode='a', header=False, index=False)

for i in unique_val_list_a:
    temp_df = agb.get_group(i)

    if i == 1 or i == -11:
        if not os.path.isfile(folpath + sym + '-I.csv'):
            temp_df.to_csv(folpath + sym + '-I.csv', index=False)
        else: # else it exists so append without writing the header
            temp_df.to_csv(folpath + sym + '-I.csv', mode='a', header=False, index=False)

    elif i == 2 or i == -10:
        if not os.path.isfile(folpath + sym + '-II.csv'):
            temp_df.to_csv(folpath + sym + '-II.csv', index=False)
        else: # else it exists so append without writing the header
            temp_df.to_csv(folpath + sym + '-II.csv', mode='a', header=False, index=False)

    elif i == 3 or i == -9:
        if not os.path.isfile(folpath + sym + '-III.csv'):
            temp_df.to_csv(folpath + sym + '-III.csv', index=False)
        else: # else it exists so append without writing the header
            temp_df.to_csv(folpath + sym + '-III.csv', mode='a', header=False, index=False)

    else:
        if not os.path.isfile(folpath + sym + 'misc.csv'):
            temp_df.to_csv(folpath + sym +'misc.csv', index=False)
        else: # else it exists so append without writing the header
            temp_df.to_csv(folpath + sym +'misc.csv', mode='a', header=False, index=False)

#print(df1)

## FOR CURRENT MONTH
if os.path.exists(r'C:\users\admin\desktop\Pyspark\Banknifty-I.csv'):
    os.remove(r'C:\users\admin\desktop\Pyspark\Banknifty-I.csv')
ddf = pd.read_csv(r"C:\users\admin\desktop\\Pyspark_Contracts\\BANKNIFTY-I.csv")
ddf['ticker'] = ddf['ticker'].str[:9]
ddf['NewSymbol'] = ddf['ticker'] + 'MONTHLY' + '-I' + ddf['Strike'].astype(int).astype(str) + ddf['Optiontype']
ddf['ticker'] = ddf['NewSymbol']
ddf = ddf.drop(ddf.columns[9:29],axis=1)
ddf = ddf.rename(columns = {'Date_x':'Date','ticker':'Ticker'})
ddf.to_csv(r'C:\users\admin\desktop\Pyspark\Banknifty-I.csv',index=False)

## FOR NEXT MONTH
if os.path.exists(r'C:\users\admin\desktop\Pyspark\Banknifty-II.csv'):
    os.remove(r'C:\users\admin\desktop\Pyspark\Banknifty-II.csv')
ddf = pd.read_csv(r"C:\users\admin\desktop\\Pyspark_Contracts\\BANKNIFTY-II.csv")
ddf['ticker'] = ddf['ticker'].str[:9]
ddf['NewSymbol'] = ddf['ticker'] + 'MONTHLY' + '-II' + ddf['Strike'].astype(int).astype(str) + ddf['Optiontype']
ddf['ticker'] = ddf['NewSymbol']
ddf = ddf.drop(ddf.columns[9:29],axis=1)
ddf = ddf.rename(columns = {'Date_x':'Date','ticker':'Ticker'})
ddf.to_csv(r'C:\users\admin\desktop\Pyspark\Banknifty-II.csv',index=False)

## FOR FAR MONTH
if os.path.exists(r'C:\users\admin\desktop\Pyspark\Banknifty-III.csv'):
    os.remove(r'C:\users\admin\desktop\Pyspark\Banknifty-III.csv')
ddf = pd.read_csv(r"C:\users\admin\desktop\\Pyspark_Contracts\\BANKNIFTY-III.csv")
ddf['ticker'] = ddf['ticker'].str[:9]
ddf['NewSymbol'] = ddf['ticker'] + 'MONTHLY' + '-III' + ddf['Strike'].astype(int).astype(str) + ddf['Optiontype']
ddf['ticker'] = ddf['NewSymbol']
ddf = ddf.drop(ddf.columns[9:29],axis=1)
ddf = ddf.rename(columns = {'Date_x':'Date','ticker':'Ticker'})
ddf.to_csv(r'C:\users\admin\desktop\Pyspark\Banknifty-III.csv',index=False)

et=time.time()

elapsed_time=et-st;
print("elapsed_time:",elapsed_time)
print("No of rows:",q.count())
print('BankNifty Data',len(bndata))

