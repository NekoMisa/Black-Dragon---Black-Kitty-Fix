"""Package only a hash-verified clean prior payload plus the current compiled viewer.

Do not use an installed viewer folder as --base-payload. The build directory must
have been compiled from this repository's viewer/ source. Requires NSIS3.12 and
.NET Framework4.8 csc.exe. Run --help for the required local paths.
"""
from pathlib import Path
import argparse, hashlib, json, re, shutil, subprocess, zipfile

def sha(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda:f.read(4*1024*1024),b''): h.update(b)
    return h.hexdigest()

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    for name in ['base-payload','base-manifest','build','nsis','staging','output']:
        parser.add_argument('--'+name,type=Path,required=True)
    a=parser.parse_args()
    here=Path(__file__).resolve().parent
    repo=here.parents[1]
    out=a.output.resolve(); out.mkdir(parents=True,exist_ok=True)
    payload=a.staging.resolve(); payload.mkdir(parents=True,exist_ok=False)
    original=json.loads(a.base_manifest.read_text(encoding='utf-8-sig'))
    for e in original:
        rel=Path(e['path']); assert not rel.is_absolute() and '..' not in rel.parts
        assert not set(x.lower() for x in rel.parts)&{'logs','user_settings','.git','texturecache','browser_profile'}
        assert rel.suffix.lower() not in {'.log','.pdb','.dmp'}
        origin=a.base_payload/rel
        assert sha(origin)==e['sha256'], 'Base payload changed: '+str(rel)
        dest=payload/rel; dest.parent.mkdir(parents=True,exist_ok=True); shutil.copy2(origin,dest)
    shutil.copy2(a.build/'newview/Release/blackdragon-bin.exe',payload/'BlackDragonViewer.exe')
    for name in ['menu_viewer.xml','notifications.xml','strings.xml','panel_login.xml','floater_about.xml']:
        shutil.copy2(repo/'viewer/indra/newview/skins/default/xui/en'/name,payload/'skins/default/xui/en'/name)
    shutil.copy2(here/'README.txt',payload/'Black-Kitty-Fix-README.txt')
    (payload/'black-kitty-fix-install.txt').write_text('BlackDragonBlackKittyFix\nBase=26.2.0.57700\nRelease=5.6.3\nFix=1.0.0\nInstallerRevision=1\n',encoding='utf-8')
    meta={'base_viewer':'26.2.0.57700','black_dragon_release':'5.6.3','release_name':'Favorite Dragon',
        'black_kitty_fix':'1.0.0','status':'independent release','installer_revision':1,'installer_only_revision':False,
        'installation_scope':'all users','automatic_update_checks':True,'updates_require_approval':True,
        'release_repository':'https://github.com/NekoMisa/Black-Dragon---Black-Kitty-Fix'}
    (payload/'black-kitty-fix-version.json').write_text(json.dumps(meta,indent=2),encoding='utf-8')
    if (payload/'build_data.json').is_file():
        data=json.loads((payload/'build_data.json').read_text())
        for key in ('Channel','Channel Base','AppName'):
            if key in data: data[key]=data[key].replace('0.1.0 Preview','1.0.0')
        data['Update Service']='https://api.github.com/repos/NekoMisa/Black-Dragon---Black-Kitty-Fix/releases/latest'
        (payload/'build_data.json').write_text(json.dumps(data,indent=2),encoding='utf-8')
    csc=Path(r'C:\Windows\Microsoft.NET\Framework64\v4.0.30319\csc.exe')
    updater=repo/'tools/black-kitty-updater/Updater.cs'
    subprocess.run([str(csc),'/nologo','/target:winexe','/out:'+str(payload/'BlackKittyUpdater.exe'),
        '/win32icon:'+str(repo/'viewer/indra/newview/res/bd_icon.ico'),
        '/r:System.Windows.Forms.dll','/r:System.Drawing.dll','/r:System.Net.Http.dll','/r:System.Web.Extensions.dll',str(updater)],check=True)
    manifest=[];install=[];uninstall=[];dirs=set()
    for p in sorted(x for x in payload.rglob('*') if x.is_file()):
        rel=p.relative_to(payload); folder=str(rel.parent)
        install+=['SetOutPath "$INSTDIR'+('\\'+folder if folder!='.' else '')+'"', 'File "'+str(p).replace('$','$$').replace('"','$\\"')+'"']
        uninstall+=['Delete "$INSTDIR\\'+str(rel).replace('$','$$')+'"']
        dirs.update(str(d) for d in rel.parents if str(d)!='.')
        manifest.append({'path':str(rel),'bytes':p.stat().st_size,'sha256':sha(p)})
    uninstall+=['RMDir "$INSTDIR\\'+d+'"' for d in sorted(dirs,key=lambda x:(x.count('\\'),x),reverse=True)]
    (out/'install-files.nsh').write_text('\n'.join(install),encoding='utf-8-sig')
    (out/'uninstall-files.nsh').write_text('\n'.join(uninstall),encoding='utf-8-sig')
    (out/'PAYLOAD-MANIFEST.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
    old={e['path']:e['sha256'] for e in original}
    changed=[e['path'] for e in manifest if e['path'] not in old or e['sha256']!=old[e['path']]]
    allowed={'BlackDragonViewer.exe','BlackKittyUpdater.exe','Black-Kitty-Fix-README.txt','black-kitty-fix-install.txt','black-kitty-fix-version.json','build_data.json'}|{'skins\\default\\xui\\en\\'+x for x in ['menu_viewer.xml','notifications.xml','strings.xml','panel_login.xml','floater_about.xml']}
    assert set(changed)<=allowed,changed
    (out/'PAYLOAD-CHANGES.json').write_text(json.dumps(changed,indent=2),encoding='utf-8')
    exe=out/'Black-Kitty-Fix-1.0.0-Windows-x64-Setup.exe'
    with (out/'installer-build.log').open('w',encoding='utf-8') as log:
        subprocess.run([str(a.nsis.resolve()),'/V3','/DPAYLOAD='+str(payload),'/DOUTPUT='+str(exe),
            '/DGUARD='+str(here/'InstallerGuard.ps1'),'/DINSTALL_FILES='+str(out/'install-files.nsh'),
            '/DUNINSTALL_FILES='+str(out/'uninstall-files.nsh'),str(here/'BlackKittyFix.nsi')],check=True,stdout=log,stderr=subprocess.STDOUT)
    source=out/'Black-Kitty-Fix-1.0.0-Source.zip'
    inventory=[]
    with zipfile.ZipFile(source,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
        for p in sorted(repo.rglob('*')):
            if not p.is_file(): continue
            rel=p.relative_to(repo)
            if {'.git','__pycache__'}&set(rel.parts): continue
            assert p.suffix.lower() not in {'.exe','.dll','.pdb','.obj','.log','.dmp'},str(rel)
            z.write(p,str(rel)); inventory.append({'path':rel.as_posix(),'sha256':sha(p)})
    (out/'SOURCE-MANIFEST.json').write_text(json.dumps(inventory,indent=2),encoding='utf-8')
    shutil.copy2(here/'README.txt',out/'README.txt')
    (out/'SHA256SUMS.txt').write_text(''.join(sha(p)+'  '+p.name+'\n' for p in [exe,source]),encoding='utf-8')
    print('Created clean installer/source:',exe,source,flush=True)

if __name__=='__main__': main()
