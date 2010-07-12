from distutils.core import setup
import py2exe #@UnusedImport #@UnresolvedImport
import os

setup( 
        name = "RToolDS",
        options = {"py2exe": {"compressed": 2,
                              "optimize": 2,
                              "bundle_files": 3}},
        windows = [
        {
            "script": "RToolDS.py",
            "icon_resources": [( 1, os.path.join ( "..", "gfx", "GFX_Icon.ico" ) )]
        }
    ],
        data_files = [( ".",
                   ["ReadMe.txt", "License.txt", "unrar.dll", "RToolDS_Trimmed.dat.new", "ADVANsCEne_RToolDS.xml"] )]
 )
