## MMR Ranking + Backtest Code

    #include <Includeok.afl>

    bi = BarIndex();
    exitLastBar = bi == LastValue( bi );
    maxpos = 10;

    SetOption("InitialEquity",10000000);
    SetOption("AccountMargin",100);
    SetOption("MaxOpenPositions",maxpos);
    SetTradeDelays(0,0,0,0);
    SetPositionSize(100/maxpos,spsPercentOfEquity);

    ///// Code to count number of bars in the month/////////

    x = IIf(Year() > Ref(Year() ,-1),1, IIf( Month() > Ref(Month() ,-1),1,0));
    y = IIf(Year() < Ref(Year() ,1),1, IIf( Month() < Ref(Month() ,1),1,0));

    xdate = BarsSince(x);//// will give the number of bars in the month 

    vp = 4;//Optimize("vp",4,1,4,3);
    f =  0.2;//Optimize("f",0.3,0.1,0.3,0.1);
    xf = 0.2;//Optimize("xf",0.4,0.1,0.3,0.1);
    llb = 8;//Optimize("llb",10,2,30,6);
    //MAllb = Optimize("MAllb",100,20,100,20);

    prevbars = Optimize("prevbars",20,1,5,1);
    startperiod = Ref(y,prevbars-1);

    Buycond = Sum(startperiod,prevbars);
    dayOK = Buycond == 1;

    //r = Optimize("r",1,1,30,1);
    maxrank = 30;

    watchlist = 0;

    List = CategoryGetSymbols(categoryWatchlist,watchlist);

    if ( Status("stocknum") == 0 ) // Generate ranking when we are on the very first symbol
    {
      StaticVarRemove( "values*" );

      for ( n = 0; ( Symbol = StrExtract( List, n ) )  != "";  n++    )
      {
        SetForeign ( symbol );

        #include <Includeok.afl>


        bi = BarIndex();
        exitLastBar = bi == LastValue( bi );
        rankday = IIf(dayOK == 0 AND Ref(dayOK,1) == 1,1,0);
        lti = ValueWhen(rankday,ROC(EMA(Close,10),llb) + ROC(EMA(Close,20),llb) + ROC(EMA(Close,30),llb));
        values = IIf(includeOK AND exitLastBar == 0 , lti, Null);
        RestorePriceArrays();
        StaticVarSet (  "values"  +  symbol, values );
        _TRACE( symbol );
        }

      StaticVarGenerateRanks( "rank", "values", 0, 1234 );
    }

    symbol = Name();
    values = StaticVarGet ( "values" +  symbol );
    rank = StaticVarGet ( "rankvalues" +  symbol );


    rankday = IIf(dayOK == 0 AND Ref(dayOK,1) == 1,1,0);

    poi = Ref(Close,-1);////ValueWhen(Rankday,Close);
    vol = Ref(ATR(Vp),-1);//ValueWhen(rankday,ATR(vp));//;
    //lti = ValueWhen(rankday,ROC(EMA(Close,20),llb) + ROC(EMA(Close,40),llb) + ROC(EMA(Close,60),llb));

    Buycond = Sum(startperiod,prevbars);

    dist = vol * f;
    xdist = vol * xf;

    bl = poi - dist;
    sl = poi + xdist;

    dayOK = Buycond == 1;
    rankOK = rank <= maxrank;
    trigOK = L <= bl;
    xtrigOK = H >= sl;



    Buy = includeOK AND dayOK AND rankok AND trigOK AND exitLastBar == 0 ;
    BuyPrice = Min(Open,bl);

    ldw = xdate == 0;
    //ldw = buycond == 0 AND Ref(buycond,1) == 1;
    Sell = ldw OR exitLastBar OR includeOK == 0;
    SellPrice = IIf(xdate == 0 AND xtrigOK , Max(Open,sl) , Close);

    Buy = ExRem(Buy,Sell);
    Sell = ExRem(Sell,Buy);

    PositionScore = Random();

    Filter = 1;
    //AddColumn(rank,"Rank");
    //AddColumn(values,"values");
    AddColumn(startperiod,"startperiod");
    AddColumn(dayOK,"Dayok");
    AddColumn(xdate,"xdate");
    AddColumn(ValueWhen(rankday,Close),"Close");
