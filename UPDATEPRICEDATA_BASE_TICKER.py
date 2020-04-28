"""
Title: Update Price Data - Ticker Data
Date Started: April 26, 2019
Version: 1.0
Vers Date: Nov 9, 2019
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied without the express written consent of David Hyongsik Choi.
Purpose: Retrieve list of tickers of all the companies listed on the NYSE and NASDAQ.
"""

# IMPORT TOOLS
#   STANDARD LIBRARY IMPORTS
import json as js
import requests as rq
import re
#   THIRD PARTY IMPORTS
import pandas as pd
#   LOCAL APPLICATION IMPORTS
from filelocations import savetopkl


def symfilt(x):
    y = x.get("symbol")
    z = x.get("name")
    return {'symbol': y, 'name': z}


def checkaccuracy(a, b, c, verbose):  # a = stocklist at issue; b = correct length; c = tolerance
    # YOUR LIST'S TALLY
    tally = len(a)

    # ACTUAL NUMBER OF NASDAQ + NYSE STOCKS TRADEABLE FROM INDEPENDENT SOURCE
    truetally = b
    tolerance = c

    # CALCULATE DIFFERENCE
    diff = tally - truetally

    # REPORT FINDINGS
    if tally in range(truetally - tolerance, truetally + tolerance):
        if verbose == 'verbose':
            print(
                "%s \n %s %s %s \n %s %s %s \n %s %+d \n %s%s"
                % (
                    "YAY!! THE LIST IS ACCURATE!",
                    "YOUR LIST:",
                    tally,
                    "SYMBOLS",
                    "TRADEABLE US STOCKS:",
                    truetally,
                    "SYMBOLS",
                    "DIFFERENCE:",
                    diff,
                    "TOLERANCE: +/-",
                    tolerance,
                )
            )
        return True
    else:
        if verbose == 'verbose':
            print(
                "%s \n %s %s %s \n %s %s %s \n %s %+d \n %s%s"
                % (
                    "WARNING!! THE LIST IS NOT ACCURATE!",
                    "YOUR LIST:",
                    tally,
                    "SYMBOLS",
                    "TRADEABLE US STOCKS:",
                    truetally,
                    "SYMBOLS",
                    "DIFFERENCE:",
                    diff,
                    "TOLERANCE: +/-",
                    tolerance,
                )
            )
        return False


def storealltickers(destfolder, tickerfilename_all, tickerfilename_common):
    # API PREP
    base = ["https://cloud.iexapis.com/"]

    endpoint = ["stable", "ref-data/symbols"]

    apiprep = ["token="]

    apiprepk = ["sk_515e8be68f01497cabba3d0fcaa18638"]

    param = [["filter=symbol,name,exchange,type"]]

    paramstr = "&".join(param[0])

    url = (
        base[0]
        + "/"
        + endpoint[0]
        + "/"
        + endpoint[1]
        + "?"
        + apiprep[0]
        + apiprepk[0]
        + "&"
        + paramstr
    )

    # RETRIEVE AND STORE TICKER DATA, AND RECORD TIMESTAMP OF RETRIEVAL
    tickraw = rq.get(url)
    ticktxt = tickraw.text
    ticklist = js.loads(ticktxt)

    # FILTER OUT NON-NYSE AND NON-NASDAQ STOCKS AS WELL AS NON-COMMON SHARES
    alltickers = list(
        filter(lambda x: x["exchange"] == "NAS" or x["exchange"] == "NYS", ticklist)
    )

    # FILTER OUT NON-COMMON SHARES
    commontickers = list(
        filter(lambda x: x["type"] == "cs", alltickers)
    )

    # FILTER THE LIST TO CONTAIN ONLY TICKER SYMBOLS and NAMES
    drafttickall = list(map(symfilt, alltickers))
    drafttickcommon = list(map(symfilt, commontickers))

    # REMOVE ANY DUPLICATES
    finaltickall = []
    finaltickcommon = []
    for pair in [[drafttickall, finaltickall], [drafttickcommon, finaltickcommon]]:
        uniquesymbols = []
        for stockdict in pair[0]:
            if stockdict['symbol'] not in uniquesymbols:
                uniquesymbols.append(stockdict['symbol'])
                pair[1].append(stockdict)

    # EDIT LIST FOR TIINGO SYNTAX
    for stocklist in [finaltickall, finaltickcommon]:
        for stockdict in stocklist:
            if stockdict['symbol'].find('=') != -1:  # UNITS OF FORM "SYMBOL="
                newsym = stockdict['symbol'].replace("=", "-U")
                stockdict.update({'symbol': newsym})
            elif re.search('\.', stockdict['symbol']) is not None:  # PREFERRED CLASSES OF FORM "SYMBOL.*"
                newsym = stockdict['symbol'].replace(".", "-")
                stockdict.update({'symbol': newsym})
            elif re.search('-\w', stockdict['symbol']) is not None:  # PREFERRED CLASSES OF FORM "SYMBOL-*"
                newsym = stockdict['symbol'].replace("-", "-P-")
                stockdict.update({'symbol': newsym})
            elif re.search('-$', stockdict['symbol']) is not None:  # PREFERRED CLASSES OF FORM "SYMBOL-"
                newsym = stockdict['symbol'].replace("-", "-P")
                stockdict.update({'symbol': newsym})
            elif re.search('\^$', stockdict['symbol']) is not None:  # RIGHTS OF FORM "SYMBOL^"
                newsym = stockdict['symbol'].replace("^", "-R")
                stockdict.update({'symbol': newsym})
            elif re.search('\^#$', stockdict['symbol']) is not None:  # RIGHTS WHEN ISSUED OF FORM "SYMBOL^#"
                newsym = stockdict['symbol'].replace("^#", "-R-W")
                stockdict.update({'symbol': newsym})
            elif re.search('#$', stockdict['symbol']) is not None:  # WARRANTS OF FORM "SYMBOL#"
                newsym = stockdict['symbol'].replace("#", "-WI")
                stockdict.update({'symbol': newsym})
            elif re.search('\+$', stockdict['symbol']) is not None:  # WARRANTS OF FORM "SYMBOL+"
                newsym = stockdict['symbol'].replace("+", "-WS")
                stockdict.update({'symbol': newsym})
            elif stockdict['symbol'].find('+') != -1:  # WARRANTS OF FORM "SYMBOL+*"
                newsym = stockdict['symbol'].replace("+", "-WS-")
                stockdict.update({'symbol': newsym})

    finalalldf = pd.DataFrame(data=finaltickall)
    finalcommondf = pd.DataFrame(data=finaltickcommon)

    # SAVE TO FILE
    savetopkl(tickerfilename_all, destfolder, finalalldf)
    savetopkl(tickerfilename_common, destfolder, finalcommondf)
    finalalldf.to_csv(index=False, path_or_buf=destfolder / '{}.csv'.format(tickerfilename_all))
    finalcommondf.to_csv(index=False, path_or_buf=destfolder / '{}.csv'.format(tickerfilename_common))
