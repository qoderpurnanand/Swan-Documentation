## SHORT FLAT AVERAGE RANKING
    #include <Includeok.afl>
    #include <Banlist.afl>
    afl = "ShortflatAvgranking";
    maxpos = 10;//Optimize("maxpos",10,10,15,1);
    Worstrank = maxpos+5;//Optimize("Worstrank",5,1,5,1);
    SetOption("InitialEquity",1000000);
    SetOption("Maxopenpositions",maxpos);
    SetPositionSize(100/maxpos,spsPercentOfEquity);

    weightcase = 1;//Optimize("Weightcase",1,1,2,1);
    if(weightcase == 1){x1 = 1; x2 = x3 = x4 = 0;}
    if(weightcase == 2){x1 = x2 = 1/2; x3 = x4 = 0;}
    if(weightcase == 3){x1 = x2 = x3 = 1/3; x4 = 0;}
    if(weightcase == 4){x1 = x2 = x3 = x4 = 1/4;}
    if(weightcase == 5){x1 = x4 = 1/2; x2 = x3 = 0;}
    if(weightcase == 6){x2 = x4 = 1/2; x1 = x3 = 0;}


    sma = 10;//Optimize("Sma",40,10,80,20);
    Slb = sma;//Optimize("Slb",40,10,80,20);
    emallb = 220;//Optimize("Slb",40,180,240,20);
    lb = 40;//Optimize("lb",40,100,200,20);
    vp = 5;
    Nifty = Foreign("$NIFTY_50-NSE","Close");

    sniftyma = MA(Nifty,sma);

    sti = (ROC(EMA(Close,emallb),Slb) + ROC(EMA(Close,emallb+20),slb) + ROC(EMA(Close,emallb+40),slb));
    ROCPrice = ROC(Close,lb);
    ROCMA = ROC(MA(Close,emallb),lb);
    MAATRC = MA(ATR(vp)/Close,emallb)*100; 
    Deliveryvol = Ref(ROC(MA(Aux1,emallb),lb),-1);

    Watchlist = 3;
    List = CategoryGetSymbols(categoryWatchlist,watchlist);

    if ( Status("stocknum") == 0 ) // Generate ranking when we are on the very first symbol
    {


    StaticVarRemove(afl +  "values*" );

    for ( n = 0; ( Sym = StrExtract( List, n ) )  != "";  n++    )
    {

    SetForeign ( sym );

        #include <Includeok.afl>
        #include <Banlist.afl>

        sti = (ROC(EMA(Close,emallb),Slb) + ROC(EMA(Close,emallb+20),slb) + ROC(EMA(Close,emallb+40),slb));
        ROCPrice = ROC(Close,lb);
        ROCMA = ROC(MA(Close,emallb),lb);
        MAATRC = MA(ATR(vp)/Close,lb)*100; 
        Deliveryvol = Ref(ROC(MA(Aux1,emallb),lb),-1);

        values1 = IIf(includeok AND excludeok == 0 AND sti < 0,-sti,Null);	
              values2 = IIf(includeok AND excludeok == 0 AND Deliveryvol < 0, -Deliveryvol, Null);
        values3 = IIf(includeok AND excludeok == 0 AND ROCMA < 0, -ROCMA, Null);
        values4 = IIf(includeok AND excludeok == 0 AND MAATRC > 0, MAATRC, Null);

    RestorePriceArrays();
    StaticVarSet (afl + "values1"  +  sym, values1);
    StaticVarSet(afl + "values2" + sym, values2);
    StaticVarSet(afl + "values3" + sym, values3);
    StaticVarSet(afl + "values4" + sym, values4);



    _TRACE( sym );
        }

    StaticVarGenerateRanks( "rank", afl + "values1", 0, 1234 );
    StaticVarGenerateRanks( "rank",afl + "values2",0,1234);
    StaticVarGenerateRanks( "rank",afl + "values3",0,1234);
    StaticVarGenerateRanks( "rank",afl + "values4",0,1234);


    for ( n = 0; ( Sym = StrExtract( List, n ) )  != "";  n++    )
    {
    SetForeign ( sym );

    rank1 = StaticVarGet("rank" + afl + "values1" + sym);
    rank2 = StaticVarGet("rank" + afl + "values2" + sym);
    rank3 = StaticVarGet("rank" + afl + "values3" + sym);
    rank4 = StaticVarGet("rank" + afl + "values4" + sym);

    Avgrank = rank1*x1 + rank2*x2 + rank3*x3 + rank4*x4;

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


    Short = finalrank <= maxpos AND includeok AND excludeok == 0 AND nifty < sniftyma;
    Cover = finalrank > Worstrank OR includeok==0 OR nifty >= sniftyma;

    ShortPrice = Close;
    CoverPrice = Close;


    Filter = 1;
    AddColumn(finalrank,"Finalrank");
    SetSortColumns(3);
