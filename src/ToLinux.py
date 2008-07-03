from cx_Freeze import setup, Executable #@PydevCodeAnalysisIgnore

setup(
        name = "RToolDS",
        version = "0.3",
        description = "RToolDS",
        executables = [Executable("RToolDS.py")]
)

#
#setup( 
#        name = "RToolDS", 
#        options = {"py2exe": {"compressed": 1, 
#                              "optimize": 2, 
#                              "bundle_files": 1}}, 
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
