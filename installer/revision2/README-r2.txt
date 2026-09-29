BLACK DRAGON 5.6.3 "FAVORITE DRAGON" (26.2.0.57700)
BLACK KITTY FIX 0.1.0 - UNOFFICIAL PREVIEW
INSTALLER-ONLY REVISION 2

The viewer executable, libraries, rendering, AMD patch, posing, photography and
motion-blur features are unchanged from Black Kitty Fix 0.1.0. Only the installer
and installation documentation/metadata have changed. No viewer recompilation.

INSTALLATION
64-bit Windows. Run Setup-r2.exe and approve the administrator request. Setup
installs for all Windows users. The default folder is:
  C:\Program Files\BlackDragonBlackKittyFix
(The system's 64-bit Program Files location is used if Windows is on another drive.)
The "Choose installation folder" page lets you choose another local folder.
Choose an empty folder, or an existing Black Kitty Fix folder with its valid
black-kitty-fix-install.txt marker. Do not select official Black Dragon, Firestorm,
or another application's directory. Mixed installations and redirected folders
(junctions/symbolic links) are refused. Close Black Kitty Fix in all Windows
sessions before installation, update or uninstall.

Setup adds shared Start menu and desktop shortcuts, and a machine-wide entry in
Installed Apps. Start the viewer normally from its shortcut, not as administrator.
Visual Studio, Python and NSIS are not required to use the viewer; runtime DLLs
are bundled. Setup uses built-in Windows PowerShell to validate the destination
and running processes. If that helper is blocked by a machine policy, Setup stops.

VERSIONS AND UPDATES
Base viewer: 26.2.0.57700 / Black Dragon 5.6.3 "Favorite Dragon".
Separate fix release: Black Kitty Fix 0.1.0.
Separate installer revision: r2.
This is an unsigned installer. There is no automatic updater; updates are manual.
Select the existing marked installation folder to update it. A machine-wide copy
registered in another folder must be uninstalled manually before switching folders.

OLDER PER-USER INSTALLATIONS
The original installer used:
  %LOCALAPPDATA%\Programs\BlackDragonBlackKittyFix
To upgrade IN PLACE, choose that existing folder. After successful installation,
Setup removes old per-user uninstall entries that point to that exact folder,
including matching entries in other currently loaded Windows user profiles.
It leaves entries for installations in any other folder untouched. Existing
personal shortcuts may remain; they still point to the same viewer. If another
user's registry profile is not loaded, sign in as that user to handle their old
entry; Setup does not load or modify offline registry profiles.

For a shared installation, Program Files is recommended. A folder under one
user's LocalAppData can retain access permissions that exclude other users.
Setup does not change those permissions or make private folders public.

To MIGRATE TO PROGRAM FILES:
1. Close Black Kitty Fix in every Windows session.
2. In your original Windows account, uninstall the older per-user application
   using its own uninstaller. It retains your settings and cache.
3. Run Setup-r2.exe and select the default Program Files folder.
4. Start normally in your original account; its separate Black Kitty Fix profile
   remains available. Other Windows users get their own profiles on first launch.
Setup never automatically moves or deletes an installation in another folder.
If you keep both copies, their uninstall entries are intentionally both retained.

PERSONAL DATA
Per-user settings: %APPDATA%\BlackDragonBlackKittyFix
Per-user cache:    %LOCALAPPDATA%\Black Dragon Black Kitty Fix
Updates and uninstall preserve both. Uninstall deletes only enumerated package
files; unrelated files added to the application folder are retained. No personal
settings, accounts, passwords, credentials, logs, caches or chat history are
included in this package. It contains only clean application files and defaults.
The official Black Dragon installation and its settings remain separate.

FIXES AND LIMITATIONS
Experimental AMD mesh/shadow flicker adaptation from Firestorm commit
0c132c2eb3d15afc56d7fe42589dc8f2eb778197. OpenJPEG 2.5.4 supports progressive
texture downloads. Camera presets and missing SMAA entry points are included.
The user reported the mesh fix appeared to work on RX 7900 XTX, and confirmed
textures and camera/UI controls work. This is not a universal visual-fix claim.
This build uses OpenAL and OpenJPEG, and omits Havok, FMOD, Kakadu, Discord,
NVAPI and Tracy. Audio and Havok-dependent functions can differ from official BD.

SOURCE AND CREDITS
Black Dragon by NiranV and contributors, based on the Second Life viewer.
https://github.com/NiranV/Black-Dragon-Viewer
Base commit: b2ca434b39bcd93aff0e23414999dddd73527e05
OpenJPEG: https://github.com/uclouvain/openjpeg (v2.5.4).
Licenses: LICENSE.txt, licenses.txt and ThirdPartyLicenses.
Share the matching Source-r2.zip alongside Setup-r2.exe. It retains the exact
viewer/OpenJPEG sources and adds the revised installer scripts. The original
installer scripts are retained as historical references in that source archive.
SHA256SUMS.txt identifies these revision-2 artifacts. See VALIDATION.md for checks
actually performed and remaining installation tests.
