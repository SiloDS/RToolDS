# -*- coding: iso-8859-1 -*-

import wx
import os

from ROMS import MyROMS
import Config
import Utils

class cROMListCtrl( wx.ListCtrl ):
    def __init__( self, *args, **kwds ):
        wx.ListCtrl.__init__( self, *args, **kwds )

        self.IconList = None
        self.IconDict = None

        self.UpdateColour()

    def Local_Init ( self ):
#        self.UpdateIcons ()

        self.Add_Columns ()
        
        self.Resize_Columns ()
        
    def Add_Columns( self ):
        self.DeleteAllColumns()
        self.SetImageList( None, wx.IMAGE_LIST_SMALL)
        ColNum = 0
        for Column in Config.Config ["ROMColumns"]:
            if Column != "Size" and Column != "Trimmed Size" and Column != "Saves":
                self.InsertColumn( ColNum, Config.Config ["ROMColumn_Titles"][Column] )
            else:
                self.InsertColumn( ColNum, Config.Config ["ROMColumn_Titles"][Column], wx.LIST_FORMAT_RIGHT )
            ColNum += 1
            
    def Resize_Columns( self ):
        ColNum = 0
        for Column in Config.Config ["ROMColumns"]:
#            print "%s , %d" % (Column, Config.Config ["ROMColumn_Sizes"][Column])
            if Config.Config ["ROMColumn_Sizes"][Column] != -1:
                self.SetColumnWidth( ColNum, Config.Config ["ROMColumn_Sizes"][Column] )
            else:
                if Column != "Release Number":
                    self.SetColumnWidth( ColNum, wx.LIST_AUTOSIZE )
                else:
                    self.SetColumnWidth( ColNum, 37)
            ColNum += 1

    def UpdateIcons ( self ):
        if "Icon" in Config.Config ["ROMColumns"]:
            self.SetImageList( self.IconList, wx.IMAGE_LIST_SMALL )
        else:
            self.SetImageList( None, wx.IMAGE_LIST_SMALL )
            
    def Get_ROM ( self, item ):
        return MyROMS.Get_Current_List_ROM ( item )
    
    def Get_Selected_ROM_Size (self):
        if self.GetItemCount() == 0:
            return 0
        
        Item = self.GetFirstSelected()
        
        Total = 0
        while Item != -1:
            ROM = self.Get_ROM(Item)
            Total += ROM.Effective_Size
            Item = self.GetNextSelected(Item)
            
        return Total

    def UpdateColour (self):
        if Config.Config ["Show_Alternate_Colours"]:
            self.attr1 = wx.ListItemAttr()
            self.attr1.SetBackgroundColour(Config.Config ["Alternate_Colour"])
        else:
            self.attr1 = None                
    
    def OnGetItemText( self, item, col ):
        try:
            if Config.Config ["ROMColumns"][col] == "Release Number":
                return self.Get_ROM ( item ).Comment
            elif Config.Config ["ROMColumns"][col] == "Name":
                return self.Get_ROM ( item ).Title
            elif Config.Config ["ROMColumns"][col] == "Original Size":
                return Utils.Format_ROM_Size (self.Get_ROM ( item ).ROM_Size)
            elif Config.Config ["ROMColumns"][col] == "Trimmed":
                if self.Get_ROM ( item ).Trimmed:
                    return _("Yes")
                else:
                    return _("No")
            elif Config.Config ["ROMColumns"][col] == "Saves":
                return str (self.Get_ROM ( item ).Saves)
            elif Config.Config ["ROMColumns"][col] == "Location":
                try:
                    Str = Config.Config ["Locations"][self.Get_ROM ( item ).Location]
                except:
                    Str = _("Unknown")
                return Str
            elif Config.Config ["ROMColumns"][col] == "Genre":
                return self.Get_ROM ( item ).Genre
            elif Config.Config ["ROMColumns"][col] == "Archive":
                return self.Get_ROM ( item ).Archive_File
            elif Config.Config ["ROMColumns"][col] == "ROM File":
                return self.Get_ROM ( item ).ROM_File
            elif Config.Config ["ROMColumns"][col] == "ROM File (No Ext)":
                return os.path.splitext (self.Get_ROM ( item ).ROM_File)[0]
            elif Config.Config ["ROMColumns"][col] == "CRC":
                return self.Get_ROM ( item ).ROM_CRC
            elif Config.Config ["ROMColumns"][col] == "Publisher":
                return self.Get_ROM ( item ).Publisher
            elif Config.Config ["ROMColumns"][col] == "Release Group":
                return self.Get_ROM ( item ).Source_ROM
            elif Config.Config ["ROMColumns"][col] == "Save Type":
                return self.Get_ROM ( item ).Save_Type
            elif Config.Config ["ROMColumns"][col] == "Size":
                if Config.Config ["Use_Trimmed"]:
                    return Utils.Format_ROM_Size (self.Get_ROM ( item ).Effective_Size)
                else:
                    return Utils.Format_ROM_Size (self.Get_ROM ( item ).ROM_Size)
            elif Config.Config ["ROMColumns"][col] == "Internal Name":
                return self.Get_ROM ( item ).Internal_Name
            elif Config.Config ["ROMColumns"][col] == "Serial":
                Serial = self.Get_ROM ( item ).Serial
                if Serial == "":
                    return _("Unknown")
                return Serial
            elif Config.Config ["ROMColumns"][col] == "Version":
                return self.Get_ROM ( item ).Version
            elif Config.Config ["ROMColumns"][col] == "Tags":
                Str = ", "
                return Str.join (self.Get_ROM ( item ).Tags)
            elif Config.Config ["ROMColumns"][col] == "Wi-Fi":
                return self.Get_ROM ( item ).Wifi
            else:
                return ""
        except:
            return ""
        
    def Get_Item_Icon (self, item):
        return self.IconList.GetBitmap (self.IconDict [self.Get_ROM ( item ).Image_Number])

    def OnGetItemImage( self, item ):
        try:
            Icon_Num = self.IconDict [self.Get_ROM ( item ).Image_Number]
        except:
            Icon_Num = -1
  
        return Icon_Num

    def OnGetItemAttr( self, item ):
        if item % 2 == 1:
            return self.attr1
        else:
            return None