import os

Ignore = [
"v0.2.634",
"v0.2.632",
"v0.2.631",
"v0.2.890",
"v0.2.868",
"v0.2.1064",
"v0.2.1065",
"v0.2.1106",
"v0.2.1159",
"v0.2.1160",
"v0.3.1328",
"v0.3.1381"
]

def Process (ReleasePre, ReleaseSuf, START_ENTRY, END_ENTRY):
    CMD = '"svn.exe" log https://server/svn/RToolDS -r' + START_ENTRY + ':' + END_ENTRY
    
    File = os.popen (CMD)
    
    State = "None"
    
    for Line in File:
        Line = Line.strip ()
        
        if Line == "------------------------------------------------------------------------":
            State = "Start"
            continue
        if State == "Start":
           Data = Line.split (" | ")
           RevNum = int (Data[0][1:])
    #       print ReleasePre + str (RevNum) + ReleaseSuf
           State = "Blank"
           continue
        if State == "Blank":
            State = "Text1"
            continue
        if State == "Text1":
            if len (Line) == 0:
                continue
            if Line[0:6] == "Backup":
                continue
            if Line[0:5] == "Note:":
                continue
            if Line == "Changelog":
                continue
            if ReleasePre + str (RevNum) + ReleaseSuf in Ignore:
                continue
            print ReleasePre + str (RevNum) + ReleaseSuf + " - " + Line
            State = "Text2"
            continue
        if State == "Text2":
            if len (Line) == 0:
                continue
            print "            " + Line
            
    File.close()
    
#Process ("v0.3.", "", "HEAD", "478")
#Process ("v0.2.", "", "477", "470")

Process ("v0.3.", "", "HEAD", "1322")
