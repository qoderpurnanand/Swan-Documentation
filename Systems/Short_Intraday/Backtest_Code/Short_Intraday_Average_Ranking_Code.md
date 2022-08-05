## SHORT INTRADAY AVERAGE RANKING CODE
    afl = "ShortAvgRanking2";
    maxpos = 15;

    #include <Includeok.afl>
    #include <Banlist.afl>

    x1 = x2 = x3 = x4 = x5 = x6 = x7 = x8 = x9 = 1/9;

    maxrank = maxpos;

    vp = 1;
    llb = 1;
    zslb = 5;

    //excludeok = 0; // add banlist include

    Volfilter = 1;

    paramLenRSI = 3;
    paramLenUD = 2;
    paramLenRank = 100;

    function ConnorsRSI(lenRSI, lenUD, lenROC)
    {
          upDays = BarsSince(C <= Ref(C,-1));
          downDays = BarsSince(C >= Ref(C,-1));
          updownDays = IIf(upDays > 0, upDays, IIf(downDays > 0, -downDays, 0));
          crsi = ( PercentRank(ROC(C,1), lenROC) + RSIa(updownDays,lenUD) +RSI(lenRSI))/3;

         return crsi;

    }


    watchlist = 1;

    List = CategoryGetSymbols(categoryWatchlist,watchlist);

    if ( Status("stocknum") == 0 ) // Generate ranking when we are on the very first symbol
    {


    StaticVarRemove( "values*" );

    for ( n = 0; ( Sym = StrExtract( List, n ) )  != "";  n++    )
    {

    SetForeign ( sym );

    #include <Includeok.afl>
    #include <Banlist.afl>

        ROCVol = Ref(ROC(Volume,llb),-1);
        crsi = Ref(ConnorsRSI(paramLenRSI,paramLenUD,paramLenRank),-1);

        ROCprice = ref(ROC(Close,llb),-1);
        rsiprice = ref(RSIa(Close,14),-1);

        //Volatility indicators
        atrpr = ref(PercentRank(ATR(vp),100),-1);
        mb = ref(MA(C,zslb+1),-1);
        Zscore = ref((C - mb) / (StDev(C,zslb+1)),-1);		
        atrc = ref((ATR(vp)/Close)*100,-1);

        // Volume Indicators
        ROCvol = ref(ROC(Volume,llb),-1);
        rsivol = ref(RSIa(Volume,14),-1);
        volpr = ref(PercentRank(Volume,100),-1);



        values1 = IIf(includeok AND Excludeok == 0 AND Volfilter AND sym != "$NIFTY-NSE", CRSI, Null);
        values2 = IIf(includeok AND Excludeok == 0 AND Volfilter AND sym != "$NIFTY-NSE", ROCprice , Null);
        values3 = IIf(includeok AND Excludeok == 0 AND Volfilter AND sym != "$NIFTY-NSE", rsiprice , Null);
        values4 = IIf(includeok AND Excludeok == 0 AND Volfilter AND sym != "$NIFTY-NSE", atrpr , Null);
        values5 = IIf(includeok AND Excludeok == 0 AND Volfilter AND sym != "$NIFTY-NSE", Zscore , Null);
        values6 = IIf(includeok AND Excludeok == 0 AND Volfilter AND sym != "$NIFTY-NSE", atrc , Null);
        values7 = IIf(includeok AND Excludeok == 0 AND Volfilter AND sym != "$NIFTY-NSE", ROCvol , Null);
        values8 = IIf(includeok AND Excludeok == 0 AND Volfilter AND sym != "$NIFTY-NSE", rsivol , Null);
        values9 = IIf(includeok AND Excludeok == 0 AND Volfilter AND sym != "$NIFTY-NSE", volpr , Null);

        RestorePriceArrays();

        StaticVarSet(afl+"values1"+Sym, values1);
        StaticVarSet(afl+"values2"+Sym, values2);
        StaticVarSet(afl+"values3"+Sym, values3);
        StaticVarSet(afl+"values4"+Sym, values4);
        StaticVarSet(afl+"values5"+Sym, values5);
        StaticVarSet(afl+"values6"+Sym, values6);
        StaticVarSet(afl+"values7"+Sym, values7);
        StaticVarSet(afl+"values8"+Sym, values8);
        StaticVarSet(afl+"values9"+Sym, values9);



    _TRACE( sym );
        }

      StaticVarGenerateRanks("rank",afl+"Values1",0,1234);
      StaticVarGenerateRanks("rank",afl+"Values2",0,1234);
      StaticVarGenerateRanks("rank",afl+"Values3",0,1234);
      StaticVarGenerateRanks("rank",afl+"Values4",0,1234);
      StaticVarGenerateRanks("rank",afl+"Values5",0,1234);
      StaticVarGenerateRanks("rank",afl+"Values6",0,1234);
      StaticVarGenerateRanks("rank",afl+"Values7",0,1234);
      StaticVarGenerateRanks("rank",afl+"Values8",0,1234);
      StaticVarGenerateRanks("rank",afl+"Values9",0,1234);


    }


    Sym = Name();


    values1 = StaticVarGet(afl+"values1" + Sym);
    values2 = StaticVarGet(afl+"values2" + Sym);
    values3 = StaticVarGet(afl+"values3" + Sym);
    values4 = StaticVarGet(afl+"values4" + Sym);
    values5 = StaticVarGet(afl+"values5" + Sym);
    values6 = StaticVarGet(afl+"values6" + Sym);
    values7 = StaticVarGet(afl+"values7" + Sym);
    values8 = StaticVarGet(afl+"values8" + Sym);
    values9 = StaticVarGet(afl+"values9" + Sym);

    v1 = StaticVarGet("rank" + afl + "values1" + Sym);
    v2 = StaticVarGet("rank" + afl + "values2" + Sym);
    v3 = StaticVarGet("rank" + afl + "values3" + Sym);
    v4 = StaticVarGet("rank" + afl + "values4" + Sym);
    v5 = StaticVarGet("rank" + afl + "values5" + Sym);
    v6 = StaticVarGet("rank" + afl + "values6" + Sym);
    v7 = StaticVarGet("rank" + afl + "values7" + Sym);
    v8 = StaticVarGet("rank" + afl + "values8" + Sym); 
    v9 = StaticVarGet("rank" + afl + "values9" + Sym); 


    if ( Status("stocknum") == 0 ) // Generate ranking when we are on the very first symbol
    {
      //StaticVarRemove( "values*" );

      for ( n = 0; ( Sym = StrExtract( List, n ) )  != "";  n++    )
      {
        SetForeign ( Sym );

        //Sym = Name();


        #include <Includeok.afl>
        //excludeok = 0;

        v1 = 10000 - StaticVarGet("rank" + afl + "values1"+Sym);
        v2 = 10000 - StaticVarGet("rank" + afl + "values2"+Sym);
        v3 = 10000 - StaticVarGet("rank" + afl + "values3"+Sym);
        v4 = 10000 - StaticVarGet("rank" + afl + "values4"+Sym);
        v5 = 10000 - StaticVarGet("rank" + afl + "values5"+Sym);
        v6 = 10000 - StaticVarGet("rank" + afl + "values6"+Sym);
        v7 = 10000 - StaticVarGet("rank" + afl + "values7"+Sym);
        v8 = 10000 - StaticVarGet("rank" + afl + "values8"+Sym);
        v9 = 10000 - StaticVarGet("rank" + afl + "values9"+Sym);

        AvgRank =  v1*X1 + v2*x2 + v3*x3 + v4*x4 + v5*x5 + v6*x6 + v7*x7 + v8*x8 + v9*x9 ;

        RestorePriceArrays();

        StaticVarSet(afl+"AvgRank"+Sym, AvgRank);
    _TRACE( sym );
        }

    StaticVarGenerateRanks( "rank", afl+"AvgRank", 0, 1234 );

      rank = StaticVarGet ( "rank" + afl + "AvgRank" +  Sym );


        StaticVarRemove(afl+"addrank");
        StaticVarRemove(afl+"valuecheck");

    }
    crsi = Ref(ConnorsRSI(paramLenRSI,paramLenUD,paramLenRank),-1);
    rocvol = Ref(ROC(Volume,llb),-1);


    sym = Name();
    AvgRank = StaticVarGet ( afl+"AvgRank" +  Sym );
    rank = StaticVarGet ( "rank" + afl + "AvgRank" +  Sym );


    rankOK = rank <= 20;

    //AddToComposite(rank,"~SIDLMT0.1FUT" + name(),"X",atcFlagResetValues);
    //AddToComposite(rank,"~SIDLMT0.1FUT" + name(),"X",atcFlagResetValues);

    //comprank = Foreign("~SIDLMT0.1FUT" + Name() ,"C");


    Filter = 1;
    AddColumn(rankOK,"rankOK");
    AddColumn(AvgRank,"Finalrank");
    AddColumn(rank,"rank");
    SetSortColumns(3);
