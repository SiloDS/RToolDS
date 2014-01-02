import os
import sys
from cx_Freeze import setup, Executable

build_exe_options = {"packages": ["os"], "excludes": ["tkinter"]}

base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup( name = "RToolDS",
        version = "0.1.1",
        description = "RToolDS ROM Manager",
        options = {"build_exe": build_exe_options},
        executables = [Executable( "RToolDS.py", base = base, icon = os.path.join ( "..", "gfx", "GFX_Icon.ico" ) )],
        data_files = [( '.', ["ReadMe.txt", "License.txt", "unrar.dll", "RToolDS_Trimmed.dat.new", "ADVANsCEne_RToolDS.xml"] )]
 )
