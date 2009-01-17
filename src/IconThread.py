import wx #@UnusedImport
#import wx.lib.newevent #@Reimport
import threading
import os
import GFX
import Config
from ROMS import MyROMS

class IconThread ( threading.Thread ):
    def __init__ ( self, q ):
        threading.Thread.__init__( self )
        self.q = q
        
    def LoadIcons ( self ):
        To_Process = MyROMS.Master_List_Count

#        self.List2.IconDict = {}
#        self.List2.IconList = wx.ImageList ( 32, 32 )
        
        No_Icon = GFX.getGFX_No_IconBitmap()
#        self.List2.IconList.Add ( No_Icon )
#        self.List2.IconDict [0] = 0
        Count = 1
        for ROM in MyROMS.Master_List:
            if ROM.Found:
                if ROM.Comment [0] != "U":
                    Image_Filename = os.path.join ( Config.Config ["Image_Path"], "%04d.png" % ROM.Image_Number )
                else:
                    Image_Filename = os.path.join ( Config.Config ["Image_Path"], os.path.splitext( os.path.basename ( ROM.Archive_File ) )[0] + ".png" )
                if os.path.isfile( Image_Filename ):
                    try:
                        self.List2.IconList.Add ( wx.Image( Image_Filename, wx.BITMAP_TYPE_PNG ).ConvertToBitmap() )
                    except:
                        self.List2.IconList.Add ( No_Icon )
                else:
                    self.List2.IconList.Add ( No_Icon )
                self.List2.IconDict [ROM.Image_Number] = Count
                Count += 1
        
        self.List1.IconDict = self.List2.IconDict
        self.List1.IconList = self.List2.IconList
        
        self.List2.UpdateIcons()
        self.List1.UpdateIcons()

    def run ( self ):
        while True:
            self.List1, self.List2, self.List, self.Dict = self.q.get()
            if self.List1 == None:
                break
            self.LoadIcons()
            self.q.task_done()

