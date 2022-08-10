## QGF_Fundamental_Ranking

    maxpos = 20;
    SetOption("InitialEquity",10000000);
    SetOption("Maxopenpositions",maxpos);
    SetPositionSize(100/maxpos,spsPercentOfEquity);

    Mcaplowcase = Optimize("Mcaplowcase",1,1,2,1);

    if(Mcaplowcase == 1){Mcaplow = 500; Mcaphigh = 20000;}
    if(Mcaplowcase == 2){Mcaplow = 20000; Mcaphigh = 50000;}
    if(Mcaplowcase == 3){Mcaplow = 50000; Mcaphigh = 200000;}

    mcap = ValueWhen(Month() == 7 AND Month()!=Ref(Month(),-1),Foreign("~MCAP"+Name(),"C"));

    Cases = Optimize("Cases",1,1,5,1);
    lb = Optimize("lb",1,1,20,1);
    //vp = 10;


    ASCDEC = Optimize("ascdec",1,1,2,1);

    if(Cases == 1)
    {
    // ROCE
    indicator = Foreign("~~F"+Name(),"O",2);
    INDICATOR = IIf(ascdec == 1, indicator, -indicator);


    }

    if(Cases == 2)
    {
    // ROE
    indicator = Foreign("~~F"+Name(),"H",2);
    INDICATOR = IIf(ascdec == 1, indicator, -indicator);

    }

    // Debt/Equity
    DtoE = Foreign("~~F"+Name(),"L",2);

    if(Cases == 3)
    {
    // QOQ PAT growth

    QOQ = Foreign("~~F"+Name(),"V",2);
    QOQ1 = Ref(TimeFrameCompress(QOQ,inQuarterly,compressopen),-lb);
    QOQ2 = TimeFrameExpand(QOQ1,inQuarterly,expandFirst);

    indicator = (QOQ-QOQ2)/abs(QOQ2)*100;
    INDICATOR = IIf(ascdec == 1, indicator, -indicator);

    }


    if(Cases == 4)
    {
    // QOQ EBIT growth

    QOQ = Foreign("~~F"+Name(),"I",2);
    QOQ1 = Ref(TimeFrameCompress(QOQ,inQuarterly,compressopen),-lb);
    QOQ2 = TimeFrameExpand(QOQ1,inQuarterly,expandFirst);

    indicator = (QOQ-QOQ2)/abs(QOQ2)*100;
    INDICATOR = IIf(ascdec == 1, indicator, -indicator);

    }

    if(Cases == 5)
    {
    // QOQ Revenue growth
    QOQ = Foreign("~~F"+Name(),"1",2);
    QOQ1 = Ref(TimeFrameCompress(QOQ,inQuarterly,compressopen),-lb);
    QOQ2 = TimeFrameExpand(QOQ1,inQuarterly,expandFirst);

    indicator = (QOQ-QOQ2)/abs(QOQ2)*100;
    INDICATOR = IIf(ascdec == 1, indicator, -indicator);

    }

    if(Cases == 6)
    {
    // PE ratio = mcap/TTM pat
    mcapdaily = Foreign("~MCAP"+Name(),"C");
    indicator = mcapdaily/Foreign("~~F"+Name(),"2");
    INDICATOR = IIf(ascdec == 1, indicator, -indicator);

    }

    if(Cases == 7)
    {
    // P/B ratio = mcap/sh funds
    mcapdaily = Foreign("~MCAP"+Name(),"C");
    indicator = mcapdaily/Foreign("~~F"+Name(),"C");
    INDICATOR = IIf(ascdec == 1, indicator, -indicator);

    }


    List = CategoryGetSymbols(categoryWatchlist, 2);

    if(Status("StockNum") == 0)
    {
      StaticVarRemove("values*");

      for(i = 0; (symbol = StrExtract(List, i)) != ""; i++)
      {
        SetForeign(symbol);

        mcap = ValueWhen(Month() == 7 AND Month()!=Ref(Month(),-1),Foreign("~MCAP"+Name(),"C"));


        if(Cases == 1)
        {
        // ROCE
        indicator = Foreign("~~F"+Name(),"O",2);
        INDICATOR = IIf(ascdec == 1, indicator, -indicator);


        }

        if(Cases == 2)
        {
        // ROE
        indicator = Foreign("~~F"+Name(),"H",2);
        INDICATOR = IIf(ascdec == 1, indicator, -indicator);

        }


        if(Cases == 3)
        {
        // QOQ PAT growth

        QOQ = Foreign("~~F"+Name(),"V",2);
        QOQ1 = Ref(TimeFrameCompress(QOQ,inQuarterly,compressopen),-lb);
        QOQ2 = TimeFrameExpand(QOQ1,inQuarterly,expandFirst);

        indicator = (QOQ-QOQ2)/abs(QOQ2)*100;
        INDICATOR = IIf(ascdec == 1, indicator, -indicator);

        }


        if(Cases == 4)
        {
        // QOQ EBIT growth

        QOQ = Foreign("~~F"+Name(),"I",2);
        QOQ1 = Ref(TimeFrameCompress(QOQ,inQuarterly,compressopen),-lb);
        QOQ2 = TimeFrameExpand(QOQ1,inQuarterly,expandFirst);

        indicator = (QOQ-QOQ2)/abs(QOQ2)*100;
        INDICATOR = IIf(ascdec == 1, indicator, -indicator);

        }

        if(Cases == 5)
        {
        // QOQ Revenue growth
        QOQ = Foreign("~~F"+Name(),"1",2);
        QOQ1 = Ref(TimeFrameCompress(QOQ,inQuarterly,compressopen),-lb);
        QOQ2 = TimeFrameExpand(QOQ1,inQuarterly,expandFirst);

        indicator = (QOQ-QOQ2)/abs(QOQ2)*100;
        INDICATOR = IIf(ascdec == 1, indicator, -indicator);

        }

        if(Cases == 6)
        {
        // PE ratio = mcap/TTM pat
        mcapdaily = Foreign("~MCAP"+Name(),"C");
        indicator = mcapdaily/Foreign("~~F"+Name(),"2");
        INDICATOR = IIf(ascdec == 1, indicator, -indicator);

        }

        if(Cases == 7)
        {
        // P/B ratio = mcap/sh funds
        mcapdaily = Foreign("~MCAP"+Name(),"C");
        indicator = mcapdaily/Foreign("~~F"+Name(),"C");
        INDICATOR = IIf(ascdec == 1, indicator, -indicator);

        }


        DtoE = Foreign("~~F"+Name(),"L",2);
        TTMPAT =  Foreign("~~F"+Name(),"2");
        exitlastbar = BarIndex() == LastValue(BarIndex());
        shfunds = Foreign("~~F"+Name(),"C");

        values = IIf(mcap >=Mcaplow AND mcap <Mcaphigh and mcap!=0 AND Close > 10 AND IIf(ascdec == 1,  indicator > 0 AND DtoE > 0 AND TTMPAT > 0, indicator > 0)  AND shfunds > 0  AND exitlastbar == 0 AND SectorID() != 6 AND SectorID() != 3 AND IndustryID() != 25,Indicator,Null);

        RestorePriceArrays();

        StaticVarSet("values" + symbol, values);

      }

      StaticVarGenerateRanks("rank", "values", 0, 1234);

    }

    symbol = Name();
    values = StaticVarGet("values" + symbol);

    rank = StaticVarGet("rankvalues" + symbol);

    DtoE = Foreign("~~F"+Name(),"L",2);
    TTMPAT =  Foreign("~~F"+Name(),"2");

    d1 = DateNum();
    d1ref = Ref(DateNum(),-1);
    d2 = DateTimeConvert(2,d1);
    d2ref = DateTimeConvert(2,d1ref);
    datediff = DateTimeDiff(d2,d2ref)/86400;

    exitlastbar = BarIndex() == LastValue(BarIndex());

    Buy = rank > 0 AND rank <= maxpos AND Month()==7 AND Month()!=Ref(Month(),-1) AND IIf(Name()=="AVANTIFEED.EQ-NSE",Year() >= 2015,1) and mcap>=mcaplow AND datediff < 60 AND Close > 10 AND exitlastbar == 0;
    Sell = (rank > maxpos AND Month()==7 AND Month()!=Ref(Month(),-1)) OR exitlastbar OR (Month()==7 AND Month()!=Ref(Month(),-1) AND mcap > mcaphigh);

    //Buy = rank <= maxpos AND rank >=1 AND Month()==7 AND Month()!=Ref(Month(),-1) AND Name()!="AVANTIFEED.EQ-NSE" and aux2>mcaplow AND datediff < 60;
    //Sell = rank > maxpos AND Month()==7 AND Month()!=Ref(Month(),-1);

    BuyPrice = Close;
    SellPrice = Close;

    /*
    SetCustomBacktestProc("");
    if( Status("action") == actionPortfolio )
    {
    bo = GetBacktesterObject();
    bo.Backtest();
    AddToComposite( bo.EquityArray,
    "~~QGF"+","+McapLow+","+McapHigh, "X",
    atcFlagDeleteValues | atcFlagEnableInPortfolio );
    }
    */
    ROE = Foreign("~~F"+Name(),"H",2);


    Filter =1;//mcap>=mcaplow AND mcap<mcaphigh AND datediff < 60 AND Close > 10 AND exitlastbar == 0;

    AddColumn(rank,"rank");
    AddColumn(values,"values");
    AddColumn(indicator,"indicator");
    AddColumn(Open,"Open");
    AddColumn(mcap,"mcap");
    AddColumn(exitlastbar,"exitlastbar");
