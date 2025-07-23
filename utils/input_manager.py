"""
Input Management Module
Handles keyboard and mouse input to Tibia
"""

import time
import keyboard
import mouse
import logging
import random
from typing import Optional, Tuple
from .window_manager import WindowManager

class InputManager:
    """Manages input operations to Tibia"""
    
    def __init__(self, window_manager: WindowManager, log_file: str = "logs/input_manager.log"):
        self.window_manager = window_manager
        self.logger = self._setup_logger(log_file)
        self.last_input_time = 0
        self.input_delay = 0.1  # Minimum delay between inputs
        
        # Humanization settings for more realistic behavior
        self.humanization_enabled = True
        self.mouse_move_delay_min = 0.5  # Minimum time to move mouse
        self.mouse_move_delay_max = 1.5  # Maximum time to move mouse
        self.click_delay_min = 0.2       # Minimum delay before click
        self.click_delay_max = 0.8       # Maximum delay before click
        self.post_click_delay_min = 0.3  # Minimum delay after click
        self.post_click_delay_max = 1.0  # Maximum delay after click
        self.mouse_accuracy = 0.90       # Mouse accuracy (90% = more randomness)
        self.key_delay_min = 0.3         # Minimum delay before key press
        self.key_delay_max = 1.2         # Maximum delay before key press
        self.post_key_delay_min = 0.4    # Minimum delay after key press
        self.post_key_delay_max = 1.5    # Maximum delay after key press
    
    def _setup_logger(self, log_file: str) -> logging.Logger:
        """Setup logging for input operations"""
        logger = logging.getLogger('InputManager')
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
    
    def _ensure_focus(self) -> bool:
        """Ensure Tibia window is focused before input"""
        return self.window_manager.ensure_focus()
    
    def _rate_limit(self) -> None:
        """Rate limit inputs to prevent spam"""
        current_time = time.time()
        time_since_last = current_time - self.last_input_time
        if time_since_last < self.input_delay:
            time.sleep(self.input_delay - time_since_last)
        self.last_input_time = time.time()
    
    def _humanize_delay(self, min_delay: float, max_delay: float) -> float:
        """Generate a random delay within the specified range"""
        if not self.humanization_enabled:
            return min_delay
        return random.uniform(min_delay, max_delay)
    
    def _humanize_coordinates(self, x: int, y: int) -> Tuple[int, int]:
        """Add slight randomness to mouse coordinates for more human-like movement"""
        if not self.humanization_enabled:
            return x, y
        
        # Add random offset (±3 pixels) for more natural movement
        offset_range = 3
        x_offset = random.randint(-offset_range, offset_range)
        y_offset = random.randint(-offset_range, offset_range)
        
        return x + x_offset, y + y_offset
    
    def _humanize_mouse_move(self, x: int, y: int) -> bool:
        """Move mouse to position with human-like delays"""
        try:
            # Humanize coordinates
            human_x, human_y = self._humanize_coordinates(x, y)
            
            # Move mouse with human-like delay
            move_delay = self._humanize_delay(self.mouse_move_delay_min, self.mouse_move_delay_max)
            mouse.move(human_x, human_y, duration=int(move_delay * 1000))  # Convert to milliseconds
            
            return True
        except Exception as e:
            self.logger.error(f"Error en movimiento humanizado: {e}")
            return False
    
    def send_key(self, key: str, delay: float = 0.1) -> bool:
        """Send a key press to Tibia with humanization"""
        try:
            if not self._ensure_focus():
                return False
            
            self._rate_limit()
            
            # Humanized key press
            if self.humanization_enabled:
                # Random delay before pressing key (like human reaction time)
                pre_key_delay = self._humanize_delay(self.key_delay_min, self.key_delay_max)
                time.sleep(pre_key_delay)
                
                # Press and release with slight delay (like human finger movement)
                keyboard.press(key)
                time.sleep(self._humanize_delay(0.05, 0.15))
                keyboard.release(key)
                
                # Random delay after key press
                post_key_delay = self._humanize_delay(self.post_key_delay_min, self.post_key_delay_max)
                time.sleep(post_key_delay)
            else:
                # Fast key press for non-humanized mode
                keyboard.press_and_release(key)
                time.sleep(delay)
            
            self.logger.info(f"Tecla humanizada enviada: {key}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error enviando tecla {key}: {e}")
            return False
    
    def send_attack(self) -> bool:
        """Send attack command (space key)"""
        return self.send_key('space', 0.05)
    
    def send_spell(self, spell_key: str) -> bool:
        """Send spell command"""
        return self.send_key(spell_key, 0.1)
    
    def send_movement(self, direction: str) -> bool:
        """Send movement command (arrow keys or WASD)"""
        return self.send_key(direction, 0.05)
    
    def click_position(self, x: int, y: int, button: str = 'left') -> bool:
        """Click at specific position relative to Tibia window with humanization"""
        try:
            if not self._ensure_focus():
                return False
            
            # Get Tibia window position and size
            if not self.window_manager.tibia_hwnd:
                self.logger.error("No hay ventana de Tibia configurada")
                return False
            
            window_rect = self.window_manager.get_window_rect(self.window_manager.tibia_hwnd)
            window_x, window_y, window_right, window_bottom = window_rect
            window_width = window_right - window_x
            window_height = window_bottom - window_y
            
            # Calculate absolute screen coordinates
            # Tibia client area is typically offset by title bar and borders
            # For a maximized window, we need to account for the title bar (~30px) and borders
            title_bar_height = 30
            border_width = 8
            
            # Calculate position within the client area
            client_x = window_x + border_width + x
            client_y = window_y + title_bar_height + y
            
            # Ensure coordinates are within window bounds
            if client_x < window_x or client_x > window_right or client_y < window_y or client_y > window_bottom:
                self.logger.warning(f"Coordenadas fuera de la ventana: ({client_x}, {client_y}) vs ventana: {window_rect}")
                return False
            
            self._rate_limit()
            
            # Humanized mouse movement and click
            if self.humanization_enabled:
                # Move mouse with human-like delay
                if not self._humanize_mouse_move(client_x, client_y):
                    return False
                
                # Random delay before clicking (like a human thinking)
                pre_click_delay = self._humanize_delay(self.click_delay_min, self.click_delay_max)
                time.sleep(pre_click_delay)
                
                # Perform the click
                mouse.click(button=button)
                
                # Random delay after clicking (like a human reaction)
                post_click_delay = self._humanize_delay(self.post_click_delay_min, self.post_click_delay_max)
                time.sleep(post_click_delay)
            else:
                # Fast movement for non-humanized mode
                mouse.move(client_x, client_y)
                time.sleep(0.1)
                mouse.click(button=button)
                time.sleep(0.1)
            
            self.logger.info(f"Click humanizado en posicion relativa: ({x}, {y}) -> absoluta: ({client_x}, {client_y})")
            return True
            
        except Exception as e:
            self.logger.error(f"Error haciendo click en ({x}, {y}): {e}")
            return False
    
    def right_click_position(self, x: int, y: int) -> bool:
        """Right click at specific position"""
        return self.click_position(x, y, 'right')
    
    def drag_mouse(self, start_x: int, start_y: int, end_x: int, end_y: int) -> bool:
        """Drag mouse from start to end position"""
        try:
            if not self._ensure_focus():
                return False
            
            self._rate_limit()
            mouse.move(start_x, start_y)
            time.sleep(0.1)
            mouse.drag(start_x, start_y, end_x, end_y)
            time.sleep(0.1)
            
            self.logger.info(f"Drag de ({start_x}, {start_y}) a ({end_x}, {end_y})")
            return True
            
        except Exception as e:
            self.logger.error(f"Error en drag: {e}")
            return False
    
    def test_input(self, test_key: str = 'space') -> bool:
        """Test if input is working"""
        try:
            if not self._ensure_focus():
                return False
            
            # Send test key
            keyboard.press_and_release(test_key)
            time.sleep(0.1)
            
            self.logger.info(f"Test de input exitoso con tecla: {test_key}")
            return True
            
        except Exception as e:
            self.logger.error(f"Test de input fallo: {e}")
            return False
    
    def continuous_attack(self, interval: float = 2.0, duration: Optional[float] = None) -> None:
        """Send continuous attacks at specified interval"""
        self.logger.info(f"Iniciando ataque continuo cada {interval}s")
        
        start_time = time.time()
        while True:
            if duration and (time.time() - start_time) > duration:
                break
            
            if not self.send_attack():
                self.logger.warning("Fallo en ataque continuo")
            
            time.sleep(interval)
    
    def auto_walk(self, directions: list, interval: float = 1.0) -> None:
        """Automatically walk in sequence of directions"""
        self.logger.info(f"Iniciando auto-walk con {len(directions)} direcciones")
        
        for direction in directions:
            if not self.send_movement(direction):
                self.logger.warning(f"Fallo en movimiento: {direction}")
            time.sleep(interval)

# Convenience functions for backward compatibility
def send_attack_to_tibia():
    """Legacy function to send attack"""
    window_manager = WindowManager()
    input_manager = InputManager(window_manager)
    return input_manager.send_attack()

def test_input_to_tibia():
    """Legacy function to test input"""
    window_manager = WindowManager()
    input_manager = InputManager(window_manager)
    return input_manager.test_input()

if __name__ == "__main__":
    # Test the input manager
    window_manager = WindowManager()
    input_manager = InputManager(window_manager)
    
    if input_manager.test_input():
        print("Test de input exitoso!")
        input_manager.send_attack()
    else:
        print("Test de input fallo") 