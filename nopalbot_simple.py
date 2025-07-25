#!/usr/bin/env python3
"""
NopalBot Simple - Solo Auto Attack y Auto Walk
Versión simplificada y funcional
"""

import time
import threading
import keyboard
import pyautogui
import win32gui
import win32con
import customtkinter as ctk
from datetime import datetime
import random

class TransparentOverlay:
    def __init__(self, parent):
        self.parent = parent
        self.is_visible = False
        self.create_overlay()
        
    def create_overlay(self):
        self.overlay = ctk.CTkToplevel(self.parent)
        self.overlay.title("NopalBot Overlay")
        self.overlay.geometry("400x300+1400+50")
        self.overlay.configure(fg_color="black")
        self.overlay.attributes('-alpha', 0.8)
        self.overlay.attributes('-topmost', True)
        self.overlay.overrideredirect(True)
        
        # Log text
        self.log_text = ctk.CTkTextbox(self.overlay, fg_color="black", text_color="yellow")
        self.log_text.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Hide initially
        self.overlay.withdraw()
        
    def show(self):
        self.overlay.deiconify()
        self.is_visible = True
        
    def hide(self):
        self.overlay.withdraw()
        self.is_visible = False
        
    def add_log(self, message):
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"
        self.log_text.insert("end", log_entry)
        self.log_text.see("end")

class NopalBotSimple:
    def __init__(self, gui_callback=None):
        self.gui_callback = gui_callback
        self.running = False
        self.paused = False
        
        # Configuración básica
        self.auto_attack_enabled = False
        self.auto_walk_enabled = False
        self.auto_heal_enabled = False
        self.heal_with_spell = True  # True = spell, False = potion
        
        # Variables de salud y mana
        self.health = 100
        self.mana = 100
        self.heal_threshold = 40  # Curar cuando vida < 40%
        self.spell_mana_threshold = 60  # Solo usar spells si mana > 60%
        
        # Variables de ventana de Tibia
        self.tibia_window = None
        self.tibia_left = 0
        self.tibia_top = 0
        self.tibia_width = 0
        self.tibia_height = 0
        
        # Variables de movimiento
        self.last_movement = 0
        self.movement_direction = 'S'  # Empezar hacia abajo
        self.stuck_counter = 0
        self.last_position = None
        self.stuck_threshold = 3  # Segundos antes de cambiar dirección
        self.direction_change_timer = time.time()  # Inicializar timer
        self.direction_change_interval = 15  # Cambiar dirección cada 15 segundos automáticamente
        
        # Variables de timing
        self.last_heal = 0
        self.last_rune = 0
        self.heal_cooldown = 2.0  # Cooldown entre curas
        self.rune_cooldown = 1.0  # Cooldown entre runas
        
        # Hotkeys
        self.hotkeys = {
            'attack': 'CTRL+SPACE',
            'next_target': 'SPACE',
            'movement_up': 'w',
            'movement_down': 's', 
            'movement_left': 'a',
            'movement_right': 'd',
            'heal_spell': 'f3',  # Exura para druid
            'heal_potion': 'f1',  # Health potion
            'rune': 'r'  # Rune casting
        }
        
    def log_to_gui(self, message):
        if self.gui_callback:
            self.gui_callback(message)
        print(f"[{datetime.now().strftime('%H:%M:%S')}] {message}")
        
    def find_tibia_window(self):
        """Encontrar ventana de Tibia"""
        try:
            # Método 1: Buscar por nombre exacto
            self.tibia_window = win32gui.FindWindow(None, "Tibia")
            
            # Método 2: Si no encuentra, buscar por nombre parcial
            if not self.tibia_window:
                self.log_to_gui("🔍 Trying partial name search...")
                def enum_windows_callback(hwnd, windows):
                    if win32gui.IsWindowVisible(hwnd):
                        window_title = win32gui.GetWindowText(hwnd)
                        if "tibia" in window_title.lower():
                            windows.append((hwnd, window_title))
                    return True
                
                windows = []
                win32gui.EnumWindows(enum_windows_callback, windows)
                
                if windows:
                    self.tibia_window = windows[0][0]
                    self.log_to_gui(f"✅ Found Tibia window: {windows[0][1]}")
                else:
                    self.log_to_gui("❌ No Tibia window found!")
                    return False
            
            if self.tibia_window:
                rect = win32gui.GetWindowRect(self.tibia_window)
                self.tibia_left = rect[0]
                self.tibia_top = rect[1]
                self.tibia_width = rect[2] - rect[0]
                self.tibia_height = rect[3] - rect[1]
                
                self.log_to_gui(f"✅ Tibia window found!")
                self.log_to_gui(f"📍 Position: ({self.tibia_left}, {self.tibia_top})")
                self.log_to_gui(f"📏 Size: {self.tibia_width}x{self.tibia_height}")
                return True
            else:
                self.log_to_gui("❌ Tibia window not found!")
                return False
        except Exception as e:
            self.log_to_gui(f"❌ Error finding Tibia: {e}")
            return False
    
    def activate_tibia_window(self):
        """Activar ventana de Tibia"""
        try:
            if self.tibia_window:
                # Solo activar si no está ya activa
                foreground_window = win32gui.GetForegroundWindow()
                if foreground_window != self.tibia_window:
                    win32gui.SetForegroundWindow(self.tibia_window)
                    time.sleep(0.1)
                return True
            return False
        except Exception as e:
            self.log_to_gui(f"❌ Error activating Tibia: {e}")
            return False
    
    def simple_attack(self):
        """Ataque simple y directo"""
        try:
            if not self.activate_tibia_window():
                return False
            
            # PASO 1: SPACE (next target)
            keyboard.press_and_release('space')
            time.sleep(0.2)
            
            # PASO 2: CTRL+SPACE (attack)
            keyboard.press('ctrl')
            keyboard.press_and_release('space')
            keyboard.release('ctrl')
            
            self.log_to_gui("⚔️ Attack sequence sent")
            return True
            
        except Exception as e:
            self.log_to_gui(f"❌ Error in attack: {e}")
            return False
    
    def auto_heal(self):
        """Curación automática con spell o potión"""
        try:
            current_time = time.time()
            
            # Verificar cooldown
            if current_time - self.last_heal < self.heal_cooldown:
                return False
            
            # Simular detección de salud (en un bot real esto vendría de OCR)
            if self.health < self.heal_threshold:
                if not self.activate_tibia_window():
                    return False
                
                if self.heal_with_spell and self.mana > self.spell_mana_threshold:
                    # Usar spell de curación
                    keyboard.press_and_release(self.hotkeys['heal_spell'])
                    self.log_to_gui(f"🔮 Healing with spell {self.hotkeys['heal_spell']}")
                    self.mana = max(0, self.mana - 20)  # Simular consumo de mana
                else:
                    # Usar potión de vida
                    keyboard.press_and_release(self.hotkeys['heal_potion'])
                    self.log_to_gui(f"❤️ Healing with potion {self.hotkeys['heal_potion']}")
                
                self.health = min(100, self.health + 30)  # Simular recuperación
                self.last_heal = current_time
                return True
            
            return False
            
        except Exception as e:
            self.log_to_gui(f"❌ Error in auto heal: {e}")
            return False
    
    def cast_rune(self):
        """Lanzar runa al target"""
        try:
            current_time = time.time()
            
            # Verificar cooldown
            if current_time - self.last_rune < self.rune_cooldown:
                return False
            
            # Solo lanzar runas si hay suficiente mana
            if self.mana < self.spell_mana_threshold:
                return False
            
            if not self.activate_tibia_window():
                return False
            
            # Lanzar runa
            keyboard.press_and_release(self.hotkeys['rune'])
            self.log_to_gui(f"💎 Casting rune {self.hotkeys['rune']}")
            self.mana = max(0, self.mana - 15)  # Simular consumo de mana
            self.last_rune = current_time
            return True
            
        except Exception as e:
            self.log_to_gui(f"❌ Error casting rune: {e}")
            return False
    
    def avoid_stairs(self):
        """Evitar subir/bajar escaleras"""
        try:
            # Simular detección de escaleras (en un bot real esto sería OCR)
            # Por ahora, solo evitamos movimientos que podrían ser escaleras
            stair_directions = ['w', 's']  # Arriba y abajo pueden ser escaleras
            
            if self.movement_direction.lower() in stair_directions:
                # Cambiar a dirección horizontal
                if self.movement_direction.lower() == 'w':
                    self.movement_direction = 'a'  # Cambiar a izquierda
                elif self.movement_direction.lower() == 's':
                    self.movement_direction = 'd'  # Cambiar a derecha
                
                self.log_to_gui(f"🚫 Avoiding stairs, changing to {self.movement_direction}")
                return True
            
            return False
            
        except Exception as e:
            self.log_to_gui(f"❌ Error avoiding stairs: {e}")
            return False
    
    def smart_walk(self):
        """Movimiento inteligente que evita paredes y escaleras"""
        try:
            current_time = time.time()
            if current_time - self.last_movement < 0.8:  # Mover cada 0.8 segundos
                return False
            
            # Cambio automático de dirección cada 15 segundos
            if current_time - self.direction_change_timer > self.direction_change_interval:
                directions = ['S', 'D', 'W', 'A']
                current_index = directions.index(self.movement_direction)
                self.movement_direction = directions[(current_index + 1) % len(directions)]
                self.direction_change_timer = current_time
                self.log_to_gui(f"🔄 Auto direction change: {self.movement_direction}")
            
            # Evitar escaleras
            if self.avoid_stairs():
                self.direction_change_timer = current_time  # Resetear timer
            
            # Sistema mejorado de detección de stuck
            if self.last_position:
                time_since_last_move = current_time - self.last_movement
                if time_since_last_move > self.stuck_threshold:
                    self.stuck_counter += 1
                    self.log_to_gui(f"🚧 Stuck detected! Changing direction... (Attempt {self.stuck_counter})")
                    
                    # Cambiar dirección de forma más inteligente
                    if self.stuck_counter <= 2:
                        # Primera vez: cambiar a dirección perpendicular
                        if self.movement_direction in ['S', 'W']:
                            self.movement_direction = 'D' if self.movement_direction == 'S' else 'A'
                        else:
                            self.movement_direction = 'S' if self.movement_direction == 'D' else 'W'
                    else:
                        # Después de 2 intentos: probar dirección opuesta
                        opposite = {'S': 'W', 'W': 'S', 'A': 'D', 'D': 'A'}
                        self.movement_direction = opposite.get(self.movement_direction, 'S')
                        self.stuck_counter = 0
                        self.log_to_gui(f"🔄 Trying opposite direction: {self.movement_direction}")
                    
                    # Resetear timer de movimiento
                    self.last_movement = current_time
            
            if not self.activate_tibia_window():
                return False
            
            # Enviar movimiento
            keyboard.press_and_release(self.movement_direction.lower())
            self.log_to_gui(f"🚶 Moving {self.movement_direction}")
            
            # Actualizar posición y timer
            self.last_position = self.get_character_position()
            self.last_movement = current_time
            return True
            
        except Exception as e:
            self.log_to_gui(f"❌ Error in movement: {e}")
            return False
    
    def get_character_position(self):
        """Obtener posición del personaje (simulado pero más realista)"""
        try:
            # Simular posición basada en el tiempo y dirección
            current_time = time.time()
            base_x = 100 + (int(current_time) % 50)  # Posición base X
            base_y = 100 + (int(current_time) % 50)  # Posición base Y
            
            # Agregar pequeña variación basada en la dirección
            if self.movement_direction == 'S':
                base_y += 5
            elif self.movement_direction == 'W':
                base_y -= 5
            elif self.movement_direction == 'A':
                base_x -= 5
            elif self.movement_direction == 'D':
                base_x += 5
            
            return (base_x, base_y)
        except:
            # Fallback si hay error
            return (random.randint(100, 200), random.randint(100, 200))
    
    def setup_hotkeys(self):
        """Configurar hotkeys globales"""
        keyboard.add_hotkey('f11', self.toggle_pause)
        keyboard.add_hotkey('f10', self.stop_bot)
        
    def toggle_pause(self):
        """Pausar/Reanudar bot"""
        self.paused = not self.paused
        status = "PAUSED" if self.paused else "RESUMED"
        self.log_to_gui(f"⏸️ Bot {status}")
        
    def stop_bot(self):
        """Parar bot"""
        self.running = False
        self.log_to_gui("🛑 Bot stopped by F10")
        
    def run_bot(self):
        """Ejecutar bot principal"""
        try:
            self.setup_hotkeys()
            
            self.log_to_gui("🚀 Starting NopalBot Simple...")
            self.log_to_gui("⚔️ Auto Attack: " + ("ENABLED" if self.auto_attack_enabled else "DISABLED"))
            self.log_to_gui("🚶 Auto Walk: " + ("ENABLED" if self.auto_walk_enabled else "DISABLED"))
            self.log_to_gui("❤️ Auto Heal: " + ("ENABLED" if self.auto_heal_enabled else "DISABLED"))
            self.log_to_gui("🔮 Heal Method: " + ("SPELL" if self.heal_with_spell else "POTION"))
            self.log_to_gui("🎮 Press F11 to pause/resume + cast runes, F10 to stop")
            
            if not self.find_tibia_window():
                self.log_to_gui("❌ Cannot find Tibia window!")
                return
                
            self.running = True
            self.paused = False
            
            while self.running:
                if not self.paused:
                    # Auto Heal (prioridad alta)
                    if self.auto_heal_enabled:
                        if self.auto_heal():
                            time.sleep(0.3)
                            continue
                    
                    # Auto Attack
                    if self.auto_attack_enabled:
                        if self.simple_attack():
                            # Después de atacar, lanzar runa si hay target
                            self.cast_rune()
                            time.sleep(0.5)
                    
                    # Auto Walk (solo si no hay enemigos o si está habilitado)
                    if self.auto_walk_enabled:
                        self.smart_walk()
                        time.sleep(0.3)
                    
                time.sleep(0.2)
                
        except Exception as e:
            self.log_to_gui(f"❌ Error in main loop: {e}")
        finally:
            self.running = False
            self.log_to_gui("🏁 Bot finished")

class NopalBotSimpleGUI:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("🤖 NopalBot Simple - Auto Attack & Walk")
        self.root.geometry("600x500")
        
        self.bot = None
        self.bot_thread = None
        self.overlay = TransparentOverlay(self.root)
        
        # Variables de control
        self.auto_attack_enabled = False
        self.auto_walk_enabled = False
        self.auto_heal_enabled = False
        self.heal_with_spell = True  # True = spell, False = potion
        
        self.setup_gui()
        
    def setup_gui(self):
        # Frame principal
        main_frame = ctk.CTkFrame(self.root)
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Título
        title = ctk.CTkLabel(main_frame, text="🤖 NOPALBOT SIMPLE", 
                            font=ctk.CTkFont(size=24, weight="bold"))
        title.pack(pady=10)
        
        # Frame de controles principales
        controls_frame = ctk.CTkFrame(main_frame)
        controls_frame.pack(fill='x', padx=10, pady=10)
        
        controls_title = ctk.CTkLabel(controls_frame, text="🎮 MAIN CONTROLS", 
                                     font=ctk.CTkFont(size=16, weight="bold"))
        controls_title.pack(pady=5)
        
        # Botones principales
        buttons_frame = ctk.CTkFrame(controls_frame)
        buttons_frame.pack(pady=10)
        
        self.start_button = ctk.CTkButton(buttons_frame, text="🚀 START BOT", 
                                         command=self.start_bot, fg_color="green")
        self.start_button.pack(side='left', padx=5)
        
        self.stop_button = ctk.CTkButton(buttons_frame, text="🛑 STOP BOT", 
                                        command=self.stop_bot, fg_color="red", state="disabled")
        self.stop_button.pack(side='left', padx=5)
        
        self.overlay_button = ctk.CTkButton(buttons_frame, text="📊 SHOW OVERLAY", 
                                           command=self.toggle_overlay)
        self.overlay_button.pack(side='left', padx=5)
        
        # Frame de controles individuales
        individual_frame = ctk.CTkFrame(main_frame)
        individual_frame.pack(fill='x', padx=10, pady=5)
        
        individual_title = ctk.CTkLabel(individual_frame, text="⚙️ INDIVIDUAL CONTROLS", 
                                       font=ctk.CTkFont(size=16, weight="bold"))
        individual_title.pack(pady=5)
        
        controls_grid = ctk.CTkFrame(individual_frame)
        controls_grid.pack(pady=5)
        
        # Controles individuales
        row1_controls = ctk.CTkFrame(controls_grid)
        row1_controls.pack(pady=5)
        
        self.attack_button = ctk.CTkButton(row1_controls, text="⚔️ AUTO ATTACK", 
                                          command=self.toggle_auto_attack,
                                          fg_color="purple", hover_color="darkpurple")
        self.attack_button.pack(side='left', padx=5)
        
        self.walk_button = ctk.CTkButton(row1_controls, text="🚶 AUTO WALK", 
                                        command=self.toggle_auto_walk,
                                        fg_color="orange", hover_color="darkorange")
        self.walk_button.pack(side='left', padx=5)
        
        self.heal_button = ctk.CTkButton(row1_controls, text="❤️ AUTO HEAL", 
                                        command=self.toggle_auto_heal,
                                        fg_color="red", hover_color="darkred")
        self.heal_button.pack(side='left', padx=5)

        # Frame de controles de curación
        heal_frame = ctk.CTkFrame(individual_frame)
        heal_frame.pack(pady=5)

        heal_title = ctk.CTkLabel(heal_frame, text="💊 HEALING OPTIONS", 
                                   font=ctk.CTkFont(size=16, weight="bold"))
        heal_title.pack(pady=5)

        self.heal_spell_button = ctk.CTkButton(heal_frame, text="🔮 HEAL WITH SPELL", 
                                               command=self.toggle_heal_with_spell,
                                               fg_color="blue", hover_color="darkblue")
        self.heal_spell_button.pack(side='left', padx=5)

        self.heal_potion_button = ctk.CTkButton(heal_frame, text="❤️ HEAL WITH POTION", 
                                                command=self.toggle_heal_with_potion,
                                                fg_color="red", hover_color="darkred")
        self.heal_potion_button.pack(side='left', padx=5)
        
        # Frame de configuración
        config_frame = ctk.CTkFrame(main_frame)
        config_frame.pack(fill='x', padx=10, pady=5)
        
        config_title = ctk.CTkLabel(config_frame, text="⚙️ CONFIGURATION", 
                                   font=ctk.CTkFont(size=16, weight="bold"))
        config_title.pack(pady=5)
        
        # Hotkeys info
        hotkeys_text = """
        🎯 Attack: CTRL+SPACE    🎯 Next Target: SPACE
        🚶 Movement: WASD        ⏸️ Pause/Resume: F11
        🛑 Stop Bot: F10
        """
        
        hotkeys_label = ctk.CTkLabel(config_frame, text=hotkeys_text, 
                                    font=ctk.CTkFont(size=12))
        hotkeys_label.pack(pady=5)
        
        # Frame de logs
        log_frame = ctk.CTkFrame(main_frame)
        log_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        log_title = ctk.CTkLabel(log_frame, text="📊 BOT LOGS", 
                                font=ctk.CTkFont(size=16, weight="bold"))
        log_title.pack(pady=5)
        
        self.log_text = ctk.CTkTextbox(log_frame, height=150)
        self.log_text.pack(fill='both', expand=True, padx=5, pady=5)
        
    def toggle_auto_attack(self):
        self.auto_attack_enabled = not self.auto_attack_enabled
        status = "ENABLED" if self.auto_attack_enabled else "DISABLED"
        color = "green" if self.auto_attack_enabled else "purple"
        self.attack_button.configure(fg_color=color)
        self.log_to_gui(f"⚔️ Auto Attack {status}")
        
    def toggle_auto_walk(self):
        self.auto_walk_enabled = not self.auto_walk_enabled
        status = "ENABLED" if self.auto_walk_enabled else "DISABLED"
        color = "green" if self.auto_walk_enabled else "orange"
        self.walk_button.configure(fg_color=color)
        self.log_to_gui(f"🚶 Auto Walk {status}")
        
    def toggle_auto_heal(self):
        self.auto_heal_enabled = not self.auto_heal_enabled
        status = "ENABLED" if self.auto_heal_enabled else "DISABLED"
        color = "green" if self.auto_heal_enabled else "red"
        self.heal_button.configure(fg_color=color)
        self.log_to_gui(f"❤️ Auto Heal {status}")

    def toggle_heal_with_spell(self):
        self.heal_with_spell = not self.heal_with_spell
        status = "SPELL" if self.heal_with_spell else "POTION"
        color = "blue" if self.heal_with_spell else "red"
        self.heal_spell_button.configure(fg_color=color)
        self.heal_potion_button.configure(fg_color="red") # Ensure potion button is red
        self.log_to_gui(f"💊 Healing method changed to {status}")
        
    def toggle_heal_with_potion(self):
        self.heal_with_spell = False
        self.heal_spell_button.configure(fg_color="red") # Ensure spell button is red
        self.heal_potion_button.configure(fg_color="red") # Ensure potion button is red
        self.log_to_gui(f"💊 Healing method changed to POTION")
        
    def log_to_gui(self, message):
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"
        
        self.log_text.insert("end", log_entry)
        self.log_text.see("end")
        
        # Actualizar overlay si está visible
        if self.overlay and self.overlay.is_visible:
            self.overlay.add_log(message)
            
    def start_bot(self):
        if self.bot and self.bot.running:
            self.log_to_gui("⚠️ Bot is already running!")
            return
            
        try:
            # Crear nuevo bot
            self.bot = NopalBotSimple(self.log_to_gui)
            
            # Configurar controles individuales
            self.bot.auto_attack_enabled = self.auto_attack_enabled
            self.bot.auto_walk_enabled = self.auto_walk_enabled
            self.bot.auto_heal_enabled = self.auto_heal_enabled
            self.bot.heal_with_spell = self.heal_with_spell
            
            # Iniciar bot en thread separado
            self.bot_thread = threading.Thread(target=self.bot.run_bot, daemon=True)
            self.bot_thread.start()
            
            self.start_button.configure(state="disabled")
            self.stop_button.configure(state="normal")
            
            self.log_to_gui("🚀 Bot started successfully!")
            
        except Exception as e:
            self.log_to_gui(f"❌ Error starting bot: {e}")
            
    def stop_bot(self):
        if self.bot:
            self.bot.stop_bot()
            
        self.start_button.configure(state="normal")
        self.stop_button.configure(state="disabled")
        
        self.log_to_gui("🛑 Bot stopped!")
        
    def toggle_overlay(self):
        if self.overlay.is_visible:
            self.overlay.hide()
            self.overlay_button.configure(text="📊 SHOW OVERLAY")
        else:
            self.overlay.show()
            self.overlay_button.configure(text="📊 HIDE OVERLAY")
            
    def run(self):
        self.root.mainloop()

def main():
    app = NopalBotSimpleGUI()
    app.run()

if __name__ == "__main__":
    main() 