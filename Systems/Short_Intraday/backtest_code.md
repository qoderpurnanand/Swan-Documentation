## Inputs:

Entry time: 091500 

Exit time: 151000 or stoploss

Transaction Cost: 0.15%

Timeframe: Backtested on daily and 5 minute timeframe

MaxPos: 15

Stoploss: 6/10 ATR or min 2% or max 8%

Ef: 0.1

Vp: 4

## Database Details:

DB Name: Network\iMAC2\f\All databases\Equities\ F&O Equities (EOD database)
Watchlist: F&O Equities

DB Name: Network\iMAC2\f\All databases\Futures\ Futures Database (Continuous)
Watchlist: All symbols


Database and Backtest Settings:
 
![image](https://user-images.githubusercontent.com/63246619/183023236-95755c3f-946b-4393-8438-181fe5dbda31.png)



## PROCESS:

•	Run the short intraday average ranking code on F&O Equites database and add to composite the selected ranks 

•	Use the includeok EQ and banlist EQ code from Database maintenance and add in #include folder and filter the stocks while ranking. Backtest can be done without banlist code too

•	Copy the composite symbols from the current database folder and paste it in Futures Database folder and delete broker master file

•	Run the backtest code on on Futures database

•	Use custom backtester code and add it in #include folder. Change the number of maxpos in it depending on the maxpos in backtest. Currently 15.

•	Use the expiry selection code and add it in #include folder for selection of expiry since we trade next expiry on last day

•	The whole backtest can also be done on F&O equities instead of futures database to check the overall optimization results

*For expiry selection, includeok and banlist codes – refer to database maintenance.*

