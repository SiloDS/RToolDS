# -*- coding: iso-8859-1 -*-

import xml.dom.minidom
import cPickle
import os
import copy
import time
import shelve
import glob
import wx

import Config
import Utils

Master_List_Dat_Version = 7
Unknown_Shelve = None # Unknown ROMs
Trimmed_Shelve = None
Tag_Shelve = None

class ROM:
    def __init__ ( self ):
        self.Image_Number   = 0
        self.Release_Number = 0
        self.Title          = ""
        self.Save_Type      = _( "Unknown" )
        self.ROM_Size       = 0
        self.Publisher      = _( "Unknown" )
        self.Location       = 254
        self.Language       = 0
        self.Source_ROM     = _( "Unknown" )
        self.Comment        = 0
        self.ROM_CRC        = ""
        self.Archive_File   = ""
        self.Archive_Date   = ""
        self.ROM_File       = ""
        self.Im1_CRC        = ""
        self.Im2_CRC        = ""
        self.Ico_CRC        = ""
        self.Nfo_CRC        = ""
        self.Saves          = 0
        self.Trimmed        = False
        self.Effective_Size = 0
        self.Orig_Genre     = _( "Unknown" )
        self.Genre          = _( "Unknown" )
        self.Internal_Name  = _( "Unknown" )
        self.Serial         = _( "Unknown" )
        self.Version        = _( "Unknown" )
        self.Wifi           = False
        self.Tags           = []
        self.Trimmed_CRC    = ""
        self.Found          = False
        self.Dump_Date      = _( "Unknown" )
        self.Duplicate_ID   = "0"
        self.Orig_Filename  = ""
        
    def Trim ( self ):
        global TrimmedShelve
        
        OK, TempFileName, Data = Utils.Read_Data ( self.Archive_File, self.ROM_File )

        if OK:
            First = True
            Count = self.ROM_Size
            c = 0
            while Count > 0:
                c += 1
                if c == 1024:
                    wx.YieldIfNeeded()
                    c = 0
                Count -= 1
                if First:
                    TrimChar = Data[Count]
                    First = False
                if Data [Count] != TrimChar:
                    EndFound = Count + 1
                    break
            TrimSize = EndFound

            Data = Data[:TrimSize + Config.Config["Safe_Trim"]]
            Trimmed_CRC = Utils.Get_Data_CRC ( Data )
            Trimmed_Shelve [str (self.ROM_CRC)] = ( TrimSize, Trimmed_CRC )
            Trimmed_Shelve.sync()
            
            self.Trimmed = True
            self.Effective_Size = TrimSize + Config.Config ["Safe_Trim"]
            self.Trimmed_CRC = Trimmed_CRC
        else:
            TrimSize = -1
            
        if TempFileName:
            try:
                os.unlink( TempFileName )
            except:
                pass
            
        del Data
        
        return ( OK, TrimSize )

    def Un_Trim ( self ):
        global Trimmed_Shelve
        
        try:
            del ( Trimmed_Shelve [str ( self.ROM_CRC )] )
            Trimmed_Shelve.sync()
        except:
            pass
        
        self.Trimmed = False
        self.Effective_Size = self.ROM_Size
        self.Trimmed_CRC = ""

        return ( True, self.Effective_Size )
    
    def Add_Tag (self, Tag):
        global Tag_Shelve
        
        if Tag not in self.Tags:
            if self.Tags == []:
                Tag_Shelve [str ( self.ROM_CRC )] = [ Tag ]
                self.Tags = [ Tag ]
            else:
                try:
                    tmp = Tag_Shelve [str ( self.ROM_CRC )]
                except:
                    tmp = []
                tmp.append ( Tag )
                Tag_Shelve [str ( self.ROM_CRC )] = tmp
                self.Tags.append(Tag)

            try:
                if Tag not in Tag_Shelve ["Tags"] and Tag != _("Hidden ROMs"):
                    tmp = Tag_Shelve ["Tags"]
                    tmp.append ( Tag )
                    Tag_Shelve ["Tags"] = tmp
            except:
                if Tag != _("Hidden ROMs"):
                    Tag_Shelve ["Tags"] = [ Tag ]

            Tag_Shelve.sync()

    def Remove_Tag (self, Tag):
        global Tag_Shelve
        
        if Tag in self.Tags:
            self.Tags.remove (Tag)
            Tag_Shelve [str ( self.ROM_CRC )] = self.Tags
            Tag_Shelve.sync()
            
    def Get_ROM_Data (self, Get_Save=False):
        Save = []

        OK, TempFilename, Data = Utils.Read_Data ( self.Archive_File, self.ROM_File )
            
        if TempFilename:
            try:
                os.unlink( TempFilename )
            except:
                pass
        
        if Get_Save:
            try:
                File = open ( os.path.join ( Config.Config ["Save_Path"], self.ROM_CRC + ".sav.001" ), "rb" )
                Save = File.read ()
                File.close ()
            except:
                pass

        return ( OK, Data, Save )

    def Get_ROM_Save (self):
        Save = []

        try:
            File = open ( os.path.join ( Config.Config ["Save_Path"], self.ROM_CRC + ".sav.001" ), "rb" )
            Save = File.read ()
            File.close ()
        except:
            pass

        return ( Save )
    
    def Get_Country (self):
        OK, TempFilename, Data = Utils.Read_Data ( self.Archive_File, self.ROM_File, 0x20 )
            
        if OK:
            return str (Data [0x0F]), Utils.Get_Serial(Data)

    
class ROMS:
    def __init__ ( self ):
        global Unknown_Shelve
        global Trimmed_Shelve
        global Tag_Shelve

        self.Master_List = []
        self.Master_List_Count = 0
        self.Master_List_XML_Version = 0
        self.Master_List_CRC_Dict = {}
        self.Master_List_Filename_Dict = {}
        self.Master_List_Serial_Dict = {}
        self.Genres = []
        
        self.Process_All = False
        
        self._AllGenres = _( "All Genres" )
        self._AllTags = _("All ROMs")
        self._Hidden_ROMs = _("Hidden ROMs")
        
        self.Open_Unknown_Shelve ()
        self.Open_Trimmed_Shelve ()
        self.Open_Tag_Shelve ()
        
    def Get_XML_Version( self ):
        Version = 0
        
        try:
            File = open ( Config.Config ["Master_XML_File"], "rt" )
        except:
            return Version
        
        for Line in File:
            Line = Line.strip()
            if Line[0:12] == "<datVersion>":
                try:
                    Version = int ( Line [12:Line[12:].find( '<' )+12] )
                except:
                    pass
                break
        
        File.close()
        
        return Version

    def Load_Master_List ( self, AltName=False ):
        global Master_List_Dat_Version

        Create_Master_List = False
        Merge_Master_List = False
        
        try:
            if AltName == False:
                Pickle_File = open ( "RToolDS_Master_List.dat", "rb" )
            else:
                Pickle_File = open ( "RToolDS_Master_List.dat.bak", "rb" )
            
            tmp = cPickle.load( Pickle_File )
            if Master_List_Dat_Version != tmp:
                Create_Master_List = True
            
            self.Master_List_XML_Version = cPickle.load( Pickle_File )
            if self.Master_List_XML_Version != self.Get_XML_Version():
                Merge_Master_List = True

            if Merge_Master_List == False and Create_Master_List == False:
                self.Master_List          = cPickle.load ( Pickle_File )
                self.Master_List_Count    = cPickle.load ( Pickle_File )
                self.Master_List_CRC_Dict = cPickle.load ( Pickle_File )
                self.Master_List_Filename_Dict = cPickle.load ( Pickle_File )
                self.Master_List_Serial_Dict = cPickle.load ( Pickle_File )
                self.Genres               = cPickle.load ( Pickle_File )
#                self.Unknown_Count        = cPickle.load ( Pickle_File )

            Pickle_File.close ()
            Result = True
        except:
            Create_Master_List = True
        
        if Create_Master_List:
            Result = self.Create_Master_List( False )
            
        if Merge_Master_List:
            Result = self.Create_Master_List ( True )
            
        self.Merge_Saves ()
        self.Merge_Trim ()
        self.Sort_Current_List ()
        self.Populate_Current_List ()
        
        return Result
        
    def Create_Master_List( self, Merge ):
        global Master_List_Dat_Version
        
        if Merge:
            old_Master_List = copy.copy ( self.Master_List )
            old_Master_List_Count = copy.copy ( self.Master_List_Count )
            old_Master_List_CRC_Dict = copy.copy ( self.Master_List_CRC_Dict )
            old_Master_List_Filename_Dict = copy.copy ( self.Master_List_Filename_Dict )
            old_Master_List_Serial_Dict = copy.copy ( self.Master_List_Serial_Dict )
            old_Genres = copy.copy ( self.Genres )
        self.Master_List = []
        self.Master_List_Count = 0
        self.Master_List_CRC_Dict = {}
        self.Master_List_Filename_Dict = {}
        self.Master_List_Serial_Dict = {}
        self.Genres = []
       
        try:
            dom = xml.dom.minidom.parse( Config.Config ["Master_XML_File"] )
        except:
            if Merge:
                self.Master_List = old_Master_List
                self.Master_List_Count = old_Master_List_Count
                self.Master_List_CRC_Dict = old_Master_List_CRC_Dict
                self.Master_List_Filename_Dict = old_Master_List_Filename_Dict
                self.Master_List_Serial_Dict = old_Master_List_Serial_Dict
                self.Genres = old_Genres
            return False
        
        self.Master_List_XML_Version = int ( dom.getElementsByTagName ( "datVersion" )[0].childNodes[0].data )

        Games = dom.getElementsByTagName( "game" )

        for Game in Games:
            tmpROM = ROM()
            tmpROM.Image_Number   = int ( self.getText( Game.getElementsByTagName( "imageNumber" ) ) )
            tmpROM.Release_Number = int ( self.getText( Game.getElementsByTagName( "releaseNumber" ) ) )
            tmpROM.Title          = self.getText( Game.getElementsByTagName( "title" ) )
            tmpROM.Save_Type      = self.getText( Game.getElementsByTagName( "saveType" ) )
            tmpROM.ROM_Size       = int ( self.getText( Game.getElementsByTagName( "romSize" ) ) )
            tmpROM.Publisher      = self.getText( Game.getElementsByTagName( "publisher" ) )
            tmpROM.Location       = int ( self.getText( Game.getElementsByTagName( "location" ) ) )
            tmpROM.Source_ROM     = self.getText( Game.getElementsByTagName( "sourceRom" ) )
            tmpROM.Language       = int ( self.getText( Game.getElementsByTagName( "language" ) ) )
            tmpROM.Comment        = self.getText( Game.getElementsByTagName( "comment" ) )
            tmpROM.Im1_CRC        = self.getText( Game.getElementsByTagName( "im1CRC" ) )
            tmpROM.Im2_CRC        = self.getText( Game.getElementsByTagName( "im2CRC" ) )
            tmpROM.Ico_CRC        = self.getText( Game.getElementsByTagName( "icoCRC" ) )
            tmpROM.Nfo_CRC        = self.getText( Game.getElementsByTagName( "nfoCRC" ) )
            tmpROM.ROM_CRC        = self.getText( Game.getElementsByTagName( "romCRC" ) )
            tmpROM.Genre          = self.getText( Game.getElementsByTagName( "genre" ) )
            tmpROM.Orig_Genre     = tmpROM.Genre
            tmpROM.Internal_Name  = self.getText( Game.getElementsByTagName( "internal_name" ) )
            tmpROM.Serial         = self.getText( Game.getElementsByTagName( "serial" ) )
            tmpROM.Version        = self.getText( Game.getElementsByTagName( "version" ) )
            tmpROM.Effective_Size = tmpROM.ROM_Size
            tmpROM.Dump_Date      = self.getText( Game.getElementsByTagName( "dumpdate" ) )
            tmpROM.Duplicate_ID   = self.getText( Game.getElementsByTagName( "duplicateid" ) )
            tmpROM.Orig_Filename  = self.getText( Game.getElementsByTagName( "filename" ) )
            
            if self.getText( Game.getElementsByTagName( "wifi" ) ).lower () == "no":
                tmpROM.Wifi = False
            else:
                tmpROM.Wifi = True
                
            # Copy Over Original Fields
            if Merge:
                try:
                    origROM = old_Master_List [old_Master_List_CRC_Dict [tmpROM.ROM_CRC]]
                    tmpROM.Genre = origROM.Genre
                    tmpROM.Found = origROM.Found
                    tmpROM.Archive_File = origROM.Archive_File
                    tmpROM.Archive_Date = origROM.Archive_Date
                    tmpROM.ROM_File = origROM.ROM_File
                    tmpROM.Tags = origROM.Tags
                    tmpROM.Effective_Size = origROM.Effective_Size
                    tmpROM.Trimmed = origROM.Trimmed
                    tmpROM.Trimmed_CRC = origROM.Trimmed_CRC
                    tmpROM.Saves = origROM.Saves
                    self.Master_List_Filename_Dict [tmpROM.ROM_File] = tmpROM.Release_Number
                except:
                    pass
                
            if tmpROM.Genre not in self.Genres:
                self.Genres.append( tmpROM.Genre )
                self.Genres.sort()
                
            self.Master_List.append ( tmpROM )
            self.Master_List_CRC_Dict [tmpROM.ROM_CRC] = self.Master_List_Count
            self.Master_List_Serial_Dict [str ( tmpROM.Serial )] = self.Master_List_Count

            self.Master_List_Count += 1

        dom.unlink()
        
        self.Unknown_Count = 1
#        if Merge:
#            for tmpROM in old_Master_List:
#                if tmpROM.Comment [0] == "U":
#                    tmpROM.Comment = "U%03d" %self.Unknown_Count
#                    tmpROM.Image_Number = self.Master_List_Count + self.Unknown_Count
#                    tmpROM.Release_Number = tmpROM.Image_Number
#                    self.Master_List.append (tmpROM)
#                    self.Master_List_CRC_Dict [tmpROM.ROM_CRC] = self.Master_List_Count
#                    self.Master_List_Filename_Dict [tmpROM.ROM_File] = tmpROM.Release_Number
#        
#                    Unknown_Shelve [str ( tmpROM.ROM_CRC )] = tmpROM
#                    Unknown_Shelve [str ( tmpROM.Release_Number ) ] = str ( tmpROM.ROM_CRC )
#                    Unknown_Shelve.sync() 
#                    self.Unknown_Count += 1
#            self.Master_List_Count += self.Unknown_Count - 1
        
        self.Save_Master_List ()
        
        return True
    
    def Save_Master_List ( self, AltName = False ):
        global Master_List_Dat_Version

        if AltName == False:
            Pickle_File = open ( "RToolDS_Master_List.dat", "wb" )
        else:
            Pickle_File = open ( "RToolDS_Master_List.dat.bak", "wb" )
        cPickle.dump( Master_List_Dat_Version, Pickle_File )
        cPickle.dump( self.Master_List_XML_Version, Pickle_File )
        cPickle.dump( self.Master_List, Pickle_File )
        cPickle.dump( self.Master_List_Count, Pickle_File )
        cPickle.dump( self.Master_List_CRC_Dict, Pickle_File )
        cPickle.dump( self.Master_List_Filename_Dict, Pickle_File )
        cPickle.dump( self.Master_List_Serial_Dict, Pickle_File )
        cPickle.dump( self.Genres, Pickle_File )
#        cPickle.dump( self.Unknown_Count, Pickle_File )
        Pickle_File.close()
        
    def Merge_Saves (self):
        for ROM in self.Master_List:
            ROM.Saves = 0
        Saves = glob.glob (os.path.join (Config.Config ["Save_Path"],"*.001"))
        Saves.sort ()
        for Save in Saves:
            CRC = os.path.basename(Save)
            CRC = os.path.splitext(CRC)[0]
            CRC = str (os.path.splitext(CRC)[0])
            try:
                ROM = self.Lookup_ROM_CRC(CRC)
                ROM.Saves = len (glob.glob (os.path.splitext (Save)[0] + ".*"))
            except:
                pass

    def Merge_Trim (self):
        global Trimmed_Shelve

        for ROM in self.Master_List:
            ROM.Trimmed = False
            ROM.Effective_Size = ROM.ROM_Size
            if Trimmed_Shelve.has_key( str ( ROM.ROM_CRC ) ) == True:
                TrimSize, Trimmed_CRC = Trimmed_Shelve [str (ROM.ROM_CRC)]
                ROM.Trimmed = True
                ROM.Effective_Size = TrimSize + Config.Config ["Safe_Trim"]
                ROM.Trimmed_CRC = Trimmed_CRC

    def getText( self, nodelist ):
        nodelist = nodelist[0].childNodes
        rc = ""
        for node in nodelist:
            if node.nodeType == node.TEXT_NODE:
                rc = rc + node.data
        return rc
    
    def Lookup_ROM_CRC ( self, CRC ):
        return self.Master_List [ self.Master_List_CRC_Dict [CRC]]
    
    def Lookup_ROM_Filename ( self, Filename ):
        return self.Master_List [ self.Master_List_Filename_Dict [Filename]]
    
    def Lookup_ROM_Serial ( self, MySerial ):
        return self.Master_List [ self.Master_List_Serial_Dict [str ( MySerial )]]
    
    def Get_Current_List_ROM ( self, Position ):
        return self.Master_List [ self.Current_List [Position]]

    def Sort_Current_List ( self ):
        if Config.Config ["Sort"] == "Size":
            self.Master_List.sort ( key=lambda x:x.Title, reverse=False )
            self.Master_List.sort ( key=lambda x:x.Effective_Size, reverse=Config.Config["Sort_Reverse"] )
        elif Config.Config ["Sort"] == "Trimmed":
            self.Master_List.sort ( key=lambda x:x.Comment, reverse=Config.Config["Sort_Reverse"] )
            self.Master_List.sort ( key=lambda x:x.Trimmed, reverse=Config.Config["Sort_Reverse"] )
        elif Config.Config ["Sort"] == "Saves":
            self.Master_List.sort ( key=lambda x:x.Comment, reverse=Config.Config["Sort_Reverse"] )
            self.Master_List.sort ( key=lambda x:x.Saves, reverse=Config.Config["Sort_Reverse"] )
        elif Config.Config ["Sort"] == "Archive":
            self.Master_List.sort ( key=lambda x:x.Comment, reverse=Config.Config["Sort_Reverse"] )
            self.Master_List.sort ( key=lambda x:x.Archive_File, reverse=Config.Config["Sort_Reverse"] )
        elif Config.Config ["Sort"] == "ROM File":
            self.Master_List.sort ( key=lambda x:x.Comment, reverse=Config.Config["Sort_Reverse"] )
            self.Master_List.sort ( key=lambda x:x.ROM_File, reverse=Config.Config["Sort_Reverse"] )
        elif Config.Config ["Sort"] == "Location":
            self.Master_List.sort ( key=lambda x:x.Comment, reverse=Config.Config["Sort_Reverse"] )
            self.Master_List.sort ( key=lambda x:x.Location, reverse=Config.Config["Sort_Reverse"] )
        elif Config.Config ["Sort"] == "Genre":
            self.Master_List.sort ( key=lambda x:x.Comment, reverse=Config.Config["Sort_Reverse"] )
            self.Master_List.sort ( key=lambda x:x.Genre, reverse=Config.Config["Sort_Reverse"] )
        elif Config.Config ["Sort"] == "Original Size":
            self.Master_List.sort ( key=lambda x:x.Comment, reverse=Config.Config["Sort_Reverse"] )
            self.Master_List.sort ( key=lambda x:x.ROM_Size, reverse=Config.Config["Sort_Reverse"] )
        elif Config.Config ["Sort"] == "Release Group":
            self.Master_List.sort ( key=lambda x:x.Comment, reverse=Config.Config["Sort_Reverse"] )
            self.Master_List.sort ( key=lambda x:x.Source_ROM, reverse=Config.Config["Sort_Reverse"] )
        elif Config.Config ["Sort"] == "CRC":
            self.Master_List.sort ( key=lambda x:x.ROM_CRC, reverse=Config.Config["Sort_Reverse"] )
        elif Config.Config ["Sort"] == "Save Type":
            self.Master_List.sort ( key=lambda x:x.Comment, reverse=Config.Config["Sort_Reverse"] )
            self.Master_List.sort ( key=lambda x:x.Save_Type, reverse=Config.Config["Sort_Reverse"] )
        elif Config.Config ["Sort"] == "Publisher":
            self.Master_List.sort ( key=lambda x:x.Comment, reverse=Config.Config["Sort_Reverse"] )
            self.Master_List.sort ( key=lambda x:x.Publisher, reverse=Config.Config["Sort_Reverse"] )
        elif Config.Config ["Sort"] == "Internal Name":
            self.Master_List.sort ( key=lambda x:x.Comment, reverse=Config.Config["Sort_Reverse"] )
            self.Master_List.sort ( key=lambda x:x.Internal_Name, reverse=Config.Config["Sort_Reverse"] )
        elif Config.Config ["Sort"] == "Serial":
            self.Master_List.sort ( key=lambda x:x.Comment, reverse=Config.Config["Sort_Reverse"] )
            self.Master_List.sort ( key=lambda x:x.Serial, reverse=Config.Config["Sort_Reverse"] )
        elif Config.Config ["Sort"] == "Version":
            self.Master_List.sort ( key=lambda x:x.Comment, reverse=Config.Config["Sort_Reverse"] )
            self.Master_List.sort ( key=lambda x:x.Version, reverse=Config.Config["Sort_Reverse"] )
        elif Config.Config ["Sort"] == "Tags":
            self.Master_List.sort ( key=lambda x:x.Comment, reverse=Config.Config["Sort_Reverse"] )
            self.Master_List.sort ( key=lambda x:x.Tags, reverse=Config.Config["Sort_Reverse"] )
        elif Config.Config ["Sort"] == "Wifi":
            self.Master_List.sort ( key=lambda x:x.Comment, reverse=Config.Config["Sort_Reverse"] )
            self.Master_List.sort ( key=lambda x:x.Wifi, reverse=Config.Config["Sort_Reverse"] )
        elif Config.Config ["Sort"] == "Name":
            self.Master_List.sort ( key=lambda x:x.Title.lower(), reverse=Config.Config["Sort_Reverse"] )
        else:
            self.Master_List.sort ( key=lambda x:x.Title, reverse=False )
            self.Master_List.sort ( key=lambda x:x.Comment, reverse=Config.Config["Sort_Reverse"] )

        self.Master_List_CRC_Dict = {}
        self.Master_List_Filename_Dict = {}
        self.Master_List_Serial_Dict = {}
        
        Count = 0
        for ROM in self.Master_List:
            self.Master_List_CRC_Dict [ROM.ROM_CRC] = Count
            self.Master_List_Filename_Dict [ROM.ROM_File] = Count
            self.Master_List_Serial_Dict [str ( ROM.Serial )] = Count
            Count += 1

    def Populate_Current_List ( self ):
        self.Current_List = []
        self.Current_Count = 0
        
        for Count in range ( 0, len ( self.Master_List ) ):
            ROM = self.Master_List[Count]
            if ROM.Found:
                if ROM.Title.lower().find ( Config.Config ["Current_Search"].lower() ) != -1:
                    if Config.Config ["Filter_Location"] == 255 or ROM.Location == Config.Config ["Filter_Location"] or (Config.Config ["Filter_Location"] == 26 and ROM.Location == 254):
                        if Config.Config ["Filter_Language"] == 0 or ROM.Language & Config.Config ["Filter_Language"]:
                            if ( Config.Config ["Filter_Exact_Size"] == False and ( Config.Config ["Filter_Size"] == 0 or ROM.Effective_Size <= Config.Config ["Filter_Size"] ) ) or ( Config.Config ["Filter_Exact_Size"] == True and ( Config.Config ["Filter_Size"] == 0 or ROM.ROM_Size == Config.Config ["Filter_Size"] ) ):
                                if Config.Config ["Filter_Genre"] == self._AllGenres or ROM.Genre == Config.Config ["Filter_Genre"]:
                                    if ( ROM.Comment.lower() != "xxxx" or Config.Config["Show_XXXX_Files"] ):
                                        if ( ROM.Comment.lower()[0] != "u" or Config.Config ["Show_Unknown_Files"] ):
                                            if Config.Config ["Current_Tag"] == self._AllTags or Config.Config ["Current_Tag"] in ROM.Tags:
                                                if self._Hidden_ROMs not in ROM.Tags or Config.Config ["Current_Tag"] == self._Hidden_ROMs:
                                                    self.Current_List.append ( Count )
                                                    self.Current_Count += 1
    
    def Start_ROM_Find ( self ):
        self.Save_Master_List(AltName=True)
        self.Duplicates = []
        self.Originally_Found = []
        for Count in range ( len ( self.Master_List )-1,-1,-1 ):
            ROM = self.Master_List[Count]
            if ROM.Found:
                self.Originally_Found.append ( ROM.ROM_CRC )
            ROM.Found = False
#            if ROM.Comment[0] == "U":
#                del self.Master_List[Count]

        self.Create_Master_List(Merge=False)

#        if self.Unknown_Count > 1:
#            self.Master_List = self.Master_List[:-(self.Unknown_Count)]
        self.Unknown_Count = 1
            
    def Close_ROM_Find ( self ):
        del ( self.Duplicates )
        del ( self.Originally_Found )
        
        self.Master_List_Count = len (self.Master_List)
        self.Save_Master_List()
    
    def Process_ROM ( self, Filename ):
        CRC, Date, ROMFile = Utils.Get_CRC_or_Date ( Filename )
        
        if Date != "": # Not an Archive
            try:
                TheROM = self.Lookup_ROM_Filename ( os.path.basename( Filename ) )
                TimeStr = time.strftime( "%d/%m/%Y %I:%M:%S %p", time.localtime( os.path.getmtime ( Filename ) ) ).lower()
                if TimeStr != TheROM.Archive_Date:
                    CRC = Utils.Get_File_CRC ( Filename )
                else:
                    CRC = TheROM.ROM_CRC
            except:
                CRC = Utils.Get_File_CRC ( Filename )
            
        if CRC != "": # Archive Found
            if CRC in self.Duplicates:
                return ""
            self.Duplicates.append( CRC )
            
            try:
                TheROM = self.Lookup_ROM_CRC( CRC )
#                Position = self.Master_List_CRC_Dict [CRC]
                if CRC in self.Originally_Found:
                    Result = ""
                else:
                    Result = TheROM.Title
                if TheROM.Comment [0] == "U": # Force Unknowns to be Re-Numbered
                    raise RuntimeError
                TheROM.Found = True
                TheROM.Archive_File = Filename
                TheROM.Archive_Date = time.strftime( "%d/%m/%Y %I:%M:%S %p", time.localtime( os.path.getmtime ( Filename ) ) ).lower()
                TheROM.ROM_File = ROMFile
                self.Master_List_Filename_Dict [ROMFile] = self.Master_List_CRC_Dict [CRC]
                self.Master_List_Serial_Dict [str ( TheROM.Serial )] = self.Master_List_CRC_Dict [CRC]
            except:
                Result = ""
                if Config.Config ["Find_Unknown"] == True:
                    Result = self.Process_Unknown ( Filename, ROMFile, CRC )

            return Result
        return ""
    
    def Process_Unknown ( self, Filename, ROMFile, CRC ):
        global Unknown_Shelve

        Result = ""
#        if Unknown_Shelve.has_key( str ( CRC ) ) == False: # A New One
        OK, TempFilename, Data = Utils.Read_Data ( Filename, ROMFile, 0x1ff )
#        else:
#            OK = True
#            TempFilename = ""
#            Data = []
            
        if OK:
            if Unknown_Shelve.has_key( str ( CRC ) ) == False: # A New One
                Result = _( "Unknown" ) + " : %s" % ( os.path.basename( Filename ) )
            
            tmpROM = ROM()
            tmpROM.Comment = "U%03d" %self.Unknown_Count
            tmpROM.Image_Number = self.Master_List_Count + self.Unknown_Count
            tmpROM.Release_Number = tmpROM.Image_Number
            
            if Config.Config ["Unknown_Name"] == "FILENAME":
                tmpROM.Title = os.path.splitext( ROMFile )[0]
            else:
                tmpROM.Title = os.path.splitext( os.path.basename ( Filename ) )[0]
                
            tmpROM.ROM_Size = Utils.Get_File_Size( Filename, ROMFile, TempFilename )
            tmpROM.Effective_Size = tmpROM.ROM_Size
            tmpROM.ROM_CRC = CRC
            tmpROM.Archive_File = Filename
            tmpROM.Archive_Date = time.strftime( "%d/%m/%Y %I:%M:%S %p", time.localtime( os.path.getmtime ( Filename ) ) ).lower()
            tmpROM.ROM_File = ROMFile

            tmpROM.Found = True
            
            Icon_Filename = os.path.join ( Config.Config ["Image_Path"], os.path.splitext( os.path.basename ( Filename ) )[0] + ".png" )
            if not os.path.isfile( Icon_Filename ):
                Icon_CRC = Utils.Extract_Icon ( Filename, ROMFile, TempFilename, Data )
                if Icon_CRC != "":
                    tmpROM.Ico_CRC = Icon_CRC
            else:
                tmpROM.Ico_CRC = Utils.Get_File_CRC ( Icon_Filename )
                
            tmpROM.Serial = Utils.Get_Serial ( Data )
            
            self.Master_List.append ( tmpROM )
            self.Master_List_CRC_Dict [CRC] = tmpROM.Release_Number
            self.Master_List_Filename_Dict [ROMFile] = tmpROM.Release_Number
            self.Master_List_Serial_Dict [str ( tmpROM.Serial )] = tmpROM.Release_Number
            
#            if Unknown_Shelve.has_key( str ( CRC ) ) == False: # A New One
            if TempFilename != "":
                try:
                    os.unlink( TempFilename )
                except:
                    pass

            Unknown_Shelve [str ( CRC )] = tmpROM
            Unknown_Shelve [str ( tmpROM.Release_Number ) ] = str ( CRC )
            Unknown_Shelve.sync() 

            self.Unknown_Count += 1
            
        return Result

    def Open_Unknown_Shelve ( self ):
        global Unknown_Shelve
        
        Unknown_Shelve = shelve.open ( "RToolDS_Unknown.dat" )

    def Clear_Unknown_Shelve ( self ):
        global Unknown_Shelve
        
        Unknown_Shelve.close ()
        try:
            os.unlink( "RToolDS_Unknown.dat" )
        except:
            pass
        self.Open_Unknown_Shelve()

    def Open_Trimmed_Shelve ( self ):
        global Trimmed_Shelve
        
        Trimmed_Shelve = shelve.open ( "RToolDS_Trimmed.dat" )
        
    def Close_Trimmed_Shelve ( self ):
        global Trimmed_Shelve
        
        Trimmed_Shelve.close ()
        
    def Get_Trimmed_Shelve (self):
        global Trimmed_Shelve
        
        return Trimmed_Shelve

    def Open_Tag_Shelve ( self ):
        global Tag_Shelve
        
        Tag_Shelve = shelve.open ( "RToolDS_Tags.dat" )
        
    def Get_Tag_Shelve (self):
        global Tag_Shelve
        
        return Tag_Shelve

    def Get_All_Tags ( self ):
        global Tag_Shelve
        
        try:
            return Tag_Shelve ["Tags"]
        except:
            return []

    def Remove_Tag (self, Tag):
        global Tag_Shelve
        
        try:
            tmp = Tag_Shelve ["Tags"]
            if Tag in tmp:
                tmp.remove (Tag)
                Tag_Shelve ["Tags"] = tmp
        except:
            pass
        Tag_Shelve.sync()
        
    def Delete_Tag (self, Tag):
        global Tag_Shelve
        

        for CRC in Tag_Shelve.iterkeys():
            if CRC != "Tags":
                if Tag in Tag_Shelve [CRC]:
                    Tags = Tag_Shelve[CRC]
                    Tags.remove (Tag)
                    Tag_Shelve[CRC] = Tags
                    try:
                        ROM = self.Lookup_ROM_CRC(CRC)
                        ROM.Tags = Tags
                    except:
                        pass
        self.Remove_Tag (Tag)
        
    def Rename_Tag (self, Tag, New_Name):
        global Tag_Shelve
        

        for CRC in Tag_Shelve.iterkeys():
            if CRC != "Tags":
                if Tag in Tag_Shelve [CRC]:
                    Tags = Tag_Shelve[CRC]
                    Tags [Tags.index (Tag)] = New_Name
                    Tag_Shelve[CRC] = Tags
                    try:
                        ROM = self.Lookup_ROM_CRC(CRC)
                        ROM.Tags = Tags
                    except:
                        pass
        t = Tag_Shelve ["Tags"]
        t [t.index (Tag)] = New_Name
        Tag_Shelve ["Tags"] = t
        Tag_Shelve.sync ()
        
    def __iter__( self ):
        self.Current_ROM = 0
        return self
    
    def next ( self ):
        if self.Process_All:
            if self.Current_ROM == self.Master_List_Count:
                raise StopIteration
            else:
                self.Current_ROM += 1
                return self.Master_List [ self.Current_ROM - 1]
        else:
            if self.Current_ROM == self.Current_Count:
                raise StopIteration
            else:
                self.Current_ROM += 1
                return self.Master_List [ self.Current_List [self.Current_ROM - 1]]

MyROMS = ROMS()