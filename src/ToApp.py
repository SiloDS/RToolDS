from setuptools import setup

setup( 
        app = ["RToolDS.py"], 
	setup_requires = ["py2app"],
        options = dict(py2app=dict(argv_emulation=1,)),
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
