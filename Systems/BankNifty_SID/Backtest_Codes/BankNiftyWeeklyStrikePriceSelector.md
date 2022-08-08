### BankNifty Weekly Strike Price Selector Code
    _SECTION_BEGIN("Price"); 

    TimeFrameSet(inDaily);
    #include <ExpiryDates.afl>  
    OptionExpiryDate = DateTimeConvert(2,WeeklyExpiryDate);
    StartDate = DateTimeConvert(2,DateNum());
    DTE = round(DateTimeDiff(OptionExpiryDate,StartDate)/(3600*24));
    TimeFrameRestore();

    DaysToExpiry = TimeFrameExpand(DTE,inDaily,expandFirst);
    NextExpirySym = IIf(StrRight(Name(),2)=="-I",1,0);

    StrikePrice1 = StrToNum(StrLeft(StrRight(Name(),7),5));
    StrikePrice2 = StrToNum(StrLeft(StrRight(Name(),9),5));
    StrikePrice  = IIf(NextExpirySym==0,StrikePrice1,StrikePrice2);  
    //Type = WriteIf(nextexpirysym==1,StrLeft(StrRight(Name(),4),2),StrRight(Name(),2));
    Type = StrRight(Name(),2);

    BankNiftyClose = Foreign("$BANKNIFTY-NSE", "C" );
    CallATM = (round(BankNiftyClose/100)*100);
    PutATM = (round(BankNiftyClose/100)*100);

    OTMPf = 0;

    CallOTM = round((CallATM + OTMPf)/100)*100;
    PutOTM = round((PutATM - OTMPf)/100)*100;

    Moneyness = 1000;

    CallSelection = IIf(Type == "CE" AND (StrikePrice >= CallOTM), 1 , 0);
    PutSelection  = IIf(Type == "PE" AND (StrikePrice <= PutOTM), 1 , 0);

    StrikePriceSelector = CallSelection OR PutSelection;

    Code  = StrToNum(strmid(Name(),15,1))*10000 + StrToNum(strmid(Name(),16,1))*1000 + StrToNum(StrMid(Name(),17,1))*100;

    LongCallOTM = CallOTM + Moneyness;
    LongPutOTM  = PutOTM - Moneyness;

    LongCallSelection = IIf(Type == "CE" AND StrikePrice == LongCallOTM , 1 ,0);
    LongPutSelection = IIf(Type == "PE" AND StrikePrice == LongPutOTM , 1 ,0);

    LongStrikePriceSelector = LongCallSelection OR LongPutSelection;
