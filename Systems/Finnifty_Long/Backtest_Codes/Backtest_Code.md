///Will need to include the Strike Price Selector to choose the correct Banknifty Symbols///////
///Input Parameters///
///Fin_nifty weekly expiry : Thursday was expiry until 14.10.2021 and from 19.10.2021(first) tuesday was the new expiry
///Fin_nifty weeklies started in Jan.2021

maxpos = Optimize("maxpos",1,2,8,2);
Initialequity = 1000000;
Commissions = 1/100;////1% of either side of the trade

///OPtimization Parameters: 1. Entrytime 2.Exittime 3.Strike 4.Gap Condition 

#include <finnifty_strikepriceselector.afl>

LotSize = 40;
addtime = 459;

SetOption("InitialEquity",initialequity);
SetPositionSize(1/maxpos,spsPercentOfEquity);
SetOption("maxopenpositions",maxpos);
SetTradeDelays(0,0,0,0);
SetOption("priceboundchecking",False);
SetOption("DisableRuinStop",True);

DiwaliDates = DateNum()!=1111026 AND DateNum()!=1121113 AND DateNum()!=1131103 AND DateNum()!=1141023 AND DateNum()!=1151111 AND DateNum()!=1161030 AND DateNum()!=1171019 AND DateNum()!=1181107 AND DateNum()!=1191027 AND DateNum()!=1201114 AND DateNum()!=1211104;

Cases = Optimize("Cases",8,1,4,1);

if(cases == 1){EntryTime = 093000; Exittime =144500; Gapfilter = 30;gapcaln = Close;}
if(cases == 2){EntryTime = 103000; Exittime =150000; Gapfilter = 30;gapcaln = Close;}
if(cases == 3){EntryTime = 113000; Exittime =151000; Gapfilter = 40;gapcaln = Open;}
if(cases == 4){EntryTime = 123000; Exittime =152000; Gapfilter = 50;gapcaln = Close;}
if(cases == 5){EntryTime = 093000; Exittime =144500; Gapfilter = 50;gapcaln = Open;}
if(cases == 6){EntryTime = 103000; Exittime =150000; Gapfilter = 40;gapcaln = Close;}
if(cases == 7){EntryTime = 113000; Exittime =151000; Gapfilter = 30;gapcaln = Open;}
if(cases == 8){EntryTime = 123000; Exittime =152000; Gapfilter = 30;gapcaln = Close;}


EntryTime  = Entrytime+addtime;
NextDayExitTime  = Day()!=Ref(Day(),-1);

/*
Cases1 = Optimize("Cases1",2,1,3,1);

if(cases1 == 1){NextDayExitTime = 092000;}
if(cases1 == 2){NextDayExitTime = 092500;}
if(cases1 == 3){NextDayExitTime = 093000;}
*/
OpBar = ValueWhen(DateNum()!=Ref(DateNum(),-1),gapcaln);
	
IntradayGap = (Close/OpBar-1)*100;
//GapFilter = Optimize("gapfilter",20,10,60,10);
GapCond = IntradayGap > GapFilter;

bi = BarIndex();
exitlastbar = bi == LastValue(bi - 1);    
/*
Entrypf = Optimize("entrypf",0.1,0.1,1,0.2);

POI = Close;

edist = ATR(3);

Btrig = POI - (edist*entrypf);

Strig = POI + (Entrypf*edist);
*/
TimeFrameSet(inDaily);
#include <finnifty_ExpiryDates.afl>
Daychange = Day() != Ref(Day(),-1);
Tom = Ref(DateNum(),1);
finnifty_weeklyexpiry = IIf(Ref(DateNum(),1) > finnifty_weeklyexpiry,DateNum(),finnifty_weeklyexpiry);
datenumdiff = DateTimeDiff(DateTimeConvert(2,Ref(DateNum(),1)),DateTimeConvert(2,DateNum()))/(24*60*60);
no_data_ahead = IIf((datenumdiff)>4,1,0);

TimeFrameRestore();


 

finnifty_weeklyexpiry = TimeFrameExpand(finnifty_weeklyexpiry,inDaily,expandFirst);
Daychange = TimeFrameExpand(Daychange,inDaily,expandFirst);
Tom = TimeFrameExpand(Tom,inDaily,expandFirst);
no_data_ahead = TimeFrameExpand(no_data_ahead,inDaily,expandFirst);
datenumdiff = TimeFrameExpand(datenumdiff,inDaily,expandFirst);

Exittime =IIf(DateNum()==finnifty_weeklyexpiry,exittime+addtime,153000+addtime);

BuyCond = TimeNum()>Entrytime AND TimeNum()<ExitTime AND StrikePriceSelector == 1 AND Gapcond AND diwalidates;

Buy = TimeNum()>Entrytime AND TimeNum()<ExitTime AND StrikePriceSelector == 1 AND Gapcond AND diwalidates;

Buyday = ValueWhen(Buy==1,DateNum());
WeeklyExpiryLastbar = IIf( DateNum()==finnifty_weeklyexpiry AND Day() != Ref(Day(),1),1,0);



Sell = IIf(Buyday==finnifty_weeklyexpiry OR (DateNum()==buyday AND no_data_ahead),TimeNum()>=ExitTime OR (Day()!=Ref(Day(),1)) , NextDayExitTime) OR exitlastbar ;

Buy = ExRem(Buy,Sell);
Sell = ExRem(Sell,Buy);

BuyPrice = Close;
SellPrice = Close;




Filter =1;
AddColumn(Intradaygap,"intradaygap");
AddColumn(gapcond,"gapcond");
AddColumn(Buy,"Buy");
AddColumn(buyday,"buyday");
AddColumn(Sell,"Sell");
AddColumn(nextdayexittime,"nextdayexittime");
AddColumn(no_data_ahead,"no_data");
AddColumn(tom,"tom");
AddColumn(datenumdiff,"datenumdiff");




