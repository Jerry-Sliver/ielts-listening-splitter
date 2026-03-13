#!/usr/bin/env python3
"""
打包雅思听力切分工具为exe
"""

import os
import sys
import shutil
from pathlib import Path


def build_exe():
    print("🎧 开始打包雅思听力切分工具...")
    
    # 检查PyInstaller是否安装
    try:
        import PyInstaller
    except ImportError:
        print("❌ PyInstaller未安装，正在安装...")
        os.system("pip install pyinstaller")
    
    # 创建打包脚本
    spec_content = '''# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['ielts_audio_splitter.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('README.md', '.'),
        ('requirements.txt', '.'),
    ],
    hiddenimports=[
        'whisper',
        'pydub',
        'openai_whisper',
    ],
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
    name='ielts_listening_splitter',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,
)
'''
    
    with open('build.spec', 'w', encoding='utf-8') as f:
        f.write(spec_content)
    
    print("📝 已创建打包配置文件")
    
    # 执行打包
    print("🚀 开始打包（这可能需要几分钟）...")
    cmd = "pyinstaller --onefile --name ielts_listening_splitter ielts_audio_splitter.py"
    print(f"执行命令: {cmd}")
    os.system(cmd)
    
    # 检查是否成功
    if os.path.exists('dist/ielts_listening_splitter.exe') or os.path.exists('dist/ielts_listening_splitter'):
        print("\n✅ 打包成功！")
        print(f"📦 可执行文件位置: dist/")
        
        # 复制其他文件到dist目录
        dist_path = Path('dist')
        files_to_copy = [
            'generate_html_player.py',
            'run_ielts_split.sh',
            'requirements.txt',
            'README.md',
        ]
        
        for file in files_to_copy:
            if os.path.exists(file):
                shutil.copy2(file, dist_path / file)
                print(f"   已复制: {file}")
        
        print("\n🎉 全部完成！")
        print("dist/ 目录下包含所有需要的文件")
    else:
        print("\n❌ 打包可能失败，请检查输出")


if __name__ == '__main__':
    build_exe()
