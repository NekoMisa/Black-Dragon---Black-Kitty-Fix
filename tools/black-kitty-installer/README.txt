BLACK DRAGON — BLACK KITTY FIX 1.0.0
Based on Black Dragon26.2.0.57700 /5.6.3 “Favorite Dragon”.

This independent hobby build adds the AMD mesh/shadow flicker fix while keeping
Black Dragon's posing, photography and motion blur. Updates may follow official
Black Dragon releases and maintain the AMD fix until it is included upstream.

INSTALLATION
Windows x64. Default C:\Program Files\BlackDragonBlackKittyFix.
Administrator approval and .NET Framework4.8 or newer are required.
Setup is unsigned; Windows may identify its publisher as unknown.
Install in an empty folder or an existing marked Black Kitty Fix folder.
Official Black Dragon/Firestorm, unrelated nonempty folders and redirected folders
are refused. Close Black Kitty Fix and its updater in all Windows sessions first.
Existing installations in another folder are never moved or deleted automatically.
To relocate, uninstall the old application first (its settings/cache are retained),
then install in the new folder. Updating in place removes only matching legacy
per-user uninstall entries after the all-users installation succeeds.

UPDATES
The viewer checks on startup unless disabled in the updater. Use Check for Updates
on the login screen or in About for a manual check. Releases come only from:
https://github.com/NekoMisa/Black-Dragon---Black-Kitty-Fix
Downloads and installation require your approval. The downloaded installer's
SHA-256 and size are checked against GitHub metadata. This verifies file integrity,
not a publisher signature. The updater asks the viewer to close normally and
waits for shutdown prompts; it never force-kills it or bypasses UAC.
If shutdown is cancelled, installation is postponed. Updates retain settings/cache.
Users of0.1.0 must install1.0.0 manually once to receive the updater.

PERSONAL DATA
Separate settings: %APPDATA%\BlackDragonBlackKittyFix
Separate cache: %LOCALAPPDATA%\Black Dragon Black Kitty Fix
Updater downloads: %LOCALAPPDATA%\BlackDragonBlackKittyFix\updates
Updates and uninstall preserve these folders. Only enumerated application files
are removed by uninstall; unrelated files added to the install folder are retained.
No personal settings, saved accounts, credentials, logs or cache are packaged.
Official Black Dragon and Stellarys profiles remain separate.

MY VIEWER PROJECTS
Black Dragon - Black Kitty Fix preserves Black Dragon's features with the AMD
flicker fix and built-in update checks:
https://github.com/NekoMisa/Black-Dragon---Black-Kitty-Fix
Stellarys Viewer is a Firestorm-based hobby viewer with the AMD flicker fix,
permission-based posing of other avatars and built-in update checks:
https://github.com/NekoMisa/stellarys-viewer
Each project has separate settings, cache and updates.

CREDITS AND SOURCE
Black Dragon by NiranV and contributors, based on Linden Lab's viewer.
AMD adaptation references Firestorm commit0c132c2eb3d15afc56d7fe42589dc8f2eb778197.
Updater adapted from Stellarys. Credits and component licence notices retained.
This configuration uses OpenAL/OpenJPEG and does not include Havok, FMOD, Kakadu,
Discord, NVAPI or Tracy. Some functions can differ from official Black Dragon.
Download matching source/checksums from the same release. See VALIDATION.md for
checks actually performed and any remaining tests.
