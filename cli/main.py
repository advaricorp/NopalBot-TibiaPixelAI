#!/usr/bin/env python3
"""
Matrix CLI for PBT Bot
Enhanced version with configuration and spells
By Taquito Loco 🎮

- ASCII art Matrix style
- Interactive menu with configuration
- Green/black theme, icons, spinners
- Real-time logs and status
- Compatible Windows/Linux
"""
import sys
import os
import time
import threading
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt, IntPrompt
from rich.text import Text
from rich.live import Live
from rich.spinner import Spinner
from rich.align import Align
from rich import box
from rich.theme import Theme

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from bot.main import PBTBot
    from config.config_manager import ConfigManager
except ImportError as e:
    print(f"[ERROR] No se pudo importar módulos: {e}")
    print("Asegúrate de ejecutar desde la raíz del proyecto")
    sys.exit(1)

ASCII = r'''
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
                                                                                                  
'''

custom_theme = Theme({
    "primary": "bold green",
    "secondary": "white",
    "accent": "bold bright_green",
    "warning": "yellow",
    "error": "bold red",
    "success": "bold green",
    "prompt": "bold bright_green",
    "ascii": "bold green",
    "menu": "bold green",
    "option": "bold white",
    "log": "green",
    "spinner": "green",
})
console = Console(theme=custom_theme)

bot = None
bot_thread = None
bot_running = False
config = ConfigManager()
log_lines = []
log_lock = threading.Lock()

# --- Logging Thread ---
def log_listener():
    global log_lines
    while bot_running:
        if hasattr(bot, 'get_status'):
            status = bot.get_status()
            with log_lock:
                log_lines.append(f"[LOG] Status: {status['profession']} - Health: {status['health']}/{status.get('max_health', 100)}")
        time.sleep(2)

# --- CLI Menu ---
def print_ascii():
    console.print(ASCII, style="ascii")

def main_menu():
    print_ascii()
    menu = Table.grid(padding=1)
    menu.add_column(justify="center", style="menu", width=30)
    menu.add_row("[primary]1.[/primary] Iniciar Bot")
    menu.add_row("[primary]2.[/primary] Detener Bot")
    menu.add_row("[primary]3.[/primary] Estado del Bot")
    menu.add_row("[primary]4.[/primary] Configurar Profesión")
    menu.add_row("[primary]5.[/primary] Configurar Funciones")
    menu.add_row("[primary]6.[/primary] Ver Hechizos")
    menu.add_row("[primary]7.[/primary] Ver Logs")
    menu.add_row("[primary]8.[/primary] Salir")
    console.print(Panel(menu, title="[accent]PBT Bot Matrix CLI[/accent]", border_style="accent", box=box.DOUBLE))

def start_bot():
    global bot, bot_thread, bot_running
    if bot_running:
        console.print("[warning]Bot ya está ejecutándose[/warning]")
        return
    
    with console.status("[spinner]Iniciando bot...", spinner="dots"):
        bot = PBTBot()
        bot_thread = threading.Thread(target=bot.run, daemon=True)
        bot_thread.start()
        bot_running = True
        time.sleep(2)
    
    console.print("[success]✅ Bot iniciado exitosamente[/success]")
    console.print(f"[log]🔮 Profesión: {config.get_setting('bot_settings', 'profession')}[/log]")
    console.print(f"[log]⚔️ Ataque: {config.get_hotkey('attack')}[/log]")
    console.print(f"[log]💰 Loot: {config.get_hotkey('loot')}[/log]")
    console.print(f"[log]🚶 Movimiento: {config.get_setting('bot_settings', 'movement_type')}[/log]")
    console.print(f"[log]🔮 Hechizos: {'HABILITADOS' if config.is_feature_enabled('spells_enabled') else 'DESHABILITADOS'}[/log]")
    console.print("[log]💀 F12 para KILL EMERGENCY[/log]")

def stop_bot():
    global bot, bot_running
    if not bot_running:
        console.print("[warning]Bot no está ejecutándose[/warning]")
        return
    
    with console.status("[spinner]Deteniendo bot...", spinner="dots"):
        bot.stop()
        bot_running = False
        time.sleep(1)
    
    console.print("[success]✅ Bot detenido exitosamente[/success]")

def show_status():
    if bot_running and bot:
        status = bot.get_status()
        status_table = Table(title="Estado del Bot")
        status_table.add_column("Componente", style="primary")
        status_table.add_column("Estado", style="success")
        status_table.add_row("Bot", "🟢 Ejecutándose" if status["running"] else "🛑 Detenido")
        status_table.add_row("Profesión", status["profession"].title())
        status_table.add_row("Salud", f"{status['health']}/{status.get('max_health', 100)}")
        status_table.add_row("Mana", f"{status['mana']}/{status.get('max_mana', 100)}")
        status_table.add_row("Combate", "⚔️ En Combate" if status["in_combat"] else "❌ Sin Combate")
        status_table.add_row("Ataque", "🟢 Activo" if status["features"]["auto_attack"] else "🔴 Inactivo")
        status_table.add_row("Movimiento", "🟢 Activo" if status["features"]["auto_movement"] else "🔴 Inactivo")
        status_table.add_row("Loot", "🟢 Automático" if status["features"]["auto_loot"] else "🔴 Manual")
        status_table.add_row("Hechizos", "🟢 Habilitados" if status["features"]["spells_enabled"] else "🔴 Deshabilitados")
        console.print(status_table)
    else:
        console.print("[warning]Bot no está ejecutándose[/warning]")

def configure_profession():
    professions = config.get_all_professions()
    console.print("[prompt]Profesiones disponibles:[/prompt]")
    for i, prof in enumerate(professions, 1):
        console.print(f"[primary]{i}.[/primary] {prof.title()}")
    
    choice = IntPrompt.ask("Selecciona profesión", choices=[str(i) for i in range(1, len(professions) + 1)])
    selected_profession = professions[choice-1]
    
    config.set_setting("bot_settings", "profession", selected_profession)
    console.print(f"[success]Profesión cambiada a: {selected_profession.title()}[/success]")
    
    # Show spells for selected profession
    spells = config.get_profession_spells(selected_profession)
    console.print(f"\n[prompt]Hechizos de {selected_profession.title()}:[/prompt]")
    for spell_type, spell_list in spells.items():
        console.print(f"[log]{spell_type.title()}:[/log]")
        for spell in spell_list:
            console.print(f"  • {spell}")

def configure_features():
    features = [
        ("Auto Attack", "auto_attack"),
        ("Auto Movement", "auto_movement"),
        ("Auto Loot", "auto_loot"),
        ("Spells Enabled", "spells_enabled"),
        ("Emergency Spells", "emergency_spells"),
    ]
    
    console.print("[prompt]Funciones disponibles:[/prompt]")
    for i, (name, key) in enumerate(features, 1):
        status = "🟢 Habilitado" if config.is_feature_enabled(key) else "🔴 Deshabilitado"
        console.print(f"[primary]{i}.[/primary] {name}: {status}")
    
    choice = IntPrompt.ask("Selecciona función para cambiar", choices=[str(i) for i in range(1, len(features) + 1)])
    selected_feature = features[choice-1]
    
    current = config.is_feature_enabled(selected_feature[1])
    config.set_setting("bot_settings", selected_feature[1], not current)
    
    new_status = "HABILITADA" if not current else "DESHABILITADA"
    console.print(f"[success]Función {selected_feature[0]} {new_status}[/success]")

def show_spells():
    profession = config.get_setting("bot_settings", "profession")
    spells = config.get_profession_spells(profession)
    
    console.print(f"[prompt]Hechizos de {profession.title()}:[/prompt]")
    for spell_type, spell_list in spells.items():
        console.print(f"\n[log]{spell_type.title()}:[/log]")
        for spell in spell_list:
            console.print(f"  • {spell}")

def view_logs():
    if not log_lines:
        console.print("[warning]No hay logs disponibles[/warning]")
        return
    
    console.print("[prompt]Últimos logs:[/prompt]")
    for line in log_lines[-10:]:  # Show last 10 logs
        console.print(f"[log]{line}[/log]")

def main():
    global bot_running
    
    while True:
        try:
            main_menu()
            choice = Prompt.ask("Selecciona una opción", choices=["1", "2", "3", "4", "5", "6", "7", "8"])
            
            if choice == "1":
                start_bot()
            elif choice == "2":
                stop_bot()
            elif choice == "3":
                show_status()
            elif choice == "4":
                configure_profession()
            elif choice == "5":
                configure_features()
            elif choice == "6":
                show_spells()
            elif choice == "7":
                view_logs()
            elif choice == "8":
                if bot_running:
                    stop_bot()
                console.print("[success]¡Hasta luego! 👋[/success]")
                break
            
            if choice != "8":
                Prompt.ask("\nPresiona Enter para continuar")
                console.clear()
                
        except KeyboardInterrupt:
            console.print("\n[warning]Interrupción detectada[/warning]")
            if bot_running:
                stop_bot()
            break
        except Exception as e:
            console.print(f"[error]Error: {e}[/error]")

if __name__ == "__main__":
    main() 