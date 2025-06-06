
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['kivy_app.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('frontend/assets/*', 'frontend/assets'),
        ('version.txt', '.'),
        ('browser_data.json', '.')
    ],
    hiddenimports=['kivy_garden.webview'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='GS_Browser',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,  # Set to True temporarily for debugging
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='frontend/assets/icon.ico'
)
