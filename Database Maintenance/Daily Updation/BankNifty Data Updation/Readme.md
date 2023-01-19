# DAILY UPDATION OF BANKNIFTY DATA AND CREATING CONTINUOUS CONTRACTS

## PROCESS :
  1. From the Raw Data that is updated every day, we filter out BankNifty data and create Monthly, Weekly, Quarterly, Half-Yearly and Yearly Continuous Contracts.
  2. The codes for the same are given here - <br/>
      a) [Monthly Continuous Contracts <br/>](https://github.com/qodeinvestments/Swan-Documentation/blob/main/Database%20Maintenance/Daily%20Updation/BankNifty%20Data%20Updation/Continuous_Contracts.py)
      b) [Weekly Continuous Contracts](https://github.com/qodeinvestments/Swan-Documentation/blob/main/Database%20Maintenance/Daily%20Updation/BankNifty%20Data%20Updation/Continuous_Contracts_Weekly.py) <br/>
      c) [Quarterly Continuous Contracts](https://github.com/qodeinvestments/Swan-Documentation/blob/main/Database%20Maintenance/Daily%20Updation/BankNifty%20Data%20Updation/Continuous_Contracts_Quarterly.py) <br/>
      d) [Half-Yearly Continuous Contracts](https://github.com/qodeinvestments/Swan-Documentation/blob/main/Database%20Maintenance/Daily%20Updation/BankNifty%20Data%20Updation/Continuous_Contracts_HalfYearly.py) <br/>
      e) [Yearly Continuous Contracts](https://github.com/qodeinvestments/Swan-Documentation/blob/main/Database%20Maintenance/Daily%20Updation/BankNifty%20Data%20Updation/Continuous_Contracts_Yearly.py) <br/>
 3. These files are stored locally (daily gets modified) in the system and updated to the database.
 4. If the number of rows present in these files do not match the number of rows being added to Postgres database, an error is thrown.
 5. In such a case, we delete entries for that particular date and run the updation code again.
 6. The **Updation Code** for BankNifty Monthly Contracts is given here - [Updation Code](https://github.com/qodeinvestments/Swan-Documentation/blob/main/Database%20Maintenance/Daily%20Updation/BankNifty%20Data%20Updation/BankNiftyDailyUpdation.py) and the **Deletion Code** for the same is given here [Deletion Code](https://github.com/qodeinvestments/Swan-Documentation/blob/main/Database%20Maintenance/Daily%20Updation/BankNifty%20Data%20Updation/DeleteBNData.py)

**NOTE - The updation and deletion codes are the same; the only difference being the table and schema name.**
