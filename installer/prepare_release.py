from pathlib import Path
import shutil

root = Path(r'C:\BD-AMD-Test')
src = root/'source'
backup = root/'backups/before-kitty-release'
backup.mkdir(parents=True, exist_ok=True)

def change(rel, pairs):
    p=src/rel
    old=p.read_text(encoding='utf-8')
    new=old
    for a,b in pairs:
        assert a in new, (rel,a)
        new=new.replace(a,b)
    out=backup/rel
    out.parent.mkdir(parents=True,exist_ok=True)
    shutil.copy2(p,out)
    p.write_text(new,encoding='utf-8',newline='\n')

change('indra/newview/llappviewer.cpp', [
 ('initAppDirs("BlackDragon")','initAppDirs("BlackDragonBlackKittyFix")'),
 ('VIEWER_WINDOW_CLASSNAME = "Black Dragon"','VIEWER_WINDOW_CLASSNAME = "Black Dragon Black Kitty Fix"'),
])
change('indra/llfilesystem/lldir.cpp', [('add(getOSCacheDir(), "Black Dragon")','add(getOSCacheDir(), "Black Dragon Black Kitty Fix")')])
change('indra/newview/res/viewerRes.rc', [
 ('Loading Black Dragon...','Loading Black Dragon - Black Kitty Fix...'),
 ('VALUE "FileDescription", "Black Dragon"','VALUE "FileDescription", "Black Dragon - Black Kitty Fix 0.1.0 (Unofficial Preview)"'),
 ('VALUE "ProductName", "Second Life"','VALUE "ProductName", "Black Dragon 5.6.3 - Black Kitty Fix 0.1.0"'),
])
change('indra/newview/skins/default/xui/en/strings.xml', [
 ('<string name="APP_NAME">Black Dragon</string>','<string name="APP_NAME">Black Dragon - Black Kitty Fix 0.1.0</string>'),
 ('[VIEWER_VERSION_LOCAL] - [VIEWER_VERSION_IDENTIFIER]', '[VIEWER_VERSION_LOCAL] - [VIEWER_VERSION_IDENTIFIER]\nBlack Kitty Fix: 0.1.0 (Unofficial Preview)\nManual updates only. Separate settings and cache.'),
])
helper=Path('work/package/Black-Dragon-AMD-Port/build_windows.py')
s=helper.read_text()
shutil.copy2(helper,backup/'build_windows.py')
s=s.replace('Black Dragon AMD Test','Black Dragon Black Kitty Fix 0.1.0 Preview').replace('AUTOBUILD_BUILD_ID="57701"','AUTOBUILD_BUILD_ID="57700"')
helper.write_text(s)
print('Prepared separate product identity; base version remains 26.2.0.57700.')
