# -*- coding: iso-8859-15 -*-
# generated by wxGlade 0.6.1 on Tue Dec 11 12:10:17 2007

import wx

import os
import sys

import Config
import Utils
from ColumnListCtrlMixin import SGCListCtrlMixin

# begin wxGlade: dependencies
# end wxGlade

# begin wxGlade: extracode

# end wxGlade

class cRenameFiles( wx.Dialog ):
    def __init__( self, *args, **kwds ):
        # begin wxGlade: cRenameFiles.__init__
        kwds["style"] = wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER | wx.THICK_FRAME
        wx.Dialog.__init__( self, *args, **kwds )
        self.LabelText = wx.StaticText( self, - 1, _( "Double Click or Press Enter on a Line to Rename the File as it is Copied :" ) )
        self.RenameListCtrl = SGCListCtrlMixin( self, - 1 )
        self.OK = wx.Button( self, wx.ID_OK, _( "OK" ) )
        self.Cancel = wx.Button( self, wx.ID_CANCEL, _( "Cancel" ) )

        self.__set_properties()
        self.__do_layout()

        self.Bind( wx.EVT_BUTTON, self.On_OK, id = wx.ID_OK )
        # end wxGlade

    def __set_properties( self ):
        # begin wxGlade: cRenameFiles.__set_properties
        self.SetTitle( _( "Rename Files" ) )
        self.SetSize( ( 700, 400 ) )
        # end wxGlade

    def __do_layout( self ):
        self.Freeze()
        # begin wxGlade: cRenameFiles.__do_layout
        grid_sizer_1 = wx.FlexGridSizer( 2, 1, 0, 0 )
        Convert_Sizer3_copy = wx.FlexGridSizer( 1, 5, 0, 0 )
        grid_sizer_17 = wx.FlexGridSizer( 2, 1, 0, 0 )
        grid_sizer_17.Add( self.LabelText, 0, wx.ALL, 3 )
        grid_sizer_17.Add( self.RenameListCtrl, 1, wx.EXPAND, 0 )
        grid_sizer_17.AddGrowableRow( 1 )
        grid_sizer_17.AddGrowableCol( 0 )
        grid_sizer_1.Add( grid_sizer_17, 1, wx.EXPAND, 0 )
        Convert_Sizer3_copy.Add( ( 20, 20 ), 0, wx.EXPAND, 0 )
        Convert_Sizer3_copy.Add( self.OK, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5 )
        Convert_Sizer3_copy.Add( ( 20, 20 ), 0, wx.EXPAND, 0 )
        Convert_Sizer3_copy.Add( self.Cancel, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5 )
        Convert_Sizer3_copy.Add( ( 20, 20 ), 0, wx.EXPAND, 0 )
        Convert_Sizer3_copy.AddGrowableCol( 0 )
        Convert_Sizer3_copy.AddGrowableCol( 4 )
        grid_sizer_1.Add( Convert_Sizer3_copy, 1, wx.TOP | wx.BOTTOM | wx.EXPAND, 5 )
        self.SetSizer( grid_sizer_1 )
        grid_sizer_1.AddGrowableRow( 0 )
        grid_sizer_1.AddGrowableCol( 0 )
        self.Layout()
        self.Centre()
        # end wxGlade
        self.__LocalInit ()        
        self.Thaw()
        
    def __LocalInit ( self ):
        self.SetSize( Config.Config ["Rename_Size"] )
        
        if Config.Config ["Rename_Position"] [ 0 ] == - 1:
            self.CentreOnScreen ()
        else:
            self.SetPosition( Config.Config ["Rename_Position"] )
            
        self.Bind( wx.EVT_SIZE, self.On_Window_Size )
        self.Bind( wx.EVT_MOVE, self.On_Window_Move )
        
        self.RenameListCtrl.InsertColumn ( 0, _( "ROM" ) )
        self.RenameListCtrl.InsertColumn ( 1, _( "Renamed" ) )
        
        self.RenameListCtrl.Bind ( wx.EVT_CHAR, self.On_List_KeyDown )
        
        self.Results = []

    def Populate ( self, ROMS ):
        self.ROMS = ROMS
        Count = 0
        for ROM in self.ROMS:
            index = self.RenameListCtrl.InsertStringItem ( sys.maxint, os.path.splitext ( ROM.ROM_File )[0] )
            Str = os.path.split ( os.path.splitext ( Utils.Get_Name_on_Device ( ROM ) )[0] )[1]

            self.RenameListCtrl.SetStringItem ( index, 1, Str )
            self.RenameListCtrl.SetItemData( index, Count )
            Count += 1

        self.RenameListCtrl.SetColumnWidth( 0, wx.LIST_AUTOSIZE )
        self.RenameListCtrl.SetColumnWidth( 1, 10 )
        self.RenameListCtrl.SetColumnWidth ( 0, self.RenameListCtrl.GetColumnWidth( 0 ) + 5 )
        
        self.RenameListCtrl.SetFocus()
        self.RenameListCtrl.Focus( 0 )
        self.RenameListCtrl.SetItemState( 0, wx.LIST_STATE_FOCUSED | wx.LIST_STATE_SELECTED, wx.LIST_STATE_FOCUSED | wx.LIST_STATE_SELECTED )

        self.RenameListCtrl.Bind ( wx.EVT_CHAR, self.On_List_KeyDown )

    def On_Window_Size ( self, event ):
        Config.Config ["Rename_Size"] = self.GetSize()
        event.Skip ()
    
    def On_Window_Move ( self, event ):
        Config.Config ["Rename_Position"] = self.GetScreenPosition()
        event.Skip ()

    def On_OK( self, event ): # wxGlade: cRenameFiles.<event_handler>
        for Count in range ( 0, self.RenameListCtrl.GetItemCount() ):
            MyListItem = self.RenameListCtrl.GetItem( Count, 1 )
            self.Results.append ( os.path.join ( Config.Config ["Device_Path"], MyListItem.GetText() ) + ".nds" )
        
        event.Skip()

    def On_List_KeyDown( self, event ): # wxGlade: MySaveGameComments.<event_handler>
        if event.GetUnicodeKey() == 13: # Return
            self.RenameListCtrl.col_locs = [0]
            loc = 0
            for n in range( self.RenameListCtrl.GetColumnCount() ):
                loc = loc + self.RenameListCtrl.GetColumnWidth( n )
                self.RenameListCtrl.col_locs.append( loc )

            self.RenameListCtrl.OpenEditor( 1, self.RenameListCtrl.GetFirstSelected() )
        else:
            event.Skip ()

# end of class cRenameFiles