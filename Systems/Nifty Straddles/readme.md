
# Nifty Straddles

Nifty Straddles is an option strategy which runs on weekly and monthly timeframes.
In the weekly part of this system, 
- Current week CE & PE contracts are short depending on the delta.
- In the Monthly part of this system, Current month CE & PE contracts are bought depending on the delta.


# Backtest:
Data used: 
- EoD Weekly and Monthly options data for Nifty(with contract filter >=1000).
- Expiry dates
- Strike Selection: We have used strikes closest to the delta.



## Optimisations
### 1. Delta Optimisations
  - Optimised for 5-50 delta
  - No trend was seen, 30 and 40 delta had the best results.
  - We chose a range of 15-50 delta.
### 2. Opening Day optimisations
#### - Weekly - Optimised for opening on Thursday, Friday, Monday, Tuesday and Wednesday; all squaring off on Expiry.
-  - Monday and Tuesday opening had the best results; Thursday had the poorest results.
-  - We chose to open a combination of Monday,Tuesday and Wednesday opening day.
### 3. Adjustments - Delta
- Squaring off the existing position when underlying(Nifty) crosses the trigger on either side and opening strikes closest to the same delta, on the same day.
- These are performed for Monthly LONG
### 4. Adjustments - Premium Neutral
- Squaring off the existing position when underlying(Nifty) crosses the trigger on either side and opening Strikes worth the same premium, on the same day. 
- For example, we square off a straddle at a total premium of 100,
- We Short a CALL strike going at a premium closest to 50 (100/2),
- Similarly, We Short a PUT strike going at a premium closest to 50 (100/2).
- The idea is to collect the premium missed out on when shifting.
- These are performed for Weekly SHORT

### 5. Reverse Monthly Straddles (Long) with adjustments
- We chose 6x Leverage

## Trigger Logic
- Trigger % Range 25-200
- Upper Trigger = (Total Premium)*trigger% + CE Strike
- Lower Trigger = PE Strike - (Total Premium)*trigger%


## Position Sizing
1. Number of Shares

