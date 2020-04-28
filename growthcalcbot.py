"""
Title: Portfolio Growth Bot
Date Started: Jun 8, 2019
Version: 4.0
Vers Start Date: Dec 3, 2019
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied
    without the express written consent of David Hyongsik Choi.
Purpose: The purpose of the Portfolio Growth Calculator Module is to calculate
    the growth of a portfolio and its value assuming any changes to the
    portfolio composition are made where all stocks in the new composition are
    equally funded.
"""

# IMPORT TOOLS
#   Standard library imports
import datetime as dt
#   Third party imports
import numpy as np
#   Local application imports
from statresearchbot import outlier_remover, list_aggregator


# RETURNS GROWTH OF A PORTFOLIO-TIMEPERIOD PAIR GIVEN PRICEHISTORY MATRIX DATAFRAME
def period_growth_portfolio(aggregatemethod, remove_outliers, strength, verbose, plot, pricematrix, item):

    # MAP OUT ITERATOR
    beg_date = item[1][0]
    end_date = item[1][1]
    portfolio = item[0]

    # PULL UP PRICE MATRIX AND SLICE OUT STOCKS REQUESTED
    all_cols = ['___Date___'] + portfolio
    sliced = pricematrix[all_cols].copy()

    # SLICE OUT DATE RANGE REQUESTED
    sliced = sliced.loc[(sliced['___Date___'] >= dt.date.fromisoformat(beg_date)) & (sliced['___Date___'] <= dt.date.fromisoformat(end_date))]

    # RESET INDEX
    sliced.reset_index(drop=True, inplace=True)

    # REMOVE EVERY ROW EXCEPT FIRST AND LAST
    sliced = sliced.iloc[[0, -1], :]
    sliced.reset_index(drop=True, inplace=True)

    # CORRECT FOR INFINITE SLOPE (IF STARTING PRICE IS ZERO, CHANGE TO 1 DOLLAR)
    sliced.replace(to_replace=float(0), value=1, inplace=True)

    # CALCULATE CHANGE
    sliced.iloc[:, 1:] = sliced.iloc[:, 1:].pct_change(fill_method="ffill")
    all_data = sliced.iloc[1, 1:].tolist()

    # REMOVE OUTLIERS?
    if remove_outliers == 'yes':
        all_data = outlier_remover(verbose, plot, strength, all_data)

    answer = list_aggregator(aggregatemethod, all_data)

    if verbose == 'verbose':
        max = 6
        slicedwidth = len(sliced.columns) - 1
        if slicedwidth > max:
            rounds = (slicedwidth // max)
            for round in range(rounds+1):
                factor = round * max
                if max+factor > slicedwidth:
                    listofcolnums = [0] + list(range(1+factor, slicedwidth+1))
                else:
                    listofcolnums = [0] + list(range(1+factor, (max+factor)+1))
                print(sliced.iloc[:, listofcolnums])
        else:
            print(sliced)
        print('\n')
    return answer


# MULTIPLE PERIOD GROWTH CALCULATION of POOL OF CONTIGUOUS (PORTFOLIO, PERIOD) PAIRS
def multiperiod_growth_portfolio(pricematrix, package, aggregatemethod, remove_outliers, strength, verbose, plot):

    growth_rates = [period_growth_portfolio(aggregatemethod, remove_outliers, strength, verbose, plot, pricematrix, item) for item in package]
    factors = [sample + 1 for sample in growth_rates]
    product = np.prod(factors)
    answer = product - 1
    if verbose == "verbose":
        print('Period Growth Rates + 1: {} || Product of (Growth Rates + 1): {}'.format(factors, product))
        print('Overall Total Growth: {}'.format(answer))
        print('\n')

    return answer
