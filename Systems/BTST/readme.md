## BUY TODAY SELL TOMORROW:
BTST system is a futures trading strategy that buys top 10 futures as based on 1 Indicator. Currently running the system at 3 timings and different gaps:
1.	Gap: Close at 110000/091500 open – 1 >= 3%
2.	Gap: Close at 120000/091500 open – 1 >= 3.5%
3.	Gap: Close at 130000/091500 open – 1 >= 4%<br/>
This strategy aims to take advantage of overnight gains. According to the trend analysis, the F&O stocks gain overnight and not intraday. <br/>
Mention the different entry/exit signals for the particular system-<br/>
Stock selection: EQ symbols <br/>
Entry Signals: Gap: Close at entrytime/exittime open – 1 > gap%<br/>
Exit Signals: next day morning 091700,092400,093000<br/>
Expiry Symbol: Trading all Same Expiries, except for last 2 days where we open next expiry as margin for same expiry is higher.<br/>
Limit orders are placed that gets modified every 1 minute for 5 minutes. This reduces slippage that happens cause of REL orders.<br/>

## PROCESS: -
1. A Trend Analysis (Analysing the price action during the day and the very next day) is done on all the stocks that belong / have belonged to the F&O List. The Analysis is done on the "F&O Equities" Database within the Equities subfolder of the All Database folder on the Common Drive (Drive E:).<br/>
2. Within the "F&O Equities" Database, there is a "F&O Stocks" watchlist. On that watchlist, run the Trend Analysis AFL Code on Amibroker. [AmiBrokerTrendAnalysis](https://github.com/qodeinvestments/Swan-Documentation/blob/main/Systems/Trend_Analysis/AmibrokerTrendAnalysis.md)<br/>
3. The Output from Amibroker is then saved on a CSV File. On the CSVFile the Python Trend Analysis code is run. [PythonTrendAnalysis](https://github.com/qodeinvestments/Swan-Documentation/blob/main/Systems/Trend_Analysis/PythonTrendAnalysis.ipynb)<br/>
4. The above analysis is done only on Equities. The same analysis is then done on Future Symbols. There is an "All Symbols" watchlist on the "Futures Database (Continuous)" within the Futures subfolder of the All Database folder on the Common Drive (Drive E:).<br/>
5. Analysis is then done using different percentages moves which have their starting points at different times.<br/>
6. Once a graphical representation of the trend is done on Python, we go ahead with doing an exhaustive Optimization and Backtest on Amibroker.<br/>
7. Two versions have been backtested. One is buying at a particular time and the other is buying throughout the day.Within each of them there are different methadologies adopted. One is where the Ranking and Backtest is done on the Equities Symbols. The other is where Ranking is done on the Equity Symbols and Backtest is done on Future Symbols and lastly where Ranking and the Backtest is done on Future Symbols. All the codes are mentioned below: <br/>
[BTSTBuyAllDayEquityRankingFutureTrade](https://github.com/qodeinvestments/Swan-Documentation/blob/main/Systems/BTST/Backtest_Code/BTSTBuyAllDayEquityRankingFutureTrade.md) <br/>
[BTSTBuyAllDayEquityRankingEquityTrade](https://github.com/qodeinvestments/Swan-Documentation/blob/main/Systems/BTST/Backtest_Code/BTSTBuyAllDayEquityRankingEquityTrade.md) <br/>
[BTSTBuyAllDayFutureRankingFutureTrade](https://github.com/qodeinvestments/Swan-Documentation/blob/main/Systems/BTST/Backtest_Code/BTSTBuyAllDayFutureRankingFutureTrade.md) <br/>
[BTSTBuyRankTimeEquityRankingFutureTrade](https://github.com/qodeinvestments/Swan-Documentation/blob/main/Systems/BTST/Backtest_Code/BTSTBuyRankTimeEquityRankingFutureTrade.md) <br/>
[BTSTBuyRankTimeEquityRankingEquityTrade](https://github.com/qodeinvestments/Swan-Documentation/blob/main/Systems/BTST/Backtest_Code/BTSTBuyRankTimeEquityRankingEquityTrade.md) <br/>
[BTSTBuyRankTimeFutureRankingFutureTrade](https://github.com/qodeinvestments/Swan-Documentation/blob/main/Systems/BTST/Backtest_Code/BTSTBuyRankTimeFutureRankingFutureTrade.md) <br/>
In case the Backtest is where Ranking is done on Equities and Trading on the Futures, the ranking has to be done on the "F&O Equities" database first. For that to be done, this particular code needs to be run [BTSTRankingCompositeSymbols](https://github.com/qodeinvestments/Swan-Documentation/blob/main/Systems/BTST/Backtest_Code/BTSTRankingCompositeSymbols.md). Once the Composite symbols are created, they are copied on to the "Futures Database (Continuous)" and the Optimizations and backtest continues from there onwards.<br/>
8. The following variables have been optimized for Ranking on Equity and Backtest on Equity and for Buying at RankTime and Buying All Day: a) MaxOpenPositions b) RankTime c) MaxTime d) GapPercent e) SellTime. Also Optimizations have been done for GapPercent using 090700 Open and 091500 Open. Similarly,the same set of Variables have been optimized for Ranking on Futures and Backtest on Futures and for Ranking on Equity and Backtest on Futures for Buying at RankTime and Buying All Day. All the Optimizations have been saved on E:\Dropboximac\Dropbox\Strategy Testing\BTST\2022\BTST Optimizations (01012013 - 31122021) on the E: Drive.<br/>
9. Every Backtest code mentioned above also has a Limit Order Logic to it which is commented in the code. To use that snippet, uncomment it and then comment the normal Buy, Sell rules.)<br/>

## VERSIONS: -
The current variant of BTST that we are running live is the one where the Gap is calculated from the days open. Alternatively we have tried two More Variations: 
1. The Gap is being calculated from Previous Day's Close as opposed to Current Day's Open. There was no significant improvement in the results in the results. No Optimizations or Backtest for are saved.
2. Fundamental Filters like ROCE and Market Cap were added to the existing BTST System to see if those filters added any value. The ROCE and Market Cap data was got from Ace Equity and Imported onto the "F&O Equities" database. Ranking and Trading is being done on Equities and the code can be found here: [BTSTBuyRankTimeFundamentalFilters](https://github.com/qodeinvestments/Swan-Documentation/blob/main/Systems/BTST/Backtest_Code/BTSTBuyRankTimeFundamentalFilters.md).
The Optimizations is saved on E:\Dropboximac\Dropbox\Strategy Testing\BTST\2022\BTST with Fundamental Filters on the E: Drive. The Filters did not add any value.
