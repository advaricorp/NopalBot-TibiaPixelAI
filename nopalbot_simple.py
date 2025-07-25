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
import cv2
import numpy as np
from PIL import Image, ImageGrab
import tkinter as tk
from tkinter import messagebox

# Configurar tema
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class Tooltip:
    """Clase para mostrar tooltips informativos"""
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip = None
        self.widget.bind("<Enter>", self.show_tooltip)
        self.widget.bind("<Leave>", self.hide_tooltip)
    
    def show_tooltip(self, event=None):
        x, y, _, _ = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 20
        
        self.tooltip = tk.Toplevel(self.widget)
        self.tooltip.wm_overrideredirect(True)
        self.tooltip.wm_geometry(f"+{x}+{y}")
        
        label = tk.Label(self.tooltip, text=self.text, 
                        justify=tk.LEFT,
                        background="#ffffe0", 
                        relief=tk.SOLID, 
                        borderwidth=1,
                        font=("Arial", "8", "normal"))
        label.pack()
    
    def hide_tooltip(self, event=None):
        if self.tooltip:
            self.tooltip.destroy()
            self.tooltip = None

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

class NopalBotEliteKnight:
    """Bot especializado para Elite Knight - NopalBot by Pikos Nopal"""
    
    def __init__(self, gui_callback=None):
        self.gui_callback = gui_callback
        self.running = False
        self.paused = False
        self.tibia_window = None
        
        # Variables de control para Elite Knight
        self.auto_attack_enabled = False
        self.auto_walk_enabled = False
        self.auto_heal_enabled = False
        self.auto_mana_enabled = False
        self.auto_food_enabled = False
        self.auto_utani_hur_enabled = False  # Haste para Elite Knight
        self.auto_exori_enabled = False      # Exori para Elite Knight
        self.auto_exori_ico_enabled = False  # Exori Ico para Elite Knight
        self.auto_exori_gran_enabled = False # Exori Gran para Elite Knight
        self.auto_utito_tempo_enabled = False # Berserk para Elite Knight
        
        # Variables de curación
        self.heal_with_spell = True  # True = spell, False = potion
        self.health = 100
        self.mana = 100
        self.heal_threshold = 40  # Curar al 40% HP
        self.mana_threshold = 30  # Usar mana al 30%
        self.food_threshold = 50  # Comer al 50% HP
        self.last_heal = 0
        self.last_mana = 0
        self.last_food = 0
        self.heal_cooldown = 2.0
        self.mana_cooldown = 1.5
        self.food_cooldown = 3.0
        
        # Variables de tiempo para hechizos de Elite Knight
        self.last_utani_hur = 0
        self.last_exori = 0
        self.last_exori_ico = 0
        self.last_exori_gran = 0
        self.last_utito_tempo = 0
        
        # Variables de movimiento
        self.movement_direction = 'S'
        self.last_movement = 0
        self.direction_change_timer = time.time()
        self.direction_change_interval = 15
        self.stuck_threshold = 3
        self.stuck_counter = 0
        self.last_position = None
        
        # Sistema anti-stuck mejorado
        self.position_history = []
        self.movement_attempts = 0
        self.max_movement_attempts = 5
        self.last_position_check = time.time()
        self.position_check_interval = 2.0
        
        # Variables de mapping
        self.visited_coordinates = set()
        self.current_position = (0, 0, 0)
        self.target_position = None
        self.path_to_target = []
        self.mapping_enabled = False
        self.auto_exploration = False
        self.computer_vision_enabled = False
        
        # Hotkeys específicos para Elite Knight
        self.hotkeys = {
            'attack': 'ctrl+space',
            'next_target': 'space',
            'heal_spell': 'f1',
            'heal_potion': 'f2',
            'mana_potion': 'f3',
            'food': 'f12',
            'utani_hur': 'f4',      # Haste
            'exori': 'f5',          # Exori
            'exori_ico': 'f6',      # Exori Ico
            'exori_gran': 'f7',     # Exori Gran
            'utito_tempo': 'f8',    # Berserk
            'rune': 'r'
        }
        
        # Configurar hotkeys
        self.setup_hotkeys()
        
        # Encontrar ventana de Tibia
        self.find_tibia_window()
        
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
        """Lanzar runa si hay suficiente mana"""
        try:
            if not self.auto_rune_enabled:
                return False
                
            current_time = time.time()
            if current_time - self.last_rune < self.rune_cooldown:
                return False
            
            # Simular verificación de mana (deberías implementar detección real)
            if self.mana < self.spell_mana_threshold:
                return False
            
            if not self.activate_tibia_window():
                return False
            
            # Lanzar runa
            keyboard.press_and_release(self.hotkeys['rune'])
            self.log_to_gui(f"⚡ Casting rune (Mana: {self.mana}%)")
            
            # Simular consumo de mana
            self.mana = max(0, self.mana - 20)
            self.last_rune = current_time
            
            return True
            
        except Exception as e:
            self.log_to_gui(f"❌ Error casting rune: {e}")
            return False
    
    def cast_utani_hur(self):
        """Lanzar Utani Hur (Haste)"""
        try:
            if not self.auto_utani_hur_enabled:
                return False
                
            current_time = time.time()
            if current_time - self.last_utani_hur < 30.0:  # Cooldown de 30 segundos
                return False
            
            if self.mana < 40:  # Necesita 40 mana
                return False
            
            if not self.activate_tibia_window():
                return False
            
            keyboard.press_and_release(self.hotkeys['utani_hur'])
            self.log_to_gui(f"⚡ Utani Hur lanzado (Mana: {self.mana}%)")
            
            self.mana = max(0, self.mana - 40)
            self.last_utani_hur = current_time
            
            return True
            
        except Exception as e:
            self.log_to_gui(f"❌ Error lanzando Utani Hur: {e}")
            return False
    
    def cast_exori(self):
        """Lanzar Exori (ataque área)"""
        try:
            if not self.auto_exori_enabled:
                return False
                
            current_time = time.time()
            if current_time - self.last_exori < 8.0:  # Cooldown de 8 segundos
                return False
            
            if self.mana < 115:  # Necesita 115 mana
                return False
            
            if not self.activate_tibia_window():
                return False
            
            keyboard.press_and_release(self.hotkeys['exori'])
            self.log_to_gui(f"⚔️ Exori lanzado (Mana: {self.mana}%)")
            
            self.mana = max(0, self.mana - 115)
            self.last_exori = current_time
            
            return True
            
        except Exception as e:
            self.log_to_gui(f"❌ Error lanzando Exori: {e}")
            return False
    
    def cast_exori_ico(self):
        """Lanzar Exori Ico (ataque área mejorado)"""
        try:
            if not self.auto_exori_ico_enabled:
                return False
                
            current_time = time.time()
            if current_time - self.last_exori_ico < 6.0:  # Cooldown de 6 segundos
                return False
            
            if self.mana < 20:  # Necesita 20 mana
                return False
            
            if not self.activate_tibia_window():
                return False
            
            keyboard.press_and_release(self.hotkeys['exori_ico'])
            self.log_to_gui(f"⚔️ Exori Ico lanzado (Mana: {self.mana}%)")
            
            self.mana = max(0, self.mana - 20)
            self.last_exori_ico = current_time
            
            return True
            
        except Exception as e:
            self.log_to_gui(f"❌ Error lanzando Exori Ico: {e}")
            return False
    
    def cast_exori_gran(self):
        """Lanzar Exori Gran (ataque área grande)"""
        try:
            if not self.auto_exori_gran_enabled:
                return False
                
            current_time = time.time()
            if current_time - self.last_exori_gran < 12.0:  # Cooldown de 12 segundos
                return False
            
            if self.mana < 185:  # Necesita 185 mana
                return False
            
            if not self.activate_tibia_window():
                return False
            
            keyboard.press_and_release(self.hotkeys['exori_gran'])
            self.log_to_gui(f"⚔️ Exori Gran lanzado (Mana: {self.mana}%)")
            
            self.mana = max(0, self.mana - 185)
            self.last_exori_gran = current_time
            
            return True
            
        except Exception as e:
            self.log_to_gui(f"❌ Error lanzando Exori Gran: {e}")
            return False
    
    def cast_utito_tempo(self):
        """Lanzar Utito Tempo (Berserk)"""
        try:
            if not self.auto_utito_tempo_enabled:
                return False
                
            current_time = time.time()
            if current_time - self.last_utito_tempo < 60.0:  # Cooldown de 60 segundos
                return False
            
            if self.mana < 110:  # Necesita 110 mana
                return False
            
            if not self.activate_tibia_window():
                return False
            
            keyboard.press_and_release(self.hotkeys['utito_tempo'])
            self.log_to_gui(f"🔥 Utito Tempo lanzado (Mana: {self.mana}%)")
            
            self.mana = max(0, self.mana - 110)
            self.last_utito_tempo = current_time
            
            return True
            
        except Exception as e:
            self.log_to_gui(f"❌ Error lanzando Utito Tempo: {e}")
            return False
    
    def use_food(self):
        """Usar comida"""
        try:
            if not self.auto_food_enabled:
                return False
                
            current_time = time.time()
            if current_time - self.last_food < self.food_cooldown:
                return False
            
            if self.health > self.food_threshold:
                return False
            
            if not self.activate_tibia_window():
                return False
            
            keyboard.press_and_release(self.hotkeys['food'])
            self.log_to_gui(f"🍖 Comida usada (HP: {self.health}%)")
            
            self.last_food = current_time
            return True
            
        except Exception as e:
            self.log_to_gui(f"❌ Error usando comida: {e}")
            return False
    
    def use_mana_potion(self):
        """Usar poción de mana"""
        try:
            if not self.auto_mana_enabled:
                return False
                
            current_time = time.time()
            if current_time - self.last_mana < self.mana_cooldown:
                return False
            
            if self.mana > self.mana_threshold:
                return False
            
            if not self.activate_tibia_window():
                return False
            
            keyboard.press_and_release(self.hotkeys['mana_potion'])
            self.log_to_gui(f"🔮 Poción de mana usada (Mana: {self.mana}%)")
            
            self.last_mana = current_time
            return True
            
        except Exception as e:
            self.log_to_gui(f"❌ Error usando poción de mana: {e}")
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
    
    def update_position(self):
        """Actualizar posición actual basada en movimiento"""
        try:
            x, y, z = self.current_position
            
            # Simular movimiento basado en dirección
            if self.movement_direction == 'W':
                y -= 1
            elif self.movement_direction == 'S':
                y += 1
            elif self.movement_direction == 'A':
                x -= 1
            elif self.movement_direction == 'D':
                x += 1
            
            self.current_position = (x, y, z)
            
            # Agregar a coordenadas visitadas
            if self.mapping_enabled:
                self.visited_coordinates.add(self.current_position)
                self.log_to_gui(f"📍 Position updated: {self.current_position}")
            
        except Exception as e:
            self.log_to_gui(f"❌ Error updating position: {e}")
    
    def find_unexplored_area(self):
        """Encontrar área no explorada cercana"""
        try:
            if not self.mapping_enabled:
                return None
            
            x, y, z = self.current_position
            
            # Buscar en un radio de 10 tiles
            for radius in range(1, 11):
                for dx in range(-radius, radius + 1):
                    for dy in range(-radius, radius + 1):
                        new_pos = (x + dx, y + dy, z)
                        if new_pos not in self.visited_coordinates:
                            return new_pos
            
            return None
            
        except Exception as e:
            self.log_to_gui(f"❌ Error finding unexplored area: {e}")
            return None
    
    def calculate_path_to_target(self, target):
        """Calcular ruta simple hacia target"""
        try:
            if not target:
                return []
            
            current_x, current_y, current_z = self.current_position
            target_x, target_y, target_z = target
            
            path = []
            
            # Movimiento horizontal primero
            if current_x < target_x:
                path.extend(['D'] * (target_x - current_x))
            elif current_x > target_x:
                path.extend(['A'] * (current_x - target_x))
            
            # Movimiento vertical después
            if current_y < target_y:
                path.extend(['S'] * (target_y - current_y))
            elif current_y > target_y:
                path.extend(['W'] * (current_y - target_y))
            
            return path
            
        except Exception as e:
            self.log_to_gui(f"❌ Error calculating path: {e}")
            return []
    
    def auto_explore(self):
        """Exploración automática de la cueva"""
        try:
            if not self.auto_exploration:
                return False
            
            # Si no hay target, buscar área no explorada
            if not self.target_position:
                unexplored = self.find_unexplored_area()
                if unexplored:
                    self.target_position = unexplored
                    self.path_to_target = self.calculate_path_to_target(unexplored)
                    self.log_to_gui(f"🎯 New target: {unexplored}")
                else:
                    # Si no hay áreas no exploradas, cambiar dirección aleatoriamente
                    directions = ['W', 'A', 'S', 'D']
                    self.movement_direction = random.choice(directions)
                    self.log_to_gui(f"🔄 No unexplored areas, random direction: {self.movement_direction}")
                    return True
            
            # Seguir path hacia target
            if self.path_to_target:
                next_direction = self.path_to_target.pop(0)
                self.movement_direction = next_direction
                self.log_to_gui(f"🗺️ Following path: {next_direction}")
                return True
            else:
                # Llegamos al target
                self.target_position = None
                self.log_to_gui("✅ Reached target, looking for next area")
                return False
            
        except Exception as e:
            self.log_to_gui(f"❌ Error in auto explore: {e}")
            return False
    
    def save_map_data(self):
        """Guardar datos del mapa en archivo"""
        try:
            if not self.mapping_enabled:
                return
            
            map_data = {
                'visited_coordinates': list(self.visited_coordinates),
                'current_position': self.current_position,
                'timestamp': datetime.now().isoformat(),
                'total_visited': len(self.visited_coordinates)
            }
            
            import json
            with open('tibia_map_data.json', 'w') as f:
                json.dump(map_data, f, indent=2)
            
            self.log_to_gui(f"💾 Map data saved: {len(self.visited_coordinates)} coordinates")
            
        except Exception as e:
            self.log_to_gui(f"❌ Error saving map data: {e}")
    
    def capture_tibia_screen(self):
        """Capturar pantalla de Tibia"""
        try:
            if not self.tibia_window:
                return None
            
            # Obtener posición de la ventana de Tibia
            rect = win32gui.GetWindowRect(self.tibia_window)
            x, y, w, h = rect[0], rect[1], rect[2] - rect[0], rect[3] - rect[1]
            
            # Capturar pantalla
            screenshot = ImageGrab.grab(bbox=(x, y, x + w, y + h))
            return np.array(screenshot)
            
        except Exception as e:
            self.log_to_gui(f"❌ Error capturing screen: {e}")
            return None
    
    def detect_enemies(self, image):
        """Detectar enemigos en la imagen"""
        try:
            if image is None:
                return False
            
            # Convertir a HSV
            hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
            
            # Definir rangos de color para enemigos (rojos, marrones, grises)
            # Enemigos suelen ser rojos, marrones o grises
            lower_red1 = np.array([0, 100, 100])
            upper_red1 = np.array([10, 255, 255])
            lower_red2 = np.array([170, 100, 100])
            upper_red2 = np.array([180, 255, 255])
            
            lower_brown = np.array([10, 50, 50])
            upper_brown = np.array([20, 255, 255])
            
            lower_gray = np.array([0, 0, 50])
            upper_gray = np.array([180, 30, 200])
            
            # Crear máscaras
            mask_red1 = cv2.inRange(hsv, lower_red1, upper_red1)
            mask_red2 = cv2.inRange(hsv, lower_red2, upper_red2)
            mask_brown = cv2.inRange(hsv, lower_brown, upper_brown)
            mask_gray = cv2.inRange(hsv, lower_gray, upper_gray)
            
            # Combinar máscaras
            mask = cv2.bitwise_or(mask_red1, mask_red2)
            mask = cv2.bitwise_or(mask, mask_brown)
            mask = cv2.bitwise_or(mask, mask_gray)
            
            # Aplicar morfología para limpiar ruido
            kernel = np.ones((3,3), np.uint8)
            mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
            mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
            
            # Buscar contornos
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            # Filtrar contornos por tamaño y forma
            for contour in contours:
                area = cv2.contourArea(contour)
                if 200 < area < 5000:  # Enemigos suelen ser de tamaño medio
                    # Verificar forma (enemigos suelen ser cuadrados/rectangulares)
                    x, y, w, h = cv2.boundingRect(contour)
                    aspect_ratio = w / h if h > 0 else 0
                    
                    if 0.5 < aspect_ratio < 2.0:  # Forma rectangular
                        self.log_to_gui(f"⚔️ Enemy detected! Area: {area}, Position: ({x},{y})")
                        return True
            
            return False
            
        except Exception as e:
            self.log_to_gui(f"❌ Error detecting enemies: {e}")
            return False
    
    def detect_stairs(self, image):
        """Detectar escaleras en la imagen (mejorado)"""
        try:
            if image is None:
                return False
            
            # Convertir a HSV
            hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
            
            # Definir rangos de color para escaleras (grises, marrones, beige)
            lower_gray = np.array([0, 0, 50])
            upper_gray = np.array([180, 30, 200])
            
            lower_brown = np.array([10, 50, 50])
            upper_brown = np.array([20, 255, 255])
            
            lower_beige = np.array([20, 30, 150])
            upper_beige = np.array([30, 100, 255])
            
            # Crear máscaras
            mask_gray = cv2.inRange(hsv, lower_gray, upper_gray)
            mask_brown = cv2.inRange(hsv, lower_brown, upper_brown)
            mask_beige = cv2.inRange(hsv, lower_beige, upper_beige)
            
            # Combinar máscaras
            mask = cv2.bitwise_or(mask_gray, mask_brown)
            mask = cv2.bitwise_or(mask, mask_beige)
            
            # Aplicar morfología para limpiar ruido
            kernel = np.ones((5,5), np.uint8)
            mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
            mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
            
            # Buscar contornos
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            # Filtrar contornos por tamaño y forma
            for contour in contours:
                area = cv2.contourArea(contour)
                if area > 800:  # Escaleras suelen ser grandes
                    # Verificar forma (escaleras suelen ser rectangulares)
                    x, y, w, h = cv2.boundingRect(contour)
                    aspect_ratio = w / h if h > 0 else 0
                    
                    if 0.3 < aspect_ratio < 3.0:  # Forma rectangular
                        # Verificar si está en el centro de la pantalla (donde suelen estar las escaleras)
                        center_x = image.shape[1] // 2
                        center_y = image.shape[0] // 2
                        distance_to_center = ((x + w//2 - center_x)**2 + (y + h//2 - center_y)**2)**0.5
                        
                        if distance_to_center < 200:  # Cerca del centro
                            self.log_to_gui(f"🚪 Stairs detected! Area: {area}, Center distance: {distance_to_center:.1f}")
                            return True
            
            return False
            
        except Exception as e:
            self.log_to_gui(f"❌ Error detecting stairs: {e}")
            return False
    
    def detect_portals(self, image):
        """Detectar portales en la imagen"""
        try:
            if image is None:
                return False
            
            # Convertir a HSV
            hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
            
            # Definir rangos de color para portales (azules, morados, mágicos)
            # Portales suelen ser azules o morados brillantes
            lower_blue = np.array([100, 100, 100])
            upper_blue = np.array([130, 255, 255])
            
            lower_purple = np.array([130, 100, 100])
            upper_purple = np.array([170, 255, 255])
            
            # Crear máscaras
            mask_blue = cv2.inRange(hsv, lower_blue, upper_blue)
            mask_purple = cv2.inRange(hsv, lower_purple, upper_purple)
            
            # Combinar máscaras
            mask = cv2.bitwise_or(mask_blue, mask_purple)
            
            # Aplicar morfología para limpiar ruido
            kernel = np.ones((5,5), np.uint8)
            mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
            mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
            
            # Buscar contornos
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            # Filtrar contornos
            for contour in contours:
                area = cv2.contourArea(contour)
                if area > 500:  # Portales suelen ser más pequeños que escaleras
                    # Verificar forma circular/oval
                    x, y, w, h = cv2.boundingRect(contour)
                    aspect_ratio = w / h if h > 0 else 0
                    
                    if 0.7 < aspect_ratio < 1.3:  # Forma más circular
                        self.log_to_gui(f"🌀 Portal detected! Area: {area}, Ratio: {aspect_ratio:.2f}")
                        return True
            
            return False
            
        except Exception as e:
            self.log_to_gui(f"❌ Error detecting portals: {e}")
            return False
    
    def detect_obstacles(self, image):
        """Detectar obstáculos y paredes"""
        try:
            if image is None:
                return False
            
            # Convertir a escala de grises
            gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
            
            # Detectar bordes
            edges = cv2.Canny(gray, 50, 150)
            
            # Buscar líneas horizontales y verticales (paredes)
            lines = cv2.HoughLinesP(edges, 1, np.pi/180, threshold=50, 
                                   minLineLength=50, maxLineGap=10)
            
            if lines is not None:
                for line in lines:
                    x1, y1, x2, y2 = line[0]
                    # Verificar si es línea horizontal o vertical
                    if abs(x2 - x1) < 10 or abs(y2 - y1) < 10:
                        self.log_to_gui(f"🧱 Wall detected! Line: ({x1},{y1}) to ({x2},{y2})")
                        return True
            
            return False
            
        except Exception as e:
            self.log_to_gui(f"❌ Error detecting obstacles: {e}")
            return False
    
    def computer_vision_scan(self):
        """Escaneo completo con Computer Vision"""
        try:
            if not self.activate_tibia_window():
                return False
            
            # Capturar pantalla
            image = self.capture_tibia_screen()
            if image is None:
                return False
            
            # Detectar elementos
            enemies_detected = self.detect_enemies(image)
            stairs_detected = self.detect_stairs(image)
            portals_detected = self.detect_portals(image)
            obstacles_detected = self.detect_obstacles(image)
            
            # Tomar decisiones basadas en detecciones
            if enemies_detected:
                self.log_to_gui("⚔️ Enemy detected - stopping movement to attack")
                return "enemy"
            elif stairs_detected:
                self.log_to_gui("🚫 Stairs detected - avoiding movement")
                return "stairs"
            elif portals_detected:
                self.log_to_gui("🌀 Portal detected - avoiding movement")
                return "portal"
            elif obstacles_detected:
                self.log_to_gui("🧱 Obstacle detected - changing direction")
                return "obstacle"
            else:
                self.log_to_gui("👁️ Computer Vision: Clear path ahead")
                return "clear"
            
        except Exception as e:
            self.log_to_gui(f"❌ Error in computer vision scan: {e}")
            return "error"
    
    def smart_walk(self):
        """Movimiento inteligente que evita paredes y escaleras"""
        try:
            current_time = time.time()
            if current_time - self.last_movement < 0.8:  # Mover cada 0.8 segundos
                return False
            
            # Verificar si la posición cambió (sistema anti-stuck)
            if not self.check_position_change():
                # Si está atascado, probar todas las teclas de movimiento
                if self.try_all_movement_keys():
                    self.last_movement = current_time
                    return True
                else:
                    # Si ninguna tecla funcionó, esperar un poco más
                    time.sleep(2.0)
                    return False
            
            # Computer Vision scan cada 2 segundos
            if self.computer_vision_enabled and current_time - self.last_movement > 2.0:
                cv_result = self.computer_vision_scan()
                if cv_result == "enemy":
                    # Si detecta enemigo, parar movimiento para atacar
                    self.log_to_gui("⚔️ Enemy detected - stopping movement")
                    return False
                elif cv_result == "stairs":
                    # Cambiar dirección si detecta escaleras
                    directions = ['A', 'D']  # Solo horizontales
                    self.movement_direction = random.choice(directions)
                    self.log_to_gui(f"🚫 Avoiding stairs, new direction: {self.movement_direction}")
                    return False
                elif cv_result == "portal":
                    # Cambiar dirección si detecta portal
                    directions = ['A', 'D']  # Solo horizontales
                    self.movement_direction = random.choice(directions)
                    self.log_to_gui(f"🌀 Avoiding portal, new direction: {self.movement_direction}")
                    return False
                elif cv_result == "obstacle":
                    # Cambiar dirección si detecta obstáculo
                    opposite = {'S': 'W', 'W': 'S', 'A': 'D', 'D': 'A'}
                    self.movement_direction = opposite.get(self.movement_direction, 'S')
                    self.log_to_gui(f"🧱 Avoiding obstacle, new direction: {self.movement_direction}")
                    return False
            
            # Auto exploración si está habilitada
            if self.auto_exploration:
                if self.auto_explore():
                    pass  # La dirección ya se actualizó en auto_explore
            
            # Cambio automático de dirección cada 15 segundos
            if current_time - self.direction_change_timer > self.direction_change_interval:
                directions = ['S', 'D', 'W', 'A']
                current_index = directions.index(self.movement_direction)
                self.movement_direction = directions[(current_index + 1) % len(directions)]
                self.direction_change_timer = current_time
                self.movement_attempts = 0  # Resetear intentos
                self.log_to_gui(f"🔄 Auto direction change: {self.movement_direction}")
            
            # Evitar escaleras (método anterior como backup)
            if self.avoid_stairs():
                self.direction_change_timer = current_time  # Resetear timer
            
            if not self.activate_tibia_window():
                return False
            
            # Enviar movimiento
            keyboard.press_and_release(self.movement_direction.lower())
            self.log_to_gui(f"🚶 Moving {self.movement_direction}")
            
            # Actualizar posición y timer
            self.last_position = self.get_character_position()
            self.last_movement = current_time
            
            # Actualizar posición para mapping
            self.update_position()
            
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
    
    def check_position_change(self):
        """Verificar si la posición realmente cambió"""
        try:
            current_time = time.time()
            if current_time - self.last_position_check < self.position_check_interval:
                return True  # No verificar tan frecuentemente
            
            current_position = self.get_character_position()
            self.last_position_check = current_time
            
            # Agregar posición al historial
            self.position_history.append(current_position)
            if len(self.position_history) > 3:  # Mantener solo las últimas 3 posiciones
                self.position_history.pop(0)
            
            # Verificar si la posición cambió
            if len(self.position_history) >= 2:
                last_pos = self.position_history[-2]
                current_pos = self.position_history[-1]
                
                # Calcular distancia entre posiciones
                distance = abs(current_pos[0] - last_pos[0]) + abs(current_pos[1] - last_pos[1])
                
                if distance > 0:
                    # ¡La posición cambió! Resetear contadores
                    self.movement_attempts = 0
                    self.stuck_counter = 0
                    self.log_to_gui(f"✅ Position changed! Distance: {distance}")
                    return True
                else:
                    # La posición no cambió
                    self.movement_attempts += 1
                    self.log_to_gui(f"🚧 Position unchanged! Attempts: {self.movement_attempts}/{self.max_movement_attempts}")
                    
                    if self.movement_attempts >= self.max_movement_attempts:
                        self.log_to_gui("🚨 STUCK DETECTED! Trying different direction...")
                        return False
            
            return True
            
        except Exception as e:
            self.log_to_gui(f"❌ Error checking position: {e}")
            return True
    
    def try_all_movement_keys(self):
        """Probar todas las teclas de movimiento para encontrar una que funcione"""
        try:
            movement_keys = ['w', 'a', 's', 'd']
            current_key = self.movement_direction.lower()
            
            # Remover la tecla actual de la lista
            if current_key in movement_keys:
                movement_keys.remove(current_key)
            
            # Probar cada tecla
            for key in movement_keys:
                self.log_to_gui(f"🔄 Trying movement key: {key.upper()}")
                
                if not self.activate_tibia_window():
                    continue
                
                # Enviar tecla
                keyboard.press_and_release(key)
                time.sleep(0.5)  # Esperar un poco
                
                # Verificar si la posición cambió
                old_position = self.get_character_position()
                time.sleep(1.0)  # Esperar más tiempo
                new_position = self.get_character_position()
                
                # Calcular distancia
                distance = abs(new_position[0] - old_position[0]) + abs(new_position[1] - old_position[1])
                
                if distance > 0:
                    # ¡Esta tecla funciona!
                    self.movement_direction = key.upper()
                    self.movement_attempts = 0
                    self.stuck_counter = 0
                    self.log_to_gui(f"✅ Found working key: {key.upper()} (Distance: {distance})")
                    return True
                else:
                    self.log_to_gui(f"❌ Key {key.upper()} didn't work")
            
            # Si ninguna tecla funcionó, probar dirección opuesta
            opposite = {'S': 'W', 'W': 'S', 'A': 'D', 'D': 'A'}
            opposite_key = opposite.get(self.movement_direction, 'S')
            self.movement_direction = opposite_key
            self.log_to_gui(f"🔄 Trying opposite direction: {opposite_key}")
            
            return False
            
        except Exception as e:
            self.log_to_gui(f"❌ Error trying movement keys: {e}")
            return False
    
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
        """Ejecutar el bot principal"""
        try:
            self.log_to_gui("🚀 Iniciando NopalBot Elite Knight...")
            self.log_to_gui(f"⚔️ Auto Ataque: {'HABILITADO' if self.auto_attack_enabled else 'DESHABILITADO'}")
            self.log_to_gui(f"🚶 Auto Caminar: {'HABILITADO' if self.auto_walk_enabled else 'DESHABILITADO'}")
            self.log_to_gui(f"❤️ Auto Curar: {'HABILITADO' if self.auto_heal_enabled else 'DESHABILITADO'}")
            self.log_to_gui(f"🔮 Auto Mana: {'HABILITADO' if self.auto_mana_enabled else 'DESHABILITADO'}")
            self.log_to_gui(f"🍖 Auto Comida: {'HABILITADO' if self.auto_food_enabled else 'DESHABILITADO'}")
            self.log_to_gui(f"⚡ Utani Hur: {'HABILITADO' if self.auto_utani_hur_enabled else 'DESHABILITADO'}")
            self.log_to_gui(f"⚔️ Exori: {'HABILITADO' if self.auto_exori_enabled else 'DESHABILITADO'}")
            self.log_to_gui(f"⚔️ Exori Ico: {'HABILITADO' if self.auto_exori_ico_enabled else 'DESHABILITADO'}")
            self.log_to_gui(f"⚔️ Exori Gran: {'HABILITADO' if self.auto_exori_gran_enabled else 'DESHABILITADO'}")
            self.log_to_gui(f"🔥 Utito Tempo: {'HABILITADO' if self.auto_utito_tempo_enabled else 'DESHABILITADO'}")
            self.log_to_gui(f"🗺️ Mapping: {'HABILITADO' if self.mapping_enabled else 'DESHABILITADO'}")
            self.log_to_gui(f"🔍 Auto Exploración: {'HABILITADO' if self.auto_exploration else 'DESHABILITADO'}")
            self.log_to_gui(f"👁️ Computer Vision: {'HABILITADO' if self.computer_vision_enabled else 'DESHABILITADO'}")
            self.log_to_gui("🎮 Presiona F11 para pausar/reanudar + lanzar hechizos, F10 para detener")
            
            # Encontrar ventana de Tibia
            if not self.find_tibia_window():
                self.log_to_gui("❌ ¡Ventana de Tibia no encontrada!")
                return
            
            self.log_to_gui("✅ Ventana de Tibia encontrada!")
            
            # Inicializar variables de tiempo
            last_save_time = time.time()
            save_interval = 60  # Guardar cada 60 segundos
            
            while self.running:
                try:
                    if self.paused:
                        time.sleep(0.1)
                        continue
                    
                    # Auto curación (prioridad alta)
                    if self.auto_heal_enabled:
                        self.auto_heal()
                    
                    # Auto mana
                    if self.auto_mana_enabled:
                        self.use_mana_potion()
                    
                    # Auto comida
                    if self.auto_food_enabled:
                        self.use_food()
                    
                    # Hechizos de Elite Knight
                    if self.auto_utani_hur_enabled:
                        self.cast_utani_hur()
                    
                    if self.auto_exori_enabled:
                        self.cast_exori()
                    
                    if self.auto_exori_ico_enabled:
                        self.cast_exori_ico()
                    
                    if self.auto_exori_gran_enabled:
                        self.cast_exori_gran()
                    
                    if self.auto_utito_tempo_enabled:
                        self.cast_utito_tempo()
                    
                    # Auto ataque
                    if self.auto_attack_enabled:
                        self.simple_attack()
                    
                    # Auto caminar
                    if self.auto_walk_enabled:
                        self.smart_walk()
                    
                    # Guardar datos del mapa periódicamente
                    current_time = time.time()
                    if current_time - last_save_time > save_interval:
                        if self.mapping_enabled:
                            self.save_map_data()
                        last_save_time = current_time
                    
                    time.sleep(0.1)  # Pequeña pausa para no saturar CPU
                    
                except Exception as e:
                    self.log_to_gui(f"❌ Error en loop principal: {e}")
                    time.sleep(1)
            
            # Guardar datos finales
            if self.mapping_enabled:
                self.save_map_data()
            
            self.log_to_gui("🏁 Bot finalizado")
            
        except Exception as e:
            self.log_to_gui(f"❌ Error crítico en run_bot: {e}")

class NopalBotEliteKnightGUI:
    """GUI especializada para Elite Knight - NopalBot by Pikos Nopal"""
    
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("NopalBot Elite Knight - by Pikos Nopal")
        self.root.geometry("800x900")
        self.root.resizable(True, True)
        
        # Variables de control
        self.auto_attack_enabled = False
        self.auto_walk_enabled = False
        self.auto_heal_enabled = False
        self.auto_mana_enabled = False
        self.auto_food_enabled = False
        self.auto_utani_hur_enabled = False
        self.auto_exori_enabled = False
        self.auto_exori_ico_enabled = False
        self.auto_exori_gran_enabled = False
        self.auto_utito_tempo_enabled = False
        self.heal_with_spell = True
        self.mapping_enabled = False
        self.auto_exploration_enabled = False
        self.computer_vision_enabled = False
        
        # Bot instance
        self.bot = None
        self.bot_thread = None
        self.overlay = None
        
        self.setup_gui()
        
    def setup_gui(self):
        """Configurar la interfaz gráfica"""
        # Frame principal
        main_frame = ctk.CTkFrame(self.root)
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Título principal
        title_label = ctk.CTkLabel(main_frame, text="⚔️ NOPALBOT ELITE KNIGHT ⚔️", 
                                  font=ctk.CTkFont(size=24, weight="bold"))
        title_label.pack(pady=10)
        
        subtitle_label = ctk.CTkLabel(main_frame, text="by Pikos Nopal", 
                                     font=ctk.CTkFont(size=14))
        subtitle_label.pack(pady=5)
        
        # Frame de controles principales
        controls_frame = ctk.CTkFrame(main_frame)
        controls_frame.pack(fill='x', padx=10, pady=10)
        
        controls_title = ctk.CTkLabel(controls_frame, text="🎮 CONTROLES PRINCIPALES", 
                                     font=ctk.CTkFont(size=18, weight="bold"))
        controls_title.pack(pady=10)
        
        # Botones principales
        main_buttons_frame = ctk.CTkFrame(controls_frame)
        main_buttons_frame.pack(pady=10)
        
        # Fila 1: Ataque y Movimiento
        row1_frame = ctk.CTkFrame(main_buttons_frame)
        row1_frame.pack(pady=5)
        
        self.attack_button = ctk.CTkButton(row1_frame, text="⚔️ AUTO ATAQUE", 
                                          command=self.toggle_auto_attack,
                                          fg_color="red", hover_color="#8B0000",
                                          width=150, height=40)
        self.attack_button.pack(side='left', padx=5)
        Tooltip(self.attack_button, "Activa el ataque automático con CTRL+SPACE")
        
        self.walk_button = ctk.CTkButton(row1_frame, text="🚶 AUTO CAMINAR", 
                                        command=self.toggle_auto_walk,
                                        fg_color="blue", hover_color="#00008B",
                                        width=150, height=40)
        self.walk_button.pack(side='left', padx=5)
        Tooltip(self.walk_button, "Activa el movimiento automático con WASD")
        
        # Fila 2: Curación y Mana
        row2_frame = ctk.CTkFrame(main_buttons_frame)
        row2_frame.pack(pady=5)
        
        self.heal_button = ctk.CTkButton(row2_frame, text="❤️ AUTO CURAR", 
                                        command=self.toggle_auto_heal,
                                        fg_color="green", hover_color="#006400",
                                        width=150, height=40)
        self.heal_button.pack(side='left', padx=5)
        Tooltip(self.heal_button, "Cura automáticamente cuando HP < 40%")
        
        self.mana_button = ctk.CTkButton(row2_frame, text="🔮 AUTO MANA", 
                                        command=self.toggle_auto_mana,
                                        fg_color="purple", hover_color="#4B0082",
                                        width=150, height=40)
        self.mana_button.pack(side='left', padx=5)
        Tooltip(self.mana_button, "Usa pociones de mana cuando Mana < 30%")
        
        self.food_button = ctk.CTkButton(row2_frame, text="🍖 AUTO COMIDA", 
                                        command=self.toggle_auto_food,
                                        fg_color="orange", hover_color="#FF8C00",
                                        width=150, height=40)
        self.food_button.pack(side='left', padx=5)
        Tooltip(self.food_button, "Come automáticamente cuando HP < 50%")
        
        # Frame de hechizos de Elite Knight
        spells_frame = ctk.CTkFrame(main_frame)
        spells_frame.pack(fill='x', padx=10, pady=10)
        
        spells_title = ctk.CTkLabel(spells_frame, text="⚡ HECHIZOS ELITE KNIGHT", 
                                   font=ctk.CTkFont(size=18, weight="bold"))
        spells_title.pack(pady=10)
        
        # Fila 1 de hechizos
        spells_row1 = ctk.CTkFrame(spells_frame)
        spells_row1.pack(pady=5)
        
        self.utani_hur_button = ctk.CTkButton(spells_row1, text="⚡ UTANI HUR", 
                                             command=self.toggle_utani_hur,
                                             fg_color="yellow", hover_color="#FFD700",
                                             width=120, height=35)
        self.utani_hur_button.pack(side='left', padx=3)
        Tooltip(self.utani_hur_button, "Lanza Utani Hur (Haste) cada 30 segundos")
        
        self.exori_button = ctk.CTkButton(spells_row1, text="⚔️ EXORI", 
                                         command=self.toggle_exori,
                                         fg_color="red", hover_color="#8B0000",
                                         width=120, height=35)
        self.exori_button.pack(side='left', padx=3)
        Tooltip(self.exori_button, "Lanza Exori (ataque área) cada 8 segundos")
        
        self.exori_ico_button = ctk.CTkButton(spells_row1, text="⚔️ EXORI ICO", 
                                             command=self.toggle_exori_ico,
                                             fg_color="darkred", hover_color="#660000",
                                             width=120, height=35)
        self.exori_ico_button.pack(side='left', padx=3)
        Tooltip(self.exori_ico_button, "Lanza Exori Ico (ataque área mejorado) cada 6 segundos")
        
        # Fila 2 de hechizos
        spells_row2 = ctk.CTkFrame(spells_frame)
        spells_row2.pack(pady=5)
        
        self.exori_gran_button = ctk.CTkButton(spells_row2, text="⚔️ EXORI GRAN", 
                                              command=self.toggle_exori_gran,
                                              fg_color="darkred", hover_color="#660000",
                                              width=120, height=35)
        self.exori_gran_button.pack(side='left', padx=3)
        Tooltip(self.exori_gran_button, "Lanza Exori Gran (ataque área grande) cada 12 segundos")
        
        self.utito_tempo_button = ctk.CTkButton(spells_row2, text="🔥 UTITO TEMPO", 
                                               command=self.toggle_utito_tempo,
                                               fg_color="orange", hover_color="#FF8C00",
                                               width=120, height=35)
        self.utito_tempo_button.pack(side='left', padx=3)
        Tooltip(self.utito_tempo_button, "Lanza Utito Tempo (Berserk) cada 60 segundos")
        
        # Frame de opciones avanzadas
        advanced_frame = ctk.CTkFrame(main_frame)
        advanced_frame.pack(fill='x', padx=10, pady=10)
        
        advanced_title = ctk.CTkLabel(advanced_frame, text="🔧 OPCIONES AVANZADAS", 
                                     font=ctk.CTkFont(size=18, weight="bold"))
        advanced_title.pack(pady=10)
        
        # Fila de opciones avanzadas
        advanced_row = ctk.CTkFrame(advanced_frame)
        advanced_row.pack(pady=5)
        
        self.mapping_button = ctk.CTkButton(advanced_row, text="🗺️ MAPPING", 
                                           command=self.toggle_mapping,
                                           fg_color="cyan", hover_color="#008B8B",
                                           width=120, height=35)
        self.mapping_button.pack(side='left', padx=3)
        Tooltip(self.mapping_button, "Mapea las coordenadas visitadas")
        
        self.exploration_button = ctk.CTkButton(advanced_row, text="🔍 AUTO EXPLORAR", 
                                               command=self.toggle_auto_exploration,
                                               fg_color="green", hover_color="#006400",
                                               width=120, height=35)
        self.exploration_button.pack(side='left', padx=3)
        Tooltip(self.exploration_button, "Explora automáticamente áreas no visitadas")
        
        self.vision_button = ctk.CTkButton(advanced_row, text="👁️ COMPUTER VISION", 
                                          command=self.toggle_computer_vision,
                                          fg_color="purple", hover_color="#4B0082",
                                          width=120, height=35)
        self.vision_button.pack(side='left', padx=3)
        Tooltip(self.vision_button, "Detecta enemigos, escaleras y obstáculos visualmente")
        
        # Frame de opciones de curación
        heal_options_frame = ctk.CTkFrame(main_frame)
        heal_options_frame.pack(fill='x', padx=10, pady=10)
        
        heal_options_title = ctk.CTkLabel(heal_options_frame, text="💊 OPCIONES DE CURACIÓN", 
                                         font=ctk.CTkFont(size=16, weight="bold"))
        heal_options_title.pack(pady=5)
        
        heal_buttons_frame = ctk.CTkFrame(heal_options_frame)
        heal_buttons_frame.pack(pady=5)
        
        self.heal_spell_button = ctk.CTkButton(heal_buttons_frame, text="🔮 CURAR CON HECHIZO", 
                                              command=self.toggle_heal_with_spell,
                                              fg_color="blue", hover_color="#00008B",
                                              width=150, height=35)
        self.heal_spell_button.pack(side='left', padx=5)
        Tooltip(self.heal_spell_button, "Usa hechizos de curación (Exura)")
        
        self.heal_potion_button = ctk.CTkButton(heal_buttons_frame, text="🧪 CURAR CON POCIÓN", 
                                               command=self.toggle_heal_with_potion,
                                               fg_color="orange", hover_color="#FF8C00",
                                               width=150, height=35)
        self.heal_potion_button.pack(side='left', padx=5)
        Tooltip(self.heal_potion_button, "Usa pociones de vida")
        
        # Frame de control principal
        control_frame = ctk.CTkFrame(main_frame)
        control_frame.pack(fill='x', padx=10, pady=10)
        
        control_title = ctk.CTkLabel(control_frame, text="🎮 CONTROL PRINCIPAL", 
                                    font=ctk.CTkFont(size=18, weight="bold"))
        control_title.pack(pady=10)
        
        control_buttons_frame = ctk.CTkFrame(control_frame)
        control_buttons_frame.pack(pady=10)
        
        self.start_button = ctk.CTkButton(control_buttons_frame, text="🚀 INICIAR BOT", 
                                         command=self.start_bot,
                                         fg_color="green", hover_color="#006400",
                                         width=150, height=50)
        self.start_button.pack(side='left', padx=10)
        Tooltip(self.start_button, "Inicia el bot con las opciones seleccionadas")
        
        self.stop_button = ctk.CTkButton(control_buttons_frame, text="🛑 DETENER BOT", 
                                        command=self.stop_bot,
                                        fg_color="red", hover_color="#8B0000",
                                        width=150, height=50)
        self.stop_button.pack(side='left', padx=10)
        Tooltip(self.stop_button, "Detiene el bot completamente")
        
        self.overlay_button = ctk.CTkButton(control_buttons_frame, text="📊 MOSTRAR OVERLAY", 
                                           command=self.toggle_overlay,
                                           fg_color="purple", hover_color="#4B0082",
                                           width=150, height=50)
        self.overlay_button.pack(side='left', padx=10)
        Tooltip(self.overlay_button, "Muestra/oculta el overlay de logs en pantalla")
        
        # Frame de información
        info_frame = ctk.CTkFrame(main_frame)
        info_frame.pack(fill='x', padx=10, pady=10)
        
        info_title = ctk.CTkLabel(info_frame, text="ℹ️ INFORMACIÓN", 
                                 font=ctk.CTkFont(size=16, weight="bold"))
        info_title.pack(pady=5)
        
        info_text = """
        🎯 Ataque: CTRL+SPACE    🎯 Siguiente Target: SPACE
        🚶 Movimiento: WASD       ⏸️ Pausar/Reanudar: F11
        🛑 Detener Bot: F10       🍖 Comida: F12
        ⚡ Haste: F4              ⚔️ Exori: F5
        ⚔️ Exori Ico: F6         ⚔️ Exori Gran: F7
        🔥 Berserk: F8           🔮 Mana: F3
        """
        
        info_label = ctk.CTkLabel(info_frame, text=info_text, 
                                 font=ctk.CTkFont(size=12))
        info_label.pack(pady=5)
        
        # Frame de logs
        log_frame = ctk.CTkFrame(main_frame)
        log_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        log_title = ctk.CTkLabel(log_frame, text="📊 LOGS DEL BOT", 
                                font=ctk.CTkFont(size=16, weight="bold"))
        log_title.pack(pady=5)
        
        self.log_text = ctk.CTkTextbox(log_frame, height=200)
        self.log_text.pack(fill='both', expand=True, padx=5, pady=5)
        
    def toggle_auto_attack(self):
        self.auto_attack_enabled = not self.auto_attack_enabled
        status = "ENABLED" if self.auto_attack_enabled else "DISABLED"
        color = "green" if self.auto_attack_enabled else "red"
        self.attack_button.configure(fg_color=color)
        self.log_to_gui(f"⚔️ Auto Attack {status}")
        
    def toggle_auto_walk(self):
        self.auto_walk_enabled = not self.auto_walk_enabled
        status = "ENABLED" if self.auto_walk_enabled else "DISABLED"
        color = "green" if self.auto_walk_enabled else "blue"
        self.walk_button.configure(fg_color=color)
        self.log_to_gui(f"🚶 Auto Walk {status}")
        
    def toggle_auto_heal(self):
        self.auto_heal_enabled = not self.auto_heal_enabled
        status = "ENABLED" if self.auto_heal_enabled else "DISABLED"
        color = "green" if self.auto_heal_enabled else "gray"
        self.heal_button.configure(fg_color=color)
        self.log_to_gui(f"❤️ Auto Heal {status}")

    def toggle_auto_mana(self):
        self.auto_mana_enabled = not self.auto_mana_enabled
        status = "ENABLED" if self.auto_mana_enabled else "DISABLED"
        color = "green" if self.auto_mana_enabled else "purple"
        self.mana_button.configure(fg_color=color)
        self.log_to_gui(f"🔮 Auto Mana {status}")

    def toggle_auto_food(self):
        self.auto_food_enabled = not self.auto_food_enabled
        status = "ENABLED" if self.auto_food_enabled else "DISABLED"
        color = "green" if self.auto_food_enabled else "orange"
        self.food_button.configure(fg_color=color)
        self.log_to_gui(f"🍖 Auto Food {status}")

    def toggle_utani_hur(self):
        self.auto_utani_hur_enabled = not self.auto_utani_hur_enabled
        status = "ENABLED" if self.auto_utani_hur_enabled else "DISABLED"
        color = "green" if self.auto_utani_hur_enabled else "yellow"
        self.utani_hur_button.configure(fg_color=color)
        self.log_to_gui(f"⚡ Utani Hur {status}")

    def toggle_exori(self):
        self.auto_exori_enabled = not self.auto_exori_enabled
        status = "ENABLED" if self.auto_exori_enabled else "DISABLED"
        color = "green" if self.auto_exori_enabled else "red"
        self.exori_button.configure(fg_color=color)
        self.log_to_gui(f"⚔️ Exori {status}")

    def toggle_exori_ico(self):
        self.auto_exori_ico_enabled = not self.auto_exori_ico_enabled
        status = "ENABLED" if self.auto_exori_ico_enabled else "DISABLED"
        color = "green" if self.auto_exori_ico_enabled else "darkred"
        self.exori_ico_button.configure(fg_color=color)
        self.log_to_gui(f"⚔️ Exori Ico {status}")

    def toggle_exori_gran(self):
        self.auto_exori_gran_enabled = not self.auto_exori_gran_enabled
        status = "ENABLED" if self.auto_exori_gran_enabled else "DISABLED"
        color = "green" if self.auto_exori_gran_enabled else "darkred"
        self.exori_gran_button.configure(fg_color=color)
        self.log_to_gui(f"⚔️ Exori Gran {status}")

    def toggle_utito_tempo(self):
        self.auto_utito_tempo_enabled = not self.auto_utito_tempo_enabled
        status = "ENABLED" if self.auto_utito_tempo_enabled else "DISABLED"
        color = "green" if self.auto_utito_tempo_enabled else "orange"
        self.utito_tempo_button.configure(fg_color=color)
        self.log_to_gui(f"🔥 Utito Tempo {status}")

    def toggle_mapping(self):
        self.mapping_enabled = not self.mapping_enabled
        status = "ENABLED" if self.mapping_enabled else "DISABLED"
        color = "green" if self.mapping_enabled else "gray"
        self.mapping_button.configure(fg_color=color)
        self.log_to_gui(f"🗺️ Mapping {status}")

    def toggle_auto_exploration(self):
        self.auto_exploration_enabled = not self.auto_exploration_enabled
        status = "ENABLED" if self.auto_exploration_enabled else "DISABLED"
        color = "green" if self.auto_exploration_enabled else "gray"
        self.exploration_button.configure(fg_color=color)
        self.log_to_gui(f"🔍 Auto Exploration {status}")
        
    def toggle_computer_vision(self):
        self.computer_vision_enabled = not self.computer_vision_enabled
        status = "ENABLED" if self.computer_vision_enabled else "DISABLED"
        color = "green" if self.computer_vision_enabled else "gray"
        self.vision_button.configure(fg_color=color)
        self.log_to_gui(f"👁️ Computer Vision {status}")
        
    def toggle_heal_with_spell(self):
        self.heal_with_spell = True
        self.heal_spell_button.configure(fg_color="blue")
        self.heal_potion_button.configure(fg_color="gray")
        self.log_to_gui("🔮 Healing with SPELL enabled")
        
    def toggle_heal_with_potion(self):
        self.heal_with_spell = False
        self.heal_spell_button.configure(fg_color="gray")
        self.heal_potion_button.configure(fg_color="orange")
        self.log_to_gui("🧪 Healing with POTION enabled")
        
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
            self.bot = NopalBotEliteKnight(self.log_to_gui) # Pass the GUI callback
            
            # Configurar controles individuales
            self.bot.auto_attack_enabled = self.auto_attack_enabled
            self.bot.auto_walk_enabled = self.auto_walk_enabled
            self.bot.auto_heal_enabled = self.auto_heal_enabled
            self.bot.auto_mana_enabled = self.auto_mana_enabled
            self.bot.auto_food_enabled = self.auto_food_enabled
            self.bot.auto_utani_hur_enabled = self.auto_utani_hur_enabled
            self.bot.auto_exori_enabled = self.auto_exori_enabled
            self.bot.auto_exori_ico_enabled = self.auto_exori_ico_enabled
            self.bot.auto_exori_gran_enabled = self.auto_exori_gran_enabled
            self.bot.auto_utito_tempo_enabled = self.auto_utito_tempo_enabled
            self.bot.heal_with_spell = self.heal_with_spell
            self.bot.mapping_enabled = self.mapping_enabled
            self.bot.auto_exploration = self.auto_exploration_enabled
            self.bot.computer_vision_enabled = self.computer_vision_enabled
            
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
        if self.overlay is None: # Initialize overlay if not already
            self.overlay = TransparentOverlay(self.root)
            
        if self.overlay.is_visible:
            self.overlay.hide()
            self.overlay_button.configure(text="📊 MOSTRAR OVERLAY")
        else:
            self.overlay.show()
            self.overlay_button.configure(text="📊 OCULTAR OVERLAY")
            
    def run(self):
        self.root.mainloop()

def main():
    app = NopalBotEliteKnightGUI()
    app.run()

if __name__ == "__main__":
    main() 