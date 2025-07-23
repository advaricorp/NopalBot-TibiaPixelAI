import os
import sys
import subprocess
import shutil
from pathlib import Path

def build_executable():
    """Compilar el bot final en un ejecutable"""
    
    print("🚀 Building NopalBot Final Executable...")
    
    # Verificar que PyInstaller esté instalado
    try:
        import PyInstaller
        print("✅ PyInstaller found")
    except ImportError:
        print("❌ PyInstaller not found. Installing...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # Crear archivo spec personalizado
    spec_content = '''# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['nopalbot_final.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[
        'customtkinter',
        'cv2',
        'numpy',
        'pyautogui',
        'keyboard',
        'win32gui',
        'win32con',
        'win32api',
        'PIL',
        'psutil'
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
    name='NopalBot_Final',
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
    icon=None,
)
'''
    
    # Escribir archivo spec
    with open('NopalBot_Final.spec', 'w') as f:
        f.write(spec_content)
    
    print("📝 Spec file created")
    
    # Compilar con PyInstaller
    print("🔨 Compiling executable...")
    result = subprocess.run([
        sys.executable, "-m", "PyInstaller",
        "--clean",
        "--onefile",
        "--windowed",
        "--name=NopalBot_Improved",
        "nopalbot_final.py"
    ], capture_output=True, text=True)
    
    if result.returncode == 0:
        print("✅ Compilation successful!")
        
        # Verificar que el ejecutable existe
        exe_path = Path("dist/NopalBot_Improved.exe")
        if exe_path.exists():
            print(f"🎉 Executable created: {exe_path}")
            
            # Crear archivo batch para ejecutar
            batch_content = '''@echo off
title NopalBot Improved - Complete Edition
echo.
echo ========================================
echo    NOPALBOT IMPROVED - COMPLETE EDITION
echo ========================================
echo.
echo Starting NopalBot...
echo.
echo Controls:
echo - F11: Pause/Resume
echo - F12: Stop Bot
echo.
echo Make sure Tibia is running!
echo.
pause
NopalBot_Improved.exe
pause
'''
            
            with open("dist/LAUNCH_NOPALBOT_IMPROVED.bat", 'w', encoding='utf-8') as f:
                f.write(batch_content)
            
            print("📄 Launch script created: dist/LAUNCH_NOPALBOT_IMPROVED.bat")
            
            # Crear README
            readme_content = '''# 🤖 NopalBot Improved - Complete Edition

## 🚀 How to Use

1. **Make sure Tibia is running**
2. **Double-click `LAUNCH_NOPALBOT_IMPROVED.bat`** or `NopalBot_Improved.exe`
3. **Configure your Tibia hotkeys** (see below)
4. **Click "START BOT"** in the GUI
5. **Use F11 to pause/resume, F12 to stop**

## ⌨️ Required Tibia Hotkeys

Configure these hotkeys in your Tibia client:

- **K** → Attack
- **F1** → Health Potion
- **F2** → Mana Potion  
- **F3** → Spell 1 (Exori vis for Druid)
- **F4** → Spell 2 (Exura for Druid)
- **F5** → Loot
- **0** → Quick Loot Nearby Corpses
- **WASD** → Movement
- **CTRL** → Face Enemy

## 🎮 Bot Features

- ✅ **Intelligent Healing** (random thresholds 20-40%)
- ✅ **Intelligent Mana Management** (random thresholds 20-40%)
- ✅ **Visual Enemy Detection** (red/brown colors)
- ✅ **Automatic Attack** (clicks enemy + presses K)
- ✅ **Smart Spell Casting** (only if mana > 60%)
- ✅ **Quick Loot Automation** (1 second after enemy death)
- ✅ **Smart WASD Movement** (detects obstacles and avoids them)
- ✅ **Transparent Overlay** (real-time status)
- ✅ **Character Detection** (name and vocation)
- ✅ **Potion Detection** (stops using when out of potions)
- ✅ **Real Health/Mana Detection** (from screen)
- ✅ **Pause/Resume** (F11)
- ✅ **Emergency Stop** (F12)

## 🔧 Troubleshooting

- **Bot not clicking**: Make sure Tibia window is active
- **Not detecting enemies**: Check if enemies are visible on screen
- **Not healing**: Verify F1 hotkey is set to health potion
- **Not using spells**: Check F3/F4 hotkeys and mana threshold
- **Movement issues**: Bot automatically detects and avoids obstacles

## 📊 Overlay

The transparent overlay shows real-time bot status in the top-right corner.
Toggle it with the "TOGGLE OVERLAY" button.

## 🛡️ Safety

- Bot only clicks within Tibia window
- F12 stops bot immediately
- F11 pauses for manual control
- All actions are logged for monitoring
- Smart movement prevents getting stuck

---
**Created with ❤️ for Tibia players**
'''
            
            with open("dist/README_NOPALBOT_IMPROVED.txt", 'w', encoding='utf-8') as f:
                f.write(readme_content)
            
            print("📖 README created: dist/README_NOPALBOT_IMPROVED.txt")
            
            print("\n🎉 BUILD COMPLETED SUCCESSFULLY!")
            print("📁 Check the 'dist' folder for:")
            print("   - NopalBot_Improved.exe")
            print("   - LAUNCH_NOPALBOT_IMPROVED.bat")
            print("   - README_NOPALBOT_IMPROVED.txt")
            
        else:
            print("❌ Executable not found after compilation")
            
    else:
        print("❌ Compilation failed!")
        print("Error:", result.stderr)

if __name__ == "__main__":
    build_executable() 