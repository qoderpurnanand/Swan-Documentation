## BTST Backtest (for live)

    #include <F&O Expiry selection.afl> 
    #include <F&O BanList.afl> 

    Bi = BarIndex(); 
    Exitlastbar = LastValue(bi) == bi ;  
    Addtime = 0; 
    Lev = 2; 
    Maxpos = 10; 
    f = 0.1; 
    Buyvp = 25; 
    Sellvp = 25; 

    SetOption("InitialEquity",10000000); 
    SetOption("AccountMargin",100/lev); 
    SetOption("MaxOpenPositions",maxpos); 
    SetPositionSize(100/Maxpos*lev,spsPercentOfEquity); 

    SetOption("Priceboundchecking",False); 

    SetTradeDelays(0,0,0,0); 

    TimeFrameSet(inDaily); 
    Fdw = DayOfWeek() < Ref(DayOfWeek(),-1); 
    TimeFrameRestore(); 
    Fdw = TimeFrameExpand(Fdw,inDaily,expandFirst); 

    Expirysym = IIf(StrRight(Name(),1)=="1",1,0); 

    NIIT = IIf( Expirysym ==1 AND DateNum() <= 1200730,Foreign("~~BTSTgapall"+ StrReplace(Name(),"NIITTECH.FUT1","COFORGE.EQ-NSE"),"Close"),Foreign("~~BTSTgapall"+ StrReplace(Name(),"NIITTECH.FUT","COFORGE.EQ-NSE"),"Close")); 
    TATACONSUM = IIf( Expirysym ==1 AND DateNum() <= 1200131,Foreign("~~BTSTgapall"+ StrReplace(Name(),"TATAGLOBAL.FUT1","TATACONSUM.EQ-NSE"),"Close"),Foreign("~~BTSTgapall"+ StrReplace(Name(),"TATAGLOBAL.FUT","TATACONSUM.EQ-NSE"),"Close")); 
    INDUSTOWER = IIf( Expirysym ==1 AND DateNum() <= 1201218,Foreign("~~BTSTgapall"+ StrReplace(Name(),"INFRATEL.FUT1","INDUSTOWER.EQ-NSE"),"Close"),Foreign("~~BTSTgapall"+ StrReplace(Name(),"INFRATEL.FUT","INDUSTOWER.EQ-NSE"),"Close")); 

    Gap = IIf((Name() == "NIITTECH.FUT" OR Name() == "NIITTECH.FUT1") AND DateNum() < 1200730,NIIT,IIf((Name() == "TATAGLOBAL.FUT" OR Name() == "TATAGLOBAL.FUT1") AND DateNum() < 1200131 ,TATACONSUM, IIf((Name() == "INFRATEL.FUT" OR Name() == "INFRATEL.FUT1") AND DateNum() < 1201218 ,INDUSTOWER, IIf( expirysym ==1 ,Foreign("~~BTSTgapall"+ StrReplace(Name(),".FUT1",".EQ-NSE"),"Close"),Foreign("~~BTSTgapall"+ StrReplace(Name(),".FUT",".EQ-NSE"),"Close"))))); 

    Ranktime = iif(Dayofweek()==1,101000+Addtime,121000+Addtime); 

    BuyTime = IIf(Dayofweek()==1,102500+Addtime,122500+Addtime); 

    StopTime = IIf(DayOfWeek()==1,114000+Addtime,124000+Addtime); 

    Selltime = 092500+Addtime; 

    Gapok = 3; 

    Prevbars = 3;

    Vol = ValueWhen(TimeNum()== Ranktime,(ATR(Buyvp))); 

    Btrig = Ref(C,-1) - (Vol * f); 

    EntrytimeOK = TimeNum() >= Buytime AND TimeNum() < Stoptime;  

    TrigOK = L < Btrig; 

    Buycond1 = (TrigOK AND EntrytimeOK) AND ValueWhen(TimeNum() == Ranktime,Gap) >= Gapok; 
    Buycond2 = (TimeNum() >= Stoptime) AND ValueWhen(TimeNum() == Ranktime,Gap) >= Gapok; 

    TimeFrameSet(inDaily); 
    Newday = Day() != Ref(Day(),-1); 

    X = IIf(Year() > Ref(Year() ,-1),1, IIf( Month() > Ref(Month() ,-1),1,0)); 
    Y = IIf(Year() < Ref(Year() ,1),1, IIf( Month() < Ref(Month() ,1),1,0)); 

    Xdate = BarsSince(X);  

    Startperiod = Ref(Y,Prevbars-1); 

    Buycond = Sum(Startperiod,Prevbars); 
    DayOK = Buycond == 1; 

    TimeFrameRestore(); 
    Newday = TimeFrameExpand(newday,inDaily,expandFirst); 
    Dayok = TimeFrameExpand(dayok,inDaily,expandFirst); 
    TimeFrameSet(inDaily);

    NextDay = valuewhen(Day() != Ref(Day(),1),Ref(DateNum(),1));
    NextDay = DateTimeConvert(2,NextDay);
    CurrentDate = DateTimeConvert(2,DateNum());
    Difference = round(DateTimeDiff(NextDay,CurrentDate)/(3600*24));
    TimeFrameRestore();

    Difference = TimeFrameExpand(Difference,inDaily,expandFirst);

    Buy = (Buycond1 OR buycond2) AND Difference <= 10 AND Overnight AND Exitlastbar == 0 AND Excludeok == 0 AND IIf(DateNum() >= 1200901, Dayok == 0,1); 

    Dow = ValueWhen(Buy,DayOfWeek()); 

    Sellvol = Ref(ATR(Sellvp),-1); 
    Strig = Ref(C,-1) + (Sellvol * f); 
    Selllimit = IIf(DateNum() == 1200313, TimeNum() == 102000+Addtime, TimeNum()==Selltime) AND H > Strig; 

    Sell = Selllimit OR (IIf(DateNum() == 1200313, TimeNum() > 102000+Addtime,TimeNum()>Selltime) AND TimeNum()<Ranktime) OR Exitlastbar; 

    Dow = ValueWhen(Buy,DayOfWeek());

    BuyPrice = IIf( buycond1, Min(Open,btrig)*IIf(DateNum() >= 1200301 AND DateNum() <= 1200331,(1+0.0005),(1+0.0005)), Open*IIf(DateNum() >= 1200301 AND DateNum() <= 1200331,(1+0.0005),(1+0.001))); 
    SellPrice = IIf(selllimit, max(Open,strig)*IIf(DateNum() >= 1200301 AND DateNum() <= 1200331,(1-0.0005),(1-0.0005)), Open*IIf(DateNum() >= 1200301 AND DateNum() <= 1200331,(1-0.0005),(1-0.001))); 

    PortEquity = Foreign("~~~Equity","C");

    Filter = 1;
    AddColumn(PortEquity,"PortEquity",1.2);
