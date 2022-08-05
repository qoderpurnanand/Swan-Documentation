    SetCustomBacktestProc("");

    if( Status( "action" ) == actionPortfolio )
    {
        bo = GetBacktesterObject(); //  Get backtester object
        bo.PreProcess(); //  Do pre-processing (always required)
        newday = Day() != Ref(Day(),-1);
        count = 0;

        for( i = 0; i < BarCount; i++ ) //  Loop through all bars
        {
            if(newday[i]==1)
            {
    count=0;

            }

            for( sig = bo.GetFirstSignal( i ); sig; sig = bo.GetNextSignal( i ) )
            {
                if( sig.IsEntry())
                {
                    if( count< 15 )
                        count ++;
                    else
                        sig.Price = -1 ; // ignore entry signal
                }
            }

            bo.ProcessTradeSignals( i ); //  Process trades at bar (always required)
        }

        bo.PostProcess(); //  Do post-processing (always required)


    /*
    bo.Backtest();
    AddToComposite( bo.EquityArray,
    "~~~SIDEQUITY"+ef, "X",
    atcFlagDeleteValues | atcFlagEnableInPortfolio );
     */   
    }
