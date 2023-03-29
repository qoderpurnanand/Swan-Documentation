## CODES FOR DAILY UPDATION:

This repository contains the codes for creating Continuous Contracts for BankNifty, Nifty and FinNifty and appending the data on to SQL.

## PROCESS 

1. From the RawDataBase, we fetch BankNifty/Nifty/FinNifty data.
2. To create contracts, we can use the code(s) given in the link -<br/>
   [BankNifty](https://github.com/qodeinvestments/Swan-Documentation/blob/main/Database%20Maintenance/SQL/BankNifty_Daily_Contracts.ipynb)<br/>
   [Nifty](https://github.com/qodeinvestments/Swan-Documentation/blob/main/Database%20Maintenance/SQL/Nifty_Daily_Contracts.ipynb)<br/>
   [FinNifty](https://github.com/qodeinvestments/Swan-Documentation/blob/main/Database%20Maintenance/SQL/FinNifty_Daily_Contracts.ipynb)<br/>
3. Once these contracts are created, we need to append the data onto the particular schema in the database, code for which is given here [Daily Updation Code](https://github.com/qodeinvestments/Swan-Documentation/blob/main/Database%20Maintenance/SQL/Daily_Updation_Code.ipynb)
4. In case of any errors, we can use the [Deletion Code](https://github.com/qodeinvestments/Swan-Documentation/blob/main/Database%20Maintenance/SQL/Deletion_Code_UserInput.ipynb) to delete a entry for a particular date (date here is an input).

## CODE TO FETCH DATA FROM SQL
BEFORE RUNNING THIS CODE, MAKE SURE ALL THE LIBRARIES OF PYTHON ARE INSTALLED.
   <br/>Required libraries - <br/>
      ***pyspark***<br/>
      ***tqdm***<br/>
      ***psycopg2***<br/>
<br/>The below code is used to fetch data from SQL, which would contain user inputs such as - Index, Schema, Date Range, Timeframe<br/>
[Fetch Data](https://github.com/qodeinvestments/Swan-Documentation/blob/main/Database%20Maintenance/SQL/Fetch_data_without_tqdm.py)

