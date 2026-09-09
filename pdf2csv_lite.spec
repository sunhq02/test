# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['pdf2csv.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=['pymupdf'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    # 排除一切用不到的模块
    excludes=[
        # 多进程/调试
        'multiprocessing', 'concurrent.futures',
        # GUI
        'tkinter', 'Qt5', 'PyQt', 'PySide', 'wx',
        # 数值计算/ML
        'numpy', 'scipy', 'pandas', 'matplotlib', 'seaborn',
        'torch', 'tensorflow', 'keras',
        # Web/网络
        'http', 'urllib', 'requests', 'selenium', 'scrapy',
        # 数据库
        'sqlite3', 'mysql', 'psycopg', 'sqlalchemy',
        # 测试文档
        'unittest', 'doctest', 'pytest', 'pydoc',
        # 终端交互
        'curses', 'prompt_toolkit',
        # Jupyter/IPython
        'IPython', 'jupyter', 'notebook',
        # 加密/安全（除非明确需要）
        'cryptography', 'paramiko',
        # PDF 扩展功能（只保留核心）
        'fontTools',  # fontTools 是 pymupdf 的子集依赖，会极大膨胀
        # image processing
        'PIL', 'Pillow',
        # 其他不需要的
        'xml.etree.ElementInclude', 'lxml',
    ],
    noarchive=False,
    optimize=1,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='pdf2csv',
    debug=False,
    bootloader_ignore_signals=False,
    strip=True,
    upx=False,  # 先用非压缩模式看大小
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
