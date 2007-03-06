# -*- coding: ISO-8859-1 -*-

import wx
import urllib2

class MyWeb:
    def __init__ (self,m_Con):
        self.m_Con = m_Con
        
    def GetGenre (self, MyRel, PocketHeavenNum):
#<tr><td>Genre</td><td>Action</td></tr>
#<tr><td>Genre</td><td>n/a</td></tr>
#http://releases.pocketheaven.com/?system=nds&section=release&rel=0100
        Genre = "NA"
        try:
            File = urllib2.urlopen("http://releases.pocketheaven.com/?system=nds&section=release&rel=%04d" % PocketHeavenNum)
            Data = File.readlines()
            File.close()
        except:
            return Genre
    
        for Line in Data:
            Line = Line.strip()
            if Line.find ('<tr><td>Genre</td><td>') != -1:
                StartPos = Line.find('</td><td>') + 9
                return Line [StartPos:Line.find ('</td>',StartPos)]

    def Sync(self,Parent):
        dlg = wx.ProgressDialog( "Syncronizing", 
                             "Synconization in Progress - Page 0",
                              maximum = 6, 
                              parent=Parent, 
                              style = wx.PD_APP_MODAL
                            )
        Count = 1
        SomethingProcessed = False
        while Count > 0:
            wx.Yield()
            dlg.Update( (Count-1) % 6, "Synconization in Progress - Page %d" % ( Count ) )
            wx.Yield()
            try:
                File = urllib2.urlopen("http://releases.pocketheaven.com/?system=nds&section=release_list&sort=Release&serres=%d" % Count)
                Data = File.readlines()
                File.close()
            except:
                Count = 0
                continue
    
            StartFound = None
            for Line in Data:
                Line = Line.strip()
                if Line.find ("?system=nds&section=release&rel=") != -1:
                    StartFound = True
                    SomethingProcessed = True
                    self.Process (Line)
            if StartFound == None:
                Count = -1
            Count += 1
        dlg.Destroy()
        if SomethingProcessed:
            wx.MessageBox( 'Release Numbers have been Syncronized', 'Synconization', wx.OK | wx.ICON_INFORMATION )
        else:
            wx.MessageBox( 'An Error Occured', 'Synconization', wx.OK | wx.ICON_ERROR )
        

    def Process (self,Line):
        c = self.m_Con.cursor()
        Count = 0
        Pos = Line.find ('<tr><td><a href="?system=nds&section=release&rel=')
        while Pos != -1:
            Start = Line.find ('">',Pos)
            End = Line.find ('</a>',Pos)
            ReleaseStr = Line[Start+2:End]
            if ReleaseStr.isdigit():
                InternalRelease = Line [Pos+49:Pos+49+4]
#                print InternalRelease," - ",ReleaseStr
                PhRel = int (InternalRelease)
                MyRel = int (ReleaseStr)
                try:
                    c.execute ( "update Files set PocketHeavenNum="+str(PhRel)+" where ReleaseNumber="+str(MyRel) )
                except:
                    pass
            
            Count += 1
            Pos += 1
            Pos = Line.find ('<tr><td><a href="?system=nds&section=release&rel=',Pos)
        self.m_Con.commit()
        c.close()
