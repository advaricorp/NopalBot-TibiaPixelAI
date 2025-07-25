#!/usr/bin/env python3
"""
Build Script for NopalBot Improved
"""

import subprocess
import os
from pathlib import Path

def build_executable():
    print("🚀 Building NopalBot Improved Executable...")
    
    # Crear spec file
    spec_content = '''# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['nopalbot_simple.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=['win32gui', 'win32con', 'keyboard', 'pyautogui', 'customtkinter'],
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
    name='NopalBot_Improved',
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
    icon=None
)
'''
    
    with open("nopalbot_improved.spec", "w") as f:
        f.write(spec_content)
    
    print("📝 Spec file created")
    
    # Compilar ejecutable
    print("🔨 Compiling executable...")
    result = subprocess.run([
        "python", "-m", "PyInstaller",
        "--name=NopalBot_Improved",
        "nopalbot_simple.py"
    ], capture_output=True, text=True)
    
    if result.returncode == 0:
        print("✅ Compilation successful!")
        
        # Verificar que el ejecutable existe
        exe_path = Path("dist/NopalBot_Improved.exe")
        if exe_path.exists():
            print(f"🎉 Executable created: {exe_path}")
            
            # Crear archivo batch para ejecutar
            batch_content = '''@echo off
title NopalBot Improved - Auto Attack, Walk & Heal
echo.
echo ========================================
echo    NOPALBOT IMPROVED - FULL FEATURES
echo ========================================
echo.
echo Starting NopalBot Improved...
echo.
echo Features:
echo - Auto Attack (CTRL+SPACE)
echo - Smart Auto Walk (WASD with wall detection)
echo - Auto Heal (Spell or Potion at 40%% HP)
echo - Rune Casting (F11 + R key)
echo - Stair Avoidance
echo - F11 to pause/resume + cast runes
echo - F10 to stop
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
            readme_content = '''# 🤖 NopalBot Improved - Full Features

## 🚀 How to Use

1. **Make sure Tibia is running**
2. **Double-click `LAUNCH_NOPALBOT_IMPROVED.bat`** or `NopalBot_Improved.exe`
3. **Configure your Tibia hotkeys** (see below)
4. **Enable desired features** in the GUI
5. **Click "START BOT"**
6. **Use F11 to pause/resume + cast runes, F10 to stop**

## ⌨️ Required Tibia Hotkeys

Configure these hotkeys in your Tibia client:

- **SPACE** → Next Target
- **CTRL + SPACE** → Attack
- **F3** → Healing Spell (Exura for Druid)
- **F1** → Health Potion
- **R** → Rune Casting
- **WASD** → Movement

## 🎮 Features

- ✅ **Auto Attack** (SPACE + CTRL+SPACE)
- ✅ **Smart Auto Walk** (WASD with wall detection)
- ✅ **Auto Heal** (Spell or Potion at 40% HP)
- ✅ **Rune Casting** (F11 + R key for extra damage)
- ✅ **Stair Avoidance** (prevents going up/down stairs)
- ✅ **Wall Detection** (changes direction when stuck)
- ✅ **Continuous Movement** (never stops unless enemies)
- ✅ **Transparent Overlay** (real-time status)
- ✅ **Pause/Resume** (F11)
- ✅ **Emergency Stop** (F10)

## 🚶 Smart Walk System

The bot uses intelligent movement:
- **Starts moving South (S)**
- **Auto direction change** every 15 seconds
- **If stuck for 3 seconds**: Changes direction
- **Stair avoidance**: Prevents going up/down
- **Movement speed**: Every 0.8 seconds
- **Never stops moving** unless enemies are present

## ❤️ Auto Heal System

- **Triggers at 40% HP**
- **Two healing methods**:
  - **Spell (F3)**: Uses Exura if mana > 60%
  - **Potion (F1)**: Uses health potion
- **2-second cooldown** between heals
- **Priority over other actions**

## 💎 Rune Casting

- **F11 key**: Pause/resume + cast runes
- **R key**: Casts runes at target
- **Only if mana > 60%**
- **1-second cooldown** between runes
- **Automatic after attacks**

## 🚫 Stair Avoidance

The bot automatically avoids stairs:
- **Detects W/S movements** (up/down)
- **Changes to A/D** (left/right) instead
- **Prevents level changes**
- **Keeps you on same floor**

## 🔧 Troubleshooting

- **Bot not clicking**: Make sure Tibia window is active
- **Not moving**: Check if WASD hotkeys are set in Tibia
- **Not attacking**: Verify SPACE and CTRL+SPACE hotkeys
- **Not healing**: Check F3 (spell) or F1 (potion) hotkeys
- **Not casting runes**: Verify R hotkey is set
- **Movement issues**: Bot automatically detects and avoids obstacles

## 📊 Overlay

The transparent overlay shows real-time bot status in the top-right corner.
Toggle it with the "SHOW OVERLAY" button.

## 🛡️ Safety

- Bot only clicks within Tibia window
- F10 stops bot immediately
- F11 pauses for manual control
- All actions are logged for monitoring
- Smart movement prevents getting stuck
- Stair avoidance prevents level changes

---
**Created with ❤️ for Tibia players - Full featured and safe!**
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