#!/usr/bin/env python
import os

# define the record count each page display
PER_PAGE_COUNT = 15
# the log file
LOG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs/logs")
# define app name
APP_NAME = "cmdb"
# define server,equipment,projects permission require status
PERMISSION_REQUIRE = {
    "server": True,
    "equipment": True,
    "projects": False,
    "assets": True
}
# current customer default id
CUST_ID = 10011
