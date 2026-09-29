import importlib.util, os, subprocess, shutil
from pathlib import Path
root = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('helper', root/'package/Black-Dragon-AMD-Port/build_windows.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
*_, env = module.visual_studio_environment()
subprocess.run([shutil.which('cl.exe', path=env['PATH']), '/nologo', '/MD',
    '/I', r'C:\BD-AMD-Test\openjpeg25-source\src\lib\openjp2',
    '/I', r'C:\BD-AMD-Test\openjpeg25-build\src\lib\openjp2',
    str(root/'openjpeg25_probe.c'), '/Fe:'+str(root/'openjpeg25_probe.exe'), '/Fo:'+str(root/'openjpeg25_probe.obj'),
    '/link', r'C:\BD-AMD-Test\openjpeg25-build\bin\Release\openjp2.lib'], env=env, check=True, cwd=root)
env['PATH'] = r'C:\BD-AMD-Test\openjpeg25-build\bin\Release' + os.pathsep + env['PATH']
failures = 0
for p in list(Path(r'C:\BD-AMD-Test\viewer\skins\default\textures').glob('*.j2c'))[:8]:
    for size in [600, 0]:
        print(p.name, 'partial' if size else 'complete', flush=True)
        data = p.read_bytes()
        sample = root/'probe-input.j2c'
        sample.write_bytes(data[:size] if size else data)
        result = subprocess.run([str(root/'openjpeg25_probe.exe'), str(sample)],env=env)
        failures += result.returncode != 0
sample.write_bytes(b'Invalid JPEG2000 data')
invalid = subprocess.run([str(root/'openjpeg25_probe.exe'), str(sample)],env=env)
print(f'Valid texture tests: {16-failures}/16 passed; invalid input rejected: {invalid.returncode != 0}', flush=True)
raise SystemExit(1 if failures or invalid.returncode == 0 else 0)
