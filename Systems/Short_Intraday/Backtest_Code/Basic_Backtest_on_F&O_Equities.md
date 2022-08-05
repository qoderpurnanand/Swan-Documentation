    maxpos = 10; //Optimize("mp",10,1,10,1);

    SetOption("MaxOpenPositions",maxpos);
    SetOption("InitialEquity",10000000);
    SetOption("AccountMargin",100/1);
    SetPositionSize(100/maxpos*1,spsPercentOfEquity);
    SetTradeDelays(0,0,0,0);
    //SetOption("PriceBoundChecking",False);

    dayx = 1; //Optimize("dayx",1,1,5,1);

    ef = Optimize("f",0.1,0,0.5,0.1);
    xf = 0; //Optimize("f",0.2,0,0.5,0.1);
    vp = Optimize("vp",1,1,15,1);
    rlb = 1; //Optimize("rlb",1,1,5,1);

    paramLenRSI = Param("RSI Closes Length", 3, 2, 100, 1);
    paramLenUD = Param("RSI UpClose Length", 2, 2, 100, 1);
    paramLenRank = Param("PerecentRank Length", 100, 10, 200, 1);

    function ConnorsRSI(lenRSI, lenUD, lenROC)
    {
          upDays = BarsSince(C <= Ref(C,-1));
          downDays = BarsSince(C >= Ref(C,-1));
          updownDays = IIf(upDays > 0, upDays, IIf(downDays > 0, -downDays, 0));
          crsi = ( PercentRank(ROC(C,1), lenROC) + RSIa(updownDays,lenUD) +RSI(lenRSI))/3;
          return crsi;
    }

    factor = 1; //Optimize("factor",1,1,3,0.5);

    stop = 3; //Optimize("stop",1,2,5,1);

    r = 1; //Optimize("r",1,1,100,1);

    watchlist = 0;

    List = CategoryGetSymbols(categoryWatchlist,watchlist);

    if ( Status("stocknum") == 0 ) // Generate ranking when we are on the very first symbol
    {
      StaticVarRemove( "values*" );

      for ( n = 0; ( Symbol = StrExtract( List, n ) )  != "";  n++    )
      {
        SetForeign ( symbol );
        {
          #include <includeok.afl>
        }
        crsi = ConnorsRSI(3,2,100);
        values = IIf(includeOK AND Ref(Volume,-1) > (Ref(MA(Volume,50),-1) * factor) AND Ref(C,-1) > Ref(C,-2) , /*Ref(ROC(C,rlb),-1) Ref(PercentRank(ATR(vp),100),-1)*/ Ref(crsi,-1) , Null);
        RestorePriceArrays();
        StaticVarSet (  "values"  +  symbol, values );
        _TRACE( symbol );
        }

      StaticVarGenerateRanks( "rank", "values", 0, 1234 );
    }

    symbol = Name();
    values = StaticVarGet ( "values" +  symbol );
    rank = StaticVarGet ( "rankvalues" +  symbol );

    {
      #include <includeok.afl>
    }

    poi = Ref(C,-1);
    edist = Ref(ATR(vp),-1) * ef;
    xdist = Ref(ATR(vp),-1) * xf;

    strig = poi + edist;
    ctrig = poi - xdist;

    strade = H >= strig;
    rankOK = rank <= 10;

    ctrade = L <= ctrig;

    upday = Ref(Volume,-1) > (Ref(MA(Volume,50),-1) * factor) AND Ref(C,-1) > Ref(C,-2);

    Short = strade AND rankOK AND includeOK AND upday;// AND DayOfWeek() != dayx;
    ShortPrice = IIf(Max(Open,strig) == Open , Open * 1 , strig);

    Cover = Short;
    CoverPrice = C * 1;

    //ApplyStop(stopTypeLoss,stopModePercent,stop);

    PositionScore = Random();

    Filter = includeOK;
    AddColumn(rank,"rank");
    AddColumn(values,"values");
    //AddColumn(PercentRank(ATR(vp),100),"atrpr");
    //AddColumn(C,"Eq");
