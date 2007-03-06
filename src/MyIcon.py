import sys
import wx

if sys.platform == "win32":
    import win32api

    def GetIcon():
        exeName = win32api.GetModuleFileName( win32api.GetModuleHandle( None ) )
        icon = wx.Icon( exeName, wx.BITMAP_TYPE_ICO )
        return icon
    
elif sys.platform == "linux":
    def GetIcon():
        return None