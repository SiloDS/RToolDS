from distutils.core import setup
import py2exe

setup( 
        name="RToolDS", 
        options = {"py2exe": {"compressed": 0, 
                              "optimize": 2, 
                              "bundle_files": 1}}, 
        windows = [
        {
            "script": "RToolDS.py", 
            "icon_resources": [( 1, "icon.ico" )]
        }
    ], 
        data_files=[( ".", 
                   ["logo.png", "About.png", ] ), ]
        
 )
#working

#setup(
#        name="RToolDS",
#        options = {"py2exe": {"compressed": 0,
#                              "optimize": 2,
#                              "bundle_files": 1}},
#        windows=["RToolDS.py",],
#        data_files=[(".",
#                   ["logo.png","about.png"],), ]
#        
#)
#setup(name="wxTail",scripts=["wxTail.py"],)

#setup(name="RToolDS",
#      description="RToolDS",
#      version='0.0.1',
#      scripts=['app.py', ],
#      data_files=[(".",
#                   ["logo2.bmp",]), ]
#      )