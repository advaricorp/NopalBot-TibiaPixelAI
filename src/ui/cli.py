"""
Tibia Bot - CLI Interface
By Taquito Loco 🎮

Command Line Interface for the Tibia Bot with all features.
"""

import sys
import os
import time
import threading
import logging
from pathlib import Path

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from vision.screen_reader import ScreenReader
from control.keyboard_controller import KeyboardController
from control.mouse_controller import MouseController
from features.auto_attack import AutoAttack
from features.auto_spell import AutoSpell
from features.auto_loot import AutoLoot
from features.auto_walk import AutoWalk

logger = logging.getLogger(__name__)

class TibiaBotCLI:
    """
    Command Line Interface for Tibia Bot.
    
    Features:
    - Auto-Attack
    - Auto-Spell
    - Auto-Loot
    - Auto-Walk
    - Status monitoring
    - Configuration
    """
    
    def __init__(self):
        """Initialize CLI interface."""
        self.running = False
        self.screen_reader = None
        self.keyboard = None
        self.mouse = None
        
        # Feature instances
        self.auto_attack = None
        self.auto_spell = None
        self.auto_loot = None
        self.auto_walk = None
        
        # Status
        self.features_status = {
            "auto_attack": False,
            "auto_spell": False,
            "auto_loot": False,
            "auto_walk": False
        }
        
        self.setup_logging()
    
    def setup_logging(self):
        """Setup logging configuration."""
        logging.basicConfig(
            level=logging.INFO,
            format='[%(asctime)s] [%(levelname)s] %(message)s',
            handlers=[
                logging.FileHandler('bot_cli.log', encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
    
    def initialize_systems(self):
        """Initialize all bot systems."""
        try:
            print("🔧 Inicializando sistemas...")
            
            # Initialize screen reader
            self.screen_reader = ScreenReader("Tibia")
            if not self.screen_reader.find_window():
                print("❌ No se encontró la ventana de Tibia")
                return False
            
            window_info = self.screen_reader.get_window_info()
            print(f"✅ Ventana de Tibia encontrada: {window_info.title}")
            
            if not self.screen_reader.start_capture():
                print("❌ No se pudo iniciar captura de pantalla")
                return False
            
            # Initialize controllers
            self.keyboard = KeyboardController("Tibia")
            self.mouse = MouseController("Tibia")
            
            # Initialize features
            self.auto_attack = AutoAttack(self.screen_reader, self.keyboard, self.mouse)
            self.auto_spell = AutoSpell(self.keyboard)
            self.auto_loot = AutoLoot(self.screen_reader, self.mouse, self.keyboard)
            self.auto_walk = AutoWalk(self.keyboard)
            
            print("✅ Todos los sistemas inicializados")
            return True
            
        except Exception as e:
            print(f"❌ Error inicializando sistemas: {e}")
            return False
    
    def show_menu(self):
        """Show main menu."""
        print("\n" + "="*60)
        print("🎮 TIBIA BOT - INTERFAZ DE LÍNEA DE COMANDOS")
        print("="*60)
        print("By Taquito Loco 🎮")
        print()
        
        print("📋 FUNCIONALIDADES:")
        print("1. ⚔️  Auto-Attack")
        print("2. 🔮 Auto-Spell")
        print("3. 💰 Auto-Loot")
        print("4. 🚶 Auto-Walk")
        print("5. 🎯 Todas las funcionalidades")
        print("6. 📊 Estado del bot")
        print("7. ⚙️  Configuración")
        print("8. 🛑 Detener todo")
        print("9. ❌ Salir")
        print()
    
    def handle_auto_attack(self):
        """Handle auto-attack menu."""
        while True:
            print("\n⚔️ AUTO-ATTACK")
            print("-" * 20)
            print("1. Iniciar auto-attack")
            print("2. Detener auto-attack")
            print("3. Configurar teclas")
            print("4. Estado")
            print("5. Volver")
            
            choice = input("\nElige una opción (1-5): ").strip()
            
            if choice == "1":
                if self.auto_attack.start():
                    self.features_status["auto_attack"] = True
                    print("✅ Auto-attack iniciado")
                else:
                    print("❌ Error iniciando auto-attack")
            
            elif choice == "2":
                self.auto_attack.stop()
                self.features_status["auto_attack"] = False
                print("✅ Auto-attack detenido")
            
            elif choice == "3":
                self.configure_auto_attack()
            
            elif choice == "4":
                status = self.auto_attack.get_status()
                print(f"Estado: {'🟢 Activo' if status['running'] else '🔴 Inactivo'}")
            
            elif choice == "5":
                break
            
            else:
                print("❌ Opción inválida")
    
    def handle_auto_spell(self):
        """Handle auto-spell menu."""
        while True:
            print("\n🔮 AUTO-SPELL")
            print("-" * 15)
            print("1. Iniciar auto-spell")
            print("2. Detener auto-spell")
            print("3. Configurar hechizos")
            print("4. Estado")
            print("5. Volver")
            
            choice = input("\nElige una opción (1-5): ").strip()
            
            if choice == "1":
                if self.auto_spell.start():
                    self.features_status["auto_spell"] = True
                    print("✅ Auto-spell iniciado")
                else:
                    print("❌ Error iniciando auto-spell")
            
            elif choice == "2":
                self.auto_spell.stop()
                self.features_status["auto_spell"] = False
                print("✅ Auto-spell detenido")
            
            elif choice == "3":
                self.configure_auto_spell()
            
            elif choice == "4":
                status = self.auto_spell.get_status()
                print(f"Estado: {'🟢 Activo' if status['running'] else '🔴 Inactivo'}")
                print(f"Hechizos activos: {status['enabled_spells']}/{status['total_spells']}")
            
            elif choice == "5":
                break
            
            else:
                print("❌ Opción inválida")
    
    def handle_auto_loot(self):
        """Handle auto-loot menu."""
        while True:
            print("\n💰 AUTO-LOOT")
            print("-" * 15)
            print("1. Iniciar auto-loot")
            print("2. Detener auto-loot")
            print("3. Configurar items")
            print("4. Estado")
            print("5. Volver")
            
            choice = input("\nElige una opción (1-5): ").strip()
            
            if choice == "1":
                if self.auto_loot.start():
                    self.features_status["auto_loot"] = True
                    print("✅ Auto-loot iniciado")
                else:
                    print("❌ Error iniciando auto-loot")
            
            elif choice == "2":
                self.auto_loot.stop()
                self.features_status["auto_loot"] = False
                print("✅ Auto-loot detenido")
            
            elif choice == "3":
                self.configure_auto_loot()
            
            elif choice == "4":
                status = self.auto_loot.get_status()
                print(f"Estado: {'🟢 Activo' if status['running'] else '🔴 Inactivo'}")
                print(f"Items activos: {status['enabled_items']}/{status['total_items']}")
            
            elif choice == "5":
                break
            
            else:
                print("❌ Opción inválida")
    
    def handle_auto_walk(self):
        """Handle auto-walk menu."""
        while True:
            print("\n🚶 AUTO-WALK")
            print("-" * 15)
            print("1. Iniciar auto-walk")
            print("2. Detener auto-walk")
            print("3. Configurar patrón")
            print("4. Estado")
            print("5. Volver")
            
            choice = input("\nElige una opción (1-5): ").strip()
            
            if choice == "1":
                if self.auto_walk.start():
                    self.features_status["auto_walk"] = True
                    print("✅ Auto-walk iniciado")
                else:
                    print("❌ Error iniciando auto-walk")
            
            elif choice == "2":
                self.auto_walk.stop()
                self.features_status["auto_walk"] = False
                print("✅ Auto-walk detenido")
            
            elif choice == "3":
                self.configure_auto_walk()
            
            elif choice == "4":
                status = self.auto_walk.get_status()
                print(f"Estado: {'🟢 Activo' if status['running'] else '🔴 Inactivo'}")
                print(f"Patrón actual: {status['current_pattern']}")
            
            elif choice == "5":
                break
            
            else:
                print("❌ Opción inválida")
    
    def start_all_features(self):
        """Start all features."""
        print("🚀 Iniciando todas las funcionalidades...")
        
        features = [
            ("Auto-Attack", self.auto_attack),
            ("Auto-Spell", self.auto_spell),
            ("Auto-Loot", self.auto_loot),
            ("Auto-Walk", self.auto_walk)
        ]
        
        for name, feature in features:
            try:
                if feature.start():
                    self.features_status[name.lower().replace("-", "_")] = True
                    print(f"✅ {name} iniciado")
                else:
                    print(f"❌ Error iniciando {name}")
            except Exception as e:
                print(f"❌ Error en {name}: {e}")
        
        print("🎉 Todas las funcionalidades iniciadas")
    
    def stop_all_features(self):
        """Stop all features."""
        print("🛑 Deteniendo todas las funcionalidades...")
        
        features = [
            ("Auto-Attack", self.auto_attack),
            ("Auto-Spell", self.auto_spell),
            ("Auto-Loot", self.auto_loot),
            ("Auto-Walk", self.auto_walk)
        ]
        
        for name, feature in features:
            try:
                feature.stop()
                self.features_status[name.lower().replace("-", "_")] = False
                print(f"✅ {name} detenido")
            except Exception as e:
                print(f"❌ Error deteniendo {name}: {e}")
        
        print("🎉 Todas las funcionalidades detenidas")
    
    def show_status(self):
        """Show bot status."""
        print("\n📊 ESTADO DEL BOT")
        print("-" * 20)
        
        for feature, status in self.features_status.items():
            icon = "🟢" if status else "🔴"
            name = feature.replace("_", " ").title()
            print(f"{icon} {name}: {'Activo' if status else 'Inactivo'}")
        
        print(f"\n🖥️  Ventana de Tibia: {'✅ Conectado' if self.screen_reader else '❌ No conectado'}")
    
    def configure_auto_attack(self):
        """Configure auto-attack settings."""
        print("\n⚙️ CONFIGURACIÓN AUTO-ATTACK")
        print("-" * 30)
        
        print(f"Tecla de ataque actual: {self.auto_attack.attack_key}")
        print(f"Tecla siguiente objetivo: {self.auto_attack.next_target_key}")
        print(f"Intervalo actual: {self.auto_attack.attack_interval}s")
        
        new_key = input("Nueva tecla de ataque (Enter para mantener): ").strip()
        if new_key:
            self.auto_attack.set_attack_key(new_key)
            print(f"✅ Tecla de ataque cambiada a: {new_key}")
    
    def configure_auto_spell(self):
        """Configure auto-spell settings."""
        print("\n⚙️ CONFIGURACIÓN AUTO-SPELL")
        print("-" * 30)
        
        spells = self.auto_spell.get_spells()
        for i, spell in enumerate(spells, 1):
            status = "🟢" if spell["enabled"] else "🔴"
            print(f"{i}. {status} {spell['name']} ({spell['key']}) - {spell['interval']}s")
        
        try:
            choice = int(input("\nElige hechizo para configurar (0 para volver): ")) - 1
            if 0 <= choice < len(spells):
                spell = spells[choice]
                print(f"\nConfigurando: {spell['name']}")
                
                new_interval = input(f"Nuevo intervalo (actual: {spell['interval']}s): ").strip()
                if new_interval:
                    self.auto_spell.set_spell_interval(spell['name'], float(new_interval))
                    print(f"✅ Intervalo cambiado a {new_interval}s")
                
                enable = input("¿Habilitar? (s/n): ").strip().lower()
                if enable == 's':
                    self.auto_spell.enable_spell(spell['name'])
                    print("✅ Hechizo habilitado")
                elif enable == 'n':
                    self.auto_spell.disable_spell(spell['name'])
                    print("✅ Hechizo deshabilitado")
        except (ValueError, IndexError):
            print("❌ Opción inválida")
    
    def configure_auto_loot(self):
        """Configure auto-loot settings."""
        print("\n⚙️ CONFIGURACIÓN AUTO-LOOT")
        print("-" * 30)
        
        items = self.auto_loot.get_loot_items()
        for i, item in enumerate(items, 1):
            status = "🟢" if item["enabled"] else "🔴"
            print(f"{i}. {status} {item['name']} (prioridad: {item['priority']})")
        
        try:
            choice = int(input("\nElige item para configurar (0 para volver): ")) - 1
            if 0 <= choice < len(items):
                item = items[choice]
                print(f"\nConfigurando: {item['name']}")
                
                enable = input("¿Habilitar? (s/n): ").strip().lower()
                if enable == 's':
                    self.auto_loot.enable_loot_item(item['name'])
                    print("✅ Item habilitado")
                elif enable == 'n':
                    self.auto_loot.disable_loot_item(item['name'])
                    print("✅ Item deshabilitado")
        except (ValueError, IndexError):
            print("❌ Opción inválida")
    
    def configure_auto_walk(self):
        """Configure auto-walk settings."""
        print("\n⚙️ CONFIGURACIÓN AUTO-WALK")
        print("-" * 30)
        
        patterns = self.auto_walk.get_patterns()
        for i, pattern in enumerate(patterns, 1):
            print(f"{i}. {pattern}")
        
        try:
            choice = int(input("\nElige patrón (0 para volver): ")) - 1
            if 0 <= choice < len(patterns):
                pattern = patterns[choice]
                self.auto_walk.set_pattern(pattern)
                print(f"✅ Patrón cambiado a: {pattern}")
        except (ValueError, IndexError):
            print("❌ Opción inválida")
    
    def run(self):
        """Run the CLI interface."""
        print("🎮 Iniciando Tibia Bot CLI...")
        
        if not self.initialize_systems():
            print("❌ Error inicializando sistemas")
            return
        
        self.running = True
        
        while self.running:
            try:
                self.show_menu()
                choice = input("Elige una opción (1-9): ").strip()
                
                if choice == "1":
                    self.handle_auto_attack()
                
                elif choice == "2":
                    self.handle_auto_spell()
                
                elif choice == "3":
                    self.handle_auto_loot()
                
                elif choice == "4":
                    self.handle_auto_walk()
                
                elif choice == "5":
                    self.start_all_features()
                
                elif choice == "6":
                    self.show_status()
                    input("Presiona Enter para continuar...")
                
                elif choice == "7":
                    print("\n⚙️ CONFIGURACIÓN")
                    print("-" * 15)
                    print("1. Auto-Attack")
                    print("2. Auto-Spell")
                    print("3. Auto-Loot")
                    print("4. Auto-Walk")
                    print("5. Volver")
                    
                    config_choice = input("Elige configuración (1-5): ").strip()
                    
                    if config_choice == "1":
                        self.configure_auto_attack()
                    elif config_choice == "2":
                        self.configure_auto_spell()
                    elif config_choice == "3":
                        self.configure_auto_loot()
                    elif config_choice == "4":
                        self.configure_auto_walk()
                
                elif choice == "8":
                    self.stop_all_features()
                
                elif choice == "9":
                    self.stop_all_features()
                    self.running = False
                    print("👋 ¡Hasta luego!")
                
                else:
                    print("❌ Opción inválida")
                
            except KeyboardInterrupt:
                print("\n🛑 Interrumpido por el usuario")
                self.stop_all_features()
                break
            except Exception as e:
                print(f"❌ Error: {e}")

def main():
    """Main function."""
    cli = TibiaBotCLI()
    cli.run()

if __name__ == "__main__":
    main() 