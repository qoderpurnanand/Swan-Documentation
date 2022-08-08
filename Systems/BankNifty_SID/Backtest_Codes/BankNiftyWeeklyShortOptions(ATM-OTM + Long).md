## BankNiftyWeeklyShortOptions(ATM-OTM + Long)

    _SECTION_BEGIN("Price");   
    SetChartOptions(0,chartShowArrows|chartShowDates);   
    _N(Title = StrFormat("{{NAME}} - {{INTERVAL}} {{DATE}} Open %g, Hi %g, Lo %g, Close %g (%.1f%%) Vol " +WriteVal( V, 1.0 ) +" {{VALUES}}", O, H, L, C, SelectedValue( ROC( C, 1 )) ));   
    Plot( C, "Close", ParamColor("Color", colorDefault ), styleNoTitle | ParamStyle("Style") | GetPriceStyle() );    

    #include <BankNifty Weekly StrikePriceSelector(CO).afl>    
    SetOption("InitialEquity",10000000);    
    SetOption("AccountMargin",100);  
    MaxPos = 4;  
    SetOption("MaxOpenPositions",MaxPos);    
    SetTradeDelays(0,0,0,0);    
    SetOption("DisableRuinStop",True);  

    Cases = Optimize("Cases",1,1,13,4);

    if(Cases == 0){Entrytime = 091500;}
    if(Cases == 1){Entrytime = 093000;}
    if(Cases == 2){Entrytime = 094500;}
    if(Cases == 3){Entrytime = 100000;}
    if(Cases == 4){Entrytime = 101500;}
    if(Cases == 5){Entrytime = 103000;}
    if(Cases == 6){Entrytime = 104500;}
    if(Cases == 7){Entrytime = 110000;}
    if(Cases == 8){Entrytime = 111500;}
    if(Cases == 9){Entrytime = 113000;}
    if(Cases == 10){Entrytime = 114500;}
    if(Cases == 11){Entrytime = 120000;}
    if(Cases == 12){Entrytime = 121500;}
    if(Cases == 13){Entrytime = 123000;}
    if(Cases == 14){Entrytime = 124500;}
    if(Cases == 15){Entrytime = 130000;}

    ExitTime = 152000;  

    bi = BarIndex();  
    exitlastbar = bi == LastValue(bi - 1);      

    DiwaliDates = DateNum()!=1111026 AND DateNum()!=1121113 AND DateNum()!=1131103 AND DateNum()!=1141023 AND DateNum()!=1151111 AND DateNum()!=1161030 AND DateNum()!=1171019 AND DateNum()!=1181107 AND DateNum()!=1191027 AND DateNum()!=1200604;  

    LongStrikeCall = ValueWhen(LongStrikePriceSelector == 1 AND Type == "CE",Foreign(StrLeft(Name(),15) + (Strikeprice - Moneyness) + "CE","Close"));
    LongStrikePut = ValueWhen(LongStrikePriceSelector == 1 AND Type == "PE",Foreign(StrLeft(Name(),15) + (Strikeprice + Moneyness) + "PE","Close"));

    EquityPercent = Optimize("POE",5,3,8,1);

    LotSize = IIf(Datenum()>=1110101 AND DateNum()<=1151029, 25 , IIf( DateNum()>=1151030 AND DateNum()<=1160630 , 30, IIf( DateNum()>=1160701 AND DateNum()<=1181025 , 40 , IIf( DateNum()>=1181026 AND DateNum()<=1200730 , 20 , 25)))) ;     

    POE = EquityPercent;   

    PositionScore = IIf(Type == "PE" AND StrikePriceSelector == 1,1000000,IIf(Type =="PE" AND LongStrikePriceSelector == 1,1000000-Code,IIf(Type =="CE" AND StrikePriceSelector == 1,1000000,Code)));  

    Short =  StrikePriceSelector == 1 AND TimeNum()==Entrytime AND DiwaliDates; 
    ShortPrice = Close;    

    SL = 0.40;  
    ShortClose = ValueWhen(Short,Close);  
    SqOff = High > ShortClose*(1 + SL);  

    Cover = TimeNum()==ExitTime OR exitlastbar OR DateNum()!=Ref(DateNum(),1) OR SqOff;    
    CoverPrice = IIf(SqOff,ShortClose*(1 + SL),Close);      

    Short = ExRem(Short,Cover);    
    Cover = ExRem(Cover,Short);  

    Buy = ((LongStrikePriceSelector == 1 AND TimeNum()==EntryTime AND DiwaliDates AND LongStrikeCall < ActualMinPremium AND Type=="CE") OR (LongStrikePriceSelector == 1 AND TimeNum()==EntryTime AND DiwaliDates AND LongStrikePut < ActualMinPremium AND Type=="PE" ) );  
    BuyPrice = Close;   

    Sell = TimeNum()==Exittime OR exitlastbar OR DateNum()!=Ref(DateNum(),1);    
    SellPrice = Close;    

    Buy = ExRem(Buy,Sell);     
    Sell = ExRem(Sell,Buy);    

    SetCustomBacktestProc("");     

    PercentOfEq = POE/100; 
    Limit = 1;   
    if(Status("action") == actionPortfolio)     
    {     

       bo = GetBacktesterObject();     
       bo.PreProcess();    
       CEstoploss = 0;   
       PEstoploss = 0;   

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

          CallSymbol = StrLeft(sig.symbol,20)+"CE";    
          PutSymbol = StrLeft(sig.symbol,20)+"PE";    
          CallPremium = Foreign(CallSymbol,"Close");   
          PutPremium = Foreign(PutSymbol,"Close"); 
          CallPremiumAmount = IIF(Type == "CE" AND StrikePriceSelector == 1,Foreign(StrLeft(sig.symbol,20) + "CE","Close"),0) + IIF(Type == "PE" AND StrikePriceSelector == 1,Foreign(StrLeft(sig.symbol,20) + "PE","Close"),0); 
          PutPremiumAmount = IIF(Type == "PE"AND StrikePriceSelector == 1,Foreign(StrLeft(sig.symbol,20)+"PE","Close"),0) + IIF(Type == "CE" AND StrikePriceSelector == 1,Foreign(StrLeft(sig.symbol,20)+"CE","Close"),0);

          LotSize = IIf(Datenum()>=1110101 AND DateNum()<=1151029, 25 , IIf( DateNum()>=1151030 AND DateNum()<=1160630 , 30, IIf( DateNum()>=1160701 AND DateNum()<=1181025 , 40 , IIf( DateNum()>=1181026 AND DateNum()<=1200730 , 20 , 25)))) ;     

          MaxLev = 8;
          POE = PercentOfEq; 
          ActualDeposit = ((Foreign("$BANKNIFTY-NSE", "C")*LotSize[i]*2)/MaxLev);    
          ActualMinPremium = (ActualDeposit*POE)/LotSize[i];    

          ExposureMargin = BankNiftyClose*2*0.02*LotSize[i];   
          SpanMargin = Moneyness*LotSize[i];   
          TotalMargin = ExposureMargin + SpanMargin;   
          MISLeverage = IIf(CallPremiumAmount < ActualMinPremium AND PutPremiumAmount < ActualMinPremium,(BankNiftyClose*2*LotSize[i]/TotalMargin),MaxLev);   
          Deposit = ((BankNiftyClose*LotSize[i]*2)/MISLeverage);    
          MinPremium = (Deposit*(PercentOfEq))/LotSize[i];    
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

              if(sig.Reason == 1)   
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
