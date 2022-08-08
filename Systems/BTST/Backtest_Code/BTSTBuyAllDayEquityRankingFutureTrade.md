## BTSTBuyAllDayEquityRankingFutureTrade

    #include <F&O expiry selection.afl>
    #include <F&O BanList.afl>

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

    ranktime = 110000;

    maxtime = 150000;

    buytime = ranktime + buybuffer;

    stoptime = buytime + stopbuffer;

    Selltime = 092500;

    GapPer = 4;

    TimeFrameSet(inDaily);
    NextDay = valuewhen(Day() != Ref(Day(),1),Ref(DateNum(),1));
    NextDay = DateTimeConvert(2,NextDay);
    CurrentDate = DateTimeConvert(2,DateNum());
    Difference = round(DateTimeDiff(NextDay,CurrentDate)/(3600*24));
    TimeFrameRestore();

    Difference = TimeFrameExpand(Difference,inDaily,expandFirst);

    expirysym = IIf(StrRight(Name(),1)=="1",1,0);

    NIIT = IIf( expirysym ==1 AND DateNum() <= 1200626,Foreign("~~BTSTgapall"+ StrReplace(Name(),"NIITTECH.FUT1","COFORGE.EQ-NSE"),"Close"),Foreign("~~BTSTgapall"+ StrReplace(Name(),"NIITTECH.FUT","COFORGE.EQ-NSE"),"Close"));
    TATACONSUM = IIf( expirysym ==1 AND DateNum() <= 1200626,Foreign("~~BTSTgapall"+ StrReplace(Name(),"TATAGLOBAL.FUT1","TATACONSUM.EQ-NSE"),"Close"),Foreign("~~BTSTgapall"+ StrReplace(Name(),"TATAGLOBAL.FUT","TATACONSUM.EQ-NSE"),"Close"));

    gap = IIf((Name() == "NIITTECH.FUT" OR Name() == "NIITTECH.FUT1") AND DateNum() < 1200616,NIIT,IIf((Name() == "TATAGLOBAL.FUT" OR Name() == "TATAGLOBAL.FUT1") AND DateNum() < 1200211 ,TATACONSUM, IIf( expirysym ==1 ,Foreign("~~BTSTgapall"+ StrReplace(Name(),".FUT1",".EQ-NSE"),"Close"),Foreign("~~BTSTgapall"+ StrReplace(Name(),".FUT",".EQ-NSE"),"Close"))));

    Buy = overnight AND gap >= GapPer AND TimeNum() >= ranktime AND TimeNum() < maxtime AND Difference <=10 AND exitlastbar == 0 AND excludeok == 0;

    dow = ValueWhen(Buy,DayOfWeek());

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

    PortEquity = Foreign("~~~Equity","C");

    Filter = 1;
    AddColumn(PortEquity,"PortEquity",1.2);


