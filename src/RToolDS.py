#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-
# generated by wxGlade 0.6.1 on Fri Nov 02 11:07:38 2007

import os
import sys

if sys.platform == "win32":
    import UnRAR2 as UnRAR #@UnusedImport

OldDir = os.getcwd()

if sys.platform == "win32":
    try:
        os.chdir(os.path.join (os.environ["APPDATA"], "RToolDS"))
    except:
        try:
            os.mkdir(os.path.join (os.environ["APPDATA"], "RToolDS"))
            os.chdir(os.path.join (os.environ["APPDATA"], "RToolDS"))
        except:
            exit ()
    try:
        os.mkdir(os.path.join (os.environ["APPDATA"], "RToolDS", "cache"))
    except:
        pass
    try:
        os.mkdir(os.path.join (os.environ["APPDATA"], "RToolDS", "cache", "img"))
    except:
        pass
    try:
        os.mkdir(os.path.join (os.environ["APPDATA"], "RToolDS", "cache", "nfo"))
    except:
        pass
    try:
        os.mkdir(os.path.join (os.environ["APPDATA"], "RToolDS", "cache", "saves"))
    except:
        pass
            
if sys.platform == "linux2":
    try:
        os.chdir(os.path.expanduser("~/.RToolDS"))
    except:
        try:
            os.mkdir(os.path.expanduser("~/.RToolDS"))
            os.chdir(os.path.expanduser("~/.RToolDS"))
        except:
            exit ()
    try:
        os.mkdir(os.path.join (os.path.expanduser("~/.RToolDS"), "cache"))
    except:
        pass
    try:
        os.mkdir(os.path.join (os.path.expanduser("~/.RToolDS"), "cache", "img"))
    except:
        pass
    try:
        os.mkdir(os.path.join (os.path.expanduser("~/.RToolDS"), "cache", "nfo"))
    except:
        pass
    try:
        os.mkdir(os.path.join (os.path.expanduser("~/.RToolDS"), "cache", "saves"))
    except:
        pass

if os.path.isfile ("RToolDS_Trimmed.dat.new") and os.path.isfile ("RToolDS_Trimmed.dat") == False:
    os.rename( "RToolDS_Trimmed.dat.new", "RToolDS_Trimmed.dat" )
    os.utime( "RToolDS_Trimmed.dat", None )

import gettext
gettext.install("RToolDS") # replace with the appropriate catalog name

import wx

from cDummyFrame import cDummyFrame
from cMainFrame import cMainFrame
import Config
import GFX

Config.Load ()

RToolDS = wx.PySimpleApp(0)
wx.InitAllImageHandlers()

DummyFrame = cDummyFrame ( None )
RToolDS.SetTopWindow(DummyFrame)
if sys.platform != "linux2":
    #DummyFrame.Freeze()
    DummyFrame.Show()
    #DummyFrame.Hide()

if Config.Config ["Show_Splash"]:
    wx.SplashScreen( bitmap=GFX.catalog ["GFX_Logo"].getBitmap(), milliseconds=3000, parent = DummyFrame, splashStyle = wx.SPLASH_CENTRE_ON_SCREEN|wx.SPLASH_TIMEOUT )

MainFrame = cMainFrame(None, -1, "", DummyFrame=DummyFrame)
RToolDS.SetTopWindow(MainFrame)
DummyFrame.Destroy()
MainFrame.Show()
RToolDS.MainLoop()

Config.Save ()

os.chdir(OldDir)
