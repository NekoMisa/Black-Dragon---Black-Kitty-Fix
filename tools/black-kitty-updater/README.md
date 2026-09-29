# Black Kitty Fix Windows updater

Bundled `BlackKittyUpdater.exe` starts from the viewer and Check for Updates on the login screen or in About.
Uses .NET Framework4.8 without credentials. Only installation requests elevation.
Optional startup checks stay quiet when no newer release is available.
Downloads/installations require approval; normal viewer shutdown waits up to90s.
Installation is postponed if shutdown is cancelled. Installer checks all sessions.

## Release contract

- Repository: NekoMisa/Black-Dragon---Black-Kitty-Fix.
- Stable tag: `vMAJOR.MINOR.PATCH` (Black Kitty Fix version, not official BD version).
- Asset: `Black-Kitty-Fix-MAJOR.MINOR.PATCH-Windows-x64-Setup.exe`.
- Exactly one uploaded asset with GitHub SHA-256 digest and size, max2GiB.
- Exact repository/tag/asset HTTPS URL; only GitHub release-asset hosts for redirects.
- Reject drafts/prereleases, missing digest, wrong size/hash or unexpected URLs.
- Download integrity is not publisher signing; installer remains unsigned.
- Separate settings/preference/download/mutex identities from Stellarys.

Compile Updater.cs with Framework64 csc.exe, `/target:winexe`, references
System.Windows.Forms, System.Drawing, System.Net.Http and System.Web.Extensions.
Use `/target:exe /main:UpdaterTests` with both sources for core validation checks.
See installer package_release.py for packaging. Update all Black Kitty Fix version
labels together for a new release; preserve the official Black Dragon base version.
