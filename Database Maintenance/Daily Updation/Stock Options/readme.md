# STOCK OPTIONS DAILY UPDATION

## PROCESS :

### Download csv file from Dropbox
1. Everyday we get a dropbox folder link from GDFL (noreply1@globaldatafeeds.in) for F&O 1-min data. 
2. Copy and paste this link in the [DownloadFileFromDropbox](https://github.com/qodeinvestments/Swan-Documentation/blob/main/Database%20Maintenance/Daily%20Updation/Stock%20Options/DownloadFileFromDropbox.ipynb) code as zip_file_url to download the csv file to common drive. 

### Upload csv file to sql database
1. Start the sql database.
2. To upload today's file to the sql database run [DailyUpdateRawDatabase](https://github.com/qodeinvestments/Swan-Documentation/blob/main/Database%20Maintenance/Daily%20Updation/Stock%20Options/DailyUpdateRawDatabase.ipynb) code keeping date = date.today(). 
3. If you want to upload file for the specific date you can mention that date as well. 
4. Check on DBeaver whether data is uploaded correctly or not.

### Update stock options data
1. Start the sql database.
2. To create today's stock options data run [DailyUpdateStockOptions](https://github.com/qodeinvestments/Swan-Documentation/blob/main/Database%20Maintenance/Daily%20Updation/Stock%20Options/DailyUpdateStockOptions.ipynb) code keeping date = date.today().
3. If you want to create data for the specific range of dates you can mention the start and end date as well.
4. [DailyUpdateStockOptions](https://github.com/qodeinvestments/Swan-Documentation/blob/main/Database%20Maintenance/Daily%20Updation/Stock%20Options/DailyUpdateStockOptions.ipynb) code will fetch the raw GDFL file from sql database for the specific date. 
5. It will create symbolwise files and then segregate ticker to create a labelled data.
6. This labelled data will be split into current month, next month and far month contracts.
7. Continuous contracts will be then appended to the historical stock options data which is stored on external hard drive.
8. Go through the corporate actions for that day and if there are any adjustments perfrom them individually on that specific stock.
