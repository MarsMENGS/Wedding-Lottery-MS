# -*- mode: python ; coding: utf-8 -*-
import sys
import os
sys.setrecursionlimit(5000)

block_cipher = None
BASE_PATH = os.path.abspath('.')

# Qt插件路径（仅保留发布版插件，删除调试版）
QT_PLUGIN_PATH = r'C:\Users\ll\AppData\Local\Programs\Python\Python314\Lib\site-packages\PySide6\plugins\platforms'

a = Analysis(
    ['main.py'],  # 入口文件
    pathex=[BASE_PATH],  # 项目根目录
    binaries=[
        # ========== 关键：只保留发布版 qwindows.dll，删除 qwindowsd.dll ==========
        (os.path.join(QT_PLUGIN_PATH, 'qwindows.dll'), 'platforms'),
    ],
    datas=[
        # 打包所有资源和模块
        (os.path.join(BASE_PATH, 'resources'), 'resources'),
        (os.path.join(BASE_PATH, 'lottery_config_example.json'), '.'),
        (QT_PLUGIN_PATH, 'platforms'),  # 打包整个platforms文件夹（含qwindows.dll）
        (os.path.join(BASE_PATH, 'utils'), 'utils'),
        (os.path.join(BASE_PATH, 'core'), 'core'),
        (os.path.join(BASE_PATH, 'ui'), 'ui'),
    ],
    hiddenimports=[
        # Qt核心模块
        'PySide6.QtCore', 'PySide6.QtGui', 'PySide6.QtWidgets',
        # 自定义模块
        'core.lottery_engine',
        'core.number_validator',
        'utils.resource_path',
        'ui.main_window', 'ui.animated_label', 'ui.confetti_widget',
        'ui.draw_page', 'ui.rounded_card', 'ui.setup_page',
        'ui.side_menu', 'ui.summary_page'
    ],
    excludes=[
        # 排除无用模块，减小体积
        'PySide6.QtWebEngine', 'PySide6.QtMultimedia', 'PySide6.QtBluetooth',
        'tkinter', 'unittest'
    ],
    win_no_prefer_redirects=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

# EXE配置（COLLECT模式专用）
exe = EXE(
    pyz,
    a.scripts,
    [],  # COLLECT模式下留空
    exclude_binaries=True,
    name='婚礼抽奖系统',
    debug=False,  # 关闭调试模式（打包发布版）
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=True,  # 保留控制台，方便查看日志
    target_arch='x64',
    icon=os.path.join(BASE_PATH, 'resources/logo.ico'),
)

# 文件夹模式打包（核心！）
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=False,
    name='婚礼抽奖系统',
)