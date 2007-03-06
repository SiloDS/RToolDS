#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

import os
import copy
import sys
if sys.version_info[0] == 2 and sys.version_info[1] >= 5:
    from sqlite3 import dbapi2 as sqlite
else:
    from pysqlite2 import dbapi2 as sqlite
import cPickle

ConfigVersion = 1
ProgVersion = "0.1(Build 67) Very Beta"
DBVersion=1
CartDrive=None
SaveDir=""
CartExtensions = [ ".nds" ]
SaveExtensions = [ ".sav" ]
Regions     = {
               "America":"(U)", 
               "Europe":"(E)", 
               "Japan":"(J)", 
               "Not Japan":"!(J)"
               }
ROMPaths = []
AllExtensions = copy.copy( CartExtensions )
AllExtensions.append ( ".zip" )
Columns = ["Icon", "Release Number", "Filename", "Display Name", "Size", "Header Title", "Maker", "Logo Title", "Saves", "Genre", "Trimmed Size"]
ColumnTitles  = {"Icon":"Icon", "Release Number":"No", "Filename":"Filename", "Display Name":"Display Name", "Size":"Size", "Header Title":"Header Title", "Maker":"Maker", "Logo Title":"Logo Title", "Saves":"Saves", "Genre":"Genre", "Trimmed Size":"Trimmed Size" }
ColumnsToDisplay = ["Icon", "Release Number", "Display Name", "Size"]
ColumnSizes  = {"Icon":36, "Release Number":-1, "Filename":-1, "Display Name":245, "Size":-1, "Header Title":10, "Maker":10, "Logo Title":10, "Saves":-1, "Genre":-1, "Trimmed Size":-1 }
#ColumnSizes = [36, -1, 245, -1]
ScreenSize = ( 800, 600 )
ScreenPos = ( -1, -1 )
OptionsSize = ( 473, 353 )
OptionsPos = ( -1, -1 )
AutoBackupSaves = 1
AutoRestoreSaves = 1
OptionsAreOK = False
NumSaves = 5
CheckNewFilesOnStartup = 0
ShowSplash = 1
ScreenMaximize = False
CurrentRegion = "Any Country"
SaveMgrColSizes = [330, 25, 110]
SaveMgrSize = ( 500, 400 )
CurrentSize = "Any Size"
Sizes = [8, 16, 24, 32, 64, 128]
Missing = []
Genres = ["Action", "Adventure", "Other", "Platform", "Puzzle", "RPG", "Racing", "Simulation", "Sports", "Strategy", "Unknown", "n/a" ]
Genre = [ "Any Genre" ]
SaveFilters = True
CurrentFilter = ""
ShowROMSizes = ["MegaBits","MegaBytes","KiloBits","KiloBytes","Bytes"]
ShowROMSizeIn = "MegaBytes"
CopyTrim = True
DBCreateVersion = """
CREATE TABLE [Version] ([Version] INTEGER NOT NULL PRIMARY KEY);
"""
DBCreateFiles = """
CREATE TABLE [Files] (
[ID] VARCHAR(6)  UNIQUE NOT NULL,
[ReleaseNumber] INTEGER  NOT NULL,
[DisplayName] TEXT  NOT NULL,
[FileName] TEXT  NOT NULL,
[DirectoryName] TEXT  NOT NULL,
[InternalZipName] TEXT  NULL,
[Size] INTEGER  NOT NULL,
[Date] TIMESTAMP  NOT NULL,
[Image] BLOB  NULL,
[SmallImage] BLOB  NULL,
[Header_Title] VARCHAR(12)  NULL,
[Header_Maker_Code] VARCHAR(2)  NULL,
[Header_Game_Code] VARCHAR(4)  NULL,
[Header_Card_Size] INTEGER  NULL,
[Header_Logo_Title] VARCHAR(256)  NULL,
[TrimSize] INTEGER DEFAULT '0' NULL,
[PocketHeavenNum] INTEGER  NULL
)
"""
DBCreateGenre = """
CREATE TABLE [Genre] (
[ReleaseNum] INTEGER  NOT NULL PRIMARY KEY,
[Genre] TEXT DEFAULT '20' NULL,
[PocketHeavenGenre] TEXT DEFAULT '20' NULL
)
"""
DBCreateView = """
CREATE VIEW [DefaultView] AS 
select f.*, g.Genre, g.PocketHeavenGenre as Genre from files f , genre g
where f.ReleaseNumber = g.ReleaseNum
order by f.ReleaseNumber
"""

def SetupDatabase ():
    global DBVersion
    DBFileName = os.path.join ( os.path.realpath( os.path.dirname( sys.argv[0] ) ), "RToolDS.s3db" )

    con = sqlite.connect( DBFileName )
    m_Cursor = con.cursor()
    try:
        m_Cursor.execute ( "select Version from Version" )
    except:
        m_Cursor.execute ( DBCreateVersion )
        m_Cursor.execute ( DBCreateFiles )
        m_Cursor.execute ( DBCreateGenre )
        m_Cursor.execute ( DBCreateView )
        m_Cursor.execute ( "INSERT INTO VERSION VALUES ("+str( DBVersion )+");" )
        con.commit ();
        m_Cursor.execute ( "select Version from Version" )
    DBVersion = m_Cursor.fetchone()[0]
    
    m_Cursor.close()
    return con

def Save( Filename ):
    global ConfigVersion, ROMPaths, Columns, ColumnsToDisplay, ColumnTitles
    global CartDrive, ScreenSize, ColumnSizes, SaveDir, AutoBackupSaves
    global AutoRestoreSaves, ScreenPos, OptionsSize, OptionsPos, NumSaves
    global CheckNewFilesOnStartup, ShowSplash, ScreenMaximize, CurrentRegion
    global SaveMgrColSizes, SaveMgrSize, CurrentSize, Sizes, Genres, Genre
    global SaveFilters, CurrentFilter, ShowROMSizeIn, CopyTrim
    
    if not SaveFilters:
        CurrentFilter = ""
        Genre = "Any Genre"
        CurrentSize = "Any Size"
        CurrentRegion = "Any Country"
        
    try:
        sf = open ( Filename, 'wb' )
        cPickle.dump ( ConfigVersion, sf )
        cPickle.dump ( ROMPaths, sf )
        cPickle.dump ( Columns, sf )
        cPickle.dump ( ColumnsToDisplay, sf )
        cPickle.dump ( ColumnTitles, sf )
        cPickle.dump ( ColumnSizes, sf )
        cPickle.dump ( CartDrive, sf )
        cPickle.dump ( ScreenSize, sf )
        cPickle.dump ( SaveDir, sf )
        cPickle.dump ( AutoBackupSaves, sf )
        cPickle.dump ( AutoRestoreSaves, sf )
        cPickle.dump ( ScreenPos, sf )
        cPickle.dump ( OptionsSize, sf )
        cPickle.dump ( OptionsPos, sf )
        cPickle.dump ( NumSaves, sf )
        cPickle.dump ( CheckNewFilesOnStartup, sf )
        cPickle.dump ( ShowSplash, sf )
        cPickle.dump ( ScreenMaximize, sf )
        cPickle.dump ( CurrentRegion, sf )
        cPickle.dump ( SaveMgrColSizes, sf )
        cPickle.dump ( SaveMgrSize, sf )
        cPickle.dump ( CurrentSize, sf )
        cPickle.dump ( Sizes, sf )
        cPickle.dump ( Genres, sf )
        cPickle.dump ( Genre, sf )
        cPickle.dump ( SaveFilters, sf )
        cPickle.dump ( CurrentFilter, sf )
        cPickle.dump ( ShowROMSizeIn, sf )
        cPickle.dump ( CopyTrim, sf )
        sf.close()
    except:
        pass

def Load( Filename ):
    global ConfigVersion, ROMPaths, Columns, ColumnsToDisplay, ColumnTitles
    global CartDrive, ScreenSize, ColumnSizes, SaveDir, AutoBackupSaves
    global AutoRestoreSaves, ScreenPos, OptionsSize, OptionsPos, NumSaves
    global CheckNewFilesOnStartup, ShowSplash, ScreenMaximize, CurrentRegion
    global SaveMgrColSizes, SaveMgrSize, CurrentSize, Sizes, Genres, Genre
    global SaveFilters, CurrentFilter, ShowROMSizeIn, CopyTrim
    try:
        sf = open ( Filename, 'rb' )
        ConfigVersion =  cPickle.load ( sf )
        ROMPaths = cPickle.load ( sf )
        Columns = cPickle.load ( sf )
        ColumnsToDisplay = cPickle.load ( sf )
        ColumnTitles = cPickle.load ( sf )
        ColumnSizes = cPickle.load ( sf )
        CartDrive = cPickle.load ( sf )
        ScreenSize = cPickle.load ( sf )
        SaveDir = cPickle.load ( sf )
        AutoBackupSaves = cPickle.load ( sf )
        AutoRestoreSaves = cPickle.load ( sf )
        ScreenPos = cPickle.load ( sf )
        OptionsSize = cPickle.load ( sf )
        OptionsPos = cPickle.load ( sf )
        NumSaves = cPickle.load ( sf )
        CheckNewFilesOnStartup = cPickle.load ( sf )
        ShowSplash = cPickle.load ( sf )
        ScreenMaximize = cPickle.load ( sf )
        CurrentRegion = cPickle.load ( sf )
        SaveMgrColSizes = cPickle.load ( sf )
        SaveMgrSize = cPickle.load ( sf )
        CurrentSize = cPickle.load ( sf )
        Sizes = cPickle.load ( sf )
        Genres = cPickle.load ( sf )
        Genre = cPickle.load ( sf )
        SaveFilters = cPickle.load ( sf )
        CurrentFilter = cPickle.load ( sf )
        ShowROMSizeIn = cPickle.load ( sf )
        CopyTrim = cPickle.load ( sf )
        sf.close()
    except:
        pass