import psycopg2
import time
from io import StringIO
import pandas as pd
import os
from datetime import datetime
from datetime import date
import numpy as np

index = input("ENTER THE INDEX YOU WANT IN THE FORMAT BELOW - \nBankNifty\nNifty\nFinNifty\n")
schema = input("ENTER THE SCHEMA OF WHOSE DATA YOU WANT - \nMonthlyI , MonthlyII , WeeklyI , QuarterlyI and so on\n")
hyphen_index = schema.find("I")

def EOD(year1, year2):
    print("CONVERTING TO EOD")
    for i in range(int(year1),int(year2)+1):
        df = pd.read_csv(rf"C:\\Users\\Admin\\Desktop\\{index}_{schema}_Data\\{index}_{schema}_"+str(i)+".csv")
        df = df.rename(columns={'ticker' : 'Ticker',
                                'date' : 'Date',
                                'time' : 'Time',
                                'open' : 'Open',
                                'high' : 'High', 
                                'low' : 'Low',
                                'close' : 'Close',
                                'volume' : 'Volume', 
                                'Open Int' : 'Open Interest'})
        df['Date'] = pd.to_datetime(df['Date'], dayfirst=True)
        df = df.sort_values(by=['Date'])

        ## CHANGE AS PER USER INPUT
        symbol = index.upper()
        j='-' + schema[hyphen_index:]
        schema_find = schema[:hyphen_index].upper()

        final_df = df.copy()
        final_df['Final_strike'] = final_df['Ticker'].str.replace(j, '')
        final_df['Final_strike'] = final_df['Final_strike'].str.replace(f'{index.upper()}'+schema_find, '').str.replace(f'{index.upper()}','').str.replace('CE', '').str.replace('PE', '')
        final_df['Final_strike'] = final_df['Final_strike'].astype(float)
        final_df['Option_Type'] = final_df['Ticker'].str[-2:]

        final_df = final_df.rename(columns={'Time' : 'Timestamp',
                                            'Open' : 'Adj_Open',
                                            'High' : 'Adj_High',
                                            'Low' : 'Adj_Low',
                                            'Close' : 'Adj_Close',
                                            'Volume' : 'Adj_Volume',
                                            'Open Interest' : 'Adj_OI',        
                                            'Option_type' : 'Option_Type'})
        final_df['Date'] = pd.to_datetime(final_df['Date'],dayfirst=True).dt.date
        final_df['Timestamp'] = pd.to_datetime(final_df['Timestamp']).dt.time
        final_df = final_df.sort_values(by=['Date', 'Timestamp'])
        final_df['Date'] = final_df['Date'].astype(str)
        final_df['Timestamp'] = final_df['Timestamp'].astype(str)
        final_df['Datetime'] = pd.to_datetime(final_df['Date'] + ' ' + final_df['Timestamp'], dayfirst=True)

        final_df = final_df.set_index("Datetime")
        final_df['Adj_OI_1'] = final_df['Adj_OI']

        df_eod = final_df.groupby(['Final_strike', 'Option_Type', pd.Grouper(freq='B')]).agg({"Adj_Open" : "first", 
                                                              "Adj_High" : "max",
                                                              "Adj_Low" : "min",
                                                              "Adj_Close" : "last", 
                                                              'Adj_Volume' : 'sum',
                                                              'Adj_OI' : 'first',
                                                              'Adj_OI_1' : 'last'})
        df_eod.columns = ["Adj_Open", "Adj_High", "Adj_Low", "Adj_Close", 'Adj_Volume', 'First_OI', 'Last_OI']
        df_eod = df_eod.reset_index()
        df_eod['rem'] = df_eod['Final_strike']%df_eod['Final_strike'].astype(int)
        df_eod.loc[df_eod['rem'] == 0, 'Ticker'] = symbol + schema_find + j +  df_eod['Final_strike'].astype(int).astype(str) + df_eod['Option_Type']
        df_eod.loc[df_eod['rem'] != 0, 'Ticker'] = symbol + schema_find + j + df_eod['Final_strike'].round(2).astype(str) + df_eod['Option_Type'] 

        df_eod = df_eod.sort_values(by=['Datetime', 'Final_strike'])
        df_eod = df_eod.rename(columns={'Datetime' : 'Date'})
        ddf = df_eod.copy()
        ddf['Date'] = pd.to_datetime(ddf['Date'],dayfirst=True)
        ## CHECKING IF NULL VALUES
        ddf_OI = ddf.copy()
        ddf_OI['New_OI'] = ddf_OI['Last_OI']
        ddf_OI = ddf_OI.rename(columns={'Adj_Open':'Open','Adj_High':'High','Adj_Low':'Low','Adj_Close':'Close','Adj_Volume':'Volume','New_OI':'Open_Interest'})
        ddf_OI = ddf_OI.drop(['First_OI','Last_OI','Option_Type','Final_strike','rem'],axis=1)
        ddf_OI = ddf_OI[['Ticker','Date','Time','Open','High','Low','Close','Volume','Open_Interest']]
        ddf_OI.to_csv(fr"C:\users\admin\desktop\\{index}_{schema}_Data\\{index}_{schema}.csv",mode='a',header= not os.path.exists(fr"C:\users\admin\desktop\\{index}_{schema}_Data\\{index}_{schema}.csv"),index=False)
        os.remove(rf"C:\\Users\\Admin\\Desktop\\{index}_{schema}_Data\\{index}_{schema}_"+str(i)+".csv")

def fifteen_min(year1, year2):
    print("CONVERTING TO 15Min")
    for i in range(int(year1),int(year2)+1):
        df = pd.read_csv(rf"C:\\Users\\Admin\\Desktop\\{index}_{schema}_Data\\{index}_{schema}_"+str(i)+".csv")
        df = df.rename(columns={'ticker' : 'Ticker',
                                'date' : 'Date',
                                'time' : 'Time',
                                'open' : 'Open',
                                'high' : 'High', 
                                'low' : 'Low',
                                'close' : 'Close',
                                'volume' : 'Volume', 
                                'Open Int' : 'Open Interest'})
        df['Date'] = pd.to_datetime(df['Date'], dayfirst=True)
        df = df.sort_values(by=['Date'])

        ## CHANGE AS PER USER INPUT
        symbol = index.upper()
        j='-' + schema[hyphen_index:]
        schema_find = schema[:hyphen_index].upper()

        final_df = df.copy()
        final_df['Final_strike'] = final_df['Ticker'].str.replace(j, '')
        final_df['Final_strike'] = final_df['Final_strike'].str.replace(f'{index.upper()}'+schema_find, '').str.replace(f'{index.upper()}','').str.replace('CE', '').str.replace('PE', '')
        final_df['Final_strike'] = final_df['Final_strike'].astype(float)
        final_df['Option_Type'] = final_df['Ticker'].str[-2:]

        final_df = final_df.rename(columns={'Time' : 'Timestamp',
                                            'Open' : 'Adj_Open',
                                            'High' : 'Adj_High',
                                            'Low' : 'Adj_Low',
                                            'Close' : 'Adj_Close',
                                            'Volume' : 'Adj_Volume',
                                            'Open Interest' : 'Adj_OI',        
                                            'Option_type' : 'Option_Type'})
        final_df['Date'] = pd.to_datetime(final_df['Date'],dayfirst=True).dt.date
        final_df['Timestamp'] = pd.to_datetime(final_df['Timestamp']).dt.time
        final_df = final_df.sort_values(by=['Date', 'Timestamp'])
        final_df['Date'] = final_df['Date'].astype(str)
        final_df['Timestamp'] = final_df['Timestamp'].astype(str)
        final_df['Datetime'] = pd.to_datetime(final_df['Date'] + ' ' + final_df['Timestamp'], dayfirst=True)

        final_df = final_df.set_index("Datetime")
        final_df['Adj_OI_1'] = final_df['Adj_OI']

        df_eod = final_df.groupby(['Final_strike', 'Option_Type', pd.Grouper(freq='15min')]).agg({"Adj_Open" : "first", 
                                                              "Adj_High" : "max",
                                                              "Adj_Low" : "min",
                                                              "Adj_Close" : "last", 
                                                              'Adj_Volume' : 'sum',
                                                              'Adj_OI' : 'first',
                                                              'Adj_OI_1' : 'last'})
        df_eod.columns = ["Adj_Open", "Adj_High", "Adj_Low", "Adj_Close", 'Adj_Volume', 'First_OI', 'Last_OI']
        df_eod = df_eod.reset_index()
        df_eod['rem'] = df_eod['Final_strike']%df_eod['Final_strike'].astype(int)
        df_eod.loc[df_eod['rem'] == 0, 'Ticker'] = symbol + schema_find + j +  df_eod['Final_strike'].astype(int).astype(str) + df_eod['Option_Type']
        df_eod.loc[df_eod['rem'] != 0, 'Ticker'] = symbol + schema_find + j + df_eod['Final_strike'].round(2).astype(str) + df_eod['Option_Type'] 

        df_eod = df_eod.sort_values(by=['Datetime', 'Final_strike'])
        df_eod = df_eod.rename(columns={'Datetime' : 'Date'})
        ddf = df_eod.copy()
        ddf['Time'] = pd.to_datetime(ddf['Date']).dt.time
        ddf['Date'] = pd.to_datetime(ddf['Date'],dayfirst=True).dt.date
        ## CHECKING IF NULL VALUES
        ddf_OI = ddf.copy()
        ddf_OI['New_OI'] = ddf_OI['Last_OI']
        ddf_OI = ddf_OI.rename(columns={'Adj_Open':'Open','Adj_High':'High','Adj_Low':'Low','Adj_Close':'Close','Adj_Volume':'Volume','New_OI':'Open_Interest'})
        ddf_OI = ddf_OI.drop(['First_OI','Last_OI','Option_Type','Final_strike','rem'],axis=1)
        ddf_OI = ddf_OI[['Ticker','Date','Time','Open','High','Low','Close','Volume','Open_Interest']]
        ddf_OI.to_csv(fr"C:\users\admin\desktop\\{index}_{schema}_Data\\{index}_{schema}.csv",mode='a',header= not os.path.exists(fr"C:\users\admin\desktop\\{index}_{schema}_Data\\{index}_{schema}.csv"),index=False)
        os.remove(rf"C:\\Users\\Admin\\Desktop\\{index}_{schema}_Data\\{index}_{schema}_"+str(i)+".csv")

def five_min(year1,year2):
    print("CONVERTING TO 5Min")
    for i in range(int(year1),int(year2)+1):
        df = pd.read_csv(rf"C:\\Users\\Admin\\Desktop\\{index}_{schema}_Data\\{index}_{schema}_"+str(i)+".csv")
        df = df.rename(columns={'ticker' : 'Ticker',
                                'date' : 'Date',
                                'time' : 'Time',
                                'open' : 'Open',
                                'high' : 'High', 
                                'low' : 'Low',
                                'close' : 'Close',
                                'volume' : 'Volume', 
                                'Open Int' : 'Open Interest'})
        df['Date'] = pd.to_datetime(df['Date'], dayfirst=True)
        df = df.sort_values(by=['Date'])

        ## CHANGE AS PER USER INPUT
        symbol = index.upper()
        j='-' + schema[hyphen_index:]
        schema_find = schema[:hyphen_index].upper()

        final_df = df.copy()
        final_df['Final_strike'] = final_df['Ticker'].str.replace(j, '')
        final_df['Final_strike'] = final_df['Final_strike'].str.replace(f'{index.upper()}'+schema_find, '').str.replace(f'{index.upper()}','').str.replace('CE', '').str.replace('PE', '')
        final_df['Final_strike'] = final_df['Final_strike'].astype(float)
        final_df['Option_Type'] = final_df['Ticker'].str[-2:]

        final_df = final_df.rename(columns={'Time' : 'Timestamp',
                                            'Open' : 'Adj_Open',
                                            'High' : 'Adj_High',
                                            'Low' : 'Adj_Low',
                                            'Close' : 'Adj_Close',
                                            'Volume' : 'Adj_Volume',
                                            'Open Interest' : 'Adj_OI',        
                                            'Option_type' : 'Option_Type'})
        final_df['Date'] = pd.to_datetime(final_df['Date'],dayfirst=True).dt.date
        final_df['Timestamp'] = pd.to_datetime(final_df['Timestamp']).dt.time
        final_df = final_df.sort_values(by=['Date', 'Timestamp'])
        final_df['Date'] = final_df['Date'].astype(str)
        final_df['Timestamp'] = final_df['Timestamp'].astype(str)
        final_df['Datetime'] = pd.to_datetime(final_df['Date'] + ' ' + final_df['Timestamp'], dayfirst=True)

        final_df = final_df.set_index("Datetime")
        final_df['Adj_OI_1'] = final_df['Adj_OI']

        df_eod = final_df.groupby(['Final_strike', 'Option_Type', pd.Grouper(freq='5min')]).agg({"Adj_Open" : "first", 
                                                              "Adj_High" : "max",
                                                              "Adj_Low" : "min",
                                                              "Adj_Close" : "last", 
                                                              'Adj_Volume' : 'sum',
                                                              'Adj_OI' : 'first',
                                                              'Adj_OI_1' : 'last'})
        df_eod.columns = ["Adj_Open", "Adj_High", "Adj_Low", "Adj_Close", 'Adj_Volume', 'First_OI', 'Last_OI']
        df_eod = df_eod.reset_index()
        df_eod['rem'] = df_eod['Final_strike']%df_eod['Final_strike'].astype(int)
        df_eod.loc[df_eod['rem'] == 0, 'Ticker'] = symbol + schema_find + j +  df_eod['Final_strike'].astype(int).astype(str) + df_eod['Option_Type']
        df_eod.loc[df_eod['rem'] != 0, 'Ticker'] = symbol + schema_find + j + df_eod['Final_strike'].round(2).astype(str) + df_eod['Option_Type'] 

        df_eod = df_eod.sort_values(by=['Datetime', 'Final_strike'])
        df_eod = df_eod.rename(columns={'Datetime' : 'Date'})
        ddf = df_eod.copy()
        ddf['Time'] = pd.to_datetime(ddf['Date']).dt.time
        ddf['Date'] = pd.to_datetime(ddf['Date'],dayfirst=True).dt.date
        ## CHECKING IF NULL VALUES
        ddf_OI = ddf.copy()
        ddf_OI['New_OI'] = ddf_OI['Last_OI']
        ddf_OI = ddf_OI.rename(columns={'Adj_Open':'Open','Adj_High':'High','Adj_Low':'Low','Adj_Close':'Close','Adj_Volume':'Volume','New_OI':'Open_Interest'})
        ddf_OI = ddf_OI.drop(['First_OI','Last_OI','Option_Type','Final_strike','rem'],axis=1)
        ddf_OI = ddf_OI[['Ticker','Date','Time','Open','High','Low','Close','Volume','Open_Interest']]
        ddf_OI.to_csv(fr"C:\users\admin\desktop\\{index}_{schema}_Data\\{index}_{schema}.csv",mode='a',header= not os.path.exists(fr"C:\users\admin\desktop\\{index}_{schema}_Data\\{index}_{schema}.csv"),index=False)
        os.remove(rf"C:\\Users\\Admin\\Desktop\\{index}_{schema}_Data\\{index}_{schema}_"+str(i)+".csv")

def one_min(year1,year2):
    for i in range(int(year1),int(year2)+1):
        df = pd.read_csv(rf"C:\\Users\\Admin\\Desktop\\{index}_{schema}_Data\\{index}_{schema}_"+str(i)+".csv")
        df = df.rename(columns={'ticker' : 'Ticker',
                                'date' : 'Date',
                                'time' : 'Time',
                                'open' : 'Open',
                                'high' : 'High', 
                                'low' : 'Low',
                                'close' : 'Close',
                                'volume' : 'Volume', 
                                'Open Int' : 'Open Interest'})
        df['Date'] = pd.to_datetime(df['Date'], dayfirst=True)
        df = df.sort_values(by=['Date'])

        ## CHANGE AS PER USER INPUT
        symbol = index.upper()
        j='-' + schema[hyphen_index:]
        schema_find = schema[:hyphen_index].upper()

        final_df = df.copy()
        final_df['Final_strike'] = final_df['Ticker'].str.replace(j, '')
        final_df['Final_strike'] = final_df['Final_strike'].str.replace(f'{index.upper()}'+schema_find, '').str.replace(f'{index.upper()}','').str.replace('CE', '').str.replace('PE', '')
        final_df['Final_strike'] = final_df['Final_strike'].astype(float)
        final_df['Option_Type'] = final_df['Ticker'].str[-2:]

        final_df = final_df.rename(columns={'Time' : 'Timestamp',
                                            'Open' : 'Adj_Open',
                                            'High' : 'Adj_High',
                                            'Low' : 'Adj_Low',
                                            'Close' : 'Adj_Close',
                                            'Volume' : 'Adj_Volume',
                                            'Open Interest' : 'Adj_OI',        
                                            'Option_type' : 'Option_Type'})
        final_df['Date'] = pd.to_datetime(final_df['Date'],dayfirst=True).dt.date
        final_df['Timestamp'] = pd.to_datetime(final_df['Timestamp']).dt.time
        final_df = final_df.sort_values(by=['Date', 'Timestamp'])
        final_df['Date'] = final_df['Date'].astype(str)
        final_df['Timestamp'] = final_df['Timestamp'].astype(str)
        final_df['Datetime'] = pd.to_datetime(final_df['Date'] + ' ' + final_df['Timestamp'], dayfirst=True)

        final_df = final_df.set_index("Datetime")
        final_df['Adj_OI_1'] = final_df['Adj_OI']

        df_eod = final_df.groupby(['Final_strike', 'Option_Type', pd.Grouper(freq='1min')]).agg({"Adj_Open" : "first", 
                                                              "Adj_High" : "max",
                                                              "Adj_Low" : "min",
                                                              "Adj_Close" : "last", 
                                                              'Adj_Volume' : 'sum',
                                                              'Adj_OI' : 'first',
                                                              'Adj_OI_1' : 'last'})
        df_eod.columns = ["Adj_Open", "Adj_High", "Adj_Low", "Adj_Close", 'Adj_Volume', 'First_OI', 'Last_OI']
        df_eod = df_eod.reset_index()
        df_eod['rem'] = df_eod['Final_strike']%df_eod['Final_strike'].astype(int)
        df_eod.loc[df_eod['rem'] == 0, 'Ticker'] = symbol + schema_find + j +  df_eod['Final_strike'].astype(int).astype(str) + df_eod['Option_Type']
        df_eod.loc[df_eod['rem'] != 0, 'Ticker'] = symbol + schema_find + j + df_eod['Final_strike'].round(2).astype(str) + df_eod['Option_Type'] 

        df_eod = df_eod.sort_values(by=['Datetime', 'Final_strike'])
        df_eod = df_eod.rename(columns={'Datetime' : 'Date'})
        ddf = df_eod.copy()
        ddf['Time'] = pd.to_datetime(ddf['Date']).dt.time
        ddf['Date'] = pd.to_datetime(ddf['Date'],dayfirst=True).dt.date
        ## CHECKING IF NULL VALUES
        ddf_OI = ddf.copy()
        ddf_OI['New_OI'] = ddf_OI['Last_OI']
        ddf_OI = ddf_OI.rename(columns={'Adj_Open':'Open','Adj_High':'High','Adj_Low':'Low','Adj_Close':'Close','Adj_Volume':'Volume','New_OI':'Open_Interest'})
        ddf_OI = ddf_OI.drop(['First_OI','Last_OI','Option_Type','Final_strike','rem'],axis=1)
        ddf_OI = ddf_OI[['Ticker','Date','Time','Open','High','Low','Close','Volume','Open_Interest']]
        ddf_OI.to_csv(fr"C:\users\admin\desktop\\{index}_{schema}_Data\\{index}_{schema}.csv",mode='a',header= not os.path.exists(fr"C:\users\admin\desktop\\{index}_{schema}_Data\\{index}_{schema}.csv"),index=False)
        os.remove(rf"C:\\Users\\Admin\\Desktop\\{index}_{schema}_Data\\{index}_{schema}_"+str(i)+".csv")


conn = psycopg2.connect(database=f"{index}db",
                        user='postgres', password='swancap123',
                        host='swandatabase.cfehmk2wtejq.ap-south-1.rds.amazonaws.com', port='5432'
)
date1 = input("Enter start date as YYYY-MM-DD ")
date2 = input("Enter end date as YYYY-MM-DD ")
conversion = input("Enter 1 for 1 minute, 5 for 5 minutes, 15 for 15 minutes, E for EOD\n")
conn.autocommit = True
cursor = conn.cursor()
buffer = StringIO()
st=time.time()

## CREATING A DIRECTORY OF THE REQUIRED INDEX AND SCHEMA
if not os.path.exists(rf"C:\\users\\admin\\desktop\\{index}_{schema}_Data\\"):
    os.makedirs(rf"C:\users\admin\desktop\\{index}_{schema}_Data\\")
    
## CHECKING IF THE FILE ALREADY EXISTS 
# if os.path.exists(f"C:\\Users\\Admin\\Desktop\\{index}_{schema}_Data\\{index}_{schema}_"+str(i)+".csv"):
#     os.remove(f"C:\\Users\\Admin\\Desktop\\{index}_{schema}_Data\\{index}_{schema}_"+str(i)+".csv")

date1 = datetime.strptime(date1, "%Y-%m-%d").date()
date2 = datetime.strptime(date2, "%Y-%m-%d").date()
year1 = date1.year
year2 = date2.year

for i in range(int(year1),int(year2)+1):
    ddate1 = '-01-01'
    ddate2 = '-12-31'
    year_start = str(str(i)+ddate1)
    year_end = str(str(i)+ddate2)
    year_start = datetime.strptime(year_start, "%Y-%m-%d").date()
    year_end = datetime.strptime(year_end, "%Y-%m-%d").date()
    if date1 > year_start :
        year_start = date1
    else:
        year_start = year_start
    if year_end > date2 :
        year_end = date2
    else:
        year_end = year_end
    sql=f"COPY (select *from \"{index}{schema}\".select_datewise(\'{year_start}\',\'{year_end}\')) TO STDOUT WITH DELIMITER ',' CSV HEADER"
    print("Generating data from ", year_start , " to " , year_end)
    with open(f"C:\\Users\\Admin\\Desktop\\{index}_{schema}_Data\\{index}_{schema}_"+str(i)+".csv", "w") as file:
        cursor.copy_expert(sql, file)
if conversion == 'E':
    df = EOD(year1, year2)
    print("FILE CREATED")

elif conversion == '15':
    df = fifteen_min(year1, year2)
    print("FILE CREATED")

elif conversion == '5':
    df = five_min(year1,year2)
    print("FILE CREATED")

elif conversion == '1':
    print("FILE CREATED")
    
conn.commit()
conn.close()
et=time.time()

elapsed_time=et-st;
print("FILE GENERATED!")
print("elapsed_time:",elapsed_time)
