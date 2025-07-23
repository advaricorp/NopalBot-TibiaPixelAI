"""
Bot Features Module
Core bot functionality including auto-attack, auto-loot, auto-walk, etc.
"""

import time
import threading
import logging
from typing import Optional, List, Dict, Any
from utils.window_manager import WindowManager
from utils.input_manager import InputManager

class BotFeatures:
    """Core bot features and functionality"""
    
    def __init__(self, window_manager: WindowManager, input_manager: InputManager, log_file: str = "logs/bot_features.log"):
        self.window_manager = window_manager
        self.input_manager = input_manager
        self.logger = self._setup_logger(log_file)
        
        # Feature states
        self.auto_attack_enabled = False
        self.auto_loot_enabled = False
        self.auto_walk_enabled = False
        self.auto_spell_enabled = False
        
        # Threading
        self.attack_thread = None
        self.loot_thread = None
        self.walk_thread = None
        self.spell_thread = None
        self.monitor_thread = None
        
        # Configuration
        self.attack_interval = 2.0
        self.loot_interval = 1.0
        self.walk_interval = 3.0
        self.spell_interval = 5.0
        self.monitor_interval = 5.0
        
        # Running state
        self.running = False
    
    def _setup_logger(self, log_file: str) -> logging.Logger:
        """Setup logging for bot features"""
        logger = logging.getLogger('BotFeatures')
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
    
    def _attack_loop(self) -> None:
        """Auto-attack loop"""
        self.logger.info("Iniciando auto-attack...")
        while self.auto_attack_enabled and self.running:
            try:
                if self.input_manager.send_attack():
                    self.logger.debug("Ataque enviado")
                else:
                    self.logger.warning("Fallo en ataque")
                time.sleep(self.attack_interval)
            except Exception as e:
                self.logger.error(f"Error en auto-attack: {e}")
                time.sleep(1)
    
    def _loot_loop(self) -> None:
        """Auto-loot loop"""
        self.logger.info("Iniciando auto-loot...")
        while self.auto_loot_enabled and self.running:
            try:
                # Simple loot implementation - click common loot positions
                loot_positions = [
                    (400, 300),  # Center
                    (350, 250),  # Top-left
                    (450, 250),  # Top-right
                    (350, 350),  # Bottom-left
                    (450, 350),  # Bottom-right
                ]
                
                for x, y in loot_positions:
                    if not self.running:
                        break
                    self.input_manager.click_position(x, y)
                    time.sleep(0.2)
                
                time.sleep(self.loot_interval)
            except Exception as e:
                self.logger.error(f"Error en auto-loot: {e}")
                time.sleep(1)
    
    def _walk_loop(self) -> None:
        """Auto-walk loop"""
        self.logger.info("Iniciando auto-walk...")
        directions = ['up', 'right', 'down', 'left']  # Simple pattern
        direction_index = 0
        
        while self.auto_walk_enabled and self.running:
            try:
                direction = directions[direction_index]
                if self.input_manager.send_movement(direction):
                    self.logger.debug(f"Movimiento: {direction}")
                else:
                    self.logger.warning(f"Fallo en movimiento: {direction}")
                
                direction_index = (direction_index + 1) % len(directions)
                time.sleep(self.walk_interval)
            except Exception as e:
                self.logger.error(f"Error en auto-walk: {e}")
                time.sleep(1)
    
    def _spell_loop(self) -> None:
        """Auto-spell loop"""
        self.logger.info("Iniciando auto-spell...")
        spells = ['f1', 'f2', 'f3']  # Common spell keys
        
        while self.auto_spell_enabled and self.running:
            try:
                for spell in spells:
                    if not self.running:
                        break
                    if self.input_manager.send_spell(spell):
                        self.logger.debug(f"Hechizo enviado: {spell}")
                    else:
                        self.logger.warning(f"Fallo en hechizo: {spell}")
                    time.sleep(0.5)
                
                time.sleep(self.spell_interval)
            except Exception as e:
                self.logger.error(f"Error en auto-spell: {e}")
                time.sleep(1)
    
    def _monitor_loop(self) -> None:
        """Input monitoring loop"""
        self.logger.info("Iniciando monitoreo de input...")
        while self.running:
            try:
                if not self.input_manager.test_input():
                    self.logger.warning("Input perdido - Forzando ventana...")
                    self.window_manager.ensure_focus()
                time.sleep(self.monitor_interval)
            except Exception as e:
                self.logger.error(f"Error en monitoreo: {e}")
                time.sleep(1)
    
    def start_auto_attack(self, interval: float = 2.0) -> bool:
        """Start auto-attack feature"""
        if self.auto_attack_enabled:
            self.logger.warning("Auto-attack ya está activo")
            return False
        
        self.attack_interval = interval
        self.auto_attack_enabled = True
        
        if not self.attack_thread or not self.attack_thread.is_alive():
            self.attack_thread = threading.Thread(target=self._attack_loop, daemon=True)
            self.attack_thread.start()
        
        self.logger.info(f"Auto-attack iniciado cada {interval}s")
        return True
    
    def stop_auto_attack(self) -> bool:
        """Stop auto-attack feature"""
        if not self.auto_attack_enabled:
            return False
        
        self.auto_attack_enabled = False
        self.logger.info("Auto-attack detenido")
        return True
    
    def start_auto_loot(self, interval: float = 1.0) -> bool:
        """Start auto-loot feature"""
        if self.auto_loot_enabled:
            self.logger.warning("Auto-loot ya está activo")
            return False
        
        self.loot_interval = interval
        self.auto_loot_enabled = True
        
        if not self.loot_thread or not self.loot_thread.is_alive():
            self.loot_thread = threading.Thread(target=self._loot_loop, daemon=True)
            self.loot_thread.start()
        
        self.logger.info(f"Auto-loot iniciado cada {interval}s")
        return True
    
    def stop_auto_loot(self) -> bool:
        """Stop auto-loot feature"""
        if not self.auto_loot_enabled:
            return False
        
        self.auto_loot_enabled = False
        self.logger.info("Auto-loot detenido")
        return True
    
    def start_auto_walk(self, interval: float = 3.0) -> bool:
        """Start auto-walk feature"""
        if self.auto_walk_enabled:
            self.logger.warning("Auto-walk ya está activo")
            return False
        
        self.walk_interval = interval
        self.auto_walk_enabled = True
        
        if not self.walk_thread or not self.walk_thread.is_alive():
            self.walk_thread = threading.Thread(target=self._walk_loop, daemon=True)
            self.walk_thread.start()
        
        self.logger.info(f"Auto-walk iniciado cada {interval}s")
        return True
    
    def stop_auto_walk(self) -> bool:
        """Stop auto-walk feature"""
        if not self.auto_walk_enabled:
            return False
        
        self.auto_walk_enabled = False
        self.logger.info("Auto-walk detenido")
        return True
    
    def start_auto_spell(self, interval: float = 5.0) -> bool:
        """Start auto-spell feature"""
        if self.auto_spell_enabled:
            self.logger.warning("Auto-spell ya está activo")
            return False
        
        self.spell_interval = interval
        self.auto_spell_enabled = True
        
        if not self.spell_thread or not self.spell_thread.is_alive():
            self.spell_thread = threading.Thread(target=self._spell_loop, daemon=True)
            self.spell_thread.start()
        
        self.logger.info(f"Auto-spell iniciado cada {interval}s")
        return True
    
    def stop_auto_spell(self) -> bool:
        """Stop auto-spell feature"""
        if not self.auto_spell_enabled:
            return False
        
        self.auto_spell_enabled = False
        self.logger.info("Auto-spell detenido")
        return True
    
    def start_monitoring(self, interval: float = 5.0) -> bool:
        """Start input monitoring"""
        self.monitor_interval = interval
        
        if not self.monitor_thread or not self.monitor_thread.is_alive():
            self.monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
            self.monitor_thread.start()
        
        self.logger.info(f"Monitoreo iniciado cada {interval}s")
        return True
    
    def get_status(self) -> Dict[str, Any]:
        """Get current bot status"""
        return {
            'running': self.running,
            'auto_attack': self.auto_attack_enabled,
            'auto_loot': self.auto_loot_enabled,
            'auto_walk': self.auto_walk_enabled,
            'auto_spell': self.auto_spell_enabled,
            'attack_interval': self.attack_interval,
            'loot_interval': self.loot_interval,
            'walk_interval': self.walk_interval,
            'spell_interval': self.spell_interval,
            'monitor_interval': self.monitor_interval
        }
    
    def start_all_features(self) -> bool:
        """Start all bot features"""
        self.running = True
        
        # Start monitoring first
        self.start_monitoring()
        
        # Start features
        self.start_auto_attack()
        self.start_auto_loot()
        self.start_auto_walk()
        # self.start_auto_spell()  # Commented out as requested
        
        self.logger.info("Todas las funcionalidades iniciadas")
        return True
    
    def stop_all_features(self) -> bool:
        """Stop all bot features"""
        self.running = False
        
        self.stop_auto_attack()
        self.stop_auto_loot()
        self.stop_auto_walk()
        self.stop_auto_spell()
        
        self.logger.info("Todas las funcionalidades detenidas")
        return True

if __name__ == "__main__":
    # Test the bot features
    window_manager = WindowManager()
    input_manager = InputManager(window_manager)
    features = BotFeatures(window_manager, input_manager)
    
    print("Iniciando test de funcionalidades...")
    features.start_all_features()
    
    try:
        time.sleep(10)
    except KeyboardInterrupt:
        print("Deteniendo bot...")
    
    features.stop_all_features()
    print("Test completado") 