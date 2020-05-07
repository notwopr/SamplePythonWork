"""
Title: Stock Price Retriever - Tiingo API
Date Started: March 16, 2019
Version: 1.1
Version Start Date: May 5, 2020
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied
    without the express written consent of David Hyongsik Choi.
Purpose: Retrieve prices for a given stock.

ON TIINGO BEHAVIOR: TIINGO WILL RETURN ANY AND ALL PRICES AVAILABLE WITHIN A GIVEN DATE RANGE.  IT WON'T RETURN ANY ENTRIES FOR DATES WHERE THE PRICES ARE NOT AVAILABLE.  IF THERE ARE NO PRICES AVAILABLE WITHIN A DATE RANGE, IT WILL RETURN A BLANK.

Version Notes:
1.1: Simplify code.

"""


# IMPORT TOOLS
#   STANDARD LIBRARY IMPORTS
#   THIRD PARTY IMPORTS
import requests as rq
import pandas as pd
#   LOCAL APPLICATION IMPORTS


def stockpriceretrieval(stock, start_date, end_date):

    # SET PRICE URL
    stockpriceurl = f'https://api.tiingo.com/tiingo/daily/{stock}/prices?token=&startDate={start_date}&endDate={end_date}&resampleFreq=daily&format=json&columns=date,adjClose'

    # RETRIEVE PRICES
    prices = rq.get(stockpriceurl)
    # PARSE PRICES
    prices = prices.json()

    # CONVERT TO DATAFRAME
    prices = pd.DataFrame(prices)

    # CHANGE ORDER OF COLUMNS
    prices = prices[["date", "adjClose"]]
    prices = prices.rename(columns={"adjClose": stock})

    # RE-NUMBER INDEX
    prices.reset_index(drop=True, inplace=True)
    return prices
