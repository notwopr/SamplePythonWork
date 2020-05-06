"""
Title: Computer Settings Bot
Date Started: Oct 24, 2019
Version: 1.2
Version Date: May 5, 2020
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied without the express written consent of David Hyongsik Choi.
Purpose: Settings depending on computer used to run code.
On AMD D drive, downloading all prices: 1 min 35 secs
On AMD C drive, downloading all prices: 0 min 34 secs

Version Notes:
1.1: Changed AMD processor max to usecores - 4.  With Python 3.8.1 update started getting errors when processors was 61 or higher.  So made max 60.
1.2: Simplified code and added Surface Laptop.
"""
# IMPORT TOOLS
#   STANDARD LIBRARY IMPORTS
from pathlib import Path
import psutil

# GET NUMBER OF CORES
num_cores = psutil.cpu_count(logical=True)

# DEFINE SYSTEMS ON WHICH TO RUN THIS SCRIPT
surfacepro = {
    'dump_predicate': 'C:',
    'importantloc_predicate': 'C:',
    'use_cores': num_cores - 1
}
intelcomp = {
    'dump_predicate': 'F:',
    'importantloc_predicate': 'F:',
    'use_cores': num_cores - 1
}
amdcomp = {
    'dump_predicate': 'C:',
    'dump_predicate2': 'D:',
    'importantloc_predicate': 'C:/Users/david',
    'use_cores': num_cores - 4
}

'''PLEASE CHOOSE WHICH ABOVE COMPUTER TO RUN ON'''
comptype = surfacepro

# SET USE CORES & CHUNKSIZE
use_cores = comptype['use_cores']
chunksize = 5

# SET PARENT DIRECTORIES
BOT_DUMP = Path(f'{comptype["dump_predicate"]}/BOT_DUMP')
BOT_IMPORTANT = Path(f'{comptype["importantloc_predicate"]}/Google Drive/Goals/Careers/Business/Good Business Ideas/Fund Business/Investment Strategy Research/BOTOUTPUT')
if comptype == amdcomp:
    BOT_DUMP2 = Path(f'{comptype["dump_predicate2"]}/BOT_DUMP')
