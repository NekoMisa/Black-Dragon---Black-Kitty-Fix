"""Repackage an existing, hash-verified clean payload. Never compile the viewer."""
from pathlib import Path
import argparse, hashlib, json, shutil, subprocess, zipfile

def digest(p): return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--base-payload', type=Path, required=True)
    parser.add_argument('--base-manifest', type=Path, required=True)
    parser.add_argument('--base-source', type=Path, required=True)
    parser.add_argument('--nsis', type=Path, required=True)
    parser.add_argument('--staging', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args=parser.parse_args()
    here=Path(__file__).resolve().parent
    out=args.output.resolve(); out.mkdir(parents=True,exist_ok=True)
    payload=args.staging.resolve()
    payload.mkdir(parents=True,exist_ok=False)
    base=json.loads(args.base_manifest.read_text())
    # Copy only the original enumerated release files, never the working profile
    # or anything added to an installed directory since it was released.
    for e in base:
        rel=Path(e['path']); assert not rel.is_absolute() and '..' not in rel.parts
        origin=args.base_payload/rel
        assert digest(origin)==e['sha256'], f'Original release file changed: {rel}'
        assert not set(x.lower() for x in rel.parts)&{'logs','user_settings','.git','texturecache','browser_profile'}
        assert rel.suffix.lower() not in {'.log','.pdb','.dmp'}
        dst=payload/rel; dst.parent.mkdir(parents=True,exist_ok=True); shutil.copy2(origin,dst)
    shutil.copy2(here/'README-r2.txt',payload/'Black-Kitty-Fix-README.txt')
    marker=payload/'black-kitty-fix-install.txt'
    marker.write_text(marker.read_text().rstrip()+'\nInstallerRevision=2\n')
    v=payload/'black-kitty-fix-version.json'
    meta=json.loads(v.read_text()); meta['installer_revision']=2; meta['installer_only_revision']=True
    meta['installation_scope']='all users'; v.write_text(json.dumps(meta,indent=2))

    files=sorted(p for p in payload.rglob('*') if p.is_file())
    install=[]; uninstall=[]; dirs=set(); manifest=[]
    for p in files:
        rel=p.relative_to(payload); folder=str(rel.parent)
        escaped=str(p).replace('$','$$').replace('"','$\\"')
        install+=['SetOutPath "$INSTDIR'+('\\'+folder if folder!='.' else '')+'"',f'File "{escaped}"']
        uninstall+=['Delete "$INSTDIR\\'+str(rel).replace('$','$$')+'"']
        dirs.update(str(d) for d in rel.parents if str(d)!='.')
        manifest.append({'path':str(rel),'bytes':p.stat().st_size,'sha256':digest(p)})
    uninstall+=['RMDir "$INSTDIR\\'+d+'"' for d in sorted(dirs,key=lambda d:(d.count('\\'),d),reverse=True)]
    (out/'install-files.nsh').write_text('\n'.join(install),encoding='utf-8-sig')
    (out/'uninstall-files.nsh').write_text('\n'.join(uninstall),encoding='utf-8-sig')
    (out/'payload-manifest.json').write_text(json.dumps(manifest,indent=2))
    before={e['path']:e['sha256'] for e in base}
    changed=[e['path'] for e in manifest if e['sha256']!=before[e['path']]]
    assert set(changed)=={'Black-Kitty-Fix-README.txt','black-kitty-fix-install.txt','black-kitty-fix-version.json'}, changed
    assert digest(args.base_source)=='3a4d62323e25124cbd4c363e0553b7e27603edef08914ef7b03819a8df47ed01'
    for name in ['BlackKittyFix-r2.nsi','InstallerGuard.ps1','package_revision2.py','README-r2.txt','Test-InstallerGuard.ps1']:
        shutil.copy2(here/name,out/name)
    shutil.copy2(here/'README-r2.txt',out/'README.txt')
    stem='Black-Dragon-5.6.3-Black-Kitty-Fix-0.1.0'
    exe=out/(stem+'-Setup-r2.exe')
    command=[str(args.nsis.resolve()),'/V3',f'/DPAYLOAD={payload}',f'/DOUTPUT={exe}',f'/DGUARD={out/"InstallerGuard.ps1"}',f'/DINSTALL_FILES={out/"install-files.nsh"}',f'/DUNINSTALL_FILES={out/"uninstall-files.nsh"}',str(out/'BlackKittyFix-r2.nsi')]
    with (out/'installer-build-r2.log').open('w') as log:
        subprocess.run(command,stdout=log,stderr=subprocess.STDOUT,check=True)
    source=out/(stem+'-Source-r2.zip')
    with zipfile.ZipFile(args.base_source) as old, zipfile.ZipFile(source,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as new:
        for info in old.infolist(): new.writestr(info,old.read(info.filename))
        for name in ['BlackKittyFix-r2.nsi','InstallerGuard.ps1','package_revision2.py','README-r2.txt','Test-InstallerGuard.ps1']:
            new.write(out/name,'installer/revision2/'+name)
        new.write(args.base_manifest,'installer/revision2/base-payload-manifest.json')
        new.writestr('INSTALLER-REVISION-2.txt', 'Installer-only revision 2. All viewer/ and openjpeg/ source files are unchanged.\nSee installer/revision2/README-r2.txt.\nTo repackage, run package_revision2.py --help; supply the original clean payload, base manifest and Source.zip, and the NSIS 3.12 compiler.\nThe builder verifies original file hashes before copying. No source or viewer compilation is performed.\n')
    (out/'SHA256SUMS.txt').write_text(''.join(digest(p)+'  '+p.name+'\n' for p in [exe,source]))
    (out/'PAYLOAD-VERIFICATION.json').write_text(json.dumps({'original_payload_files_verified':len(base),'new_payload_files':len(manifest),'changed_payload_files':changed,'viewer_and_all_libraries_unchanged':True,'viewer_recompiled':False,'base_version':'26.2.0.57700','black_dragon_release':'5.6.3 Favorite Dragon','fix_version':'0.1.0','installer_revision':2},indent=2))
    print('Built',exe,flush=True)
    print('Source archive',source,flush=True)

if __name__=='__main__': main()
