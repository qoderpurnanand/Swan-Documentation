## QGF_Aug_2021

    //#include <FutIncludeok.afl>

    SetOption("InitialEquity",1000000);
    SetOption("Maxopenpositions",30);
    SetPositionSize(100/30,spsPercentOfEquity);

    Mcaplow = 500;
    Mcaphigh = 20000; 

    List = CategoryGetSymbols(categoryWatchlist, 0);

    if(Status("StockNum") == 0)
    {
      StaticVarRemove("values*");

      for(i = 0; (symbol = StrExtract(List, i)) != ""; i++)
      {
        SetForeign(symbol);


        //#include <FutIncludeok.afl>
        values = IIf(Aux2 >=Mcaplow AND Aux2 <=Mcaphigh and aux2!=0 /*AND includeok*/,Aux1,Null);

        RestorePriceArrays();

        StaticVarSet("values" + symbol, values);

      }

      StaticVarGenerateRanks("rank", "values", 0, 1234);

    }

    symbol = Name();
    values = StaticVarGet("values" + symbol);

    rank = StaticVarGet("rankvalues" + symbol);


    Buy = rank <= 30 AND rank >=1 AND Month()==7 AND Month()!=Ref(Month(),-1) AND Name()!="AVANTIFEED.EQ-NSE" and aux2>mcaplow /*AND includeok==1*/;
    Sell = rank >30 AND Month()==7 AND Month()!=Ref(Month(),-1);

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


    Filter =1;
    AddColumn(rank,"rank");
    AddColumn(aux1,"aux1");
    AddColumn(Aux2,"Aux2");
    AddColumn(Open,"Open");
    AddColumn(High,"High");
    AddColumn(Low,"Low");
    AddColumn(Close,"Close");
    AddColumn(Volume,"Volume");
