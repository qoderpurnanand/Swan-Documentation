## STRIKE SELECTOR
    NiftyWeeklyStrikePriceSelector

    TimeFrameSet(inDaily);
    #include <expirydates.afl>  
    OptionExpiryDate = DateTimeConvert(2,WeeklyExpiryDate);
    StartDate = DateTimeConvert(2,DateNum());
    DTE = round(DateTimeDiff(OptionExpiryDate,StartDate)/(3600*24));
    TimeFrameRestore();

    DaysToExpiry = TimeFrameExpand(DTE,inDaily,expandFirst);
    NextExpirySym = IIf(StrRight(Name(),2)=="-I",1,0);

    StrikePrice1 = IIf(StrLen(Name())==18,StrToNum(StrLeft(StrRight(Name(),7),5)),StrToNum(StrLeft(StrRight(Name(),6),4)));
    StrikePrice2 = IIf(StrLen(Name())==18,StrToNum(StrLeft(StrRight(Name(),9),5)),StrToNum(StrLeft(StrRight(Name(),8),4)));
    StrikePrice  = IIf(NextExpirySym==0,StrikePrice1,StrikePrice2);  
    Type = WriteIf(nextexpirysym==1,StrLeft(StrRight(Name(),4),2),StrRight(Name(),2));

    BankNiftyClose = Foreign("$NIFTY-NSE", "C" );
    CallATM = (round(BankNiftyClose/100)*100);
    PutATM = (round(BankNiftyClose/100)*100);

    OTMPf = optimize("otmpf",0,-200,200,100);

    CallOTM = round((CallATM + OTMPf)/100)*100;
    PutOTM = round((PutATM - OTMPf)/100)*100;

    CallSelection = IIf(Type == "CE" AND (StrikePrice == CallOTM), 1 , 0);
    PutSelection  = IIf(Type == "PE" AND (StrikePrice == PutOTM), 1 , 0);

    StrikePriceSelector = CallSelection OR PutSelection;
