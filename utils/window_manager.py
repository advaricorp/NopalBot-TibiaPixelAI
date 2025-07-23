"""
Window Management Module
Handles Tibia window detection, maximization, and focus management
"""

import time
import win32gui
import win32con
import win32api
import logging
from typing import List, Tuple, Optional

class WindowManager:
    """Manages Tibia window operations"""
    
    def __init__(self, log_file: str = "logs/window_manager.log"):
        self.logger = self._setup_logger(log_file)
        self.tibia_hwnd = None
        self.window_name = None
    
    def _setup_logger(self, log_file: str) -> logging.Logger:
        """Setup logging for window operations"""
        logger = logging.getLogger('WindowManager')
        logger.setLevel(logging.INFO)
        
        # File handler
        fh = logging.FileHandler(log_file)
        fh.setLevel(logging.INFO)
        
        # Console handler
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        
        # Formatter
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)
        
        logger.addHandler(fh)
        logger.addHandler(ch)
        
        return logger
    
    def find_tibia_windows(self) -> List[Tuple[int, str]]:
        """Find all Tibia windows"""
        def enum_windows_callback(hwnd, windows):
            if win32gui.IsWindowVisible(hwnd):
                window_text = win32gui.GetWindowText(hwnd)
                if "tibia" in window_text.lower():
                    windows.append((hwnd, window_text))
            return True
        
        windows = []
        win32gui.EnumWindows(enum_windows_callback, windows)
        return windows
    
    def find_tibia_window(self) -> Optional[Tuple[int, str]]:
        """Find the first Tibia window"""
        windows = self.find_tibia_windows()
        return windows[0] if windows else None
    
    def get_window_state(self, hwnd: int) -> int:
        """Get current window state"""
        placement = win32gui.GetWindowPlacement(hwnd)
        return placement[1]
    
    def is_window_maximized(self, hwnd: int) -> bool:
        """Check if window is maximized"""
        return self.get_window_state(hwnd) == win32con.SW_SHOWMAXIMIZED
    
    def is_window_minimized(self, hwnd: int) -> bool:
        """Check if window is minimized"""
        return self.get_window_state(hwnd) == win32con.SW_SHOWMINIMIZED
    
    def is_window_focused(self, hwnd: int) -> bool:
        """Check if window is in foreground"""
        return win32gui.GetForegroundWindow() == hwnd
    
    def restore_window(self, hwnd: int) -> bool:
        """Restore minimized window"""
        try:
            self.logger.info("Restaurando ventana minimizada...")
            win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
            time.sleep(0.5)
            return True
        except Exception as e:
            self.logger.error(f"Error restaurando ventana: {e}")
            return False
    
    def maximize_window(self, hwnd: int) -> bool:
        """Maximize window"""
        try:
            self.logger.info("Maximizando ventana...")
            win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)
            time.sleep(0.5)
            return True
        except Exception as e:
            self.logger.error(f"Error maximizando ventana: {e}")
            return False
    
    def focus_window(self, hwnd: int) -> bool:
        """Bring window to foreground"""
        try:
            self.logger.info("Traiendo ventana al primer plano...")
            win32gui.SetForegroundWindow(hwnd)
            time.sleep(0.5)
            return True
        except Exception as e:
            self.logger.error(f"Error forzando ventana: {e}")
            return False
    
    def get_window_rect(self, hwnd: int) -> Tuple[int, int, int, int]:
        """Get window position and size"""
        return win32gui.GetWindowRect(hwnd)
    
    def setup_tibia_window(self) -> bool:
        """Setup and focus Tibia window"""
        # Find Tibia window
        result = self.find_tibia_window()
        if not result:
            self.logger.error("No se encontro ninguna ventana de Tibia")
            return False
        
        self.tibia_hwnd, self.window_name = result
        self.logger.info(f"Encontrada ventana: {self.window_name} (HWND: {self.tibia_hwnd})")
        
        # Get current state
        current_state = self.get_window_state(self.tibia_hwnd)
        self.logger.info(f"Estado actual: {current_state}")
        
        # Restore if minimized
        if self.is_window_minimized(self.tibia_hwnd):
            if not self.restore_window(self.tibia_hwnd):
                return False
        
        # Focus window
        if not self.focus_window(self.tibia_hwnd):
            return False
        
        # Maximize if not already maximized
        if not self.is_window_maximized(self.tibia_hwnd):
            if not self.maximize_window(self.tibia_hwnd):
                return False
        
        # Verify final state
        final_state = self.get_window_state(self.tibia_hwnd)
        rect = self.get_window_rect(self.tibia_hwnd)
        
        self.logger.info(f"Estado final: {final_state}")
        self.logger.info(f"Posicion: {rect}")
        
        if self.is_window_focused(self.tibia_hwnd):
            self.logger.info("VENTANA EN PRIMER PLANO - EXITOSO")
            return True
        else:
            self.logger.warning("VENTANA NO esta en primer plano")
            return False
    
    def ensure_focus(self) -> bool:
        """Ensure Tibia window is focused"""
        if not self.tibia_hwnd:
            return self.setup_tibia_window()
        
        if not self.is_window_focused(self.tibia_hwnd):
            self.logger.warning("Input perdido - Forzando ventana...")
            return self.focus_window(self.tibia_hwnd)
        
        return True
    
    def monitor_focus(self, duration: int = 10) -> None:
        """Monitor window focus for specified duration"""
        if not self.tibia_hwnd:
            self.logger.error("No hay ventana de Tibia configurada")
            return
        
        self.logger.info(f"Monitoreando foco por {duration} segundos...")
        for i in range(duration):
            time.sleep(1)
            if self.is_window_focused(self.tibia_hwnd):
                self.logger.info(f"Tibia sigue en primer plano ({duration-i}s restantes)")
            else:
                self.logger.warning(f"Tibia perdio el foco ({duration-i}s restantes)")

# Convenience function for backward compatibility
def maximize_tibia_window():
    """Legacy function to maximize Tibia window"""
    manager = WindowManager()
    return manager.setup_tibia_window()

if __name__ == "__main__":
    # Test the window manager
    manager = WindowManager()
    if manager.setup_tibia_window():
        print("Maximizacion exitosa!")
        manager.monitor_focus(5)
    else:
        print("Fallo en la maximizacion") 