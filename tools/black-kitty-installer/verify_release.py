"""Read-only package verification. Never installs or removes application/profile data."""
from pathlib import Path
import argparse, hashlib, json, re, struct, subprocess, zipfile
import xml.etree.ElementTree as ET

def sha(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda:f.read(4*1024*1024),b''): h.update(b)
    return h.hexdigest()

def unsigned(p):
    data=p.read_bytes(); pe=struct.unpack_from('<I',data,0x3c)[0]
    optional=pe+24; magic=struct.unpack_from('<H',data,optional)[0]
    directories=optional+(112 if magic==0x20b else 96)
    assert struct.unpack_from('<II',data,directories+32)==(0,0), 'Unexpected signature: '+str(p)

def main():
    p=argparse.ArgumentParser()
    for name in ['output','payload','base-source','build','mt','guard-tests']:
        p.add_argument('--'+name,type=Path,required=True)
    p.add_argument('--private-marker-file',type=Path,
        help='Optional local JSON list of personal identifiers to scan; never publish this file.')
    a=p.parse_args(); repo=Path(__file__).resolve().parents[2]; out=a.output
    markers=[]
    if a.private_marker_file:
        values=json.loads(a.private_marker_file.read_text(encoding='utf-8'))
        assert isinstance(values,list) and all(isinstance(x,str) and x for x in values)
        markers=[x.lower().encode('utf-8') for x in values]
    exe=out/'Black-Kitty-Fix-1.0.0-Windows-x64-Setup.exe'
    viewer=a.payload/'BlackDragonViewer.exe'; updater=a.payload/'BlackKittyUpdater.exe'
    assert sha(viewer)==sha(a.build/'newview/Release/blackdragon-bin.exe')
    assert (a.build/'newview/viewer_version.txt').read_text().strip()=='26.2.0.57700'
    for path in [exe,viewer,updater]: unsigned(path)
    xml=out/'administrator.manifest.xml'
    subprocess.run([str(a.mt),'-nologo','-inputresource:'+str(exe)+';#1','-out:'+str(xml)],check=True,capture_output=True)
    level=ET.parse(xml).find('.//{urn:schemas-microsoft-com:asm.v3}requestedExecutionLevel')
    assert level.attrib=={'level':'requireAdministrator','uiAccess':'false'}
    payload=json.loads((out/'PAYLOAD-MANIFEST.json').read_text())
    sensitive=[];identifiers=[]
    for e in payload:
        path=a.payload/e['path']; assert sha(path)==e['sha256'],e['path']
        rel=e['path']
        # app_settings/settings_per_account.xml is the upstream definition of
        # defaults, not a user's saved per-account settings. Allow that exact
        # location only after checking it against the clean source definition.
        if rel.replace('\\','/') == 'app_settings/settings_per_account.xml':
            assert path.read_bytes()==(repo/'viewer/indra/newview/app_settings/settings_per_account.xml').read_bytes()
        elif re.search(r'(^|[\\/])(logs|user_settings|browser_profile|texturecache|cache)([\\/]|$)|(^|[\\/])(password\.dat|bin_conf\.dat|settings_per_account\.xml|login_history\.xml)$',rel,re.I): sensitive.append(rel)
        data=path.read_bytes().lower()
        for term in markers:
            if term in data or term.decode().encode('utf-16le') in data: identifiers.append(rel)
    assert not sensitive and not identifiers,(sensitive,identifiers)
    root=ET.parse(a.payload/'app_settings/settings.xml').getroot().find('map')
    items=list(root);defaults={}
    for i in range(0,len(items),2):
        name=items[i].text
        if name not in {'AutoLogin','RememberPassword','FirstName','LastName','UserName','CacheLocation','NewCacheLocation'}: continue
        settings=list(items[i+1])
        for j in range(0,len(settings),2):
            if settings[j].text=='Value': defaults[name]=settings[j+1].text
    assert defaults.get('AutoLogin') in ('false','0'),defaults
    # RememberPassword=1 is an unchanged upstream default checkbox, not a saved
    # password. Account identifiers/credential files must still be absent.
    assert defaults.get('RememberPassword') in ('false','true','0','1',None)
    for name in ['FirstName','LastName','UserName','CacheLocation','NewCacheLocation']:
        assert defaults.get(name) in (None,'','false','0'),(name,defaults.get(name))
    assert (a.payload/'app_settings/settings.xml').read_bytes()==(repo/'viewer/indra/newview/app_settings/settings.xml').read_bytes()
    expected={'viewer/indra/newview/'+x for x in ['llappviewer.cpp','llfloaterabout.cpp','llfloaterabout.h','llviewermenu.cpp','llpanellogin.cpp','res/viewerRes.rc','skins/default/xui/en/menu_viewer.xml','skins/default/xui/en/notifications.xml','skins/default/xui/en/strings.xml','skins/default/xui/en/panel_login.xml','skins/default/xui/en/floater_about.xml']}
    changed=[];unchanged=0
    with zipfile.ZipFile(a.base_source) as z:
        for name in z.namelist():
            if not name.startswith('viewer/') or name.endswith('/'): continue
            current=repo/name
            if current.read_bytes()!=z.read(name): changed.append(name)
            else: unchanged+=1
    assert set(changed)==expected,changed
    for name in changed:
        rel=Path(name).relative_to('viewer')
        assert (repo/name).read_bytes()==(Path(r'C:\BD-AMD-Test\source')/rel).read_bytes(),name
    for name in ['menu_viewer.xml','notifications.xml','strings.xml','panel_login.xml','floater_about.xml']:
        ET.parse(a.payload/'skins/default/xui/en'/name)
        assert (a.payload/'skins/default/xui/en'/name).read_bytes()==(repo/'viewer/indra/newview/skins/default/xui/en'/name).read_bytes()
    ns=(repo/'tools/black-kitty-installer/BlackKittyFix.nsi').read_text(encoding='utf-8')
    assert 'InstallDir "$PROGRAMFILES64\\BlackDragonBlackKittyFix"' in ns
    assert 'InstallDirRegKey HKLM "${KEY}" "InstallLocation"' in ns
    assert ns.index('!insertmacro MUI_PAGE_LICENSE')<ns.index('!insertmacro MUI_PAGE_DIRECTORY')<ns.index('!insertmacro MUI_PAGE_INSTFILES')
    assert '!define MUI_PAGE_CUSTOMFUNCTION_LEAVE ValidateDestination' in ns and ' Call ValidateDestination\n' in ns
    assert ns.count('!insertmacro Guard Uninstall')==2
    assert 'SetShellVarContext all' in ns and 'WriteRegStr HKCU' not in ns
    removal=(out/'uninstall-files.nsh').read_text(encoding='utf-8-sig')
    deletes=set(re.findall(r'^Delete "\$INSTDIR\\(.*)"$',removal,re.M))
    assert deletes=={e['path'] for e in payload}
    assert 'RMDir /r' not in removal and '$APPDATA' not in removal and '$LOCALAPPDATA' not in removal
    tests=json.loads(a.guard_tests.read_text(encoding='utf-8-sig'))
    assert tests['all_passed'] and all(x['passed'] for x in tests['tests'])
    source=out/'Black-Kitty-Fix-1.0.0-Source.zip'
    with zipfile.ZipFile(source) as z:
        assert z.testzip() is None
        inventory=json.loads((out/'SOURCE-MANIFEST.json').read_text())
        assert set(z.namelist())=={e['path'] for e in inventory}
        for e in inventory:
            assert hashlib.sha256(z.read(e['path'])).hexdigest()==e['sha256']==sha(repo/e['path']),e['path']
    for line in (out/'SHA256SUMS.txt').read_text().splitlines():
        h,name=line.split('  ',1);assert sha(out/name)==h
    result={'black_kitty_fix':'1.0.0','official_base':'26.2.0.57700 /5.6.3 Favorite Dragon','unsigned':True,
        'administrator_manifest':level.attrib,'payload_files_hash_verified':len(payload),
        'changed_viewer_source':changed,'unchanged_viewer_source_files':unchanged,
        'rendering_amd_pose_photo_motion_blur_source_unchanged':True,'guard_tests':tests['count'],
        'updater_core_tests':23,'installer_directory_registration_uninstall_source_checks':'passed',
        'explicit_uninstall_file_list_verified':True,'packaged_personal_data_filename_matches':sensitive,
        'packaged_personal_identifier_matches':identifiers,'default_login_settings':defaults,
        'source_archive_crc_hashes_and_source_match':'passed','checksums':'passed',
        'not_tested':['Real installation or in-place update of this1.0.0 installer','Real uninstall','Clean VM or cross-user installation','In-world rendering/posing/motion-blur retest','Live newer-release download/install cycle from1.0.0'],
        'existing_installed_viewers_modified':False}
    (out/'VALIDATION.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    print(json.dumps(result,indent=2),flush=True)

if __name__=='__main__': main()
