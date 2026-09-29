# Source provenance

Official base: Black Dragon 26.2.0.57700, release 5.6.3 “Favorite Dragon”,
commit b2ca434b39bcd93aff0e23414999dddd73527e05 from
https://github.com/NiranV/Black-Dragon-Viewer.

The `viewer/` tree contains the exact patched source from Black Kitty Fix 0.1.0,
plus the 1.0.0 updater launch/menu integration and version labels. AMD rendering,
posing, photography, motion blur and OpenJPEG texture changes are retained.
The adaptation references Firestorm commit
0c132c2eb3d15afc56d7fe42589dc8f2eb778197. `openjpeg/` contains OpenJPEG 2.5.4.
The Windows updater is adapted from the LGPL-2.1 Stellarys helper.

The original clean source archive is retained locally and comparisons identify
all changed viewer files. Historical build/installer notes live under `build/`
and `installer/`; the current updater/installer sources live under `tools/`.
No personal profile, saved accounts, private keys, cache or logs are included.
External dependencies retain their own licences; this configuration uses
OpenAL/OpenJPEG and does not include Havok, FMOD, Kakadu, Discord, NVAPI or Tracy.
