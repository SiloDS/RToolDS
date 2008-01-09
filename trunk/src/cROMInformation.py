# -*- coding: iso-8859-15 -*-
# generated by wxGlade 0.6.1 on Thu Nov 08 15:53:21 2007

import wx

import GFX
import Config
import Utils
from cNFODialog import cNFODialog
from cSaveGameManager import cSaveGameManager

# begin wxGlade: dependencies
# end wxGlade

# begin wxGlade: extracode

# end wxGlade

class cROMInformation( wx.Dialog ):
    def __init__( self, *args, **kwds ):
        self.Current_Ctrl = kwds["Current_Ctrl"]
        del kwds["Current_Ctrl"]
        self.Save_Comments_Shelve = kwds["Save_Comments_Shelve"]
        del kwds["Save_Comments_Shelve"]
        self.Device_List = kwds["Device_List"]
        del kwds["Device_List"]
        self.From_Device = kwds["From_Device"]
        del kwds["From_Device"]
        # begin wxGlade: cROMInformation.__init__
        kwds["style"] = wx.DEFAULT_DIALOG_STYLE
        wx.Dialog.__init__(self, *args, **kwds)
        self.ROMInformation_Static_Sizer_staticbox = wx.StaticBox(self, -1, "")
        self.ROMInformation_Panel = wx.Panel(self, -1)
        self.Previous_Button = wx.BitmapButton(self.ROMInformation_Panel, -1, (GFX.catalog ["GFX_Icon_Previous16"].getBitmap()))
        self.Next_Button = wx.BitmapButton(self.ROMInformation_Panel, -1, (GFX.catalog ["GFX_Icon_Next16"].getBitmap()))
        self.View_NFO_Button = wx.BitmapButton(self.ROMInformation_Panel, -1, (GFX.catalog ["GFX_Icon_NFO16"].getBitmap()))
        self.Save_Game_Button = wx.BitmapButton(self.ROMInformation_Panel, -1, (GFX.catalog ["GFX_Icon_SaveGameMgr16"].getBitmap()))
        self.Case_Bitmap = wx.StaticBitmap(self, -1, wx.NullBitmap)
        self.SS_Bitmap = wx.StaticBitmap(self, -1, wx.NullBitmap)
        self.Label_Icon = wx.StaticText(self, -1, _("Icon : "))
        self.Icon_Bitmap = wx.StaticBitmap(self, -1, wx.NullBitmap)
        self.Label_Release_Number = wx.StaticText(self, -1, _("Rel Num : "))
        self.Comment_Text = wx.StaticText(self, -1, _("<RelNum>"))
        self.Label_Title = wx.StaticText(self, -1, _("Title : "))
        self.Title_Text = wx.StaticText(self, -1, _("<Title>"))
        self.Label_Publisher = wx.StaticText(self, -1, _("Publisher : "))
        self.Publisher_Text = wx.StaticText(self, -1, _("<Publisher>"))
        self.Label_Genre = wx.StaticText(self, -1, _("Genre : "))
        self.Genre_Text = wx.StaticText(self, -1, _("<Genre>"))
        self.Label_Release_Group = wx.StaticText(self, -1, _("Release Group : "))
        self.Source_ROM_Text = wx.StaticText(self, -1, _("<Release Grp>"))
        self.Label_Dump_Date = wx.StaticText(self, -1, _("Dumped : "))
        self.Dump_Date_Text = wx.StaticText(self, -1, _("<Dumped>"))
        self.Label_Filename = wx.StaticText(self, -1, _("Filename : "))
        self.Filename_Text = wx.StaticText(self, -1, _("<Filename>"))
        self.Label_CRC = wx.StaticText(self, -1, _("CRC32 : "))
        self.ROM_CRC_Text = wx.StaticText(self, -1, _("<CRC32>"))
        self.Label_Internal_Name = wx.StaticText(self, -1, _("Internal Name : "))
        self.Internal_Name_Text = wx.StaticText(self, -1, _("<Internal Name>"))
        self.Label_Serial = wx.StaticText(self, -1, _("Serial : "))
        self.Serial_Text = wx.StaticText(self, -1, _("<Serial>"))
        self.Label_Size = wx.StaticText(self, -1, _("Official Size : "))
        self.ROM_Size_Text = wx.StaticText(self, -1, _("<Size>"))
        self.Label_Location = wx.StaticText(self, -1, _("Region : "))
        self.Location_Text = wx.StaticText(self, -1, _("<Region>"))
        self.Label_Save_Type = wx.StaticText(self, -1, _("Save Type : "))
        self.Save_Type_Text = wx.StaticText(self, -1, _("<Save Type>"))
        self.Label_Saved_Games = wx.StaticText(self, -1, _("Saved Games : "))
        self.Saved_Games_Text = wx.StaticText(self, -1, _("<Saved Gamesi>"))
        self.Label_Version = wx.StaticText(self, -1, _("Version : "))
        self.Version_Text = wx.StaticText(self, -1, _("<Version>"))
        self.Label_Wifi = wx.StaticText(self, -1, _("Wi-Fi : "))
        self.Wifi_Text = wx.StaticText(self, -1, _("<Wifi>"))
        self.Label_Languages = wx.StaticText(self, -1, _("Languages : "))
        self.Language_Text = wx.StaticText(self, -1, _("<Languages>"))
        self.Label_Tags = wx.StaticText(self, -1, _("Tags : "))
        self.Tags_Text = wx.StaticText(self, -1, _("<Tags>"))
        self.OK_Button = wx.Button(self, wx.ID_OK, _("&OK"))

        self.__set_properties()
        self.__do_layout()

        self.Bind(wx.EVT_BUTTON, self.On_Previous, self.Previous_Button)
        self.Bind(wx.EVT_BUTTON, self.On_Next, self.Next_Button)
        self.Bind(wx.EVT_BUTTON, self.On_ViewNFO, self.View_NFO_Button)
        self.Bind(wx.EVT_BUTTON, self.On_Save_Game_Button, self.Save_Game_Button)
        # end wxGlade

    def __set_properties( self ):
        ToolSize = Config.Config ["Toolbar_Size"]
        self.Previous_Button.SetBitmapLabel( eval ( "GFX.getGFX_Icon_Previous"+ToolSize+"Bitmap" )() )
        self.Next_Button.SetBitmapLabel( eval ( "GFX.getGFX_Icon_Next"+ToolSize+"Bitmap" )() )
        self.View_NFO_Button.SetBitmapLabel( eval ( "GFX.getGFX_Icon_NFO"+ToolSize+"Bitmap" )() )
        self.Save_Game_Button.SetBitmapLabel( eval ( "GFX.getGFX_Icon_SaveGameMgr"+ToolSize+"Bitmap" )())        

        # begin wxGlade: cROMInformation.__set_properties
        self.SetTitle(_("ROM Information"))
        self.Previous_Button.SetToolTipString(_("Previous ROM"))
        self.Previous_Button.SetSize(self.Previous_Button.GetBestSize())
        self.Next_Button.SetToolTipString(_("Next ROM"))
        self.Next_Button.SetSize(self.Next_Button.GetBestSize())
        self.View_NFO_Button.SetToolTipString(_("View NFO File"))
        self.View_NFO_Button.SetSize(self.View_NFO_Button.GetBestSize())
        self.Save_Game_Button.SetToolTipString(_("Save Game Manager"))
        self.Save_Game_Button.Hide()
        self.Save_Game_Button.SetSize(self.Save_Game_Button.GetBestSize())
        self.OK_Button.SetFocus()
        # end wxGlade

    def __do_layout( self ):
        self.Freeze()
        # begin wxGlade: cROMInformation.__do_layout
        ROMInformation_Sizer = wx.FlexGridSizer(2, 1, 0, 0)
        ROMInformation_Sizer2 = wx.FlexGridSizer(2, 1, 0, 0)
        ROMInformation_Static_Sizer = wx.StaticBoxSizer(self.ROMInformation_Static_Sizer_staticbox, wx.HORIZONTAL)
        ROMInformation_Sizer3 = wx.GridSizer(2, 1, 0, 0)
        ROMInformation_Sizer4 = wx.FlexGridSizer(2, 1, 0, 0)
        ROMInformation_Sizer6 = wx.FlexGridSizer(2, 1, 0, 0)
        ROMInformation_Sizer10 = wx.GridSizer(10, 1, 0, 0)
        ROMInformation_Sizer23_copy = wx.FlexGridSizer(1, 2, 0, 0)
        ROMInformation_Sizer23 = wx.FlexGridSizer(1, 2, 0, 0)
        ROMInformation_Sizer30 = wx.GridSizer(1, 2, 0, 0)
        ROMInformation_Sizer32 = wx.FlexGridSizer(1, 2, 0, 0)
        ROMInformation_Sizer31 = wx.FlexGridSizer(1, 2, 0, 0)
        ROMInformation_Sizer27 = wx.GridSizer(1, 2, 0, 0)
        ROMInformation_Sizer32_copy = wx.FlexGridSizer(1, 2, 0, 0)
        ROMInformation_Sizer21 = wx.FlexGridSizer(1, 2, 0, 0)
        ROMInformation_Sizer24_copy = wx.GridSizer(1, 2, 0, 0)
        ROMInformation_Sizer20 = wx.FlexGridSizer(1, 2, 0, 0)
        ROMInformation_Sizer17 = wx.FlexGridSizer(1, 2, 0, 0)
        ROMInformation_Sizer22 = wx.GridSizer(1, 1, 0, 0)
        ROMInformation_Sizer24 = wx.GridSizer(1, 2, 0, 0)
        ROMInformation_Sizer29 = wx.FlexGridSizer(1, 2, 0, 0)
        ROMInformation_Sizer28 = wx.FlexGridSizer(1, 2, 0, 0)
        ROMInformation_Sizer19 = wx.GridSizer(1, 2, 0, 0)
        ROMInformation_Sizer26 = wx.FlexGridSizer(1, 2, 0, 0)
        ROMInformation_Sizer26_copy = wx.FlexGridSizer(1, 2, 0, 0)
        ROMInformation_Sizer16 = wx.GridSizer(1, 2, 0, 0)
        ROMInformation_Sizer15_copy = wx.FlexGridSizer(1, 2, 0, 0)
        ROMInformation_Sizer15 = wx.FlexGridSizer(1, 2, 0, 0)
        ROMInformation_Sizer13 = wx.GridSizer(1, 2, 0, 0)
        ROMInformation_Sizer25 = wx.FlexGridSizer(1, 2, 0, 0)
        ROMInformation_Sizer14 = wx.FlexGridSizer(1, 2, 0, 0)
        ROMInformation_Sizer11 = wx.GridSizer(1, 1, 0, 0)
        ROMInformation_Sizer12 = wx.FlexGridSizer(1, 2, 0, 0)
        ROMInformation_Sizer7 = wx.GridSizer(1, 2, 0, 0)
        ROMInformation_Sizer9 = wx.FlexGridSizer(1, 2, 0, 0)
        ROMInformation_Sizer8 = wx.FlexGridSizer(1, 2, 0, 0)
        ROMInformation_Sizer5 = wx.FlexGridSizer(1, 2, 0, 0)
        ROMInformation_Toolbar_Sizer = wx.FlexGridSizer(1, 4, 0, 0)
        ROMInformation_Toolbar_Sizer.Add(self.Previous_Button, 0, 0, 1)
        ROMInformation_Toolbar_Sizer.Add(self.Next_Button, 0, 0, 1)
        ROMInformation_Toolbar_Sizer.Add(self.View_NFO_Button, 0, 0, 1)
        ROMInformation_Toolbar_Sizer.Add(self.Save_Game_Button, 0, 0, 1)
        self.ROMInformation_Panel.SetSizer(ROMInformation_Toolbar_Sizer)
        ROMInformation_Sizer.Add(self.ROMInformation_Panel, 1, wx.EXPAND, 0)
        ROMInformation_Sizer5.Add(self.Case_Bitmap, 0, wx.ALL, 3)
        ROMInformation_Sizer5.Add(self.SS_Bitmap, 0, wx.ALL, 3)
        ROMInformation_Sizer4.Add(ROMInformation_Sizer5, 1, wx.EXPAND, 0)
        ROMInformation_Sizer8.Add(self.Label_Icon, 0, wx.ALL, 3)
        ROMInformation_Sizer8.Add(self.Icon_Bitmap, 0, wx.ALL, 3)
        ROMInformation_Sizer7.Add(ROMInformation_Sizer8, 1, wx.EXPAND, 0)
        ROMInformation_Sizer9.Add(self.Label_Release_Number, 0, wx.ALL, 3)
        ROMInformation_Sizer9.Add(self.Comment_Text, 0, wx.ALL|wx.EXPAND, 3)
        ROMInformation_Sizer7.Add(ROMInformation_Sizer9, 1, wx.EXPAND, 0)
        ROMInformation_Sizer6.Add(ROMInformation_Sizer7, 1, wx.EXPAND, 0)
        ROMInformation_Sizer12.Add(self.Label_Title, 0, wx.ALL, 3)
        ROMInformation_Sizer12.Add(self.Title_Text, 0, wx.ALL|wx.EXPAND, 3)
        ROMInformation_Sizer11.Add(ROMInformation_Sizer12, 1, wx.EXPAND, 0)
        ROMInformation_Sizer10.Add(ROMInformation_Sizer11, 1, wx.EXPAND, 0)
        ROMInformation_Sizer14.Add(self.Label_Publisher, 0, wx.ALL, 3)
        ROMInformation_Sizer14.Add(self.Publisher_Text, 0, wx.ALL|wx.EXPAND, 3)
        ROMInformation_Sizer13.Add(ROMInformation_Sizer14, 1, wx.EXPAND, 0)
        ROMInformation_Sizer25.Add(self.Label_Genre, 0, wx.ALL, 3)
        ROMInformation_Sizer25.Add(self.Genre_Text, 0, wx.ALL|wx.EXPAND, 3)
        ROMInformation_Sizer13.Add(ROMInformation_Sizer25, 1, wx.EXPAND, 0)
        ROMInformation_Sizer10.Add(ROMInformation_Sizer13, 1, wx.EXPAND, 0)
        ROMInformation_Sizer15.Add(self.Label_Release_Group, 0, wx.ALL, 3)
        ROMInformation_Sizer15.Add(self.Source_ROM_Text, 0, wx.ALL|wx.EXPAND, 3)
        ROMInformation_Sizer16.Add(ROMInformation_Sizer15, 1, wx.EXPAND, 0)
        ROMInformation_Sizer15_copy.Add(self.Label_Dump_Date, 0, wx.ALL, 3)
        ROMInformation_Sizer15_copy.Add(self.Dump_Date_Text, 0, wx.ALL|wx.EXPAND, 3)
        ROMInformation_Sizer16.Add(ROMInformation_Sizer15_copy, 1, wx.EXPAND, 0)
        ROMInformation_Sizer10.Add(ROMInformation_Sizer16, 1, wx.EXPAND, 0)
        ROMInformation_Sizer26_copy.Add(self.Label_Filename, 0, wx.ALL, 3)
        ROMInformation_Sizer26_copy.Add(self.Filename_Text, 0, wx.ALL|wx.EXPAND, 3)
        ROMInformation_Sizer19.Add(ROMInformation_Sizer26_copy, 1, wx.EXPAND, 0)
        ROMInformation_Sizer26.Add(self.Label_CRC, 0, wx.ALL, 3)
        ROMInformation_Sizer26.Add(self.ROM_CRC_Text, 0, wx.ALL|wx.EXPAND, 3)
        ROMInformation_Sizer19.Add(ROMInformation_Sizer26, 1, wx.EXPAND, 0)
        ROMInformation_Sizer10.Add(ROMInformation_Sizer19, 1, wx.EXPAND, 0)
        ROMInformation_Sizer28.Add(self.Label_Internal_Name, 0, wx.ALL, 3)
        ROMInformation_Sizer28.Add(self.Internal_Name_Text, 0, wx.ALL|wx.EXPAND, 3)
        ROMInformation_Sizer24.Add(ROMInformation_Sizer28, 1, wx.EXPAND, 0)
        ROMInformation_Sizer29.Add(self.Label_Serial, 0, wx.ALL, 3)
        ROMInformation_Sizer29.Add(self.Serial_Text, 0, wx.ALL|wx.EXPAND, 3)
        ROMInformation_Sizer24.Add(ROMInformation_Sizer29, 1, wx.EXPAND, 0)
        ROMInformation_Sizer22.Add(ROMInformation_Sizer24, 1, wx.EXPAND, 0)
        ROMInformation_Sizer10.Add(ROMInformation_Sizer22, 1, wx.EXPAND, 0)
        ROMInformation_Sizer17.Add(self.Label_Size, 0, wx.ALL, 3)
        ROMInformation_Sizer17.Add(self.ROM_Size_Text, 0, wx.ALL|wx.EXPAND, 3)
        ROMInformation_Sizer24_copy.Add(ROMInformation_Sizer17, 1, wx.EXPAND, 0)
        ROMInformation_Sizer20.Add(self.Label_Location, 0, wx.ALL, 3)
        ROMInformation_Sizer20.Add(self.Location_Text, 0, wx.ALL|wx.EXPAND, 3)
        ROMInformation_Sizer24_copy.Add(ROMInformation_Sizer20, 1, wx.EXPAND, 0)
        ROMInformation_Sizer10.Add(ROMInformation_Sizer24_copy, 1, wx.EXPAND, 0)
        ROMInformation_Sizer21.Add(self.Label_Save_Type, 0, wx.ALL, 3)
        ROMInformation_Sizer21.Add(self.Save_Type_Text, 0, wx.ALL|wx.EXPAND, 3)
        ROMInformation_Sizer27.Add(ROMInformation_Sizer21, 1, wx.EXPAND, 0)
        ROMInformation_Sizer32_copy.Add(self.Label_Saved_Games, 0, wx.ALL, 3)
        ROMInformation_Sizer32_copy.Add(self.Saved_Games_Text, 0, wx.ALL|wx.EXPAND, 3)
        ROMInformation_Sizer27.Add(ROMInformation_Sizer32_copy, 1, wx.EXPAND, 0)
        ROMInformation_Sizer10.Add(ROMInformation_Sizer27, 1, wx.EXPAND, 0)
        ROMInformation_Sizer31.Add(self.Label_Version, 0, wx.ALL, 3)
        ROMInformation_Sizer31.Add(self.Version_Text, 0, wx.ALL|wx.EXPAND, 3)
        ROMInformation_Sizer30.Add(ROMInformation_Sizer31, 1, wx.EXPAND, 0)
        ROMInformation_Sizer32.Add(self.Label_Wifi, 0, wx.ALL, 3)
        ROMInformation_Sizer32.Add(self.Wifi_Text, 0, wx.ALL|wx.EXPAND, 3)
        ROMInformation_Sizer30.Add(ROMInformation_Sizer32, 1, wx.EXPAND, 0)
        ROMInformation_Sizer10.Add(ROMInformation_Sizer30, 1, wx.EXPAND, 0)
        ROMInformation_Sizer23.Add(self.Label_Languages, 0, wx.ALL, 3)
        ROMInformation_Sizer23.Add(self.Language_Text, 0, wx.ALL|wx.EXPAND, 3)
        ROMInformation_Sizer10.Add(ROMInformation_Sizer23, 1, wx.EXPAND, 0)
        ROMInformation_Sizer23_copy.Add(self.Label_Tags, 0, wx.ALL, 3)
        ROMInformation_Sizer23_copy.Add(self.Tags_Text, 0, wx.ALL|wx.EXPAND, 3)
        ROMInformation_Sizer10.Add(ROMInformation_Sizer23_copy, 1, wx.EXPAND, 0)
        ROMInformation_Sizer6.Add(ROMInformation_Sizer10, 1, wx.EXPAND, 0)
        ROMInformation_Sizer6.AddGrowableRow(1)
        ROMInformation_Sizer6.AddGrowableCol(0)
        ROMInformation_Sizer4.Add(ROMInformation_Sizer6, 1, wx.EXPAND, 0)
        ROMInformation_Sizer4.AddGrowableRow(1)
        ROMInformation_Sizer4.AddGrowableCol(0)
        ROMInformation_Sizer3.Add(ROMInformation_Sizer4, 1, wx.EXPAND, 0)
        ROMInformation_Static_Sizer.Add(ROMInformation_Sizer3, 1, wx.EXPAND, 0)
        ROMInformation_Sizer2.Add(ROMInformation_Static_Sizer, 1, wx.EXPAND, 0)
        ROMInformation_Sizer2.Add(self.OK_Button, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5)
        ROMInformation_Sizer2.AddGrowableRow(0)
        ROMInformation_Sizer2.AddGrowableCol(0)
        ROMInformation_Sizer.Add(ROMInformation_Sizer2, 1, wx.ALL|wx.EXPAND, 5)
        self.SetSizer(ROMInformation_Sizer)
        ROMInformation_Sizer.Fit(self)
        ROMInformation_Sizer.AddGrowableRow(1)
        ROMInformation_Sizer.AddGrowableCol(0)
        self.Layout()
        # end wxGlade
        self.__LocalInit ()
        self.Thaw()
        
    def __LocalInit ( self ):
        try:
            self.ROM = self.Current_Ctrl.Get_ROM ( self.Current_Ctrl.GetFocusedItem() )
        except:
            self.Close()
            
        self.CaseW = 214
        self.CaseH = 384
        self.SSW = 256
        self.SSH = 384
        
        self.Case_Bitmap.SetBitmap( Utils.Get_Case( self.ROM, self.CaseW, self.CaseH ) )
        self.SS_Bitmap.SetBitmap( Utils.Get_Screenshot( self.ROM, self.SSW, self.SSH ) )
        
        self.Icon_Bitmap.SetBitmap( self.Current_Ctrl.Get_Item_Icon( self.Current_Ctrl.GetFocusedItem() ) )
        
        self.Comment_Text.SetLabel ( self.ROM.Comment )
        self.Title_Text.SetLabel ( self.ROM.Title.replace ("&","&&") )

        if Config.Config ["Use_Trimmed"]:
            if self.ROM.Trimmed:
                ROMSize_String = _( "%s, Trimmed Size : %s" ) % ( Utils.Format_ROM_Size( self.ROM.ROM_Size ), Utils.Format_ROM_Size ( self.ROM.Effective_Size ) )
            else:
                ROMSize_String = _( "%s, Trimmed Size : N/A" ) % Utils.Format_ROM_Size( self.ROM.ROM_Size )
        else:
            ROMSize_String = Utils.Format_ROM_Size ( self.ROM.ROM_Size )

        self.ROM_Size_Text.SetLabel (ROMSize_String)
#        self.ROM_Size_Text.SetLabel( Utils.Format_ROM_Size ( self.ROM.ROM_Size ) )

#        if self.ROM.Trimmed:
#            Trimmed = Utils.Format_ROM_Size ( self.ROM.Effective_Size )
#        else:
#            Trimmed = "N/A"
#        self.Trimmed_Size_Text.SetLabel( Trimmed )
        
        if self.ROM.Location == 254:
            self.Location_Text.SetLabel( _( "Unknown" ) )
        else:
            try:
                self.Location_Text.SetLabel( Config.Config ["Locations"][self.ROM.Location] )
            except:
                self.Location_Text.SetLabel( _( "Unknown/New" ) + " (%d)" % self.ROM.location )

        Language_String = ""
        for Language in Config.Config ["Languages"]:
            if self.ROM.Language & Language:
                Language_String +=  Config.Config ["Languages"][Language]+ ", "

        if Language_String == "":
            Language_String = "Unknown, "
        self.Language_Text.SetLabel( Language_String[:-2] )
        
        self.Publisher_Text.SetLabel( self.ROM.Publisher )
        self.Source_ROM_Text.SetLabel( self.ROM.Source_ROM )
        self.Genre_Text.SetLabel( self.ROM.Genre )
        self.Save_Type_Text.SetLabel( self.ROM.Save_Type )
        self.ROM_CRC_Text.SetLabel( self.ROM.ROM_CRC )
        self.Internal_Name_Text.SetLabel( self.ROM.Internal_Name )
        if self.ROM.Serial == "":
            self.Serial_Text.SetLabel( _("Unknown") )
        else:
            self.Serial_Text.SetLabel( self.ROM.Serial )
        self.Version_Text.SetLabel( self.ROM.Version )
        if self.ROM.Wifi:
            self.Wifi_Text.SetLabel( _( "Yes" ) )
        else:
            self.Wifi_Text.SetLabel( _( "No" ) )
            
        self.Dump_Date_Text.SetLabel( self.ROM.Dump_Date )
        self.Filename_Text.SetLabel( "N/A" )
        self.Saved_Games_Text.SetLabel( "%d" % self.ROM.Saves )

        Str = ", "
        Str = Str.join ( self.ROM.Tags )
        if Str == "":
            Str = _( "None" )

        self.Tags_Text.SetLabel(Str)
        
        if self.From_Device == False:
            self.ROMInformation_Static_Sizer_staticbox.SetLabel( " " + self.ROM.Archive_File.replace ("&","&&") + " " )
        else:
            self.ROMInformation_Static_Sizer_staticbox.SetLabel( " " + self.ROM.Name_On_Device.replace ("&","&&") + " " )
        
        if self.ROM.Saves > 0:
            self.Save_Game_Button.Show()
        else:
            self.Save_Game_Button.Hide()

        lsize = self.Label_Release_Group.GetSize()
        self.Label_Icon.SetMinSize( lsize )
        self.Label_Title.SetMinSize( lsize )
        self.Label_Languages.SetMinSize( lsize )
        self.Label_Filename.SetMinSize( lsize )
        self.Label_Size.SetMinSize( lsize )
        self.Label_Save_Type.SetMinSize( lsize )
        self.Label_Version.SetMinSize( lsize )
        self.Label_Tags.SetMinSize( lsize )
        self.Label_Internal_Name.SetMinSize( lsize )
        self.Label_Publisher.SetMinSize( lsize )

        rsize = self.Label_Saved_Games.GetSize()
        self.Label_Genre.SetMinSize( rsize )
        self.Label_Dump_Date.SetMinSize( rsize)
        self.Label_CRC.SetMinSize( rsize )
        self.Label_Location.SetMinSize( rsize )
        self.Label_Serial.SetMinSize( rsize )
        self.Label_Wifi.SetMinSize( rsize )
        
#        self.Label_Trimmed_Size.SetMinSize( rsize )
        
        self.Fit()
        self.Center()

        Item = self.Current_Ctrl.GetFocusedItem()
        if Item == 0:
            self.Previous_Button.Disable()
        else:
            self.Previous_Button.Enable()                        
        if Item == self.Current_Ctrl.GetItemCount() - 1:
            self.Next_Button.Disable()
        else:
            self.Next_Button.Enable()
            
    def On_Previous( self, event ): # wxGlade: cROMInformation.<event_handler>
        Item = self.Current_Ctrl.GetFocusedItem()
        self.Current_Ctrl.SetItemState ( Item, 0, wx.LIST_STATE_FOCUSED|wx.LIST_STATE_SELECTED )
        Item -= 1
        self.Current_Ctrl.SetItemState ( Item, wx.LIST_STATE_FOCUSED|wx.LIST_STATE_SELECTED, wx.LIST_STATE_FOCUSED|wx.LIST_STATE_SELECTED )
        self.Current_Ctrl.EnsureVisible( Item )
        self.__LocalInit()

    def On_Next( self, event ): # wxGlade: cROMInformation.<event_handler>
        Item = self.Current_Ctrl.GetFocusedItem()
        self.Current_Ctrl.SetItemState (Item, 0, wx.LIST_STATE_FOCUSED|wx.LIST_STATE_SELECTED)
        Item += 1
        self.Current_Ctrl.SetItemState (Item, wx.LIST_STATE_FOCUSED|wx.LIST_STATE_SELECTED, wx.LIST_STATE_FOCUSED|wx.LIST_STATE_SELECTED)
        self.Current_Ctrl.EnsureVisible(Item)
        self.__LocalInit()
        
    def On_ViewNFO( self, event ): # wxGlade: cROMInformation.<event_handler>
        dlg = cNFODialog ( self, Current_Ctrl=self.Current_Ctrl )
        dlg.ShowModal()
        dlg.Destroy()

    def On_Save_Game_Button(self, event): # wxGlade: cROMInformation.<event_handler>
        dlg = cSaveGameManager ( self, Save_Comments_Shelve=self.Save_Comments_Shelve, Select="%s - %s" % ( self.ROM.Comment, self.ROM.Title ) )
        dlg.ShowModal ()
        dlg.Destroy()

# end of class cROMInformation