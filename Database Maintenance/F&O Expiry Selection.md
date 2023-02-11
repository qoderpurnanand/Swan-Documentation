## F&O Expiry Selection

    TimeFrameSet(inDaily);

    {
    Expirydates = (datenum()==1130131 OR
    datenum()==1130228 OR
    datenum()==1130328 OR
    datenum()==1130425 OR
    datenum()==1130530 OR
    datenum()==1130627 OR
    datenum()==1130725 OR
    datenum()==1130829 OR
    datenum()==1130926 OR
    datenum()==1131031 OR
    datenum()==1131128 OR
    datenum()==1131226 OR
    datenum()==1140130 OR
    datenum()==1140226 OR
    datenum()==1140327 OR
    datenum()==1140424 OR
    datenum()==1140529 OR
    datenum()==1140626 OR
    datenum()==1140731 OR
    datenum()==1140828 OR
    datenum()==1140925 OR
    datenum()==1141030 OR
    datenum()==1141127 OR
    datenum()==1141224 OR
    datenum()==1150129 OR
    datenum()==1150226 OR
    datenum()==1150326 OR
    datenum()==1150430 OR
    datenum()==1150528 OR
    datenum()==1150625 OR
    datenum()==1150730 OR
    datenum()==1150827 OR
    datenum()==1150924 OR
    datenum()==1151029 OR
    datenum()==1151126 OR
    datenum()==1151231 OR
    datenum()==1160128 OR
    datenum()==1160225 OR
    datenum()==1160331 OR
    datenum()==1160428 OR
    datenum()==1160526 OR
    datenum()==1160630 OR
    datenum()==1160728 OR
    datenum()==1160825 OR
    datenum()==1160929 OR
    datenum()==1161027 OR
    datenum()==1161124 OR
    datenum()==1161229 OR
    datenum()==1170125 OR
    datenum()==1170223 OR
    datenum()==1170330 OR
    datenum()==1170427 OR
    datenum()==1170525 OR
    datenum()==1170629 OR
    datenum()==1170727 OR
    datenum()==1170831 OR
    datenum()==1170928 OR
    datenum()==1171026 OR
    datenum()==1171130 OR
    datenum()==1171228 OR
    datenum()==1180125 OR
    datenum()==1180222 OR
    datenum()==1180328 OR
    datenum()==1180426 OR
    datenum()==1180531 OR
    datenum()==1180628 OR
    datenum()==1180726 OR
    datenum()==1180830 OR
    datenum()==1180927 OR
    datenum()==1181025 OR
    datenum()==1181129 OR
    datenum()==1181227 OR
    datenum()==1190131 OR
    datenum()==1190228 OR
    datenum()==1190328 OR
    datenum()==1190425 OR
    datenum()==1190530 OR
    datenum()==1190627 OR
    datenum()==1190725 OR
    datenum()==1190829 OR
    datenum()==1190926 OR
    datenum()==1191031 OR
    datenum()==1191128 OR
    datenum()==1191226 OR
    datenum()==1200130 OR
    datenum()==1200227 OR
    datenum()==1200326 OR
    datenum()==1200430 OR
    datenum()==1200528 OR
    datenum()==1200625 OR
    datenum()==1200730 OR
    DateNum()==1200827 OR
    DateNum()==1200924 OR
    DateNum()==1201029 OR
    DateNum()==1201126 OR
    DateNum()==1201230 OR
    DateNum()==1210128 OR
    DateNum()==1210225 OR
    DateNum()==1210325 OR
    DateNum()==1210429 OR
    Datenum()==1210527 OR 
    Datenum()==1210624 OR 
    Datenum()==1210729 OR 
    Datenum()==1210826 OR 
    Datenum()==1210930 OR 
    Datenum()==1211028 OR 
    Datenum()==1211125 OR 
    Datenum()==1211230 OR 
    Datenum()==1220127 OR 
    Datenum()==1220224 OR 
    Datenum()==1220331 OR 
    Datenum()==1220428 OR 
    Datenum()==1220526 OR 
    Datenum()==1220630 OR 
    Datenum()==1220728 OR 
    Datenum()==1220825 OR 
    Datenum()==1220929 OR 
    Datenum()==1221027 OR 
    Datenum()==1221124 OR 
    Datenum()==1221229 OR
    Datenum()==1230125 OR
    Datenum()==1230223  );
    }

    sym = Strright(Name(),  4 );
    sym1 = Strright(Name(),  5 );

    day1 = Ref(expirydates,1) AND  expirydates==0;///Today is one day prior to expiry

    Day0 = expirydates == 1;///today is expiry

    dayafterexp = Ref(Expirydates,-1);

    overnight = IIf((day1 OR day0) AND sym1 == ".FUT1",1,IIf(day1==0 AND day0==0 AND sym==".FUT",1,0));////BTST and STBT
    intraday  = iif( day0 AND sym1 ==".FUT1",1,IIf(day0==0 AND sym==".FUT",1,0));///Only on expiry day for SID
    explore = IIf(dayafterexp AND sym1==".FUT1",1,IIf(dayafterexp==0 AND sym==".FUT",1,0));

    TimeFrameRestore();

    Day1 =  TimeFrameExpand(Day1,inDaily,expandFirst);
    Day0 =  TimeFrameExpand(Day0,inDaily,expandFirst);
    Overnight = TimeFrameExpand(overnight,inDaily,expandFirst);
    Intraday = TimeFrameExpand(intraday,inDaily,expandFirst);
