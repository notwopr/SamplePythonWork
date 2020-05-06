"""
Title: Update Price Data Base_Dates
Date Started: Sept 17, 2019
Version: 1.1
Version Start Date: May 5, 2020
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied
    without the express written consent of David Hyongsik Choi.
Purpose: The purpose of the Date Range Bot is to retrieve the earliest and latest available trade dates of a given stock.  Another function is to create a database of those dates.

Version Notes:
1.1: Update and clean up code.
"""

# IMPORT TOOLS
#   STANDARD LIBRARY IMPORTS
import pickle as pkl
from functools import partial
from multiprocessing import Pool
#   THIRD PARTY IMPORTS
import pandas as pd
#   LOCAL APPLICATION IMPORTS
from filelocations import savetopkl
from computersettings import use_cores, chunksize
from filetests import checknum


# STORE A SINGLE STOCK'S DATE RANGE TO FILE
def get_daterange(stockpricefolder, datedumpfolder, stock):

    with open(stockpricefolder / f"{stock}_prices.pkl", "rb") as targetfile:
        prices = pkl.load(targetfile)

    # STORE DATES
    first_date = str(prices.iat[0, 0])
    last_date = str(prices.iat[-1, 0])

    # SAVE NAME AND FIRST DATE TO FILE
    summary = {'stock': stock, 'first_date': first_date, 'last_date': last_date}
    savetopkl(f"daterange-{stock}.pkl", datedumpfolder, summary)


# CREATES DATABASE OF THE EARLIEST TRADE DATES OF ALL US NASDAQ AND NYSE STOCKS
def create_daterangedb(datedumpfolder, tickerlistsource, stockpricefolder, destfolder, daterangedb_name):

    # OPEN TICKER LIST FILE AND STORE TICKER LIST TO OBJECT
    with open(tickerlistsource, "rb") as targetfile:
        tickerlistdf = pkl.load(targetfile)
    tickerlist = tickerlistdf['symbol'].tolist()

    # RUN MULTIPROCESSOR DOWNLOAD OF DATE RANGES
    pool = Pool(processes=use_cores)
    fn = partial(get_daterange, stockpricefolder, datedumpfolder)
    pool.map(fn, tickerlist, chunksize)
    pool.close()
    pool.join()

    # WAIT FOR ALL FILES TO DOWNLOAD
    correct = len(tickerlist)
    edfinish = checknum(datedumpfolder, correct, '')
    while edfinish is False:
        edfinish = checknum(datedumpfolder, correct, '')

    # ASSEMBLE DATA
    table_results = []
    for child in datedumpfolder.iterdir():
        with open(child, "rb") as targetfile:
            summary = pkl.load(targetfile)
        table_results.append(summary)

    # CONSTRUCT DATAFRAME
    daterangedf = pd.DataFrame(data=table_results)

    # CHECK ACCURACY
    if len(table_results) != len(tickerlist['symbol']):
        print("The number of date ranges listed does not match the number of available tickers.  Program exiting...no date range database has been created.  Please fix.")
        exit()

    # ARCHIVE FILE
    savetopkl(daterangedb_name, destfolder, daterangedf)
    daterangedf.to_csv(index=False, path_or_buf=destfolder / f'{daterangedb_name}.csv')
