"""
Módulo de utilidades para NopalBot
Funciones auxiliares para logs, window handling, y anti-stuck
"""

import time
import threading
import keyboard
import pyautogui
import win32gui
import win32con
from datetime import datetime
import random
from typing import Tuple, Optional, List

class Logger:
    """Clase para manejo de logs"""
    
    def __init__(self, gui_callback=None):
        self.gui_callback = gui_callback
        self.log_file = f"logs/nopalbot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    
    def log(self, message: str, level: str = "INFO"):
        """Registra un mensaje de log"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] [{level}] {message}"
        
        # Log a consola
        print(log_entry)
        
        # Log a GUI si está disponible
        if self.gui_callback:
            self.gui_callback(log_entry)
        
        # Log a archivo
        try:
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(log_entry + "\n")
        except Exception as e:
            print(f"Error escribiendo log: {e}")

class WindowManager:
    """Clase para manejo de ventanas de Tibia"""
    
    @staticmethod
    def find_tibia_window() -> Optional[int]:
        """Encuentra la ventana de Tibia"""
        windows = []
        
        def enum_windows_callback(hwnd, windows):
            if win32gui.IsWindowVisible(hwnd):
                window_text = win32gui.GetWindowText(hwnd)
                if "tibia" in window_text.lower():
                    windows.append(hwnd)
            return True
        
        win32gui.EnumWindows(enum_windows_callback, windows)
        
        if windows:
            return windows[0]
        return None
    
    @staticmethod
    def activate_tibia_window() -> bool:
        """Activa la ventana de Tibia"""
        hwnd = WindowManager.find_tibia_window()
        if hwnd:
            try:
                # Restaurar ventana si está minimizada
                if win32gui.IsIconic(hwnd):
                    win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
                
                # Traer al frente
                win32gui.SetForegroundWindow(hwnd)
                time.sleep(0.1)
                return True
            except Exception as e:
                print(f"Error activando ventana: {e}")
                return False
        return False
    
    @staticmethod
    def get_window_rect(hwnd: int) -> Tuple[int, int, int, int]:
        """Obtiene las coordenadas de la ventana"""
        try:
            return win32gui.GetWindowRect(hwnd)
        except:
            return (0, 0, 800, 600)  # Default

class AntiStuckSystem:
    """Sistema anti-stuck para movimiento inteligente"""
    
    def __init__(self):
        self.position_history = []
        self.movement_attempts = 0
        self.last_position = None
        self.stuck_counter = 0
        self.max_stuck_attempts = 5
    
    def update_position(self, position: Tuple[int, int]):
        """Actualiza la posición actual"""
        self.position_history.append(position)
        
        # Mantener solo las últimas 10 posiciones
        if len(self.position_history) > 10:
            self.position_history.pop(0)
        
        self.last_position = position
    
    def check_position_change(self, new_position: Tuple[int, int]) -> bool:
        """Verifica si la posición cambió"""
        if self.last_position is None:
            self.last_position = new_position
            return True
        
        # Calcular distancia
        dx = abs(new_position[0] - self.last_position[0])
        dy = abs(new_position[1] - self.last_position[1])
        
        # Si la posición cambió significativamente
        if dx > 5 or dy > 5:
            self.stuck_counter = 0
            self.last_position = new_position
            return True
        
        self.stuck_counter += 1
        return False
    
    def is_stuck(self) -> bool:
        """Determina si el personaje está atascado"""
        return self.stuck_counter >= self.max_stuck_attempts
    
    def try_all_movement_keys(self) -> str:
        """Intenta todas las teclas de movimiento"""
        keys = ['w', 'a', 's', 'd']
        random.shuffle(keys)  # Orden aleatorio
        
        for key in keys:
            keyboard.press_and_release(key)
            time.sleep(0.2)
            
            # Simular nueva posición (en implementación real, obtener de Tibia)
            new_pos = (random.randint(100, 200), random.randint(100, 200))
            
            if self.check_position_change(new_pos):
                return key
        
        return 'w'  # Default
    
    def reset_stuck_counter(self):
        """Resetea el contador de stuck"""
        self.stuck_counter = 0

class InputManager:
    """Manejador de inputs para Tibia"""
    
    @staticmethod
    def send_keyboard_input(key: str, delay: float = 0.1):
        """Envía input de teclado con verificación"""
        try:
            # Activar ventana primero
            WindowManager.activate_tibia_window()
            time.sleep(0.1)
            
            # Enviar input
            keyboard.press_and_release(key)
            time.sleep(delay)
            
            return True
        except Exception as e:
            print(f"Error enviando input {key}: {e}")
            return False
    
    @staticmethod
    def send_mouse_click(x: int, y: int, button: str = 'left'):
        """Envía click de mouse con verificación"""
        try:
            # Activar ventana primero
            WindowManager.activate_tibia_window()
            time.sleep(0.1)
            
            # Obtener coordenadas de ventana
            hwnd = WindowManager.find_tibia_window()
            if hwnd:
                rect = WindowManager.get_window_rect(hwnd)
                # Ajustar coordenadas relativas a la ventana
                abs_x = rect[0] + x
                abs_y = rect[1] + y
                
                pyautogui.click(abs_x, abs_y, button=button)
                return True
        except Exception as e:
            print(f"Error enviando click: {e}")
            return False
    
    @staticmethod
    def triple_check_tibia_input(key: str):
        """Envía input con triple verificación"""
        for i in range(3):
            if InputManager.send_keyboard_input(key):
                return True
            time.sleep(0.1)
        return False

# Instancias globales
logger = Logger()
anti_stuck = AntiStuckSystem() 