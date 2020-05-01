"""
Title: Market Retriever Module - WORLD TRADING DATA API
Date Started: May 2, 2019
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied
without the express written consent of David Hyongsik Choi.
Purpose: The purpose of the Market Retriever Module is to retrieve market
prices from a single day and prices within a given date range.
"""


# IMPORT TOOLS
import requests as rq

# API PREP
base = ["https://www.worldtradingdata.com/api/v1"]  # WTD

endpoint = ["stock", "history"]  # WTD Realtime Prices  # WTD Historical Prices

apiprep = ["api_token="]

apiprepk = ["YncbuuilRUEfRrf71Uz1UkybBKNRUbT9NMcSGyg5H9mrOCAbvuPSGsKiAq1V"]


def parametizer(v, w, x, y):  # x=startdate; y=enddate
    param = [
        [
            apiprep[0] + apiprepk[0],
            "symbol=" + w,
            "ouput=json",
            "sort=oldest",
            "date_from=" + x,
            "date_to=" + y,
        ],
        [apiprep[0] + apiprepk[0], "symbol=" + w, "output=json"],
        [apiprep[0] + apiprepk[0], "symbol=" + w, "ouput=json", "sort=oldest"],
    ]
    param_str = "&".join(param[v])
    return param_str


def retriever(w, x, y, z):
    # w=stock, x=startdate, y=enddate, z=(0=span/single, 1=realtime,2=fullhist)
    url = [
        (base[0] + "/" + endpoint[1] + "?" + parametizer(0, w, x, y)),
        (base[0] + "/" + endpoint[0] + "?" + parametizer(1, w, "", "")),
        (base[0] + "/" + endpoint[1] + "?" + parametizer(2, w, "", "")),
    ]
    return rq.get(url[z])
