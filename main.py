#!/usr/bin/env python3
"""
PBT Bot - Main Entry Point
By Taquito Loco 🎮

Choose your interface:
1. CLI Matrix Style
2. GUI Moderna
3. Direct Bot Execution
"""

import sys
import os

def print_banner():
    """Print the project banner"""
    banner = """
████████╗ █████╗  ██████╗ ██╗   ██╗██╗████████╗ ██████╗     ██╗      ██████╗  ██████╗ ██████╗     
╚══██╔══╝██╔══██╗██╔═══██╗██║   ██║██║╚══██╔══╝██╔═══██╗    ██║     ██╔═══██╗██╔════╝██╔═══██╗    
   ██║   ███████║██║   ██║██║   ██║██║   ██║   ██║   ██║    ██║     ██║   ██║██║     ██║   ██║    
   ██║   ██╔══██║██║▄▄ ██║██║   ██║██║   ██║   ██║   ██║    ██║     ██║   ██║██║     ██║   ██║    
   ██║   ██║  ██║╚██████╔╝╚██████╔╝██║   ██║   ╚██████╔╝    ███████╗╚██████╔╝╚██████╗╚██████╔╝    
   ╚═╝   ╚═╝  ╚═╝ ╚══▀▀═╝  ╚═════╝ ╚═╝   ╚═╝    ╚═════╝     ╚══════╝ ╚═════╝  ╚═════╝ ╚═════╝     
                                                                                                  
███████╗██╗  ██╗██╗   ██╗███╗   ██╗██╗  ██╗    ██╗    ██╗ ██████╗ ██████╗ ██╗  ██╗███████╗        
██╔════╝██║ ██╔╝██║   ██║████╗  ██║██║ ██╔╝    ██║    ██║██╔═══██╗██╔══██╗██║ ██╔╝██╔════╝        
███████╗█████╔╝ ██║   ██║██╔██╗ ██║█████╔╝     ██║ █╗ ██║██║   ██║██████╔╝█████╔╝ ███████╗        
╚════██║██╔═██╗ ██║   ██║██║╚██╗██║██╔═██╗     ██║███╗██║██║   ██║██╔══██╗██╔═██╗ ╚════██║        
███████║██║  ██╗╚██████╔╝██║ ╚████║██║  ██╗    ╚███╔███╔╝╚██████╔╝██║  ██║██║  ██╗███████║        
╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝╚═╝  ╚═╝     ╚══╝╚══╝  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝        
                                                                                                  
    """
    print(banner)
    print("🤖 PBT Bot - By Taquito Loco 🎮")
    print("=" * 60)

def show_menu():
    """Show the main menu"""
    print("\n🎮 SELECCIONA TU INTERFAZ:")
    print("1. 🖥️  CLI Matrix Style (Línea de comandos)")
    print("2. 🖼️  GUI Moderna (Interfaz gráfica)")
    print("3. ⚡ Bot Directo (Ejecución directa)")
    print("4. 🧪 Ejecutar Tests")
    print("5. 🔨 Compilar Ejecutables")
    print("6. 📖 Ver Documentación")
    print("7. 🚪 Salir")

def run_cli():
    """Run the CLI interface"""
    print("\n🖥️ Iniciando CLI Matrix Style...")
    try:
        from cli.main import main as cli_main
        cli_main()
    except ImportError as e:
        print(f"❌ Error importando CLI: {e}")
        print("Asegúrate de que todos los módulos estén instalados")

def run_gui():
    """Run the GUI interface"""
    print("\n🖼️ Iniciando GUI Moderna...")
    try:
        from gui.main import main as gui_main
        gui_main()
    except ImportError as e:
        print(f"❌ Error importando GUI: {e}")
        print("Asegúrate de que todos los módulos estén instalados")

def run_bot_direct():
    """Run the bot directly"""
    print("\n⚡ Iniciando Bot Directo...")
    try:
        from bot.main import main as bot_main
        bot_main()
    except ImportError as e:
        print(f"❌ Error importando Bot: {e}")
        print("Asegúrate de que todos los módulos estén instalados")

def run_tests():
    """Run the test suite"""
    print("\n🧪 Ejecutando Tests...")
    try:
        from tests.test_bot import main as test_main
        test_main()
    except ImportError as e:
        print(f"❌ Error importando Tests: {e}")
        print("Asegúrate de que todos los módulos estén instalados")

def build_executables():
    """Build all executables"""
    print("\n🔨 Compilando Ejecutables...")
    try:
        from scripts.build_all_executables import main as build_main
        build_main()
    except ImportError as e:
        print(f"❌ Error importando Build Script: {e}")
        print("Asegúrate de que todos los módulos estén instalados")

def show_documentation():
    """Show documentation"""
    print("\n📖 DOCUMENTACIÓN:")
    print("=" * 40)
    print("📄 README.md - Documentación principal del proyecto")
    print("🔮 SPELLS_FIXED_SOLUTION.md - Solución sin hechizos")
    print("\n📁 ESTRUCTURA DEL PROYECTO:")
    print("   • bot/ - Lógica principal del bot")
    print("   • cli/ - Interfaz de línea de comandos")
    print("   • gui/ - Interfaz gráfica")
    print("   • scripts/ - Scripts de utilidad")
    print("   • tests/ - Tests del proyecto")
    print("   • utils/ - Utilidades del bot")
    print("\n🎮 CARACTERÍSTICAS DEL BOT:")
    print("   • 🔮 SIN HECHIZOS - Solo ataque físico (SPACE)")
    print("   • 🚶 MOVIMIENTO CONSTANTE - WASD automático")
    print("   • 🪜 DETECCIÓN DE ESCALERAS - Movimiento vertical")
    print("   • 💰 LOOT AUTOMÁTICO - F4")
    print("   • 💀 F12 para KILL EMERGENCY")

def main():
    """Main function"""
    while True:
        try:
            print_banner()
            show_menu()
            
            choice = input("\n🎯 Selecciona una opción (1-7): ").strip()
            
            if choice == "1":
                run_cli()
            elif choice == "2":
                run_gui()
            elif choice == "3":
                run_bot_direct()
            elif choice == "4":
                run_tests()
            elif choice == "5":
                build_executables()
            elif choice == "6":
                show_documentation()
                input("\nPresiona Enter para continuar...")
            elif choice == "7":
                print("\n👋 ¡Hasta luego! By Taquito Loco 🎮")
                break
            else:
                print("❌ Opción inválida. Selecciona 1-7.")
                input("Presiona Enter para continuar...")
            
            # Clear screen for next iteration
            os.system('cls' if os.name == 'nt' else 'clear')
            
        except KeyboardInterrupt:
            print("\n\n👋 ¡Hasta luego! By Taquito Loco 🎮")
            break
        except Exception as e:
            print(f"\n❌ Error inesperado: {e}")
            input("Presiona Enter para continuar...")

if __name__ == "__main__":
    main() 