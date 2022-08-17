# Nifty-Weekly-ShortOptions-Intraday-

INTRODUCTION:-

Nifty Weekly Short Options Intraday (NW SID) is a Short Options Intraday Strategy on Weekly Current Expiries of the Nifty Index.EveryDay an 
Out-of-the-Money or At-The-Money Call and Put having the same expiration date are sold.A Percentage Stop Loss on the price of the Options are kept and once 
the Stop Loss is triggered,that particular leg is squared off and the other leg (if any remaining) are squraed off at the end of the day.

PROCESS:-

1) While testing Weekly Options, All the analysis was done on BankNifty. It started with first testing ATM Options on BankNifty, then OTM Options and 
   then finalizing on a Dynamic Strike Selvetion based on Minimum Premium. In case Of Nifty Weekly Short Options, Only OTM Strikes and Dynamic Strikes were tested
   rather than ATM Strikes.This backtest is done on the Nifty (Weekly Continuous Contracts) Database on the "All Symbols" watchlist 
   which is in Amibroker/Index Option/Options of the All Database folder on the Common Drive (Drive E:). Using the Nifty Weekly StrikePriceSelector we select              going short a Strangle (OTM Call and Put) for the current expiry. A certain Percentage Stop Loss is kept on the option premium and the leg(s) where the stop loss      is not triggered, are squared of at the end of the day.That code can be found here:[NiftyWeeklyShortOPtions(ATM-OTM)]
   https://github.com/qodeinvestments/Swan-Documentation/blob/a71d6815ca11327e9de6f06aa2ce6fa6d292a0bc/Systems/Nifty_SID/Backtest_Codes/NiftyWeeklyShortOptions(ATM-OTM). The Variables optimized were 1) Entry Time 2) Exit Time 3) Stop Loss Percentage 4) POE 5) Leverage. All these Optimizations are saved in 
   Strategy Testing/Short Options/BankNifty Weekly Short Options on DropBox. The critical part in this code is the calculation of Minimum Premium which is 
   the Margin needed for opening a Strangle (based on the leverage input) multiplied by the Percent Of Equity (POE) divided by the Current Lot Size.
   Position Size is linked to this Minimum Premium value.
   
2) Also we have optimized as to which strike should be opened on which day.All those Optimizations are saved in 
   Strategy Testing/Short Options/Nifty Weekly Short Options on DropBox.Th strike selector has to be modified in a certain way so that the strike selector can            incorporate taking different strikes on different days.Even the Stop Loss Percentage has been optimized differently for every day rather than having a 
   fixed percentage stop. 

3) Lastly, we tried having a more Dynamic Strike Selection process. In our earlier codes Minimum Premium was mostly being used as a factor for the Position
   Sizing. We now use Minimum Premium not only as a factor in position sizing but also to help select which strike to trade. The Option Price from the
   Option Chain which is closest to the Minimum Premium is traded.Variables Optimized were 1) Entry Time 2) Exit Time 3) Stop Loss Percentage 4) POE
   5) Levearge. All these Optimizations are saved in Strategy Testing/Short Options/Nifty Weekly Short Options on DropBox. The Backtest Code for the
   same can be found here.[NiftyWeeklyShortOptions(MinPremium)]
   https://github.com/qodeinvestments/Swan-Documentation/blob/a71d6815ca11327e9de6f06aa2ce6fa6d292a0bc/Systems/Nifty_SID/Backtest_Codes/NiftyWeeklyShortOptions(MinPremium)
   
4) Earlier in All Intraday (MIS) Options Strategies the NSE gave upto 25x Leverage. Since September 2021, this was changed and the Leverage was bought down to
   12x which is what all Overnight (NRML) Option Strategies get. Eventually, trading spreads is what we tried as that helps in reducing the Margin Required.
   Variables Optimized were same as the earlier strategies. The additional varaible being the Long Strike that ranged from 1 strike to alomost 20 strikes out.
   The Strike Selection for the long strike is also controlled from the Strike Price Selector. The Optimizations are saved in Strategy Testing/Short   
   Options/BankNifty Weekly Short Options on DropBox. This was tested with the short strike selection being At-The-Money,Out-Of-The-Money and Minimum Premium.
   Both those codes are here.[NiftyWeeklyShortOptions(ATM-OTM + Long)]
   https://github.com/qodeinvestments/Swan-Documentation/blob/a71d6815ca11327e9de6f06aa2ce6fa6d292a0bc/Systems/Nifty_SID/Backtest_Codes/NiftyWeeklyShortOptions(ATM-OTM%20+%20Long)
   [NiftyWeeklyShortOptions(MinPremium+Long)
   https://github.com/qodeinvestments/Swan-Documentation/blob/a71d6815ca11327e9de6f06aa2ce6fa6d292a0bc/Systems/Nifty_SID/Backtest_Codes/NiftyWeeklyShortOptions(MinPremium%20+%20Long).
   
   The latter code needs to be run on the same database i.e "Nifty (Weekly Continuous Contracts)" but on the "All Symbols DHF" watchlist. This code can only be        run when there are no data holes.The variables that were optimized are the same as the ones mentioned in the earlier strategy additionally with the Long Strike      being optimized to decide how many strikes further from the Short Strike should the Long option be bought. Depending on the moneyness of the Long Leg, the          leverage changes. All the different versions and optimizations of this variant can be found in in Strategy Testing/Short Options/Nifty Weekly Short Options on      DropBox.
 
