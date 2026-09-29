Unicode true
!include "MUI2.nsh"
!include "LogicLib.nsh"
!include "x64.nsh"
!define PRODUCT "Black Dragon - Black Kitty Fix"
!define KEY "Software\Microsoft\Windows\CurrentVersion\Uninstall\BlackDragonBlackKittyFix"
Name "${PRODUCT} 1.0.0 (Black Dragon 5.6.3) - Installer r1"
OutFile "${OUTPUT}"
InstallDir "$PROGRAMFILES64\BlackDragonBlackKittyFix"
InstallDirRegKey HKLM "${KEY}" "InstallLocation"
RequestExecutionLevel admin
SetCompressor /SOLID lzma
SetCompressorDictSize 32
BrandingText "Black Dragon 5.6.3 / Black Kitty Fix 1.0.0 - Installer r1"
VIProductVersion "26.2.0.57700"
VIAddVersionKey /LANG=1033 "ProductName" "Black Dragon 5.6.3 - Black Kitty Fix 1.0.0"
VIAddVersionKey /LANG=1033 "FileDescription" "Black Kitty Fix 1.0.0 - Updater-enabled release 1.0.0"
VIAddVersionKey /LANG=1033 "FileVersion" "26.2.0.57700"
VIAddVersionKey /LANG=1033 "ProductVersion" "5.6.3 / Black Kitty Fix 1.0.0 / Installer r1"
VIAddVersionKey /LANG=1033 "LegalCopyright" "Original viewer and libraries: their respective authors."
Var GuardResult
Var GuardMessage
!define MUI_ABORTWARNING
!define MUI_WELCOMEPAGE_TEXT "Black Dragon 5.6.3 'Favorite Dragon' (26.2.0.57700), with Black Kitty Fix 1.0.0.$\r$\n$\r$\nUpdater-enabled release 1.0.0: the viewer is unchanged. This installs for all Windows users and requires administrator permission. Each user keeps separate settings and cache.$\r$\n$\r$\nTo move an older per-user installation to Program Files, first uninstall the old application yourself; its profile is retained. This installer never moves or removes another installation automatically."
!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_LICENSE "${PAYLOAD}\LICENSE.txt"
!define MUI_PAGE_HEADER_TEXT "Choose installation folder"
!define MUI_PAGE_HEADER_SUBTEXT "Select an empty folder or a marked Black Kitty Fix installation to update."
!define MUI_PAGE_CUSTOMFUNCTION_LEAVE ValidateDestination
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!define MUI_FINISHPAGE_TEXT "Black Kitty Fix is installed for all Windows users.$\r$\n$\r$\nStart it from the Start menu or desktop shortcut. Existing per-user settings and cache are preserved.$\r$\n$\r$\nUse Check for Updates on the login screen or in About. Downloading and installation require approval. See Black-Kitty-Fix-README.txt for details."
!insertmacro MUI_PAGE_FINISH
!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES
!insertmacro MUI_LANGUAGE "English"

!macro Guard MODE
 InitPluginsDir
 File /oname=$PLUGINSDIR\InstallerGuard.ps1 "${GUARD}"
 ; Run the built-in 64-bit Windows PowerShell for the 64-bit registry view.
 ; ExecutionPolicy applies only to this helper process; no policy is changed.
 nsExec::ExecToStack /TIMEOUT=60000 '"$WINDIR\Sysnative\WindowsPowerShell\v1.0\powershell.exe" -NoLogo -NoProfile -NonInteractive -ExecutionPolicy Bypass -File "$PLUGINSDIR\InstallerGuard.ps1" -Mode ${MODE} -Destination "$INSTDIR"'
 Pop $GuardResult
 Pop $GuardMessage
 ${If} $GuardResult != 0
  MessageBox MB_OK|MB_ICONSTOP "$GuardMessage$\r$\n$\r$\nSetup cannot safely continue." /SD IDOK
  SetErrorLevel 3
  Abort
 ${EndIf}
!macroend

Function .onInit
 SetShellVarContext all
 SetRegView 64
 ReadRegDWORD $0 HKLM "SOFTWARE\Microsoft\NET Framework Setup\NDP\v4\Full" "Release"
 ${If} $0 < 528040
  MessageBox MB_OK|MB_ICONSTOP "Black Kitty Fix requires Microsoft .NET Framework 4.8 or newer for its updater. Install it through Windows Update and retry." /SD IDOK
  SetErrorLevel 3
  Abort
 ${EndIf}
 ${IfNot} ${RunningX64}
  MessageBox MB_OK|MB_ICONSTOP "This viewer requires 64-bit Windows." /SD IDOK
  SetErrorLevel 3
  Abort
 ${EndIf}
FunctionEnd

Function ValidateDestination
 !insertmacro Guard Install
FunctionEnd

Section "Viewer"
 ; Also validate here: silent installs and /D= must not bypass the checks.
 Call ValidateDestination
 SetOverwrite on
 ClearErrors
 SetOutPath "$INSTDIR"
 !include "${INSTALL_FILES}"
 IfErrors copy_failed
 WriteUninstaller "$INSTDIR\Uninstall.exe"
 IfErrors copy_failed
 CreateDirectory "$SMPROGRAMS\${PRODUCT}"
 SetOutPath "$INSTDIR"
 CreateShortCut "$SMPROGRAMS\${PRODUCT}\${PRODUCT}.lnk" "$INSTDIR\BlackDragonViewer.exe" "" "$INSTDIR\BlackDragonViewer.exe"
 CreateShortCut "$SMPROGRAMS\${PRODUCT}\Read me.lnk" "$INSTDIR\Black-Kitty-Fix-README.txt"
 CreateShortCut "$SMPROGRAMS\${PRODUCT}\Uninstall.lnk" "$INSTDIR\Uninstall.exe"
 CreateShortCut "$DESKTOP\${PRODUCT}.lnk" "$INSTDIR\BlackDragonViewer.exe" "" "$INSTDIR\BlackDragonViewer.exe"
 WriteRegStr HKLM "${KEY}" "DisplayName" "Black Dragon 5.6.3 - Black Kitty Fix 1.0.0 (Installer r1)"
 WriteRegStr HKLM "${KEY}" "DisplayVersion" "5.6.3 / Black Kitty Fix 1.0.0"
 WriteRegStr HKLM "${KEY}" "BaseViewerVersion" "26.2.0.57700"
 WriteRegStr HKLM "${KEY}" "FixVersion" "1.0.0"
 WriteRegStr HKLM "${KEY}" "InstallerRevision" "1"
 WriteRegStr HKLM "${KEY}" "Publisher" "Black Kitty Fix (unofficial build)"
 WriteRegStr HKLM "${KEY}" "InstallLocation" "$INSTDIR"
 WriteRegStr HKLM "${KEY}" "DisplayIcon" "$INSTDIR\BlackDragonViewer.exe"
 WriteRegStr HKLM "${KEY}" "UninstallString" '$\"$INSTDIR\Uninstall.exe$\"'
 WriteRegStr HKLM "${KEY}" "QuietUninstallString" '$\"$INSTDIR\Uninstall.exe$\" /S'
 WriteRegDWORD HKLM "${KEY}" "NoModify" 1
 WriteRegDWORD HKLM "${KEY}" "NoRepair" 1
 IfErrors registration_failed
 ; Remove old per-user entries only AFTER copying and registering succeeded.
 ; The guard compares canonical paths and examines loaded user hives, so an
 ; installation in any other folder is left entirely alone.
 !insertmacro Guard CleanupLegacy
 Goto done
 copy_failed:
  MessageBox MB_OK|MB_ICONSTOP "Application files could not be written. Close the viewer and retry. No old per-user uninstall registration has been removed." /SD IDOK
  SetErrorLevel 4
  Abort
 registration_failed:
  MessageBox MB_OK|MB_ICONSTOP "The machine-wide installation could not be registered. Retry with administrator permission. Old per-user entries have been preserved." /SD IDOK
  SetErrorLevel 5
  Abort
 done:
SectionEnd

Function un.onInit
 SetShellVarContext all
 SetRegView 64
 !insertmacro Guard Uninstall
FunctionEnd

Section "Uninstall"
 ; Recheck just before removal in case the viewer started at the confirm page.
 !insertmacro Guard Uninstall
 ; Explicit package files only. No recursive deletion, no profile/cache paths.
 !include "${UNINSTALL_FILES}"
 Delete "$INSTDIR\Uninstall.exe"
 RMDir "$INSTDIR"
 ; An obsolete uninstaller in another folder cannot unregister the new copy.
 ReadRegStr $0 HKLM "${KEY}" "InstallLocation"
 ${If} $0 != ""
  GetFullPathName $0 "$0"
  GetFullPathName $1 "$INSTDIR"
  ${If} $0 == $1
   Delete "$DESKTOP\${PRODUCT}.lnk"
   Delete "$SMPROGRAMS\${PRODUCT}\${PRODUCT}.lnk"
   Delete "$SMPROGRAMS\${PRODUCT}\Read me.lnk"
   Delete "$SMPROGRAMS\${PRODUCT}\Uninstall.lnk"
   RMDir "$SMPROGRAMS\${PRODUCT}"
   DeleteRegKey HKLM "${KEY}"
  ${EndIf}
 ${EndIf}
SectionEnd
