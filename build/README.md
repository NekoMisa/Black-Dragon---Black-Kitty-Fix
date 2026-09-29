# Black Dragon 5.6.3 — experimental AMD flicker port

Prepared for Misa's Windows build of Black Dragon 5.6.3 (Favorite Dragon).

**This is source code and a build helper, not a compiled viewer.** The Windows
build helper has not been run on Windows. The port has not been tested on an
AMD GPU or in Second Life. A successful build may still require fixes and
visual testing.

## Continue in local ChatGPT Work

Open the installed ChatGPT desktop app and select **Work → Work locally**.
Enable **Plugins → Computer Use** if you want the agent to operate desktop
apps. Availability depends on your account, region, app version and policies.
Opening the existing cloud chat in the app does not itself make it a local task.

Extract this ZIP into a folder and give a local task access to it. Ask:

> Continue this Black Dragon 5.6.3 AMD patch build on my Windows PC. Read
> README.md and inspect build_windows.py before running it. I have Visual
> Studio 2026. Verify that v143, the Windows SDK, Python and Git are installed,
> then build in C:\BD-AMD-Test. Resolve build errors and report what was tested.
> Keep my installed Black Dragon separate. The port is experimental and has
> only passed the source and software-OpenGL checks documented here.

## Manual build

Prerequisites:

- Windows x64.
- Visual Studio 2026 or 2022 with **Desktop development with C++**, **MSVC v143
  VS 2022 C++ x64/x86 build tools**, and a **Windows SDK**.
- Git for Windows, accessible as `git` in a new terminal.
- Windows Python 3.11 or newer, with pip and venv. Python 3.11 is the version
  used by the repository's checked-in CI workflow.
- Internet access and substantial free disk space for the source, dependencies
  and build output. Dependency downloads may take a while.

In PowerShell, change into the extracted folder and run:

```powershell
py -3.11 .\build_windows.py 2>&1 | Tee-Object -FilePath .\build.log
```

If you installed a different supported Python version, use `py -3` instead.
For a different build location:

```powershell
py -3 .\build_windows.py --work-dir D:\BD-AMD-Test
```

The helper:

1. Creates an isolated Python environment and installs autobuild 3.10.2,
   CMake 4.2 or later (below 5), and llsd into that environment.
2. Finds Visual Studio 2026/2022 with the v143 x64 compiler and initializes its
   build environment. Uses the appropriate CMake generator explicitly, avoiding
   autobuild's missing explicit VS 2026 generator mapping.
3. Fetches the exact Black Dragon revision below into its own source folder.
4. Checks and applies the included patch. A repeat run recognizes the same
   patch; it does not reset an existing checkout or discard local changes.
5. Configures an x64 Release build with OpenAL and OpenJPEG, disabling FMOD,
   Kakadu, proprietary Havok, Discord, NVAPI and Tracy for this test build.
6. Builds and uses Black Dragon's file manifest to assemble a separate viewer
   folder, omitting the NSIS installer creation step.

Expected output after a successful build: `C:\BD-AMD-Test\viewer`.
The helper does not launch the viewer or change your installed copy.
Use `--configure-only` to stop after generating `BlackDragon.sln`.
If any step fails, retain the complete log for investigation.

The build differs from the official release: OpenAL may have different sound
or streaming behavior, and proprietary Havok-dependent functions are omitted.
The repository's default Windows FMOD dependency points at the original
developer's `C:\bld` drive, so the helper deliberately selects OpenAL.
Other upstream dependencies may still fail to download or build; Windows
compilation has not been verified.

## Sources and scope

Black Dragon repository:
https://github.com/NiranV/Black-Dragon-Viewer

Exact base: `b2ca434b39bcd93aff0e23414999dddd73527e05`

Original Firestorm change by Trish_sl:
https://github.com/FirestormViewer/phoenix-firestorm/commit/0c132c2eb3d15afc56d7fe42589dc8f2eb778197

This is an adapted port of the applicable changes, not a byte-for-byte copy
of the full Firestorm commit. No official Black Dragon endorsement is implied.

| Area | Treatment |
| --- | --- |
| Rigged-mesh positions | Avatar-relative palette translations; shared stable transform helpers. |
| Normals and tangents | Direction transforms rather than subtraction of large transformed positions. |
| Mesh weights | Valid palette bounds and zero-weight fallback. |
| Shader arithmetic | Optional precise arithmetic and invariant vertex positions. |
| Black Dragon motion blur | Preserves previous palette and its origin together; velocity shaders use corresponding transforms; missing/stale history falls back to current data. |
| Shading | Upstream normal encoding safeguards, specular filtering and applicable fragment-shader corrections. |
| AMD texture uploads | Windows AMD threading override; no staggered texture uploads on AMD. |
| Shader cache | Driver/source-sensitive versioning, entry-point checks and Windows AMD bypass setting. |
| Firestorm DSA workaround | Omitted: this Black Dragon base has no `mHasDSA` dispatch flag or corresponding DSA call sites. Its legacy path is retained. |
| Firestorm depth-of-field kernel rewrite | Omitted: Black Dragon's custom foreground blur and chromatic behavior are retained. |
| Firestorm screen-space-reflection rewrite | Omitted: Black Dragon uses a different ray marcher. The sample-count bounds are retained separately. |

Files include upstream copyright headers and changes adapted for Black Dragon
with AI assistance. See the included upstream LICENSE. This package contains
no proprietary third-party binaries.

## Checks completed

- Patch applies to a clean Git index at the exact pinned Black Dragon revision.
- `git diff --check` passes for included source changes.
- Settings XML parses, and the new uniform identifiers/name entries agree.
- 512 shader-object compilation cases pass on Mesa llvmpipe software OpenGL
  using GLSL 4.20. Vertex checks cover all on/off combinations of precise math,
  local origin, direct normals and skinning; fragment checks use one representative
  configuration with the needed build defines. This is not every possible
  renderer permutation.
- 16 program links pass for the rigged bump and velocity paths with separately
  compiled helper objects across the eight precision/local-origin/normal options.
- Python build helper parses and resolves the repository's Windows compiler
  variables correctly in a local check.

**Not checked:** Windows C++ compilation/linking, Windows helper execution and
packaging, AMD driver compilation, in-world rendering, performance, and all
remaining shader program links. This is a candidate for testing, not a confirmed
fix or a production release.

## Visual test after a successful Windows build

Use the same affected mesh, location, lighting, camera position and graphics
settings in the official viewer and the test viewer. Compare:

- Stationary and slowly moving camera, close-up normal maps and highlights.
- Sun shadows and projector shadows.
- Avatar animation, posing, attachment changes and teleporting.
- Motion blur off and on; watch for trails or displacement.
- Depth of field and a full-resolution snapshot.

The new Debug Settings are `RenderRiggedLocalOrigin`,
`RenderRiggedDirectNormals`, `RenderRiggedPreciseMath`,
`RenderAMDDisableTextureThreading`, and `RenderAMDDisableShaderCache`.
They default to enabled; the last two act on Windows AMD. Restart after
changing them. Precise math may reduce performance. The rigged settings are
not restricted to AMD, matching the original patch's behavior.

Do not copy just the shaders into your installed viewer: they require matching
C++ uniform and palette changes. To stop using the test build, close it and
launch the official installed viewer. A separate program folder does not by
itself guarantee separate per-user settings or caches; back up your settings
before testing.
