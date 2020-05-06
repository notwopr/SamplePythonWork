"""
Title: Update Data Bot
Date Started: June 26, 2019
Version: 4.1
Version Date: Dec 11, 2019
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied without the express written consent of David Hyongsik Choi.
Purpose: List of functions needed to run to update data.
"""

# IMPORT TOOLS
#   STANDARD LIBRARY IMPORTS
import pickle as pkl
import os
#   THIRD PARTY IMPORTS
#   LOCAL APPLICATION IMPORTS
from computersettings import BOT_DUMP
from filetests import checknum
from filelocations import delete_create_folder
from UPDATEPRICEDATA_BASE import store_allprices
from UPDATEPRICEDATA_BASE_TICKER import storealltickers
from UPDATEPRICEDATA_BASE_DATERANGES import create_daterangedb
from UPDATEPRICEDATA_BASE_PRICEMATRIX import allprice_matrix
from UPDATEPRICEDATA_BASE_FULLINFOTICKERDATABASE import create_fullinfotickerdatabase


'''DEFINE FOLDER STRUCTURE'''
PRICES = BOT_DUMP / "prices"
STOCKPRICES = PRICES / "stockprices"
INDEXPRICES = PRICES / "indexprices"
TICKERS = BOT_DUMP / "tickers"
DATES = BOT_DUMP / "dates"
DATE_DUMP = DATES / 'dump'
DATE_RESULTS = DATES / 'results'
FULL_INFO_DB = BOT_DUMP / 'fullinfodb'
folder_index = [
    PRICES,
    STOCKPRICES,
    INDEXPRICES,
    TICKERS,
    DATES,
    DATE_DUMP,
    DATE_RESULTS,
    FULL_INFO_DB
]

# SET FILENAMES
tickerlistall_name = 'tickerlist_all'
tickerlistcommon_name = 'tickerlist_common'
daterangedb_name = 'daterangedb'
tickerlistall_source = TICKERS / f'{tickerlistall_name}.pkl'
tickerlistcommon_source = TICKERS / f'{tickerlistcommon_name}.pkl'
tickerlistall_source_csv = TICKERS / f'{tickerlistall_name}.csv'
tickerlistcommon_source_csv = TICKERS / f'{tickerlistcommon_name}.csv'
daterangedb_source = DATE_RESULTS / f'{daterangedb_name}.pkl'
alltickerfiles = [
    tickerlistall_source,
    tickerlistcommon_source,
    tickerlistall_source_csv,
    tickerlistcommon_source_csv
]

if __name__ == '__main__':

    '''CREATE DUMP FOLDERS IF NON-EXISTENT'''
    for folder in folder_index:
        delete_create_folder(folder)

    '''BENCHMARK DOWNLOAD (INDEPENDENT)'''
    store_allprices(INDEXPRICES, '', "benchmark")

    # WAIT FOR ALL FILES TO DOWNLOAD
    benchfilecount = checknum(INDEXPRICES, 3, '')
    while benchfilecount is False:
        benchfilecount = checknum(INDEXPRICES, 3, '')

    '''TICKERLIST DOWNLOAD'''
    storealltickers(TICKERS, tickerlistall_name, tickerlistcommon_name)

    '''STOCKPRICE DOWNLOAD (DEPENDENT ON TICKERLIST DOWNLOAD)'''
    # WAIT UNTIL TICKERLIST FILES EXIST
    for fileloc in alltickerfiles:
        tlistexist = os.path.isfile(fileloc)
        while tlistexist is False:
            tlistexist = os.path.isfile(fileloc)

    # DOWNLOAD STOCK PRICES
    store_allprices(STOCKPRICES, tickerlistall_source, "")

    # WAIT FOR ALL FILES TO DOWNLOAD
    with open(tickerlistall_source, "rb") as targetfile:
        masterlist = pkl.load(targetfile)
    correct = len(masterlist['symbol'])
    downloadfinish = checknum(STOCKPRICES, correct, '')
    while downloadfinish is False:
        downloadfinish = checknum(STOCKPRICES, correct, '')

    '''EARLIEST DATE DATABASE (DEPENDENT ON STOCK PRICE DOWNLOAD)'''
    create_daterangedb(DATE_DUMP, tickerlistall_source, STOCKPRICES, DATE_RESULTS, daterangedb_name)

    '''CREATE PRICE HISTORY MATRIX (DEPENDENT ON STOCK PRICE DOWNLOAD)'''
    allprice_matrix(daterangedb_source, tickerlistall_source, STOCKPRICES, PRICES)
    allprice_matrix(daterangedb_source, tickerlistcommon_source, STOCKPRICES, PRICES)
    allprice_matrix(daterangedb_source, 'faang', STOCKPRICES, PRICES)
    allprice_matrix(daterangedb_source, 'bench', INDEXPRICES, PRICES)

    '''CREATE FULL INFO DATABASE'''
    create_fullinfotickerdatabase(tickerlistcommon_source, tickerlistall_source, daterangedb_source, FULL_INFO_DB)
