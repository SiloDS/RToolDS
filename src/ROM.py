#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

import wx

class ROM:
        def __init__( self, Data ):
            Count = 0
            self.m_ID = Data[Count]
            Count += 1
            self.m_ReleaseNumber = Data[Count]
            Count += 1
            self.m_DisplayName = Data[Count]
            Count += 1
            self.m_FileName = Data[Count]
            Count += 1
            self.m_DirectoryName = Data[Count]
            Count += 1
            self.m_InternalZipName = Data[Count]
            Count += 1
            self.m_Size = Data[Count]
            Count += 1
            self.m_Date = Data[Count]
            Count += 1
            Temp_Image = wx.EmptyImage ( 32, 32 )
            Temp_Image.SetData ( Data[Count] )
            self.m_LargeImage = Temp_Image.ConvertToBitmap ()
            Count += 1
            self.m_SmallImage = Data[Count]
            Count += 1
            self.m_Header_Title = Data[Count]
            Count += 1
            self.m_Header_Game_Code = Data[Count]
            Count += 1
            self.m_Header_Maker_Code = Data[Count]
            Count += 1
            self.m_Header_Card_Size = Data[Count]
            Count += 1
            self.m_Header_Logo_Title = Data[Count]
            Count += 1
            self.m_TrimSize = Data[Count]
            Count += 1
            self.m_PocketHeavenNum = Data[Count]
            Count += 1
            self.m_Genre = Data[Count]
            Count += 1
            self.m_PocketHeavenGenre = Data[Count]
            Count += 1

        