from distutils.core import setup
import py2exe #@UnusedImport #@UnresolvedImport
import os

manifest = """
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<assembly xmlns="urn:schemas-microsoft-com:asm.v1"
manifestVersion="1.0">
<assemblyIdentity
    version="0.64.1.0"
    processorArchitecture="x86"
    name="Controls"
    type="win32"
/>
<description>RToolDS</description>
<dependency>
    <dependentAssembly>
        <assemblyIdentity
            type="win32"
            name="Microsoft.Windows.Common-Controls"
            version="6.0.0.0"
            processorArchitecture="X86"
            publicKeyToken="6595b64144ccf1df"
            language="*"
        />
    </dependentAssembly>
</dependency>
</assembly>
"""

setup( 
        name = "RToolDS",
        options = {"py2exe": {"compressed": 1,
                              "optimize": 2,
                              "bundle_files": 1}},
        windows = [
        {
            "script": "RToolDS.py",
            "icon_resources": [( 1, os.path.join ( "..", "gfx", "GFX_Icon.ico" ) )],
            "other_resources": [( 24, 1, manifest )]
        }
    ],
        data_files = [( ".",
                   ["ReadMe.txt", "License.txt", "unrar.dll", "RToolDS_Trimmed.dat.new", "ADVANsCEne_RToolDS.xml"] )]
 )