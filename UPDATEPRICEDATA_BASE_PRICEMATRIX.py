"""
Title: Price Matrix
Date Started: Nov 9, 2019
Version: 1.1
Vers. Start: Nov 10, 2019
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied without the express written consent of David Hyongsik Choi.
Purpose: Create one dataframe for all stock price histories available.
"""

# IMPORT TOOLS
#   STANDARD LIBRARY IMPORTS
import datetime as dt
import pickle as pkl
import os
#   THIRD PARTY IMPORTS
import pandas as pd
import numpy as np
#   LOCAL APPLICATION IMPORTS
from filelocations import savetopkl, readpkl


# CREATE MATRIX OF ALL PRICE HISTORIES OF ALL STOCKS
def allprice_matrix(datesource, tickersource, pricedatafolder, destfolder):

    # FIND EARLIEST AND LATEST DATE AVAILABLE
    with open(datesource, "rb") as targetfile:
        daterangedb = pkl.load(targetfile)
    lastdate_dateobj = daterangedb['last_date'].apply(lambda x: dt.date.fromisoformat(x))
    lastdates = lastdate_dateobj.tolist()
    latestdate = str(np.max(lastdates))
    firstdate_dateobj = daterangedb['first_date'].apply(lambda x: dt.date.fromisoformat(x))
    firstdates = firstdate_dateobj.tolist()
    firstdate = str(np.min(firstdates))

    # CREATE MASTER DATAFRAME
    dates = pd.date_range(firstdate, latestdate)
    mdf = pd.DataFrame(dates)
    mdf = mdf.rename(columns={0: "___Date___"})

    # MAKE MASTER DATA FRAME DATE COLUMN DATETIME OBJECT
    mdf["___Date___"] = pd.to_datetime(mdf["___Date___"])
    mdf["___Date___"] = mdf["___Date___"].apply(dt.datetime.date)

    # GET TICKERLIST
    if type(tickersource) == list:
        tickerlist = tickersource
        filename = "allpricematrix_custom"
    elif tickersource == 'bench':
        tickerlist = ["DJI", "INX", "IXIC"]
        filename = "allpricematrix_bench"
    elif tickersource == 'faang':
        tickerlist = ["NFLX", "AMZN", "AAPL", "FB", "GOOGL"]
        filename = "allpricematrix_faang"
    elif (os.path.split(tickersource)[1])[0:11] == 'tickerlist_':
        tickersourcefilename = os.path.split(tickersource)[1]
        suffix = tickersourcefilename[11:-4]
        with open(tickersource, "rb") as targetfile:
            tickerlistdf = pkl.load(targetfile)
        tickerlist = tickerlistdf['symbol'].tolist()
        filename = "allpricematrix_" + suffix

    # COMBINE STOCK PRICE HISTORIES TOGETHER
    for stock in tickerlist:
        symbol = stock + "_prices"
        stock_price_history = readpkl(symbol, pricedatafolder)
        mdf = mdf.join(stock_price_history.set_index("date"), how="left", on="___Date___")

    # FILL FORWARD THEN BACKWARDS THE EMPTY PRICE SPACES
    mdf = mdf.fillna(method='ffill')
    mdf = mdf.fillna(method='bfill')

    # RESET INDEX
    mdf.sort_values(ascending=True, by=['___Date___'], inplace=True)
    mdf.reset_index(drop=True, inplace=True)

    # ARCHIVE TO FILE
    savetopkl(filename, destfolder, mdf)
