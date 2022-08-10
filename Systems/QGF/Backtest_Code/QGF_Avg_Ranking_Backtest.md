## QGF_Avg_Ranking_Backtest

    afl = "QGFAvgRanking";
    maxpos = 30;
    SetOption("InitialEquity",1000000);
    SetOption("Maxopenpositions",maxpos);
    SetPositionSize(100/maxpos,spsPercentOfEquity);


    watchlist = 0;

    Mcaplow = 500;
    Mcaphigh = 20000; 
    x = 1/2;

    pricelb = Optimize("ROCPrice",60,20,200,20);

    List = CategoryGetSymbols(categoryWatchlist,watchlist);

    if ( Status("stocknum") == 0 ) // Generate ranking when we are on the very first symbol
    {


    StaticVarRemove(afl +  "values*" );
    StaticVarRemove(afl + "volumerank*");

    for ( n = 0; ( Sym = StrExtract( List, n ) )  != "";  n++    )
    {

    SetForeign ( sym );

        ROCPrice = Ref(ROC(Close,pricelb),-1);
        ROCVolume = Ref(ROC(Volume,pricelb),-1);

        values1 = IIf(Aux2 >=Mcaplow AND Aux2 <=Mcaphigh and aux2!=0 and C >10/*AND includeok*/,Aux1,Null);	
            values2 = IIf(/*ROCprice > 0 AND */Aux1 != 0 AND Aux2 >=Mcaplow AND Aux2 <=Mcaphigh and C >10, ROCPrice, Null);
        values3 = IIf(/*ROCprice > 0 AND */Aux1 != 0 AND Aux2 >=Mcaplow AND Aux2 <=Mcaphigh and C >10, ROCVolume, Null);

    RestorePriceArrays();
    StaticVarSet ( afl + "values1"  +  sym, values1 );
    StaticVarSet(afl + "values2" + sym, values2);
    StaticVarSet(afl + "values3" + sym, values3);

    //StaticVarSet ( afl + "Volfilter"  +  sym, volfilter );


    _TRACE( sym );
        }

    StaticVarGenerateRanks( "rank", afl + "values1", 0, 1234 );
    StaticVarGenerateRanks( "rank",afl + "values2",0,1234);
    StaticVarGenerateRanks( "rank",afl + "values3",0,1234);


    for ( n = 0; ( Sym = StrExtract( List, n ) )  != "";  n++    )
    {
    SetForeign ( sym );

    rank1 = StaticVarGet("rank" + afl + "values1" + sym);
    rank2 = StaticVarGet("rank" + afl + "values2" + sym);
    rank3 = StaticVarGet("rank" + afl + "values3" + sym);

    Avgrank = rank1*x + rank2*x /*+ rank3*x*/;

    RestorePriceArrays();
    StaticVarSet ( afl + "Avgrank"  +  sym , -Avgrank);
    _TRACE( sym );
        }

    StaticVarGenerateRanks( "rank",afl + "Avgrank", 0, 1234 );

    }


    sym = Name();
    values1 =  StaticVarGet(afl + "values1"  +  sym);
    values2 = StaticVarGet(afl + "values2"  +  sym);
    rank1 = StaticVarGet("rank" + afl + "values1"+sym);
    rank2 = StaticVarGet("rank" + afl + "values2"+sym);
    avgrank = StaticVarGet(afl + "avgrank"+sym);
    finalrank = StaticVarGet("rank" + afl + "Avgrank"+sym);


    Buy = finalrank >0 AND finalrank <= 30 AND Month()==7 AND Month()!=Ref(Month(),-1) AND Name()!="AVANTIFEED.EQ-NSE" and aux2>mcaplow /*AND includeok==1*/;
    Sell = finalrank >30 AND Month()==7 AND Month()!=Ref(Month(),-1) OR Aux2 < mcaplow;


    BuyPrice = Close;
    SellPrice = Close;

    ROCPrice = Ref(ROC(Close,60),-1);

    Filter = 1;
    AddColumn(finalrank,"Finalrank");
    AddColumn(values1,"values1");
    AddColumn(ROCprice,"ROCPRice");
    AddColumn(Aux2,"Aux2");
    AddColumn(Aux2 > mcaplow,"mcapcheck");
    SetSortColumns(3);

