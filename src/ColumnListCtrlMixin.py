# -*- coding: ISO-8859-1 -*-

import wx
from wx.lib.mixins.listctrl import CheckListCtrlMixin
from wx.lib.mixins.listctrl import TextEditMixin
from wx.lib.mixins.listctrl import ListCtrlAutoWidthMixin

class ColumnListCtrlMixin( wx.ListCtrl, CheckListCtrlMixin, TextEditMixin ):
    def __init__( self, parent, id, ColumnsToSkip = [ 0 ] ):
        wx.ListCtrl.__init__( self, parent, - 1, style = wx.LC_REPORT | wx.LC_SINGLE_SEL )
        CheckListCtrlMixin.__init__( self )
        TextEditMixin.__init__( self )
        self.Bind( wx.EVT_LIST_BEGIN_LABEL_EDIT, self.OnEndLabelEdit )
        self.ColumnsToSkip = ColumnsToSkip
        
    def OnItemActivated( self, evt ):
        self.ToggleItem( evt.m_itemIndex )
    
    def OnEndLabelEdit( self, event ):
        if event.GetColumn() in self.ColumnsToSkip:
            event.Veto()
        else:
            event.Skip()
            
class SGCListCtrlMixin( wx.ListCtrl, TextEditMixin, ListCtrlAutoWidthMixin ):
    def __init__( self, parent, id, ColumnsToSkip = [ 0 ] ):
        wx.ListCtrl.__init__( self, parent, - 1, style = wx.LC_REPORT | wx.LC_SINGLE_SEL )
        TextEditMixin.__init__( self )
        ListCtrlAutoWidthMixin.__init__ ( self )
        self.Bind( wx.EVT_LIST_BEGIN_LABEL_EDIT, self.OnEndLabelEdit )
        self.ColumnsToSkip = ColumnsToSkip
        
    def OnEndLabelEdit( self, event ):
        if event.GetColumn() in self.ColumnsToSkip:
            event.Veto()
        else:
            event.Skip()
            
class StatsListCtrlMixin( wx.ListCtrl, ListCtrlAutoWidthMixin ):
    def __init__( self, parent, ids ):
        wx.ListCtrl.__init__( self, parent, - 1, style = wx.LC_REPORT | wx.LC_SINGLE_SEL | wx.LC_NO_HEADER )
        ListCtrlAutoWidthMixin.__init__ ( self )
