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


def earliest_price(q):
    respraw_meta = retriever(q, "", "", 2)
    respjs_meta = respraw_meta.json()
    earliest_date = respjs_meta["startDate"]
    respraw_ed = retriever(q, earliest_date, earliest_date, 0)
    return respraw_ed.json()


# I. DATE RANGE PRICE RETRIEVAL

def func1():
    start_date = "1950-09-10"
    end_date = "2019-12-31"
    respraw_dr = retriever("OPRX", start_date, end_date, 0)
    respjs_dr = respraw_dr.json()


def func2():
    start_date = "1950-09-10"
    end_date = "2019-12-31"
    respraw_dr = rq.get("https://api.tiingo.com/tiingo/daily/OPRX/prices?token=ea0e9806c6cf888517ed0a6e99527f6f5b0467ad&startDate=1950-09-10&endDate=2019-12-31&resampleFreq=daily&format=json&columns=date,adjClose")
    respjs_dr = respraw_dr.json()


def func3():
    start_date = "1950-09-10"
    respraw_dr = rq.get("https://api.tiingo.com/tiingo/daily/OPRX/prices?token=ea0e9806c6cf888517ed0a6e99527f6f5b0467ad&startDate=1950-09-10&resampleFreq=daily&format=json&columns=date,adjClose")
    respjs_dr = respraw_dr.json()





# II. SINGLE DATE PRICE RETRIEVAL
'''
target_date = "2013-11-08"

respraw_sd = retriever('DLY', target_date, target_date, 0)
respjs_sd = respraw_sd.json()


# III. REALTIME PRICE RETRIEVAL

respraw_rt = retriever(stocklist[0], "", "", 1)
respjs_rt = respraw_rt.json()
datetimestamp = respjs_rt[0]["timestamp"]
date_stamp = datetimestamp[0:10]
time_stamp = datetimestamp[11:19]
price_rt = respjs_rt[0]["tngoLast"]


# IV. EARLIEST AVAILABLE PRICE



respjs_ed = retriever("EWJE", "", "", 2)
respjs_meta = respjs_ed.json()
print(respjs_meta)
'''