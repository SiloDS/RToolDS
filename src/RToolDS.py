from app import MyApp
import MyConfig
import os

import sys

ConfigFileName = os.path.join ( os.path.realpath( os.path.dirname( sys.argv[0] ) ), "RToolDS.cfg" )
MyConfig.Load ( ConfigFileName )
app = MyApp( 0 )
app.MainLoop()
MyConfig.Save ( ConfigFileName )