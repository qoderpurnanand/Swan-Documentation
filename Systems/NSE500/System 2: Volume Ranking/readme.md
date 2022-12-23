## NSE500 VolRanking Review: 24.11.2022

### Introduction:-

This is the review for the NSE500 VolumeRanking System.The purpose for this review is that we want to compare the Live results with the Backtest
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
Overall Performance Drop has been seen in the system compared to the previous years:
1. Curve Fitting of the system
2. Reduction in Trading Edge
3. Overall Trend Analysis shows a Smile: Stocks rising at EOD
4. Excludeok does not make so much of a difference

#### Full Backtest without Excludeok
![image](https://user-images.githubusercontent.com/67407393/209301514-bf82fbb9-8dc3-44d1-8a07-f6d8a68b2901.png)

#### Trading Edge Year Wise
![image](https://user-images.githubusercontent.com/67407393/209301650-c5deaadc-39fb-4c99-bcdf-9dbe7d06f965.png)




           
               
