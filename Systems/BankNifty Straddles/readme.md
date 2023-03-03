# BankNifty Straddles

BankNifty Straddles is an option strategy which runs on weekly and monthly timeframes.
In the weekly part of this system, 
- Current week CE & PE contracts are short depending on the delta.
In the Monthly part of this system,
- Current month CE & PE contracts are bought depending on the delta.


# Backtest:
Data used: 
- EoD Weekly and Monthly options data for BankNifty(with contract filter >=1000).
- Expiry dates
- Strike Selection: We have used strikes closest to the delta.



## Optimisations
### 1. Delta Optimisations
  - Optimised for 5-50 delta
  - Although No trend was seen, 30 and 40 delta had the best results.
  - We chose a range of 15-50 delta, as it did not diminish the results and it made sense to be covered against most market movement.
### 2. SL and Profit Target optimisation
- Based on percent of premium Collected or lost.
- These did not add any value to the system, the CAR/MDD was flat.
### 3. Opening Day optimisations
#### - Weekly - Optimised for opening on Thursday, Friday, Monday, Tuesday and Wednesday; all squaring off on Weekly Expiry.
-  - Monday and Tuesday opening had the best results; Thursday had the poorest(negative) results.
-  - We chose to open a combination of Monday,Tuesday and Wednesday opening day as including Thursday increased the drawdowns. 
#### - Monthly - Optimised for opening on Friday,Monday; all squaring off on Monthly Expiry
-   - Opening on Monday had similar returns but reduced the Drawdown.
-   - We chose to open on Monday (i.e the second day of the month).
### 4. Adjustments - Delta Based
- The existing position is squared off when the underlying(BankNifty) crosses the trigger on either side (Trigger logic is stated below) and a new position is opened, with strikes closest to the same delta, on the same day.
- We chose to perform these for Monthly LONG Straddles.
### 5. Adjustments - Premium Neutral
- The existing position is squared off when the underlying(BankNifty) crosses the trigger on either side (Trigger logic is stated below) and a new position is opened, with Strikes worth the same premium, on the same day. 
- For example, we open a straddle having a total premium of 200 and after the trigger is hit, we square it off at a total premium of 100, this 100 is then divided into 2 (for CE & PE),
- While adjusting, we open a CALL strike going at a premium closest to 50 (100/2),
- Similarly, We open a PUT strike going at a premium closest to 50 (100/2).
- The idea is to collect the premium missed out on when shifting.
- These are performed for Weekly SHORT

### 6. Short Monthly Straddles
- We tested Shorting both CE and PE on current month contracts.
- This system had negative results.
### 7. Reverse Monthly Straddles(Long), Base case and with adjustments
- Here, we went long on Monthly CE and PE instead of short, at the start of the month on Friday and Monday.
- For adjustments, we tested both Delta Based and premium neutral adjustments. We decided to go with Delta based adjustments as it perfomed slightly better and since we are going long, we havent missed out on any premium.
- Base Case had slightly better results.
- We Chose a combination of Base Case and Adjustments, opening on Monday .
### 8. Leverage Optimisation 
- Optimisation were performed on a leverage of 4,6,8,10,12,15,16.
- Higher leverages had higher returns but higher drawdowns as well.
- We chose 12x Leverage, as it had optimal drawdowns and returns.
### 9. Opening Monthly Long every week.
- Here, we tested opening monthly long CE and PE every Friday and squared them off on weekly expiry.
- This system had flat results, did not add any value.
### 10. Squaring off Current Monthly Long and Opening Monthly-II long in the final week of current Month.
- Here, in the final week of the month, the main idea behind this optimisation is when to prevent the chance of going long and short on the same strike, we tested squaring off the current expiry on the before the final week began and went long on Next Month contracts on the First day of the final month.

## Trigger Logic
- Trigger % Range 25-200
- Upper Trigger = (Total Premium)*Trigger% + CE Strike
- Lower Trigger = PE Strike - (Total Premium)*Trigger%


df.loc[idi,'ratio']=df.loc[idi,'Min_premium']*poe*100/df.loc[idi,'Total_Premium']
                                    df.loc[idi , 'units_new'] = (((df.loc[idi ,'pl_check'])*df.loc[idi,'ratio'])/(df.loc[idi,  "OPT_Close_CE"]+df.loc[idi,  "OPT_Close_PE"])/2)



## Position Sizing
1. Minimum Premium
- Here, to calculate the minimum premium, Margin per Share is calculated by dividing the Underlying equity value by the leverage.
- Margin per share is multiplied with the percent of equity to get the minimum premium.
- If total premium of the position on that day is greater than the minimum premium, number of shares logic is used to calculate the quantity (stated below).
- If total premium of the position on that day is lesser than the minimum premium, to get the new units, a ratio is calculated Minimum_Premium*percent_of_equity/Total_Premium. 
- This ratio is then multiplied with the number of units to get the final quantitity.
- The main aim here is to not open exorbitantly high quantities for positions with very low premium.


2. Number of Shares
- Here, the available equity is multiplied with the leverage to get the Total available margin. We then divide this margin with the underlying equity value and then by 2 (for CE and PE) to get the margin required to open 1 unit. The total number of units are then calculated by dividing the available margin by margin required to open 1 unit.


Both were tried with and without compounding, 
Number of shares performed better.
We decided to go ahead with Number of Shares with compounding
