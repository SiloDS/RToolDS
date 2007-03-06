; example2.nsi
;
; This script is based on example1.nsi, but it remember the directory, 
; has uninstall support and (optionally) installs start menu shortcuts.
;
; It will install example2.nsi into a directory that the user selects,

;--------------------------------

; The name of the installer
Name "RToolDS"

; The file to write
OutFile "RToolDS_v0.1.67.exe"

; The default installation directory
InstallDir $PROGRAMFILES\RToolDS

; Registry key to check for directory (so if you install again, it will 
; overwrite the old one automatically)
InstallDirRegKey HKLM "Software\RToolDS" "Install_Dir"

;--------------------------------

; Pages

Page components
Page directory
Page instfiles

UninstPage uninstConfirm
UninstPage instfiles

;--------------------------------

; The stuff to install
Section "RToolDS (required)"

  SectionIn RO
  
  ; Set output path to the installation directory.
  SetOutPath $INSTDIR
  
  ; Put file there
  File "library.zip"
  File "logo.png"
  File "About.png"
  File "MSVCR71.dll"
  File "RToolDS.exe"
  File "w9xpopen.exe"
  
  ; Write the installation path into the registry
  WriteRegStr HKLM SOFTWARE\RToolDS "Install_Dir" "$INSTDIR"
  
  ; Write the uninstall keys for Windows
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\RToolDS" "DisplayName" "RToolDS"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\RToolDS" "UninstallString" '"$INSTDIR\uninstall.exe"'
  WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\RToolDS" "NoModify" 1
  WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\RToolDS" "NoRepair" 1
  WriteUninstaller "uninstall.exe"
  
SectionEnd

; Optional section (can be disabled by the user)
Section "Start Menu Shortcuts"

  CreateDirectory "$SMPROGRAMS\RToolDS"
  CreateShortCut "$SMPROGRAMS\RToolDS\Uninstall.lnk" "$INSTDIR\uninstall.exe" "" "$INSTDIR\uninstall.exe" 0
  CreateShortCut "$SMPROGRAMS\RToolDS\RToolDS.lnk" "$INSTDIR\RToolDS.exe" "" "$INSTDIR\RToolDS.exe" 0
  
SectionEnd

;--------------------------------

; Uninstaller

Section "Uninstall"
  
  ; Remove registry keys
  DeleteRegKey HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\RToolDS"
  DeleteRegKey HKLM SOFTWARE\RToolDS

  ; Remove files and uninstaller
  Delete $INSTDIR\RToolDS.nsi
  Delete $INSTDIR\library.zip
  Delete $INSTDIR\logo.png
  Delete $INSTDIR\About.png
  Delete $INSTDIR\MSVCR71.dll
  Delete $INSTDIR\RToolDS.exe
  Delete $INSTDIR\w9xpopen.exe
  Delete $INSTDIR\uninstall.exe

  ; Remove shortcuts, if any
  Delete "$SMPROGRAMS\RToolDS\*.*"

  ; Remove directories used
  RMDir "$SMPROGRAMS\RToolDS"
  RMDir "$INSTDIR"

SectionEnd
