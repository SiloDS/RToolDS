# -*- coding: iso-8859-15 -*-
# generated by wxGlade 0.6.1 on Fri Nov 09 14:23:34 2007

import wx
import os
import sys
import time
from ColumnListCtrlMixin import StatsListCtrlMixin
if sys.platform == "win32":
    import win32api

import Config
import Utils
from ROMS import MyROMS

# begin wxGlade: dependencies
# end wxGlade

# begin wxGlade: extracode

# end wxGlade

class cStatisticsDialog(wx.Dialog):
    def __init__(self, *args, **kwds):
        # begin wxGlade: cStatisticsDialog.__init__
        kwds["style"] = wx.DEFAULT_DIALOG_STYLE
        wx.Dialog.__init__(self, *args, **kwds)
        self.Statistics_Notebook = wx.Notebook(self, -1, style=0)
        self.MissingXXXXPanel = wx.Panel(self.Statistics_Notebook, -1)
        self.MissingROMSSizer = wx.Panel(self.Statistics_Notebook, -1)
        self.StatisticsPanel = wx.Panel(self.Statistics_Notebook, -1)
        self.SummaryPanel = wx.Panel(self.Statistics_Notebook, -1)
        self.Summary_Text = wx.TextCtrl(self.SummaryPanel, -1, "", style=wx.TE_MULTILINE|wx.TE_READONLY)
        self.Statistics_Text = wx.TextCtrl(self.StatisticsPanel, -1, "", style=wx.TE_MULTILINE|wx.TE_READONLY)
        self.Missing_Ctrl = StatsListCtrlMixin(self.MissingROMSSizer, -1)
        self.MissingXXXX_Ctrl = StatsListCtrlMixin(self.MissingXXXXPanel, -1)
        self.OK_Button = wx.Button(self, wx.ID_OK, _("&OK"))

        self.__set_properties()
        self.__do_layout()
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: cStatisticsDialog.__set_properties
        self.SetTitle(_("Statistics"))
        self.SetSize((506, 406))
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: cStatisticsDialog.__do_layout
        Statistics_Sizer = wx.FlexGridSizer(2, 1, 0, 0)
        MissingXXXXSizer = wx.FlexGridSizer(1, 1, 0, 0)
        MissingSizer = wx.FlexGridSizer(1, 1, 0, 0)
        StatsSizer = wx.FlexGridSizer(1, 1, 0, 0)
        SummarySizer = wx.FlexGridSizer(1, 1, 0, 0)
        SummarySizer.Add(self.Summary_Text, 0, wx.ALL|wx.EXPAND, 3)
        self.SummaryPanel.SetSizer(SummarySizer)
        SummarySizer.AddGrowableRow(0)
        SummarySizer.AddGrowableCol(0)
        StatsSizer.Add(self.Statistics_Text, 0, wx.ALL|wx.EXPAND, 3)
        self.StatisticsPanel.SetSizer(StatsSizer)
        StatsSizer.AddGrowableRow(0)
        StatsSizer.AddGrowableCol(0)
        MissingSizer.Add(self.Missing_Ctrl, 1, wx.ALL|wx.EXPAND, 3)
        self.MissingROMSSizer.SetSizer(MissingSizer)
        MissingSizer.AddGrowableRow(0)
        MissingSizer.AddGrowableCol(0)
        MissingXXXXSizer.Add(self.MissingXXXX_Ctrl, 1, wx.ALL|wx.EXPAND, 3)
        self.MissingXXXXPanel.SetSizer(MissingXXXXSizer)
        MissingXXXXSizer.AddGrowableRow(0)
        MissingXXXXSizer.AddGrowableCol(0)
        self.Statistics_Notebook.AddPage(self.SummaryPanel, _("Summary"))
        self.Statistics_Notebook.AddPage(self.StatisticsPanel, _("Statistics"))
        self.Statistics_Notebook.AddPage(self.MissingROMSSizer, _("Missing ROMs"))
        self.Statistics_Notebook.AddPage(self.MissingXXXXPanel, _("Missing XXXX ROMs"))
        Statistics_Sizer.Add(self.Statistics_Notebook, 1, wx.ALL|wx.EXPAND, 3)
        Statistics_Sizer.Add(self.OK_Button, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5)
        self.SetSizer(Statistics_Sizer)
        Statistics_Sizer.AddGrowableRow(0)
        Statistics_Sizer.AddGrowableCol(0)
        self.Layout()
        self.Centre()
        # end wxGlade
        self.__LocalInit ()

    def __LocalInit (self):
        self.SetSize( Config.Config ["Statistics_Size"] )
        
        if Config.Config ["Statistics_Position"] [ 0 ] == -1:
            self.CentreOnScreen ()
        else:
            self.SetPosition( Config.Config ["Statistics_Position"] )
            
        self.Bind( wx.EVT_SIZE, self.On_Window_Size )
        self.Bind( wx.EVT_MOVE, self.On_Window_Move )
        
        SummaryText  = _("Application Information") + " :\n\n"
        SummaryText += "RToolDS Version : v%s\n" % Config.Version_String
        SummaryText += _("Scene Dat File Version") + " : %04d\n" % (MyROMS.Master_List_XML_Version)
#        SummaryText += "Scene Dat File Date : %s\n\n" % (time.strftime( "%d/%m/%Y %I:%M:%S %p", time.localtime( os.path.getmtime ( Config.Config ["AllXMLFilename"] ) ) ).lower())
        try:
            SummaryText += _("Scene Dat File Date") + " : %s %s\n\n" % (win32api.GetDateFormat (win32api.GetSystemDefaultLCID(),0,time.localtime( os.path.getmtime ( Config.Config ["Master_XML_File"] ) ) ).lower(), win32api.GetTimeFormat (win32api.GetSystemDefaultLCID(),0,time.localtime( os.path.getmtime ( Config.Config ["Master_XML_File"] ) ) ))
        except:
            SummaryText += _("Scene Dat File Date") + " : " + _("Not Availabe") + "\n\n"

        SummaryText += _("Official ROM Information") + " :\n\n"
        
        self.Missing_Ctrl.InsertColumn( 0, "ROM Name" )
        self.MissingXXXX_Ctrl.InsertColumn( 0, "ROM Name" )

        XXXX = []
        Size = 0
        AllXXXX = 0
        UnknownCount = 0
        Current_Count = 0
        MyROMS.Process_All = True
        for ROM in MyROMS:
            if ROM.Found:
                Current_Count += 1
            if ROM.Comment [0].upper() == "U":
                UnknownCount += 1
                continue
            if ROM.Comment.upper() == "XXXX":
                AllXXXX += 1
            try: #TODO: WTF?
                tmpROM = MyROMS.Lookup_ROM_CRC (ROM.ROM_CRC)
                Size += os.path.getsize(tmpROM.Archive_File)
            except:
                if ROM.Comment.upper() == "XXXX":
                    XXXX.append (ROM.Comment + " - " + ROM.Title)
                else:
                    self.Missing_Ctrl.InsertStringItem(sys.maxint, ROM.Comment + " - " + ROM.Title)
                    
        MyROMS.Process_All = False

        XXXX.sort()
        for Item in XXXX:
            self.MissingXXXX_Ctrl.InsertStringItem(sys.maxint, Item)
            
        MyXXXX = AllXXXX - len (XXXX)

        SummaryText += _("Total ROMs Released") + " : %d\n" % (MyROMS.Master_List_Count - UnknownCount)

        SummaryText += _("Game ROMs") + " : %d\n" % (MyROMS.Master_List_Count - AllXXXX - UnknownCount)
        SummaryText += _("Demo ROMs") + " (XXXX) : %d\n\n" % AllXXXX

        SummaryText += _("My Library") + " :\n\n"
        SummaryText += _("Total Official ROMs") + " : %d\n" % (Current_Count - UnknownCount)
        SummaryText += _("Official Game ROMs") + " : %d\n" % (Current_Count - UnknownCount - MyXXXX)
        SummaryText += _("Official Demo ROMs") + " : %d\n" % (MyXXXX)
        SummaryText += _("Unknown ROMs") + " : %d\n\n" % (UnknownCount)
        SummaryText += _("Official Missing ROMs  : %d of which %d are Demo (XXXX) ROMs") % (MyROMS.Master_List_Count - Current_Count, len (XXXX)) + "\n\n"

        SummaryText += _("ROM Library Size") + " : %s" % (Utils.Format_Normal_Size (Size))

        self.Summary_Text.AppendText(SummaryText)
        
        self.Statistics_Text.AppendText(_("ROMs In My Collection") + "\n\n" + _("ROMs by Region") + " :\n\n")
        
        Temp = {}
        for Key in Config.Config ["Locations"].keys():
            if Key != 255:
                Temp [Key] = 0

        MyROMS.Process_All = True
        for ROM in MyROMS:
            if ROM.Found:
                try:
                    Temp [ROM.Location] = Temp [ROM.Location] + 1
                except:
                    pass
        MyROMS.Process_All = False
            
        for Key in Temp.keys():
            if Temp[Key] != 0:
                self.Statistics_Text.AppendText("%s : %d\n" % (Config.Config ["Locations"][Key], Temp[Key]))

        self.Statistics_Text.AppendText("\n" + _("ROMs by Language") + " :\n\n")

        Temp = {}
        for Key in Config.Config ["Languages"].keys():
            if Key != 0:
                Temp [Key] = 0

        MyROMS.Process_All = True
        for ROM in MyROMS:
            if ROM.Found:
                try:
                    for t in Temp.keys():
                        if t & ROM.Language: 
                            Temp [t] = Temp [t] + 1
                except:
                    pass
        MyROMS.Process_All = False
            
        for Key in Temp.keys():
            if Temp[Key] != 0:
                self.Statistics_Text.AppendText("%s : %d\n" % (Config.Config ["Languages"][Key], Temp[Key]))
        
        self.Statistics_Text.AppendText("\n" + _("ROMs by Genre") + " :\n")

        Temp = {}
        for Key in MyROMS.Genres:
            Temp [Key] = 0

        MyROMS.Process_All = True
        for ROM in MyROMS:
            if ROM.Found:
                try:
                    Temp [ROM.Genre] = Temp [ROM.Genre] + 1
                except:
                    pass
        MyROMS.Process_All = False
            
        for Key in Temp.keys():
            if Temp[Key] != 0:
                self.Statistics_Text.AppendText("\n%s : %d" % (Key, Temp[Key]))

    def On_Window_Size ( self, event ):
        Config.Config ["Statistics_Size"] = self.GetSize()
        event.Skip ()
    
    def On_Window_Move ( self, event ):
        Config.Config ["Statistics_Position"] = self.GetScreenPosition()
        event.Skip ()


# end of class cStatisticsDialog