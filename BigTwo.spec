# Single-file build; paths are relative to this spec, never the caller.
from pathlib import Path

root = Path(SPECPATH)
for resource in ('fonts/NotoSansCJKtc-Regular.otf', 'fonts/OFL.txt',
                 'FreeSansBold.ttf', 'Image/table.png'):
    if not (root / resource).is_file():
        raise SystemExit(f'Missing required build resource: {resource}')

a = Analysis(
    [str(root / 'main.py')],
    pathex=[str(root)],
    binaries=[],
    datas=[(str(root / 'Image'), 'Image'),
           (str(root / 'fonts'), 'fonts'),
           (str(root / 'FreeSansBold.ttf'), '.')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)
exe = EXE(
    pyz, a.scripts, a.binaries, a.datas, [],
    name='BigTwo',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=False,
    icon=str(root / 'Image' / 'simpybigtwo_default.ico'),
)
