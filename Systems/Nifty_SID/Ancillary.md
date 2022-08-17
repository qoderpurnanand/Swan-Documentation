
Along with Backtest Codes, there are a few Ancillary codes that form a part of the main Backtest Codes. These codes need to be updated from time to time:

StrikePriceSelector: - This code helps in selecting the correct strike price. If you want to trade At-The-Money or a strike Out-Of-The-Money or a strike In-The-Money
or a Dynamic Strike Selection, that can be done by making the required changes in this code.This code also has the functionality of selecting which strike needs to be bought as protection in case the Short Options backtest is being done along with protection. The code can be found here[NiftyWeeklyStrikePriceSelector]
https://github.com/qodeinvestments/Swan-Documentation/blob/2fc382476ce498d0ecd0239888dc4694f938fc23/Systems/Nifty_SID/Backtest_Codes/NiftyWeeklyStrikePriceSelector

ExpiryDates: - This code has all the Expiry Dates starting from January 2011 for Bank Nifty Options having Monthly Expiries and June 2016 for Bank Nifty Options having Weekly Expiries. This code needs to updated perodically and also helps in creating the BankNifty (Weekly Continuous Contracts) and the BankNift (Weekly Continuous Contracts) (Next Expiry).This code helps in calculating the Days To ExpiryThe code can be found here 
