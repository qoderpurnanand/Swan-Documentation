## Simple_Backtest_Code

    SetOption("InitialEquity",1000000);
    SetOption("Maxopenpositions",30);
    SetPositionSize(100/30,spsPercentOfEquity);

    #Include <QGFIncludeok.afl>

    bi = BarIndex();
    exitLastBar = bi == LastValue( bi );

    Buy = Includeok==1;
    Sell = Includeok==0 OR exitlastbar;

    BuyPrice =Close;
    SellPrice =Close;
