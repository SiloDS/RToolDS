# -*- coding: ISO-8859-1 -*-

import wx

class cDropTarget( wx.PyDropTarget ):
    def __init__( self, window ):
        wx.PyDropTarget.__init__( self )
        self.dv = window

        self.data = wx.CustomDataObject( "RToolDS_DD" )
        self.SetDataObject( self.data )

    def OnEnter( self, dummy_x, dummy_y, d ):
        return d

    def OnLeave( self ):
        pass

    def OnDrop( self, dummy_x, dummy_y ):
        return True

    def OnDragOver( self, dummy_x, dummy_y, d ):
        return d

    def OnData( self, dummy_x, dummy_y, d ):
        return d  