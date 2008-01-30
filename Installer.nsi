; Script generated by the HM NIS Edit Script Wizard.

; HM NIS Edit Wizard helper defines
!define PRODUCT_NAME "RToolDS"
!define PRODUCT_VERSION "v0.2.1179"
!define PRODUCT_PUBLISHER "Silo - Ex Blackbag"
!define PRODUCT_WEB_SITE "http://silods.moddz.com"
!define PRODUCT_DIR_REGKEY "Software\Microsoft\Windows\CurrentVersion\App Paths\RToolDS.exe"
!define PRODUCT_UNINST_KEY "Software\Microsoft\Windows\CurrentVersion\Uninstall\${PRODUCT_NAME}"
!define PRODUCT_UNINST_ROOT_KEY "HKLM"

SetCompressor lzma

; GetWindowsVersion
 ;
 ; Based on Yazno's function, http://yazno.tripod.com/powerpimpit/
 ; Updated by Joost Verburg
 ;
 ; Returns on top of stack
 ;
 ; Windows Version (95, 98, ME, NT x.x, 2000, XP, 2003, Vista)
 ; or
 ; '' (Unknown Windows Version)
 ;
 ; Usage:
 ;   Call GetWindowsVersion
 ;   Pop $R0
 ;   ; at this point $R0 is "NT 4.0" or whatnot
 
 Function GetWindowsVersion
 
   Push $R0
   Push $R1
 
   ClearErrors
 
   ReadRegStr $R0 HKLM \
   "SOFTWARE\Microsoft\Windows NT\CurrentVersion" CurrentVersion

   IfErrors 0 lbl_winnt
   
   ; we are not NT
   ReadRegStr $R0 HKLM \
   "SOFTWARE\Microsoft\Windows\CurrentVersion" VersionNumber
 
   StrCpy $R1 $R0 1
   StrCmp $R1 '4' 0 lbl_error
 
   StrCpy $R1 $R0 3
 
   StrCmp $R1 '4.0' lbl_win32_95
   StrCmp $R1 '4.9' lbl_win32_ME lbl_win32_98
 
   lbl_win32_95:
     StrCpy $R0 '95'
   Goto lbl_done
 
   lbl_win32_98:
     StrCpy $R0 '98'
   Goto lbl_done
 
   lbl_win32_ME:
     StrCpy $R0 'ME'
   Goto lbl_done
 
   lbl_winnt:
 
   StrCpy $R1 $R0 1
 
   StrCmp $R1 '3' lbl_winnt_x
   StrCmp $R1 '4' lbl_winnt_x
 
   StrCpy $R1 $R0 3
 
   StrCmp $R1 '5.0' lbl_winnt_2000
   StrCmp $R1 '5.1' lbl_winnt_XP
   StrCmp $R1 '5.2' lbl_winnt_2003
   StrCmp $R1 '6.0' lbl_winnt_vista lbl_error
 
   lbl_winnt_x:
     StrCpy $R0 "NT $R0" 6
   Goto lbl_done
 
   lbl_winnt_2000:
     Strcpy $R0 '2000'
   Goto lbl_done
 
   lbl_winnt_XP:
     Strcpy $R0 'XP'
   Goto lbl_done
 
   lbl_winnt_2003:
     Strcpy $R0 '2003'
   Goto lbl_done
 
   lbl_winnt_vista:
     Strcpy $R0 'Vista'
   Goto lbl_done
 
   lbl_error:
     Strcpy $R0 ''
   lbl_done:
 
   Pop $R1
   Exch $R0
 
 FunctionEnd


; MUI 1.67 compatible ------
!include "MUI.nsh"

; MUI Settings
!define MUI_ABORTWARNING
!define MUI_ICON "${NSISDIR}\Contrib\Graphics\Icons\modern-install.ico"
!define MUI_UNICON "${NSISDIR}\Contrib\Graphics\Icons\modern-uninstall.ico"

; Welcome page
!insertmacro MUI_PAGE_WELCOME
; License page
!insertmacro MUI_PAGE_LICENSE "License.txt"
; Directory page
!insertmacro MUI_PAGE_DIRECTORY
; Instfiles page
!insertmacro MUI_PAGE_INSTFILES
; Finish page
!define MUI_FINISHPAGE_RUN "$INSTDIR\RToolDS.exe"
!define MUI_FINISHPAGE_SHOWREADME "$INSTDIR\ReadMe.txt"
!insertmacro MUI_PAGE_FINISH

; Uninstaller pages
!insertmacro MUI_UNPAGE_INSTFILES

; Language files
!insertmacro MUI_LANGUAGE "English"

; Reserve files
!insertmacro MUI_RESERVEFILE_INSTALLOPTIONS

; MUI end ------

Name "${PRODUCT_NAME} ${PRODUCT_VERSION}"
OutFile "${PRODUCT_NAME}_${PRODUCT_VERSION}.exe"
InstallDir "$PROGRAMFILES\RToolDS"
InstallDirRegKey HKLM "${PRODUCT_DIR_REGKEY}" ""
ShowInstDetails show
ShowUnInstDetails show

Section "MainSection" SEC01
  SetOutPath "$INSTDIR"
  SetOverwrite on
  File "RToolDS.exe"
  CreateDirectory "$SMPROGRAMS\RToolDS"
  CreateShortCut "$SMPROGRAMS\RToolDS\RToolDS.lnk" "$INSTDIR\RToolDS.exe"
  File "ReadMe.txt"
  File "library.zip"
  File "msvcp71.dll"
  File "MSVCR71.dll"
  File "w9xpopen.exe"
  File "gdiplus.dll"
  File "unrar.dll"
  File "Help.htb"

Call GetWindowsVersion
Pop $R0

${If} $R0 == "Vista"
  Goto vista
${Else}
  Goto not_vista
${EndIf}


vista:
  CreateDirectory "$APPDATA\RToolDS"
  SetOutPath "$APPDATA\RToolDS"
  File "RToolDS_Trimmed.dat.new"
  Goto go_end

not_vista:
  CreateDirectory "$APPDATA\RToolDS"
  SetOutPath "$APPDATA\RToolDS"
  File "RToolDS_Trimmed.dat.new"

go_end:

SectionEnd

Section -AdditionalIcons
  WriteIniStr "$INSTDIR\${PRODUCT_NAME}.url" "InternetShortcut" "URL" "${PRODUCT_WEB_SITE}"
  CreateShortCut "$SMPROGRAMS\RToolDS\Website.lnk" "$INSTDIR\${PRODUCT_NAME}.url"
  CreateShortCut "$SMPROGRAMS\RToolDS\Uninstall.lnk" "$INSTDIR\uninst.exe"
SectionEnd

Section -Post
  WriteUninstaller "$INSTDIR\uninst.exe"
  WriteRegStr HKLM "${PRODUCT_DIR_REGKEY}" "" "$INSTDIR\RToolDS.exe"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "DisplayName" "$(^Name)"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "UninstallString" "$INSTDIR\uninst.exe"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "DisplayIcon" "$INSTDIR\RToolDS.exe"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "DisplayVersion" "${PRODUCT_VERSION}"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "URLInfoAbout" "${PRODUCT_WEB_SITE}"
  WriteRegStr ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}" "Publisher" "${PRODUCT_PUBLISHER}"
SectionEnd


Function un.onUninstSuccess
  HideWindow
  MessageBox MB_ICONINFORMATION|MB_OK "RToolDS was successfully removed from your computer."
FunctionEnd

Function un.onInit
  MessageBox MB_ICONQUESTION|MB_YESNO|MB_DEFBUTTON2 "Are you sure you want to completely remove RToolDS and all of its components?" IDYES +2
  Abort
FunctionEnd

Section Uninstall
  MessageBox MB_ICONQUESTION|MB_YESNO|MB_DEFBUTTON2 "Remove Downloaded Screenshots and Case Graphics?" IDYES next1 IDNO next2
next1:
  RMdir /r "$APPDATA\RToolDS\cache\img"
  RMdir /r "$APPDATA\RToolDS\cache\nfo"
next2:
  MessageBox MB_ICONQUESTION|MB_YESNO|MB_DEFBUTTON2 "Remove Backed Up Save Games?" IDYES next3 IDNO next4
next3:
  RMdir /r "$APPDATA\RToolDS\cache\saves"
next4:
  RMdir "$APPDATA\RToolDS\cache"
  Delete "$INSTDIR\${PRODUCT_NAME}.url"
  Delete "$INSTDIR\uninst.exe"
  Delete "$INSTDIR\ReadMe.txt"
  Delete "$INSTDIR\RToolDS.exe"
  Delete "$INSTDIR\library.zip"
  Delete "$INSTDIR\msvcp71.dll"
  Delete "$INSTDIR\MSVCR71.dll"
  Delete "$INSTDIR\w9xpopen.exe"
  Delete "$INSTDIR\gdiplus.dll"
  Delete "$INSTDIR\unrar.dll"
  Delete "$APPDATA\RToolDS\RToolDS.cfg"
  Delete "$APPDATA\RToolDS\ADVANsCEne_RToolDS.xml"
  Delete "$APPDATA\RToolDS\RToolDS_Master_List.dat"
  Delete "$APPDATA\RToolDS\RToolDS_Tags.dat"
  Delete "$APPDATA\RToolDS\RToolDS_Trimmed.dat"
  Delete "$APPDATA\RToolDS\RToolDS_Unknown.dat"
  Delete "$APPDATA\RToolDS\RToolDS_Trimmed.dat.new"
  Delete "$INSTDIR\Help.htb"
  RMDir "$APPDATA\RToolDS"
 
  Delete "$SMPROGRAMS\RToolDS\Uninstall.lnk"
  Delete "$SMPROGRAMS\RToolDS\Website.lnk"
  Delete "$SMPROGRAMS\RToolDS\RToolDS.lnk"

  RMDir "$SMPROGRAMS\RToolDS"
  RMDir "$INSTDIR"

  DeleteRegKey ${PRODUCT_UNINST_ROOT_KEY} "${PRODUCT_UNINST_KEY}"
  DeleteRegKey HKLM "${PRODUCT_DIR_REGKEY}"
  SetAutoClose true
SectionEnd