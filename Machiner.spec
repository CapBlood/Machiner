# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


def get_pandas_path():
    import pandas
    pandas_path = pandas.__path__[0]
    return pandas_path


a = Analysis(['machiner/__main__.py'],
             pathex=['/Users/donsangre/Documents/Place for chill/Workspace/Python/Machiner'],
             binaries=[],
             datas=[('machiner/app/design.qss', 'app/')],
             hiddenimports=['pkg_resources.py2_warn', 'pandas', 'sklearn', 'numpy', 'pytz', 'dateutil', 'scipy.special.cython_special',
                            'sklearn.utils._cython_blas', 'sklearn.neighbors._typedefs', 'sklearn.neighbors.quad_tree',
                            'sklearn.tree._utils'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)


dict_tree = Tree(get_pandas_path(), prefix='pandas', excludes=["*.pyc"])
a.datas += dict_tree
a.binaries = filter(lambda x: 'pandas' not in x[0], a.binaries)


pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='Machiner',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='Machiner')
app = BUNDLE(coll,
             name='Machiner.app',
             icon=None,
             bundle_identifier=None)
