# -*- coding: utf-8 -*-
"""
Created on Wed Jan 18 14:51:37 2023

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
warnings.filterwarnings('ignore')


if os.path.exists(r"C:\Users\admin\Desktop\Pyspark\Yearly\\Banknifty-I.csv"):
    os.remove(r"C:\Users\admin\Desktop\Pyspark\Yearly\\Banknifty-I.csv")
    
final_df = pd.DataFrame()
file = 'I'
add_file = 'I'
for i in range(2):
    print(i,file)
    if os.path.exists(r"C:\Users\admin\Desktop\Pyspark_Contracts\Quarterly_Data\BANKNIFTY-"+str(file)+".csv"):  
        df = pd.read_csv(r"C:\Users\admin\Desktop\Pyspark_Contracts\Quarterly_Data\BANKNIFTY-"+str(file)+".csv")
        temp = df.copy()
        temp = temp.rename(columns = {'ticker':'Ticker','date':'Date','time':'Time','open':'Open','low':'Low','high':'High','close':'Close','volume':'Volume'})
        temp['Time'] = pd.to_datetime(temp['Time']).dt.time
        temp['Date'] = pd.to_datetime(temp['Date'])
        temp = temp.loc[:, ~temp.columns.str.contains('^Unnamed')]
        temp['Option_type'] = temp['Ticker'].str[-2:]
        temp["Temp"] = temp["Ticker"].str.replace('BANKNIFTY',"")
        temp["Temp"] = temp["Temp"].str[:-2]
        temp["Strike"] = np.where((temp['Temp'].str.len()==12) | (temp['Temp'].str.len()==10),
                                    temp['Temp'].str[-5:],
                                    temp['Temp'].str[-4:])
        temp['Current_Year'] = temp['Date'].dt.year
        temp['Current_Year'] = temp['Current_Year'].astype(str).str[-2:]
        temp["Exp_year"] = np.where(temp['Temp'].str.len()==12,temp["Temp"].str[5:7],temp['Temp'].str[:2])
        temp["Exp_month"] = temp["Temp"].str[2:5]
        temp['Length_of_Temp'] = np.where(temp['Temp'].str.len()==12,12,temp['Temp'].str.len())
        temp = temp[(temp['Exp_month']=='DEC')]
        temp = temp.reset_index(drop=True)
        final_df = final_df.append(temp)
        final_df = final_df.reset_index(drop=True)
        final_df = final_df.drop(final_df.columns[9:],axis=1)
        if i==2:
            file='IV'
        else:
            file+=add_file
        
    else:
        print("BANKNIFTY QUARTERLY-"+str(file)+" does not exist")

if final_df.empty==False:
    test = final_df.copy()
    test['Option_Type'] = test['Ticker'].str[-2:]
    test['Last'] = test['Ticker'].str[-7:]
    test['Strike'] = test['Last'].astype('str').str.extractall('(\d+)').unstack().fillna('').sum(axis=1).astype(int)
    test['Symbol'] = test['Ticker'].str[:9] + '-I' + test['Strike'].astype(str) + test['Option_Type'].astype(str)
    test['Ticker'] = test['Symbol']
    test = test.drop(test.columns[9:13],axis=1)
    print("BANKNIFTY YEARLY-I CREATED")
    test.to_csv(r"C:\Users\admin\Desktop\Pyspark\Yearly\\Banknifty-I.csv",index=False)

else:
    print("Dataframe is empty!!!")