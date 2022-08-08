## MONTHLY MEAN REVERSION (MMR):
Monthly mean reversion system is a futures trading strategy that buys top 10 futures as based on LTI Indicator:
1.	 lti = ROC(EMA(Close,EMALLB),llb) + ROC(EMA(Close,EMALLB+10),llb) + ROC(EMA(Close,EMALLB+20),llb)
1.	EMALLB = 10
2.	Llb = 10
According to the Daily ROC trend analysis on F&O list, there is an upward trend during the last 4-6 days till the end of month and the highest on the first day of the next month. (Refer to the sheet Dropbox\Study\Long Mean Reversion Daily ROC.xlsx)
 ![image](https://user-images.githubusercontent.com/63246619/183395347-af61447e-4907-48fc-90ad-b13fb77d0200.png)


**Mention the different entry/exit signals for the particular system-**<br/>
Stock selection: EQ symbols  (Rank = 30) First 10 stocks selected based on lti.<br/>
Currently run 3 systems with entry on 3 different days: 5, 4 and 3 days before month end. Since MMR positions are open only for the last 5 days of the month, the funds lie idle throughout the month. To avoid this, we combined BTST and MMR as one system and don’t run BTST when MMR positions are about to open.<br/>
Entry Signals: low < btrig and time > 09:55am on Day1 and 09:15am from Day2.<br/>
Exit Signals: time = 093000 and day = 1st day of the next month<br/>
Expiry Symbol: Trading all Next Expiries<br/>
The avg CAR from 1/1/2014 to 1/11/2021 is 12% with the drawdown of 10.5% at 1x leverage; trading edge 0.99%.<br/>

