## NSE500 VolRanking Review: 24.11.2022

### Introduction:-

This is the review for the NSE500 ATRRanking System.The purpose for this review is that we want to compare the Live results with the Backtest
Results. A system like NSE500 has a lot of moving parts due to which there can be several discrepancies between the Live and Backtest results,therefore the
review of such a system is necessary.Following process has been adopted for the review.

Period: 10.05.2022 - 24.11.2022
Slippage: Matched with Live(take same for BT)
Reference: Dropbox---> KavanRanking ---> Rankingsheets with Date(Rankingdate is one day prior to trade_Date)
Excludeok Code: From 02-03-2022 onwards: [Excludeok](https://github.com/qodeinvestments/Swan-Documentation/blob/main/Systems/NSE500/nse500_excludeok_24.11.2022)

### Process: - 

Step1: Generate Backtest ranking and then hit the backtest.  

Step2: Match Trades: Match trade count and unique symbols for each day

### Review:

1. Only 63% trades are matching because of two reasons : 
   a. Backtest Entry time is 09.20 and Live we are entering at 09.17am 
   b. Ban List
   
2. Re-done Analysis by Excluding those stocks that are in the ban list: Matching Trades: 76% 

![image](https://user-images.githubusercontent.com/67407393/209291834-2e19299e-0b17-4bc4-9e4a-8bf9c9a97939.png)

### Conclusion:
We have also done a backtets from "01-01-2013 to 24-11-2013". This backtest doesn't include the "NSE500 ExcludeOk" code as we dont have data on stocks
which were excluded from trading on a day to day basis from 2013 onwards. As seen in the backtest, 2022 has not been particularly a great year for the "ATR Ranking"
system. Nevertheless its been positive and similarly average performances were seen in a couple of earlier years. The ATRRanking System generally trades stocks 
which are a lot more volatile. Stocks that are banned from trading on any given day are the stocks which are volatile. This system breeds on volatility, so by not 
getting an opportunity to trade such stocks, the live returns we get may never match the backtested returns unless the Historical Backtest is been done with the 
Excludeok code which unfortunately we don not have.The last step we will adopt is to do a trend analysis with and without the "NSE500 ExcludeOk" code to see how stocks


It might be worthwhile to trade this sytem with another broker. 
           
               
