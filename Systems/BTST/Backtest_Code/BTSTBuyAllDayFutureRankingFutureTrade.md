## BTSTBuyAllDayFutureRankingFutureTrade

    #include <F&O BanList.afl>
    #include <F&O expiry selection.afl>

    bi = BarIndex();
    exitlastbar = LastValue(bi) == bi ; 
    addtime = 0;
    Lev = 1;
    f = 0.1; 
    Buyvp = 25; 
    Sellvp = 25;
    buybuffer = 1000;
    stopbuffer = 1000; 
    maxpos = Optimize("Maxpos",10,5,20,3);

    SetOption("InitialEquity",10000000);
    SetOption("AccountMargin",100/lev);
    SetOption("MaxOpenPositions",maxpos);
    SetPositionSize(100/Maxpos*lev,spsPercentOfEquity);
    SetOption("Priceboundchecking",False);

    SetTradeDelays(1,0,0,0);

    Cases = Optimize("Cases",6,1,7,1);

    if(cases == 1){ranktime = 100000+addtime; maxtime = 110000+addtime;}
    if(cases == 2){ranktime = 110000+addtime; maxtime = 120000+addtime;}
    if(cases == 3){ranktime = 120000+addtime; maxtime = 130000+addtime;}
    if(cases == 4){ranktime = 130000+addtime; maxtime = 140000+addtime;}
    if(cases == 5){ranktime = 100000+addtime; maxtime = 150000+addtime;}
    if(cases == 6){ranktime = 110000+addtime; maxtime = 150000+addtime;}
    if(cases == 7){ranktime = 120000+addtime; maxtime = 150000+addtime;}

    buytime = ranktime + buybuffer;

    stoptime = buytime + stopbuffer;

    Sellcase = Optimize("Sellcase",3,1,10,1);

    if(sellcase == 1){selltime = 091500+addtime;}
    if(sellcase == 2){selltime = 092000+addtime;}
    if(sellcase == 3){selltime = 092500+addtime;}
    if(sellcase == 4){selltime = 093000+addtime;}
    if(sellcase == 5){selltime = 093500+addtime;}
    if(sellcase == 6){selltime = 094000+addtime;}
    if(sellcase == 7){selltime = 094500+addtime;}
    if(sellcase == 8){selltime = 095000+addtime;}
    if(sellcase == 9){selltime = 095500+addtime;}
    if(sellcase == 10){selltime = 100000+addtime;}

    TimeFrameSet(inDaily);
    NextDay = valuewhen(Day() != Ref(Day(),1),Ref(DateNum(),1));
    NextDay = DateTimeConvert(2,NextDay);
    CurrentDate = DateTimeConvert(2,DateNum());
    Difference = round(DateTimeDiff(NextDay,CurrentDate)/(3600*24));
    TimeFrameRestore();

    Difference = TimeFrameExpand(Difference,inDaily,expandFirst);

    CurrentBarOpen = TimeFrameGetPrice("O" , inDaily ,0);

    Dailyclose = TimeFrameGetPrice("C",inDaily,0);

    GapPer = Optimize("GapPer",4,3,6,1);

    Gap = ( ( Close / CurrentBarOpen  ) -1 ) * 100;
    EODGap = ((Dailyclose/Currentbaropen)-1)*100;

    Buy = overnight AND Difference <= 10 AND Gap >= GapPer AND TimeNum() >= ranktime AND TimeNum() < maxtime AND exitlastbar == 0 AND excludeok == 0;

    Dow = ValueWhen(Buy,DayOfWeek());

    Sell = (((TimeNum() == selltime) ) AND DayOfWeek() != dow ) OR exitlastbar;

    BuyPrice = Close;
    SellPrice = Open;

    ///Limit Order Logic
    /*
    vol = ValueWhen(TimeNum()== ranktime,(ATR(Buyvp))); 

    btrig = Ref(C,-1) - (vol * f); 

    entrytimeOK = TimeNum() >= buytime AND TimeNum() < stoptime;  

    trigOK = L < btrig; 

    buycond1 = (trigOK AND entrytimeOK) AND ValueWhen(TimeNum() == ranktime,Gap) >= GapPer; 
    buycond2 = (TimeNum() >= stoptime) AND ValueWhen(TimeNum() == ranktime,Gap) >= GapPer; 

    Buy = (Buycond1 OR buycond2) AND Difference <= 10 AND overnight AND exitlastbar == 0 AND excludeok == 0; 

    sellvol = Ref(ATR(Sellvp),-1);
    strig = Ref(C,-1) + (sellvol * f);
    selllimit = TimeNum()==selltime AND H > strig ;

    Sell = selllimit OR (TimeNum()>selltime AND TimeNum()<ranktime) OR exitlastbar;

    BuyPrice = IIf( buycond1, Min(Open,btrig), Open); 
    SellPrice = IIf(selllimit, max(Open,strig), Open); 
    */

    PositionScore = IIf(Gap >= gapper , gap, 0); 

    PortEquity = Foreign("~~~Equity","C");

    Filter = 1;
    AddColumn(PortEquity,"PortEquity",1.2);

