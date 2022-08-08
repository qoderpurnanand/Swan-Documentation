## BTSTBuyRankTimeEquityRankingEquityTrade

    #include <F&O includeok.afl>
    #include <F&O BanList.afl>

    bi = BarIndex();
    exitlastbar = LastValue(bi) == bi ; 
    addtime = 0;
    Lev = 1;
    maxpos = Optimize("maxpos",8,5,20,3);

    SetOption("InitialEquity",10000000);
    SetOption("AccountMargin",100/lev);
    SetOption("MaxOpenPositions",maxpos);
    SetPositionSize(100/Maxpos*lev,spsPercentOfEquity);
    SetOption("Priceboundchecking",False);

    SetTradeDelays(1,0,0,0);

    Cases = Optimize("Cases",4,1,7,1);

    if(cases == 1){ranktime = 094500+addtime;}
    if(cases == 2){ranktime = 100000+addtime;}
    if(cases == 3){ranktime = 110000+addtime;}
    if(cases == 4){ranktime = 120000+addtime;}
    if(cases == 5){ranktime = 130000+addtime;}
    if(cases == 6){ranktime = 140000+addtime;}
    if(cases == 7){ranktime = 150000+addtime;}

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

    CurrentBarOpen = TimeFrameGetPrice("O" , inDaily ,0);

    Dailyclose = TimeFrameGetPrice("C",inDaily,0);

    GapPer = Optimize("GapPer",3,3,5,1);

    Gap = ( ( Close / CurrentBarOpen  ) -1 ) * 100;
    EODGap = ((Dailyclose/Currentbaropen)-1)*100;

    Buy = includeOK AND Gap >= GapPer AND TimeNum() == ranktime AND exitlastbar == 0 AND excludeok == 0;

    dow = ValueWhen(Buy,DayOfWeek());

    Sell = ((includeok == 0 OR (TimeNum() == selltime) ) AND DayOfWeek() != dow ) OR exitlastbar;

    BuyPrice = Close;
    SellPrice = Open;

    PositionScore = IIf(Gap >= gapper , gap, 0);
