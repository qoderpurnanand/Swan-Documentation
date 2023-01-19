# STOCK OPTIONS DAILY UPDATION

## PROCESS :

### Download csv file from Dropbox
1. Everyday we get a dropbox link from GDFL (noreply1@globaldatafeeds.in) for F&O 1-min data. 
2. Copy and paste this link in the [DownloadFileFromDropbox](https://github.com/qodeinvestments/Swan-Documentation/blob/main/Database%20Maintenance/Daily%20Updation/Stock%20Options/DownloadFileFromDropbox.ipynb) code as zip_file_url to download the csv file to common drive. 

### Upload csv file to sql database
1. Start the sql database.
2. To upload today's file to the sql database run [DailyUpdateRawDatabase](https://github.com/qodeinvestments/Swan-Documentation/blob/main/Database%20Maintenance/Daily%20Updation/Stock%20Options/DailyUpdateRawDatabase.ipynb) keeping date = date.today(). 
3. If you want to upload file for the specific date you can mention that date as well. 
4. Check on DBeaver whether data is uploaded correctly or not.

### Update stock options data
1. Start the sql database.
2. 
