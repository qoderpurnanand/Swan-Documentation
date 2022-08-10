## QGF_Rotational_PS

    //#include<Rotationalincludeok.afl>
    EnableRotationalTrading();

    //#include <QGF Include.afl>

    maxpos = 5;
    //SetOption("InitialEquity", 3113423.16);
    SetOption("InitialEquity",  10000000);  //3035587
    SetOption("AccountMargin",100);
    SetOption("MaxOpenPositions",maxpos);
    SetTradeDelays(0,0,0,0);
    SetPositionSize(100/maxpos,spsPercentOfEquity);
    SetOption("WorstRankHeld",maxpos+5);
    //SetTradeDelays(1,1,0,0);

    MCAPLOW = 500;
    MCAPHIGH = 5000000;
    //includeok = IIf(Aux2 >= 500 AND Aux2<=20000,1,0);

    //llb = 60; 4;
    llb = 70;// Optimize("llb",190,10,200,10); //70; 

    pcase = 3;// Optimize("pcase",2,1,5,1); //3;

    p1 = IIf(pcase == 1, 5, IIf(pcase == 2, 10, IIf(pcase == 3, 20, IIf(pcase == 4, 30, 50))));
    p2 = IIf(pcase == 1, 10, IIf(pcase == 2, 20, IIf(pcase == 3, 40, IIf(pcase == 4, 60, 100))));
    p3 = IIf(pcase == 1, 15, IIf(pcase == 2, 30, IIf(pcase == 3, 60, IIf(pcase == 4, 90, 150))));

    //lti = (ROC(EMA(Close,20),llb) + ROC(EMA(Close,40),llb) + ROC(EMA(Close,60),llb));
    lti = (ROC(EMA(Close,p1),llb) + ROC(EMA(Close,p2),llb) + ROC(EMA(Close,p3),llb));

    date1 = ValueWhen(Month()!=Ref(Month(),-1) AND Month()==7,DateNum());
    mcapfilter = ValueWhen(DateNum()==date1,Aux2) >= McapLow AND ValueWhen(DateNum()==date1,Aux2) <= McapHigh;
    ROCE = ValueWhen(DateNum()==date1,Aux1);

    monthchange = Month() != Ref(Month(),-1); 
    weekchange = DayOfWeek() > Ref(DayOfWeek(),1);  

    PositionScore = IIf(weekchange == 0 , scoreNoRotate , IIf(/*includeok AND*/ weekchange AND Close > 10 AND mcapfilter , Max(LTI,0) , 0));

    Filter = DateNum()==1150102;

    //AddColumn(DayOfWeek(),"DayOfWeek()");
    //AddColumn(Ref(DayOfWeek(),1),"Ref(DayOfWeek(),1)");
    //AddColumn(Close,"Close");
    AddColumn(lti,"lti",1.4);
    SetSortColumns(-3);
    AddRankColumn();
    //AddColumn(ClosingGap ,"ClosingGap");
    AddColumn(PositionScore,"PositionScore");
    AddColumn(weekchange,"Weekchange");
