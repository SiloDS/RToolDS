@Echo Off

set SRC="C:\Documents and Settings\Rich\workspace\RToolDS"
set WX="C:\Python26\Lib\site-packages\wx-2.8-msw-unicode\wx"
set NSIS="C:\Program Files\NSIS\makensis.exe"

cd %SRC%\src
c:\python26\python ToExe.py py2exe

cd %SRC%\src\dist
del POWRPROF.dll
rem rename RToolDS.exe RToolDS6.exe

copy %SRC%\Installer.nsi %SRC%\src\dist
rem copy %WX%\msvcp71.dll %SRC%\src\dist
rem copy %WX%\msvcp90.dll %SRC%\src\dist
copy "..\..\..\Python DLLs\*" .
copy %WX%\gdiplus.dll %SRC%\src\dist

cd %SRC%\Help
zip %SRC%\src\dist\Help.zip *
copy %SRC%\Help\Help.htb %SRC%\src\dist

cd %SRC%\src\dist

rem rename Help.zip Help.htb

rem rename Trimmed.dat Trimmed.dat.new

rem upx --best *.*

%NSIS% Installer.nsi

move RToolDS_*.exe %SRC%

cd %SRC%/src
rd dist /s /q
rd build /s /q

cd %SRC%
