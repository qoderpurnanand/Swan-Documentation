## BACKTEST CODE ON FUTURES DATABASE
    #include <expiry selection.afl>

    switch1 = 20;///10 or 30///

    maxpos = 15;
    addtime = 459;
    SID1EQ = 100000000;
    SID1lev = 1;
    SetOption("MaxOpenPositions",maxpos);
    SetOption("InitialEquity",SID1eq);
    SetOption("AccountMargin",100);
    SetPositionSize(100/maxpos*SID1lev,spspercentofequity);
    //SetPositionSize(SID1EQ/maxpos,spsValue);

    SetTradeDelays(0,0,0,0);
    SetOption("PriceBoundChecking",False);

    //rand = Optimize("rand",1,1,5,1);

    ef = 0.1;//Optimize("ef",1,1,2,1)/10;
    sf = 1/10;
    vp = 1;
    covervp = 4;

    sp = Optimize("sp",6,6,7,1);
    addtime = 459;
    exittime = 151000+addtime;//094000;
    starttime = 091500+addtime;//034500;
    lasttradetime = 094000+addtime;//041000;
    maxrank = switch1;
    minstop = 0.02;
    maxstop = 0.08;

    TimeFrameSet(inDaily);
    atrstp = Ref(ATR(1),-1)*sp/10;
    fdw = DayOfWeek() < Ref(DayOfWeek(),-1);
    poi = Ref(C,-1);
    edist = Ref(ATR(vp),-1) * ef;
    slpts = atrstp;
    strig = poi + edist;


    TimeFrameRestore();

    atrstp = TimeFrameExpand(atrstp,inDaily,expandFirst);
    poi = TimeFrameExpand(poi,inDaily,expandFirst);
    slpts = TimeFrameExpand(slpts,inDaily,expandFirst);
    strig = TimeFrameExpand(strig,inDaily,expandFirst);

    dailyopen = TimeFrameGetPrice("O",inDaily,0,expandFirst);

    strade = H>strig ;

    newday = Day() != Ref(Day(),1);

    replace = WriteIf(StrToNum(StrRight(Name(),1))==1,".FUT1",".FUT");
    rank = Foreign("~SIDLMT0.1FUT" + StrReplace(Name() , replace , ".EQ-NSE") ,"C");
    rankOK = Rank <= maxrank AND Rank >=1;

    #Include<CustombcSID.afl>

    fdw = TimeFrameExpand(fdw,inDaily,expandFirst);
    timeOK = TimeNum() >= starttime AND TimeNum() < lasttradetime;///to run for whole day


    stradecount = SumSince(newday,strade);
    //stradecount = SumSince(TimeNum() == starttime+addtime-500,strade);
    shortcondi = stradecount == 1 AND strade;


    Short = intraday AND timeOK and strade AND shortcondi AND rankok /*AND strig > dailyopen*/;
    ShortPrice = IIf(Open > strig, Open/**(1-0.13/100)*/,strig/**(1-0.07/100)*/);//Max(Open*(1-0.1/100),strig*(1-0.05/100));
    //ShortPrice = Max(Open,strig);
    slprice0 = ValueWhen(Short,Max(Open,strig))*(1+minstop); // 2% stop
    slprice1 = ValueWhen(Short,Max(Open,strig))+Slpts; //ATR stop
    slprice2 = ValueWhen(Short,Max(Open,strig))*(1+maxstop); // 8% stop
    slprice = IIf(slprice1 < slprice0, slprice0, IIf(slprice1 > slprice2, slprice2, slprice1));
    //Min(slprice1,slprice2);

    //slprice = ValueWhen(Short,strig)+Slpts;

    eqslcond = H>= slprice ;

    covervol = Ref(ATR(covervp),-1);
    ctrig = Ref(C,-1) - (covervol * sf);
    Coverlimit = TimeNum() == exittime AND L < Ctrig ;


    Cover = TimeNum()>=exittime OR (eqslcond) /*if shorting at 915 close*/;
    CoverPrice = IIf(eqslcond, Max(Open,slprice)/**(1+0.13/100)*/,IIf(coverlimit, Min(Open,Ctrig)/**(1+0.07/100)*/, Open/**(1+0.13/100)*/));
    //CoverPrice = IIf(eqslcond, Max(Open,slprice),IIf(coverlimit,Min(Open,ctrig),Open));
    /*
    if(switch1==30)
    {
    PositionScore = Random();
    }
    */
    /*
    SetCustomBacktestProc("");
    if( Status("action") == actionPortfolio )
    {
    bo = GetBacktesterObject();
    bo.Backtest();
    AddToComposite( bo.EquityArray,
    "~~~SIDEQUITY"+ef, "X",
    atcFlagDeleteValues | atcFlagEnableInPortfolio );
    }
    */

    //Filter =1;
    //AddColumn(Close,"Close");


    Filter = /* TimeNum() == starttime AND rankok AND */intraday;//Short;//TimeNum()==091500 OR TimeNum()==920000;
    AddColumn(shortcondi,"shortcondi");
    AddColumn(timeOK,"timeOK");
    AddColumn(strade,"strade");
    AddColumn(short,"Short");
    AddColumn(ShortPrice,"ShortPrice");
    AddColumn(slprice1,"slprice1");
    AddColumn(slprice2,"slprice2");
    AddColumn(slprice,"slprice");
    AddColumn(Cover,"Cover");
    AddColumn(CoverPrice,"CoverPrice");
    AddColumn(High,"High");
    AddColumn(rank,"rank");
