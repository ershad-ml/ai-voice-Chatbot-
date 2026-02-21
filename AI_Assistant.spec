# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['ui\\main_window.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('assets', 'assets'),
        ('dataset', 'dataset'),
        ('encodings', 'encodings'),
        ('face', 'face'),
        ('voice', 'voice'),
        ('ui', 'ui'),
        ('chatbot', 'chatbot'),
        ('chatbot_api.py', '.'),
        ('haarcascade_frontalface_default.xml', '.'),
        ('face_recognition_models', 'face_recognition_models'),
    ],

    hiddenimports=[
        'face_recognition',
        'cv2',
        'numpy',
        'sklearn',
        'speech_recognition',
        'pyttsx3',
        'chatbot_api',
    ],

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
    name='AI_Assistant',
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
)
