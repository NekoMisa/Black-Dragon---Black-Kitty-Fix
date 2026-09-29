# Missing texture repair — 26 September 2026

The first logged-in test produced repeated `DECODE FAILED` messages. The old OpenJPEG 1.5.1 library decoded complete JPEG2000 files but rejected the initial 600-byte texture downloads. The viewer consequently marked these images as missing.

## Change

Built OpenJPEG 2.5.4 from upstream revision `6c4a29b00211eb0430fa0e5e890f1ce5c80f409f` using MSVC v143. Adapted the [official Second Life viewer integration](https://github.com/secondlife/viewer/blob/3cb70cc3d70245c01764fadb7b0eb359d235a27b/indra/llimagej2coj/llimagej2coj.cpp), which explicitly enables partial-stream decoding. Preserved Black Dragon's existing error-signalling contract, requested resolution and input byte limits. Updated linking and packaging to `openjp2.dll`.

The AMD flicker patch, posing and photography rendering code were not changed by this repair. The executable still displays version 26.2.0.57701; `viewer-sha256.json` identifies the revised executable and decoder DLL.

## Checks

- Before: all eight 600-byte texture samples failed with OpenJPEG 1.5.1; their complete files decoded.
- After: all 16 partial/complete tests passed with OpenJPEG 2.5.4; invalid input was rejected.
- Actual Black Dragon image-library integration: all 16 partial/complete texture tests passed, with correct dimensions.
- Lossless encode/decode round trips at 16×16 and 128×128 passed with identical pixels.
- Viewer rebuild and portable packaging completed with exit 0.
- Startup log reports `J2C Engine is: OpenJPEG runtime: 2.5.4` on the RX 7900 XTX. The updated viewer reached login without shader compilation/link errors.

The updated session reached STATE_STARTED at 08:43:11 UTC. At 08:46:08 UTC, its 4,198 log lines contained zero DECODE FAILED messages and zero matched shader compile/link failures. The process was responding. See texture-repair-runtime-check.json and texture-repair-runtime-check.log. This check excludes earlier sessions in the same log file.

The user subsequently confirmed that textures now display. The earlier report that the flicker fix appears to work is user-observed, not a comprehensive rendering test.

## Files and recovery

Use the same `Launch-Black-Dragon-AMD-Test.cmd` launcher. The installed official viewer remains separate; no cache purge was performed.

The previous test executable and decoder are retained in `C:\BD-AMD-Test\backups\before-openjpeg25`. The latest combined source patch is `combined-viewer.patch`; the previous one is `combined-viewer-before-textures.patch`. Build logs are `build-18-textures.log` and `package-18-textures.log`; test results are `texture-decoder-probe-after.log` and `viewer-texture-integration.log`.

The new dependency archive is `C:\BD-AMD-Test\openjpeg-2.5.4-windows64-57702.tar.bz2`. Its provenance and checksum are in `openjpeg25-package.json`. The original 1.5.1 package and its build scripts are retained only as history.
