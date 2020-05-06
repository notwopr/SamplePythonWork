"""
Title: File and Folder Operations
Date Started: June 20, 2019
Version: 1.1
Version Start Date: May 5, 2020
Author: David Hyongsik Choi
Legal:  All rights reserved.  This code may not be used, distributed, or copied without the express written consent of David Hyongsik Choi.
Purpose: The purpose of the File Location Bot is to store the address of data files.

Version Notes:
1.1: Update notes and use f string syntax.
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


# SAVE TO PKL
def savetopkl(filename, directory, data):

    # WRITE TO FILE
    with open(directory / f"{filename}.pkl", "wb") as targetfile:
        pkl.dump(data, targetfile, protocol=4)


# READ TO PKL
def readpkl(filename, directory):

    # OPEN FILE
    with open(directory / f"{filename}.pkl", "rb") as targetfile:
        data = pkl.load(targetfile)

    # PRINT DATA
    return data
