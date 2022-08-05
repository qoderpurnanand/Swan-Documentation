    ///Input Parameters///

    maxpos = 2;//Optimize("maxpos",2,1,5,1);
    Initialequity = 1000000;
    Commissions = 1/100;////1% of either side of the trade

    ///OPtimization Parameters: 1. Entrytime 2.Exittime 3.Strike 4.Gap Condition 


    #include <BankniftyWeeklyStrikePriceSelector.afl>

    LotSize = IIf(Datenum()>=1110101 AND DateNum()<=1151029, 25 , IIf( DateNum()>=1151030 AND DateNum()<=1160630 , 30, IIf( DateNum()>=1160701 AND DateNum()<=1181025 , 40 , IIf( DateNum()>=1181026 AND DateNum()<=1200730 , 20 , 25)))) ;   

    SetOption("initialEquity",initialequity);
    SetPositionSize(1/maxpos,spsPercentOfEquity);
    SetOption("maxopenpositions",maxpos);
    SetTradeDelays(0,0,0,0);
    SetOption("priceboundchecking",False);
    SetOption("DisableRuinStop",True);

    DiwaliDates = DateNum()!=1111026 AND DateNum()!=1121113 AND DateNum()!=1131103 AND DateNum()!=1141023 AND DateNum()!=1151111 AND DateNum()!=1161030 AND DateNum()!=1171019 AND DateNum()!=1181107 AND DateNum()!=1191027 AND DateNum()!=1201114 AND DateNum()!=1211104;

    Cases1 = Optimize("Cases1",0,0,3,1);

    if(cases1 == 0){NextDayExitTime = 091500;}
    if(cases1 == 1){NextDayExitTime = 092000;}
    if(cases1 == 2){NextDayExitTime = 092500;}
    if(cases1 == 3){NextDayExitTime = 093000;}

    EntryTime  = 093000;
    ExitTime  = 151500;
    NextDayExitTime  = 093000;

    OpBar = ValueWhen(DateNum()!=Ref(DateNum(),-1),Close);//Close

    IntradayGap = (Close/OpBar-1)*100;
    GapFilter = 40;//Optimize("gapfilter",40,20,70,10);
    GapCond = IntradayGap > GapFilter;

    bi = BarIndex();
    exitlastbar = bi == LastValue(bi - 1);    

    Entrypf = 0.1;//Optimize("entrypf",0.1,0.1,1,0.2);

    POI = Close;
    edist = ATR(3);

    Btrig = POI - (edist*entrypf);
    Strig = POI + (Entrypf*edist);

    TimeFrameSet(inDaily);
    #include <ExpiryDates.afl>
    Daychange = Day() != Ref(Day(),-1);
    Tom = Ref(DateNum(),1);
    WeeklyExpiryDate = IIf(Ref(DateNum(),1) > WeeklyExpiryDate,DateNum(),WeeklyExpiryDate);
    TimeFrameRestore();

    WeeklyExpiryDate = TimeFrameExpand(WeeklyExpiryDate,inDaily,expandFirst);
    Daychange = TimeFrameExpand(Daychange,inDaily,expandFirst);
    Tom = TimeFrameExpand(Tom,inDaily,expandFirst);

    BuyCond = TimeNum()>Entrytime AND TimeNum()<ExitTime AND StrikePriceSelector == 1 AND Gapcond AND diwalidates;

    WeekNumber = Foreign("WeekNumber","Close");

    Buy = TimeNum()>Entrytime AND TimeNum()<ExitTime AND StrikePriceSelector == 1 AND Gapcond AND diwalidates AND DateNum()!=1170125;// AND DaysToExpiry==TradingDays;

    Buyday = ValueWhen(Buy==1,DateNum());
    WeeklyExpiryLastbar = IIf( DateNum()==weeklyexpirydate AND Day() != Ref(Day(),1),1,0);

    Sell = IIf(Buyday==WeeklyExpiryDate,TimeNum()>=ExitTime OR DateNum()!=Ref(DateNum(),1),TimeNum()<=NextDayExitTime) OR exitlastbar;

    Buy = ExRem(Buy,Sell);
    Sell = ExRem(Sell,Buy);

    BuyPrice = Close;
    SellPrice = Close;
