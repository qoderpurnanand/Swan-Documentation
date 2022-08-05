# SHORT FLAT:

Objective:  Hedge for the Current Long Systems. Purpose is to make money in big bear markets. The system Is rotational in nature and Ranks stocks for Shorting. The system is either on cash or fully invested based on the Nifty Simple Moving Average. If nifty is below its average/its in a downtrend we want to open short positions in stocks that have shown a long term down trend.

Short flat system is a futures trading strategy that shorts futures as based on 1 Indicator:
1.	Nifty Index < MA(Nifty Index,10)

System has been tested, optimized and results saved.

This version will take STI as an Entry Indicator. sti = (ROC(EMA(Close,emallb),Slb) + ROC(EMA(Close,emallb+20),slb) + ROC(EMA(Close,emallb+40),slb))

The system ranks the top 15 symbols based on STI and shorts them. The worst rank held is 20. It the current open symbol rank is > 20, we re-rank and short the next best rank and exit the position.

Mention the different entry/exit signals for the particular system-

Entry Signals: Nifty < 10 MA of nifty and sti < 0

Exit Signals: Nifty > 10 MA of nifty or rank > worst rank

The average CAR is 10% with a drawdown of 30% from 2014 – 2022.

This system is used as a hedge to the current QGF system. When the equity curves are combined, the drawdown is reduced.




