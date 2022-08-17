## STBTShortAllDayEquityRankingFutureTrade

    #include <F&O expiry selection.afl>
    #include <F&O BanList.afl>

    bi = BarIndex();
    exitlastbar = LastValue(bi) == bi ; 
    addtime = 0;
    Lev = 1;
    maxpos = 10;
    f = 0.1;
    Shortvp = 25;
    Covervp = 25;
    ShortBuffer = 1000;
    CoverBuffer = 500;

    SetOption("InitialEquity",10000000);
    SetOption("AccountMargin",100/lev);
    SetOption("MaxOpenPositions",maxpos);
    SetPositionSize(100/Maxpos*lev,spsPercentOfEquity);
    SetOption("Priceboundchecking",False);

    SetTradeDelays(0,0,0,0);

    Cases = Optimize("Cases",4,1,7,1);

    if(cases == 1){ranktime = 100000+addtime; maxtime = 110000+addtime;}
    if(cases == 2){ranktime = 110000+addtime; maxtime = 120000+addtime;}
    if(cases == 3){ranktime = 120000+addtime; maxtime = 130000+addtime;}
    if(cases == 4){ranktime = 130000+addtime; maxtime = 140000+addtime;}
    if(cases == 5){ranktime = 100000+addtime; maxtime = 150000+addtime;}
    if(cases == 6){ranktime = 110000+addtime; maxtime = 150000+addtime;}
    if(cases == 7){ranktime = 120000+addtime; maxtime = 150000+addtime;}

    Shorttime = ranktime + Shortbuffer;

    stoptime = Shorttime + Coverbuffer;

    covercase = Optimize("covercase",2,1,5,1);

    if(covercase == 1){covertime = 091500+addtime;}
    if(covercase == 2){covertime = 092000+addtime;}
    if(covercase == 3){covertime = 092500+addtime;}
    if(covercase == 4){covertime = 093000+addtime;}
    if(covercase == 5){covertime = 093500+addtime;}
    if(covercase == 6){covertime = 094000+addtime;}
    if(covercase == 7){covertime = 094500+addtime;}
    if(covercase == 8){covertime = 095000+addtime;}
    if(covercase == 9){covertime = 095500+addtime;}
    if(covercase == 10){covertime = 100000+addtime;}

    GapPer = Optimize("GapPer",6,3,6,1);

    TimeFrameSet(inDaily);
    NextDay = valuewhen(Day() != Ref(Day(),1),Ref(DateNum(),1));
    NextDay = DateTimeConvert(2,NextDay);
    CurrentDate = DateTimeConvert(2,DateNum());
    Difference = round(DateTimeDiff(NextDay,CurrentDate)/(3600*24));
    TimeFrameRestore();

    Difference = TimeFrameExpand(Difference,inDaily,expandFirst);

    TimeFrameSet(inDaily);
    x = IIf(Year() > Ref(Year() ,-1),1, IIf( Month() > Ref(Month() ,-1),1,0));
    y = IIf(Year() < Ref(Year() ,1),1, IIf( Month() < Ref(Month() ,1),1,0));

    Xdate = BarsSince(x);
    PrevBars = 3;

    StartPeriod = Ref(y,PrevBars-1);

    Buycond = Sum(startperiod,prevbars);
    DayOK = Buycond == 1;

    TimeFrameRestore();

    DayOk = TimeFrameExpand(dayok,inDaily,expandFirst);

    expirysym = IIf(StrRight(Name(),1)=="1",1,0);

    NIIT = IIf( expirysym ==1 AND DateNum() <= 1200626,Foreign("~~STBTgapall"+ StrReplace(Name(),"NIITTECH.FUT1","COFORGE.EQ-NSE"),"Close"),Foreign("~~STBTgapall"+ StrReplace(Name(),"NIITTECH.FUT","COFORGE.EQ-NSE"),"Close"));
    TATACONSUM = IIf( expirysym ==1 AND DateNum() <= 1200626,Foreign("~~STBTgapall"+ StrReplace(Name(),"TATAGLOBAL.FUT1","TATACONSUM.EQ-NSE"),"Close"),Foreign("~~STBTgapall"+ StrReplace(Name(),"TATAGLOBAL.FUT","TATACONSUM.EQ-NSE"),"Close"));

    gap = IIf((Name() == "NIITTECH.FUT" OR Name() == "NIITTECH.FUT1") AND DateNum() < 1200616,NIIT,IIf((Name() == "TATAGLOBAL.FUT" OR Name() == "TATAGLOBAL.FUT1") AND DateNum() < 1200211 ,TATACONSUM, IIf( expirysym ==1 ,Foreign("~~STBTgapall"+ StrReplace(Name(),".FUT1",".EQ-NSE"),"Close"),Foreign("~~STBTgapall"+ StrReplace(Name(),".FUT",".EQ-NSE"),"Close"))));

    Short = overnight AND excludeok == 0 AND gap <= -GapPer AND TimeNum() >= ranktime AND TimeNum() < maxtime AND Difference <=10 AND exitlastbar == 0;

    dow = ValueWhen(Short,DayOfWeek());

    Cover = (((TimeNum() == covertime) ) AND DayOfWeek() != dow ) OR exitlastbar;

    ShortPrice = Close;

    CoverPrice = Open;

    ///Limit Order Logic
    /*
    vol = ValueWhen(TimeNum()== ranktime,(ATR(Shortvp))); 

    Strig = Ref(C,-1) + (vol * f); 

    entrytimeOK = TimeNum() >= Shorttime AND TimeNum() < stoptime;  

    trigOK = H > Strig; 

    Shortcond1 = (trigOK AND entrytimeOK) AND ValueWhen(TimeNum() == ranktime,Gap) <= -GapPer; 
    Shortcond2 = (TimeNum() >= stoptime) AND ValueWhen(TimeNum() == ranktime,Gap) <= -GapPer; 

    Short = (Shortcond1 OR Shortcond2) AND Difference <= 10 AND overnight AND exitlastbar == 0 AND excludeok == 0; 

    Covervol = Ref(ATR(Covervp),-1);
    Ctrig = Ref(C,-1) - (Covervol * f);
    Coverlimit = TimeNum()==Covertime AND L < Ctrig ;

    Cover = Coverlimit OR (TimeNum()>Covertime AND TimeNum()<ranktime) OR exitlastbar;

    ShortPrice = IIf(Shortcond1, Max(Open,Strig), Open); 
    CoverPrice = IIf(Coverlimit, Min(Open,Ctrig), Open); 
    */

    PortEquity = Foreign("~~~Equity","C");

    Filter = 1;
    AddColumn(PortEquity,"PortEquity",1.2);
