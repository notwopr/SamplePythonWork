"""
Title: Ticker Portal
Date Started: April 26, 2019
Version: 3.0
Vers Date: Nov 9, 2019
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied without the express written consent of David Hyongsik Choi.
Purpose: Return list of all NASDAQ/NYSE stocks at a given point in history.
"""

# IMPORT TOOLS
#   STANDARD LIBRARY IMPORTS
import pickle as pkl
#   THIRD PARTY IMPORTS
#   LOCAL APPLICATION IMPORTS
from POSITIVESLOPEFILTER import positive_slopes


# RETURNS A LIST OF ALL THE TICKERS AVAILABLE AT OR BEFORE A GIVEN DATE AND AT OR AFTER GIVEN DATE
def tickerportal(daterangedb_source, tickerlistcommon_source, beg_date, end_date, pool):

    # LOAD DATAFRAME OF EARLIEST DATES
    with open(daterangedb_source, "rb") as targetfile:
        all_startdates = pkl.load(targetfile)

    # SLICE DATAFRAME
    valid_rows = all_startdates[(all_startdates['first_date'] <= beg_date) & (all_startdates['last_date'] >= end_date)]
    valid_stocks = valid_rows['stock'].tolist()

    # FILTER
    if type(pool) == list:
        final_pool = list(set(valid_stocks).intersection(set(pool)))
    elif pool == 'common':
        with open(tickerlistcommon_source, "rb") as targetfile:
            tickerlistdf = pkl.load(targetfile)
        tickerlist = tickerlistdf['symbol'].tolist()
        final_pool = list(set(valid_stocks).intersection(set(tickerlist)))
    else:
        final_pool = valid_stocks

    # RETURN FINAL LIST
    return final_pool


# RETURNS A LIST OF ALL THE TICKERS AVAILABLE AT OR BEFORE A GIVEN DATE
def tickerportal2(daterangedb_source, tickerlistcommon_source, date, pool):

    # LOAD DATAFRAME OF EARLIEST DATES
    with open(daterangedb_source, "rb") as targetfile:
        all_startdates = pkl.load(targetfile)

    # SLICE DATAFRAME
    valid_rows = all_startdates[all_startdates['first_date'] <= date]
    valid_stocks = valid_rows['stock'].tolist()

    # FILTER
    if type(pool) == list:
        final_pool = list(set(valid_stocks).intersection(set(pool)))
    elif pool == 'common':
        with open(tickerlistcommon_source, "rb") as targetfile:
            tickerlistdf = pkl.load(targetfile)
        tickerlist = tickerlistdf['symbol'].tolist()
        final_pool = list(set(valid_stocks).intersection(set(tickerlist)))
    else:
        final_pool = valid_stocks

    # RETURN FINAL LIST
    return final_pool


# RETURNS A LIST OF ALL THE TICKERS AVAILABLE AT OR BEFORE A GIVEN DATE AND THAT HAVE POSITIVE SLOPES
def tickerportal3(daterangedb_source, tickerlistcommon_source, date, pool):

    unfiltered_pool = tickerportal2(daterangedb_source, tickerlistcommon_source, date, pool)

    filtered_pool = positive_slopes(unfiltered_pool, '', date)

    return filtered_pool
