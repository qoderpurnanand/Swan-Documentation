## BankNiftyWeeklyShortOptions(ATM-OTM)

    _SECTION_BEGIN("Price");   
    SetChartOptions(0,chartShowArrows|chartShowDates);   
    _N(Title = StrFormat("{{NAME}} - {{INTERVAL}} {{DATE}} Open %g, Hi %g, Lo %g, Close %g (%.1f%%) Vol " +WriteVal( V, 1.0 ) +" {{VALUES}}", O, H, L, C, SelectedValue( ROC( C, 1 )) ));   
    Plot( C, "Close", ParamColor("Color", colorDefault ), styleNoTitle | ParamStyle("Style") | GetPriceStyle() );    

    #include <BankNiftyWeeklyStrikePriceSelector.afl>    
    SetOption("InitialEquity",10000000);    
    SetOption("AccountMargin",100);  
    MaxPos = 2;  
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

    DiwaliDates = DateNum()!=1111026 AND DateNum()!=1121113 AND DateNum()!=1131103 AND DateNum()!=1141023 AND DateNum()!=1151111 AND DateNum()!=1161030 AND DateNum()!=1171019 AND DateNum()!=1181107 AND DateNum()!=1191027 AND DateNum()!=1200604 AND DateNum()!=1201114 AND DateNum()!=1211104;  

    LotSize = IIf(Datenum()>=1110101 AND DateNum()<=1151029, 25 , IIf( DateNum()>=1151030 AND DateNum()<=1160630 , 30, IIf( DateNum()>=1160701 AND DateNum()<=1181025 , 40 , IIf( DateNum()>=1181026 AND DateNum()<=1200730 , 20 , 25)))) ;     

    POE = Optimize("POE",2,3,8,1); 

    CallSymbol = StrLeft(Name(),20)+"CE";    
    PutSymbol  = StrLeft(Name(),20)+"PE";
    CallPremium = Foreign(CallSymbol,"Close");   
    PutPremium = Foreign(PutSymbol,"Close");     
    CallPremiumAmount = IIF(Type == "CE",Foreign(StrLeft(Name(),20) + "CE","Close"),0) + IIF(Type == "PE",Foreign(StrLeft(Name(),20) + "PE","Close"),0); 
    PutPremiumAmount = IIF(Type == "PE",Foreign(StrLeft(Name(),20)+"PE","Close"),0) + IIF(Type == "CE",Foreign(StrLeft(Name(),20)+"CE","Close"),0);

    ExposureMargin = Foreign("$BANKNIFTY-NSE", "C" )*2*0.02*LotSize;   
    SpanMargin = Moneyness*LotSize;   
    TotalMargin = ExposureMargin + SpanMargin;   
    MISLeverage = 12;
    Deposit = ((Foreign("$BANKNIFTY-NSE", "C" )*LotSize*2)/MISLeverage);    
    MinPremium = (Deposit*(POE/100))/LotSize;    
    CallFactor = IIf(CallPremium >= MinPremium , 1 , CallPremium / MinPremium);   
    PutFactor =  IIf(PutPremium >= MinPremium , 1 , PutPremium / MinPremium);   
    PositionSize = IIf(Type == "CE" , -CallFactor*POE , -PutFactor*POE);   

    Short =  StrikePriceSelector == 1 AND TimeNum()==Entrytime AND DiwaliDates; 
    ShortPrice = Close;    

    Cover = TimeNum()==ExitTime OR exitlastbar OR DateNum()!=Ref(DateNum(),1);   
    CoverPrice = Close;      

    Short = ExRem(Short,Cover);    
    Cover = ExRem(Cover,Short);  

    Shortstop = Optimize("ShortStop",40,10,90,10);  
    ApplyStop(StopTypeloss,stopModePercent,Shortstop,1);  

    PortEquity = Foreign("~~~EQUITY", "C" );    

    Filter = 1; 
    AddColumn(PortEquity,"PortEquity",1);   

    _SECTION_END();  
