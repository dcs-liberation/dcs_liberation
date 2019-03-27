# -*- mode: python -*-

block_cipher = None


a = Analysis(['__init__.py'],
             pathex=['C:\\Users\\shdwp\\PycharmProjects\\dcs_liberation'],
             binaries=[],
             datas=[
             ('resources', 'resources'),
             ('submodules/dcs/dcs/terrain/caucasus.p', 'dcs/terrain/'),
             ('submodules/dcs/dcs/terrain/nevada.p', 'dcs/terrain/'),
             ],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          icon="resources/icon.ico",
          exclude_binaries=True,
          name='liberation_main',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='dcs_liberation')
