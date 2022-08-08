## Inputs:
Entry time: > 095500 on Day1; >091500 from day2 <br/>
Exit time: From 093000 to 094500 <br/>
Transaction Cost: 0.05% on LMT orders 0.15% on Close <br/>
Timeframe: Backtested on daily and 5 minute timeframe <br/>
MaxPos: 10 <br/>
MMR1ef: 0.4 ; MMR2ef: 0.3 ; MMR3ef: 0.2 ;<br/>
Vp: 5 <br/>
LMT order vp: 25<br/>
LMT ordered: 0.1<br/>

## Rules: 
Entry and Exit LMT orders to be modified every 5 minutes till 15 minutes.<br/>
For backtesting on 5 minute timeframe, the ranking code is different than the execution code. <br/>
The backtest was originally done on a daily timeframe to check system strength.

## Database Details:

DB Name: Network\iMAC2\f\All databases\Equities\F&O Equities (EOD database)
Watchlist: F&O Equities

The backtest is only done on EQ database. Futures database does not have next expiry symbol data for MMR days.

## Database and Backtest Settings:
Backtest has been done on daily as well as 5 minute timeframe. The system strength is checked on Daily timeframe backtest. Only for the LMT orders, we require 5 minute timeframe.

![image](https://user-images.githubusercontent.com/63246619/183396828-56e11d48-af00-48b4-afa7-f531f5b993eb.png)
