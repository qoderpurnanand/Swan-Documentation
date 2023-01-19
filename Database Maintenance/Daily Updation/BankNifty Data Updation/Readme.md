# DAILY UPDATION OF BANKNIFTY DATA AND CREATING CONTINUOUS CONTRACTS

## PROCESS :
  1. From the Raw Data that is updated every day, we filter out BankNifty data and create Monthly, Weekly, Quarterly, Half-Yearly and Yearly Continuous Contracts.
  2. The codes for the same are given here - <br/>
      a) Monthly Continuous Contracts <br/>
      b) Weekly Continuous Contracts <br/>
      c) Quarterly Continuous Contracts <br/>
      d) Half-Yearly Continuous Contracts <br/>
      e) Yearly Continuous Contracts <br/>
 3. These files are stored locally (daily gets modified) in the system and updated to the database.
 4. If the number of rows present in these files do not match the number of rows being added to Postgres database, an error is thrown.
 5. In such a case, we delete entries for that particular date and run the updation code again.
 6. The updation code for BankNifty Monthly Contracts is given here - "Code to be pasted" and the deletion code for the same is as "Code to be pasted"

**NOTE - The updation and deletion codes are the same; the only difference being the table and schema name.**
