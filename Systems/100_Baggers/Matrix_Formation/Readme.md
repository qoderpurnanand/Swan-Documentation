## The file follows the following steps in the given order :

1. Removed Amalgamated Companies
2. Filtered companies which have data for atleast 10 years.</br>
               i} the DataFrame is exported, named as : "**Datapoints_more_than_10.csv**" which is used in further files.
3. Found the Start and End year for data of all companies. 
4. Calculating Bagger Values :</br>
               i}   Market Cap on start_year >= 100</br>
               ii}  Market Cap on end_year >= 100 (i.e. 10th year)</br>
               iii} Market Cap on present_year >= 100</br>
               iv}  Calculating the Bagger value for them (eg. 10x, 15x, etc.)</br>
5. Calculating a Matrix to store the company names according to their Bagger Values and Year wise.
6. Creating another Matrix to store company count according to their Bagger Values and Year wise.

The DataFrame is then exported, named as : "Bagger.csv"which is used in further files.</br>
The final DataFrame is then exported, named as : "**count.csv**".
