"""
Title: File Location Bot
Date Started: June 20, 2019
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied without the express written consent of David Hyongsik Choi.
Purpose: The purpose of the File Location Bot is to store the address of data files.

GUIDELINES: ONLY ADD FOLDERS THAT MORE THAN ONE MODULE NEEDS TO ACCESS DIRECTLY.  IF THE FOLDER IS ONLY USED BY A SINGLE MODULE, THEN DO NOT ADD HERE.  ADD IT ON THE MODULE ITSELF.
TO DO:
--FUNCTION THAT DETECTS WHICH COMPUTER i'M WORKING FROM AND ADJUSTS PATH ACCORDINGLY.
"""

# IMPORT TOOLS
#   STANDARD LIBRARY IMPORTS
import os
import shutil
import pickle as pkl
#   THIRD PARTY IMPORTS
#   LOCAL APPLICATION IMPORTS


# DELETE AND CREATE FOLDERS
def delete_create_folder(location):
    if os.path.isdir(location) is True:
        shutil.rmtree(location)
    os.makedirs(location)


# CREATE FOLDER IF DOESN'T EXIST
def create_nonexistent_folder(location):
    if os.path.isdir(location) is False:
        os.makedirs(location)


# DELETE FILE IF EXISTS
def delete_file(path):
    if os.path.exists(path) is True:
        os.remove(path)


def savetopkl(filename, directory, data):

    # WRITE TO FILE
    with open(directory / "{}.pkl".format(filename), "wb") as targetfile:
        pkl.dump(data, targetfile, protocol=4)


def readpkl(filename, directory):

    # OPEN FILE
    with open(directory / "{}.pkl".format(filename), "rb") as targetfile:
        data = pkl.load(targetfile)

    # PRINT DATA
    return data
