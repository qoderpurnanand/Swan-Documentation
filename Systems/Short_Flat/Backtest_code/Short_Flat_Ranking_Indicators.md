    #include <Includeok.afl>
    #include <Banlist.afl>

    maxpos = 10;
    Worstrank = maxpos+5;
    SetOption("InitialEquity",1000000);
    SetOption("Maxopenpositions",maxpos);
    SetPositionSize(100/maxpos,spsPercentOfEquity);


    sma = Optimize("lb",100,10,200,20);
    //Slb = 10;//Optimize("Slb",40,10,100,10);
    //emallb = Optimize("lb",100,10,200,20);

    Nifty = Foreign("$NIFTY_50-NSE","Close");

    sniftyma = MA(Nifty,sma);

    //sti = (ROC(EMA(Close,emallb),Slb) + ROC(EMA(Close,emallb+20),slb) + ROC(EMA(Close,emallb+40),slb));
    Cases = 4;//Optimize("Cases",2,1,24,1);
    lb = Optimize("lb",100,10,200,20);
    vp = 5;

    paramLenRSI = lb; //Param("RSI Closes Length", crsilb, crsilb, 100, 1);
    paramLenUD = lb; //Param("RSI UpClose Length", 2, 2, 100, 1); // ask
    paramLenRank = 100; //Param("PerecentRank Length", 100, 10, 200, 1); // ask

    function ConnorsRSI(lenRSI, lenUD, lenROC)
    {
          upDays = BarsSince(C <= Ref(C,-1));
          downDays = BarsSince(C >= Ref(C,-1));
          updownDays = IIf(upDays > 0, upDays, IIf(downDays > 0, -downDays, 0));
          crsi = ( PercentRank(ROC(C,lb), lenROC) + RSIa(updownDays,lenUD) +RSI(lenRSI))/3;

         return crsi;

    }


    ASCDEC = 2;//Optimize("ASCDEC",1,1,2,1);
    Rankcase = 1;//Optimize("Rankcase",1,1,11,1);
    rn = 10;

    //minrank = IIf(rankcase == 1,1,IIf(rankcase == 2,rn, IIf(rankcase == 3,rn*2,IIf(rankcase == 4,rn*3,IIf(rankcase == 5,rn*4,IIf(rankcase == 6,rn*5,IIf(rankcase == 7,rn*6,IIf(rankcase == 8,rn*7,IIf(rankcase == 9,rn*8,IIf(rankcase == 10,rn*9, IIf(rankcase == 11,rn*10,null)))))))))));
    //maxrank = IIf(rankcase == 1,rn,IIf(rankcase == 2,rn*2, IIf(rankcase == 3,rn*3,IIf(rankcase == 4,rn*4,IIf(rankcase == 5,rn*5,IIf(rankcase == 6,rn*6,IIf(rankcase == 7,rn*7,IIf(rankcase == 8,rn*8,IIf(rankcase == 9,rn*9,IIf(rankcase == 10,rn*10, IIf(rankcase == 11,rn*11,null)))))))))));

    /*
    minrank = IIf(ascdec == 1, 1, 343);
    Maxrank = IIf(ascdec == 1, 50, 393);
    */

    if(Cases == 1)
    {
    //ATRPR
    Indicator = PercentRank(ATR(vp),100);
    INDICATOR = IIf(ascdec == 1, indicator, -indicator);

    }

    if(Cases == 2)
    {
    //ROC Price
    Indicator = ROC(Close,lb);
    INDICATOR = IIf(ascdec == 1, indicator, -indicator);

    }

    if(Cases == 3)
    {
    //ROC Volume
    Indicator = ROC(Volume,lb);
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
    Indicator = (C - mb) / (StDev(C,lb+1));
    INDICATOR = IIf(ascdec == 1, indicator, -indicator);

    }

    if(Cases == 6)
    {
    //STI
    emallb = 200; // check
    Indicator = (ROC(EMA(Close,emallb),lb) + ROC(EMA(Close,emallb+20),lb) + ROC(EMA(Close,emallb+40),lb));
    INDICATOR = IIf(ascdec == 1, indicator, -indicator);

    }

    if(Cases == 7)
    {
    //RSI Price
    Indicator = RSIa(Close,14);
    INDICATOR = IIf(ascdec == 1, indicator, -indicator);

    }

    if(Cases == 8)
    {
    //RSI Volume
    Indicator = RSIa(Volume,14);
    INDICATOR = IIf(ascdec == 1, indicator, -indicator);

    }

    if(Cases == 9)
    {
    // ROC MA 
    Indicator = ROC(MA(Close,lb),lb);
    INDICATOR = IIf(ascdec == 1, indicator, -indicator);

    }

    if(Cases == 10)
    {
    // ROC Price PR 
    Indicator = PercentRank(ROC(Close,lb),100);
    INDICATOR = IIf(ascdec == 1, indicator, -indicator);

    }

    if(Cases == 11)
    {
    // PIR = Stoch K
    Indicator = StochK(14);
    INDICATOR = IIf(ascdec == 1, indicator, -indicator);

    }

    if(Cases == 12)
    {
    // Stoch D
    Indicator = StochD(14,3,3);
    INDICATOR = IIf(ascdec == 1, indicator, -indicator);

    }

    if(Cases == 13)
    {
    // ATR/C
    Indicator = ATR(vp)/Close*100;
    INDICATOR = IIf(ascdec == 1, indicator, -indicator);

    }

    if(Cases == 14)
    {
    // STDEV.P
    Indicator = StDev(ROC(Close,lb),100,True);
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
    Indicator = abs(ROC(Close,lb));
    INDICATOR = IIf(ascdec == 1, indicator, -indicator);

    }

    if(Cases == 17)
    {
    // PR ABS ROC
    Indicator = PercentRank(abs(ROC(Close,lb)),100);
    INDICATOR = IIf(ascdec == 1, indicator, -indicator);

    }


    if(Cases == 18)
    {
    // Vol PIR
    Indicator = (Volume - LLV(Volume,14)) / (HHV(Volume,14) - LLV(Volume,14))*100;
    INDICATOR = IIf(ascdec == 1, indicator, -indicator);

    }

    if(Cases == 19)
    {
    // Vol PR
    Indicator = PercentRank(Volume,100); 
    INDICATOR = IIf(ascdec == 1, indicator, -indicator);

    }

    if(Cases == 20)
    {
    // Close PR
    Indicator = PercentRank(Close,100); 
    INDICATOR = IIf(ascdec == 1, indicator, -indicator);

    }

    if(Cases == 21)
    {
    //Volume Z Score
    mb = MA(Volume,lb+1);
    Indicator = (Volume - mb) / (StDev(Volume,lb+1));
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

    Indicator = PercentRank(s1,100); 
    INDICATOR = IIf(ascdec == 1, indicator, -indicator);

    }

    if(Cases == 23)
    {
    //MFI - Similar to RSI but consideres Volume and Price
    Indicator = MFI(lb);
    INDICATOR = IIf(ascdec == 1, indicator, -indicator);

    }

    if(Cases == 24)
    {
    // MA ATR/C
    Indicator = MA(ATR(vp)/Close,lb)*100; 
    INDICATOR = IIf(ascdec == 1, indicator, -indicator);

    }


    List = CategoryGetSymbols(categoryWatchlist, 3);

    if(Status("StockNum") == 0)
    {
      StaticVarRemove("values*");

      for(i = 0; (symbol = StrExtract(List, i)) != ""; i++)
      {
        SetForeign(symbol);

        #include <Includeok.afl>
        #include <Banlist.afl>



          if(Cases == 1)
          {
          //ATRPR
          Indicator = PercentRank(ATR(vp),100);
          INDICATOR = IIf(ascdec == 1, indicator, -indicator);

          }

          if(Cases == 2)
          {
          //ROC Price
          Indicator = ROC(Close,lb);
          INDICATOR = IIf(ascdec == 1, indicator, -indicator);

          }

          if(Cases == 3)
          {
          //ROC Volume
          Indicator = ROC(Volume,lb);
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
          Indicator = (C - mb) / (StDev(C,lb+1));
          INDICATOR = IIf(ascdec == 1, indicator, -indicator);

          }

          if(Cases == 6)
          {
          //STI
          emallb = 200; // check
          Indicator = (ROC(EMA(Close,emallb),lb) + ROC(EMA(Close,emallb+20),lb) + ROC(EMA(Close,emallb+40),lb));
          INDICATOR = IIf(ascdec == 1, indicator, -indicator);

          }

          if(Cases == 7)
          {
          //RSI Price
          Indicator = RSIa(Close,14);
          INDICATOR = IIf(ascdec == 1, indicator, -indicator);

          }

          if(Cases == 8)
          {
          //RSI Volume
          Indicator = RSIa(Volume,14);
          INDICATOR = IIf(ascdec == 1, indicator, -indicator);

          }

          if(Cases == 9)
          {
          // ROC MA 
          Indicator = ROC(MA(Close,lb),lb);
          INDICATOR = IIf(ascdec == 1, indicator, -indicator);

          }

          if(Cases == 10)
          {
          // ROC Price PR 
          Indicator = PercentRank(ROC(Close,lb),100);
          INDICATOR = IIf(ascdec == 1, indicator, -indicator);

          }

          if(Cases == 11)
          {
          // PIR = Stoch K
          Indicator = StochK(14);
          INDICATOR = IIf(ascdec == 1, indicator, -indicator);

          }

          if(Cases == 12)
          {
          // Stoch D
          Indicator = StochD(14,3,3);
          INDICATOR = IIf(ascdec == 1, indicator, -indicator);

          }

          if(Cases == 13)
          {
          // ATR/C
          Indicator = ATR(vp)/Close*100;
          INDICATOR = IIf(ascdec == 1, indicator, -indicator);

          }

          if(Cases == 14)
          {
          // STDEV.P
          Indicator = StDev(ROC(Close,lb),100,True);
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
          Indicator = abs(ROC(Close,lb));
          INDICATOR = IIf(ascdec == 1, indicator, -indicator);

          }

          if(Cases == 17)
          {
          // PR ABS ROC
          Indicator = PercentRank(abs(ROC(Close,lb)),100);
          INDICATOR = IIf(ascdec == 1, indicator, -indicator);

          }


          if(Cases == 18)
          {
          // Vol PIR
          Indicator = (Volume - LLV(Volume,14)) / (HHV(Volume,14) - LLV(Volume,14))*100;
          INDICATOR = IIf(ascdec == 1, indicator, -indicator);

          }

          if(Cases == 19)
          {
          // Vol PR
          Indicator = PercentRank(Volume,100); 
          INDICATOR = IIf(ascdec == 1, indicator, -indicator);

          }

          if(Cases == 20)
          {
          // Close PR
          Indicator = PercentRank(Close,100); 
          INDICATOR = IIf(ascdec == 1, indicator, -indicator);

          }

          if(Cases == 21)
          {
          //Volume Z Score
          mb = MA(Volume,lb+1);
          Indicator = (Volume - mb) / (StDev(Volume,lb+1));
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

          Indicator = PercentRank(s1,100); 
          INDICATOR = IIf(ascdec == 1, indicator, -indicator);

          }

          if(Cases == 23)
          {
          //MFI - Similar to RSI but consideres Volume and Price
          Indicator = MFI(lb);
          INDICATOR = IIf(ascdec == 1, indicator, -indicator);

          }

          if(Cases == 24)
          {
          // MA ATR/C
          Indicator = MA(ATR(vp)/Close,lb)*100; 
          INDICATOR = IIf(ascdec == 1, indicator, -indicator);

          }

        //sti = (ROC(EMA(Close,emallb),Slb) + ROC(EMA(Close,emallb+20),slb) + ROC(EMA(Close,emallb+40),slb));

        //values = IIf(Includeok AND sti<0 AND excludeok==0,1000-sti,Null);
        values = IIf(Includeok AND excludeok==0,INDICATOR,Null);

        RestorePriceArrays();

        StaticVarSet("values" + symbol, values);

      }

      StaticVarGenerateRanks("rank", "values", 0, 1234);

    }

    symbol = Name();
    values = StaticVarGet("values" + symbol);

    rank = StaticVarGet("rankvalues" + symbol);

    Short = rank <= Maxpos AND includeok AND nifty < sniftyma;
    Cover = rank > Worstrank OR includeok==0 OR nifty >= sniftyma;

    //sti = (ROC(EMA(Close,emallb),Slb) + ROC(EMA(Close,emallb+20),slb) + ROC(EMA(Close,emallb+40),slb));

    //AddToComposite(rank,"~Shortflat"+Name(),"X");


    Shortprice = Close;
    Coverprice = Close;

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


    Filter =1;
    AddColumn(rank,"rank");
    AddColumn(values,"values");
    AddColumn(Indicator,"indicator");








