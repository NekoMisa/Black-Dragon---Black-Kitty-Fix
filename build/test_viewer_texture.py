import importlib.util, os, subprocess, shutil, xml.etree.ElementTree as ET
from pathlib import Path
work = Path(__file__).resolve().parent
build = Path(r'C:\BD-AMD-Test\build-vs18-v143')
spec = importlib.util.spec_from_file_location('helper', work/'package/Black-Dragon-AMD-Port/build_windows.py')
module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
*_, env = module.visual_studio_environment()
ns={'m':'http://schemas.microsoft.com/developer/msbuild/2003'}
def group(path):
    return next(e for e in ET.parse(path).getroot().findall('m:ItemDefinitionGroup',ns) if "'Release|x64'" in e.get('Condition',''))
def items(g, path):
    return [s for s in (g.findtext(path, namespaces=ns) or '').split(';') if s and '%(' not in s]
g=group(build/'llimagej2coj/llimagej2coj.vcxproj')
defs=items(g,'m:ClCompile/m:PreprocessorDefinitions')
includes=items(g,'m:ClCompile/m:AdditionalIncludeDirectories')
includes += [str(build/'packages/include'/p) for p in ['', 'apr-1','zlib-ng','meshoptimizer','libpng16']]
args=[shutil.which('cl.exe',path=env['PATH']),'/nologo','/MD','/EHsc','/std:c++17','/arch:AVX2']
args += ['/D'+s.replace('\\"','"') for s in defs if not s.startswith('CMAKE_INTDIR')]
args += ['/I'+s for s in includes]
g=group(build/'newview/blackdragon-bin.vcxproj')
libs=items(g,'m:Link/m:AdditionalDependencies')
args += [str(work/'viewer_texture_probe.cpp'),'/Fe:'+str(work/'viewer_texture_probe.exe'),'/Fo:'+str(work/'viewer_texture_probe.obj'),'/link','/SUBSYSTEM:CONSOLE','/LIBPATH:'+str(build/'packages/lib/release'),*libs]
subprocess.run(args,env=env,cwd=build/'newview',check=True)
env['PATH']=str(build/'packages/lib/release') + os.pathsep + env['PATH']
samples=list(Path(r'C:\BD-AMD-Test\viewer\skins\default\textures').glob('*.j2c'))[:8]
result=subprocess.run([str(work/'viewer_texture_probe.exe'),*map(str,samples)],env=env,timeout=45)
raise SystemExit(result.returncode)
