"""
Title: Update Price Data Base_Dates
Date Started: Sept 17, 2019
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied
    without the express written consent of David Hyongsik Choi.
Purpose: The purpose of the Date Range Bot is to retrieve the earliest and latest available trade dates of a given stock.  Another function is to create a database of those dates.
"""

# IMPORT TOOLS
#   STANDARD LIBRARY IMPORTS
import pickle as pkl
from functools import partial
from multiprocessing import Pool
#   THIRD PARTY IMPORTS
import pandas as pd
#   LOCAL APPLICATION IMPORTS
from filelocations import delete_create_folder, savetopkl
from computersettings import use_cores, chunksize
from filetests import checknum


# GRAB SINGLE STOCK/INDEX PRICE HISTORY DATAFRAME
def grabsinglehistory(indexpricefolder, stockpricefolder, symbol):

    # SYNTAX CORRECTION
    if symbol in ["^DJI", "^INX", "^IXIC"]:
        symbol = symbol[1:] + "_prices"
        targetfolder = indexpricefolder
    else:
        symbol = symbol + "_prices"
        targetfolder = stockpricefolder

    with open(targetfolder / "{}.pkl".format(symbol), "rb") as targetfile:
        prices = pkl.load(targetfile)

    return prices


# STORE A SINGLE STOCK'S DATE RANGE TO FILE
def get_daterange(indexpricefolder, stockpricefolder, datedumpfolder, stock):

    # OPEN UP PRICE HISTORY OF THE STOCK
    stock_prices = grabsinglehistory(indexpricefolder, stockpricefolder, stock)

    # STORE DATES
    first_date = str(stock_prices.iat[0, 0])
    last_date = str(stock_prices.iat[-1, 0])

    # SAVE NAME AND FIRST DATE TO FILE
    summary = {'stock': stock, 'first_date': first_date, 'last_date': last_date}
    with open(datedumpfolder / "daterange-{}.pkl".format(stock), "wb") as targetfile:
        pkl.dump(summary, targetfile, protocol=4)


# CREATES DATABASE OF THE EARLIEST TRADE DATES OF ALL US NASDAQ AND NYSE STOCKS
def create_daterangedb(datedumpfolder, tickerlistsource, indexpricefolder, stockpricefolder, destfolder, daterangedb_name):

    # DELETE AND DESTINATION FOLDER
    delete_create_folder(destfolder)

    # OPEN TICKER LIST FILE AND STORE TICKER LIST TO OBJECT
    with open(tickerlistsource, "rb") as targetfile:
        tickerlistdf = pkl.load(targetfile)
    tickerlist = tickerlistdf['symbol'].tolist()

    # RUN MULTIPROCESSOR DOWNLOAD OF DATE RANGES
    pool = Pool(processes=use_cores)
    fn = partial(get_daterange, indexpricefolder, stockpricefolder, datedumpfolder)
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
    with open(tickerlistsource, "rb") as targetfile:
        masterlist = pkl.load(targetfile)
    if len(table_results) != len(masterlist['symbol']):
        print("The number of date ranges listed does not match the number of available tickers.  Program exiting...no date range database has been created.  Please fix.")
        exit()

    # ARCHIVE FILE
    savetopkl(daterangedb_name, destfolder, daterangedf)
    daterangedf.to_csv(index=False, path_or_buf=destfolder / '{}.csv'.format(daterangedb_name))
