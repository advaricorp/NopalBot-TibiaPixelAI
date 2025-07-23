"""
Build All Executables Script
Compiles all bot versions into executables
By Taquito Loco 🎮
"""

import os
import sys
import subprocess
import shutil
import time
from pathlib import Path

def clean_dist():
    """Clean dist directory"""
    dist_path = Path("dist")
    if dist_path.exists():
        print("🧹 Limpiando directorio dist...")
        shutil.rmtree(dist_path)
        time.sleep(1)
    print("✅ Directorio dist limpiado")

def build_executable(script_path: str, exe_name: str, icon_path: str = None):
    """Build a single executable"""
    print(f"🔨 Compilando {exe_name}...")
    
    # Use sys.executable to get the correct Python path
    python_exe = sys.executable
    
    # Base PyInstaller command
    cmd = [python_exe, "-m", "PyInstaller", "--onefile", "--noconsole"]
    
    # Add icon if provided
    if icon_path and os.path.exists(icon_path):
        cmd.extend(["--icon", icon_path])
    
    # Add script path and output name
    cmd.extend(["--name", exe_name, script_path])
    
    try:
        print(f"Ejecutando: {' '.join(cmd)}")
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        print(f"✅ {exe_name} compilado exitosamente")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error compilando {exe_name}: {e}")
        if e.stdout:
            print(f"STDOUT: {e.stdout}")
        if e.stderr:
            print(f"STDERR: {e.stderr}")
        return False
    except Exception as e:
        print(f"❌ Error inesperado compilando {exe_name}: {e}")
        return False

def create_launcher_bat(exe_name: str, launcher_name: str, description: str):
    """Create a launcher .bat file"""
    bat_content = f"""@echo off
REM {description}
REM By Taquito Loco 🎮

echo.
echo   {description}
echo ========================================
echo.

REM Verificar si el ejecutable existe
if not exist "{exe_name}.exe" (
    echo ERROR: No se encuentra {exe_name}.exe
    echo Asegúrate de que el archivo esté en el mismo directorio
    pause
    exit /b 1
)

echo Iniciando {exe_name}...
echo.

REM Ejecutar el bot
start "" "{exe_name}.exe"

echo {exe_name} iniciado correctamente!
echo.
pause
"""
    
    bat_path = f"dist/{launcher_name}.bat"
    with open(bat_path, "w", encoding="utf-8") as f:
        f.write(bat_content)
    
    print(f"✅ Launcher {launcher_name}.bat creado")

def main():
    """Main build function"""
    print("🚀 INICIANDO COMPILACIÓN DE TODOS LOS EJECUTABLES")
    print("=" * 50)
    
    # Clean dist directory
    clean_dist()
    
    # Create dist directory
    os.makedirs("dist", exist_ok=True)
    
    # Build configurations
    builds = [
        {
            "script": "bot/main.py",
            "exe_name": "NoSpellsBotImproved",
            "launcher": "LAUNCH_IMPROVED",
            "description": "No Spells Improved Bot - By Taquito Loco 🎮"
        },
        {
            "script": "cli/main.py",
            "exe_name": "TibiaBotCLI",
            "launcher": "LAUNCH_CLI",
            "description": "Tibia Bot CLI Matrix Style - By Taquito Loco 🎮"
        },
        {
            "script": "gui/main.py",
            "exe_name": "TibiaBotGUI",
            "launcher": "LAUNCH_GUI",
            "description": "Tibia Bot GUI Moderna - By Taquito Loco 🎮"
        }
    ]
    
    successful_builds = 0
    failed_builds = 0
    
    # Build each executable
    for build in builds:
        script_path = build["script"]
        exe_name = build["exe_name"]
        launcher_name = build["launcher"]
        description = build["description"]
        
        # Check if script exists
        if not os.path.exists(script_path):
            print(f"❌ Script no encontrado: {script_path}")
            failed_builds += 1
            continue
        
        # Build executable
        if build_executable(script_path, exe_name):
            # Create launcher
            create_launcher_bat(exe_name, launcher_name, description)
            successful_builds += 1
        else:
            failed_builds += 1
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 RESUMEN DE COMPILACIÓN")
    print("=" * 50)
    print(f"✅ Ejecutables compilados exitosamente: {successful_builds}/{len(builds)}")
    
    if failed_builds > 0:
        print(f"⚠️ {failed_builds} ejecutables fallaron en la compilación")
        print("Revisa los errores arriba y vuelve a intentar")
    else:
        print("🎉 ¡Todos los ejecutables compilados exitosamente!")
        print("\n📁 Los ejecutables están en el directorio 'dist'")
        print("🚀 Usa los archivos .bat para ejecutar cada versión")

if __name__ == "__main__":
    main() 