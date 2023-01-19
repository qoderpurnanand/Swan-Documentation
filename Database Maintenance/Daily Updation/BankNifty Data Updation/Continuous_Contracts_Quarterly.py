# -*- coding: utf-8 -*-
"""
Created on Wed Jan 18 11:01:30 2023

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
import warnings
warnings.filterwarnings("ignore")

folpath = r"C:\Users\admin\Desktop\Pyspark_Contracts\Quarterly_Data\\"
sym = 'BANKNIFTY'

start_time = datetime.datetime.strptime('09:15:00', '%H:%M:%S').time()
end_time = datetime.datetime.strptime('15:30:00', '%H:%M:%S').time()

def add(stri):
    obj = datetime.datetime.strptime(stri, "%b")
    month_number = obj.month
    return month_number

date = date(2023,1,18)                      ## to be changed daily
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

## GETTING ONLY time IN time COLUMN
q = df.withColumn('time',date_format('time', 'HH:mm:ss'))
#print(q.show())

## FILTERING BANK NIFTY DATA
bndata = q.filter(q.ticker.contains('BANKNIFTY') & (q.ticker.endswith('E.NFO')))

## REPLACING .NFO IN TICKER
bndata = bndata.withColumn('ticker',regexp_replace('ticker','.NFO',''))
#print(bndata.show())

## CONVERTING PYSPARK DATAFRAME TO PANDAS DATAFRAME
bndata=bndata.toPandas()

temp = bndata

exp_date = pd.read_excel(r'C:\users\admin\desktop\Expiry_DT.xlsx')    ## reading the expiry sheet file

exp_file_path = r"C:\Users\admin\Downloads\MonthlyExpiry.csv"
exp_df = pd.read_csv(exp_file_path,parse_dates = ["curr_exp_date","curr_date"],dayfirst =True,usecols = ["curr_exp_date","curr_date"]).dropna()
exp_df.rename({'curr_date': 'New_date'}, axis=1, inplace=True)

temp['time'] = temp['time'].astype(str).str.replace(' 15:00:59','15:00:59')
temp['time'] = temp['time'].str.replace(' 9:','09:',regex=True)
temp['ticker'] = temp['ticker'].str.replace('30MAR23','29MAR23',regex=True)
temp['time'] = pd.to_datetime(temp['time']).dt.time
temp['date'] = pd.to_datetime(temp['date'])
temp = temp[(temp['time']>=start_time) & (temp['time']<=end_time)]
temp = temp.loc[:, ~temp.columns.str.contains('^Unnamed')]
temp['Option_type'] = temp['ticker'].str[-2:]
temp["Temp"] = temp["ticker"].str.replace('BANKNIFTY',"")
temp["Temp"] = temp["Temp"].str[:-2]
temp["Strike"] = np.where((temp['Temp'].str.len()==12) | (temp['Temp'].str.len()==10),
                            temp['Temp'].str[-5:],
                            temp['Temp'].str[-4:])
temp['Current_Year'] = temp['date'].dt.year
temp['Current_Year'] = temp['Current_Year'].astype(str).str[-2:]
temp["Exp_year"] = np.where(temp['Temp'].str.len()==12,temp["Temp"].str[5:7],temp['Temp'].str[:2])
temp["Exp_month"] = temp["Temp"].str[2:5]
temp['Length_of_Temp'] = np.where(temp['Temp'].str.len()==12,12,temp['Temp'].str.len())
temp['Exp_year'] = temp['Exp_year'].astype('str')
temp['MonthYear'] = temp['Exp_month']+temp['Exp_year']
temp = pd.merge(temp,exp_date,on='MonthYear')
temp = temp.drop(['MonthYear','Month','Year'],axis=1)

temp['Length_of_Temp'] = temp['Length_of_Temp'].astype('int64')
temp_10 = temp[(temp['Length_of_Temp']==10) | (temp['Length_of_Temp']==9)]
temp_12 = temp[temp['Length_of_Temp']==12]
temp_12['datedate'] = temp_12['Temp'].str[:2]
temp_12['datedate'] = temp_12['datedate'].astype('int64')
temp_12['Exp_DT'] = pd.to_datetime(temp['Exp_DT'],dayfirst=True)
temp_12['Exp_Day'] = temp_12['Exp_DT'].dt.day
temp_12 = temp_12[temp_12['Exp_Day']==temp_12['datedate']]

temp_12 = temp_12.drop(['datedate','Exp_Day'],axis=1)
temp = temp_10.append(temp_12,ignore_index=True)

temp['exp_month_number'] = temp.apply(lambda row : add(row["Exp_month"]), axis = 1)
temp['New_date'] = temp['date']
temp["New_date"] = pd.to_datetime(temp["New_date"])
temp["current_month_number"] = temp['New_date'].dt.month
temp["difference"] = temp['exp_month_number'].astype(int) - temp["current_month_number"].astype(int)
temp['Year_difference'] = temp['Exp_year'].astype(int) - temp['Current_Year'].astype(int)
temp = temp[(temp['exp_month_number']==3) | (temp['exp_month_number']==6) | (temp['exp_month_number']==9) | (temp['exp_month_number']==12)]

temp1 = pd.merge(temp, 
                     exp_df, 
                     on ='New_date', 
                     how ='left')

temp1.drop(temp1.filter(regex="Unname"),axis=1, inplace=True)
temp1["current_exp_month_number"] = temp1['curr_exp_date'].dt.month
temp1["Diff_months"] = temp1["current_exp_month_number"] - temp1["current_month_number"]
temp1["Diff_months"] = temp1["Diff_months"].astype(int) 

temp1 = temp1[temp1['Exp_DT']>=temp1['curr_exp_date']]                 ## to filter out dates which have wrong ticker

## creating groups for generating contracts
atemp = temp1[(temp1['Diff_months']==0) & (temp1['Year_difference']==0)]
agb = atemp.groupby(['difference'])
unique_a = list(atemp['difference'].unique())

if os.path.exists(folpath+sym+'-I.csv'):
    os.remove(folpath+sym+'-I.csv')
if os.path.exists(folpath+sym+'-II.csv'):
    os.remove(folpath+sym+'-II.csv')
if os.path.exists(folpath+sym+'-III.csv'):
    os.remove(folpath+sym+'-III.csv')
if os.path.exists(folpath+sym+'-IV.csv'):
    os.remove(folpath+sym+'-IV.csv')
if os.path.exists(folpath+sym+'-V.csv'):
    os.remove(folpath+sym+'-V.csv')
if os.path.exists(folpath+sym+'-VI.csv'):
    os.remove(folpath+sym+'-VI.csv')
if os.path.exists(folpath+sym+'-VII.csv'):
    os.remove(folpath+sym+'-VII.csv')
if os.path.exists(folpath+sym+'-VIII.csv'):
    os.remove(folpath+sym+'-VIII.csv')    

for i in unique_a:
    temp_df = agb.get_group(i)
    temp_df = temp_df.drop(temp_df.columns[9:],axis=1)
    if i==0 or i==1 or i==2:
        temp_df.to_csv(folpath + sym + '-I.csv', mode='a', header=not os.path.exists(folpath + sym + '-I.csv'), index=False)

    if i==3 or i==4 or i==5:
        temp_df.to_csv(folpath + sym + '-II.csv', mode='a', header=not os.path.exists(folpath + sym + '-II.csv'), index=False)

    if i==6 or i==7 or i==8:
        temp_df.to_csv(folpath + sym + '-III.csv', mode='a', header=not os.path.exists(folpath + sym + '-III.csv'), index=False)

    if i==9 or i==10 or i==11:
        temp_df.to_csv(folpath + sym + '-IV.csv', mode='a', header=not os.path.exists(folpath + sym + '-IV.csv'), index=False)

btemp = temp1[(temp1['Diff_months']==0) & (temp1['Year_difference']==1)]
bgb = btemp.groupby(['difference'])
unique_b = list(btemp['difference'].unique())        

for i in unique_b:
    temp_df = bgb.get_group(i)
    temp_df = temp_df.drop(temp_df.columns[9:],axis=1)
    if i==-7 or i==-8 or i==-9:
        temp_df.to_csv(folpath + sym + '-II.csv', mode='a', header=not os.path.exists(folpath + sym + '-II.csv'), index=False)

    if i==-4 or i==-5 or i==-6:
        temp_df.to_csv(folpath + sym + '-III.csv', mode='a', header=not os.path.exists(folpath + sym + '-III.csv'), index=False)

    if i==-1 or i==-2 or i==-3:
        temp_df.to_csv(folpath + sym + '-IV.csv', mode='a', header=not os.path.exists(folpath + sym + '-IV.csv'), index=False)

    if i==0 or i==1 or i==2:
        temp_df.to_csv(folpath + sym + '-V.csv', mode='a', header=not os.path.exists(folpath + sym + '-V.csv'), index=False)

    if i==3 or i==4 or i==5:
        temp_df.to_csv(folpath + sym + '-VI.csv', mode='a', header=not os.path.exists(folpath + sym + '-VI.csv'), index=False)

    if i==6 or i==7 or i==8:
        temp_df.to_csv(folpath + sym + '-VII.csv', mode='a', header=not os.path.exists(folpath + sym + '-VII.csv'), index=False)

    if i==9 or i==10 or i==11:
        temp_df.to_csv(folpath + sym + '-VIII.csv', mode='a', header=not os.path.exists(folpath + sym + '-VIII.csv'), index=False)

ctemp = temp1[(temp1['Diff_months']==0) & (temp1['Year_difference']==2)]
cgb = ctemp.groupby(['difference'])
unique_c = list(ctemp['difference'].unique())        

for i in unique_c:
    temp_df = cgb.get_group(i)
    temp_df = temp_df.drop(temp_df.columns[9:],axis=1)
    if i==-7 or i==-8 or i==-9:
        temp_df.to_csv(folpath + sym + '-VI.csv', mode='a', header=not os.path.exists(folpath + sym + '-VI.csv'), index=False)

    if i==-4 or i==-5 or i==-6:
        temp_df.to_csv(folpath + sym + '-VII.csv', mode='a', header=not os.path.exists(folpath + sym + '-VII.csv'), index=False)

    if i==-1 or i==-2 or i==-3:
        temp_df.to_csv(folpath + sym + '-VIII.csv', mode='a', header=not os.path.exists(folpath + sym + '-VIII.csv'), index=False)

dtemp = temp1[((temp1['Diff_months']==1) | (temp1['Diff_months']==-11)) & (temp1['Year_difference']==0)]
dgb = dtemp.groupby(['difference'])
unique_d = list(dtemp['difference'].unique())

for i in unique_d:
    temp_df = dgb.get_group(i)
    temp_df = temp_df.drop(temp_df.columns[9:],axis=1)
    if i==1 or i==2 or i==3:
        temp_df.to_csv(folpath + sym + '-I.csv', mode='a', header=not os.path.exists(folpath + sym + '-I.csv'), index=False)

    if i==4 or i==5 or i==6:
        temp_df.to_csv(folpath + sym + '-II.csv', mode='a', header=not os.path.exists(folpath + sym + '-II.csv'), index=False)

    if i==7 or i==8 or i==9:
        temp_df.to_csv(folpath + sym + '-III.csv', mode='a', header=not os.path.exists(folpath + sym + '-III.csv'), index=False)

    if i==10 or i==11:
        temp_df.to_csv(folpath + sym + '-IV.csv', mode='a', header=not os.path.exists(folpath + sym + '-IV.csv'), index=False)

etemp = temp1[((temp1['Diff_months']==1) | (temp1['Diff_months']==-11)) & (temp1['Year_difference']==1)]
egb = etemp.groupby(['difference'])
unique_e = list(etemp['difference'].unique())

for i in unique_e:
    temp_df = egb.get_group(i)
    temp_df = temp_df.drop(temp_df.columns[9:],axis=1)
    if i==-9:
        temp_df.to_csv(folpath + sym + '-I.csv', mode='a', header=not os.path.exists(folpath + sym + '-I.csv'), index=False)

    if i==-6 or i==-7:
        temp_df.to_csv(folpath + sym + '-II.csv', mode='a', header=not os.path.exists(folpath + sym + '-II.csv'), index=False)

    if i==-3 or i==-4:
        temp_df.to_csv(folpath + sym + '-III.csv', mode='a', header=not os.path.exists(folpath + sym + '-III.csv'), index=False)

    if i==0 or i==-1 or i==-2:
        temp_df.to_csv(folpath + sym + '-IV.csv', mode='a', header=not os.path.exists(folpath + sym + '-IV.csv'), index=False)

    if i==1 or i==2 or i==3:
        temp_df.to_csv(folpath + sym + '-V.csv', mode='a', header=not os.path.exists(folpath + sym + '-V.csv'), index=False)

    if i==4 or i==5 or i==6:
        temp_df.to_csv(folpath + sym + '-VI.csv', mode='a', header=not os.path.exists(folpath + sym + '-VI.csv'), index=False)

    if i==7 or i==8 or i==9:
        temp_df.to_csv(folpath + sym + '-VII.csv', mode='a', header=not os.path.exists(folpath + sym + '-VII.csv'), index=False)

    if i==10 or i==11:
        temp_df.to_csv(folpath + sym + '-VIII.csv', mode='a', header=not os.path.exists(folpath + sym + '-VIII.csv'), index=False)

ftemp = temp1[((temp1['Diff_months']==1) | (temp1['Diff_months']==-11)) & (temp1['Year_difference']==2)]
fgb = ftemp.groupby(['difference'])
unique_f = list(ftemp['difference'].unique())

for i in unique_f:
    temp_df = fgb.get_group(i)
    temp_df = temp_df.drop(temp_df.columns[9:],axis=1)
    if i==-9:
        temp_df.to_csv(folpath + sym + '-V.csv', mode='a', header=not os.path.exists(folpath + sym + '-V.csv'), index=False)

    if i==-6 or i==-7:
        temp_df.to_csv(folpath + sym + '-VI.csv', mode='a', header=not os.path.exists(folpath + sym + '-VI.csv'), index=False)

    if i==-3 or i==-4:
        temp_df.to_csv(folpath + sym + '-VII.csv', mode='a', header=not os.path.exists(folpath + sym + '-VII.csv'), index=False)

    if i==0 or i==-1 or i==-2:
        temp_df.to_csv(folpath + sym + '-VIII.csv', mode='a', header=not os.path.exists(folpath + sym + '-VIII.csv'), index=False)
    
## CREATING THE TICKER AND REMOVING ADDITIONAL COLUMNS
if os.path.exists(r'C:\users\admin\desktop\Pyspark\Quarterly\Banknifty-I.csv'):
    os.remove(r'C:\users\admin\desktop\Pyspark\Quarterly\Banknifty-I.csv')
if os.path.exists(r"C:\Users\admin\Desktop\Pyspark_Contracts\Quarterly_Data\BANKNIFTY-I.csv"):
    df = pd.read_csv(r"C:\Users\admin\Desktop\Pyspark_Contracts\Quarterly_Data\BANKNIFTY-I.csv")
    test = df.copy()
    test['Option_Type'] = test['ticker'].str[-2:]
    test['Last'] = test['ticker'].str[-7:]
    test['Strike'] = test['Last'].astype('str').str.extractall('(\d+)').unstack().fillna('').sum(axis=1).astype(int)
    test['Symbol'] = test['ticker'].str[:9] + '-I' + test['Strike'].astype(str) + test['Option_Type'].astype(str)
    test['ticker'] = test['Symbol']
    test = test.drop(test.columns[9:13],axis=1)
    test = test.rename(columns = {'date':'Date','ticker':'Ticker','time':'Time','open':'Open','high':'High','low':'Low','close':'Close','volume':'Volume'})
    test.to_csv(r'C:\users\admin\desktop\Pyspark\Quarterly\Banknifty-I.csv',index=False)

if os.path.exists(r'C:\users\admin\desktop\Pyspark\Quarterly\Banknifty-II.csv'):
    os.remove(r'C:\users\admin\desktop\Pyspark\Quarterly\Banknifty-II.csv')
if os.path.exists(r"C:\Users\admin\Desktop\Pyspark_Contracts\Quarterly_Data\BANKNIFTY-II.csv"):
    df = pd.read_csv(r"C:\Users\admin\Desktop\Pyspark_Contracts\Quarterly_Data\BANKNIFTY-II.csv")
    test = df.copy()
    test['Option_Type'] = test['ticker'].str[-2:]
    test['Last'] = test['ticker'].str[-7:]
    test['Strike'] = test['Last'].astype('str').str.extractall('(\d+)').unstack().fillna('').sum(axis=1).astype(int)
    test['Symbol'] = test['ticker'].str[:9] + '-II' + test['Strike'].astype(str) + test['Option_Type'].astype(str)
    test['ticker'] = test['Symbol']
    test = test.drop(test.columns[9:13],axis=1)
    test = test.rename(columns = {'date':'Date','ticker':'Ticker','time':'Time','open':'Open','high':'High','low':'Low','close':'Close','volume':'Volume'})
    test.to_csv(r'C:\users\admin\desktop\Pyspark\Quarterly\Banknifty-II.csv',index=False)

if os.path.exists(r'C:\users\admin\desktop\Pyspark\Quarterly\Banknifty-III.csv'):
    os.remove(r'C:\users\admin\desktop\Pyspark\Quarterly\Banknifty-III.csv')
if os.path.exists(r"C:\Users\admin\Desktop\Pyspark_Contracts\Quarterly_Data\BANKNIFTY-III.csv"):
    df = pd.read_csv(r"C:\Users\admin\Desktop\Pyspark_Contracts\Quarterly_Data\BANKNIFTY-III.csv")
    test = df.copy()
    test['Option_Type'] = test['ticker'].str[-2:]
    test['Last'] = test['ticker'].str[-7:]
    test['Strike'] = test['Last'].astype('str').str.extractall('(\d+)').unstack().fillna('').sum(axis=1).astype(int)
    test['Symbol'] = test['ticker'].str[:9] + '-III' + test['Strike'].astype(str) + test['Option_Type'].astype(str)
    test['ticker'] = test['Symbol']
    test = test.drop(test.columns[9:13],axis=1)
    test = test.rename(columns = {'date':'Date','ticker':'Ticker','time':'Time','open':'Open','high':'High','low':'Low','close':'Close','volume':'Volume'})
    test.to_csv(r'C:\users\admin\desktop\Pyspark\Quarterly\Banknifty-III.csv',index=False)

if os.path.exists(r'C:\users\admin\desktop\Pyspark\Quarterly\Banknifty-IV.csv'):
    os.remove(r'C:\users\admin\desktop\Pyspark\Quarterly\Banknifty-IV.csv')
if os.path.exists(r"C:\Users\admin\Desktop\Pyspark_Contracts\Quarterly_Data\BANKNIFTY-IV.csv"):
    df = pd.read_csv(r"C:\Users\admin\Desktop\Pyspark_Contracts\Quarterly_Data\BANKNIFTY-IV.csv")
    test = df.copy()
    test['Option_Type'] = test['ticker'].str[-2:]
    test['Last'] = test['ticker'].str[-7:]
    test['Strike'] = test['Last'].astype('str').str.extractall('(\d+)').unstack().fillna('').sum(axis=1).astype(int)
    test['Symbol'] = test['ticker'].str[:9] + '-IV' + test['Strike'].astype(str) + test['Option_Type'].astype(str)
    test['ticker'] = test['Symbol']
    test = test.drop(test.columns[9:13],axis=1)
    test = test.rename(columns = {'date':'Date','ticker':'Ticker','time':'Time','open':'Open','high':'High','low':'Low','close':'Close','volume':'Volume'})
    test.to_csv(r'C:\users\admin\desktop\Pyspark\Quarterly\Banknifty-IV.csv',index=False)



et=time.time()

elapsed_time=et-st;
print("PROCESS COMPLETED!!!!!!")
print("elapsed_time:",elapsed_time)    

