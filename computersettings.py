"""
Title: Computer Settings Bot
Date Started: Oct 24, 2019
Version: 1.1
Version Date: Feb 25, 2020
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied without the express written consent of David Hyongsik Choi.
Purpose: Settings depending on computer used to run code.
On AMD D drive, downloading all prices: 1 min 35 secs
On AMD C drive, downloading all prices: 0 min 34 secs

Version Notes:
1.1: Changed AMD processor max to usecores - 4.  With Python 3.8.1 update started getting errors when processors was 61 or higher.  So made max 60.
"""
# IMPORT TOOLS
#   STANDARD LIBRARY IMPORTS
from pathlib import Path
import psutil


# DEFINE SYSTEMS ON WHICH TO RUN THIS SCRIPT
intelcomp = {
    'dump_predicate': 'F:',
    'importantloc_predicate': 'F:'
}
amdcomp = {
    'dump_predicate': 'C:',
    'dump_predicate2': 'D:',
    'importantloc_predicate': 'C:/Users/david'
}

'''PLEASE CHOOSE WHICH ABOVE COMPUTER TO RUN ON'''
comptype = intelcomp
num_cores = psutil.cpu_count(logical=True)
if comptype == intelcomp:
    use_cores = num_cores - 1
elif comptype == amdcomp:
    use_cores = num_cores - 4
chunksize = 5

# DEFINE PARENT DIRECTORIES
BOT_DUMP = Path('{}/BOT_DUMP'.format(comptype['dump_predicate']))
if comptype == amdcomp:
    BOT_DUMP2 = Path('{}/BOT_DUMP'.format(comptype['dump_predicate2']))
BOT_IMPORTANT = Path('{}/Google Drive/Goals/Careers/Business/Good Business Ideas/Fund Business/Investment Strategy Research/BOTOUTPUT'.format(comptype['importantloc_predicate']))
