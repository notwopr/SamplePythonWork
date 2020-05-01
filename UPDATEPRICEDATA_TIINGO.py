"""
Title: Stock Price Retriever - Tiingo API
Date Started: March 16, 2019
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied
    without the express written consent of David Hyongsik Choi.
Purpose: The purpose of the Golden Retriever Module is to retrieve prices from
    a single day and prices within a given date range.

ON TIINGO BEHAVIOR: TIINGO WILL RETURN ANY AND ALL PRICES AVAILABLE WITHIN AN GIVEN DATE RANGE.  IT WON'T RETURN ANY ENTRIES FOR DATES WHERE THE PRICES ARE NOT AVAILABLE.  IF THERE ARE NO PRICES AVAILABLE WITHIN A DATE RANGE, IT WILL RETURN A BLANK.

"""


# IMPORT TOOLS
import requests as rq


# API PREP
base = ["https://api.tiingo.com"]  # TIINGO

endpoint = ["tiingo/daily", "prices", "iex"]  # TIINGO

apiprep = ["token="]  # TIINGO

apiprepk = ["ea0e9806c6cf888517ed0a6e99527f6f5b0467ad"]  # TIINGO


def parametizer(x, y):  # x=startdate; y=enddate
    param = [
        apiprep[0] + apiprepk[0],
        "startDate=" + x,
        "endDate=" + y,
        "resampleFreq=daily",
        "format=json",
        "columns=date,adjClose",
    ]
    param_str = "&".join(param)
    return param_str


def retriever(w, x, y, z):
    # w=stock, x=startdate, y=enddate,
    # z=(0=daterange/singledate, 1=realtime, 2=earliestdate)
    url = [
        (
            base[0]
            + "/"
            + endpoint[0]
            + "/"
            + w
            + "/"
            + endpoint[1]
            + "?"
            + parametizer(x, y)
        ),
        (
            base[0]
            + "/"
            + endpoint[2]
            + "/"
            + w
            + "?"
            + apiprep[0]
            + apiprepk[0]
        ),
        (
            base[0]
            + "/"
            + endpoint[0]
            + "/"
            + w
            + "?"
            + apiprep[0]
            + apiprepk[0]
        ),
    ]
    return rq.get(url[z])
