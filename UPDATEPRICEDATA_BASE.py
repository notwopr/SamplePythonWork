"""
Title: Update Price Data Base - Prices
Date Started: June 7, 2019
Version: 1.1
Version Start Date: May 5, 2020
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied without the express written consent of David Hyongsik Choi.
Purpose: The purpose of the All Price Bot is to retrieve the entire price history of a stock.  It will return all days including non-trading days (filled in with previous last closing price).  Allows for the option to fill in the unavailable rows with Nan or the last available price.
Version Notes:
1.1: Cleaned up code.  Added FRED Nasdaq API pull.  Removed startdate and enddate specification.
"""

# IMPORT TOOLS
#   STANDARD LIBRARY IMPORTS
import datetime as dt
import dateutil.parser as dup
import pickle as pkl
from functools import partial
from multiprocessing import Pool
#   THIRD PARTY IMPORTS
import pandas as pd
#   LOCAL APPLICATION IMPORTS
from UPDATEPRICEDATA_FRED import indexpriceretrieval
from UPDATEPRICEDATA_TIINGO import stockpriceretrieval
from computersettings import use_cores, chunksize


# RETRIEVE GIVEN STOCK PRICE HISTORY
def allpricebot(stock, start_date, end_date):

    # RETRIEVE STORED PRICES
    if stock in ["^DJI", "^INX", "^IXIC"]:
        prices = indexpriceretrieval(stock, '', '')
    else:
        prices = stockpriceretrieval(stock, start_date, end_date)

    return prices


# STORE ENTIRE PRICE HISTORY OF A SINGLE GIVEN STOCK TO PICKLE
def download_prices(targetfolder, start, end, symbol):

    try:
        prices = allpricebot(symbol, start, end)
        prices['date'] = prices['date'].apply(dup.parse)
        prices['date'] = prices['date'].apply(dt.datetime.date)
    except (ValueError, KeyError, TypeError):
        dates = pd.date_range(end, end)
        prices = pd.DataFrame(dates)
        prices = prices.rename(columns={0: "date"})
        prices[symbol] = float(0)
        prices["date"] = pd.to_datetime(prices["date"])
        prices["date"] = prices["date"].apply(dt.datetime.date)

    if symbol in ["^DJI", "^INX", "^IXIC"]:
        symbol = symbol[1:]

    # SAVE TO FILE
    with open(targetfolder / "{}_prices.pkl".format(symbol), "wb") as targetfile:
        pkl.dump(prices, targetfile, protocol=4)


# DOWNLOAD ALL STOCK PRICE HISTORIES TO FILES
def store_allprices(destfolder, tickerfile, option):

    # BENCHMARK OR NOT?
    if option == "benchmark":
        symbols = ["^DJI", "^IXIC", "^INX"]
    else:
        with open(tickerfile, "rb") as targetfile:
            tickerlistdf = pkl.load(targetfile)
            symbols = tickerlistdf['symbol'].tolist()

    # SET DATE RANGE
    start = "1962-01-01"
    end = str(dt.date.today())

    # DOWNLOAD
    fn = partial(download_prices, destfolder, start, end)
    pool = Pool(processes=use_cores)
    pool.map(fn, symbols, chunksize)
    pool.close()
    pool.join()
