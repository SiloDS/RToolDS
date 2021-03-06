"""
This is a setup.py script generated by py2applet

Usage:
    python setup.py py2app
"""

#@PydevCodeAnalysisIgnore

from setuptools import setup

APP = ['RToolDS.py']
DATA_FILES = ["ReadMe.txt", "License.txt", "RToolDS_Trimmed.dat.new", "ADVANsCEne_RToolDS.xml"]
OPTIONS = {'argv_emulation': True}

setup( 
    app = APP,
    data_files = DATA_FILES,
    options = {'py2app': OPTIONS},
    setup_requires = ['py2app'],
 )
