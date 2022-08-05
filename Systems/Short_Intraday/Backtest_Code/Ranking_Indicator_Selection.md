## RANKING INDICATOR SELECTION
    #include <includeok.afl>

    maxpos = 10;
    lev = 1;
    initialcap = 10000000;

    SetOption("MaxOpenPositions",maxpos);
    SetOption("InitialEquity",initialcap);
    SetOption("AccountMargin",100/Lev);
    SetPositionSize(100/maxpos*lev,spsPercentOfEquity);

    SetTradeDelays(0,0,0,0);
    lb = Optimize("lb",5,1,10,2);

    ef = Optimize("ef",1,1,3,1)/10;
    //r = Optimize("r",1,1,25,1);
    vp = 5;//Optimize("vp",11,1,12,2);
    //sd = Optimize("sd",1.1,1.1,1.4,0.1);
    Cases = Optimize("Cases",2,1,24,1);


    paramLenRSI = 3; //Param("RSI Closes Length", crsilb, crsilb, 100, 1);
    paramLenUD = 2; //Param("RSI UpClose Length", 2, 2, 100, 1); // ask
    paramLenRank = 100; //Param("PerecentRank Length", 100, 10, 200, 1); // ask

    function ConnorsRSI(lenRSI, lenUD, lenROC)
    {
          upDays = BarsSince(C <= Ref(C,-1));
          downDays = BarsSince(C >= Ref(C,-1));
          updownDays = IIf(upDays > 0, upDays, IIf(downDays > 0, -downDays, 0));
          crsi = ( PercentRank(ROC(C,1), lenROC) + RSIa(updownDays,lenUD) +RSI(lenRSI))/3;

         return crsi;

    }


    ASCDEC = 1;//Optimize("ASCDEC",1,1,2,1);
    Rankcase = 1;//Optimize("Rankcase",1,1,11,1);
    rn = 10;

    minrank = IIf(rankcase == 1,1,IIf(rankcase == 2,rn, IIf(rankcase == 3,rn*2,IIf(rankcase == 4,rn*3,IIf(rankcase == 5,rn*4,IIf(rankcase == 6,rn*5,IIf(rankcase == 7,rn*6,IIf(rankcase == 8,rn*7,IIf(rankcase == 9,rn*8,IIf(rankcase == 10,rn*9, IIf(rankcase == 11,rn*10,null)))))))))));
    maxrank = IIf(rankcase == 1,rn,IIf(rankcase == 2,rn*2, IIf(rankcase == 3,rn*3,IIf(rankcase == 4,rn*4,IIf(rankcase == 5,rn*5,IIf(rankcase == 6,rn*6,IIf(rankcase == 7,rn*7,IIf(rankcase == 8,rn*8,IIf(rankcase == 9,rn*9,IIf(rankcase == 10,rn*10, IIf(rankcase == 11,rn*11,null)))))))))));

    /*
    minrank = IIf(ascdec == 1, 1, 343);
    Maxrank = IIf(ascdec == 1, 50, 393);
    */

    if(Cases == 1)
    {
    //ATRPR
    Indicator = Ref(PercentRank(ATR(vp),100),-1);
    INDICATOR = IIf(ascdec == 1, indicator, -indicator);

    }

    if(Cases == 2)
    {
    //ROC Price
    Indicator = Ref(ROC(Close,lb),-1);
    INDICATOR = IIf(ascdec == 1, indicator, -indicator);

    }

    if(Cases == 3)
    {
    //ROC Volume
    Indicator = Ref(ROC(Volume,lb),-1);
    INDICATOR = IIf(ascdec == 1, indicator, -indicator);

    }

    if(Cases == 4)
    {
    //CRSI
    Indicator = ConnorsRSI(paramLenRSI,paramLenUD,paramLenRank);
    INDICATOR = IIf(ascdec == 1, indicator, -indicator);

    }

    if(Cases == 5)
    {
    //Z Score
    mb = MA(C,lb+1);
    Indicator = Ref((C - mb) / (StDev(C,lb+1)),-1);
    INDICATOR = IIf(ascdec == 1, indicator, -indicator);

    }

    if(Cases == 6)
    {
    //LTI
    Ltilb = 10; // check
    Indicator = Ref(ROC(EMA(Close,ltilb),lb) + ROC(EMA(Close,ltilb*2),lb) + ROC(EMA(Close,ltilb*3),lb),-1);
    INDICATOR = IIf(ascdec == 1, indicator, -indicator);

    }

    if(Cases == 7)
    {
    //RSI Price
    Indicator = Ref(RSIa(Close,14),-1);
    INDICATOR = IIf(ascdec == 1, indicator, -indicator);

    }

    if(Cases == 8)
    {
    //RSI Volume
    Indicator = Ref(RSIa(Volume,14),-1);
    INDICATOR = IIf(ascdec == 1, indicator, -indicator);

    }

    if(Cases == 9)
    {
    // ROC MA 
    Indicator = Ref(ROC(MA(Close,lb),lb),-1);
    INDICATOR = IIf(ascdec == 1, indicator, -indicator);

    }

    if(Cases == 10)
    {
    // ROC Price PR 
    Indicator = Ref(PercentRank(ROC(Close,lb),100),-1);
    INDICATOR = IIf(ascdec == 1, indicator, -indicator);

    }

    if(Cases == 11)
    {
    // PIR = Stoch K
    Indicator = Ref(StochK(14),-1);
    INDICATOR = IIf(ascdec == 1, indicator, -indicator);

    }

    if(Cases == 12)
    {
    // Stoch D
    Indicator = Ref(StochD(14,3,3),-1);
    INDICATOR = IIf(ascdec == 1, indicator, -indicator);

    }

    if(Cases == 13)
    {
    // ATR/C
    Indicator = Ref(ATR(vp)/Close,-1)*100;
    INDICATOR = IIf(ascdec == 1, indicator, -indicator);

    }

    if(Cases == 14)
    {
    // STDEV.P
    Indicator = Ref(StDev(ROC(Close,lb),100,True),-1);
    INDICATOR = IIf(ascdec == 1, indicator, -indicator);

    }

    if(Cases == 15)
    {
    // Beta
    Periods = Param("period",8,1,50,1);
    ticker = ParamStr( "Ticker", "$NIFTY-NSE" );
    P = Foreign(TICKER,"C",lb);
    Indicator = (( Periods * Sum(ROC( C,lb) * ROC(P,lb),Periods )) - (Sum(ROC(C,lb),Periods) * Sum(ROC( P,lb),Periods))) / ((Periods * Sum((ROC(P,lb)^2 ),Periods)) - (Sum(ROC(P,lb ),Periods)^2 ));
    INDICATOR = IIf(ascdec == 1, Indicator, -Indicator);

    }

    if(Cases == 16)
    {
    // ABS ROC
    Indicator = Ref(abs(ROC(Close,lb)),-1);
    INDICATOR = IIf(ascdec == 1, indicator, -indicator);

    }

    if(Cases == 17)
    {
    // PR ABS ROC
    Indicator = Ref(PercentRank(abs(ROC(Close,lb)),100),-1);
    INDICATOR = IIf(ascdec == 1, indicator, -indicator);

    }


    if(Cases == 18)
    {
    // Vol PIR
    Indicator = Ref((Volume - LLV(Volume,14)) / (HHV(Volume,14) - LLV(Volume,14)) ,-1)*100;
    INDICATOR = IIf(ascdec == 1, indicator, -indicator);

    }

    if(Cases == 19)
    {
    // Vol PR
    Indicator = Ref(PercentRank(Volume,100),-1); 
    INDICATOR = IIf(ascdec == 1, indicator, -indicator);

    }

    if(Cases == 20)
    {
    // Close PR
    Indicator = Ref(PercentRank(Close,100),-1); 
    INDICATOR = IIf(ascdec == 1, indicator, -indicator);

    }

    if(Cases == 21)
    {
    //Volume Z Score
    mb = MA(Volume,lb+1);
    Indicator = Ref((Volume - mb) / (StDev(Volume,lb+1)),-1);
    INDICATOR = IIf(ascdec == 1, indicator, -indicator);

    }

    if(Cases == 22)
    {
    //MACD
    r1 = Param( "Fast avg", 12, 2, 200, 1 );
    r2 = Param( "Slow avg", 26, 2, 200, 1 );
    r3 = Param( "Signal avg", 9, 2, 200, 1 ); 

    m1=MACD(r1,r2);
    s1=Signal(r1,r2,r3);
    //a=Cross(m1,s1);

    Indicator = Ref(PercentRank(s1,100),-1); 
    INDICATOR = IIf(ascdec == 1, indicator, -indicator);

    }

    if(Cases == 23)
    {
    //MFI - Similar to RSI but consideres Volume and Price
    Indicator = Ref(MFI(lb),-1);
    INDICATOR = IIf(ascdec == 1, indicator, -indicator);

    }

    if(Cases == 24)
    {
    // MA ATR/C
    Indicator = Ref(MA(ATR(vp)/Close,lb),-1)*100; 
    INDICATOR = IIf(ascdec == 1, indicator, -indicator);

    }


    watchlist = 0;

    List = CategoryGetSymbols(categoryWatchlist,watchlist);

    if ( Status("stocknum") == 0 ) // Generate ranking when we are on the very first symbol
    {
      StaticVarRemove( "values*" );

      for ( n = 0; ( Symbol = StrExtract( List, n ) )  != "";  n++    )
      {
        SetForeign ( symbol );

        #include <includeok.afl>  

        if(Cases == 1)
        {
        //ATRPR
        Indicator = Ref(PercentRank(ATR(vp),100),-1);
        INDICATOR = IIf(ascdec == 1, indicator, -indicator);

        }

        if(Cases == 2)
        {
        //ROC Price
        Indicator = Ref(ROC(Close,lb),-1);
        INDICATOR = IIf(ascdec == 1, indicator, -indicator);

        }

        if(Cases == 3)
        {
        //ROC Volume
        Indicator = Ref(ROC(Volume,lb),-1);
        INDICATOR = IIf(ascdec == 1, indicator, -indicator);

        }

        if(Cases == 4)
        {
        //CRSI
        Indicator = ConnorsRSI(paramLenRSI,paramLenUD,paramLenRank);
        INDICATOR = IIf(ascdec == 1, indicator, -indicator);

        }

        if(Cases == 5)
        {
        //Z Score
        mb = MA(C,lb+1);
        Indicator = Ref((C - mb) / (StDev(C,lb+1)),-1);
        INDICATOR = IIf(ascdec == 1, indicator, -indicator);

        }

        if(Cases == 6)
        {
        //LTI
        Ltilb = 10; 
        Indicator = Ref(ROC(EMA(Close,ltilb),lb) + ROC(EMA(Close,ltilb*2),lb) + ROC(EMA(Close,ltilb*3),lb),-1);
        INDICATOR = IIf(ascdec == 1, indicator, -indicator);

        }

        if(Cases == 7)
        {
        //RSI Price
        Indicator = Ref(RSIa(Close,14),-1);
        INDICATOR = IIf(ascdec == 1, indicator, -indicator);

        }

        if(Cases == 8)
        {
        //RSI Volume
        Indicator = Ref(RSIa(Volume,14),-1);
        INDICATOR = IIf(ascdec == 1, indicator, -indicator);

        }

        if(Cases == 9)
        {
        // ROC MA 
        Indicator = Ref(ROC(MA(Close,lb),lb),-1);
        INDICATOR = IIf(ascdec == 1, indicator, -indicator);

        }

        if(Cases == 10)
        {
        // ROC Price PR 
        Indicator = Ref(PercentRank(ROC(Close,lb),100),-1);
        INDICATOR = IIf(ascdec == 1, indicator, -indicator);

        }

        if(Cases == 11)
        {
        // PIR = Stoch K
        Indicator = Ref(StochK(14),-1);
        INDICATOR = IIf(ascdec == 1, indicator, -indicator);

        }

        if(Cases == 12)
        {
        // Stoch D
        Indicator = Ref(StochD(14,3,3),-1);
        INDICATOR = IIf(ascdec == 1, indicator, -indicator);

        }

        if(Cases == 13)
        {
        // ATR/C
        Indicator = Ref(ATR(vp)/Close,-1)*100;
        INDICATOR = IIf(ascdec == 1, indicator, -indicator);

        }

        if(Cases == 14)
        {
        // STDEV.P
        Indicator = Ref(StDev(ROC(Close,lb),100,True),-1);
        INDICATOR = IIf(ascdec == 1, indicator, -indicator);

        }

        if(Cases == 15)
        {
        // Beta
        Periods = Param("period",8,1,50,1);
        ticker = ParamStr( "Ticker", "$NIFTY-NSE" );
        P = Foreign(TICKER,"C",lb);
        Indicator = (( Periods * Sum(ROC( C,lb) * ROC(P,lb),Periods )) - (Sum(ROC(C,lb),Periods) * Sum(ROC( P,lb),Periods))) / ((Periods * Sum((ROC(P,lb)^2 ),Periods)) - (Sum(ROC(P,lb ),Periods)^2 ));
        INDICATOR = IIf(ascdec == 1, Indicator, -Indicator);

        }

        if(Cases == 16)
        {
        // ABS ROC
        Indicator = Ref(abs(ROC(Close,lb)),-1);
        INDICATOR = IIf(ascdec == 1, indicator, -indicator);

        }

        if(Cases == 17)
        {
        // PR ABS ROC
        Indicator = Ref(PercentRank(abs(ROC(Close,lb)),100),-1);
        INDICATOR = IIf(ascdec == 1, indicator, -indicator);

        }


        if(Cases == 18)
        {
        // Vol PIR
        Indicator = Ref((Volume - LLV(Volume,14)) / (HHV(Volume,14) - LLV(Volume,14)) ,-1)*100;
        INDICATOR = IIf(ascdec == 1, indicator, -indicator);

        }

        if(Cases == 19)
        {
        // Vol PR
        Indicator = Ref(PercentRank(Volume,100),-1); // check
        INDICATOR = IIf(ascdec == 1, indicator, -indicator);

        }

        if(Cases == 20)
        {
        // Close PR
        Indicator = Ref(PercentRank(Close,100),-1); // check
        INDICATOR = IIf(ascdec == 1, indicator, -indicator);

        }

        if(Cases == 21)
        {
        //Volume Z Score
        mb = MA(Volume,lb+1);
        Indicator = Ref((Volume - mb) / (StDev(Volume,lb+1)),-1);
        INDICATOR = IIf(ascdec == 1, indicator, -indicator);

        }

        if(Cases == 22)
        {
        //MACD
        r1 = Param( "Fast avg", 12, 2, 200, 1 );
        r2 = Param( "Slow avg", 26, 2, 200, 1 );
        r3 = Param( "Signal avg", 9, 2, 200, 1 );

        m1=MACD(r1,r2);
        s1=Signal(r1,r2,r3); 
        //a=Cross(m1,s1);

        Indicator = Ref(PercentRank(s1,100),-1); 
        INDICATOR = IIf(ascdec == 1, indicator, -indicator);

        }

        if(Cases == 23)
        {
        //MFI - Similar to RSI but consideres Volume and Price
        Indicator = Ref(MFI(lb),-1);
        INDICATOR = IIf(ascdec == 1, indicator, -indicator);

        }

        if(Cases == 24)
        {
        // MA ATR/C
        Indicator = Ref(MA(ATR(vp)/Close,lb),-1)*100; 
        INDICATOR = IIf(ascdec == 1, indicator, -indicator);

        }

            values = IIf( includeok , Indicator , Null);

        RestorePriceArrays();
        StaticVarSet (  "values"  +  symbol, values );


        _TRACE( symbol );
         }

      StaticVarGenerateRanks( "rank", "values", 0, 1234 );

    }


    symbol = Name();
    values = StaticVarGet ( "values" +  symbol );
    rank = StaticVarGet ( "rankvalues" +  symbol );



    poi = Ref(Close,-1);
    edist = Ref(ATR(vp),-1)*ef;


    strig = poi + edist;
    strade = H >= strig;



    //fdw = DayOfWeek() < Ref(DayOfWeek(),-1);

    Short = rank >= minrank AND Rank <= maxrank AND includeok /*AND Fdw !=1 */AND Strade ;
    ShortPrice = IIf(Max(Open,strig) == Open,Open,strig);

    /*
    pt = 3;//Optimize("pt",2,2,6,1);;
    slpts = Ref(Close,-1)*pt/100;
    stprc = Ref(Close,-1)+ slpts;
    */
    //PositionScore = Random(); 

    sp = 6;
    atrstp = Ref(ATR(1),-1)*sp/10;
    stopprice = ShortPrice+atrstp;

    Cover = Short;
    CoverPrice = IIf(H >= stopprice, stopprice, Close);


    //ApplyStop(stopTypeLoss,stopModePercent,pt);

    Filter = includeok;
    AddColumn(Rank,"Rank");
    AddColumn(Values,"Values");
    AddColumn(Close,"Close");
    AddColumn(indicator,"indicator");
    AddColumn((Close/Open-1)*100,"Price Change");
