## MMR Ranking Code to create Composite Symbols

    #include <Includeok.afl>

    bi = BarIndex();
    exitLastBar = bi == LastValue( bi );
    maxpos = 10;

    afl = "MMRRanking";

    SetOption("InitialEquity",10000000);
    SetOption("AccountMargin",100);
    SetOption("MaxOpenPositions",maxpos);
    SetTradeDelays(0,0,0,0);
    SetPositionSize(maxpos/100,spsPercentOfEquity);

    vp = 5;
    llb = 10;
    EMALLB = 10;

    maxrank = 30;

    watchlist = 0;

    List = CategoryGetSymbols(categoryWatchlist,watchlist);

    if ( Status("stocknum") == 0 ) // Generate ranking when we are on the very first symbol
    {
      StaticVarRemove("values*" );

      for ( n = 0; ( Sym = StrExtract( List, n ) )  != "";  n++    )
      {
        SetForeign ( Sym );

        //excludeok = 0;
        #include <Includeok.afl>
        llb = 10;
        EMALLB = 10;
        lti = Ref(ROC(EMA(Close,EMALLB),llb),-1) + Ref(ROC(EMA(Close,EMALLB+10),llb),-1) + Ref(ROC(EMA(Close,EMALLB+20),llb),-1);
        values =  IIf(includeok , lti, Null);
        RestorePriceArrays();

        StaticVarSet ("values"  +  Sym, values );

        _TRACE( Sym );
        }

      StaticVarGenerateRanks( "rank", "values", 0, 1234 );
    }

    Sym = Name();
    values = StaticVarGet ("values" +  Sym );
    rank = StaticVarGet ( "rankvalues" +  Sym );

    lti = Ref(ROC(EMA(Close,EMALLB),llb),-1) + Ref(ROC(EMA(Close,EMALLB+10),llb),-1) + Ref(ROC(EMA(Close,EMALLB+20),llb),-1);

    AddToComposite(rank,"~~MMRRank" + name(),"X") ;




    Filter = 1;
    AddColumn(C,"Close");
    AddColumn(rank,"Rank");
    AddColumn(values,"Values");
    AddColumn(LTI,"LTI"); 
