## NSE500 ATRRanking Review: 24.11.2022

### Introduction:-

This is the review for the NSE500 ATRRanking System.The purpose for this review is that we want to compare the Live results with the Backtest
Results. A system like NSE500 has a lot of moving parts due to which there can be several discrepancies between the Live and Backtest results,therefore the
review of such a system is necessary.Following process has been adopted for the review.

Period: 13.01.2022 - 24.11.2022
Slippage: Matched with Live(take same for BT)
Reference: Dropbox---> KavanRanking ---> Rankingsheets with Date(Rankingdate is one day prior to trade_Date)
Excludeok Code: From 02-03-2022 onwards: [Excludeok](https://github.com/qodeinvestments/Swan-Documentation/blob/main/Systems/NSE500/nse500_excludeok_24.11.2022)

### Process: - 

Step1: Generate Backtest ranking and then hit the backtest.  

Step2: Match Trades: Match trade count and unique symbols for each day

### Review:

1. Only 60% trades are matching because of the Excludeok List(Stocks banned from trading by the broker): Lots of difference in the stocks placed

2. Re-done Analysis by Excluding those stocks that are in the ban list: Matching Trades: 86% 

![image](https://user-images.githubusercontent.com/67407393/209287776-c339438d-d8dc-4697-85da-e73084fb84ec.png)

### Conclusion:
1. Overall system has done better becuase of more volatile stocks and better entry time:09.15.00
2. We were unable to match the system because of Ban List
3. If tried with another broker we could do well

It might be worthwhile to trade this sytem with another broker. 
           
### Full Backtest           
![image](https://user-images.githubusercontent.com/67407393/209302167-4a41a4d4-a6a4-4cfc-adc7-e9395942c31a.png)
           
###Overall Trading Edge:
![image](https://user-images.githubusercontent.com/67407393/209302394-32e2d93c-747d-4706-9690-b7b98604c0b5.png)

