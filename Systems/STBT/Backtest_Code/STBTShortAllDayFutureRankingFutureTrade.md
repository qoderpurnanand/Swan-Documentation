## STBTShortAllDayFutureRankingFutureTrade

    #include <F&O BanList.afl>
    #include <F&O expiry selection.afl>

    bi = BarIndex();
    exitlastbar = LastValue(bi) == bi ; 
    addtime = 0;
    Lev = 1;
    f = 0.1; 
    Shortvp = 25; 
    Covervp = 25;
    Shortbuffer = 1000;
    stopbuffer = 1000; 
    maxpos = Optimize("Maxpos",10,5,20,5);

    SetOption("InitialEquity",10000000);
    SetOption("AccountMargin",100/lev);
    SetOption("MaxOpenPositions",maxpos);
    SetPositionSize(100/Maxpos*lev,spsPercentOfEquity);
    SetOption("Priceboundchecking",False);

    SetTradeDelays(0,0,1,0);

    Cases = Optimize("Cases",4,1,7,1);

    if(cases == 1){ranktime = 100000+addtime; maxtime = 110000+addtime;}
    if(cases == 2){ranktime = 110000+addtime; maxtime = 120000+addtime;}
    if(cases == 3){ranktime = 120000+addtime; maxtime = 130000+addtime;}
    if(cases == 4){ranktime = 130000+addtime; maxtime = 140000+addtime;}
    if(cases == 5){ranktime = 100000+addtime; maxtime = 150000+addtime;}
    if(cases == 6){ranktime = 110000+addtime; maxtime = 150000+addtime;}
    if(cases == 7){ranktime = 120000+addtime; maxtime = 150000+addtime;}

    Shorttime = ranktime + Shortbuffer;

    stoptime = Shorttime + stopbuffer;

    Covercase = Optimize("Covercase",2,1,5,1);

    if(Covercase == 1){Covertime = 091500+addtime;}
    if(Covercase == 2){Covertime = 092000+addtime;}
    if(Covercase == 3){Covertime = 092500+addtime;}
    if(Covercase == 4){Covertime = 093000+addtime;}
    if(Covercase == 5){Covertime = 093500+addtime;}
    if(Covercase == 6){Covertime = 094000+addtime;}
    if(Covercase == 7){Covertime = 094500+addtime;}
    if(Covercase == 8){Covertime = 095000+addtime;}
    if(Covercase == 9){Covertime = 095500+addtime;}
    if(Covercase == 10){Covertime = 100000+addtime;}

    TimeFrameSet(inDaily);
    NextDay = valuewhen(Day() != Ref(Day(),1),Ref(DateNum(),1));
    NextDay = DateTimeConvert(2,NextDay);
    CurrentDate = DateTimeConvert(2,DateNum());
    Difference = round(DateTimeDiff(NextDay,CurrentDate)/(3600*24));
    TimeFrameRestore();

    Difference = TimeFrameExpand(Difference,inDaily,expandFirst);

    CurrentBarOpen = TimeFrameGetPrice("O" , inDaily ,0);

    Dailyclose = TimeFrameGetPrice("C",inDaily,0);

    GapPer = Optimize("GapPer",5,3,6,1);

    Gap = ( ( Close / CurrentBarOpen  ) -1 ) * 100;
    EODGap = ((Dailyclose/Currentbaropen)-1)*100;

    Short = overnight AND Difference <= 10 AND Gap <= -GapPer AND TimeNum() >= ranktime AND TimeNum() < maxtime AND exitlastbar == 0 AND excludeok == 0;

    Dow = ValueWhen(Short,DayOfWeek());

    Cover = (((TimeNum() == Covertime) ) AND DayOfWeek() != dow ) OR exitlastbar;

    ShortPrice = Close;
    CoverPrice = Open;

    ///Limit Order Logic
    /*
    vol = ValueWhen(TimeNum()== ranktime,(ATR(Shortvp))); 

    btrig = Ref(C,-1) - (vol * f); 

    entrytimeOK = TimeNum() >= Shorttime AND TimeNum() < stoptime;  

    trigOK = L < btrig; 

    Shortcond1 = (trigOK AND entrytimeOK) AND ValueWhen(TimeNum() == ranktime,Gap) >= GapPer; 
    Shortcond2 = (TimeNum() >= stoptime) AND ValueWhen(TimeNum() == ranktime,Gap) >= GapPer; 

    Short = (Shortcond1 OR Shortcond2) AND Difference <= 10 AND overnight AND exitlastbar == 0 AND excludeok == 0; 

    Covervol = Ref(ATR(Covervp),-1);
    strig = Ref(C,-1) + (Covervol * f);
    Coverlimit = TimeNum()==Covertime AND H > strig ;

    Cover = Coverlimit OR (TimeNum()>Covertime AND TimeNum()<ranktime) OR exitlastbar;

    ShortPrice = IIf( Shortcond1, Min(Open,btrig), Open); 
    CoverPrice = IIf(Coverlimit, max(Open,strig), Open); 
    */

    PositionScore = IIf(Gap <= -gapper , gap, 0); 

    PortEquity = Foreign("~~~Equity","C");

    Filter = 1;
    AddColumn(PortEquity,"PortEquity",1.2);
