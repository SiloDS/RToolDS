# -*- coding: iso-8859-1 -*-

import wx
import os
import sys
if sys.platform == "win32":
    import win32api

import Config
from ROMS import MyROMS
import Utils
from cProgressFrame import cProgressFrame
from cRenameFiles import cRenameFiles

class cDeviceListCtrl( wx.ListCtrl ):
    def __init__( self, *args, **kwds ):
        wx.ListCtrl.__init__( self, *args, **kwds )

        self.IconList = None
        self.IconDict = None
        
        self.BLK_SIZE = ( 1024 * 1024 ) * 2

        self.ROM_Count = 0
        self.CRC_List = []
#        self.Saves_List = []
#        self.Size_List = []
        self.Pending = []
        self.Pending_Positions = []
        
        self.UpdateColour()

    def Local_Init ( self ):
#        self.UpdateIcons ()

        self.Add_Columns ()
        
        self.Resize_Columns ()
        
    def Add_Columns( self ):
        self.DeleteAllColumns()
        ColNum = 0
        for Column in Config.Config ["CartColumns"]:
            if Column != "Size" and Column != "Trimmed Size" and Column != "Saves":
                self.InsertColumn( ColNum, Config.Config ["CartColumn_Titles"][Column] )
            else:
                self.InsertColumn( ColNum, Config.Config ["CartColumn_Titles"][Column], wx.LIST_FORMAT_RIGHT )
            ColNum += 1
            
    def Resize_Columns( self ):
        ColNum = 0
        for Column in Config.Config ["CartColumns"]:
            if Config.Config ["CartColumn_Sizes"][Column] != -1:
                self.SetColumnWidth( ColNum, Config.Config ["CartColumn_Sizes"][Column] )
            else:
                if Column != "Release Number":
                    self.SetColumnWidth( ColNum, wx.LIST_AUTOSIZE )
                else:
                    self.SetColumnWidth( ColNum, 37 )
            ColNum += 1

    def UpdateIcons ( self ):
        if "Icon" in Config.Config ["CartColumns"]:
            self.SetImageList( self.IconList, wx.IMAGE_LIST_SMALL )
        else:
            self.SetImageList( None, wx.IMAGE_LIST_SMALL )
            
    def Has_Save (self, Dir, Filename):
        Save = ["No", ""]
        for extension in Config.Config ["Save_Extensions"]:
            Save_Filename = os.path.join (Config.Config ["Save_Dir_On_Cart"], os.path.splitext( Filename )[0] + extension)
            if os.path.isfile(Save_Filename):
                Save = ["Yes", Save_Filename]
                break
            elif sys.platform == "win32":
                try:
                    Short_Save_Filename = win32api.GetShortPathName(os.path.join (Config.Config ["Save_Dir_On_Cart"], Filename ))
                    Short_Save_Filename = os.path.join (Config.Config ["Save_Dir_On_Cart"], os.path.splitext(Short_Save_Filename)[0] + Utils.Get_Save_Extension().upper())
                    if os.path.isfile (Short_Save_Filename):
                        Save = ["Yes", Short_Save_Filename]
                        break
                except:
                    pass
        return Save
            
    def Calc_FreeSpace (self):
        self.Drive_Free = Utils.Drive_Free( Config.Config ["Device_Path"] )
        for ROM in self.Pending:
            self.Drive_Free -= ROM.Effective_Size
        
    def Populate ( self ):
#        Result = ""
        self.CRC_List = []
#        self.Saves_List = []
#        self.Size_List = []
        self.Pending_Positions = []
        self.ROM_Count = 0
        
        if os.path.isdir( Config.Config ["Device_Path"] ) == False:
            self.Enable(False) 
            self.Drive_Free = 0
            self.Drive_Size = 0
            self.SetItemCount ( 0 )
            return False
        
        self.Drive_Free = Utils.Drive_Free( Config.Config ["Device_Path"] )
        self.Drive_Size = Utils.Drive_Size( Config.Config ["Device_Path"] )
        
        self.Enable()
        
        Dirs = [ Config.Config ["Device_Path"] ]
#        for Item in Config.Config ["Device_Dirs_to_Search"]:
#            Dirs.append( os.path.join ( Config.Config ["Device_Path"], Item ).lower() ) # TODO: Fix me. Shouldn't be lower for linux
            
#        if Config.Config ["Search_Device_Subdirs"]:
#            DirList = sorted ( os.listdir ( Config.Config ["Device_Path"] ) )
#            for File in DirList:
#                if File.lower() in Config.Config ["Exclude_Dirs_on_Device_Lower"]:
#                    continue
#                File = os.path.join ( Config.Config ["Device_Path"], File )
#                print File.lower()
#                if File.lower () in Dirs:
#                    continue
#                if os.path.isdir( File ) and File [0] != ".":
#                    Dirs.append( File )
        
        Dirs = Utils.Unique (Dirs)

        self.ROM_Count = 0
        for Dir in Dirs:
            try:
                DirList = sorted ( os.listdir ( os.path.join ( Config.Config ["Device_Path"], Dir ) ) )
            except:
                continue
            for File in DirList:
                if os.path.isdir( os.path.join ( Dir, File ) ):
                    continue
                Ext = os.path.splitext( File )[1]
                if Ext.lower () in Config.Config ["ROM_Extensions"]:
                    try:
                        ROM = MyROMS.Lookup_ROM_Filename ( File )
                        ROM.Name_On_Device = ""
                        Size = os.path.getsize( os.path.join ( Dir, File ) )
                        if Size == ROM.ROM_Size:
                            ROM.Trimmed_On_Device = False
                        else:
                            ROM.Trimmed_On_Device = True
                        if ROM.Found == False:  #TODO: Fix Me!!!!!
                            continue
                        ROM.Name_On_Device = os.path.join (Dir, File)
                        self.CRC_List.append( ROM.ROM_CRC )
                        ROM.Size_On_Device = os.path.getsize( os.path.join ( Dir, File ))
#                        self.Size_List.append ( os.path.getsize( os.path.join ( Dir, File ) ) )
                        ROM.Saves_List = self.Has_Save(Dir, File)
#                        self.Saves_List.append ( self.Has_Save ( Dir, File ) )
                        self.ROM_Count += 1
                    except:
                        try:
                            File_In = open (os.path.join ( Config.Config ["Device_Path"], File), "rb")
                            Data = File_In.read (0x12)
                            File_In.close ()
                            Serial = Utils.Get_Serial(Data)
                            ROM = MyROMS.Lookup_ROM_Serial ( Serial )
                            if ROM.Found == False:
                                continue
                            ROM.Name_On_Device = os.path.join (Dir, File)
                            self.CRC_List.append( ROM.ROM_CRC )
                            ROM.Size_On_Device = os.path.getsize( os.path.join ( Dir, File ))
#                            self.Size_List.append ( os.path.getsize( os.path.join ( Dir, File ) ) )
#                            self.Saves_List.append ( self.Has_Save ( Dir, File ) )
                            ROM.Saves_List = self.Has_Save(Dir, File)
                            Size = os.path.getsize( os.path.join ( Dir, File ) )
                            if Size == ROM.ROM_Size:
                                ROM.Trimmed_On_Device = False
                            else:
                                ROM.Trimmed_On_Device = True
                            self.ROM_Count += 1
                        except:
                            pass
                        pass
                    
        self.Sort ()
                
        for ROM in self.Pending:
            self.CRC_List.append( ROM.ROM_CRC )
            ROM.Size_On_Device = ROM.Effective_Size
#            self.Size_List.append ( ROM.Effective_Size )
#            self.Saves_List.append ( [bool (ROM.Saves), None] )
#            print ROM.Title + ":" + str (ROM.Saves)
            ROM.Saves_List = [ Utils.cbool (ROM.Saves), None]
            self.Pending_Positions.append (self.ROM_Count)
            self.ROM_Count += 1
                        
#            if self.CartList.GetItemCount() != 0:
#                Config.Config ["Device_Path"] = Dir
#                Result = Dir
#                break
        
        self.SetItemCount ( self.ROM_Count )
#        if self.ROM_Count == 0:
#            self.Disable() 
#        else:
#            self.Enable()

        self.Refresh()
        self.Calc_FreeSpace()
        return True
    
    def Sort (self):
        tmpList = []
        
        for Count in range (0,self.ROM_Count):
            tmpList.append (MyROMS.Lookup_ROM_CRC ( self.CRC_List[Count] ))
        
        self.CRC_List = []
#        self.Saves_List = []
#        self.Size_List = []
        self.Pending_Positions = []
        
        if Config.Config ["Cart_Sort"] == "Size":
            tmpList.sort ( key=lambda x:x.Title, reverse=False )
            tmpList.sort ( key=lambda x:x.Effective_Size, reverse=Config.Config["Cart_Sort_Reverse"] )
        elif Config.Config ["Cart_Sort"] == "Trimmed":
            tmpList.sort ( key=lambda x:x.Comment, reverse=Config.Config["Cart_Sort_Reverse"] )
            tmpList.sort ( key=lambda x:x.Trimmed, reverse=Config.Config["Cart_Sort_Reverse"] )
        elif Config.Config ["Cart_Sort"] == "Saves":
            tmpList.sort ( key=lambda x:x.Comment, reverse=Config.Config["Cart_Sort_Reverse"] )
            tmpList.sort ( key=lambda x:x.Saves, reverse=Config.Config["Cart_Sort_Reverse"] )
        elif Config.Config ["Cart_Sort"] == "Archive":
            tmpList.sort ( key=lambda x:x.Comment, reverse=Config.Config["Cart_Sort_Reverse"] )
            tmpList.sort ( key=lambda x:x.Archive_File, reverse=Config.Config["Cart_Sort_Reverse"] )
        elif Config.Config ["Cart_Sort"] == "ROM File":
            tmpList.sort ( key=lambda x:x.Comment, reverse=Config.Config["Cart_Sort_Reverse"] )
            tmpList.sort ( key=lambda x:x.ROM_File, reverse=Config.Config["Cart_Sort_Reverse"] )
        elif Config.Config ["Cart_Sort"] == "Location":
            tmpList.sort ( key=lambda x:x.Comment, reverse=Config.Config["Cart_Sort_Reverse"] )
            tmpList.sort ( key=lambda x:x.Location, reverse=Config.Config["Cart_Sort_Reverse"] )
        elif Config.Config ["Cart_Sort"] == "Genre":
            tmpList.sort ( key=lambda x:x.Comment, reverse=Config.Config["Cart_Sort_Reverse"] )
            tmpList.sort ( key=lambda x:x.Genre, reverse=Config.Config["Cart_Sort_Reverse"] )
        elif Config.Config ["Cart_Sort"] == "Original Size":
            tmpList.sort ( key=lambda x:x.Comment, reverse=Config.Config["Cart_Sort_Reverse"] )
            tmpList.sort ( key=lambda x:x.ROM_Size, reverse=Config.Config["Cart_Sort_Reverse"] )
        elif Config.Config ["Cart_Sort"] == "Release Group":
            tmpList.sort ( key=lambda x:x.Comment, reverse=Config.Config["Cart_Sort_Reverse"] )
            tmpList.sort ( key=lambda x:x.Source_ROM, reverse=Config.Config["Cart_Sort_Reverse"] )
        elif Config.Config ["Cart_Sort"] == "CRC":
            tmpList.sort ( key=lambda x:x.ROM_CRC, reverse=Config.Config["Cart_Sort_Reverse"] )
        elif Config.Config ["Cart_Sort"] == "Save Type":
            tmpList.sort ( key=lambda x:x.Comment, reverse=Config.Config["Cart_Sort_Reverse"] )
            tmpList.sort ( key=lambda x:x.Save_Type, reverse=Config.Config["Cart_Sort_Reverse"] )
        elif Config.Config ["Cart_Sort"] == "Publisher":
            tmpList.sort ( key=lambda x:x.Comment, reverse=Config.Config["Cart_Sort_Reverse"] )
            tmpList.sort ( key=lambda x:x.Publisher, reverse=Config.Config["Cart_Sort_Reverse"] )
        elif Config.Config ["Cart_Sort"] == "Internal Name":
            tmpList.sort ( key=lambda x:x.Comment, reverse=Config.Config["Cart_Sort_Reverse"] )
            tmpList.sort ( key=lambda x:x.Internal_Name, reverse=Config.Config["Cart_Sort_Reverse"] )
        elif Config.Config ["Cart_Sort"] == "Serial":
            tmpList.sort ( key=lambda x:x.Comment, reverse=Config.Config["Cart_Sort_Reverse"] )
            tmpList.sort ( key=lambda x:x.Serial, reverse=Config.Config["Cart_Sort_Reverse"] )
        elif Config.Config ["Cart_Sort"] == "Version":
            tmpList.sort ( key=lambda x:x.Comment, reverse=Config.Config["Cart_Sort_Reverse"] )
            tmpList.sort ( key=lambda x:x.Version, reverse=Config.Config["Cart_Sort_Reverse"] )
        elif Config.Config ["Cart_Sort"] == "Tags":
            tmpList.sort ( key=lambda x:x.Comment, reverse=Config.Config["Cart_Sort_Reverse"] )
            tmpList.sort ( key=lambda x:x.Tags, reverse=Config.Config["Cart_Sort_Reverse"] )
        elif Config.Config ["Cart_Sort"] == "Wi-Fi":
            tmpList.sort ( key=lambda x:x.Comment, reverse=Config.Config["Cart_Sort_Reverse"] )
            tmpList.sort ( key=lambda x:x.Wifi, reverse=Config.Config["Cart_Sort_Reverse"] )
        elif Config.Config ["Cart_Sort"] == "Name":
            tmpList.sort ( key=lambda x:x.Title.lower(), reverse=Config.Config["Cart_Sort_Reverse"] )
        else:
            tmpList.sort ( key=lambda x:x.Title, reverse=False )
            tmpList.sort ( key=lambda x:x.Comment, reverse=Config.Config["Cart_Sort_Reverse"] )
            
        for ROM in tmpList:
            self.CRC_List.append( ROM.ROM_CRC )
#            self.Size_List.append ( os.path.getsize( ROM.Name_On_Device ) )
#            self.Saves_List.append ( self.Has_Save ( os.path.split (ROM.Name_On_Device )[0], os.path.split (ROM.Name_On_Device)[1]) )

    def Get_ROM ( self, item ):
        return MyROMS.Lookup_ROM_CRC ( self.CRC_List[item] )
    
    def Get_Save_Name ( self, item ):
#        return self.Saves_List[item][1]
        return self.Get_ROM (item).Saves_List

    def Get_Selected_ROM_Size (self):
        if self.GetItemCount() == 0:
            return 0
        
        Item = self.GetFirstSelected()
        
        Total = 0
        while Item != -1:
#            Total += self.Size_List [Item]
            Total += self.Get_ROM (Item).Size_On_Device
            Item = self.GetNextSelected(Item)
            
        return Total
    
    def Get_CRC_List (self):
        CRC_List = []
        for CRC in self.CRC_List:
            CRC_List.append (CRC)
        for CRC in self.Pending:
            CRC_List.append (CRC)
            
        return CRC_List
    
    def Is_Pending (self, ROM):
        if ROM in self.Pending:
            return True
        return False

    def Add_Pending (self, ROM):
        if ROM.ROM_CRC not in self.CRC_List and ROM not in self.Pending:
            if ROM.Trimmed:
                ROM.Trimmed_On_Device = True
            else:
                ROM.Trimmed_On_Device = False
            if self.Drive_Free - ROM.Effective_Size < 0:
                self.Calc_FreeSpace()
                return False
            self.Pending.append(ROM)
            ROM.Saves_List = [ Utils.cbool (ROM.Saves), None]
        self.Calc_FreeSpace()
        return True
    
    def Clear_Pending (self):
        self.Pending = []
        self.Pending_Positions = []
        self.Calc_FreeSpace()

    def Apply_Pending (self):
        Processed_ROMS = []
        if Config.Config ["Use_Rename_Popup"]:
            RenameROMS = []
            for ROM in self.Pending:
                RenameROMS.append (ROM)
            dlg2 = cRenameFiles ( self )
            dlg2.Populate ( RenameROMS )
            dlg2.ShowModal()
            if dlg2.Results == []:
                dlg2.Destroy()
                return
            Renamimg = dlg2.Results
            dlg2.Destroy()
        
        dlg = cProgressFrame ( self )
        dlg.Proccessing_Text.SetLabel ( _("Copying ROMs to Device") )
        dlg.Guage2.SetRange ( len ( self.Pending ) )
        dlg.MakeModal()
        dlg.CenterOnScreen()
        dlg.Show()
        dlg.Update()
        
        Processed = 0
        for ROM in self.Pending:
            OK, Data, Save = ROM.Get_ROM_Data ( Get_Save = True )
            if OK:
                if Config.Config ["Use_Trimmed"]:
                    Data = Data [0:ROM.Effective_Size]
                    dlg.Guage1.SetRange ( ROM.Effective_Size )
                    Temp = ROM.Effective_Size
                    ES = Temp
                else:
                    Data = Data [0:ROM.ROM_Size]
                    dlg.Guage1.SetRange ( ROM.ROM_Size )
                    Temp = ROM.ROM_Size
                    ES = Temp
                Pos = 0
                if Config.Config ["Use_Rename_Popup"] == False:
                    FileOutName = Utils.Get_Name_on_Device (ROM)
                else:
                    FileOutName = Renamimg [Processed]
                FileOut = open (FileOutName,"wb")
                while Temp > 0:
                    FileOut.write ( Data[Pos:Pos+self.BLK_SIZE] )
                    Temp = Temp - ( self.BLK_SIZE )
                    Pos = Pos + self.BLK_SIZE
                    if Temp > 0:
                        dlg.Guage1.SetValue ( ES - Temp )
                    else:
                        FileOut.write ( Data[Pos+self.BLK_SIZE:] )
                    dlg.Update()
                    wx.YieldIfNeeded()
                    if dlg.Abort:
                        Save = []
                        break
                if Save != [] and Config.Config ["AutoCopySaves"]:
                    if Config.Config ["Use_Rename_Popup"] == False:
                        Utils.Write_Save (ROM, Save)
                    else:
                        Name = os.path.splitext(Renamimg [Processed])[0] + Utils.Get_Save_Extension()
                        Utils.Write_Save (ROM, Save, Name)

                FileOut.close ()
                
                if not dlg.Abort:
                    Processed_ROMS.append(ROM)
                    dlg.Guage1.SetValue ( ES-1 )
                else:
                    try:
                        os.unlink ( os.path.join ( Config.Config["Device_Path"], ROM.ROM_File ) )
                    except:
                        pass
                    break
            Processed += 1
            dlg.Guage2.SetValue ( Processed )
            dlg.Update()
            wx.YieldIfNeeded()
            if dlg.Abort:
                break
        
        for ROM in Processed_ROMS:
            Position = self.Pending.index (ROM)
            del (self.Pending[Position])
            del (self.Pending_Positions [Position])

        self.SetCursor( wx.StockCursor( wx.CURSOR_ARROW ) )
        dlg.MakeModal( False )
        dlg.Destroy()


    def Delete_Selected (self):
        ToProcess = self.GetSelectedItemCount()

        RealFiles = False
        ROMS = []
        Row = self.GetFirstSelected()
        while Row != -1:
            ROM = self.Get_ROM(Row)
            ROMS.append( ROM )
            if ROM not in self.Pending:
                RealFiles = True
            Row = self.GetNextSelected( Row )

        if RealFiles and Config.Config ["Confirm_Delete"]:
            Res = wx.MessageBox( _('Are you sure you want to remove files from the Device?'), _('Delete Confirmation'), wx.YES_NO| wx.ICON_QUESTION )
            if Res != wx.YES:
                return
                
        dlg = cProgressFrame ( self )
        dlg.DisableGuage2()
        dlg.Proccessing_Text.SetLabel ( _("Removing ROMS from Device" ))
        dlg.Guage1.SetRange ( ToProcess )
        dlg.MakeModal()
        dlg.CenterOnScreen()
        dlg.Show()
        dlg.Update()

        Processed = 0
        for ROM in ROMS:
            if ROM in self.Pending:
                Position = self.Pending.index (ROM)
                del (self.Pending[Position])
                del (self.Pending_Positions [Position])
            else:
#                try:
#                    Short_Save_Filename = win32api.GetShortPathName(os.path.join (Config.Config ["Save_Dir_On_Cart"], ROM.ROM_File ))
                try:
                    os.unlink( os.path.join ( Config.Config ["Device_Path"], ROM.ROM_File ) )
                except:
                    try:
                        os.unlink( ROM.Name_On_Device )
                    except:
                        pass
                if Config.Config ["Delete_Saves_with_ROM"]:
                    try:
                        Filename = ROM.Saves_List[1]
                        os.unlink (Filename)
                    except:
                        pass
#                        try:
#                            Filename = os.path.join ( Config.Config ["Save_Dir_On_Cart"], ROM.ROM_File )
#                            Filename = os.path.splitext(Filename)[0] + Utils.Get_Save_Extension()
#                            os.unlink( Filename )
#                        except:
#                            if sys.platform == "win32":
#                                try:
#                                    Short_Save_Filename = os.path.join (Config.Config ["Save_Dir_On_Cart"], os.path.splitext(Short_Save_Filename)[0] + Utils.Get_Save_Extension().upper())
#                                    if os.path.isfile (Short_Save_Filename):
#                                        os.unlink( Short_Save_Filename )
#                                except:
#                                    pass
#                except:
#                    try:
#                        Short_Save_Filename = win32api.GetShortPathName(os.path.join (Config.Config ["Save_Dir_On_Cart"], ROM.Name_On_Device ))
#                        os.unlink( ROM.Name_On_Device )
#                        if Config.Config ["Delete_Saves_with_ROM"]:
#                            try:
#                                Filename = os.path.join (Config.Config ["Save_Dir_On_Cart"], os.path.split (ROM.Name_On_Device)[1])
#                                Filename = os.path.splitext(Filename)[0] + Utils.Get_Save_Extension()
#                                os.unlink( Filename )
#                            except:
#                                if sys.platform == "win32":
#                                    try:
#                                        Short_Save_Filename = os.path.join (Config.Config ["Save_Dir_On_Cart"], os.path.splitext(Short_Save_Filename)[0] + Utils.Get_Save_Extension().upper())
#                                        if os.path.isfile (Short_Save_Filename):
#                                            os.unlink( Short_Save_Filename )
#                                    except:
#                                        pass
#                    except:
#                        pass
                    
            Processed += 1
            dlg.Guage1.SetValue ( Processed )
            dlg.Update()
            wx.YieldIfNeeded()
            if dlg.Abort:
                break

        dlg.MakeModal( False )
        dlg.Destroy()
        self.Calc_FreeSpace()

    def Delete_Selected_Saves (self):
        ToProcess = self.GetSelectedItemCount()

        RealFiles = False
        ROMS = []
        Row = self.GetFirstSelected()
        while Row != -1:
            ROM = self.Get_ROM(Row)
            ROMS.append( ROM )
            if ROM not in self.Pending:
                RealFiles = True
            Row = self.GetNextSelected( Row )

        if RealFiles and Config.Config ["Confirm_Delete"]:
            Res = wx.MessageBox( _('Are you sure you want to remove Save Games from the Device?'), _('Delete Confirmation'), wx.YES_NO| wx.ICON_QUESTION )
            if Res != wx.YES:
                return

        dlg = cProgressFrame ( self )
        dlg.DisableGuage2()
        dlg.Proccessing_Text.SetLabel ( _("Removing Saves from Device" ))
        dlg.Guage1.SetRange ( ToProcess )
        dlg.MakeModal()
        dlg.CenterOnScreen()
        dlg.Show()
        dlg.Update()

        Processed = 0
        for ROM in ROMS:
            if ROM in self.Pending:
                pass
            else:
                try:
                    Filename = ROM.Saves_List[1]
                    os.unlink (Filename)
                except:
                    pass
#                try:
#                    Short_Save_Filename = win32api.GetShortPathName(os.path.join (Config.Config ["Save_Dir_On_Cart"], ROM.ROM_File ))
#                    try:
#                        Filename = os.path.join ( Config.Config ["Save_Dir_On_Cart"], ROM.ROM_File )
#                        Filename = os.path.splitext(Filename)[0] + Utils.Get_Save_Extension() 
#                        os.unlink( Filename )
#                    except:
#                        if sys.platform == "win32":
#                            try:
#                                Short_Save_Filename = os.path.join (Config.Config ["Save_Dir_On_Cart"], os.path.splitext(Short_Save_Filename)[0] + Utils.Get_Save_Extension().upper())
#                                if os.path.isfile (Short_Save_Filename):
#                                    os.unlink( Short_Save_Filename )
#                            except:
#                                pass
#                except:
#                    try:
#                        Short_Save_Filename = win32api.GetShortPathName(os.path.join (Config.Config ["Save_Dir_On_Cart"], ROM.Name_On_Device ))
#                        try:
#                            Filename = os.path.join (Config.Config ["Save_Dir_On_Cart"], os.path.split (ROM.Name_On_Device)[1])
#                            Filename = os.path.splitext(Filename)[0] + Utils.Get_Save_Extension()
#                            os.unlink( Filename )
#                        except:
#                            if sys.platform == "win32":
#                                try:
#                                    Short_Save_Filename = os.path.join (Config.Config ["Save_Dir_On_Cart"], os.path.splitext(Short_Save_Filename)[0] + Utils.Get_Save_Extension().upper())
#                                    if os.path.isfile (Short_Save_Filename):
#                                        os.unlink( Short_Save_Filename )
#                                except:
#                                    pass
#                    except:
#                        pass
                    
            Processed += 1
            dlg.Guage1.SetValue ( Processed )
            dlg.Update()
            wx.YieldIfNeeded()
            if dlg.Abort:
                break

        dlg.MakeModal( False )
        dlg.Destroy()
        self.Calc_FreeSpace()

    def UpdateColour ( self ):
        if Config.Config ["Show_Alternate_Colours"]:
            self.attr1 = wx.ListItemAttr()
            self.attr1.SetBackgroundColour( Config.Config ["Alternate_Colour"] )
        else:
            self.attr1 = None
        self.attr_pending = wx.ListItemAttr()
        self.attr_pending.SetBackgroundColour( Config.Config ["Pending_Colour"])                
    
    def OnGetItemText( self, item, col ):
        try:
            if Config.Config ["CartColumns"][col] == "Release Number":
                return self.Get_ROM ( item ).Comment
            elif Config.Config ["CartColumns"][col] == "Name":
                return self.Get_ROM ( item ).Title
            elif Config.Config ["CartColumns"][col] == "Original Size":
#                return Utils.Format_ROM_Size ( self.Size_List [ item ] )
                try:
                    s = Utils.Format_ROM_Size ( self.Get_ROM ( item ).Size_On_Device )
                except:
                    s = Utils.Format_ROM_Size(self.Get_ROM ( item ).ROM_Size)
                return s
            elif Config.Config ["CartColumns"][col] == "Trimmed":
                if self.Get_ROM ( item ).Trimmed_On_Device:
                    return _( "Yes" )
                else:
                    return _( "No" )
            elif Config.Config ["CartColumns"][col] == "Saves":
#                return self.Saves_List [ item ][0]
                r = self.Get_ROM (item)
                try:
                    t = r.Saves_List [0]
                except:
                    t = "Arg"  
                return t 
            elif Config.Config ["CartColumns"][col] == "Location":
                try:
                    Str = Config.Config ["Locations"][self.Get_ROM ( item ).Location]
                except:
                    Str = _( "Unknown" )
                return Str
            elif Config.Config ["CartColumns"][col] == "Genre":
                return self.Get_ROM ( item ).Genre
            elif Config.Config ["CartColumns"][col] == "Archive":
                return self.Get_ROM ( item ).Archive_File
            elif Config.Config ["CartColumns"][col] == "ROM File":
                r = self.Get_ROM ( item )
                try:
                    s = r.Name_On_Device
                except:
                    s = r.ROM_File
                if s == "":
                    s = r.ROM_File
                return s
            elif Config.Config ["CartColumns"][col] == "ROM File (No Ext)":
                r = self.Get_ROM ( item )
                if r.Name_On_Device != "":
                    return os.path.splitext (r.Name_On_Device)[0]
                else:
                    return os.path.splitext (r.ROM_File)[0]
            elif Config.Config ["CartColumns"][col] == "CRC":
                return self.Get_ROM ( item ).ROM_CRC
            elif Config.Config ["CartColumns"][col] == "Publisher":
                return self.Get_ROM ( item ).Publisher
            elif Config.Config ["CartColumns"][col] == "Release Group":
                return self.Get_ROM ( item ).Source_ROM
            elif Config.Config ["CartColumns"][col] == "Save Type":
                return self.Get_ROM ( item ).Save_Type
            elif Config.Config ["CartColumns"][col] == "Size":
#                return Utils.Format_ROM_Size ( self.Size_List [ item ] )
                if self.Get_ROM ( item ) not in self.Pending:
                    try:
                        s = Utils.Format_ROM_Size ( self.Get_ROM ( item ).Size_On_Device )
                    except:
    #                    s = Utils.Format_ROM_Size(self.Get_ROM ( item ).Effective_Size)
                        if Config.Config ["Use_Trimmed"]:
                            s = Utils.Format_ROM_Size (self.Get_ROM ( item ).Effective_Size)
                        else:
                            s = Utils.Format_ROM_Size (self.Get_ROM ( item ).ROM_Size)
                    return s
                else:
                    if Config.Config ["Use_Trimmed"]:
                        s = Utils.Format_ROM_Size (self.Get_ROM ( item ).Effective_Size)
                    else:
                        s = Utils.Format_ROM_Size (self.Get_ROM ( item ).ROM_Size)
                    return s
            elif Config.Config ["CartColumns"][col] == "Internal Name":
                return self.Get_ROM ( item ).Internal_Name
            elif Config.Config ["CartColumns"][col] == "Serial":
                return self.Get_ROM ( item ).Serial
            elif Config.Config ["CartColumns"][col] == "Version":
                return self.Get_ROM ( item ).Version
            elif Config.Config ["CartColumns"][col] == "Tags":
                Str = ", "
                return Str.join ( self.Get_ROM ( item ).Tags )
            elif Config.Config ["CartColumns"][col] == "Wi-Fi":
                return self.Get_ROM ( item ).Wifi
            else:
                return ""
        except:
            return ""

    def Get_Item_Icon (self, item):
        return self.IconList.GetBitmap (self.IconDict [self.Get_ROM ( item ).Image_Number])

    def OnGetItemImage( self, item ):
        try:
            return self.IconDict [self.Get_ROM ( item ).Image_Number]
        except:
            return self.IconDict [0]

    def OnGetItemAttr( self, item ):
        if item in self.Pending_Positions:
            return self.attr_pending

        if item % 2 == 1:
            return self.attr1
        else:
            return None