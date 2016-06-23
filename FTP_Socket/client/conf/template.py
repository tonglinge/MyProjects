#!/usr/bin/env python

START_MENU = """
-------------------------------------------
              FTP CLIENT
-------------------------------------------
"""

LOGINED_MENU = """
---------------------------------------------------------------------------------------------
                                    FTP CLIENT

User:{0}         TotalSpace:{1} MB         UsedSpace:{2} MB
---------------------------------------------------------------------------------------------
Commands:
    put:   put|[filename]     # upload a file to server,[filename] must have a full path name
    get:   get|[filename]     # download a file from server
    show:  show               # show the folder and files in the home folder
    cd:    cd|[folder]        # go to [folder],return back input cd|..
    quit:                     # exit system
"""