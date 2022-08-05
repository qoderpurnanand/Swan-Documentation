    #include <Includeok.afl>
    #include <Banlist.afl>

    EnableRotationalTrading();

    Lev = 1;
    Maxpos = 15;//Optimize("Maxpos",10,10,20,5);
    Worstrank = Maxpos + Optimize("Worstrank",5,2,10,2);
    Eq = 10000000;
    SetOption("InitialEquity",Eq);
    SetOption("AccountMargin",100/Lev);
    SetPositionSize(100/maxpos*Lev,spsPercentOfEquity);
    //SetPositionSize(Eq/Lev*Maxpos,spsValue);
    SetOption("Maxopenpositions",Maxpos);
    SetOption("Worstrankheld",Worstrank);

    sma = Optimize("Sma",10,10,80,20);
    Slb = Optimize("Slb",10,10,80,20);
    emallb = Optimize("emallb",20,80,240,80);

    Nifty = Foreign("$NIFTY-NSE","Close");//Foreign("$NIFTY_50-NSE","Close");


    sniftyma = MA(Nifty,sma);

    sti = (ROC(EMA(Close,emallb),Slb) + ROC(EMA(Close,emallb+20),slb) + ROC(EMA(Close,emallb+40),slb));

    //PositionSize = -100/maxpos;
    PositionScore = IIf( nifty < sniftyma AND IncludeOk and sti < 0 AND excludeok==0 , Min(sti,0) ,0);

    CHG = ((Close/Ref(Close,-1)) -1)*100;

    //Eq= Foreign("~~~Equity","Close");

    Filter =1;
    AddColumn(sti,"sti");
    AddRankColumn();
