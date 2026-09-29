BLACK DRAGON 5.6.3 "FAVORITE DRAGON"
BLACK KITTY FIX 0.1.0 - UNOFFICIAL PREVIEW
Base viewer version: 26.2.0.57700

An unofficial experimental build of Black Dragon with an AMD rendering fix.
This is not an official Black Dragon release and is not endorsed by its authors.

CHANGES
- Experimental adaptation of Firestorm commit
  0c132c2eb3d15afc56d7fe42589dc8f2eb778197 for mesh/shadow flickering.
- OpenJPEG 2.5.4 with partial JPEG2000 decoding, correcting missing textures.
- Bundled camera presets and missing SMAA shader entry points.
- Separate application profile, cache, installer and shortcuts.
Black Dragon's posing, photography and motion-blur code is retained.

INSTALL AND USE
64-bit Windows. Install for your current Windows account. Launch using
"Black Dragon - Black Kitty Fix" in the Start menu or on the desktop.
No Visual Studio, Python or build tools are required to run the installed viewer.
Required Visual C++ runtime DLLs are bundled alongside the application.
No personal settings, passwords, logs or cache files are distributed.

The installation uses LocalAppData\Programs\BlackDragonBlackKittyFix.
Settings: AppData\Roaming\BlackDragonBlackKittyFix.
Cache: AppData\Local\Black Dragon Black Kitty Fix.
The official viewer is separate. Do not copy its settings.xml wholesale: it can
contain absolute cache and account paths. Configure this preview independently.
Uninstall removes packaged application files and shortcuts; settings and cache
are retained. There is no automatic updater. Install newer versions manually
after closing the viewer. The installer is unsigned.

TEST STATUS AND LIMITATIONS
The original test build compiled on Windows using MSVC v143. The user reported
the flicker fix appeared to work on an AMD RX 7900 XTX and confirmed that textures
display after the decoder repair. This does not establish a fix for every mesh,
material, graphics configuration or GPU. Test important photography workflows.
The build uses OpenAL/OpenJPEG and omits proprietary Havok, FMOD and Kakadu,
plus Discord, NVAPI and Tracy. Audio and Havok-dependent features can differ.

SOURCE AND CREDITS
Black Dragon by NiranV and contributors, based on the Second Life viewer.
https://github.com/NiranV/Black-Dragon-Viewer
Base commit: b2ca434b39bcd93aff0e23414999dddd73527e05
Rendering adaptation from FirestormViewer/phoenix-firestorm, commit above.
OpenJPEG: https://github.com/uclouvain/openjpeg (v2.5.4).
Modern JPEG2000 adapter based on the official Second Life viewer integration.
Original copyright notices and licenses are retained in LICENSE.txt, licenses.txt
and ThirdPartyLicenses. Matching modified viewer source, OpenJPEG source and
build/installer scripts are supplied in the companion Source.zip. Share that
source archive alongside this installer when distributing this preview.

See the accompanying RELEASE-NOTES.md for installer validation results.
