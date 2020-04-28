"""
Title: Outlier Visualizer
Date Started: ?, 2019
Version: 1.0
Version Start Date: ?, 2019
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied
    without the express written consent of David Hyongsik Choi.
Purpose: Visualize the effects of different strengths of outlier thresholds.
"""
# IMPORT TOOLS
#   STANDARD LIBRARY IMPORTS
#   THIRD PARTY IMPORTS
#   LOCAL APPLICATION IMPORTS
from UPDATEPRICEDATA_MASTERSCRIPT import PRICES, daterangedb_source, tickerlistcommon_source
from filelocations import readpkl
from growthcalcbot import period_growth_portfolio
from tickerportalbot import tickerportal

# PRICE MATRIX LOCATION
pricematrix = 'allpricematrix_common'
pricematrixfolder = PRICES

# RANGE OF OUTLIER TOLERANCE TO TEST
strength_min = 0
strength_max = 10
increment = 0.5
all_strengths = [((strength_max * 2) - elem) * increment for elem in range(strength_min, (strength_max * 2) + 1)]
print(all_strengths)


# INPUT TIME PERIOD OF SAMPLE DATA
period = ['2014-11-21', '2016-02-12']

# SET METHOD FOR AGGREGATING CHANGE OVER MAXPRICE SAMPLES
aggregatemethod = 'median'
remove_outliers = 'yes'

# VERBOSITY
verbose = ''
plot = 'plot'

# GET RESULTS
pricematrixdf = readpkl(pricematrix, pricematrixfolder)
pool = tickerportal(daterangedb_source, tickerlistcommon_source, period[0], period[1], 'common')
item = [pool, period]
for strength in all_strengths:
    period_growth_portfolio(aggregatemethod, remove_outliers, strength, verbose, plot, pricematrixdf, item)
