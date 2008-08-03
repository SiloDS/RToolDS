# -*- coding: iso-8859-1 -*-

import wx
import cPickle
import os

import Utils

Config_Version = 42
Version_String = "0.3.1342 Beta"

Config = {}

def Load():
    global Config_Version, Config
    
    Config = {}
    
    try:
        Config_File = open ( "RToolDS.cfg", 'rb' )
    except:
        Load_Defaults ( 0 )
        return True

    File_Version = cPickle.load ( Config_File )
    Config       = cPickle.load ( Config_File )
    
    if File_Version != Config_Version:
        Load_Defaults ( File_Version )
        
    Config_File.close()

    Config ["Current_Search"] = ""
#    Config ["ROM_Path"] = "E:\\misc\\Emulators\\DS\\Roms"
#    Config ["Device_Path"] = "L:\\"
#    Config ["Image_Path"] = "E:\\Misc\\Emulators\\DS\\ndscrc\\Cache\\img"
#    Config ["NFO_Path"] = "E:\\Misc\\Emulators\\DS\\ndscrc\\Cache\\nfo"    
    
#    Config ["ROM_Path"] = "/home/rich/ds/roms"
#    Config ["Device_Path"] = "/device"
#    Config ["Image_Path"] = "/home/rich/ds/ndscrc/Cache/img"
#    Config ["NFO_Path"] = "/home/rich/ds/ndscrc/Cache/nfo"    
    return True

def Save():
    global Config_Version, Config
    
    try:
        Config_File = open ( "RToolDS.cfg", 'wb' )
    except:
        return False
    
    cPickle.dump ( Config_Version, Config_File )
    cPickle.dump ( Config, Config_File )

    Config_File.close()
    
    return True
    
def Load_Defaults( Version ):
    if Version < 1: # No Config File so set Version 1 Defaults
        Config ["Window_Size"] = ( 994, 726 )
        Config ["Window_Position"] = ( -1, -1 )
        Config ["Window_Maximized"] = False
        Config ["Sash_Position"] = -1
        Config ["Sash_Position_Maximized"] = -1
        Config ["Master_XML_URL"] = "http://www.advanscene.com/offline/datas/ADVANsCEne_RToolDS.zip"
        Config ["Master_XML_File"] = "ADVANsCEne_RToolDS.xml"
        Config ["Master_XML_Version_URL"] = "http://www.advanscene.com/offline/version/ADVANsCEne_RToolDS.txt"
        Config ["Parse_Subdirs"] = True
        Config ["ROM_Path"] = ""
        Config ["Device_Path"] = "D:\\"
        Config ["Image_Path"] = ""
        Config ["NFO_Path"] = ""
        Config ["Save_Path"] = ""
        Config ["Log_Size"] = ( 500, 400 )
        Config ["Log_Position"] = ( -1, -1 )
        Config ["ROM_Extensions"] = [".nds"]
        Config ["Find_Unknown"] = True
        Config ["Unknown_Name"] = "ARCHIVE" # or "FILENAME" 
        Config ["Show_Alternate_Colours"] = True
        Config ["Alternate_Colour"] = wx.Color ( 245, 245, 245 )
        Config ["Pending_Colour"] = wx.Color (173, 216, 230)

        Config ["Show_ROM_Size_In"] = "MegaBytes"
        Config ["RealTime_Search"] = True
        Config ["Current_Search"] = ""
        Config ["Filter_Location"] = 255
        Config ["Filter_Language"] = 0
        Config ["Filter_Genre"] = _("All Genres")
        Config ["Filter_Size"] = 0
        Config ["Filter_Exact_Size"] = False
        Config ["Filter_Use_Exact_Sizes"] = False
        Config ["Use_Trimmed"] = True
        Config ["SwapSSCase"] = False
        Config ["Show_Splash"] = True
        
        Config ["Hide_Screenshots"] = False
        Config ["Hide_Case_Pictures"] = False
        Config ["Hide_Language"] = False
        Config ["Hide_Location"] = False
        Config ["Hide_Genre"] = True
        Config ["Hide_Size"] = False
        Config ["Hide_Backup_Save_Games"] = False
        Config ["Hide_CRC"] = True
        Config ["Hide_Publisher"] = False
        Config ["Hide_Release_Group"] = True
        Config ["Hide_Save_Game_Type"] = False
        Config ["Hide_Internal_Name"] = True
        Config ["Hide_Serial"] = True
        Config ["Hide_Version"] = True
        Config ["Hide_Wifi"] = False
        Config ["Hide_Tags"] = True
        
        Config ["Show_Toolbar"] = True
        Config ["Toolbar_Size"] = "24"
        Config ["Show_Search"] = True
        Config ["Show_Filter"] = True
        Config ["Sort"] = "Release Number"
        Config ["Sort_Reverse"] = False
        
        Config ["Show_XXXX_Files"] = True
        Config ["Show_Unknown_Files"] =  True

        Config ["Copy_Saves_with_ROM"] = True
        Config ["Device_Dirs_to_Search"] = ["NDS", "ROMS", "Games"]
        Config ["Search_Device_Subdirs"] = True
        Config ["Exclude_Dirs_on_Device" ]      = ["Recycled", "System Volume Information"]
        Config ["Exclude_Dirs_on_Device_Lower"] = ["recycled", "system volume information"]

        Config ["ROM_Extensions"] = [ ".nds" ]
        
        Config ["NFO_Size"] = ( 600, 500 )
        Config ["NFO_Position"] = ( -1, -1 )
        Config ["NFO_Zoom"] = 8

        Config ["Statistics_Size"] = ( 500, 400 )
        Config ["Statistics_Position"] = ( -1, -1 )
        
        Config ["Safe_Trim"] = 188
        
        Config ["Current_Tag"] = _("All ROMs")
        Config ["Last_Tag"] = ""
        
        Config ["Confirm_Delete"] = True
        
        Config ["First_Run"] = True

        Config ["SGM_Position"] = ( -1, -1 )
        Config ["SGM_Size"] = ( 600, 400 )
        Config ["SGM_Col_Sizes"] = [330, 25, 125, 100]
        Config ["Save_Games_to_Keep"] = 5

        Config ["SC_Position"] = ( -1, -1 )
        Config ["SC_Size"] = ( 600, 400 )
        Config ["SC_Col_Sizes"] = [-1, -1 ]
        Config ["Use_Save_Comments"] = True

        Config ["Columns"] = ["Icon", "Release Number", "Name", "Size", "Trimmed", 
                              "Saves", "Archive", "ROM File", "Location", "Genre", 
                              "Original Size", "Release Group", "CRC", "Save Type", 
                              "Publisher", "Internal Name", "Serial", "Version", "Wi-Fi", "Tags" ]
        Config ["ROMColumn_Titles"] = { "Icon":_( "Icon" ), "Release Number":_( "No" ), 
                                        "Name":_( "Title" ), "Size":_( "Size" ), "Trimmed":_( "Trimmed" ), 
                                        "Saves":_( "Saves" ), "Archive":_( "Archive" ), 
                                        "ROM File":_( "ROM File" ), "Location":_( "Region" ), 
                                        "Genre":_( "Genre" ), "Original Size":_( "Original Size" ), 
                                        "Release Group":_( "Group" ), "CRC":_( "CRC" ), 
                                        "Save Type":_( "Save Type" ), "Publisher":_( "Publisher" ), 
                                        "Internal Name":_( "Internal Name" ), "Serial":_( "Serial" ), 
                                        "Version":_( "Version" ), "Wi-Fi":_( "Wi-Fi" ), "Tags":_( "Tags" ) }
        Config ["ROMColumns"] = [ "Icon", "Release Number", "Name", "Size", "Trimmed", "Saves" ]
        Config ["ROMColumn_Sizes"]  = {"Icon":36, "Release Number":37, "Name":265, "Size":53, "Saves":50, 
                                       "Trimmed":37, "Archive":380, "ROM File":321, "Location":60, 
                                       "Genre":76, "Original Size":54, "Release Group":70, "CRC":68, 
                                       "Save Type":99, "Publisher":88, "Internal Name":105, "Serial":99, 
                                       "Version":27, "Wi-Fi":37, "Tags":105 }
        Config ["CartColumn_Titles"] = { "Icon":_( "Icon" ), "Release Number":_( "No" ), 
                                        "Name":_( "Title" ), "Size":_( "Size" ), "Trimmed":_( "Trimmed" ), 
                                        "Saves":_( "Saves" ), "Archive":_( "Archive" ), 
                                        "ROM File":_( "ROM File" ), "Location":_( "Region" ), 
                                        "Genre":_( "Genre" ), "Original Size":_( "Original Size" ), 
                                        "Release Group":_( "Group" ), "CRC":_( "CRC" ), 
                                        "Save Type":_( "Save Type" ), "Publisher":_( "Publisher" ), 
                                        "Internal Name":_( "Internal Name" ), "Serial":_( "Serial" ), 
                                        "Version":_( "Version" ), "Wi-Fi":_( "Wi-Fi" ), "Tags":_( "Tags" ) }
        Config ["CartColumns"] = [ "Icon", "Release Number", "Name", "Size", "Saves" ]
        Config ["CartColumn_Sizes"]  = {"Icon":36, "Release Number":37, "Name":265, "Size":53, 
                                        "Saves":50, "Trimmed":37, "Archive":380, "ROM File":321, 
                                        "Location":60, "Genre":76, "Original Size":54, 
                                        "Release Group":70, "CRC":68, "Save Type":99, "Publisher":88, 
                                        "Internal Name":105, "Serial":99, "Version":27, "Wi-Fi":37, "Tags":105 }
        Config ["Languages"] = {
                0:_("All Languages"), 
                1:_("French"), 
                2:_("English"), 
                4:_("Chinese"), 
                8:_("Danish"), 
                16:_("Dutch"), 
                32:_("Finnish"), 
                64:_("German"), 
                128:_("Italian"), 
                256:_("Japanese"), 
                512:_("Norwegian"), 
                1024:_("Polish"), 
#                2048:"Portuguese", 
                4096:_("Spanish"), 
                8192:_("Swedish"), 
#                16384:"English (UK)", 
                32768:_("Portuguese (BR)"), 
                65536:_("Korean"),
                131072:_("Russian"),
                262144:_("Greek") }
        Config ["Locations"] = {
                255:_("All Regions"), 
                0:_("Europe"), 
                1:_("USA"), 
                2:_("Germany"), 
                3:_("China"), 
                4:_("Spain"), 
                5:_("France"), 
                6:_("Italy"), 
                7:_("Japan"), 
                8:_("Netherlands"), 
                9:_("England"), 
                10:_("Denmark"), 
                11:_("Finland"), 
                12:_("Norway"), 
                13:_("Poland"), 
                14:_("Portugal"), 
                15:_("Sweden"), 
                16:_("Europe USA"), 
                17:_("Europe USA Japan"), 
                18:_("USA Japan"), 
                19:_("Australia"), 
                20:_("North Korea"), 
                21:_("Brazil"), 
                22:_("South Korea"), 
                23:_("Europe Brazil"), 
                24:_("Europe USA Brazil"), 
                25:_("USA Brazil"),
                26:_("Unknown"),
                27:_("Russia") }
        Config ["Sizes"] = [0, 8*1024*1024, 16*1024*1024, 24*1024*1024,
                            32*1024*1024, 64*1024*1024, 128*1024*1024, 256*1024*1024 ]

        Config ["Country_Codes"] = { "J":"JPN",
                                     'E':"USA",
                                     'P':"EUR",
                                     'D':"NOE",
                                     'F':"NOE",
                                     'I':"ITA",
                                     'S':"SPA",
                                     'H':"HOL",
                                     'K':"KOR",
                                     'X':"EUU",
                                     'Y':"EUU" }
    if Version < 2:
        Config ["AutoCopySaves"] = True
    if Version < 3:
        Config ["Devices"] = [
                                ["Generic 512k (.sav)", Utils.Device_Generic_512, "Generic 512k"],
                                ["Generic 256k (.sav)", Utils.Device_Generic_256, "Generic 256k"],
                                ["Action Replay (.duc)", Utils.Device_Action_Replay, "Action Replay"],
                                ["Action Replay (.dss)", Utils.Device_Action_Replay, ""],
                                ["CycloDS Evolution (.sav)", Utils.Device_Generic_512, "CycloDS Evolution"],
                                ["CycloDS SD (.sav)", Utils.Device_Generic_512, "CycloDS SD"],
                                ["DSLinker (.sav)", Utils.Device_Generic_256, "DSLinker"],
                                ["DS-Xtreme (.sav)", Utils.Device_Generic_256, "DS-Xtreme"],
                                ["EZ-Flash IV (.sav)", Utils.Device_Generic_256, "EZ-Flash IV"],
                                ["EZ-Flash V (.sav)", Utils.Device_Generic_256, "EZ-Flash V"],
                                ["G6 DS Real (.0)", Utils.Device_Generic_512, "G6 DS Real"],
                                ["G6 Lite (.0)", Utils.Device_Generic_256, "G6 Lite"],
                                ["M3 DS Real (.0)", Utils.Device_Generic_512, "M3 DS Real"],
                                ["M3 DS Simply (.sav)", Utils.Device_Generic_512, "M3 DS Simply"],
                                ["M3 SD (.dat)", Utils.Device_Generic_256, "M3 SD"],
                                ["N-Card and Clones (.sav)", Utils.Device_Generic_256, "N-Card and Clones"],
                                ["NinjaDS (.sav)", Utils.Device_Generic_512, "NinjaDS"],
                                ["NinjaPass x9 (.sav)", Utils.Device_Generic_256, "NinjaPass x9"],
                                ["R4 Revolution (.sav)", Utils.Device_R4_512, "R4 Revolution"],
                                ["SuperCard SD (.sav)", Utils.Device_Generic_256, "SuperCard SD"],
                                ["SuperCard DS One (.sav)", Utils.Device_Generic_256, "SuperCard DS One"]
                             ]
        Config ["Default_Device"] = "Generic 256k (.sav)"
    if Version < 4:
        Config ["Last_Import_Path"] = os.getcwd()
        Config ["Convert_Imports"] = False
    if Version < 5:
        Config ["Delete_Saves_with_ROM"] = True
    if Version < 6:
        Config ["Use_Original_Save_Time"] = True
    if Version < 7:
        Config ["Use_Renaming"] = False
        Config ["Rename_Mask"] = ""
    if Version < 8:
        Config ["Swap_SS_and_Case"] = False
    if Version < 9:
        Config ["Use_Smaller_Pictures"] = False
    if Version < 10:
        Config ["AutoCloseUpdate"] = False
    if Version < 11:
        Config ["Show_Device_List"] = True
    if Version < 12:
        Config ["Cart_Sort"] = "Release Number"
        Config ["Cart_Sort_Reverse"] = False
    if Version < 13:
        Config ["Save_Dir_On_Cart"] = ""
    if Version < 14:
        Config ["Auto_Backup_Saved_Games"] = False
    if Version < 15:
        Config ["Country_Codes"]['Y'] = "EUU"
    if Version < 16:
        Config ["Country_Codes"]['R'] = "???"
    if Version < 17:
        Config ["Parse_Subdirs"] = False
        Config ["Device_Dirs_to_Search"] = []
    if Version < 18:
        Config ["Rename_Position"] = ( -1, -1 )
        Config ["Rename_Size"] = ( 700, 400 )
    if Version < 19:
        Config ["Use_Rename_Popup"] = False
    if Version < 20:
        Config ["Country_Codes"]['R'] = "RUS"
        Config ["Country_Codes"]['W'] = "XXX"
        Config ["Country_Codes"]['Z'] = "EUU"
        Config ["Country_Codes"]['U'] = "AUS"
        Config ["Country_Codes"]['C'] = "CHN"
    if Version < 21:
        Config ["Country_Codes"]['J'] = "JPN"
    if Version < 22:
        Config ["Hide_Screenshots"] = False
        Config ["Hide_Case_Pictures"] = False
        Config ["Hide_Language"] = False
        Config ["Hide_Location"] = False
        Config ["Hide_Genre"] = True
        Config ["Hide_Size"] = False
        Config ["Hide_Backup_Save_Games"] = False
        Config ["Hide_CRC"] = True
        Config ["Hide_Publisher"] = False
        Config ["Hide_Release_Group"] = True
        Config ["Hide_Save_Game_Type"] = False
        Config ["Hide_Internal_Name"] = True
        Config ["Hide_Serial"] = True
        Config ["Hide_Version"] = True
        Config ["Hide_Wifi"] = False
        Config ["Hide_Tags"] = True
    if Version < 23:
        Config ["Languages"] = {
                0:_("All Languages"), 
                4:_("Chinese"), 
                8:_("Danish"), 
                16:_("Dutch"), 
                2:_("English"), 
                32:_("Finnish"), 
                1:_("French"), 
                64:_("German"), 
                262144:_("Greek"),
                128:_("Italian"), 
                256:_("Japanese"), 
                65536:_("Korean"),
                512:_("Norwegian"), 
                1024:_("Polish"), 
                32768:_("Portuguese"), 
#                2048:"Portuguese", 
                131072:_("Russian"),
                4096:_("Spanish"), 
                8192:_("Swedish")} 
#                16384:"English (UK)", 
        Config ["Locations"] = {
                255:_("All Regions"), 
                0:_("Europe"), 
                1:_("USA"), 
                2:_("Germany"), 
                3:_("China"), 
                4:_("Spain"), 
                5:_("France"), 
                6:_("Italy"), 
                7:_("Japan"), 
                8:_("Netherlands"), 
#                9:_("England"), 
#                10:_("Denmark"), 
#                11:_("Finland"), 
#                12:_("Norway"), 
#                13:_("Poland"), 
#                14:_("Portugal"), 
#                15:_("Sweden"), 
#                16:_("Europe USA"), 
#                17:_("Europe USA Japan"), 
#                18:_("USA Japan"), 
                19:_("Australia"), 
#                20:_("North Korea"), 
#                21:_("Brazil"), 
                22:_("South Korea"), 
#                23:_("Europe Brazil"), 
#                24:_("Europe USA Brazil"), 
#                25:_("USA Brazil"),
                26:_("Unknown"),
                27:_("Russia") }
        Config ["Country_Codes"] = { "E":"USA",
                                     "P":"EUR",
                                     "J":"JPN",
                                     "X":"EUU",
                                     "Y":"EUU",
                                     "Z":"EUU",
                                     "F":"FRA",
                                     "I":"ITA",
                                     "S":"ESP",
                                     "D":"NOE",
                                     "K":"KOR",
                                     "C":"CHN",
                                     "H":"HOL",
                                     "U":"AUS",
                                     "R":"RUS"}
    if Version < 24:
        Config ["UseShortSaveName"] = False
    if Version < 25:
        Config ["Country_Codes"]['W'] = "EUU"
    if Version < 26:
        Config ["Save_Extensions"] = [ ".sav", ".duc", ".dss", ".0", ".dat" ]
    if Version < 27:
        Config ["Columns"].append ("ROM File (No Ext)")
        Config ["ROMColumn_Titles"]["ROM File (No Ext)"] = "ROM File"
        Config ["ROMColumn_Sizes"]["ROM File (No Ext)"] = 321
        Config ["CartColumn_Titles"]["ROM File (No Ext)"] = "ROM File"
        Config ["CartColumn_Sizes"]["ROM File (No Ext)"] = 321
    if Version < 28:
        Config ["Languages"][-1] = "Unknown"
    if Version < 29:
        Config ["Sizes"] = [0, 8*1024*1024, 16*1024*1024,
                            32*1024*1024, 64*1024*1024, 128*1024*1024, 256*1024*1024 ]
    if Version < 30:
        Config ["Columns"].append ("Filename")
        Config ["ROMColumn_Titles"]["Filename"] = "Filename"
        Config ["ROMColumn_Sizes"]["Filename"] = 99
        Config ["CartColumn_Titles"]["Filename"] = "Filename"
        Config ["CartColumn_Sizes"]["Filename"] = 99
        Config ["Columns"].append ("Dumped")
        Config ["ROMColumn_Titles"]["Dumped"] = "Dumped"
        Config ["ROMColumn_Sizes"]["Dumped"] = 99
        Config ["CartColumn_Titles"]["Dumped"] = "Dumped"
        Config ["CartColumn_Sizes"]["Dumped"] = 99
    if Version < 31:
        Config ["Hide_Icon"] = True
        Config ["Hide_ReleaseNumber"] = True
        Config ["Hide_Title"] = True
    if Version < 32:
        Config ["Search_Method"] = 0
    if Version < 33:
        Config ["Columns"].append ("Save Date")
        Config ["ROMColumn_Titles"]["Save Date"] = "Save Date"
        Config ["ROMColumn_Sizes"]["Save Date"] = 99
        Config ["CartColumn_Titles"]["Save Date"] = "Save Date"
        Config ["CartColumn_Sizes"]["Save Date"] = 99
    if Version < 34:
        Config ["SC_Col_Sizes"] = [-1, -1, -1 ]
    if Version < 35:
        Config ["SC_Size"] = ( 800, 400 )
    if Version < 36:
        Config ["Country_Codes_Lookup"] = { "JPN":7,
                                            "USA":1,
                                            "EUR":0,
                                            "NOE":0,
                                            "ITA":6,
                                            "SPA":4,
                                            "HOL":8,
                                            "KOR":22,
                                            "EUU":0,
                                            "RUS":27 }
    if Version < 37:
        Config ["Devices"] = [
                                ["Generic 512k (.sav)", Utils.Device_Generic_512, "Generic 512k"],
                                ["Generic 256k (.sav)", Utils.Device_Generic_256, "Generic 256k"],
                                ["Acekard2/rpg (.nds.sav)", Utils.Device_Generic_512, "Acekard2/rpg"],
                                ["Action Replay (.duc)", Utils.Device_Action_Replay, "Action Replay"],
                                ["Action Replay (.dss)", Utils.Device_Action_Replay, ""],
                                ["CycloDS Evolution (.sav)", Utils.Device_Generic_512, "CycloDS Evolution"],
                                ["CycloDS SD (.sav)", Utils.Device_Generic_512, "CycloDS SD"],
                                ["DSLinker (.sav)", Utils.Device_Generic_256, "DSLinker"],
                                ["DS-Xtreme (.sav)", Utils.Device_Generic_256, "DS-Xtreme"],
                                ["EZ-Flash IV (.sav)", Utils.Device_Generic_256, "EZ-Flash IV"],
                                ["EZ-Flash V (.sav)", Utils.Device_Generic_256, "EZ-Flash V"],
                                ["G6 DS Real (.0)", Utils.Device_Generic_512, "G6 DS Real"],
                                ["G6 Lite (.0)", Utils.Device_Generic_256, "G6 Lite"],
                                ["M3 DS Real (.0)", Utils.Device_Generic_512, "M3 DS Real"],
                                ["M3 DS Simply (.sav)", Utils.Device_Generic_512, "M3 DS Simply"],
                                ["M3 SD (.dat)", Utils.Device_Generic_256, "M3 SD"],
                                ["N-Card and Clones (.sav)", Utils.Device_Generic_256, "N-Card and Clones"],
                                ["NinjaDS (.sav)", Utils.Device_Generic_512, "NinjaDS"],
                                ["NinjaPass x9 (.sav)", Utils.Device_Generic_256, "NinjaPass x9"],
                                ["R4 Revolution (.sav)", Utils.Device_R4_512, "R4 Revolution"],
                                ["SuperCard SD (.sav)", Utils.Device_Generic_256, "SuperCard SD"],
                                ["SuperCard DS One (.sav)", Utils.Device_Generic_256, "SuperCard DS One"]
                             ]
    if Version < 38:
        Config ["Save_Extensions"] = [ ".sav", ".duc", ".dss", ".0", ".dat", ".nds.sav" ]
    if Version < 39:
        Config ["Devices"] = [
                                ["Generic 512k (.sav)", Utils.Device_Generic_512, "Generic 512k"],
                                ["Generic 256k (.sav)", Utils.Device_Generic_256, "Generic 256k"],
                                ["Acekard2/rpg (.nds.sav)", Utils.Device_Generic_512, "Acekard2/rpg"],
                                ["Action Replay (.duc)", Utils.Device_Action_Replay, "Action Replay"],
                                ["Action Replay (.dss)", Utils.Device_Action_Replay, ""],
                                ["CycloDS Evolution (.sav)", Utils.Device_Generic_512, "CycloDS Evolution"],
                                ["CycloDS SD (.sav)", Utils.Device_Generic_512, "CycloDS SD"],
                                ["DSLinker (.sav)", Utils.Device_Generic_256, "DSLinker"],
                                ["DS-Xtreme (.sav)", Utils.Device_Generic_256, "DS-Xtreme"],
                                ["EZ-Flash IV (.sav)", Utils.Device_Generic_256, "EZ-Flash IV"],
                                ["EZ-Flash V (.sav)", Utils.Device_Generic_256, "EZ-Flash V"],
                                ["G6 DS Real (.0)", Utils.Device_Generic_512, "G6 DS Real"],
                                ["G6 Lite (.0)", Utils.Device_Generic_256, "G6 Lite"],
                                ["M3 DS Real (.sav)", Utils.Device_Generic_512, "M3 DS Real"],
                                ["M3 DS Simply (.sav)", Utils.Device_Generic_512, "M3 DS Simply"],
                                ["M3 SD (.dat)", Utils.Device_Generic_256, "M3 SD"],
                                ["N-Card and Clones (.sav)", Utils.Device_Generic_256, "N-Card and Clones"],
                                ["NinjaDS (.sav)", Utils.Device_Generic_512, "NinjaDS"],
                                ["NinjaPass x9 (.sav)", Utils.Device_Generic_256, "NinjaPass x9"],
                                ["R4 Revolution (.sav)", Utils.Device_R4_512, "R4 Revolution"],
                                ["SuperCard SD (.sav)", Utils.Device_Generic_256, "SuperCard SD"],
                                ["SuperCard DS One (.sav)", Utils.Device_Generic_256, "SuperCard DS One"]
                             ]
    if Version < 40:
        Config ["Devices"] = [
                                ["Generic 512k (.sav)", Utils.Device_Generic_512, "Generic 512k"],
                                ["Generic 256k (.sav)", Utils.Device_Generic_256, "Generic 256k"],
                                ["Acekard2/rpg (.nds.sav)", Utils.Device_Generic_512, "Acekard2/rpg"],
                                ["Action Replay (.duc)", Utils.Device_Action_Replay, "Action Replay"],
                                ["Action Replay (.dss)", Utils.Device_Action_Replay, ""],
                                ["CycloDS Evolution (.sav)", Utils.Device_Generic_512, "CycloDS Evolution"],
                                ["CycloDS SD (.sav)", Utils.Device_Generic_512, "CycloDS SD"],
                                ["DSLinker (.sav)", Utils.Device_Generic_256, "DSLinker"],
                                ["DS-Xtreme (.sav)", Utils.Device_Generic_256, "DS-Xtreme"],
                                ["EZ-Flash IV (.sav)", Utils.Device_Generic_256, "EZ-Flash IV"],
                                ["EZ-Flash V (.sav)", Utils.Device_Generic_256, "EZ-Flash V"],
                                ["G6 DS Real (.0)", Utils.Device_Generic_512, "G6 DS Real"],
                                ["G6 Lite (.0)", Utils.Device_Generic_256, "G6 Lite"],
                                ["M3 DS Real (.sav)", Utils.Device_Generic_512, "M3 DS Real"],
                                ["M3 DS Simply (.sav)", Utils.Device_Generic_512, "M3 DS Simply"],
                                ["M3 SD (.dat)", Utils.Device_Generic_256, "M3 SD"],
                                ["N-Card and Clones (.sav)", Utils.Device_Generic_256, "N-Card and Clones"],
                                ["NinjaDS (.sav)", Utils.Device_Generic_512, "NinjaDS"],
                                ["NinjaPass x9 (.sav)", Utils.Device_Generic_256, "NinjaPass x9"],
                                ["R4 Revolution (.sav)", Utils.Device_R4_512, "R4 Revolution"],
                                ["SuperCard SD (.sav)", Utils.Device_Generic_256, "SuperCard SD"],
                                ["SuperCard DS One 512k (.sav)", Utils.Device_Generic_512, "SuperCard DS One 512k"]
                             ]
        Config ["NFO_Weight"] = wx.FONTWEIGHT_NORMAL
        Config ["NFO_Style"] = wx.FONTSTYLE_NORMAL
        Config ["NFO_Family"] = wx.FONTFAMILY_SWISS
    if Version < 41:
        Config ["NFO_Face"] = "Lucida Console"
    if Version < 42:
#            <imURL>http://www.retrocovers.com/offline/imgs/ADVANsCEne_NDS/</imURL>
#            <icURL>http://www.advanscene.com/offline/imgs/NDSicon/</icURL>
#            <ipsURL>http://www.advanscene.com/offline/ips/NDSips/</ipsURL>
            Config ["imURL"]  = "http://www.retrocovers.com/offline/imgs/ADVANsCEne_NDS/"
            Config ["icURL"]  = "http://www.advanscene.com/offline/imgs/NDSicon/"
            Config ["ipsURL"] = "http://www.advanscene.com/offline/ips/NDSips/"
