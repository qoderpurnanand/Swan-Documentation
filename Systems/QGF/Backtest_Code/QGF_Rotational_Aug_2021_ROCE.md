## QGF_Rotational_Aug_2021_ROCE

    Maxpos = 15;
    SetOption("INitialEquity",1000000);
    SetOption("Maxopenpositions",maxpos);
    SetPositionSize(100/maxpos,spsPercentOfEquity);

    date1 = ValueWhen(Month()!=Ref(Month(),-1) AND Month()==7,DateNum());
    List = CategoryGetSymbols(categoryWatchlist, 0);

    McapLow = 20000;
    McapHigh = 200000;


    if(Status("StockNum") == 0)
    {
    StaticVarRemove("values*");

    for(i = 0; (symbol = StrExtract(List, i)) != ""; i++)
    {
    SetForeign(symbol);

    date1 = ValueWhen(Month()!=Ref(Month(),-1) AND Month()==7,DateNum());
    values = IIf(ValueWhen(DateNum()==date1,Aux2) >= McapLow AND ValueWhen(DateNum()==date1,Aux2) <= McapHigh,ValueWhen(DateNum()==Date1,Aux1),Null);

    RestorePriceArrays();

    StaticVarSet("values" + symbol, values);

    }

    StaticVarGenerateRanks("rank", "values", 0, 1234);

    }

    symbol = Name();
    values = StaticVarGet("values" + symbol);

    rank = StaticVarGet("rankvalues" + symbol);
    llb = 70;// Optimize("llb",190,10,200,10); //70;

    pcase = 3;// Optimize("pcase",2,1,5,1); //3;

    p1 = IIf(pcase == 1, 5, IIf(pcase == 2, 10, IIf(pcase == 3, 20, IIf(pcase == 4, 30, 50))));
    p2 = IIf(pcase == 1, 10, IIf(pcase == 2, 20, IIf(pcase == 3, 40, IIf(pcase == 4, 60, 100))));
    p3 = IIf(pcase == 1, 15, IIf(pcase == 2, 30, IIf(pcase == 3, 60, IIf(pcase == 4, 90, 150))));

    //lti = (ROC(EMA(Close,20),llb) + ROC(EMA(Close,40),llb) + ROC(EMA(Close,60),llb));
    lti = (ROC(EMA(Close,p1),llb) + ROC(EMA(Close,p2),llb) + ROC(EMA(Close,p3),llb));


    List = CategoryGetSymbols(categoryWatchlist, 0);

    if(Status("StockNum") == 0)
    {
    StaticVarRemove("values*");

    for(i = 0; (symbol = StrExtract(List, i)) != ""; i++)
    {
    SetForeign(symbol);
    rank = StaticVarGet("rankvalues" + symbol);
    lti = (ROC(EMA(Close,p1),llb) + ROC(EMA(Close,p2),llb) + ROC(EMA(Close,p3),llb));

    date1 = ValueWhen(Month()!=Ref(Month(),-1) AND Month()==7,DateNum());
    values1 = IIf(rank>=1 AND rank<=30,Max(lti,0),Null);


    RestorePriceArrays();

    StaticVarSet("values1" + symbol, values1);

    }

    StaticVarGenerateRanks("rank", "values1", 0, 1234);

    }

    values1 = StaticVarGet("values1" + symbol);

    finalrank = StaticVarGet("rankvalues1" + symbol);




    Buy = finalrank <= maxpos AND finalrank >=1 AND  Month()!=Ref(Month(),-1) AND lti > 0;
    Sell = (finalrank >maxpos+5 AND Month()!=Ref(Month(),-1));

    BuyPrice = Close;
    SellPrice = Close;

    /*
    SetCustomBacktestProc("");
    if( Status("action") == actionPortfolio )
    {
    bo = GetBacktesterObject();
    bo.Backtest();
    AddToComposite( bo.EquityArray,
    "~~NSE500"+","+McapLow+","+McapHigh, "X",
    atcFlagDeleteValues | atcFlagEnableInPortfolio );
    }
    */


    Filter =1;
    AddColumn(finalrank,"finalrank");
    AddColumn(lti,"lti");
    AddColumn(aux1,"aux1");
    AddColumn(Aux2,"Aux2");
    AddColumn(Open,"Open");
    AddColumn(High,"High");
    AddColumn(Low,"Low");
    AddColumn(Close,"Close");
    AddColumn(Volume,"Volume");
