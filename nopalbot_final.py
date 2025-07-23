import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import customtkinter as ctk
import threading
import time
import random
import logging
import os
import cv2
import numpy as np
import pyautogui
import keyboard
import win32gui
import win32con
import win32api
from datetime import datetime
from pathlib import Path
import json
from PIL import Image, ImageTk
import psutil

# Configurar CustomTkinter
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class TransparentOverlay:
    def __init__(self, parent):
        self.parent = parent
        self.overlay = None
        self.is_visible = False
        
    def create_overlay(self):
        if self.overlay:
            self.overlay.destroy()
            
        self.overlay = tk.Toplevel(self.parent)
        self.overlay.title("NopalBot Overlay")
        self.overlay.geometry("400x300+1400+50")  # Esquina derecha
        self.overlay.configure(bg='black')
        self.overlay.attributes('-alpha', 0.8)  # Transparencia
        self.overlay.attributes('-topmost', True)
        self.overlay.overrideredirect(True)  # Sin bordes
        self.overlay.attributes('-transparentcolor', 'black')
        
        # Hacer no clickeable
        self.overlay.wm_attributes("-disabled", True)
        
        # Frame principal
        main_frame = tk.Frame(self.overlay, bg='black', bd=2, relief='solid')
        main_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Título
        title_label = tk.Label(main_frame, text="🤖 NOPALBOT STATUS", 
                              font=('Arial', 12, 'bold'), 
                              fg='yellow', bg='black')
        title_label.pack(pady=5)
        
        # Texto del log
        self.log_text = tk.Text(main_frame, height=12, width=45, 
                               bg='black', fg='yellow', 
                               font=('Consolas', 9),
                               insertbackground='yellow',
                               selectbackground='darkgreen')
        self.log_text.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Scrollbar
        scrollbar = tk.Scrollbar(main_frame, command=self.log_text.yview)
        scrollbar.pack(side='right', fill='y')
        self.log_text.config(yscrollcommand=scrollbar.set)
        
    def show(self):
        if not self.overlay:
            self.create_overlay()
        self.overlay.deiconify()
        self.is_visible = True
        
    def hide(self):
        if self.overlay:
            self.overlay.withdraw()
        self.is_visible = False
        
    def add_log(self, message):
        if self.overlay and self.is_visible:
            timestamp = datetime.now().strftime("%H:%M:%S")
            log_entry = f"[{timestamp}] {message}\n"
            
            self.log_text.insert(tk.END, log_entry)
            self.log_text.see(tk.END)
            
            # Limitar líneas
            lines = self.log_text.get("1.0", tk.END).split('\n')
            if len(lines) > 50:
                self.log_text.delete("1.0", "2.0")

class NopalBotIntelligent:
    def __init__(self, gui_callback=None):
        self.setup_logging()
        self.setup_hotkeys()
        self.gui_callback = gui_callback
        self.health = 100
        self.mana = 100
        self.level = 1
        self.character_name = "Unknown"
        self.character_vocation = "Druid"
        self.heal_threshold = random.randint(20, 40)
        self.mana_threshold = random.randint(20, 40)
        self.spell_mana_threshold = 60
        self.last_enemy_death = 0
        self.enemy_detected = False
        self.combat_mode = False
        self.movement_direction = 0
        self.last_movement = 0
        self.running = False
        self.paused = False
        
        # Contadores de potiones
        self.health_potions = 10  # Simular 10 potiones
        self.mana_potions = 10    # Simular 10 potiones
        self.last_potion_check = 0
        
        # Estado de movimiento
        self.movement_state = "forward"  # forward, stuck, avoiding
        self.stuck_counter = 0
        self.last_position = None
        
        # Configuración para druida
        self.hotkeys = {
            'attack': 'CTRL+SPACE',  # CTRL + SPACE para atacar
            'next_target': 'SPACE',  # SPACE para seleccionar siguiente objetivo
            'heal': 'F1',
            'mana': 'F2', 
            'spell1': 'F3',  # Exori vis
            'spell2': 'F4',  # Exura
            'loot': 'F5',
            'quick_loot': '0',
            'movement': ['W', 'A', 'S', 'D'],
            'face_enemy': 'CTRL'
        }
        
        # Configurar pyautogui
        pyautogui.FAILSAFE = False
        pyautogui.PAUSE = 0.1
        
    def setup_logging(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('nopalbot.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        
    def setup_hotkeys(self):
        # Hotkeys globales para pausar/parar
        keyboard.add_hotkey('f12', self.stop_bot)
        keyboard.add_hotkey('f11', self.toggle_pause)
        
    def log_to_gui(self, message):
        self.logger.info(message)
        if self.gui_callback:
            self.gui_callback(message)
            
    def find_tibia_window(self):
        """Busca la ventana de Tibia y la activa"""
        try:
            # Buscar ventana de Tibia
            windows = pyautogui.getWindowsWithTitle("Tibia")
            if windows:
                self.tibia_window = windows[0]
                self.tibia_window.activate()
                time.sleep(0.5)
                
                # Obtener coordenadas de la ventana
                self.tibia_left = self.tibia_window.left
                self.tibia_top = self.tibia_window.top
                self.tibia_width = self.tibia_window.width
                self.tibia_height = self.tibia_window.height
                
                self.log_to_gui(f"🎮 Tibia window found: {self.tibia_window.title}")
                self.log_to_gui(f"📍 Position: ({self.tibia_left}, {self.tibia_top})")
                self.log_to_gui(f"📏 Size: {self.tibia_width}x{self.tibia_height}")
                
                # Intentar obtener nombre del personaje
                self.detect_character_info()
                return True
            else:
                self.log_to_gui("❌ Tibia window not found!")
                return False
        except Exception as e:
            self.log_to_gui(f"❌ Error finding Tibia: {e}")
            return False
            
    def detect_character_info(self):
        """Detecta información del personaje"""
        try:
            # Activar ventana de Tibia
            self.tibia_window.activate()
            time.sleep(0.2)
            
            # Capturar región donde aparece el nombre del personaje
            # (aproximadamente en la parte superior de la ventana)
            name_region = (
                self.tibia_left + 100,
                self.tibia_top + 50,
                200,
                30
            )
            
            screenshot = pyautogui.screenshot(region=name_region)
            # Aquí podrías usar OCR para leer el nombre
            # Por ahora usamos un nombre por defecto
            self.character_name = "Roboperra Nopal"
            self.character_vocation = "Druid"
            
            self.log_to_gui(f"👤 Character: {self.character_name}")
            self.log_to_gui(f"🎭 Vocation: {self.character_vocation}")
            
        except Exception as e:
            self.log_to_gui(f"⚠️ Could not detect character info: {e}")
            
    def detect_health_mana_from_screen(self):
        """Detecta vida y mana reales desde la pantalla"""
        try:
            if not hasattr(self, 'tibia_window'):
                return False
                
            # Activar ventana de Tibia
            self.tibia_window.activate()
            time.sleep(0.1)
            
            # Capturar región donde aparecen las barras de vida/mana
            # (aproximadamente en la parte inferior de la ventana)
            bars_region = (
                self.tibia_left + 50,
                self.tibia_top + self.tibia_height - 100,
                200,
                50
            )
            
            screenshot = pyautogui.screenshot(region=bars_region)
            img = np.array(screenshot)
            
            # Convertir a HSV para detectar colores
            hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
            
            # Detectar barra de vida (rojo)
            lower_red = np.array([0, 100, 100])
            upper_red = np.array([10, 255, 255])
            health_mask = cv2.inRange(hsv, lower_red, upper_red)
            health_pixels = cv2.countNonZero(health_mask)
            
            # Detectar barra de mana (azul)
            lower_blue = np.array([100, 100, 100])
            upper_blue = np.array([130, 255, 255])
            mana_mask = cv2.inRange(hsv, lower_blue, upper_blue)
            mana_pixels = cv2.countNonZero(mana_mask)
            
            # Calcular porcentajes (aproximado)
            total_pixels = health_mask.shape[0] * health_mask.shape[1]
            self.health = min(100, max(0, int((health_pixels / total_pixels) * 100)))
            self.mana = min(100, max(0, int((mana_pixels / total_pixels) * 100)))
            
            self.log_to_gui(f"❤️ Health detected: {self.health}%")
            self.log_to_gui(f"🔮 Mana detected: {self.mana}%")
            
            return True
            
        except Exception as e:
            self.log_to_gui(f"❌ Error detecting health/mana: {e}")
            return False
            
    def check_potions_available(self):
        """Verifica si hay potiones disponibles"""
        try:
            current_time = time.time()
            if current_time - self.last_potion_check > 5.0:  # Verificar cada 5 segundos
                
                # Simular detección de potiones (en un bot real, esto sería OCR)
                # Por ahora usamos simulación
                if random.random() < 0.1:  # 10% chance de quedarse sin potiones
                    if self.health_potions <= 0:
                        self.health_potions = random.randint(5, 15)
                        self.log_to_gui(f"💊 Found {self.health_potions} health potions!")
                        
                if random.random() < 0.1:  # 10% chance de quedarse sin potiones
                    if self.mana_potions <= 0:
                        self.mana_potions = random.randint(5, 15)
                        self.log_to_gui(f"💊 Found {self.mana_potions} mana potions!")
                        
                self.last_potion_check = current_time
                
        except Exception as e:
            self.log_to_gui(f"❌ Error checking potions: {e}")
            
    def find_closest_enemy_visual(self):
        """Detección visual de enemigos usando OpenCV SOLO dentro de Tibia"""
        try:
            if not hasattr(self, 'tibia_window'):
                return False
                
            # Activar ventana de Tibia
            self.tibia_window.activate()
            time.sleep(0.1)
            
            # Capturar SOLO la región de Tibia
            screenshot = pyautogui.screenshot(region=(
                self.tibia_left, 
                self.tibia_top, 
                self.tibia_width, 
                self.tibia_height
            ))
            
            img = np.array(screenshot)
            img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
            
            # Convertir a HSV para mejor detección de colores
            hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
            
            # Detectar enemigos por color (rojo, marrón, etc.)
            # Rango para rojo (enemigos)
            lower_red1 = np.array([0, 100, 100])
            upper_red1 = np.array([10, 255, 255])
            lower_red2 = np.array([160, 100, 100])
            upper_red2 = np.array([180, 255, 255])
            
            # Rango para marrón (trolls, etc.)
            lower_brown = np.array([10, 100, 20])
            upper_brown = np.array([20, 255, 200])
            
            # Crear máscaras
            mask_red1 = cv2.inRange(hsv, lower_red1, upper_red1)
            mask_red2 = cv2.inRange(hsv, lower_red2, upper_red2)
            mask_brown = cv2.inRange(hsv, lower_brown, upper_brown)
            
            # Combinar máscaras
            mask = mask_red1 + mask_red2 + mask_brown
            
            # Encontrar contornos
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            if contours:
                # Encontrar el contorno más grande (enemigo más cercano)
                largest_contour = max(contours, key=cv2.contourArea)
                
                if cv2.contourArea(largest_contour) > 100:  # Filtrar ruido
                    # Calcular centro del enemigo
                    M = cv2.moments(largest_contour)
                    if M["m00"] != 0:
                        cx = int(M["m10"] / M["m00"])
                        cy = int(M["m01"] / M["m00"])
                        
                        # Convertir a coordenadas globales
                        global_x = self.tibia_left + cx
                        global_y = self.tibia_top + cy
                        
                        self.log_to_gui(f"🎯 Enemy found at ({global_x}, {global_y}) within Tibia")
                        return (global_x, global_y)
                        
            return False
            
        except Exception as e:
            self.log_to_gui(f"❌ Error in visual detection: {e}")
            return False
            
    def intelligent_attack(self):
        """Ataque inteligente con SPACE para next target y CTRL+SPACE para atacar"""
        try:
            enemy_pos = self.find_closest_enemy_visual()
            
            if enemy_pos:
                x, y = enemy_pos
                
                # Hacer clic en el enemigo
                pyautogui.click(x, y)
                self.log_to_gui(f"🎯 Clicked within Tibia at ({x}, {y})")
                time.sleep(0.2)
                
                # Presionar SPACE para seleccionar objetivo
                keyboard.press_and_release(self.hotkeys['next_target'])
                self.log_to_gui(f"🎯 Next target selected with {self.hotkeys['next_target']}")
                time.sleep(0.2)
                
                # Presionar CTRL+SPACE para atacar múltiples veces
                for i in range(8):  # Más ataques
                    if not self.running or self.paused:
                        break
                    # Presionar CTRL + SPACE
                    keyboard.press('CTRL')
                    keyboard.press_and_release('SPACE')
                    keyboard.release('CTRL')
                    self.log_to_gui(f"⚔️ ATTACKING with CTRL+SPACE - Hit {i+1}")
                    time.sleep(0.1)
                    
                self.log_to_gui("⚔️ ATTACK SEQUENCE COMPLETED!")
                return True
            else:
                # Si no encuentra enemigo visual, intentar con SPACE para buscar
                self.log_to_gui("🔍 No enemies found visually, trying SPACE to find target...")
                keyboard.press_and_release(self.hotkeys['next_target'])
                time.sleep(0.2)
                
                # Intentar atacar de todas formas con CTRL+SPACE
                for i in range(3):
                    if not self.running or self.paused:
                        break
                    keyboard.press('CTRL')
                    keyboard.press_and_release('SPACE')
                    keyboard.release('CTRL')
                    self.log_to_gui(f"⚔️ BLIND ATTACK with CTRL+SPACE - Hit {i+1}")
                    time.sleep(0.1)
                    
                return True
                
        except Exception as e:
            self.log_to_gui(f"❌ Error in attack: {e}")
            return False
            
    def intelligent_healing(self):
        """Curación inteligente con detección de potiones"""
        try:
            # Verificar potiones disponibles
            self.check_potions_available()
            
            # Detectar vida real
            self.detect_health_mana_from_screen()
            
            # Curar solo si la vida está realmente baja Y hay potiones
            if self.health < self.heal_threshold and self.health_potions > 0:
                # Verificar que realmente necesita curación (no confundir con vida del enemigo)
                if self.health < 50:  # Solo curar si vida < 50%
                    keyboard.press_and_release(self.hotkeys['heal'])
                    self.health_potions -= 1
                    self.health = min(100, self.health + 30)
                    self.log_to_gui(f"❤️ Health potion used! Health: {self.health}% (Potions left: {self.health_potions})")
                    return True
                else:
                    self.log_to_gui(f"⚠️ Health is {self.health}% - not low enough to waste potion")
                    return False
            elif self.health < self.heal_threshold and self.health_potions <= 0:
                self.log_to_gui(f"⚠️ Low health ({self.health}%) but no potions available!")
                return False
            elif self.health >= self.heal_threshold:
                self.log_to_gui(f"✅ Health is good: {self.health}% - no need for potion")
                return False
                
            return False
            
        except Exception as e:
            self.log_to_gui(f"❌ Error in healing: {e}")
            return False
            
    def intelligent_mana(self):
        """Mana inteligente con detección de potiones"""
        try:
            # Verificar potiones disponibles
            self.check_potions_available()
            
            # Detectar mana real
            self.detect_health_mana_from_screen()
            
            # Usar mana potion solo si está realmente baja Y hay potiones
            if self.mana < self.mana_threshold and self.mana_potions > 0:
                # Verificar que realmente necesita mana (no confundir con mana del enemigo)
                if self.mana < 40:  # Solo usar si mana < 40%
                    keyboard.press_and_release(self.hotkeys['mana'])
                    self.mana_potions -= 1
                    self.mana = min(100, self.mana + 25)
                    self.log_to_gui(f"🔮 Mana potion used! Mana: {self.mana}% (Potions left: {self.mana_potions})")
                    return True
                else:
                    self.log_to_gui(f"⚠️ Mana is {self.mana}% - not low enough to waste potion")
                    return False
            elif self.mana < self.mana_threshold and self.mana_potions <= 0:
                self.log_to_gui(f"⚠️ Low mana ({self.mana}%) but no potions available!")
                return False
            elif self.mana >= self.mana_threshold:
                self.log_to_gui(f"✅ Mana is good: {self.mana}% - no need for potion")
                return False
                
            return False
            
        except Exception as e:
            self.log_to_gui(f"❌ Error in mana: {e}")
            return False
            
    def intelligent_spells(self):
        """Hechizos inteligentes solo si hay suficiente mana"""
        try:
            # Detectar mana real
            self.detect_health_mana_from_screen()
            
            if self.mana > self.spell_mana_threshold:
                # Usar hechizo de ataque
                keyboard.press_and_release(self.hotkeys['spell1'])
                self.mana -= 20
                self.log_to_gui(f"🔮 Attack spell cast! Mana: {self.mana}%")
                time.sleep(0.5)
                
                # Usar hechizo de curación si es necesario
                if self.health < 70:
                    keyboard.press_and_release(self.hotkeys['spell2'])
                    self.mana -= 15
                    self.health = min(100, self.health + 20)
                    self.log_to_gui(f"🔮 Healing spell cast! Health: {self.health}%")
                    
                return True
            else:
                self.log_to_gui(f"🔮 Not enough mana for spells ({self.mana}% < {self.spell_mana_threshold}%)")
                return False
                
        except Exception as e:
            self.log_to_gui(f"❌ Error in spells: {e}")
            return False
            
    def automatic_quick_loot(self):
        """Loot automático después de matar enemigo"""
        try:
            current_time = time.time()
            if current_time - self.last_enemy_death > 1.0:  # 1 segundo después
                keyboard.press_and_release(self.hotkeys['quick_loot'])
                self.log_to_gui(f"💰 Quick loot triggered with key {self.hotkeys['quick_loot']}")
                self.last_enemy_death = current_time
                return True
            return False
            
        except Exception as e:
            self.log_to_gui(f"❌ Error in quick loot: {e}")
            return False
            
    def smart_movement(self):
        """Movimiento inteligente WASD con detección de obstáculos"""
        try:
            current_time = time.time()
            if current_time - self.last_movement > 1.0:  # Mover cada 1 segundo
                
                # Detectar si está atascado
                current_pos = pyautogui.position()
                if self.last_position and current_pos == self.last_position:
                    self.stuck_counter += 1
                    if self.stuck_counter > 3:
                        self.movement_state = "stuck"
                        self.log_to_gui("🚧 Detected stuck! Changing movement pattern...")
                else:
                    self.stuck_counter = 0
                    if self.movement_state == "stuck":
                        self.movement_state = "forward"
                        
                self.last_position = current_pos
                
                # Lógica de movimiento según el estado
                if self.movement_state == "forward":
                    # Movimiento hacia adelante (S)
                    movement = 'S'
                    self.log_to_gui(f"🚶 Moving forward: {movement}")
                    
                elif self.movement_state == "stuck":
                    # Patrón de evasión cuando está atascado
                    movements = ['W', 'A', 'D']  # Evitar S (atrás)
                    movement = random.choice(movements)
                    self.log_to_gui(f"🔄 Avoiding obstacle: {movement}")
                    
                    # Cambiar a estado de evasión
                    self.movement_state = "avoiding"
                    
                elif self.movement_state == "avoiding":
                    # Movimiento en círculos para evitar obstáculos
                    movements = ['W', 'A', 'D']
                    movement = random.choice(movements)
                    self.log_to_gui(f"🔄 Avoiding pattern: {movement}")
                    
                    # Volver a forward después de un tiempo
                    if random.random() < 0.3:
                        self.movement_state = "forward"
                        self.log_to_gui("✅ Back to forward movement")
                
                # Ejecutar movimiento
                keyboard.press_and_release(movement)
                self.last_movement = current_time
                return True
                
            return False
            
        except Exception as e:
            self.log_to_gui(f"❌ Error in movement: {e}")
            return False
            
    def face_enemy(self):
        """Mirar hacia el enemigo"""
        try:
            keyboard.press_and_release(self.hotkeys['face_enemy'])
            self.log_to_gui("👁️ Facing enemy with CTRL")
            return True
        except Exception as e:
            self.log_to_gui(f"❌ Error facing enemy: {e}")
            return False
            
    def combat_action(self):
        """Acción principal de combate"""
        try:
            # Prioridad: Quick loot > Healing > Mana > Attack > Spells > Movement
            
            # 1. Quick loot
            if self.automatic_quick_loot():
                return
                
            # 2. Healing
            if self.intelligent_healing():
                return
                
            # 3. Mana
            if self.intelligent_mana():
                return
                
            # 4. Attack
            if self.intelligent_attack():
                # 5. Spells después de atacar
                self.intelligent_spells()
                return
                
            # 6. Movement si no hay enemigos
            if not self.enemy_detected:
                self.smart_movement()
                
        except Exception as e:
            self.log_to_gui(f"❌ Error in combat action: {e}")
            
    def toggle_pause(self):
        """Pausar/reanudar el bot"""
        self.paused = not self.paused
        status = "PAUSED" if self.paused else "RESUMED"
        self.log_to_gui(f"⏸️ Bot {status}")
        
    def stop_bot(self):
        """Detener el bot completamente"""
        self.running = False
        self.log_to_gui("🛑 Bot stopped by F12")
        
    def run_bot(self):
        """Ejecutar el bot principal"""
        try:
            self.log_to_gui("🚀 Starting NopalBot Intelligent...")
            self.log_to_gui(f"👤 Character: {self.character_name}")
            self.log_to_gui(f"🎭 Vocation: {self.character_vocation}")
            self.log_to_gui(f"❤️ Heal threshold: {self.heal_threshold}%")
            self.log_to_gui(f"🔮 Mana threshold: {self.mana_threshold}%")
            self.log_to_gui("🎮 Press F11 to pause/resume, F12 to stop")
            
            if not self.find_tibia_window():
                self.log_to_gui("❌ Cannot find Tibia window!")
                return
                
            self.running = True
            self.paused = False
            
            while self.running:
                if not self.paused:
                    self.combat_action()
                    
                time.sleep(0.5)  # Pausa entre acciones
                
        except Exception as e:
            self.log_to_gui(f"❌ Error in main loop: {e}")
        finally:
            self.running = False
            self.log_to_gui("🏁 Bot finished")

class NopalBotGUI:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("🤖 NopalBot Intelligent - Complete Edition")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        
        # Variables
        self.bot = None
        self.bot_thread = None
        self.overlay = None
        
        # Crear overlay
        self.overlay = TransparentOverlay(self.root)
        
        self.setup_gui()
        
    def setup_gui(self):
        # Frame principal
        main_frame = ctk.CTkFrame(self.root)
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Título
        title_label = ctk.CTkLabel(main_frame, text="🤖 NOPALBOT INTELLIGENT", 
                                  font=ctk.CTkFont(size=24, weight="bold"))
        title_label.pack(pady=10)
        
        # Frame de información del personaje
        char_frame = ctk.CTkFrame(main_frame)
        char_frame.pack(fill='x', padx=10, pady=5)
        
        char_title = ctk.CTkLabel(char_frame, text="👤 CHARACTER INFO", 
                                 font=ctk.CTkFont(size=16, weight="bold"))
        char_title.pack(pady=5)
        
        # Información del personaje
        self.char_name_label = ctk.CTkLabel(char_frame, text="Name: Unknown")
        self.char_name_label.pack()
        
        self.char_vocation_label = ctk.CTkLabel(char_frame, text="Vocation: Druid")
        self.char_vocation_label.pack()
        
        self.char_level_label = ctk.CTkLabel(char_frame, text="Level: 1")
        self.char_level_label.pack()
        
        # Frame de configuración
        config_frame = ctk.CTkFrame(main_frame)
        config_frame.pack(fill='x', padx=10, pady=5)
        
        config_title = ctk.CTkLabel(config_frame, text="⚙️ CONFIGURATION", 
                                   font=ctk.CTkFont(size=16, weight="bold"))
        config_title.pack(pady=5)
        
        # Sliders para umbrales
        self.heal_slider = ctk.CTkSlider(config_frame, from_=10, to=50, 
                                        number_of_steps=40, command=self.update_heal_threshold)
        self.heal_slider.set(30)
        heal_label = ctk.CTkLabel(config_frame, text="Heal Threshold: 30%")
        heal_label.pack()
        self.heal_slider.pack(pady=5)
        
        self.mana_slider = ctk.CTkSlider(config_frame, from_=10, to=50, 
                                        number_of_steps=40, command=self.update_mana_threshold)
        self.mana_slider.set(30)
        mana_label = ctk.CTkLabel(config_frame, text="Mana Threshold: 30%")
        mana_label.pack()
        self.mana_slider.pack(pady=5)
        
        # Frame de controles
        control_frame = ctk.CTkFrame(main_frame)
        control_frame.pack(fill='x', padx=10, pady=5)
        
        control_title = ctk.CTkLabel(control_frame, text="🎮 CONTROLS", 
                                    font=ctk.CTkFont(size=16, weight="bold"))
        control_title.pack(pady=5)
        
        # Botones
        button_frame = ctk.CTkFrame(control_frame)
        button_frame.pack(pady=10)
        
        self.start_button = ctk.CTkButton(button_frame, text="🚀 START BOT", 
                                         command=self.start_bot, 
                                         fg_color="green", hover_color="darkgreen")
        self.start_button.pack(side='left', padx=5)
        
        self.stop_button = ctk.CTkButton(button_frame, text="🛑 STOP BOT", 
                                        command=self.stop_bot, 
                                        fg_color="red", hover_color="darkred")
        self.stop_button.pack(side='left', padx=5)
        
        self.overlay_button = ctk.CTkButton(button_frame, text="📊 TOGGLE OVERLAY", 
                                           command=self.toggle_overlay)
        self.overlay_button.pack(side='left', padx=5)
        
        # Frame de hotkeys
        hotkey_frame = ctk.CTkFrame(main_frame)
        hotkey_frame.pack(fill='x', padx=10, pady=5)
        
        hotkey_title = ctk.CTkLabel(hotkey_frame, text="⌨️ HOTKEYS", 
                                   font=ctk.CTkFont(size=16, weight="bold"))
        hotkey_title.pack(pady=5)
        
        # Lista de hotkeys
        hotkeys_text = """
        🎯 Attack: CTRL+SPACE
        🎯 Next Target: SPACE
        ❤️ Heal: F1
        🔮 Mana: F2
        ⚡ Spell 1: F3 (Exori vis)
        🛡️ Spell 2: F4 (Exura)
        💰 Loot: F5
        🎁 Quick Loot: 0
        🚶 Movement: WASD
        👁️ Face Enemy: CTRL
        ⏸️ Pause/Resume: F11
        🛑 Stop Bot: F12
        """
        
        hotkey_label = ctk.CTkLabel(hotkey_frame, text=hotkeys_text, 
                                   font=ctk.CTkFont(size=12))
        hotkey_label.pack(pady=5)
        
        # Frame de estado
        status_frame = ctk.CTkFrame(main_frame)
        status_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        status_title = ctk.CTkLabel(status_frame, text="📊 STATUS", 
                                   font=ctk.CTkFont(size=16, weight="bold"))
        status_title.pack(pady=5)
        
        # Log del bot
        self.log_text = ctk.CTkTextbox(status_frame, height=150)
        self.log_text.pack(fill='both', expand=True, padx=5, pady=5)
        
    def update_heal_threshold(self, value):
        if self.bot:
            self.bot.heal_threshold = int(value)
        self.log_to_gui(f"❤️ Heal threshold updated: {int(value)}%")
        
    def update_mana_threshold(self, value):
        if self.bot:
            self.bot.mana_threshold = int(value)
        self.log_to_gui(f"🔮 Mana threshold updated: {int(value)}%")
        
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
            messagebox.showwarning("Warning", "Bot is already running!")
            return
            
        try:
            # Crear nuevo bot
            self.bot = NopalBotIntelligent(self.log_to_gui)
            
            # Actualizar umbrales
            self.bot.heal_threshold = int(self.heal_slider.get())
            self.bot.mana_threshold = int(self.mana_slider.get())
            
            # Iniciar bot en thread separado
            self.bot_thread = threading.Thread(target=self.bot.run_bot, daemon=True)
            self.bot_thread.start()
            
            self.start_button.configure(state="disabled")
            self.stop_button.configure(state="normal")
            
            self.log_to_gui("🚀 Bot started successfully!")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to start bot: {e}")
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
    app = NopalBotGUI()
    app.run()

if __name__ == "__main__":
    main() 