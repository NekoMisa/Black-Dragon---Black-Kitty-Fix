Unicode true
!include "MUI2.nsh"
!include "LogicLib.nsh"
!include "x64.nsh"

!define PRODUCT "Black Dragon - Black Kitty Fix"
!define KEY "Software\Microsoft\Windows\CurrentVersion\Uninstall\BlackDragonBlackKittyFix"
Name "${PRODUCT} 0.1.0 (Black Dragon 5.6.3)"
OutFile "${OUTPUT}"
InstallDir "$LOCALAPPDATA\Programs\BlackDragonBlackKittyFix"
RequestExecutionLevel user
SetCompressor /SOLID lzma
SetCompressorDictSize 32
BrandingText "Unofficial preview - Black Dragon 5.6.3 / Black Kitty Fix 0.1.0"
VIProductVersion "26.2.0.57700"
VIAddVersionKey /LANG=1033 "ProductName" "Black Dragon 5.6.3 - Black Kitty Fix 0.1.0"
VIAddVersionKey /LANG=1033 "FileDescription" "Black Kitty Fix 0.1.0 - Unofficial Preview Setup"
VIAddVersionKey /LANG=1033 "FileVersion" "26.2.0.57700"
VIAddVersionKey /LANG=1033 "ProductVersion" "5.6.3 / Black Kitty Fix 0.1.0"
VIAddVersionKey /LANG=1033 "LegalCopyright" "Original viewer and libraries: their respective authors."
!define MUI_ABORTWARNING
!define MUI_WELCOMEPAGE_TEXT "Install the unofficial Black Kitty Fix 0.1.0 preview, based on Black Dragon 5.6.3 'Favorite Dragon' (26.2.0.57700).$\r$\n$\r$\nThis installs for your Windows account with separate settings and cache. Your official Black Dragon installation stays separate.$\r$\n$\r$\nUpdates are manual. This installer is unsigned."
!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_LICENSE "${PAYLOAD}\LICENSE.txt"
!insertmacro MUI_PAGE_INSTFILES
!define MUI_FINISHPAGE_TEXT "Black Kitty Fix is installed.$\r$\n$\r$\nUse its Start menu shortcut to launch. This preview uses a new profile; log in manually and configure your preferences.$\r$\n$\r$\nSee Black-Kitty-Fix-README.txt in the installation folder."
!insertmacro MUI_PAGE_FINISH
!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES
!insertmacro MUI_LANGUAGE "English"

Function .onInit
 SetShellVarContext current
 SetRegView 64
 ${IfNot} ${RunningX64}
  MessageBox MB_OK|MB_ICONSTOP "This viewer requires 64-bit Windows."
  Abort
 ${EndIf}
FunctionEnd

Function CheckViewerClosed
 FindWindow $0 "Black Dragon Black Kitty Fix"
 ${If} $0 != 0
  MessageBox MB_OK|MB_ICONSTOP "Close Black Kitty Fix before installing or updating it." /SD IDOK
  SetErrorLevel 2
  Abort
 ${EndIf}
FunctionEnd

Section "Viewer"
 Call CheckViewerClosed
 ; Refuse to mix this package with an unrelated nonempty directory.
 IfFileExists "$INSTDIR\*.*" 0 directory_ok
 IfFileExists "$INSTDIR\black-kitty-fix-install.txt" directory_ok
 MessageBox MB_OK|MB_ICONSTOP "The destination is not an existing Black Kitty Fix installation. Choose an empty destination." /SD IDOK
 SetErrorLevel 3
 Abort
 directory_ok:
 SetOutPath "$INSTDIR"
 !include "${INSTALL_FILES}"
 WriteUninstaller "$INSTDIR\Uninstall.exe"
 CreateDirectory "$SMPROGRAMS\${PRODUCT}"
 CreateShortCut "$SMPROGRAMS\${PRODUCT}\${PRODUCT}.lnk" "$INSTDIR\BlackDragonViewer.exe" "" "$INSTDIR\BlackDragonViewer.exe"
 CreateShortCut "$SMPROGRAMS\${PRODUCT}\Read me.lnk" "$INSTDIR\Black-Kitty-Fix-README.txt"
 CreateShortCut "$SMPROGRAMS\${PRODUCT}\Uninstall.lnk" "$INSTDIR\Uninstall.exe"
 CreateShortCut "$DESKTOP\${PRODUCT}.lnk" "$INSTDIR\BlackDragonViewer.exe" "" "$INSTDIR\BlackDragonViewer.exe"
 WriteRegStr HKCU "${KEY}" "DisplayName" "Black Dragon 5.6.3 - Black Kitty Fix 0.1.0 (Preview)"
 WriteRegStr HKCU "${KEY}" "DisplayVersion" "5.6.3 / Black Kitty Fix 0.1.0"
 WriteRegStr HKCU "${KEY}" "BaseViewerVersion" "26.2.0.57700"
 WriteRegStr HKCU "${KEY}" "FixVersion" "0.1.0"
 WriteRegStr HKCU "${KEY}" "Publisher" "Black Kitty Fix (unofficial build)"
 WriteRegStr HKCU "${KEY}" "InstallLocation" "$INSTDIR"
 WriteRegStr HKCU "${KEY}" "DisplayIcon" "$INSTDIR\BlackDragonViewer.exe"
 WriteRegStr HKCU "${KEY}" "UninstallString" '$\"$INSTDIR\Uninstall.exe$\"'
 WriteRegStr HKCU "${KEY}" "QuietUninstallString" '$\"$INSTDIR\Uninstall.exe$\" /S'
 WriteRegDWORD HKCU "${KEY}" "NoModify" 1
 WriteRegDWORD HKCU "${KEY}" "NoRepair" 1
SectionEnd

Function un.onInit
 SetShellVarContext current
 SetRegView 64
 FindWindow $0 "Black Dragon Black Kitty Fix"
 ${If} $0 != 0
  MessageBox MB_OK|MB_ICONSTOP "Close Black Kitty Fix before uninstalling it." /SD IDOK
  SetErrorLevel 2
  Abort
 ${EndIf}
 IfFileExists "$INSTDIR\black-kitty-fix-install.txt" valid
 MessageBox MB_OK|MB_ICONSTOP "Black Kitty Fix installation marker is missing. No files will be removed." /SD IDOK
 Abort
 valid:
FunctionEnd

Section "Uninstall"
 ; Explicit package files only. Never recursively remove user-created files,
 ; profiles, caches or an official viewer installation.
 !include "${UNINSTALL_FILES}"
 Delete "$INSTDIR\Uninstall.exe"
 RMDir "$INSTDIR"
 Delete "$DESKTOP\${PRODUCT}.lnk"
 Delete "$SMPROGRAMS\${PRODUCT}\${PRODUCT}.lnk"
 Delete "$SMPROGRAMS\${PRODUCT}\Read me.lnk"
 Delete "$SMPROGRAMS\${PRODUCT}\Uninstall.lnk"
 RMDir "$SMPROGRAMS\${PRODUCT}"
 DeleteRegKey HKCU "${KEY}"
SectionEnd
