#!/usr/bin/env python
"""
定义客户端类状态代码
"""


CONN_SUCC = 1000                # connect ftp-server successful
CONN_FAIL = 1001                # connect server fail
AUTH_SUCC = 2000                # login auth successfull
AUTH_USER_ERROR = 2001          # login auth user does not exists
AUTH_FAIL = 2002                # login auth failed,bad username or password
AUTH_LOCKED = 2003              # user account has locked
FILE_UPLOAD_SUCC = 3000         # upload file succ
FILE_NOT_EXISTS = 3001          # upload file does not exists
FILE_UPLOAD_FAIL = 3002         # upload file failed
FILE_NOT_FOUND = 3003           # download file ,file does not found
TRANS_READY = 4000              # upload or download file ,server is ready
FILE_MD5_SUCC = 4001            # file md5 check succ
FILE_MD5_FAIL = 4002            # file md5 check fail

