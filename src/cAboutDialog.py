# -*- coding: iso-8859-15 -*-
# generated by wxGlade 0.6.1 on Thu Nov 08 11:12:01 2007

import wx
import wx.lib.hyperlink as hl

import GFX

# begin wxGlade: dependencies
# end wxGlade

# begin wxGlade: extracode

# end wxGlade

class cAboutDialog(wx.Dialog):
    def __init__(self, *args, **kwds):
        # begin wxGlade: cAboutDialog.__init__
        kwds["style"] = wx.DEFAULT_DIALOG_STYLE
        wx.Dialog.__init__(self, *args, **kwds)
        self.About_Bitmap = wx.StaticBitmap(self, -1, (GFX.catalog ["GFX_About"].getBitmap()))
        self.TitleText = wx.StaticText(self, -1, _("RToolDS"), style=wx.ALIGN_CENTRE)
        self.Web_Site_Label = wx.StaticText(self, -1, _("Web Site :"))
        self.Web_Site_HL = hl.HyperLinkCtrl(self, -1, "N/A", URL="")
        self.EMail_Label = wx.StaticText(self, -1, _("E-Mail :"))
        self.EMail_HL = hl.HyperLinkCtrl(self, -1, "N/A", URL="")
        self.label_1 = wx.StaticText(self, -1, _("Special Thanks To:\n"))
        self.label_2 = wx.StaticText(self, -1, _("FifthE1ement @ "))
        self.Web_Site_HL_copy = hl.HyperLinkCtrl(self, -1, "www.moddz.com", URL="http://www.moddz.com")
        self.label_3 = wx.StaticText(self, -1, _(" for Beta Testing, Graphics, Ideas and Patience"))
        self.label_4 = wx.StaticText(self, -1, _("All @ "))
        self.Web_Site_HL_copy_copy = hl.HyperLinkCtrl(self, -1, "www.advanscene.com", URL="http://www.advanscene.com")
        self.label_5 = wx.StaticText(self, -1, _(" for the Custom ROM List"))
        self.Static_Line = wx.StaticLine(self, -1)
        self.OK_Button = wx.Button(self, wx.ID_OK, _("OK"))

        self.__set_properties()
        self.__do_layout()
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: cAboutDialog.__set_properties
        self.SetTitle(_("About RToolDS"))
        # end wxGlade

    def __do_layout(self):
        self.Freeze()
        # begin wxGlade: cAboutDialog.__do_layout
        About_Sizer = wx.FlexGridSizer(6, 1, 0, 0)
        sizer_9 = wx.BoxSizer(wx.VERTICAL)
        sizer_13 = wx.FlexGridSizer(1, 3, 0, 0)
        sizer_10 = wx.FlexGridSizer(1, 3, 0, 0)
        Links_Sizer = wx.FlexGridSizer(2, 2, 0, 5)
        About_Sizer.Add(self.About_Bitmap, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5)
        About_Sizer.Add(self.TitleText, 0, wx.ALL|wx.EXPAND, 10)
        Links_Sizer.Add(self.Web_Site_Label, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        Links_Sizer.Add(self.Web_Site_HL, 1, wx.EXPAND, 0)
        Links_Sizer.Add(self.EMail_Label, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        Links_Sizer.Add(self.EMail_HL, 1, wx.EXPAND, 0)
        Links_Sizer.AddGrowableCol(1)
        About_Sizer.Add(Links_Sizer, 1, wx.ALL|wx.EXPAND, 5)
        sizer_9.Add(self.label_1, 0, wx.ALL, 3)
        sizer_10.Add(self.label_2, 0, wx.ALL, 3)
        sizer_10.Add(self.Web_Site_HL_copy, 1, wx.ALIGN_CENTER_VERTICAL, 0)
        sizer_10.Add(self.label_3, 0, wx.ALL|wx.EXPAND, 3)
        sizer_10.AddGrowableCol(2)
        sizer_9.Add(sizer_10, 1, wx.EXPAND, 0)
        sizer_13.Add(self.label_4, 0, wx.ALL, 3)
        sizer_13.Add(self.Web_Site_HL_copy_copy, 1, wx.ALIGN_CENTER_VERTICAL, 0)
        sizer_13.Add(self.label_5, 0, wx.ALL|wx.EXPAND, 3)
        sizer_13.AddGrowableCol(2)
        sizer_9.Add(sizer_13, 1, wx.EXPAND, 0)
        About_Sizer.Add(sizer_9, 1, wx.EXPAND, 0)
        About_Sizer.Add(self.Static_Line, 0, wx.ALL|wx.EXPAND, 5)
        About_Sizer.Add(self.OK_Button, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL, 5)
        self.SetSizer(About_Sizer)
        About_Sizer.Fit(self)
        About_Sizer.AddGrowableCol(0)
        self.Layout()
        self.Centre()
        # end wxGlade
        self.Thaw()

# end of class cAboutDialog


