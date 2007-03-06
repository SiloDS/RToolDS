#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

import sys
import os
import datetime
import array
import Image
import zipfile2
import wx
from stat import *
from struct import *
if sys.version_info[0] == 2 and sys.version_info[1] >= 5:
    from sqlite3 import dbapi2 as sqlite
else:
    from pysqlite2 import dbapi2 as sqlite
import MyConfig
import MyDuplicateDlg

MyConfig.DuplicateFiles = []

def ReadAddress ( Data, Offset ):
    return unpack ( "I", Data[Offset:Offset+4] )[0]

def GetImage( name, size, Logo=None, BinPal=None ):
    Pal=[]
    if Logo==None:
        fp=open( name, "rb" )
        Header=fp.read( 0x01ff )
        ImageLoc=ReadAddress ( Header, 0x68 )
        fp.seek( ImageLoc+32, 0 )
        Logo=array.array( 'B' )
        Logo.fromfile ( fp, 512 )
        BinPal=array.array( 'H' )
        BinPal.fromfile ( fp, 16 )

    for Count in range( 0, 16 ):
        red   =  ( BinPal[Count] & 31 ) << 3
        green = ( ( BinPal[Count] >> 5 ) & 31 ) << 3
        blue  = ( ( BinPal[Count] >> 10 ) & 31 ) << 3
        Pal.append ( ( red, green, blue ) )
    
    image = Image.new( "RGB", ( 32, 32 ) ) 
    imagesmall = Image.new( "RGB", ( 16, 16 ) )
    tile = Image.new( "RGB", ( 8, 8 ) )
    count = 0
    for a in range ( 0, 4 ):
        for b in range ( 0, 4 ):
            for y in range ( 0, 8 ):
                for x in range( 0, 8, 2 ):
                    pixel = Logo[count] & 15
                    pixelp1 = Logo[count] >> 4
                    count = count+1
                    tile.putpixel( ( x, y ), Pal[pixel] )
                    tile.putpixel( ( x+1, y ), Pal[pixelp1] )
                    image.paste ( tile, ( ( b*8 ), ( a*8 ) ) )
    imagesmall = image.resize( ( 16, 16 ) )
    if size == "Full":
        return image
    else:
        return imagesmall
    
def InsertDB( m_Con, Path, ShortName ):
    Process=False
    LongName = os.path.join ( Path, ShortName )
    if os.path.splitext( ShortName )[1].lower() == '.zip':
        file=zipfile2.ZipFile( LongName , "r" )

        for name in file.namelist():
            if os.path.splitext( name )[1].lower() == '.nds':
                ReleaseNumber=int ( ShortName[0:4] )
                DisplayName=os.path.splitext( name[7:] )[0]
                FileName=ShortName
                InternalZipName=name
                data = file.read_size( name, 0x01ff )
                ImageLoc=ReadAddress ( data, 0x68 )
                Header_Title = data[0x00:0x0C].strip()
                Header_Game_Code = data[0x0C:0x10].strip()
                Header_Maker_Code = data[0x10:0x12]
                ID = Header_Maker_Code + Header_Game_Code
                Header_Card_Size = 2^( 20+ord( data[0x14] ) )
                data = file.read_size( name, ImageLoc+32+512+32+256+256 )
                Logo=array.array( 'B', data[ImageLoc+32:ImageLoc+32+512] )
                BinPal=array.array( 'H', data[ImageLoc+32+512:ImageLoc+32+512+32] )
                zi=file.getinfo ( name )
                Size=zi.file_size
                Date=datetime.datetime( zi.date_time[0], zi.date_time[1], zi.date_time[2], zi.date_time[3], zi.date_time[4], zi.date_time[5] )
                Imagea = GetImage ( LongName, size="Full", Logo=Logo, BinPal=BinPal ).tostring()
                SmallImagea = GetImage ( LongName, size="Small", Logo=Logo, BinPal=BinPal ).tostring()
                data=array.array( 'u', data[ImageLoc+32+512+32+256:ImageLoc+32+512+32+256+256] )
                Header_Logo_Title=data.tounicode().encode( 'ascii', 'ignore' )
                for count in range( 0, len( Header_Logo_Title ) ):
                    if ord( Header_Logo_Title[count] )==0:
                        break
                Header_Logo_Title=Header_Logo_Title[0:count]
                Process=True
                break
    else:
        ReleaseNumber=int( ShortName[0:4] )
        DisplayName=os.path.splitext( ShortName[7:] )[0]
        FileName=ShortName
        InternalZipName=FileName
        fp=open( LongName, "rb" )
        Header=fp.read( 0x01ff )
        ImageLoc=ReadAddress ( Header, 0x68 )
        Header_Title = Header[0x00:0x0C].strip()
        Header_Game_Code = Header[0x0C:0x10].strip()
        Header_Maker_Code = Header[0x10:0x12]
        ID = Header_Maker_Code + Header_Game_Code
        Header_Card_Size = 2^( 20+ord( Header[0x14] ) )
        fp.seek( ImageLoc+32, 0 )
        Logo=array.array( 'B' )
        Logo.fromfile ( fp, 512 )
        BinPal=array.array( 'H' )
        BinPal.fromfile ( fp, 16 )
        Stat = os.stat( LongName )
        Size = Stat[ST_SIZE]
        Date = datetime.datetime.fromtimestamp( Stat[ST_MTIME] )
        Imagea = GetImage ( LongName, size="Full" ).tostring()
        SmallImagea = GetImage ( LongName, size="Small" ).tostring()
        fp.seek( ImageLoc+32+512+32+256, 0 )
        data=array.array( 'u' )
        data.fromfile ( fp, 256/2 )
        Header_Logo_Title=data.tounicode().encode( 'ascii', 'ignore' )
        for count in range( 0, len( Header_Logo_Title ) ):
            if ord( Header_Logo_Title[count] )==0:
                break
        Header_Logo_Title=Header_Logo_Title[0:count]
        Process=True
    if Process:
        Data = ( ID, ReleaseNumber, DisplayName, FileName, Path , InternalZipName, Size, Date, sqlite.Binary( Imagea ), sqlite.Binary( SmallImagea ), Header_Title, Header_Maker_Code, Header_Game_Code, Header_Card_Size, Header_Logo_Title, 0 ,-1)
  
        c = m_Con.cursor()
        try:
            c.execute ( "insert into Files values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", Data )
        except:
            MyConfig.DuplicateFiles.append (os.path.join (Path,FileName))
        try:
            c.execute ( "insert into Genre values (?,?,?)", (ReleaseNumber, "Unknown", None ))
        except:
            pass
        m_Con.commit()
        c.close()

def CountFiles( Paths, Extensions ):
    Count = 0
    for Path in Paths:
        DirList = os.listdir ( Path )
        for File in DirList:
            if os.path.isdir( File ):
                pass
            else:
                Ext = os.path.splitext( File )[1]
                if Ext in Extensions:
                    Count += 1
    return Count
    
    
def CreateDB( self, Paths, m_Con, Extensions ):
    MyConfig.DuplicateFiles = []
    c = m_Con.cursor()
    c.execute ( "delete from Files" )
    m_Con.commit()
    c.close()
    Count = 1
    NumFiles = CountFiles ( Paths, Extensions )
    dlg = wx.ProgressDialog( "Creating", 
                             "Database Creation in Progress 0/0", 
                              maximum = NumFiles+1, 
                              parent=self, 
                              style = wx.PD_APP_MODAL
                            )
    
    for Path in Paths:
        DirList = os.listdir ( Path )
        for File in DirList:
            if os.path.isdir( File ):
                pass
            else:
                Ext = os.path.splitext( File )[1]
                if Ext in Extensions:
                    InsertDB ( m_Con, Path, File )
                    dlg.Update( Count, "Database Creation in Progress %d/%d" % ( Count, NumFiles ) )
                    wx.Yield()
                    Count += 1
    dlg.Destroy()
    if MyConfig.DuplicateFiles != []:
        dlg = MyDuplicateDlg.MyDuplicateDlg ( self )
        dlg.ShowModal()
        dlg.Destroy()
       
    wx.Yield()

def UpdateDB( self, Paths, m_Con, Extensions ):
    FullList=[]
    for Path in Paths:
        DirList = os.listdir ( Path )
        for File in DirList:
            if os.path.isdir( File ):
                pass
            else:
                Ext = os.path.splitext( File )[1]
                if Ext in Extensions:
                    FullList.append ( os.path.join ( Path, File ) )
    NumFiles = len(FullList) + 1
    dlg = wx.ProgressDialog( "Updating", 
                             "Updating Database in Progress 0/0", 
                              maximum = NumFiles, 
                              parent=self, 
                              style = wx.PD_APP_MODAL
                            )
    
    c = m_Con.cursor()
    DBList = []
    c.execute ( "SELECT DirectoryName, FileName from Files;" )
    for Row in c:
        DBList.append ( os.path.join ( Row[0], Row[1] ) )
    Count = 0
    for File in FullList:
        dlg.Update( Count, "Updating Database in Progress %d/%d" % ( Count, NumFiles ) )
        wx.Yield()
        if File not in DBList:
            InsertDB ( m_Con, os.path.split( File )[0], os.path.split( File )[1] )
            Count += 1
    dlg.Destroy()
    return Count