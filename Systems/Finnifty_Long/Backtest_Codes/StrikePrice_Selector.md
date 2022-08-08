## Strike Price Selector

    TimeFrameSet(inDaily);
    #include <finnifty_Expirydates.afl>  
    OptionExpiryDate = DateTimeConvert(2,finnifty_weeklyexpiry);
    StartDate = DateTimeConvert(2,DateNum());
    DTE = round(DateTimeDiff(OptionExpiryDate,StartDate)/(3600*24));
    TimeFrameRestore();

    DaysToExpiry = TimeFrameExpand(DTE,inDaily,expandFirst);
    NextExpirySym = IIf(StrRight(Name(),3)=="-II",1,0);

    StrikePrice1 = StrToNum(StrLeft(StrRight(Name(),9),5));
    StrikePrice2 = StrToNum(StrLeft(StrRight(Name(),11),5));
    StrikePrice  = IIf(NextExpirySym==0,StrikePrice1,StrikePrice2);  
    Type = StrRight(StrLeft(StrRight(Name(),9),7),2);

    finniftyclose = Foreign("$NIFTY_FIN_SERVICE-NSE", "C" );
    CallATM = (round(finniftyclose/100)*100);
    PutATM =  (round(finniftyclose/100)*100);

    OTMPf = optimize("otmpf",0,-200,200,100);

    CallOTM = round((CallATM + OTMPf)/100)*100;
    PutOTM = round((PutATM - OTMPf)/100)*100;

    CallSelection = IIf(Type == "CE" AND (StrikePrice == CallOTM), 1 , 0);
    PutSelection  = IIf(Type == "PE" AND (StrikePrice == PutOTM), 1 , 0);

    StrikePriceSelector = CallSelection OR PutSelection;

    Filter =1;
    AddColumn(Daystoexpiry,"Daystoexpiry");
    AddColumn(finniftyclose,"finniftyclose");
    AddtextColumn(type,"type");
    AddColumn(strikeprice,"strikeprice");



























