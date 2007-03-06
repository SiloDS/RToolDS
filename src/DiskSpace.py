#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

import sys
import os
from statvfs import F_BLOCKS, F_BAVAIL, F_FRSIZE

if sys.platform == "win32":
    import win32api

    def DriveSize ( Path ):
        return win32api.GetDiskFreeSpaceEx( Path )[1]

    def DriveFree ( Path ):
        return win32api.GetDiskFreeSpaceEx( Path )[0]

elif sys.platform == "linux2":
    def DriveSize ( Path ):
        return os.statvfs( Path )[F_FRSIZE ] * os.statvfs ( Path )[F_BLOCKS]
    
    def DriveFree ( Path ):
        return os.statvfs( Path )[F_FRSIZE ] * os.statvfs ( Path )[F_BAVAIL]
