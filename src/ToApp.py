from setuptools import setup #@PydevCodeAnalysisIgnore

setup( 
        app = ["RToolDS.py"],
        setup_requires = ["py2app"],
        options = dict( 
                py2app = dict( 
                    argv_emulation = 1,
#                    packages='wx',
                    iconfile = '/Users/rich/Documents/workspace/RToolDS/gfx/GFX_Icon.icns',
#                    site_packages=True,
                    plist = dict( 
                            CFBundleName = "RToolDS",
                            CFBundleShortVersionString = "0.2.5", # must be in X.X.X format
                            CFBundleGetInfoString = "RToolDS 0.2.5",
                            CFBundleExecutable = "RToolDS",
                            CFBundleIdentifier = "com.example.RToolDS",
                ),
 ) ),
 )
#        windows = [
#        {
#            "script": "RToolDS.py", 
#            "icon_resources": [( 1, os.path.join ("..","gfx","GFX_Icon.ico") )], 
#            "other_resources": [( 24, 1, manifest )]
#        }
#    ], 
#        data_files=[( ".", 
#                   ["ReadMe.txt", "License.txt", "unrar.dll", "RToolDS_Trimmed.dat.new", "ADVANsCEne_RToolDS.xml"] )]
# )

