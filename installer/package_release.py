from pathlib import Path
import importlib.util, os, shutil, json, hashlib, subprocess, zipfile

workspace=Path(__file__).resolve().parents[2]
root=Path(r'C:\BD-AMD-Test')
src=root/'source'
payload=root/'release/BlackKittyFix-0.1.0'
out=workspace/'outputs/Black-Kitty-Fix-0.1.0'
out.mkdir(parents=True,exist_ok=True)
spec=importlib.util.spec_from_file_location('bdhelper',workspace/'work/package/Black-Dragon-AMD-Port/build_windows.py')
helper=importlib.util.module_from_spec(spec); spec.loader.exec_module(helper)
assert not payload.exists(), 'Use a fresh staging directory to avoid stale files.'
helper.assemble_viewer(src,root/'build-vs18-v143',payload)
shutil.copy2(src/'LICENSE',payload/'LICENSE.txt')
shutil.copytree(root/'build-vs18-v143/packages/LICENSES',payload/'ThirdPartyLicenses')
shutil.copy2(root/'openjpeg25-source/LICENSE',payload/'ThirdPartyLicenses/OpenJPEG-2.5.4.txt')
shutil.copy2(workspace/'work/installer/README.txt',payload/'Black-Kitty-Fix-README.txt')
(payload/'black-kitty-fix-install.txt').write_text('BlackDragonBlackKittyFix\nBase=26.2.0.57700\nRelease=5.6.3\nFix=0.1.0\n')
(payload/'black-kitty-fix-version.json').write_text(json.dumps({'base_viewer':'26.2.0.57700','black_dragon_release':'5.6.3','release_name':'Favorite Dragon','black_kitty_fix':'0.1.0','status':'unofficial preview','automatic_updates':False},indent=2))

def q(s):
 return '"'+str(s).replace('$','$$').replace('"','$\\"')+'"'
files=sorted(p for p in payload.rglob('*') if p.is_file())
install=[]; uninstall=[]; dirs=set()
for f in files:
 rel=f.relative_to(payload)
 # Only runtime resources; never profile data or build intermediates.
 assert not any(part.lower() in ('.git','logs','user_settings') for part in rel.parts), rel
 folder=str(rel.parent)
 install+=['SetOutPath "$INSTDIR'+('\\'+folder if folder!='.' else '')+'"','File '+q(f)]
 uninstall+=['Delete "$INSTDIR\\'+str(rel).replace('$','$$')+'"']
 for d in rel.parents:
  if str(d)!='.': dirs.add(str(d))
uninstall+=['RMDir "$INSTDIR\\'+d+'"' for d in sorted(dirs,key=lambda x:(x.count('\\'),x),reverse=True)]
(out/'install-files.nsh').write_text('\n'.join(install),encoding='utf-8-sig')
(out/'uninstall-files.nsh').write_text('\n'.join(uninstall),encoding='utf-8-sig')
manifest=[{'path':str(p.relative_to(payload)),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in files]
(out/'payload-manifest.json').write_text(json.dumps(manifest,indent=2))
shutil.copy2(workspace/'work/installer/BlackKittyFix.nsi',out/'BlackKittyFix.nsi')
shutil.copy2(workspace/'work/installer/README.txt',out/'README.txt')
exe=out/'Black-Dragon-5.6.3-Black-Kitty-Fix-0.1.0-Setup.exe'
compiler=workspace/'work/installer/nsis-3.12/makensis.exe'
with (out/'installer-build.log').open('w') as log:
 subprocess.run([str(compiler),'/V3',f'/DPAYLOAD={payload}',f'/DOUTPUT={exe}',f'/DINSTALL_FILES={out / "install-files.nsh"}',f'/DUNINSTALL_FILES={out / "uninstall-files.nsh"}',str(out/'BlackKittyFix.nsi')],stdout=log,stderr=subprocess.STDOUT,check=True)
print('Installer created:',exe,flush=True)

# Ship the exact working sources, not unmodified upstream sources plus an
# undocumented local patch. Git's index includes the newly restored shaders.
tracked=subprocess.check_output(['git','-C',str(src),'ls-files','-z']).decode().split('\0')
sourcezip=out/'Black-Dragon-5.6.3-Black-Kitty-Fix-0.1.0-Source.zip'
with zipfile.ZipFile(sourcezip,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 for rel in tracked:
  p=src/rel
  if rel and p.is_file(): z.write(p,'viewer/'+rel)
 for p in (root/'openjpeg25-source').rglob('*'):
  if p.is_file() and '.git' not in p.relative_to(root/'openjpeg25-source').parts:
   z.write(p,'openjpeg/'+str(p.relative_to(root/'openjpeg25-source')))
 for name in ['build_windows.py','black-dragon-amd.patch','README.md']:
  p=workspace/'work/package/Black-Dragon-AMD-Port'/name
  if p.exists():z.write(p,'build/'+name)
 for name in ['BlackKittyFix.nsi','package_release.py','prepare_release.py','README.txt']:
  z.write(workspace/'work/installer'/name,'installer/'+name)
 z.write(workspace/'outputs/combined-viewer.patch','build/combined-viewer.patch')
 z.write(workspace/'outputs/TEXTURE-REPAIR.md','build/TEXTURE-REPAIR.md')
 for name in ['upgrade_openjpeg.py','modern-llimagej2coj.cpp','modern-llimagej2coj.h','test_viewer_texture.py','viewer_texture_probe.cpp','test_openjpeg25.py','openjpeg25_probe.c']:
  z.write(workspace/'work'/name,'build/'+name)
(out/'SHA256SUMS.txt').write_text('\n'.join(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+p.name for p in [exe,sourcezip])+'\n')
print('Matching source archive created:',sourcezip,flush=True)
