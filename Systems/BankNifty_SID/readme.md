## INTRODUCTION:-

BankNifty Weekly Short Options Intraday (BNW SID) is a Short Options Intraday Strategy on Weekly Current Expiries of the Bank Nifty Index.EveryDay an 
Out-of-the-Money or At-The-Money Call and Put having the same expiration date are sold.A Percentage Stop Loss on the price of the Option are kept and once 
the Stop Loss is triggered,that particular leg is squared off and the other leg (if any remaining) are squraed off at the end of the day.

## PROCESS:-

1) Initially a simple backtest was done.This backtest is done on the BankNifty (Weekly Continuous Contracts) Database on the "All Symbols" watchlist 
   which is in Amibroker/Index Option/Options of the All Database folder on the Common Drive (Drive E:).The Variables optimized were 1) Entry Time 2) Exit Time 3) Stop Loss Percentage 4) POE 5) Leverage. All these Optimizations are saved in 
   Strategy Testing/Short Options/BankNifty Weekly Short Options on DropBox. The critical part in this code is the calculation of Minimum Premium which is 
   the Margin needed for opening a straddle (based on the leverage input) multiplied by the Percent Of Equity (POE) divided by the Current Lot Size.
   Position Size is linked to this Minimum Premium value. 
   
 2) Similarly, different strikes were optimized that ranged from One strike In-the-Money to 5 strikes Out-Of-The-Money. All those Optimizations are saved in
    Strategy Testing/Short Options/BankNifty Weekly Short Options on DropBox. The Variables optimized were 1) Entry Time 2) Exit Time 3) Stop Loss Percentage 
    4) POE 5) Leverage. In some cases even DTE was optimized.The backtest codes for all of them are exactly the same as AT-The-Money. The only difference is 
    that the Strike Price Selector has to be modified if a different strike has to be traded.   
    
 3) Instead of going short either only At-The-Money or Out-of-the-Money, we optimized the strikes for each day so ideally we would be trading different 
    strikes every day.The Optimizations are saved in Strategy Testing/Short Options/BankNifty Weekly Short Options on DropBox. Even the Stop Loss Percentage
    has been optimized differently for every day rather than having a fixed percentage stop. Along with the Strikes and stop Loss Percentage,
    the Entry Time, Exit Time,POE and Leverage is also optimized. The Backtest code for this is also the same as the At-The-Money code. 
    Only The strike selection is being controlled from the Strike Price Selector.
    
4) Lastly, we tried having a more Dynamic Strike Selection process. In our earlier codes Minimum Premium was mostly being used as a factor for the Position
   Sizing. We now use Minimum Premium not only as a factor in position sizing but also to help select which strike to trade. The Option Price from the
   Option Chain which is closest to the Minimum Premium is traded.Variables Optimized were 1) Entry Time 2) Exit Time 3) Stop Loss Percentage 4) POE
   5) Levearge. All these Optimizations are saved in Strategy Testing/Short Options/BankNifty Weekly Short Options on DropBox. The Backtest Code for the
   same can be found here.
   
5) Earlier in All Intraday (MIS) Options Strategies the NSE gave upto 25x Leverage. Since September 2021, this was changed and the Leverage was bought down to
   12x which is what all Overnight (NRML) Option Strategies get. Eventually, trading spreads is what we tried as that helps in reducing the Margin Required.
   Variables Optimized were same as the earlier strategies. The additional varaible being the Long Strike that ranged from 1 strike to alomost 20 strikes out.
   The Strike Selection for the long strike is also controlled from the Strike Price Selector. The Optimizations are saved in Strategy Testing/Short   
   Options/BankNifty Weekly Short Options on DropBox. This was tested with the short strike selection being At-The-Money,Out-Of-The-Money and Minimum Premium.
   Both those codes are here.
   [BankNiftyShortOptions(ATM-OTM + Long](https://github.com/qodeinvestments/BankNifty-Weekly-ShortOptions-Intraday-/blob/e05de78f8072eef29511f93b6e4c571d429dbe47/Live_Codes/BankNiftyWeeklyShortOptions(ATM-OTM%20+%20Long)) and 
   [BankNiftyShortOptions(MinPremium + Long](https://github.com/qodeinvestments/BankNifty-Weekly-ShortOptions-Intraday-/blob/eda9e3ae0d5e34203a052e7448452a2e30b9aeee/Live_Codes/BankNiftyWeeklyShortOptions(MinPremium%20+%20Long)) The latter code needs to be run on the
   same database i.e "BankNifty (Weekly Continuous Contracts)" but on the "All Symbols DHF" watchlist. This code can only be run when there are no data holes.
   The variables that were optimized are the same as the ones mentioned in the earlier strategy additionally with the Long Strike being optimized to decide how 
   many strikes further from the Short Strike should the Long option be bought. Depending on the moneyness of the Long Leg, the leverage changes. All the different
   versions and optimizations of this variant can be found in in Strategy Testing/Short Options/BankNifty Weekly Short Options on DropBox.
   
## VERSIONS:-   

Currently for Live we are running the Minimum Premium Logic for Strike Selection and using a 3% POE and 12x Leverage for Strike Selection and 12x also for Position
Sizing. StopLoss has been optimized such that there is a different Percentage Stop Loss for Every Day. Exit Time is 15:15:00pm. There is no Optimial Timing for
Entry therefore we are trading 6 different systems spanning from 09:45:00am to 12:30:00pm with a gap of around 30-45 minutes between each system. Below is a list 
of all the different variations we have tried (as of 16/06/2022) with BankNifty Weekly Short Options: 

a) EntryTime,ExitTime,StopLoss Percentage,Long Option(Protection)Moneyness,Short Option Moneyness,Leverage,Percent Of Equity have been Optimized.(For All Versions)
b) Minimum Premium Logic has been tested.
c) With Regards to Long Options, Squaring off the Long Leg along with respective Short Leg at the same time and Squaring Off the Leg Long EOD have been tested.
   (For All Versions)
d) For Long, Buying OTM Strikes in multiples of 100 for Bank Nifty have been tested. Protection as a Percentage of Short Strike has also been tested.(For ATM,OTM)
e) With regards to Long, Buying Monthly Options while going Short Weekly Options has been tested.(For ATM,OTM)
f) With Respect to Leverage, Buying No protection when Max Upside is there and No extra Leverage when Long Options cannot be opened has been tested.(For ATM,OTM)
g) Going Short ITM Strikes (100) has been tested.(For ATM,OTM)
h) All this has been done on a 5 Min Time Frame.
j) Different StopLosses Tried - % Move in the Option, % Of Move in BankNifty and 3 Day ATR Of the Index. % StopLoss on the Option Price is the best.(Only Tried for        Minimum Premium Logic)
    
