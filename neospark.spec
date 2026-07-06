# -*- mode: python ; coding: utf-8 -*-
"""PyInstaller spec for building a single executable NeoSpark CLI."""
from PyInstaller.building.build_main import Analysis, PYZ, EXE, COLLECT

a = Analysis(
    ["src/neospark/__main__.py"],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=["neospark.commands.auth", "neospark.commands.models",
                   "neospark.commands.generate", "neospark.commands.status",
                   "neospark.commands.images", "neospark.commands.sessions",
                   "neospark.commands.billing", "neospark.commands.download"],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name="neospark",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
