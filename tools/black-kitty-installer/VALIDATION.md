# Black Kitty Fix 1.0.0 validation

Base: Black Dragon26.2.0.57700 /5.6.3 “Favorite Dragon”. Fix version:1.0.0.

## Checks performed

- Windows v143 Release build completed successfully using the restored incremental
  build cache. Viewer binary/version metadata retains official26.2.0.57700.
- Compared all released viewer source against0.1.0: exactly eleven files changed,
  limited to updater launch/menu/notification integration and version labels.
  AMD shaders/rendering, poser, photography, motion blur, OpenJPEG and separate
  settings/cache source are unchanged.
-23 updater core checks passed: stable-release metadata, versions, SHA-256/size,
  trusted URLs, readable notes and distinguishing Black Kitty Fix from official
  Black Dragon despite possible shared executable names.
-27 installer guard fixture tests passed without modifying installed viewers.
- Isolated viewer reached the login screen as Black Kitty Fix1.0.0. Its log
  confirms BlackKittyUpdater.exe --startup launched. The agent did not enter an account.
- Installer/package verification checks the embedded administrator manifest,
  unsigned PE files, all payload hashes, clean login defaults, source ZIP CRC,
  exact source archive hashes, installation-folder validation and enumerated
  uninstall files. Refer to the release VALIDATION.json for the actual results.

## Limitations

- The user confirmed that the visible Check for Updates control appears and opens
  the updater. Computer Use access to the helper was denied, and the user then
  stopped Computer Use with Escape. No further desktop automation was performed.
- Actual installation, in-place update, uninstall, clean VM and cross-user
  elevation were not performed for this1.0.0 package.
- No in-world retest of the new binary's rendering/posing/motion blur was performed.
  The earlier AMD build worked in the user's live test; source equality does not
  replace a fresh visual test.
- Live updating to a future version is not yet tested.1.0.0 is the first build
  containing this updater; existing users must install it manually once.
- Linker emitted the same upstream duplicate-symbol /FORCE warnings present in
  the earlier working build. The new binary passed isolated startup despite them.

The installer remains unsigned and requests administrator permission. Settings
and cache remain separate and are preserved during updates and uninstall.
No installed viewer or real user profile was modified while preparing this release.
