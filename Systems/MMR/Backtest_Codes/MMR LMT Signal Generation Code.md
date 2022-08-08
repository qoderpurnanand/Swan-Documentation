## MMR LMT Signal Generation Code

    maxpos = 10;
    addtime = 459 ;

    MMR1EQ1 = 10000000;
    MMR1lev = 1;

    SetOption("InitialEquity",MMR1EQ1);
    SetOption("AccountMargin",100/MMR1lev);
    SetOption("MaxOpenPositions",maxpos);
    SetTradeDelays(0,0,0,0);
    SetPositionSize(100/maxpos*MMR1lev,spsPercentOfEquity);

    vp = 5 ;
    f =  Optimize("f",0.1,0.1,0.5,0.1);
    llb = Optimize("llb",10,10,30,10);
    ef = 10/100 ;
    buytimesec = 900 ; // 15 mins
    selltimesec = 900 ; // 15mins
    vp2 = 25;
    sellvp = 25;
    starttime = 091500+addtime;
    selltime = 093000+addtime;//Optimize("selltime",094000,092000,94500,500);


    TimeFrameSet(inDaily);
    bi = BarIndex();
    exitLastBar = bi == LastValue( bi );

    x = IIf(Year() > Ref(Year() ,-1),1, IIf( Month() > Ref(Month() ,-1),1,0));
    y = IIf(Year() < Ref(Year() ,1),1, IIf( Month() < Ref(Month() ,1),1,0));

    xdate = BarsSince(x);//// will give the number of bars in the month 
    prevbars = 3;
    startperiod = Ref(y,prevbars-1);

    Buycond = Sum(startperiod,prevbars);
    dayOK = Buycond == 1;
    rankday = IIf(dayOK == 0 AND Ref(dayOK,1) == 1,1,0);

    poi = Ref(Close,-1);
    vol = Ref(ATR(Vp),-1);

    RestorePriceArrays();

    xdate = TimeFrameExpand(xdate,inDaily,expandFirst);
    buycond = TimeFrameExpand(buycond,inDaily,expandFirst);
    Dayok = TimeFrameExpand(dayok,inDaily,expandFirst);
    Poi = TimeFrameExpand(poi,inDaily,expandFirst);
    Vol = TimeFrameExpand(Vol,inDaily,expandFirst);
    exitlastbar = TimeFrameExpand(exitlastbar,inDaily,expandFirst);

    rank = Foreign("~~MMRRank" + Name(),"Close");

    rankok = rank >=1 AND  rank <=30;


    dist = vol * f;
    xdist = vol * xf;

    bl = poi - dist;
    sl = poi + xdist;

    open1 = TimeFrameGetPrice("O",inDaily);

    trigOK = LowestSince(Day() != Ref(Day(),-1),L) <= Min(bl,open1) AND dayok AND TimeNum()>=starttime+addtime AND rankok;

    triggertime = ValueWhen(trigok, TimeNum());

    bl1 = Ref(C,-1) - ValueWhen(triggertime, ATR(vp2)*ef);

    Buy1 = dayOK AND Ref(trigOK,-1) /*AND exitLastBar == 0 AND L < bl1*/ AND IIf(day1,TimeNum()>=100000+addtime,TimeNum() >= starttime+addtime)  ;

    Buytime = ValueWhen(Ref(buy1,-1) != Buy1 AND Buy1 == 1, TimeNum());
    dn = DateNum();
    dt = DateTimeConvert( 2 , dn , buytime );
    dt2 = DateTimeAdd( dt, buytimesec , in1Second );
    buyendtime = DateTimeConvert( 1 , dt2) ;
    buytimeok = TimeNum() >= buytime AND TimeNum() < buyendtime ; 

    Buy = (buy1 AND buytimeok AND L < bl1) OR ( TimeNum() >= buyendtime AND Buy1 AND Ref(buytimeok,-1)) AND rankok; 
    BuyPrice = IIf(L < bl1 AND buytimeok,Min(Open,bl1),Open);

    ldw = xdate == 0;


    prevbarsell = ValueWhen(TimeNum() == selltime, Ref(TimeNum(),-1));
    sellatr = ValueWhen(TimeNum() == prevbarsell, ATR(sellvp) ) ; 
    strig = Ref(Close,-1) + (Ref(ATR(25),-1)*ef);

    dt3 = DateTimeConvert( 2 , dn , selltime );
    dt4 = DateTimeAdd( dt3 , selltimesec , in1Second );
    sellendtime = DateTimeConvert( 1 , dt4 ) ;
    selltimeok = TimeNum() >= selltime AND TimeNum() < sellendtime ; 

    sell1 = (selltimeok AND ldw AND H > strig );
    Sell2 = (ldw AND Ref(selltimeok,-1) AND TimeNum() >= sellendtime AND TimeNum() < 150000) ;

    Sell = Sell1 OR sell2 ;
    SellPrice = IIf(sell1,Max(Open,strig), Open);

    PositionScore = Random();

