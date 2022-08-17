## STBTBacktest(ForLive)
    #include <F&O BanList.afl>
    #include <F&O expiry selection.afl>

    bi = BarIndex();
    exitlastbar = LastValue(bi) == bi ; 
    addtime = 0;
    Lev = 1;
    f = 0.1; 
    cf = f;
    vp = 25; 
    Sellvp = 25;
    Shortbuffer = 1500;
    stopbuffer = 1000; 
    maxpos = 10;//Optimize("maxpos",10,5,20,5);

    SetOption("InitialEquity",10000000);
    SetOption("AccountMargin",100/lev);
    SetOption("MaxOpenPositions",maxpos);
    SetPositionSize(100/Maxpos*lev,spsPercentOfEquity);
    SetOption("Priceboundchecking",False);

    SetTradeDelays(0,0,0,0);

    Cases = Optimize("Cases",5,1,7,1);

    if(cases == 1){ranktime = 094500+addtime;}
    if(cases == 2){ranktime = 100000+addtime;}
    if(cases == 3){ranktime = 110000+addtime;}
    if(cases == 4){ranktime = 120000+addtime;}
    if(cases == 5){ranktime = 131000+addtime;}
    if(cases == 6){ranktime = 140000+addtime;}
    if(cases == 7){ranktime = 150000+addtime;}

    Shorttime = ranktime + Shortbuffer;

    stoptime = Shorttime + stopbuffer;

    Covercase = Optimize("Sellcase",2,1,5,1);

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

    Gapper = 4;

    Difference = TimeFrameExpand(Difference,inDaily,expandFirst);

    DayOpen = ValueWhen(TimeNum() == 091500 , Open);//TimeFrameGetPrice("Open",inDaily);
    CurrentClose = ValueWhen(TimeNum() == ranktime , Close);

    gap = ValueWhen(TimeNum()==ranktime,(Currentclose / dayopen - 1) * 100);
    gapOK = ValueWhen(TimeNum() == ranktime , gap <= -gapper);

    vol = ValueWhen(TimeNum() == ranktime,(ATR(vp)));
    strig = Ref(C,-1) + (vol * f);

    trigOK = H > strig;
    nextbaropen = trigok == 0 ;

    Short =  gap <= -gapper AND TimeNum() == Shorttime AND (trigok OR nextbaropen) AND overnight AND exitlastbar==0 AND excludeok == 0;

    covervol = Ref(ATR(vp),-1);
    ctrig = Ref(C,-1) - (covervol * cf);
    coverlimit = IIf(DateNum() == 1200313, TimeNum() == 102000+addtime, TimeNum()==covertime) AND L < ctrig ;

    Cover = coverlimit OR (IIf(DateNum() == 1200313, TimeNum() > 102000+addtime, TimeNum() > covertime) AND TimeNum() < ranktime) OR exitlastbar;

    ShortPrice = IIf( trigok , Max(Open,Strig)*IIf(DateNum() >= 1200301 AND DateNum() <= 1200331,(1-0.003),(1-0.0005)) , IIf(Ref(trigok,1) == 1 AND nextbaropen, Max(Ref(Open,1),Ref(strig,1))*IIf(DateNum() >= 1200301 AND DateNum() <= 1200331,(1-0.003),(1-0.0005)), IIf(Ref(trigok,2) == 1 AND nextbaropen,Max(Ref(Open,2),Ref(strig,2))*IIf(DateNum() >= 1200301 AND DateNum() <= 1200331,(1-0.003),(1-0.0005)), Ref(Open,3)*IIf(DateNum() >= 1200301 AND DateNum() <= 1200331,(1-0.003),(1-0.0010)) )));  // Close;
    CoverPrice =IIf( coverlimit , Min(Open,ctrig)*IIf(DateNum() >= 1200301 AND DateNum() <= 1200331,(1+0.003),(1+0.0005)), Open*IIf(DateNum() >= 1200301 AND DateNum() <= 1200331,(1+0.003),(1+0.001)));

    PositionScore = IIf(Gap <= -gapper , gap, 0); 

    PortEquity = Foreign("~~~Equity","C");

    Filter = 1;//TimeNum()==ranktime;
    AddColumn(Short,"Short",1);
    AddColumn(gap,"gap",1.2);
    AddColumn(gapok,"gapok",1.2);
    AddColumn(PositionScore,"PS",1.2);
    //AddColumn(PortEquity,"PortEquity",1.2);
