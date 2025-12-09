# -*- mode: python ; coding: utf-8 -*-

"""
PyInstaller spec file for YouTube Downloader
Questo file configura la creazione dell'eseguibile .exe
"""

import sys
from pathlib import Path

block_cipher = None

# Dati aggiuntivi da includere (nessuno per questo progetto)
datas = []

# Import nascosti necessari per yt-dlp e tkinter
hiddenimports = [
    'tkinter',
    'tkinter.ttk',
    'tkinter.filedialog',
    'tkinter.messagebox',
    'tkinter.scrolledtext',
    'yt_dlp',
    'yt_dlp.extractor',
    'yt_dlp.extractor.lazy_extractors',
    'yt_dlp.downloader',
    'yt_dlp.postprocessor',
    'certifi',
    'websockets',
    'brotli',
    'mutagen',
    'pycryptodomex',
]

a = Analysis(
    ['youtube_downloader.py'],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'matplotlib',
        'numpy',
        'pandas',
        'scipy',
        'PyQt5',
        'PyQt6',
        'PySide2',
        'PySide6',
    ],
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
    name='YouTubeDownloader',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # False = nessuna finestra console (solo GUI)
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,  # Opzionale: aggiungi qui il percorso di un'icona .ico
)
