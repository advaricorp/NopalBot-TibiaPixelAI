#!/usr/bin/env python3
"""
Script para crear acceso directo al ejecutable del Tibia Bot
"""
import os
import sys
import platform
from pathlib import Path

def create_shortcut():
    """Crear acceso directo al ejecutable"""
    print("🔗 Creando acceso directo al Tibia Bot...")
    
    # Verificar si existe el ejecutable
    exe_path = Path("dist/TibiaBot.exe")
    if not exe_path.exists():
        print("❌ Ejecutable no encontrado. Ejecuta build_exe.bat primero.")
        return False
    
    # Obtener ruta del escritorio
    desktop = Path.home() / "Desktop"
    if not desktop.exists():
        print("❌ No se pudo encontrar el escritorio")
        return False
    
    # Crear acceso directo
    shortcut_path = desktop / "Tibia Bot.lnk"
    
    if platform.system().lower() == "windows":
        try:
            import winshell
            from win32com.client import Dispatch
            
            shell = Dispatch('WScript.Shell')
            shortcut = shell.CreateShortCut(str(shortcut_path))
            shortcut.Targetpath = str(exe_path.absolute())
            shortcut.WorkingDirectory = str(Path.cwd().absolute())
            shortcut.IconLocation = str(exe_path.absolute())
            shortcut.save()
            
            print(f"✅ Acceso directo creado: {shortcut_path}")
            return True
            
        except ImportError:
            print("⚠️  No se pudo crear acceso directo automático")
            print(f"💡 Copia manualmente: {exe_path.absolute()}")
            return False
        except Exception as e:
            print(f"❌ Error creando acceso directo: {e}")
            return False
    else:
        print("⚠️  Creación de acceso directo solo disponible en Windows")
        print(f"💡 Copia manualmente: {exe_path.absolute()}")
        return False

if __name__ == "__main__":
    create_shortcut() 