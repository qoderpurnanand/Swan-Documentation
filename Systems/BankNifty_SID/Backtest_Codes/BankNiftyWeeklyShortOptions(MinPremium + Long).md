## BankNiftyWeeklyShortOptions(MinPremium + Long)

    _SECTION_BEGIN("Price");   
    SetChartOptions(0,chartShowArrows|chartShowDates);   
    _N(Title = StrFormat("{{NAME}} - {{INTERVAL}} {{DATE}} Open %g, Hi %g, Lo %g, Close %g (%.1f%%) Vol " +WriteVal( V, 1.0 ) +" {{VALUES}}", O, H, L, C, SelectedValue( ROC( C, 1 )) ));   
    Plot( C, "Close", ParamColor("Color", colorDefault ), styleNoTitle | ParamStyle("Style") | GetPriceStyle() );    

    SetOption("InitialEquity",10000000);    
    SetOption("AccountMargin",100);   
    MaxPos = 4;    
    SetOption("MaxOpenPositions",MaxPos);    
    SetTradeDelays(0,0,0,0);    
    SetOption("DisableRuinStop",True); 

    TimeFrameSet(inDaily);
    #include <ExpiryDates.afl>  
    OptionExpiryDate = DateTimeConvert(2,WeeklyExpiryDate);
    StartDate = DateTimeConvert(2,DateNum());
    DTE = round(DateTimeDiff(OptionExpiryDate,StartDate)/(3600*24));
    TimeFrameRestore();

    DaysToExpiry = TimeFrameExpand(DTE,inDaily,expandFirst);

    Moneyness = 1000;

    BankNiftyClose = Foreign("$BANKNIFTY-NSE", "C");

    ATM = (round(BankNiftyClose/100)*100);

    POE = IIf(DaysToExpiry == 0 OR DaysToExpiry == 1,5,3);   

    LotSize = IIf(Datenum()>=1110101 AND DateNum()<=1151029, 25 , IIf( DateNum()>=1151030 AND DateNum()<=1160630 , 30, IIf( DateNum()>=1160701 AND DateNum()<=1181025 , 40 , IIf( DateNum()>=1181026 AND DateNum()<=1200730 , 20 , 25)))) ;     

    ExposureMargin = Foreign("$BANKNIFTY-NSE", "C" )*2*0.02*LotSize;   
    SpanMargin = Moneyness*LotSize;   
    TotalMargin = ExposureMargin + SpanMargin;   
    MISLeverage = IIf(DaysToExpiry == 0 OR DaysToExpiry == 1,25,12);//(ExposureMargin/(TotalMargin*0.02)); 
    Deposit = ((Foreign("$BANKNIFTY-NSE", "C" )*LotSize*2)/MISLeverage);    
    MinPremium = (Deposit*(POE/100))/LotSize;    

    if(Status("stocknum")==0)
    {

      List = CategoryGetSymbols(categoryWatchlist,1);

      StaticVarRemove("CallPremiumDifference*");

      for(i = 0; (sym = StrExtract(List,i)) != ""; i++)
      {
        SetForeign(sym);
        LotSize = IIf(Datenum()>=1110101 AND DateNum()<=1151029, 25 , IIf( DateNum()>=1151030 AND DateNum()<=1160630 , 30, IIf( DateNum()>=1160701 AND DateNum()<=1181025 , 40 , IIf( DateNum()>=1181026 AND DateNum()<=1200730 , 20 , 25)))) ;     

        MISLeverage = 12; 
        Deposit = ((Foreign("$BANKNIFTY-NSE", "C" )*LotSize*2)/MISLeverage);    
        MinPremium = (Deposit*(POE/100))/LotSize;    

        StrikePrice = StrToNum(StrLeft(StrRight(Name(),7),5));
        Type = StrRight(Name(),2);
        CPremiumDifference = IIf(Type == "CE" AND StrikePrice >= round(Foreign("$BANKNIFTY-NSE", "C" )/100)*100,(100000 - abs(Close - MinPremium)),0);
        RestorePriceArrays();

        StaticVarSet("CallPremiumDifference" + sym,CPremiumDifference);

      }

        StaticVarGenerateRanks("CallRank","CallPremiumDifference",0,1224);

    }

    if(Status("stocknum")==0)
    {

      List = CategoryGetSymbols(categoryWatchlist,1);

      StaticVarRemove("PutPremiumDifference*");

      for(i = 0; (sym = StrExtract(List,i)) != ""; i++)
      {
        SetForeign(sym);
        LotSize = IIf(Datenum()>=1110101 AND DateNum()<=1151029, 25 , IIf( DateNum()>=1151030 AND DateNum()<=1160630 , 30, IIf( DateNum()>=1160701 AND DateNum()<=1181025 , 40 , IIf( DateNum()>=1181026 AND DateNum()<=1200730 , 20 , 25)))) ;     

        MISLeverage = 12;
        Deposit = ((Foreign("$BANKNIFTY-NSE", "C" )*LotSize*2)/MISLeverage);    
        MinPremium = (Deposit*(POE/100))/LotSize;    

        StrikePrice = StrToNum(StrLeft(StrRight(Name(),7),5));
        Type = StrRight(Name(),2);
        PPremiumDifference = IIf(Type == "PE" AND StrikePrice <= round(Foreign("$BANKNIFTY-NSE", "C" )/100)*100,(100000 - abs(Close - MinPremium)),0);
        RestorePriceArrays();

        StaticVarSet("PutPremiumDifference" + sym,PPremiumDifference);

      }

        StaticVarGenerateRanks("PutRank","PutPremiumDifference",0,1224);

    }

    CallRank = staticvarget("CallRankCallPremiumDifference" +  Name());
    PutRank = staticvarget("PutRankPutPremiumDifference" +  Name());

    if(Status("stocknum")==0)
    {
        List = CategoryGetSymbols(categoryWatchlist,1);
      StaticVarRemove("LongCallStrike*");


      for( i = 0; ( sym = StrExtract( List, i ) )  != "";  i++ )
      {
            SetForeign(sym);
            StrikePrice = StrToNum(StrLeft(StrRight(Name(),7),5));
            rank = staticvarget("CallRankCallPremiumDifference" +  Name());
            LongCallStrike = IIf(rank == 1,StrikePrice,0);

            StaticVarAdd("LongCallStrike",LongCallStrike,False);

            RestorePriceArrays();
      }


    }

    if(Status("stocknum")==0)
    {
        List = CategoryGetSymbols(categoryWatchlist,1);
      StaticVarRemove("LongPutStrike*");

        for( i = 0; ( sym = StrExtract( List, i ) )  != "";  i++ )
      {
            SetForeign(sym);
            StrikePrice = StrToNum(StrLeft(StrRight(Name(),7),5));
            rank = staticvarget("PutRankPutPremiumDifference" +  Name());
            LongPutStrike = IIf(rank == 1,StrikePrice,0);

            StaticVarAdd("LongPutStrike",LongPutStrike,False);

            RestorePriceArrays();
      }


    }

    LongCallStrike = StaticVarGet("LongCallStrike");
    LongPutStrike = StaticVarGet("LongPutStrike");

    StrikePrice = StrToNum(StrLeft(StrRight(Name(),7),5));
    Type = StrRight(Name(),2);

    bi = BarIndex();      
    exitlastbar = bi == LastValue(bi - 1);      

    DiwaliDates = DateNum()!=1111026 AND DateNum()!=1121113 AND DateNum()!=1131103 AND DateNum()!=1141023 AND DateNum()!=1151111 AND DateNum()!=1161030 AND DateNum()!=1171019 AND DateNum()!=1181107 AND DateNum()!=1191027 AND DateNum()!=1201114 AND Datenum()!=1211104;   

    ShortCallStrike = IIf(CallRank == 1,StrikePrice,0);
    ShortPutStrike = IIf(PutRank == 1,StrikePrice,0);

    CallStrike = IIf(StrikePrice == ShortCallStrike AND Type == "CE", 1 , 0);
    PutStrike = IIf(StrikePrice == ShortPutStrike AND Type == "PE", 1 , 0);

    StrikePriceSelector = CallStrike OR PutStrike;

    Move = Optimize("Move",5,5,10,2.5)/100;

    CallMoneyness = round(LongCallStrike*Move/100)*100;
    PutMoneyness = round(LongPutStrike*Move/100)*100;

    LongCallStrike = LongCallStrike + CallMoneyness;
    LongPutStrike = LongPutStrike - PutMoneyness;

    LongCallStrike = IIf(StrikePrice == LongCallStrike AND Type == "CE", 1 , 0);
    LongPutStrike = IIf(StrikePrice == LongPutStrike AND Type == "PE", 1 , 0);

    LongStrikePriceSelector = LongCallStrike OR LongPutStrike;

    CallSymbol = StrLeft(Name(),19) + StrikePrice + "CE";   
    PutSymbol = StrLeft(Name(),19) + StrikePrice + "PE";   

    CallPremium = IIf(Type=="CE",Foreign(CallSymbol,"Close"),Null);  
    PutPremium = IIf(Type=="PE",Foreign(PutSymbol,"Close"),Null);  

    CallFactor = IIf(CallPremium >= MinPremium , 1 , CallPremium / MinPremium);  
    PutFactor =  IIf(PutPremium >= MinPremium , 1 , PutPremium / MinPremium);  

    Code  = StrToNum(strmid(Name(),19,1))*10000 + StrToNum(strmid(Name(),20,1))*1000 + StrToNum(StrMid(Name(),21,1))*100;

    PositionScore = IIf(Type == "PE" AND StrikePriceSelector == 1,1000000,IIf(Type =="PE" AND LongStrikePriceSelector == 1,1000000-Code,IIf(Type =="CE" AND StrikePriceSelector == 1,1000000,Code)));  

    Cases = Optimize("Cases",0,0,7,1);

    if(Cases == 0){Entrytime = 092000;}
    if(Cases == 1){Entrytime = 094500;}
    if(Cases == 2){Entrytime = 101500;}
    if(Cases == 3){Entrytime = 104500;}
    if(Cases == 4){Entrytime = 111500;}
    if(Cases == 5){Entrytime = 114500;}
    if(Cases == 6){Entrytime = 121500;}
    if(Cases == 7){Entrytime = 124500;}

    EntryTime = 124500;
    ExitTime  = 152000;

    TimeFrameSet(inDaily);
    NextDay = IIf(DayOfWeek()==5 AND Ref(DayOfWeek(),-1)<=4,5,IIf(DayOfWeek()==1 AND Ref(DayOfWeek(),-1)<5,1,IIf(DayOfWeek()==2 AND Ref(DayOfWeek(),-1)<4 AND Ref(DayOfWeek(),-1)>1,2,0)));
    TimeFrameRestore();

    Nextday=TimeFrameExpand(NextDay,inDaily,expandFirst);

    DTE = DayOfWeek() == 4 OR (DayOfWeek() < 4 AND Ref(DayOfWeek(),1) > 4) OR (DayOfWeek() < 4 AND Ref(DayOfWeek(),4) <= DayOfWeek());

    Short =  StrikePriceSelector == 1 AND TimeNum()==Entrytime AND DiwaliDates;   
    ShortPrice = Close;   

    Cover = TimeNum()==Exittime OR exitlastbar OR DateNum()!=Ref(DateNum(),1);    
    CoverPrice = Close;   

    Short = ExRem(Short,Cover);    
    Cover = ExRem(Cover,Short);   

    Buy =  LongStrikePriceSelector == 1 AND TimeNum()==Entrytime AND DiwaliDates;   
    BuyPrice = Close;   

    Sell = TimeNum()==Exittime AND TimeNum()==Exittime OR exitlastbar OR DateNum()!=Ref(DateNum(),1);  
    SellPrice = Close;   

    Buy = ExRem(Buy,Sell);    
    Sell = ExRem(Sell,Buy);   

    stop = IIf(DayOfWeek()==4,50,IIf(DayOfWeek()==3,40,IIf(DayOfWeek()==2,40,IIf(DayOfWeek()==1,30,IIf(DayOfWeek()==5,30,50)))));
    ShortStop = IIf(Short,stop,100);
    ApplyStop(stopTypeLoss,stopModePercent,ShortStop,1);

    SetCustomBacktestProc("");     

    PercentOfEq = POE/100; 
    Limit = 1;   
    if(Status("action") == actionPortfolio)     
    {     

       bo = GetBacktesterObject();     
       bo.PreProcess();    
       CEstoploss = 0;   
       PEstoploss = 0;
       ShortCallCount = 0;   
       ShortPutCount = 0;

       newday = Day() != Ref(Day(),-1);
       count = 0;       
       BankNiftyClose = Foreign("$BANKNIFTY-NSE", "C" );


       for( i = 0; i<BarCount; i++)     

       {       

        CurrentPortfolioEquity = bo.Equity;   


          CallCount = 0;   
          PutCount = 0;     

            if(newday[i]==1)
            {
             count=0;
            }


            for ( trade = bo.GetFirstOpenPos(); trade; trade = bo.GetNextOpenPos())   
                {  

                 BarClose = trade.GetPrice(i, "C");  

                }  

            for(sig = bo.GetFirstSignal(i) ; sig ; sig = bo.GetNextSignal(i) )
            {
                 if( sig.IsEntry() )
                {
                  count++;
                }
            }

            for(sig = bo.GetFirstSignal(i) ; sig ; sig = bo.GetNextSignal(i) )     

           {   


          Type = StrRight(sig.Symbol,2);
          StrikePrice = StrToNum(StrLeft(StrRight(sig.Symbol,7),5));

          CallRank = staticvarget("CallRankCallPremiumDifference" +  sig.Symbol);
          PutRank = staticvarget("PutRankPutPremiumDifference" +  sig.Symbol);

          ShortCallStrike = IIf(CallRank == 1,StrikePrice,0);
          ShortPutStrike  = IIf(PutRank == 1,StrikePrice,0);

          CallStrike = IIf(StrikePrice == ShortCallStrike AND Type == "CE", 1 , 0);
          PutStrike = IIf(StrikePrice == ShortPutStrike AND Type == "PE", 1 , 0);

          StrikePriceSelector = CallStrike OR PutStrike;

          LongCallStrike = ShortCallStrike + Moneyness;
          LongPutStrike = ShortCallStrike - Moneyness;

          LongCallStrike = IIf(StrikePrice == LongCallStrike AND Type == "CE", 1 , 0);
          LongPutStrike = IIf(StrikePrice == LongPutStrike AND Type == "PE", 1 , 0);

          LongStrikePriceSelector = LongCallStrike OR LongPutStrike;

          CallSymbol = StrLeft(sig.Symbol,19) + StrikePrice + "CE";   
          PutSymbol = StrLeft(sig.Symbol,19) + StrikePrice + "PE";   

          CallPremium = IIf(Type=="CE",Foreign(CallSymbol,"Close"),Null);  
          PutPremium = IIf(Type=="PE",Foreign(PutSymbol,"Close"),Null);  

          CallFactor = IIf(CallPremium >= MinPremium , 1 , CallPremium / MinPremium);  
          PutFactor =  IIf(PutPremium >= MinPremium , 1 , PutPremium / MinPremium);  


            if (sig.IsEntry() AND sig.Type==3 AND Type == "PE")     
          {     
           sig.PosSize = (CurrentPortfolioEquity*PercentOfEq[i]*PutFactor[i]);    
           PEshares = (CurrentPortfolioEquity*PercentOfEq[i]*PutFactor[i])/sig.Price;    
          }     

          if(sig.IsExit() AND sig.Type==4 AND Type == "PE")  
          {  
           PEShares = 0;  
          }  

          if (sig.IsEntry() AND sig.Type==3 AND Type == "CE")     
          {     

           sig.PosSize = (CurrentPortfolioEquity*PercentOfEq[i]*CallFactor[i]);    
           CEshares = (CurrentPortfolioEquity*PercentOfEq[i]*CallFactor[i])/sig.Price;    

          }     

          if(sig.IsExit() AND sig.Type==4 AND Type == "CE")  
          {  
           CEShares = 0;  
          }  

          if (sig.IsEntry() AND sig.IsLong() AND Type == "PE")     
          {     
           sig.PosSize = PEshares*sig.Price;  
           if(PutCount < Limit )   
              PutCount++;   
           else   
              sig.Price = -1;  

          }    

          if (sig.IsEntry() AND sig.IsLong() AND Type == "CE")     
          {     
           sig.PosSize = CEshares*sig.Price;     
           if(CallCount < Limit )   
              CallCount++;   
           else   
              sig.Price = -1;  

          }    


        }                

        bo.ProcessTradeSignals(i);   


        for( sig = bo.GetFirstSignal(i); sig; sig = bo.GetNextSignal(i) )   
        {   

              if(sig.Reason == 2)   
          {   

              if(Type == "PE")   
            {   
              if( sig.IsLong() )   
                PEstoploss[i] = PEstoploss[i-1];   
              else   
                PEstoploss[i] = PEstoploss[i-1] + 1;   
              }    

              if(Type == "CE")   
            {   
              if( sig.IsLong() )   
                CEstoploss[i] = CEstoploss[i-1];   
              else   
                CEstoploss[i] = CEstoploss[i-1] + 1;   
              }   


          }   


        }       

        for( trade = bo.GetFirstOpenPos(); trade; trade = bo.GetNextOpenPos() )   

            {   
                longsymbol = StrRight(trade.Symbol,2);   
                if( trade.IsLong() )   
                {   
            if(PEstoploss[i] > PEstoploss[i-1] AND longsymbol=="PE" )   
            {   
              bo.ExitTrade( i, trade.Symbol, trade.GetPrice( i, "C" ), 1 );	   
            }   

              if(CEstoploss[i] > CEstoploss[i-1] AND longsymbol=="CE" )   
            {   
              bo.ExitTrade( i, trade.Symbol, trade.GetPrice( i, "C" ), 1 );	   
            }   

          }	   

        }	   


        bo.UpdateStats(i, 1);     
        bo.UpdateStats(i, 2);    

        }     

       bo.PostProcess();     

    }      

    PortEquity = Foreign("~~~EQUITY", "C" );    

    Filter = 1;
    AddColumn(PortEquity,"PortEquity",1);

    _SECTION_END();  
