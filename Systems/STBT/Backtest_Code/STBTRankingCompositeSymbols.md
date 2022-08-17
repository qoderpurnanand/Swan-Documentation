## STBTRankingCompositeSymbols
	afl = "stst";
	maxrank =  10;
	watchlist = 0;
	addtime = 459;

	List = CategoryGetSymbols(categoryWatchlist,watchlist);

	if ( Status("stocknum") == 0)
	{


	StaticVarRemove(afl +  "values*" );
	StaticVarRemove( "Rank" + afl + "values*" );

	for ( n = 0; ( Sym = StrExtract( List, n ) )  != "";  n++    )
	{


		SetForeign (Sym);
		#include<F&O includeok.afl>	
		#include<F&O Banlist.afl>
		Gap = (Close/TimeFrameGetPrice("O",inDaily)-1)*100;

		values = IIf(includeok AND Gap < 0 AND excludeok == 0, 10000-Gap, -100);



		RestorePriceArrays();
		StaticVarSet ( afl + "values"  +  sym, values );

		_TRACE( sym );
	}

	StaticVarGenerateRanks( "rank", afl + "values", 0, 1234 );

	}


	sym = Name();

	TimeFrameSet(inDaily);
	fdw = DayOfWeek() < Ref(DayOfWeek(),-1);
	TimeFrameRestore();
	fdw = TimeFrameExpand(fdw,inDaily,expandFirst);

	#include<F&O includeok.afl>
	#include<F&O Banlist.afl>

	gapper = 3;
	Gap = (Close/TimeFrameGetPrice("O",inDaily)-1)*100;
	values =  StaticVarGet(afl + "values"  +  sym);
	rank = StaticVarGet("rank" + afl + "values"+sym);
	rankok = IIf(rank <= 10 AND includeok AND excludeok == 0, Gap,-100);
	AddToComposite(rankok,"~~STSTgapall" + name(),"C",atcFlagResetValues);

	Filter = TimeNum() == 110000; 
	AddColumn( Rankok,"rankok");
	AddColumn( includeok,"includeok");
	AddColumn( excludeok,"excludeok");
	AddColumn( Gap,"Gap");
	AddColumn(TimeFrameGetPrice("O",inDaily), "Dailyopen");
	AddColumn(Close,"Close");
	AddColumn(values,"values");
	AddColumn(rank,"rank");
