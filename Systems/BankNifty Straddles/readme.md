# BankNifty Straddles

BankNifty Straddles is an option strategy which runs on weekly and monthly timeframes.
In the weekly part of this system, 
- Current week CE & PE contracts are short depending on the delta.
- In the Monthly part of this system, Current month CE & PE contracts are bought depending on the delta.


# Backtest:
Data used: 
- EoD Weekly and Monthly options data for BankNifty(with contract filter >=1000).
- Expiry dates
- Strike Selection: We have used strikes closest to the delta.



## Optimisations
### 1. Delta Optimisations
  - Optimised for 5-50 delta
  - No trend was seen, 30 and 40 delta had the best results.
  - We chose a range of 15-50 delta, as it did not diminish the results and it made sense to be covered against most market movement.
### 2. SL and Profit Target optimisation
- Based on percent of premium Collected or lost.
- These did not add any value to the system.
### 3. Opening Day optimisations
#### - Weekly - Optimised for opening on Thursday, Friday, Monday, Tuesday and Wednesday; all squaring off on Expiry.
-  - Monday and Tuesday opening had the best results; Thursday had the poorest results.
-  - We chose to open a combination of Monday,Tuesday and Wednesday opening day as Thursday increased the drawdowns.
#### - Monthly - Optimised for opening on Friday,Monday; all squaring off on Expiry
-   - Opening on Monday had similar returns but reduced the Drawdown. 
### 4. Adjustments - Delta
- Squaring off the existing position when underlying(BankNifty) crosses the trigger on either side and opening strikes closest to the same delta, on the same day.
- These are performed for Monthly LONG
### 5. Adjustments - Premium Neutral
- Squaring off the existing position when underlying(BankNifty) crosses the trigger on either side and opening Strikes worth the same premium, on the same day. 
- For example, we square off a straddle at a total premium of 100,
- We Short a CALL strike going at a premium closest to 50 (100/2),
- Similarly, We Short a PUT strike going at a premium closest to 50 (100/2).
- The idea is to collect the premium missed out on when shifting.
- These are performed for Weekly SHORT

### 6. Short Monthly Straddles
- We tested Shorting both CE and PE on current month contracts.
- This system had negative results.
### 7. Reverse Monthly Straddles Base case and with adjustments
- Here, we went long on Monthly CE and PE instead of short.
- For adjustments, we tested both Delta Based and premium neutral adjustments. We decided to go with Delta based adjustments as it perfomed slightly better and since we are going long, we havent missed out on any premium.
### 8. Leverage Optimisation 2,4,6,8,10,15
- We chose 6x Leverage
### 9. Opening Monthly Long every week.
- Here, we tested opening monthly long CE and PE every Friday and squared them off on weekly expiry.
### 10. Squaring off Current Monthly Long and Opening Monthly-II long in the final week of current Month.
- Here, in the final week of the month, to prevent the chance of going long and short on the same strike, we tested squaring off the current expiry on the before the final week began and went long on Next Month contracts on the First day of the final month.

## Trigger Logic
- Trigger % Range 25-200
- Upper Trigger = (Total Premium)*trigger% + CE Strike
- Lower Trigger = PE Strike - (Total Premium)*trigger%


## Position Sizing
1. Minimum Premium
2. Number of Shares

Both were tried with and without compounding, 
Number of shares performed better.
We decided to go ahead with Number of Shares with compounding
