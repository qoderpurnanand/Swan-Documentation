## EXECUTION CODE
    ///BNL V.2.1.: This version will take Banknifty Index as an Entry Indicator and not the premium////
    //// This version will run only on Same Expiry Symbols: So will have to choose the Same Expiry WL with fewer Symbols//


    ////Input Variables:////
    maxpos = 2;//Optimize("maxpos",1,1,5,1);//to be changed if taking both
    initialequity = 1000000;
    commissions = 1/100;///1% of Equity////

    #include <BankniftyWeeklyStrikePriceSelector.afl>

    LotSize = IIf(Datenum()>=1110101 AND DateNum()<=1151029, 25 , IIf( DateNum()>=1151030 AND DateNum()<=1160630 , 30, IIf( DateNum()>=1160701 AND DateNum()<=1181025 , 40 , IIf( DateNum()>=1181026 AND DateNum()<=1200730 , 20 , 25)))) ;  


    SetOption("initialEquity",initialequity);
    SetPositionSize(1/maxpos,spsPercentOfEquity);
    SetOption("maxopenpositions",maxpos);
    SetTradeDelays(0,0,0,0);
    SetOption("priceboundchecking",False);
    SetOption("DisableRuinStop",True);


    bi = BarIndex();
    exitlastbar = bi == LastValue(bi - 1);    


    DiwaliDates = DateNum()!=1111026 AND DateNum()!=1121113 AND DateNum()!=1131103 AND DateNum()!=1141023 AND DateNum()!=1151111 AND DateNum()!=1161030 AND DateNum()!=1171019 AND DateNum()!=1181107 AND DateNum()!=1191027 AND DateNum()!=1201114 AND DateNum()!=1211104;
    Cases = 1;//Optimize("Cases",2,1,4,1);

    if(cases == 0){Entrytime = 093000;}
    if(cases == 1){Entrytime = 100000;}

    ExitTime  = 151500;
    NextDayExitTime  = 093000;


    bi = BarIndex();
    exitlastbar = bi == LastValue(bi);    
    exitlastbar1 = bi == LastValue(bi-2);  


    TimeFrameSet(inDaily);
    #include <ExpiryDates.afl>
    Daychange = Day() != Ref(Day(),-1);
    Tom = Ref(DateNum(),1);
    WeeklyExpiryDate = IIf(Ref(DateNum(),1) > WeeklyExpiryDate,DateNum(),WeeklyExpiryDate);
    TimeFrameRestore();

    WeeklyExpiryDate = TimeFrameExpand(WeeklyExpiryDate,inDaily,expandFirst);
    Daychange = TimeFrameExpand(Daychange,inDaily,expandFirst);
    Tom = TimeFrameExpand(Tom,inDaily,expandFirst);


    BankNiftyClose = Foreign("$BANKNIFTY-NSE", "C" );

    SetForeign("$BANKNIFTY-NSE");
    BNopen = TimeFrameGetPrice("Open",inDaily,0);

    RestorePriceArrays();

    bnmove = (BankNiftyClose/bnopen-1)*100;
    xfactor = Optimize("xfactor",0.7,0.1,1.5,0.3);


    BuyCond = TimeNum()>Entrytime AND TimeNum()<ExitTime AND StrikePriceSelector == 1  AND diwalidates AND IIf(type=="CE",bnmove > xfactor,bnmove < -xfactor);
    Buy = buycond and nextexpirysym==0 and DateNum()!= 1170125;

    Buyday = ValueWhen(Buy==1,DateNum());
    WeeklyExpiryLastbar = IIf( DateNum()==weeklyexpirydate AND Day() != Ref(Day(),1),1,0);

    Sell = IIf(Buyday==WeeklyExpiryDate and timenum()>=exittime,TimeNum()>=ExitTime OR DateNum()!=Ref(DateNum(),1),TimeNum()<=NextDayExitTime) OR exitlastbar;

    Buy = ExRem(Buy,Sell);
    Sell = ExRem(Sell,Buy);

    BuyPrice = Close;
    SellPrice = Close;//IIf(Ref(H,1)>strig, Max(Ref(Open,1),strig),Ref(Close,1));//*(1+0.5/100);
