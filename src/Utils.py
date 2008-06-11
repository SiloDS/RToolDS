# -*- coding: iso-8859-15 -*-

import wx
import socket
import urllib2
import cStringIO
import os
import sys
import time
import binascii
import tempfile
from struct import unpack
import array
import glob
import shutil
import base64
from PIL import Image #@UnresolvedImport
if sys.platform != "win32":
    from statvfs import F_BLOCKS, F_BAVAIL, F_FRSIZE
if sys.platform == "win32":
    import win32api
if ( sys.version_info[0] * 10 ) + sys.version_info[1] >= 25: #TODO: Fixme...
    import hashlib
else:
    import md5

import Config
import GFX

import zipfile2
Use_Zip = True

if sys.platform == "win32":
    from py7zlib2 import Archive7z
    Use_7Zip = True
else:
    Use_7Zip = False
    
if sys.platform == "win32":
    import UnRAR2 as UnRAR
    Use_RAR = True
else:
    Use_RAR = False

def Fetch_Master_List_Version ():
    try:
        socket.setdefaulttimeout( 30 )
        url = urllib2.urlopen ( Config.Config ["Master_XML_Version_URL"] )
        RetVal = int ( url.read() )
    except:
        RetVal = -1 #IGNORE:W0702
    
    return RetVal

def Fetch_Master_List ():
    try:
        socket.setdefaulttimeout( 30 )
        URL = urllib2.urlopen ( Config.Config ["Master_XML_URL"] )
        Data = URL.read()
    except:
        return False #IGNORE:W0702
    
    try:
        File_In_Memory = cStringIO.StringIO ( Data )
        File_In = zipfile2.ZipFile ( File_In_Memory )
        File_Out = open ( Config.Config ["Master_XML_File"], "wt" )
        File_Out.write ( File_In.read ( Config.Config ["Master_XML_File"] ) )
        File_Out.close()
        File_In.close()
    except:
        return False #IGNORE:W0702
    
    return True

def Get_CRC_or_Date ( Filename ):
    CRC  = []
    Date = []
    ROMFile = []
    
    if os.path.splitext( Filename )[1].lower() == ".zip" and Use_Zip:
        try:
            FileIn = zipfile2.ZipFile ( Filename , "r" )
            for File in FileIn.infolist():
                if os.path.splitext( File.filename )[1].lower() in Config.Config ["ROM_Extensions"]:
                    ROMFile.append( File.filename)
                    CRC.append (CRC2Hex ( File.CRC ))
                    Date.append ("")
        except:
            return ( [], [], [] ) #IGNORE:W0702
    elif os.path.splitext( Filename )[1].lower() == ".7z" and Use_7Zip:
        try:
            FileIn = open ( Filename , "rb" )
            archive = Archive7z ( FileIn )
            Filenames = archive.getnames()
            for File in Filenames:
                if os.path.splitext( File )[1].lower() in Config.Config ["ROM_Extensions"]:
                    ROMFile.append ( File )
                    cf = archive.getmember( File )
                    CRC.append (CRC2Hex ( cf.digest ))
                    Date.append ("")
        except:
            return ( [], [], [] ) #IGNORE:W0702
    elif os.path.splitext( Filename )[1].lower() == ".rar" and Use_RAR:
        try:
            for File in UnRAR.Archive( Filename ).iterfiles():
                if os.path.splitext( File.filename )[1].lower() in Config.Config ["ROM_Extensions"]:
                    ROMFile.append ( File.filename)
                    CRC.append (CRC2Hex ( File.crc ))
                    Date.append ("")
        except:
            return ( [], [], [] ) #IGNORE:W0702
    elif os.path.splitext( Filename )[1].lower() in Config.Config ["ROM_Extensions"]:
        try:
            Date.append ( time.strftime( "%d/%m/%Y %I:%M:%S %p", time.localtime( os.path.getmtime ( Filename ) ) ).lower())
            ROMFile.append (os.path.basename ( Filename ))
            CRC.append ("")
        except:
            return ( [], [], [] ) #IGNORE:W0702

    return ( CRC, Date, ROMFile )

def Get_File_CRC ( Filename ):
    In_File = open ( Filename, "rb" )
    Data = In_File.read()
    In_File.close()
    CRC = binascii.crc32( Data )
    del ( Data )
    return ( CRC2Hex ( CRC ) )

def Get_Data_CRC (Data):
    CRC = binascii.crc32( Data )
    return CRC2Hex (CRC)

def CRC2Hex ( CRC ):
    RetVal = ''
    for dummy_i in range ( 4 ):
        Temp = CRC & 0xFF
        CRC >>= 8
        RetVal = '%02X%s' % ( Temp, RetVal )
    return RetVal

def Check_CRC ( Filename, InCRC ):
    try:
        if os.path.isfile( Filename ):
            File_In = open ( Filename, "rb" )
            Data = File_In.read()
            File_In.close()
            CRC = binascii.crc32( Data )
            CRC = CRC2Hex ( CRC )
            del ( Data )
            if CRC == InCRC:
                return True
        return False
    except:
        return False

def Format_ROM_Size ( Number, Use_Space=True ):
    if Use_Space:
        Space_Char = " "
    else:
        Space_Char = ""
    
    if Number == -1:
        RetStr = "N/A"
    elif Config.Config ["Show_ROM_Size_In"] == "MegaBits":
        RetStr = str( ( Number/1024/1024 )* 8 )+Space_Char+"Mbit" 
    elif Config.Config ["Show_ROM_Size_In"] == "MegaBytes":
        RetStr = str( Number/1024/1024 )+Space_Char+"MB"
        if RetStr == "0"+Space_Char+"MB":
            RetStr = str( ( Number/1024 ) )+Space_Char+"KB"
    elif Config.Config ["Show_ROM_Size_In"] == "KiloBits":
        RetStr = str( ( Number/1024 )* 8 )+Space_Char+"Kbit" 
    elif Config.Config ["Show_ROM_Size_In"] == "KileBytes":
        RetStr = str( ( Number/1024 ) )+Space_Char+"KB"
    elif Config.Config ["Show_ROM_Size_In"] == "Bytes":
        RetStr = str( Number )+Space_Char+"B"
    else:
        RetStr = "Erm!!"

    return RetStr

def Format_Normal_Size ( Size, Use_Space=True ):
    if ( Size / 1024 / 1024 ) > 1023:
        return "%0.2f GB" % ( float ( Size ) / 1024 / 1024 / 1024 )
    elif ( Size / 1024 / 1024 ) == 0:
        return "%d KB" % (float ( Size ) / 1024)
    else:
        return "%d MB" % ( float ( Size ) / 1024 / 1024 )

def Create_Temp_Filename ():
    tmp = tempfile.mkstemp()
    TempFilename = tmp[1]
    tf = os.fdopen ( tmp[0], 'wb' )
    tf.close()
    os.unlink ( TempFilename )
    return TempFilename
    
def Read_Data ( Filename, ROMFile, Size=-1 ):
    TempFilename = ""
    Data = []
    OK = True
    
    try:
        if os.path.splitext( Filename )[1].lower() == ".zip" and Use_Zip:
            File = zipfile2.ZipFile ( Filename, "r" )
            if Size == -1:
                Data = File.read ( ROMFile )
            else:
                Data = File.read_size ( ROMFile, Size )
        elif os.path.splitext( Filename )[1].lower() == ".7z" and Use_7Zip:
            File = open ( Filename  , "rb" )
            archive = Archive7z ( File )
            cf = archive.getmember( ROMFile )
            Data = cf.read ()
        elif os.path.splitext( Filename )[1].lower() == ".rar" and Use_RAR:
            TempFilename = Create_Temp_Filename ()
            for ArchiveFile in UnRAR.Archive( Filename ).iterfiles():
                if ArchiveFile.filename == ROMFile:
                    ArchiveFile.extract ( TempFilename )
                    File=open ( TempFilename, "rb" )
                    if Size == -1:
                        Data = File.read()
                    else:
                        Data = File.read(Size)
                    File.close()
        else:
            File=open ( Filename, "rb" )
            if Size == -1:
                Data = File.read()
            else:
                Data = File.read(Size)
    except:
        OK = False                
    
    return ( OK, TempFilename, Data )

def Read_Address ( Data, Offset ):
    return unpack ( "I", Data[Offset:Offset+4] )[0]

def Get_Icon( Logo=None, BinPal=None ):
    Pal=[]

    for Count in range( 0, 16 ):
        red   =  ( BinPal[Count] & 31 ) << 3
        green = ( ( BinPal[Count] >> 5 ) & 31 ) << 3
        blue  = ( ( BinPal[Count] >> 10 ) & 31 ) << 3
        Pal.append ( ( red, green, blue ) )
    
    image = Image.new( "RGB", ( 32, 32 ) ) 
    tile = Image.new( "RGB", ( 8, 8 ) )
    count = 0
    for a in range ( 0, 4 ):
        for b in range ( 0, 4 ):
            for y in range ( 0, 8 ):
                for x in range( 0, 8, 2 ):
                    pixel = Logo[count] & 15
                    pixelp1 = Logo[count] >> 4
                    count = count + 1
                    tile.putpixel( ( x, y ), Pal[pixel] )
                    tile.putpixel( ( x+1, y ), Pal[pixelp1] )
                    image.paste ( tile, ( ( b*8 ), ( a*8 ) ) )
    return image

def Extract_Icon (Filename, ROMFile, TempFilename, Data):
    try:
        ImageLoc=Read_Address ( Data, 0x68 )
        Size = ImageLoc+32+512+32+256+256

        if os.path.splitext( Filename )[1].lower() == ".zip" and Use_Zip:
            File = zipfile2.ZipFile ( Filename, "r" )
            Data = File.read_size ( ROMFile, Size )
        elif os.path.splitext( Filename )[1].lower() == ".7z" and Use_7Zip:
            Data = Data [0:Size]
        elif os.path.splitext( Filename )[1].lower() == ".rar" and Use_RAR:
            File=open ( TempFilename, "rb" )
            Data = File.read(Size)
        else:
            File=open ( Filename, "rb" )
            Data = File.read(Size)

        Logo=array.array( 'B', Data[ImageLoc+32:ImageLoc+32+512] )
        BinPal=array.array( 'H', Data[ImageLoc+32+512:ImageLoc+32+512+32] )

        Icon = Get_Icon ( Logo=Logo, BinPal=BinPal )

        Icon_Filename = os.path.join ( Config.Config ["Image_Path"], os.path.splitext( os.path.basename ( Filename ) )[0] + ".png" )
        Icon.save( Icon_Filename, "PNG" )
        
        return Get_File_CRC (Icon_Filename)
    except:
        return ""

def Get_Serial (Data):
    try:
        Game_Code = str (Data [0x0C:0x10])
        Country_Code = Config.Config ["Country_Codes"][str (Data [0x0F])]
        Result = "NTR-%s-%s" % (Game_Code, Country_Code) 
        return Result  
    except:
        return ""
        

def Get_File_Size (Filename, ROMFile, TempFilename):
    Size = 0
    try:
        if os.path.splitext( Filename )[1].lower() == ".zip" and Use_Zip:
            File = zipfile2.ZipFile ( Filename, "r" )
            zi = File.getinfo ( ROMFile )
            Size = zi.file_size
        elif os.path.splitext( Filename )[1].lower() == ".7z" and Use_7Zip:
            File = open ( Filename  , "rb" )
            archive = Archive7z ( File )
            cf = archive.getmember( ROMFile )
            Size = cf.size
        elif os.path.splitext( Filename )[1].lower() == ".rar" and Use_RAR:
            for ArchiveFile in UnRAR.Archive( Filename ).iterfiles():
                if ArchiveFile.filename == ROMFile:
                    Size = ArchiveFile.size
        else:
            Size = os.path.getsize(Filename)
    except:
        pass
    
    return Size

if sys.platform == "win32":
    def Drive_Size ( Path ):
        return win32api.GetDiskFreeSpaceEx( Path )[1]

    def Drive_Free ( Path ):
        return win32api.GetDiskFreeSpaceEx( Path )[0]

else: # elif sys.platform == "linux2":
    def Drive_Size ( Path ):
#        os.stat
        try:
            ret = os.statvfs( Path )[F_FRSIZE ] * os.statvfs ( Path )[F_BLOCKS] #@UndefinedVariable
        except:
            ret = 0
        return ret
    
    def Drive_Free ( Path ):
        try:
            ret = os.statvfs( Path )[F_FRSIZE ] * os.statvfs ( Path )[F_BAVAIL] #@UndefinedVariable
        except:
            ret = 0
        return ret

def Get_Screenshot (ROM, W,H):
    try:
        if ROM.Comment [0] == "U":
            Filenameb = ""
        else:
            Filenameb = os.path.join ( Config.Config ["Image_Path"], "%04db.png" % ROM.Image_Number )
    
        Bitmap = None
        if os.path.isfile( Filenameb ):
            try:
                Bitmap = wx.Image( Filenameb, wx.BITMAP_TYPE_PNG ).Scale( W, H, wx.IMAGE_QUALITY_NORMAL ).ConvertToBitmap()
            except:
                Bitmap = GFX.getGFX_No_ScreenShotImage().Scale( W, H, wx.IMAGE_QUALITY_NORMAL ).ConvertToBitmap()
        else:
            Bitmap = GFX.getGFX_No_ScreenShotImage().Scale( W, H, wx.IMAGE_QUALITY_NORMAL ).ConvertToBitmap()
    except:
        Bitmap = GFX.getGFX_No_ScreenShotImage().Scale( W, H, wx.IMAGE_QUALITY_NORMAL ).ConvertToBitmap()
                
    return Bitmap
            
def Get_Case (ROM, W, H):
    try:
        if ROM.Comment [0] == "U":
            Filenamea = ""
        else:
            Filenamea = os.path.join ( Config.Config ["Image_Path"], "%04da.png" % ROM.Image_Number )
            
        Bitmap = None
        if os.path.isfile( Filenamea ):
            try:
                Bitmap = wx.Image( Filenamea, wx.BITMAP_TYPE_PNG ).Scale( W, H, wx.IMAGE_QUALITY_NORMAL ).ConvertToBitmap()
            except:
                Bitmap = GFX.getGFX_No_CaseImage().Scale( W, H, wx.IMAGE_QUALITY_NORMAL ).ConvertToBitmap()
        else:
            Bitmap = GFX.getGFX_No_CaseImage().Scale( W, H, wx.IMAGE_QUALITY_NORMAL ).ConvertToBitmap()
    except:
        Bitmap = GFX.getGFX_No_CaseImage().Scale( W, H, wx.IMAGE_QUALITY_NORMAL ).ConvertToBitmap()
        
    return Bitmap

def Get_NFO (ROM):
    NFO_Filename = os.path.join ( Config.Config ["NFO_Path"], "%04d.nfo" % ROM.Image_Number )
    if os.path.isfile( NFO_Filename ):
        File = open (NFO_Filename, "rt")
        Data = File.read ()
        File.close ()
        return Data
    elif os.path.splitext( ROM.Archive_File )[1].lower() == ".zip" and Use_Zip:
        try:
            File_In=zipfile2.ZipFile ( ROM.Archive_File , "r" )
            for File in File_In.infolist():
                if os.path.splitext( File.filename )[1].lower() == ".nfo":
                    Data = File_In.read ( File.filename )
                    return Data
        except:
            pass
    elif os.path.splitext( ROM.Archive_File )[1].lower() == ".7z" and Use_7Zip:
        try:
            File_In = open ( ROM.Archive_File  , "rb" )
            archive = Archive7z ( File_In )
            for File in archive.filenames:
                if os.path.splitext( File )[1].lower() == ".nfo":
                    cf = archive.getmember( File )
                    Data = cf.read ()
                    return Data
        except:
            pass
    elif os.path.splitext( ROM.Archive_File )[1].lower() == ".rar" and Use_RAR:
        try:
            TempFilename = Create_Temp_Filename ()
            for ArchiveFile in UnRAR.Archive( ROM.Archive_File ).iterfiles():
                if os.path.splitext( ArchiveFile.filename )[1].lower() == ".nfo":
                    ArchiveFile.extract ( TempFilename )
                    File=open ( TempFilename, "rt" )
                    Data = File.read ()
                    File.close ()
                    try:
                        os.unlink (TempFilename)
                    except:
                        pass
                    return Data
        except:
            pass

    return ""

def Directory_Range ( Number ): # Advanscene's Directory
    t = ( Number - 1 ) / 500
    return "%d-%d" % ( ( t * 500 ) + 1, ( t * 500 ) + 500 )

def GetFromWeb ( Url, Filename ):
    try:
        socket.setdefaulttimeout( 30 )
        url = urllib2.urlopen ( Url )
        data = url.read()
    except:
        return 1 #IGNORE:W0702
    
    FileOut=open ( Filename, "wb" )
    FileOut.write ( data )
    FileOut.close()
    
    return 0

def Get_Hash ( Filename ):
    try:
        File_In = open( Filename, "rb" )
        Data = File_In.read()
        File_In.close ()
        RetVal = Get_Hash_Data (Data)
    except:
        RetVal = 0  
    return RetVal

def Get_Hash_Data ( Data ):
    if ( sys.version_info[0] * 10 ) + sys.version_info[1] >= 25: #TODO: Fixme...
        md5hash = hashlib.md5()
    else:
        md5hash = md5.new()
    md5hash.update( Data )
    return md5hash.hexdigest()

def Add_Save (ROM, Save, SaveCommentsShelve, Save_ROMS, Auto = False):
    Save_Created = False
#    SaveName = os.path.join ( Config.Config ["Save_Path"], ROM.ROM_CRC + Get_Save_Extension() )
    SaveName = os.path.join ( Config.Config ["Save_Path"], ROM.ROM_CRC + ".sav" )
    CartHash = Get_Hash( Save )

    if os.path.isfile ( SaveName + ".001" ):
        Found = False
        for a in range (1,Config.Config ["Save_Games_to_Keep"]+1):
            if Get_Hash( SaveName + ".%03d" % a ) == CartHash:
                Found = True
        if not Found:
            Save_Created = True
            for Count in range ( Config.Config ["Save_Games_to_Keep"]-1, 0, -1 ):
                if os.path.isfile ( SaveName + ".%03d" % Count ):
                    shutil.move( SaveName + ".%03d" % ( Count ), SaveName + ".%03d" %  (Count+1) )
                    if SaveCommentsShelve.has_key( str ( ROM.ROM_CRC + "%03d" % ( Count ) ) ):
                        SaveCommentsShelve [str ( ROM.ROM_CRC + "%03d" %( Count+1 ) )] = SaveCommentsShelve [str ( ROM.ROM_CRC +"%03d" % ( Count ) )]
                        SaveCommentsShelve.sync ()
            shutil.copy2 ( Save, SaveName + ".001" )
            if Auto == False:
                SaveCommentsShelve[str (ROM.ROM_CRC+"001")] = ""
            else:
                SaveCommentsShelve[str (ROM.ROM_CRC+"001")] = _("Auto") + " %s" % ROM.Name_On_Device
                
            SaveCommentsShelve.sync ()
            Save_Created = True
    else:
        shutil.copy2 ( Save, SaveName + ".001" )
        if Auto == False:
            SaveCommentsShelve[str (ROM.ROM_CRC+"001")] = ""
        else:
            SaveCommentsShelve[str (ROM.ROM_CRC+"001")] = _("Auto") + " %s" % ROM.Name_On_Device
        SaveCommentsShelve.sync ()
        Save_Created = True

    if Config.Config ["Use_Original_Save_Time"] == False:
        os.utime( SaveName + ".001", None )

    ROM.Saves = len (glob.glob (SaveName + ".*"))

    if Save_Created: 
        Save_ROMS.append( ROM )
        
    return Save_Created

def Rename_ROM (ROM):
    Mask = Config.Config ["Rename_Mask"]
    
    Mask = Mask.replace ("(T)", ROM.Title)
    Mask = Mask.replace ("(N)", ROM.Comment)
    Mask = Mask.replace ("(G)", ROM.Source_ROM)
    Mask = Mask.replace ("(P)", ROM.Publisher)
    Mask = Mask.replace ("(S)", ROM.Save_Type)
    Mask = Mask.replace ("(C)", ROM.ROM_CRC)
    try:
        Mask = Mask.replace ("(R)", Config.Config ["Locations"][ROM.Location])
    except:
        Mask = Mask.replace ("(R)", _("Unknown"))
    
    Mask = Mask + (".nds")
    
    return Mask

def Get_Name_on_Device (ROM, Path = "Device_Path"):
    if ROM.Found == False:
        return ""
    if Config.Config ["Use_Renaming"]:
        Filename = os.path.join ( Config.Config[Path], Rename_ROM (ROM) )
    else:
        Filename = os.path.join ( Config.Config[Path], ROM.ROM_File )
    
    return Filename

def Get_Savename_on_Device (ROM):
    if Config.Config ["UseShortSaveName"] and sys.platform == "win32":
        try:
            Short_Save_Filename = win32api.GetShortPathName( ROM.Name_On_Device )
            SaveFileName = os.path.splitext(Short_Save_Filename)[0] + Get_Save_Extension().upper()
            return SaveFileName
        except:
            pass

#    try:
#        SaveFilename = os.path.splitext (ROM.Name_On_Device)[0] + Get_Save_Extension()
#    except:
    SaveFilename = Get_Name_on_Device (ROM, "Save_Dir_On_Cart" )
    SaveFilename = os.path.splitext(SaveFilename)[0] + Get_Save_Extension()
    
    return SaveFilename

def Write_Save (ROM, Save, Alternate_Name = ""):
    if Alternate_Name == "":
        SaveFileName = Get_Savename_on_Device (ROM)
    else:
        SaveFileName = Alternate_Name
#    SaveFile = open (SaveFileName,"wb")
#    SaveFile.write ( Save )
#    SaveFile.close()
    for Device in Config.Config ["Devices"]:
#        print Device [0] + " : " + Config.Config ["Default_Device"][0]
        if Device [0] == Config.Config ["Default_Device"]: #[0]:
            Routine = Device[1]
            
    try:
        Routine ("WRITE",SaveFileName,Save)
    except:
        pass
    
ARHeader  = '''QVJEUzAwMDAwMDAwMDAwMUMAbwBuAHYAZQByAHQAZQBkACAAUwBhAHYAZQBnAGEAbQBlAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAABTAGEAdgBlAGcAYQBtAGUAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAUyBoIHUgbiB5AAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AABjb252AAAAAAAAAAAAAAAAAAAAAAAAAC8AAP81c2h1bnkgY29udgAAAAAAAAAAAAAAAAAAAAAA
AAAAAABzaG55AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA='''

def Device_Action_Replay (Function, Arg1 = None, Arg2 = None):
    if Function == "SIZE":
        return 262144 + 500
    elif Function == "READ":
        Save_File = open (Arg1,"rb")
        Data = Save_File.read ()
        Save_File.close()
        
        Data = Data [500:]
        while len (Data) < 524288:
            Data += chr (255)
        
        return Data
    elif Function == "WRITE":
        if len (Arg2) != 262144 + 500: # Not in AR format
            if len (Arg2) < 262144:
                Data = Arg2
                a = chr(255)
                while len (Data) < 262144:
                    Data += a
            else:
                Data = Arg2[:262144]
            hdecode = base64.decodestring(ARHeader)
            Data = hdecode + Data
        else:
            Data = Arg2
        File = open (Arg1,"wb")
        File.write (Data)
        File.close()

def Device_Generic_512 (Function, Arg1=None, Arg2 = None):
    if Function == "SIZE":
        return 524288
    elif Function == "READ":
        Save_File = open (Arg1,"rb")
        Data = Save_File.read ()
        Save_File.close()
        a = chr(255)
        while len (Data) < 524288:
            Data += a
        return Data
    elif Function == "WRITE":
        if len (Arg2) != 524288:
            if len (Arg2) < 524288:
                Data = Arg2
                a = chr(255)
                while len (Data) < 524288:
                    Data += a
            else:
                Data = Arg2[Data:524288]
        else:
            Data = Arg2
        
        File = open (Arg1,"wb")
        File.write (Data)
        File.close()

def Device_Generic_256 (Function, Arg1=None, Arg2 = None):
    if Function == "SIZE":
        return 262144
    elif Function == "READ":
        Save_File = open (Arg1,"rb")
        Data = Save_File.read ()
        Save_File.close()
        
        a = chr(255)
        while len (Data) < 524288:
            Data += a
        
        return Data
    elif Function == "WRITE":
        if len (Arg2) != 262144:
            if len (Arg2) < 262144:
                Data = Arg2
                a = chr(255)
                while len (Data) < 262144:
                    Data += a
            else:
                Data = Arg2[:262144]
        else:
            Data = Arg2

        File = open (Arg1,"wb")
        File.write (Data)
        File.close()

def Device_R4_512 (Function, Arg1=None, Arg2=None):
    if Function == "SIZE":
        return 524288
    elif Function == "READ":
        Save_File = open (Arg1,"rb")
        Data = Save_File.read ()
        Save_File.close()
        
        a = chr(0)
        while len (Data) < 524288:
            Data += a
        
        return Data
    elif Function == "WRITE":
        if len (Arg2) != 524288:
            if len (Arg2) < 524288:
                Data = Arg2
                a = chr(0)
                while len (Data) < 524288:
                    Data += a
            else:
                Data = Arg2[:524288]
        else:
            Data = Arg2
            
        File = open (Arg1,"wb")
        File.write (Data)
        File.close()

def Unique(s):
    """Return a list of the elements in s, but without duplicates.
   
    For example, unique([1,2,3,1,2,3]) is some permutation of [1,2,3],
    unique("abcabc") some permutation of ["a", "b", "c"], and
    unique(([1, 2], [2, 3], [1, 2])) some permutation of
    [[2, 3], [1, 2]].
    
    For best speed, all sequence elements should be hashable.  Then
    unique() will usually work in linear time.
    
    If not possible, the sequence elements should enjoy a total
    ordering, and if list(s).sort() doesn't raise TypeError it's
    assumed that they do enjoy a total ordering.  Then unique() will
    usually work in O(N*log2(N)) time.
    
    If that's not possible either, the sequence elements must support
    equality-testing.  Then unique() will usually work in quadratic
    time.
    """
    
    n = len(s)
    if n == 0:
        return []
    
    # Try using a dict first, as that's the fastest and will usually
    # work.  If it doesn't work, it will usually fail quickly, so it
    # usually doesn't cost much to *try* it.  It requires that all the
    # sequence elements be hashable, and support equality comparison.
    u = {}
    try:
        for x in s:
            u[x] = 1
    except TypeError:
        del u  # move on to the next method
    else:
        return u.keys()
    
    # We can't hash all the elements.  Second fastest is to sort,
    # which brings the equal elements together; then duplicates are
    # easy to weed out in a single pass.
    # NOTE:  Python's list.sort() was designed to be efficient in the
    # presence of many duplicate elements.  This isn't true of all
    # sort functions in all languages or libraries, so this approach
    # is more effective in Python than it may be elsewhere.
    try:
        t = list(s)
        t.sort()
    except TypeError:
        del t  # move on to the next method
    else:
        assert n > 0
        last = t[0]
        lasti = i = 1
        while i < n:
            if t[i] != last:
                t[lasti] = last = t[i]
                lasti += 1
            i += 1
        return t[:lasti]
   
    # Brute force is all that's left.
    u = []
    for x in s:
        if x not in u:
            u.append(x)
    return u

def Sort_Dict(d):
    """ Returns the keys of dictionary d sorted by their values """
    items=d.items()
    backitems=[ [v[1],v[0]] for v in items]
    backitems.sort()
    return [ backitems[i][1] for i in range(0,len(backitems))]

def Get_Save_Extension ():
    Device = Config.Config ["Default_Device"]# [0]
    if Device == "Action Replay (.duc/.dss)":
        exten = ".duc"
    else:
        exten = Device[Device.find('(')+1:Device.find(')')]

    return exten

def cbool (value):
    if value:
        return _("Yes")
    return _("No")

# caselesssort.py
# A sort function for lists of strings that is case insensitive.

# Copyright Michael Foord
# You are free to modify, use and relicense this code.

# No warranty express or implied for the accuracy, fitness to purpose or otherwise for this code....
# Use at your own risk !!!

# E-mail michael AT foord DOT me DOT uk
# Maintained at www.voidspace.org.uk/atlantibots/pythonutils.html
    
"""
The built in sort method for lists is case sensitive.
This means it can be unsuitable for sorting some lists of strings.
e.g. ['Apple', 'Pear', 'apple'].sort() 
leaves 'Apple' and 'apple' at opposite ends of the list.

You can pass in a function to the sort method - but this can be very slow.
cSort still uses the sort method, so there isn't much performance hit, but it is caseless.
cSort can handle non-string members in the list without failing.

In addition cSort will sort any sets of entries for which entry1.lower() == entry2.lower()
i.e. cSort(['fish', 'FISH', 'fIsh'])
returns ['FISH', 'fIsh', 'fish']
You can turn this behaviour off by passing cSort an optional 'False' parameter.
 i.e. cSort(['fish', 'FISH', 'fIsh'], False)
returns ['fish', 'FISH', 'fIsh']
"""

def cSort(inlist, minisort=True):
    sortlist = []
    newlist = []
    sortdict = {}
    for entry in inlist:
        try:
            lentry = entry.lower()
        except AttributeError:
            sortlist.append(lentry)
        else:
            try:
                sortdict[lentry].append(entry)
            except KeyError:
                sortdict[lentry] = [entry]
                sortlist.append(lentry)

    sortlist.sort()
    for entry in sortlist:
        try:
            thislist = sortdict[entry]
            if minisort: thislist.sort()
            newlist = newlist + thislist
        except KeyError:
            newlist.append(entry)
    return newlist

def unique(seq, keepstr=True):
    t = type(seq)
    if t in (unicode, str):
        t = (list, t('').join)[bool(keepstr)]
    try:
        remaining = set(seq)
        seen = set()
        return t(c for c in seq if (c in remaining and
                                    not remaining.remove(c)))
    except TypeError: # hashing didn't work, see if seq is sortable
        try:
            from itertools import groupby
            s = sorted(enumerate(seq),key=lambda (i,v):(v,i))
            return t(g.next() for dummy_k,g in groupby(s, lambda (i,v): v))
        except:  # not sortable, use brute force
            seen = []
            return t(c for c in seq if not (c in seen or seen.append(c)))
