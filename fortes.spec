# -*- mode: python ; coding: utf-8 -*-

datas = [
    ('.env', '.'),
    ('front/src/assets', 'front/src/assets'),
    ('front/src/components', 'front/src/components'),
    ('front/src/routes', 'front/src/routes'),
    ('front/src/utils', 'front/src/utils'),
    ('front/src/views', 'front/src/views'),
    ('back/src/config', 'back/src/config'),
    ('back/src/controllers', 'back/src/controllers'),
    ('back/src/models', 'back/src/models'),
    ('back/src/repositories', 'back/src/repositories'),
    ('back/src/services', 'back/src/services'),
    ('back/src/utils', 'back/src/utils'),
]

hiddenimports = [
    'sqlalchemy',
    'sqlalchemy.dialects.mysql',
    'sqlalchemy.dialects.postgresql',
    'sqlalchemy.pool',
    'pymysql',
    'psycopg2',
    'dotenv',
    'flet',
    'flet_core',
]

a = Analysis(
    ['app.py'],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='ExportacaoFortes',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['front\\src\\assets\\icone.ico'] if os.path.exists('front\\src\\assets\\icone.ico') else None,
)