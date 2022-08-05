**Inputs:**

Entry time: 091500 

Exit time: 151000 or stoploss

Transaction Cost: 0.15%

Timeframe: Backtested on daily and 5 minute timeframe

MaxPos: 15

Stoploss: 6/10 ATR or min 2% or max 8%

Ef: 0.1

Vp: 4

**Database Details:**

DB Name: Network\iMAC2\f\All databases\Equities\ F&O Equities (EOD database)
Watchlist: F&O Equities

DB Name: Network\iMAC2\f\All databases\Futures\ Futures Database (Continuous)
Watchlist: All symbols


Database and Backtest Settings:
 
![image](https://user-images.githubusercontent.com/63246619/183023236-95755c3f-946b-4393-8438-181fe5dbda31.png)



PROCESS:

•	Run the short intraday average ranking code on F&O Equites database and add to composite the selected ranks 

•	Use the includeok EQ and banlist EQ code from Database maintenance and add in #include folder and filter the stocks while ranking. Backtest can be done without banlist code too

•	Copy the composite symbols from the current database folder and paste it in Futures Database folder and delete broker master file

•	Run the backtest code on on Futures database

•	Use custom backtester code and add it in #include folder. Change the number of maxpos in it depending on the maxpos in backtest. Currently 15.

•	Use the expiry selection code and add it in #include folder for selection of expiry since we trade next expiry on last day

•	The whole backtest can also be done on F&O equities instead of futures database to check the overall optimization results

*For expiry selection, includeok and banlist codes – refer to database maintenance.*

## SHORT INTRADAY AVERAGE RANKING CODE:

        afl = "ShortAvgRanking2";
        maxpos = 15;

        #include <Includeok.afl>
        #include <Banlist.afl>

        x1 = x2 = x3 = x4 = x5 = x6 = x7 = x8 = x9 = 1/9;

        maxrank = maxpos;

        vp = 1;
        llb = 1;
        zslb = 5;

        //excludeok = 0; // add banlist include

        Volfilter = 1;

        paramLenRSI = 3;
        paramLenUD = 2;
        paramLenRank = 100;

        function ConnorsRSI(lenRSI, lenUD, lenROC)
        {
              upDays = BarsSince(C <= Ref(C,-1));
              downDays = BarsSince(C >= Ref(C,-1));
              updownDays = IIf(upDays > 0, upDays, IIf(downDays > 0, -downDays, 0));
              crsi = ( PercentRank(ROC(C,1), lenROC) + RSIa(updownDays,lenUD) +RSI(lenRSI))/3;

             return crsi;

        }


        watchlist = 1;

        List = CategoryGetSymbols(categoryWatchlist,watchlist);

        if ( Status("stocknum") == 0 ) // Generate ranking when we are on the very first symbol
        {


        StaticVarRemove( "values*" );

        for ( n = 0; ( Sym = StrExtract( List, n ) )  != "";  n++    )
        {

        SetForeign ( sym );

        #include <Includeok.afl>
        #include <Banlist.afl>

            ROCVol = Ref(ROC(Volume,llb),-1);
            crsi = Ref(ConnorsRSI(paramLenRSI,paramLenUD,paramLenRank),-1);

            ROCprice = ref(ROC(Close,llb),-1);
            rsiprice = ref(RSIa(Close,14),-1);

            //Volatility indicators
            atrpr = ref(PercentRank(ATR(vp),100),-1);
            mb = ref(MA(C,zslb+1),-1);
            Zscore = ref((C - mb) / (StDev(C,zslb+1)),-1);		
            atrc = ref((ATR(vp)/Close)*100,-1);

            // Volume Indicators
            ROCvol = ref(ROC(Volume,llb),-1);
            rsivol = ref(RSIa(Volume,14),-1);
            volpr = ref(PercentRank(Volume,100),-1);



            values1 = IIf(includeok AND Excludeok == 0 AND Volfilter AND sym != "$NIFTY-NSE", CRSI, Null);
            values2 = IIf(includeok AND Excludeok == 0 AND Volfilter AND sym != "$NIFTY-NSE", ROCprice , Null);
            values3 = IIf(includeok AND Excludeok == 0 AND Volfilter AND sym != "$NIFTY-NSE", rsiprice , Null);
            values4 = IIf(includeok AND Excludeok == 0 AND Volfilter AND sym != "$NIFTY-NSE", atrpr , Null);
            values5 = IIf(includeok AND Excludeok == 0 AND Volfilter AND sym != "$NIFTY-NSE", Zscore , Null);
            values6 = IIf(includeok AND Excludeok == 0 AND Volfilter AND sym != "$NIFTY-NSE", atrc , Null);
            values7 = IIf(includeok AND Excludeok == 0 AND Volfilter AND sym != "$NIFTY-NSE", ROCvol , Null);
            values8 = IIf(includeok AND Excludeok == 0 AND Volfilter AND sym != "$NIFTY-NSE", rsivol , Null);
            values9 = IIf(includeok AND Excludeok == 0 AND Volfilter AND sym != "$NIFTY-NSE", volpr , Null);

            RestorePriceArrays();

            StaticVarSet(afl+"values1"+Sym, values1);
            StaticVarSet(afl+"values2"+Sym, values2);
            StaticVarSet(afl+"values3"+Sym, values3);
            StaticVarSet(afl+"values4"+Sym, values4);
            StaticVarSet(afl+"values5"+Sym, values5);
            StaticVarSet(afl+"values6"+Sym, values6);
            StaticVarSet(afl+"values7"+Sym, values7);
            StaticVarSet(afl+"values8"+Sym, values8);
            StaticVarSet(afl+"values9"+Sym, values9);



        _TRACE( sym );
            }

          StaticVarGenerateRanks("rank",afl+"Values1",0,1234);
          StaticVarGenerateRanks("rank",afl+"Values2",0,1234);
          StaticVarGenerateRanks("rank",afl+"Values3",0,1234);
          StaticVarGenerateRanks("rank",afl+"Values4",0,1234);
          StaticVarGenerateRanks("rank",afl+"Values5",0,1234);
          StaticVarGenerateRanks("rank",afl+"Values6",0,1234);
          StaticVarGenerateRanks("rank",afl+"Values7",0,1234);
          StaticVarGenerateRanks("rank",afl+"Values8",0,1234);
          StaticVarGenerateRanks("rank",afl+"Values9",0,1234);


        }


        Sym = Name();


        values1 = StaticVarGet(afl+"values1" + Sym);
        values2 = StaticVarGet(afl+"values2" + Sym);
        values3 = StaticVarGet(afl+"values3" + Sym);
        values4 = StaticVarGet(afl+"values4" + Sym);
        values5 = StaticVarGet(afl+"values5" + Sym);
        values6 = StaticVarGet(afl+"values6" + Sym);
        values7 = StaticVarGet(afl+"values7" + Sym);
        values8 = StaticVarGet(afl+"values8" + Sym);
        values9 = StaticVarGet(afl+"values9" + Sym);

        v1 = StaticVarGet("rank" + afl + "values1" + Sym);
        v2 = StaticVarGet("rank" + afl + "values2" + Sym);
        v3 = StaticVarGet("rank" + afl + "values3" + Sym);
        v4 = StaticVarGet("rank" + afl + "values4" + Sym);
        v5 = StaticVarGet("rank" + afl + "values5" + Sym);
        v6 = StaticVarGet("rank" + afl + "values6" + Sym);
        v7 = StaticVarGet("rank" + afl + "values7" + Sym);
        v8 = StaticVarGet("rank" + afl + "values8" + Sym); 
        v9 = StaticVarGet("rank" + afl + "values9" + Sym); 


        if ( Status("stocknum") == 0 ) // Generate ranking when we are on the very first symbol
        {
          //StaticVarRemove( "values*" );

          for ( n = 0; ( Sym = StrExtract( List, n ) )  != "";  n++    )
          {
            SetForeign ( Sym );

            //Sym = Name();


            #include <Includeok.afl>
            //excludeok = 0;

            v1 = 10000 - StaticVarGet("rank" + afl + "values1"+Sym);
            v2 = 10000 - StaticVarGet("rank" + afl + "values2"+Sym);
            v3 = 10000 - StaticVarGet("rank" + afl + "values3"+Sym);
            v4 = 10000 - StaticVarGet("rank" + afl + "values4"+Sym);
            v5 = 10000 - StaticVarGet("rank" + afl + "values5"+Sym);
            v6 = 10000 - StaticVarGet("rank" + afl + "values6"+Sym);
            v7 = 10000 - StaticVarGet("rank" + afl + "values7"+Sym);
            v8 = 10000 - StaticVarGet("rank" + afl + "values8"+Sym);
            v9 = 10000 - StaticVarGet("rank" + afl + "values9"+Sym);

            AvgRank =  v1*X1 + v2*x2 + v3*x3 + v4*x4 + v5*x5 + v6*x6 + v7*x7 + v8*x8 + v9*x9 ;

            RestorePriceArrays();

            StaticVarSet(afl+"AvgRank"+Sym, AvgRank);
        _TRACE( sym );
            }

        StaticVarGenerateRanks( "rank", afl+"AvgRank", 0, 1234 );

          rank = StaticVarGet ( "rank" + afl + "AvgRank" +  Sym );


            StaticVarRemove(afl+"addrank");
            StaticVarRemove(afl+"valuecheck");

        }
        crsi = Ref(ConnorsRSI(paramLenRSI,paramLenUD,paramLenRank),-1);
        rocvol = Ref(ROC(Volume,llb),-1);


        sym = Name();
        AvgRank = StaticVarGet ( afl+"AvgRank" +  Sym );
        rank = StaticVarGet ( "rank" + afl + "AvgRank" +  Sym );


        rankOK = rank <= 20;

        //AddToComposite(rank,"~SIDLMT0.1FUT" + name(),"X",atcFlagResetValues);
        //AddToComposite(rank,"~SIDLMT0.1FUT" + name(),"X",atcFlagResetValues);

        //comprank = Foreign("~SIDLMT0.1FUT" + Name() ,"C");


        Filter = 1;
        AddColumn(rankOK,"rankOK");
        AddColumn(AvgRank,"Finalrank");
        AddColumn(rank,"rank");
        SetSortColumns(3);



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


## CUSTOM BACKTESTER CODE


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

## RANKING INDICATOR SELECTION


        #include <includeok.afl>

        maxpos = 10;
        lev = 1;
        initialcap = 10000000;

        SetOption("MaxOpenPositions",maxpos);
        SetOption("InitialEquity",initialcap);
        SetOption("AccountMargin",100/Lev);
        SetPositionSize(100/maxpos*lev,spsPercentOfEquity);

        SetTradeDelays(0,0,0,0);
        lb = Optimize("lb",5,1,10,2);

        ef = Optimize("ef",1,1,3,1)/10;
        //r = Optimize("r",1,1,25,1);
        vp = 5;//Optimize("vp",11,1,12,2);
        //sd = Optimize("sd",1.1,1.1,1.4,0.1);
        Cases = Optimize("Cases",2,1,24,1);


        paramLenRSI = 3; //Param("RSI Closes Length", crsilb, crsilb, 100, 1);
        paramLenUD = 2; //Param("RSI UpClose Length", 2, 2, 100, 1); // ask
        paramLenRank = 100; //Param("PerecentRank Length", 100, 10, 200, 1); // ask

        function ConnorsRSI(lenRSI, lenUD, lenROC)
        {
              upDays = BarsSince(C <= Ref(C,-1));
              downDays = BarsSince(C >= Ref(C,-1));
              updownDays = IIf(upDays > 0, upDays, IIf(downDays > 0, -downDays, 0));
              crsi = ( PercentRank(ROC(C,1), lenROC) + RSIa(updownDays,lenUD) +RSI(lenRSI))/3;

             return crsi;

        }


        ASCDEC = 1;//Optimize("ASCDEC",1,1,2,1);
        Rankcase = 1;//Optimize("Rankcase",1,1,11,1);
        rn = 10;

        minrank = IIf(rankcase == 1,1,IIf(rankcase == 2,rn, IIf(rankcase == 3,rn*2,IIf(rankcase == 4,rn*3,IIf(rankcase == 5,rn*4,IIf(rankcase == 6,rn*5,IIf(rankcase == 7,rn*6,IIf(rankcase == 8,rn*7,IIf(rankcase == 9,rn*8,IIf(rankcase == 10,rn*9, IIf(rankcase == 11,rn*10,null)))))))))));
        maxrank = IIf(rankcase == 1,rn,IIf(rankcase == 2,rn*2, IIf(rankcase == 3,rn*3,IIf(rankcase == 4,rn*4,IIf(rankcase == 5,rn*5,IIf(rankcase == 6,rn*6,IIf(rankcase == 7,rn*7,IIf(rankcase == 8,rn*8,IIf(rankcase == 9,rn*9,IIf(rankcase == 10,rn*10, IIf(rankcase == 11,rn*11,null)))))))))));

        /*
        minrank = IIf(ascdec == 1, 1, 343);
        Maxrank = IIf(ascdec == 1, 50, 393);
        */

        if(Cases == 1)
        {
        //ATRPR
        Indicator = Ref(PercentRank(ATR(vp),100),-1);
        INDICATOR = IIf(ascdec == 1, indicator, -indicator);

        }

        if(Cases == 2)
        {
        //ROC Price
        Indicator = Ref(ROC(Close,lb),-1);
        INDICATOR = IIf(ascdec == 1, indicator, -indicator);

        }

        if(Cases == 3)
        {
        //ROC Volume
        Indicator = Ref(ROC(Volume,lb),-1);
        INDICATOR = IIf(ascdec == 1, indicator, -indicator);

        }

        if(Cases == 4)
        {
        //CRSI
        Indicator = ConnorsRSI(paramLenRSI,paramLenUD,paramLenRank);
        INDICATOR = IIf(ascdec == 1, indicator, -indicator);

        }

        if(Cases == 5)
        {
        //Z Score
        mb = MA(C,lb+1);
        Indicator = Ref((C - mb) / (StDev(C,lb+1)),-1);
        INDICATOR = IIf(ascdec == 1, indicator, -indicator);

        }

        if(Cases == 6)
        {
        //LTI
        Ltilb = 10; // check
        Indicator = Ref(ROC(EMA(Close,ltilb),lb) + ROC(EMA(Close,ltilb*2),lb) + ROC(EMA(Close,ltilb*3),lb),-1);
        INDICATOR = IIf(ascdec == 1, indicator, -indicator);

        }

        if(Cases == 7)
        {
        //RSI Price
        Indicator = Ref(RSIa(Close,14),-1);
        INDICATOR = IIf(ascdec == 1, indicator, -indicator);

        }

        if(Cases == 8)
        {
        //RSI Volume
        Indicator = Ref(RSIa(Volume,14),-1);
        INDICATOR = IIf(ascdec == 1, indicator, -indicator);

        }

        if(Cases == 9)
        {
        // ROC MA 
        Indicator = Ref(ROC(MA(Close,lb),lb),-1);
        INDICATOR = IIf(ascdec == 1, indicator, -indicator);

        }

        if(Cases == 10)
        {
        // ROC Price PR 
        Indicator = Ref(PercentRank(ROC(Close,lb),100),-1);
        INDICATOR = IIf(ascdec == 1, indicator, -indicator);

        }

        if(Cases == 11)
        {
        // PIR = Stoch K
        Indicator = Ref(StochK(14),-1);
        INDICATOR = IIf(ascdec == 1, indicator, -indicator);

        }

        if(Cases == 12)
        {
        // Stoch D
        Indicator = Ref(StochD(14,3,3),-1);
        INDICATOR = IIf(ascdec == 1, indicator, -indicator);

        }

        if(Cases == 13)
        {
        // ATR/C
        Indicator = Ref(ATR(vp)/Close,-1)*100;
        INDICATOR = IIf(ascdec == 1, indicator, -indicator);

        }

        if(Cases == 14)
        {
        // STDEV.P
        Indicator = Ref(StDev(ROC(Close,lb),100,True),-1);
        INDICATOR = IIf(ascdec == 1, indicator, -indicator);

        }

        if(Cases == 15)
        {
        // Beta
        Periods = Param("period",8,1,50,1);
        ticker = ParamStr( "Ticker", "$NIFTY-NSE" );
        P = Foreign(TICKER,"C",lb);
        Indicator = (( Periods * Sum(ROC( C,lb) * ROC(P,lb),Periods )) - (Sum(ROC(C,lb),Periods) * Sum(ROC( P,lb),Periods))) / ((Periods * Sum((ROC(P,lb)^2 ),Periods)) - (Sum(ROC(P,lb ),Periods)^2 ));
        INDICATOR = IIf(ascdec == 1, Indicator, -Indicator);

        }

        if(Cases == 16)
        {
        // ABS ROC
        Indicator = Ref(abs(ROC(Close,lb)),-1);
        INDICATOR = IIf(ascdec == 1, indicator, -indicator);

        }

        if(Cases == 17)
        {
        // PR ABS ROC
        Indicator = Ref(PercentRank(abs(ROC(Close,lb)),100),-1);
        INDICATOR = IIf(ascdec == 1, indicator, -indicator);

        }


        if(Cases == 18)
        {
        // Vol PIR
        Indicator = Ref((Volume - LLV(Volume,14)) / (HHV(Volume,14) - LLV(Volume,14)) ,-1)*100;
        INDICATOR = IIf(ascdec == 1, indicator, -indicator);

        }

        if(Cases == 19)
        {
        // Vol PR
        Indicator = Ref(PercentRank(Volume,100),-1); 
        INDICATOR = IIf(ascdec == 1, indicator, -indicator);

        }

        if(Cases == 20)
        {
        // Close PR
        Indicator = Ref(PercentRank(Close,100),-1); 
        INDICATOR = IIf(ascdec == 1, indicator, -indicator);

        }

        if(Cases == 21)
        {
        //Volume Z Score
        mb = MA(Volume,lb+1);
        Indicator = Ref((Volume - mb) / (StDev(Volume,lb+1)),-1);
        INDICATOR = IIf(ascdec == 1, indicator, -indicator);

        }

        if(Cases == 22)
        {
        //MACD
        r1 = Param( "Fast avg", 12, 2, 200, 1 );
        r2 = Param( "Slow avg", 26, 2, 200, 1 );
        r3 = Param( "Signal avg", 9, 2, 200, 1 ); 

        m1=MACD(r1,r2);
        s1=Signal(r1,r2,r3);
        //a=Cross(m1,s1);

        Indicator = Ref(PercentRank(s1,100),-1); 
        INDICATOR = IIf(ascdec == 1, indicator, -indicator);

        }

        if(Cases == 23)
        {
        //MFI - Similar to RSI but consideres Volume and Price
        Indicator = Ref(MFI(lb),-1);
        INDICATOR = IIf(ascdec == 1, indicator, -indicator);

        }

        if(Cases == 24)
        {
        // MA ATR/C
        Indicator = Ref(MA(ATR(vp)/Close,lb),-1)*100; 
        INDICATOR = IIf(ascdec == 1, indicator, -indicator);

        }


        watchlist = 0;

        List = CategoryGetSymbols(categoryWatchlist,watchlist);

        if ( Status("stocknum") == 0 ) // Generate ranking when we are on the very first symbol
        {
          StaticVarRemove( "values*" );

          for ( n = 0; ( Symbol = StrExtract( List, n ) )  != "";  n++    )
          {
            SetForeign ( symbol );

            #include <includeok.afl>  

            if(Cases == 1)
            {
            //ATRPR
            Indicator = Ref(PercentRank(ATR(vp),100),-1);
            INDICATOR = IIf(ascdec == 1, indicator, -indicator);

            }

            if(Cases == 2)
            {
            //ROC Price
            Indicator = Ref(ROC(Close,lb),-1);
            INDICATOR = IIf(ascdec == 1, indicator, -indicator);

            }

            if(Cases == 3)
            {
            //ROC Volume
            Indicator = Ref(ROC(Volume,lb),-1);
            INDICATOR = IIf(ascdec == 1, indicator, -indicator);

            }

            if(Cases == 4)
            {
            //CRSI
            Indicator = ConnorsRSI(paramLenRSI,paramLenUD,paramLenRank);
            INDICATOR = IIf(ascdec == 1, indicator, -indicator);

            }

            if(Cases == 5)
            {
            //Z Score
            mb = MA(C,lb+1);
            Indicator = Ref((C - mb) / (StDev(C,lb+1)),-1);
            INDICATOR = IIf(ascdec == 1, indicator, -indicator);

            }

            if(Cases == 6)
            {
            //LTI
            Ltilb = 10; 
            Indicator = Ref(ROC(EMA(Close,ltilb),lb) + ROC(EMA(Close,ltilb*2),lb) + ROC(EMA(Close,ltilb*3),lb),-1);
            INDICATOR = IIf(ascdec == 1, indicator, -indicator);

            }

            if(Cases == 7)
            {
            //RSI Price
            Indicator = Ref(RSIa(Close,14),-1);
            INDICATOR = IIf(ascdec == 1, indicator, -indicator);

            }

            if(Cases == 8)
            {
            //RSI Volume
            Indicator = Ref(RSIa(Volume,14),-1);
            INDICATOR = IIf(ascdec == 1, indicator, -indicator);

            }

            if(Cases == 9)
            {
            // ROC MA 
            Indicator = Ref(ROC(MA(Close,lb),lb),-1);
            INDICATOR = IIf(ascdec == 1, indicator, -indicator);

            }

            if(Cases == 10)
            {
            // ROC Price PR 
            Indicator = Ref(PercentRank(ROC(Close,lb),100),-1);
            INDICATOR = IIf(ascdec == 1, indicator, -indicator);

            }

            if(Cases == 11)
            {
            // PIR = Stoch K
            Indicator = Ref(StochK(14),-1);
            INDICATOR = IIf(ascdec == 1, indicator, -indicator);

            }

            if(Cases == 12)
            {
            // Stoch D
            Indicator = Ref(StochD(14,3,3),-1);
            INDICATOR = IIf(ascdec == 1, indicator, -indicator);

            }

            if(Cases == 13)
            {
            // ATR/C
            Indicator = Ref(ATR(vp)/Close,-1)*100;
            INDICATOR = IIf(ascdec == 1, indicator, -indicator);

            }

            if(Cases == 14)
            {
            // STDEV.P
            Indicator = Ref(StDev(ROC(Close,lb),100,True),-1);
            INDICATOR = IIf(ascdec == 1, indicator, -indicator);

            }

            if(Cases == 15)
            {
            // Beta
            Periods = Param("period",8,1,50,1);
            ticker = ParamStr( "Ticker", "$NIFTY-NSE" );
            P = Foreign(TICKER,"C",lb);
            Indicator = (( Periods * Sum(ROC( C,lb) * ROC(P,lb),Periods )) - (Sum(ROC(C,lb),Periods) * Sum(ROC( P,lb),Periods))) / ((Periods * Sum((ROC(P,lb)^2 ),Periods)) - (Sum(ROC(P,lb ),Periods)^2 ));
            INDICATOR = IIf(ascdec == 1, Indicator, -Indicator);

            }

            if(Cases == 16)
            {
            // ABS ROC
            Indicator = Ref(abs(ROC(Close,lb)),-1);
            INDICATOR = IIf(ascdec == 1, indicator, -indicator);

            }

            if(Cases == 17)
            {
            // PR ABS ROC
            Indicator = Ref(PercentRank(abs(ROC(Close,lb)),100),-1);
            INDICATOR = IIf(ascdec == 1, indicator, -indicator);

            }


            if(Cases == 18)
            {
            // Vol PIR
            Indicator = Ref((Volume - LLV(Volume,14)) / (HHV(Volume,14) - LLV(Volume,14)) ,-1)*100;
            INDICATOR = IIf(ascdec == 1, indicator, -indicator);

            }

            if(Cases == 19)
            {
            // Vol PR
            Indicator = Ref(PercentRank(Volume,100),-1); // check
            INDICATOR = IIf(ascdec == 1, indicator, -indicator);

            }

            if(Cases == 20)
            {
            // Close PR
            Indicator = Ref(PercentRank(Close,100),-1); // check
            INDICATOR = IIf(ascdec == 1, indicator, -indicator);

            }

            if(Cases == 21)
            {
            //Volume Z Score
            mb = MA(Volume,lb+1);
            Indicator = Ref((Volume - mb) / (StDev(Volume,lb+1)),-1);
            INDICATOR = IIf(ascdec == 1, indicator, -indicator);

            }

            if(Cases == 22)
            {
            //MACD
            r1 = Param( "Fast avg", 12, 2, 200, 1 );
            r2 = Param( "Slow avg", 26, 2, 200, 1 );
            r3 = Param( "Signal avg", 9, 2, 200, 1 );

            m1=MACD(r1,r2);
            s1=Signal(r1,r2,r3); 
            //a=Cross(m1,s1);

            Indicator = Ref(PercentRank(s1,100),-1); 
            INDICATOR = IIf(ascdec == 1, indicator, -indicator);

            }

            if(Cases == 23)
            {
            //MFI - Similar to RSI but consideres Volume and Price
            Indicator = Ref(MFI(lb),-1);
            INDICATOR = IIf(ascdec == 1, indicator, -indicator);

            }

            if(Cases == 24)
            {
            // MA ATR/C
            Indicator = Ref(MA(ATR(vp)/Close,lb),-1)*100; 
            INDICATOR = IIf(ascdec == 1, indicator, -indicator);

            }

                values = IIf( includeok , Indicator , Null);

            RestorePriceArrays();
            StaticVarSet (  "values"  +  symbol, values );


            _TRACE( symbol );
             }

          StaticVarGenerateRanks( "rank", "values", 0, 1234 );

        }


        symbol = Name();
        values = StaticVarGet ( "values" +  symbol );
        rank = StaticVarGet ( "rankvalues" +  symbol );



        poi = Ref(Close,-1);
        edist = Ref(ATR(vp),-1)*ef;


        strig = poi + edist;
        strade = H >= strig;



        //fdw = DayOfWeek() < Ref(DayOfWeek(),-1);

        Short = rank >= minrank AND Rank <= maxrank AND includeok /*AND Fdw !=1 */AND Strade ;
        ShortPrice = IIf(Max(Open,strig) == Open,Open,strig);

        /*
        pt = 3;//Optimize("pt",2,2,6,1);;
        slpts = Ref(Close,-1)*pt/100;
        stprc = Ref(Close,-1)+ slpts;
        */
        //PositionScore = Random(); 

        sp = 6;
        atrstp = Ref(ATR(1),-1)*sp/10;
        stopprice = ShortPrice+atrstp;

        Cover = Short;
        CoverPrice = IIf(H >= stopprice, stopprice, Close);


        //ApplyStop(stopTypeLoss,stopModePercent,pt);

        Filter = includeok;
        AddColumn(Rank,"Rank");
        AddColumn(Values,"Values");
        AddColumn(Close,"Close");
        AddColumn(indicator,"indicator");
        AddColumn((Close/Open-1)*100,"Price Change");


## BASIC BACKTEST ON F&O EQUITIES

        maxpos = 10; //Optimize("mp",10,1,10,1);

        SetOption("MaxOpenPositions",maxpos);
        SetOption("InitialEquity",10000000);
        SetOption("AccountMargin",100/1);
        SetPositionSize(100/maxpos*1,spsPercentOfEquity);
        SetTradeDelays(0,0,0,0);
        //SetOption("PriceBoundChecking",False);

        dayx = 1; //Optimize("dayx",1,1,5,1);

        ef = Optimize("f",0.1,0,0.5,0.1);
        xf = 0; //Optimize("f",0.2,0,0.5,0.1);
        vp = Optimize("vp",1,1,15,1);
        rlb = 1; //Optimize("rlb",1,1,5,1);

        paramLenRSI = Param("RSI Closes Length", 3, 2, 100, 1);
        paramLenUD = Param("RSI UpClose Length", 2, 2, 100, 1);
        paramLenRank = Param("PerecentRank Length", 100, 10, 200, 1);

        function ConnorsRSI(lenRSI, lenUD, lenROC)
        {
              upDays = BarsSince(C <= Ref(C,-1));
              downDays = BarsSince(C >= Ref(C,-1));
              updownDays = IIf(upDays > 0, upDays, IIf(downDays > 0, -downDays, 0));
              crsi = ( PercentRank(ROC(C,1), lenROC) + RSIa(updownDays,lenUD) +RSI(lenRSI))/3;
              return crsi;
        }

        factor = 1; //Optimize("factor",1,1,3,0.5);

        stop = 3; //Optimize("stop",1,2,5,1);

        r = 1; //Optimize("r",1,1,100,1);

        watchlist = 0;

        List = CategoryGetSymbols(categoryWatchlist,watchlist);

        if ( Status("stocknum") == 0 ) // Generate ranking when we are on the very first symbol
        {
          StaticVarRemove( "values*" );

          for ( n = 0; ( Symbol = StrExtract( List, n ) )  != "";  n++    )
          {
            SetForeign ( symbol );
            {
              #include <includeok.afl>
            }
            crsi = ConnorsRSI(3,2,100);
            values = IIf(includeOK AND Ref(Volume,-1) > (Ref(MA(Volume,50),-1) * factor) AND Ref(C,-1) > Ref(C,-2) , /*Ref(ROC(C,rlb),-1) Ref(PercentRank(ATR(vp),100),-1)*/ Ref(crsi,-1) , Null);
            RestorePriceArrays();
            StaticVarSet (  "values"  +  symbol, values );
            _TRACE( symbol );
            }

          StaticVarGenerateRanks( "rank", "values", 0, 1234 );
        }

        symbol = Name();
        values = StaticVarGet ( "values" +  symbol );
        rank = StaticVarGet ( "rankvalues" +  symbol );

        {
          #include <includeok.afl>
        }

        poi = Ref(C,-1);
        edist = Ref(ATR(vp),-1) * ef;
        xdist = Ref(ATR(vp),-1) * xf;

        strig = poi + edist;
        ctrig = poi - xdist;

        strade = H >= strig;
        rankOK = rank <= 10;

        ctrade = L <= ctrig;

        upday = Ref(Volume,-1) > (Ref(MA(Volume,50),-1) * factor) AND Ref(C,-1) > Ref(C,-2);

        Short = strade AND rankOK AND includeOK AND upday;// AND DayOfWeek() != dayx;
        ShortPrice = IIf(Max(Open,strig) == Open , Open * 1 , strig);

        Cover = Short;
        CoverPrice = C * 1;

        //ApplyStop(stopTypeLoss,stopModePercent,stop);

        PositionScore = Random();

        Filter = includeOK;
        AddColumn(rank,"rank");
        AddColumn(values,"values");
        //AddColumn(PercentRank(ATR(vp),100),"atrpr");
        //AddColumn(C,"Eq");
