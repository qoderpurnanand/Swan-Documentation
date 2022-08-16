
# STBT

INTRODUCTION : -
   STBT is an acronym for "Sell Today, Buy Tomorrow". Stocks on the Downward Trajectory that fulfill a minimum percentage criteria from the Open of the day 
   till any given time are given a Rank and are Short Sold if they come under the top nth rank .These Stocks are then squared off at the early minutes of 
   the very next trading session.


PROCESS : -
1) A Trend Analysis (Analysing the price action during the day and the very next day) is done on all the stocks that belong / have belonged to the F&O List.
    The Analysis is done on the "F&O Equities" Database within the Equities subfolder of the All Database folder on the Common Drive (Drive E:).
   
2) Within the "F&O Equities" Database, there is a "F&O Stocks" watchlist. On that watchlist, run the Trend Analysis AFL Code on Amibroker.
   [AmibrokerTrendAnalysis]
   https://github.com/qodeinvestments/Swan-Documentation/blob/595a1eb90e4b7f4922b4d50ea811ebe68cf368ca/Systems/STBT/Amibroker_Codes/AmibrokerTrendAnalysis
      
3) The Output from Amibroker is then saved on a CSV File. On the CSVFile the Python Trend Analysis code is run.
   [PythonTrendAnalysis]
   https://github.com/qodeinvestments/Swan-Documentation/blob/4008f1f1cf08673c902e6211869a1be14a1ca75e/Systems/STBT/Amibroker_Codes/AmibrokerTrendAnalysis

4) The above analysis is done only on Equities. The same analysis is then done on Future Symbols. There is an "All Symbols" watchlist on the 
   "Futures Database (Continuous)" within the Futures subfolder of the All Database folder on the Common Drive (Drive E:). 

5) Analysis is then done using different percentages moves which have their starting points at different times.

6) Once a graphical representation of the trend is done on Python, we go ahead with doing an exhaustive Optimization and Backtest on Amibroker.

7) Two versions have been backtested. One is Shorting at a particular time and the other is Shorting throughout the day.Within each of them there are two
   different methadologies adopted. One is where the Ranking is done on the Equity Symbols and Backtest is done on Future Symbols and the other one is 
   where Ranking and the Backtest are done on Future Symbols.
   All the codes are mentioned below: [STBTShortRankTimeEquityRankingFutureTrade]
   https://github.com/qodeinvestments/Swan-Documentation/blob/8c7e2032edf510ea9d4886ef4c41c7f9a91f7c51/Systems/STBT/Amibroker_Codes/STBTShortRankTimeEquityRankingFutureTrade.afl
   [STBTShortRankTimeFutureRankingFutureTrade]
   https://github.com/qodeinvestments/BTST/blob/756d6b8076b22f1e95334900e9e63fc2930e65e5/Amibroker_Codes/BTSTBuyRankTimeFutureRankingFutureTrade.afl
   [STBTShortAllDayEquityRankingFutureTrade]
   https://github.com/qodeinvestments/BTST/blob/292bc13547fc7a3e8d36d76be2954729222d1e83/Amibroker_Codes/BTSTBuyAllDayEquityRankingFutureTrade.afl
   [STBTShortAllDayFutureRankingFutureTrade]
   https://github.com/qodeinvestments/BTST/blob/756d6b8076b22f1e95334900e9e63fc2930e65e5/Amibroker_Codes/BTSTBuyAllDayFutureRankingFutureTrade.afl
   
   In case the Backtest is where Ranking is done on Equities and Trading on the Futures, the ranking has to be done on the "F&O Equities" database first.
   For that to be done, this particular code needs to be run [BTSTRankingCompositeSymbols]
   https://github.com/qodeinvestments/BTST/blob/de841f1b8edf1993bb6908b9ee526bf1b5056ed8/Amibroker_Codes/BTSTRankingCompositeSymbols
   Once the Composite symbols are created, they are copied on to the "Futures Database (Continuous)" and the Optimizations and backtest continues from 
   there onwards.
   
 8) The following variables have been optimized for Ranking on Equity and Backtest on Equity and for Buying at RankTime and Buying All Day: 
    a) MaxOpenPositions b) RankTime c) MaxTime d) GapPercent e) SellTime. Also Optimizations have been done for GapPercent using 090700 Open and 091500
    Open. Similarly,the same set of Variables have been optimized for Ranking on Futures and Backtest on Futures and for Ranking on Equity and Backtest on Futures
    for Buying at RankTime and Buying All Day. All the Optimizations have been saved on 
    E:\Dropboximac\Dropbox\Strategy Testing\BTST\2022\BTST Optimizations (01012013 - 31122021) on the E: Drive.
    
 9) Every Backtest code mentioned above also has a Limit Order Logic to it which is commented in the code. To use that snippet, uncomment it and then comment  
    the normal Buy, Sell rules.  
   


