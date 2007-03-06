# -*- coding: ISO-8859-1 -*-

import wx

class MyFileDropTarget(wx.PyDropTarget):
    def __init__(self, window):
        wx.PyDropTarget.__init__(self)
        self.dv = window

        self.data = wx.CustomDataObject("RToolDS_DD")
        self.SetDataObject(self.data)

    def OnEnter(self, x, y, d):
        return d

    def OnLeave(self):
        pass

    def OnDrop(self, x, y):
        return True

    def OnDragOver(self, x, y, d):
        return d

    def OnData(self, x, y, d):
        return d  