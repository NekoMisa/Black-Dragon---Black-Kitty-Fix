from pathlib import Path
import tarfile, hashlib, json

root = Path(r'C:\BD-AMD-Test')
work = Path(__file__).resolve().parent
source = root/'source'
code = (work/'modern-llimagej2coj.cpp').read_text()
# Preserve Black Dragon's existing decodeFailed() contract and byte/discard limits.
code = code.replace('S32 max_bytes = (base.getMaxBytes() ? base.getMaxBytes() : data_size);',
                    'S32 max_bytes = (base.getMaxBytes() > 0 ? llmin(base.getMaxBytes(), data_size) : data_size);')
code = code.replace('decoder.decode(base.getData(), max_bytes, &image_channels, base.mDiscardLevel)',
                    'decoder.decode(base.getData(), max_bytes, &image_channels, base.getRawDiscardLevel())')
start = code.index('    if (!decoded)\n', code.index('bool LLImageJ2COJ::decodeImpl'))
end = code.index('    opj_image_t *image', start)
code = code[:start] + '''    if (!decoded || channels <= 0)
    {
        base.setLastError("OpenJPEG could not decode the JPEG2000 stream");
        base.decodeFailed();
        return true;
    }

''' + code[end:]
code = code.replace('    U8 *rawp = raw_image.getData();', '''    U8 *rawp = raw_image.getData();
    if (!rawp)
    {
        base.setLastError("Could not allocate decoded texture");
        base.decodeFailed();
        return true;
    }''')
code = code.replace('            LL_DEBUGS("Texture") << "ERROR -> decodeImpl: failed! (OpenJPEG bug)" << LL_ENDL;',
                    '''            base.setLastError("OpenJPEG returned an empty texture component");
            base.decodeFailed();
            return true;''')
# Metadata must not overwrite the caller's requested resolution in this viewer.
code = code.replace('    base.mDiscardLevel = discard_level;\n    base.setSize(width, height, components);',
                    '    base.setSize(width, height, components);')
(source/'indra/llimagej2coj/llimagej2coj.cpp').write_text(code, newline='\n')
(source/'indra/llimagej2coj/llimagej2coj.h').write_text((work/'modern-llimagej2coj.h').read_text(), newline='\n')
cmake = source/'indra/cmake/OpenJPEG.cmake'
text = cmake.read_text().replace('debug openjpegd', 'debug openjp2').replace('optimized openjpeg)', 'optimized openjp2)')
cmake.write_text(text, newline='\n')
for rel in ['indra/cmake/Copy3rdPartyLibs.cmake', 'indra/newview/viewer_manifest.py']:
    p = source/rel
    p.write_text(p.read_text().replace('openjpeg.dll', 'openjp2.dll'), newline='\n')
archive = root/'openjpeg-2.5.4-windows64-57702.tar.bz2'
with tarfile.open(archive, 'w:bz2') as tar:
    for src, dst in [
        ('openjpeg25-source/src/lib/openjp2/openjpeg.h', 'include/openjpeg/openjpeg.h'),
        ('openjpeg25-build/src/lib/openjp2/opj_config.h', 'include/openjpeg/opj_config.h'),
        ('openjpeg25-build/bin/Release/openjp2.lib', 'lib/release/openjp2.lib'),
        ('openjpeg25-build/bin/Release/openjp2.dll', 'lib/release/openjp2.dll'),
        ('openjpeg25-source/LICENSE', 'LICENSES/openjpeg.txt')
    ]:
        tar.add(root/src, arcname=dst)
digest = hashlib.md5(archive.read_bytes()).hexdigest()
p = source/'autobuild.xml'
text = p.read_text()
assert 'file:///C:/BD-AMD-Test/openjpeg-1.5.1-windows64-57701.tar.bz2' in text
text = text.replace('file:///C:/BD-AMD-Test/openjpeg-1.5.1-windows64-57701.tar.bz2', archive.as_uri())
text = text.replace('bf7c200aec242385d2446f63780b64de', digest).replace('<string>1.5.1.200900057</string>', '<string>2.5.4</string>')
p.write_text(text, newline='\n')
print(json.dumps({'archive':str(archive),'md5':digest,'openjpeg_revision':'6c4a29b00211eb0430fa0e5e890f1ce5c80f409f',
                  'viewer_adapter_revision':'3cb70cc3d70245c01764fadb7b0eb359d235a27b'}))
