"""
Improved Tibia Bot
Enhanced version with intelligent target locking and smart combat behavior
"""

import os
import time
import logging
import threading
import random
import keyboard
from typing import Optional, Dict, Any
from utils.window_manager import WindowManager
from utils.input_manager import InputManager

class ImprovedBot:
    """Enhanced bot with intelligent target locking and smart combat behavior"""
    
    def __init__(self, log_file: str = "logs/improved_bot.log"):
        # Ensure logs directory exists
        os.makedirs("logs", exist_ok=True)
        
        # Setup logger
        self.logger = self._setup_logger(log_file)
        
        # Bot state
        self.running = False
        self.paused = False
        
        # Feature configuration
        self.auto_attack_enabled = True
        self.auto_loot_enabled = True
        self.auto_movement_enabled = True
        self.auto_heal_enabled = True
        self.auto_potions_enabled = True
        self.target_locking_enabled = True
        
        # Humanization settings
        self.humanization_enabled = True
        self.mouse_humanization = True
        self.keyboard_humanization = True
        
        # Combat state
        self.in_combat = False
        self.last_combat_time = 0
        self.target_locked = False
        self.target_lock_start = 0
        self.target_lock_duration = 30  # 30 seconds
        self.combat_timeout = 10.0  # Consider combat over after 10 seconds of no attacks
        self.attack_cooldown = 1.0  # Wait 1 second between attacks
        self.max_consecutive_attacks = 5  # Max attacks before checking if target is dead
        self.last_attack_time = 0
        
        # Movement state
        self.movement_pattern = ['w', 'a', 's', 'd']  # Up, Left, Down, Right
        self.current_direction_index = 0
        self.movement_steps = 0
        self.max_movement_steps = 5
        self.last_movement_time = 0
        self.movement_cooldown = 2.0  # 2 seconds between movements
        
        # Loot state
        self.last_loot_time = 0
        self.loot_cooldown = 6.0  # 6 seconds between loot attempts (más lento)
        self.last_gold_loot_time = 0
        self.gold_loot_cooldown = 4.0  # 4 seconds between gold loot attempts (más lento)
        
        # Health and potion state
        self.last_heal_time = 0
        self.heal_cooldown = 3.0  # 3 seconds between heals
        self.last_health_check = 0
        self.health_check_cooldown = 1.0  # 1 second between health checks
        self.last_potion_check = 0
        self.potion_check_cooldown = 1.0  # 1 second between potion checks
        self.last_health_potion_time = 0
        self.last_mana_potion_time = 0
        self.potion_cooldown = 2.0  # 2 seconds between potions
        
        # Random healing thresholds to avoid detection
        self.health_threshold_min = 25  # Minimum health percentage to heal
        self.health_threshold_max = 50  # Maximum health percentage to heal
        self.mana_threshold_min = 20    # Minimum mana percentage to use potion
        self.mana_threshold_max = 45    # Maximum mana percentage to use potion
        
        # Current random thresholds (will be regenerated periodically)
        self.current_health_threshold = random.randint(self.health_threshold_min, self.health_threshold_max)
        self.current_mana_threshold = random.randint(self.mana_threshold_min, self.mana_threshold_max)
        self.threshold_regeneration_time = 0
        self.threshold_regeneration_cooldown = 300  # Regenerate thresholds every 5 minutes
        
        # Player detection state
        self.players_nearby = False
        self.last_player_check = 0
        self.player_check_cooldown = 5.0  # 5 seconds between player checks
        self.last_player_detection = 0
        self.player_detection_timeout = 10.0  # 10 seconds timeout for player detection
        
        # Hotkeys
        self.pause_key = 'f1'
        self.stop_key = 'f2'
        self.attack_key = 'f3'
        self.loot_key = 'f4'
        self.health_potion_key = 'f1'
        self.mana_potion_key = 'f2'
        self.exura_infir_key = 'f3'
        self.emergency_kill_key = 'f12'  # F12 for emergency kill
        
        # Setup managers
        self.window_manager = WindowManager()
        self.input_manager = InputManager(self.window_manager)
        
        # Setup hotkeys
        self._setup_hotkeys()
        
        self.logger.info("Bot mejorado inicializado")
    
    def _setup_logger(self, log_file: str) -> logging.Logger:
        """Setup logging"""
        logger = logging.getLogger('ImprovedBot')
        logger.setLevel(logging.INFO)
        
        # Clear existing handlers
        for handler in logger.handlers[:]:
            logger.removeHandler(handler)
        
        # File handler
        fh = logging.FileHandler(log_file, encoding='utf-8')
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
    
    def _setup_hotkeys(self):
        """Setup control hotkeys"""
        keyboard.add_hotkey(self.pause_key, self._toggle_pause, suppress=True)
        keyboard.add_hotkey(self.stop_key, self._stop_bot, suppress=True)
        keyboard.add_hotkey(self.attack_key, self._manual_attack, suppress=True)
        keyboard.add_hotkey(self.loot_key, self._manual_loot, suppress=True)
        keyboard.add_hotkey(self.emergency_kill_key, self._emergency_kill, suppress=True)
        keyboard.add_hotkey('end', self._emergency_kill, suppress=True)  # End key as backup
        
        self.logger.info(f"Controles configurados:")
        self.logger.info(f"  {self.pause_key.upper()} - Pausar/Reanudar")
        self.logger.info(f"  {self.stop_key.upper()} - Detener bot")
        self.logger.info(f"  {self.attack_key.upper()} - Ataque manual")
        self.logger.info(f"  {self.loot_key.upper()} - Loot manual")
        self.logger.info(f"  {self.emergency_kill_key.upper()} - KILL EMERGENCY")
    
    def _toggle_pause(self):
        """Toggle pause state and release mouse"""
        self.paused = not self.paused
        if self.paused:
            # Release mouse buttons when pausing
            try:
                import ctypes
                ctypes.windll.user32.mouse_event(0x0004, 0, 0, 0, 0)  # Left up
                ctypes.windll.user32.mouse_event(0x0010, 0, 0, 0, 0)  # Right up
                ctypes.windll.user32.mouse_event(0x0040, 0, 0, 0, 0)  # Middle up
                self.logger.info("PAUSA - Mouse liberado - Presiona F1 para reanudar")
            except:
                self.logger.info("PAUSA - Presiona F1 para reanudar")
        else:
            self.logger.info("REANUDADO")
    
    def _stop_bot(self):
        """Stop the bot"""
        self.logger.info("DETENIENDO BOT...")
        self.running = False
    
    def _emergency_kill(self):
        """Emergency kill - terminate all bot processes"""
        self.logger.info("🚨 EMERGENCY KILL ACTIVATED!")
        self.logger.info("💀 Terminando TODOS los procesos del bot...")
        
        # Stop this bot instance
        self.running = False
        self.paused = False
        
        # Force exit the process
        import os
        import signal
        os._exit(0)  # Force exit immediately
    
    def _manual_attack(self):
        """Manual attack"""
        if self.running and not self.paused:
            self.input_manager.send_attack()
            self.logger.info("Ataque manual ejecutado")
    
    def _manual_loot(self):
        """Manual loot"""
        if self.running and not self.paused:
            self._perform_loot()
            self.logger.info("Loot manual ejecutado")
    
    def manual_attack(self):
        """Manual attack - public method"""
        self._manual_attack()
    
    def manual_loot(self):
        """Manual loot - public method"""
        self._manual_loot()
    
    def _detect_combat(self) -> bool:
        """Detect if we're in combat by checking for enemies"""
        # This is a simplified detection - in a real implementation you'd use
        # image recognition to detect enemies in the battle list
        # For now, we'll use a heuristic based on attack patterns
        
        current_time = time.time()
        
        # If we've been attacking recently, we're likely in combat
        if current_time - self.last_attack_time < 5.0:
            self.in_combat = True
            self.last_combat_time = current_time
            return True
        
        # If we haven't attacked for a while, combat might be over
        if current_time - self.last_combat_time > self.combat_timeout:
            self.in_combat = False
            self.target_locked = False
            self.current_target = None
            self.logger.info("🔄 Combate terminado - Iniciando patrulla")
            return False
        
        return self.in_combat
    
    def _smart_attack(self) -> bool:
        """Smart attack with target locking - only attack if safe and target is locked"""
        if not self.running or self.paused:
            return False
        
        current_time = time.time()
        
        # Check if it's safe to attack (no players nearby)
        if not self._safe_to_attack():
            return False
        
        # Check if we have a locked target and target locking is enabled
        if self.target_locking_enabled and self.target_locked:
            # Check if target lock has expired
            if current_time - self.target_lock_start > self.target_lock_duration:
                self.target_locked = False
                self.logger.info("Objetivo posiblemente muerto - Desbloqueando")
                return False
            
            # Attack the locked target
            if self.input_manager.send_attack():
                self.logger.info("Atacando objetivo bloqueado")
                return True
        else:
            # No locked target, try to find a new one
            if self.input_manager.send_attack():
                self.logger.info("Enemigo detectado - Iniciando combate")
                self.in_combat = True
                self.last_combat_time = current_time
                
                # Lock the target if target locking is enabled
                if self.target_locking_enabled:
                    self.target_locked = True
                    self.target_lock_start = current_time
                    self.logger.info("OBJETIVO BLOQUEADO - Enfocando en un enemigo por 30 segundos")
                
                return True
        
        return False
    
    def _perform_loot(self):
        """Perform loot operation with left and right click - SLOWER and STAIR-SAFE"""
        # Safe loot positions (avoiding stairs)
        safe_loot_positions = [
            (400, 300),  # Center - más seguro
            (350, 250),  # Top-left - lejos de escaleras
            (450, 250),  # Top-right - lejos de escaleras
            (350, 350),  # Bottom-left - lejos de escaleras
            (450, 350),  # Bottom-right - lejos de escaleras
        ]
        
        # Stair positions to avoid
        stair_positions = [
            (400, 200),  # Posible escalera arriba
            (400, 400),  # Posible escalera abajo
            (300, 300),  # Posible escalera izquierda
            (500, 300),  # Posible escalera derecha
        ]
        
        for x, y in safe_loot_positions:
            if not self.running or self.paused:
                break
                
            # Check if position is near stairs
            near_stairs = False
            for stair_x, stair_y in stair_positions:
                distance = ((x - stair_x) ** 2 + (y - stair_y) ** 2) ** 0.5
                if distance < 80:  # Si está muy cerca de escaleras, saltar
                    near_stairs = True
                    break
            
            if near_stairs:
                self.logger.info(f"⚠️ Saltando posición ({x}, {y}) - muy cerca de escaleras")
                continue
            
            # Left click - MÁS LENTO
            self.input_manager.click_position(x, y)
            time.sleep(0.5)  # Doble de lento (0.2 -> 0.5)
            
            # Right click - MÁS LENTO
            self.input_manager.right_click_position(x, y)
            time.sleep(0.5)  # Doble de lento (0.2 -> 0.5)
    
    def _perform_gold_loot(self):
        """Perform gold looting with improved coordinates"""
        if not self.running or self.paused:
            return
        
        current_time = time.time()
        
        # Only loot gold if enough time has passed
        if current_time - self.last_gold_loot_time < self.gold_loot_cooldown:
            return
        
        # Try to loot gold from corpses
        # Use coordinates relative to Tibia client area (not screen coordinates)
        # These coordinates are for the center area of the Tibia client where corpses typically appear
        
        # Get Tibia window dimensions to calculate relative positions
        if self.window_manager.tibia_hwnd:
            window_rect = self.window_manager.get_window_rect(self.window_manager.tibia_hwnd)
            window_x, window_y, window_right, window_bottom = window_rect
            window_width = window_right - window_x
            window_height = window_bottom - window_y
            
            # Calculate relative positions for loot areas
            # Tibia client area is typically the center portion of the window
            client_width = window_width - 16  # Account for borders
            client_height = window_height - 60  # Account for title bar and UI elements
            
            # Define loot areas in the center of the client area
            loot_positions = [
                (client_width // 2, client_height // 2),  # Center
                (client_width // 2 - 50, client_height // 2),  # Left of center
                (client_width // 2 + 50, client_height // 2),  # Right of center
                (client_width // 2, client_height // 2 - 50),  # Above center
                (client_width // 2, client_height // 2 + 50),  # Below center
            ]
            
            self.logger.info("Buscando cadáveres para lootear oro...")
            
            for gold_x, gold_y in loot_positions:
                if not self.running or self.paused:
                    break
                # Right click to loot gold - MÁS LENTO
                self.input_manager.click_position(gold_x, gold_y)
                time.sleep(0.5)  # Doble de lento (0.2 -> 0.5)
            
            # Close loot window with escape key - MÁS LENTO
            self.input_manager.send_key('escape')
            time.sleep(0.5)  # Doble de lento (0.2 -> 0.5)
        
        self.last_gold_loot_time = current_time
    
    def _smart_movement(self):
        """Smart movement - move after killing enemies, patrol area"""
        if not self.running or self.paused:
            return
        
        current_time = time.time()
        
        # Check if we should exit combat mode (enemy might be dead)
        if self.in_combat and current_time - self.last_combat_time > 5.0:
            self.in_combat = False
            self.target_locked = False
            self.logger.info("🔄 Enemigo posiblemente muerto - Iniciando patrulla")
        
        # Move if not in combat OR if enough time has passed since last movement
        if (not self.in_combat or current_time - self.last_movement_time > self.movement_cooldown * 2):
            # Get current direction
            direction = self.movement_pattern[self.current_direction_index]
            
            # Send movement
            if self.input_manager.send_movement(direction):
                self.last_movement_time = current_time
                self.movement_steps += 1
                self.logger.info(f"🚶 Movimiento: {direction} (paso {self.movement_steps}/{self.max_movement_steps})")
            
            # Check if we should change direction (after max steps)
            if self.movement_steps >= self.max_movement_steps:
                self.current_direction_index = (self.current_direction_index + 1) % len(self.movement_pattern)
                self.movement_steps = 0
                self.logger.info(f"🔄 Cambiando dirección a: {self.movement_pattern[self.current_direction_index]}")
            
            # After moving, try to attack to see if we found enemies
            time.sleep(0.5)
            if self.input_manager.send_attack():
                self.logger.info("⚔️ ¡ENEMIGO DETECTADO! - Deteniendo movimiento y atacando")
                self.in_combat = True
                self.last_combat_time = current_time
                self.movement_steps = 0  # Reset movement steps
    
    def _detect_players(self):
        """Detect if there are players nearby to avoid attacking them"""
        current_time = time.time()
        
        # Only check for players if enough time has passed
        if current_time - self.last_player_check < self.player_check_cooldown:
            return
        
        # In a real implementation, you would use image recognition to detect players
        # For now, we'll simulate player detection by checking if we're in a safe area
        # This is a placeholder - in practice you'd scan the screen for player names
        
        # Simulate player detection (this would be replaced with actual image recognition)
        # For now, we'll assume no players are nearby unless specifically detected
        self.players_nearby = False
        
        # If players were detected recently, keep the flag active
        if current_time - self.last_player_detection < self.player_detection_timeout:
            self.players_nearby = True
        
        self.last_player_check = current_time
    
    def _safe_to_attack(self):
        """Check if it's safe to attack (no players nearby)"""
        return not self.players_nearby
    
    def _monitor_input(self):
        """Monitor input and window focus"""
        while self.running:
            try:
                if not self.paused:
                    # Check if Tibia is still in focus
                    if self.window_manager.tibia_hwnd and not self.window_manager.is_window_focused(self.window_manager.tibia_hwnd):
                        self.logger.warning("Tibia perdió el foco - PAUSANDO BOT AUTOMÁTICAMENTE")
                        self.paused = True
                        continue
                    
                    # Test input
                    if not self.input_manager.test_input():
                        self.logger.warning("Input perdido - Forzando ventana...")
                        self.window_manager.ensure_focus()
                else:
                    # Bot is paused, check if Tibia regained focus
                    if self.window_manager.tibia_hwnd and self.window_manager.is_window_focused(self.window_manager.tibia_hwnd):
                        self.logger.info("Tibia recuperó el foco - REANUDANDO BOT AUTOMÁTICAMENTE")
                        self.paused = False
                
                time.sleep(2.0)  # Check every 2 seconds
                
            except Exception as e:
                self.logger.error(f"Error en monitoreo: {e}")
                time.sleep(1)
    
    def _regenerate_thresholds(self):
        """Regenerate random healing thresholds to avoid detection"""
        current_time = time.time()
        
        # Only regenerate if enough time has passed
        if current_time - self.threshold_regeneration_time < self.threshold_regeneration_cooldown:
            return
        
        # Generate new random thresholds
        old_health = self.current_health_threshold
        old_mana = self.current_mana_threshold
        
        self.current_health_threshold = random.randint(self.health_threshold_min, self.health_threshold_max)
        self.current_mana_threshold = random.randint(self.mana_threshold_min, self.mana_threshold_max)
        
        self.threshold_regeneration_time = current_time
        
        self.logger.info(f"Umbrales regenerados - Vida: {old_health}% -> {self.current_health_threshold}%, Mana: {old_mana}% -> {self.current_mana_threshold}%")
    
    def _monitor_health(self):
        """Monitor health and cast healing spells when needed"""
        current_time = time.time()
        
        # Regenerate thresholds periodically
        self._regenerate_thresholds()
        
        # Only check health if enough time has passed
        if current_time - self.last_health_check < self.health_check_cooldown:
            return
        
        # Check if we need to heal (simulate health check)
        # In a real implementation, you would use image recognition to check health bar
        # For now, we'll heal periodically during combat using random thresholds
        if self.in_combat and current_time - self.last_heal_time > self.heal_cooldown:
            # Simulate health check - heal when below random threshold
            self.logger.info(f"Vida baja detectada ({self.current_health_threshold}%) - Lanzando Exura Infir")
            
            # Cast exura infir
            if self.input_manager.send_key('f3'):  # Changed from F5 to F3
                self.last_heal_time = current_time
                self.logger.info("Exura Infir lanzado")
        
        self.last_health_check = current_time
    
    def _monitor_potions(self):
        """Monitor health and mana, use potions when needed"""
        current_time = time.time()
        
        # Regenerate thresholds periodically
        self._regenerate_thresholds()
        
        # Only check potions if enough time has passed
        if current_time - self.last_potion_check < self.potion_check_cooldown:
            return
        
        # In a real implementation, you would use image recognition to check health/mana bars
        # For now, we'll simulate potion usage during combat using random thresholds
        
        # Check health potion
        if self.in_combat and current_time - self.last_health_potion_time > self.potion_cooldown:
            # Simulate low health detection using random threshold
            self.logger.info(f"Vida baja detectada ({self.current_health_threshold}%) - Usando Health Potion (F1)")
            
            # Use health potion
            if self.input_manager.send_key(self.health_potion_key):
                self.last_health_potion_time = current_time
                self.logger.info("Health Potion usado")
        
        # Check mana potion
        if self.in_combat and current_time - self.last_mana_potion_time > self.potion_cooldown:
            # Simulate low mana detection using random threshold
            self.logger.info(f"Mana baja detectada ({self.current_mana_threshold}%) - Usando Mana Potion (F2)")
            
            # Use mana potion
            if self.input_manager.send_key(self.mana_potion_key):
                self.last_mana_potion_time = current_time
                self.logger.info("Mana Potion usado")
        
        self.last_potion_check = current_time
    
    def _combat_loop(self):
        """Main combat loop - handles attack, movement, gold looting, health monitoring, potion monitoring, and player detection"""
        while self.running:
            try:
                if not self.paused:
                    # Check for players first (safety)
                    self._detect_players()
                    
                    # Monitor health and potions if enabled
                    if self.auto_heal_enabled:
                        self._monitor_health()
                    if self.auto_potions_enabled:
                        self._monitor_potions()
                    
                    # Try to attack if enabled
                    if self.auto_attack_enabled:
                        if not self._smart_attack():
                            # If no attack was made and movement is enabled, try movement
                            if self.auto_movement_enabled:
                                self._smart_movement()
                    else:
                        # If attack is disabled, just try movement
                        if self.auto_movement_enabled:
                            self._smart_movement()
                    
                    # Always try to loot gold if enabled
                    if self.auto_loot_enabled:
                        self._perform_gold_loot()
                
                time.sleep(0.5)  # Check every 0.5 seconds
                
            except Exception as e:
                self.logger.error(f"Error en combate: {e}")
                time.sleep(1)
    
    def _loot_loop(self):
        """Loot loop - only loot when not in combat"""
        while self.running:
            try:
                if not self.paused and not self.in_combat:
                    self._perform_loot()
                    self._perform_gold_loot() # Add gold looting here
                    self.logger.debug("Loot realizado (sin combate)")
                
                time.sleep(3.0)  # Loot every 3 seconds when safe
                
            except Exception as e:
                self.logger.error(f"Error en loot: {e}")
                time.sleep(1)
    
    def start(self) -> bool:
        """Start the improved bot"""
        if self.running:
            self.logger.warning("Bot ya está ejecutándose")
            return False
        
        # Setup Tibia window - be more lenient
        window_setup = self.window_manager.setup_tibia_window()
        if not window_setup:
            self.logger.warning("Advertencia: No se pudo configurar perfectamente la ventana de Tibia")
            self.logger.info("Intentando continuar de todas formas...")
        
        # Test input - be more lenient
        input_test = self.input_manager.test_input()
        if not input_test:
            self.logger.warning("Advertencia: No se pudo verificar el input perfectamente")
            self.logger.info("Intentando continuar de todas formas...")
        
        self.running = True
        self.paused = False
        
        # Start all threads
        self.combat_thread = threading.Thread(target=self._combat_loop, daemon=True)
        self.loot_thread = threading.Thread(target=self._loot_loop, daemon=True)
        self.input_monitor_thread = threading.Thread(target=self._monitor_input, daemon=True)
        
        self.combat_thread.start()
        self.loot_thread.start()
        self.input_monitor_thread.start()
        
        self.logger.info("MEJORADO TIBIA BOT INICIADO")
        self.logger.info("=" * 50)
        self.logger.info("NUEVAS FUNCIONALIDADES:")
        self.logger.info("   - Target locking (enfoca un enemigo hasta matarlo)")
        self.logger.info("   - Target locking persistente (30 segundos)")
        self.logger.info("   - Movimiento inteligente (solo mismo nivel, sin escaleras)")
        self.logger.info("   - Detección automática de enemigos")
        self.logger.info("   - Se detiene cuando detecta enemigos")
        self.logger.info("   - Loot de oro mejorado (right click en cadáveres)")
        self.logger.info("   - Monitoreo de vida automático")
        self.logger.info("   - Exura Infir automático (F3)")
        self.logger.info("   - Health Potion automático (F1)")
        self.logger.info("   - Mana Potion automático (F2)")
        self.logger.info("   - DETECCIÓN DE JUGADORES (evita atacar personas)")
        self.logger.info("   - UMBRALES ALEATORIOS (25-50% vida, 20-45% mana)")
        self.logger.info("   - PAUSA AUTOMÁTICA cuando Tibia pierde foco")
        self.logger.info("")
        self.logger.info("CONTROLES:")
        self.logger.info(f"   {self.pause_key.upper()} - Pausar/Reanudar")
        self.logger.info(f"   {self.stop_key.upper()} - Detener bot")
        self.logger.info(f"   {self.attack_key.upper()} - Ataque manual")
        self.logger.info(f"   {self.loot_key.upper()} - Loot manual")
        self.logger.info("   F1 - Health Potion (configurar en Tibia)")
        self.logger.info("   F2 - Mana Potion (configurar en Tibia)")
        self.logger.info("   F3 - Exura Infir (configurar en Tibia)")
        self.logger.info("")
        self.logger.info(f"Umbrales actuales - Vida: {self.current_health_threshold}%, Mana: {self.current_mana_threshold}%")
        self.logger.info("Bot iniciado - Usa F1 para pausar, F2 para detener")
        
        return True
    
    def stop(self) -> bool:
        """Stop the improved bot"""
        if not self.running:
            self.logger.warning("Bot no está ejecutándose")
            return False
        
        self.logger.info("Deteniendo bot mejorado...")
        self.running = False
        self.paused = False
        
        # Wait for threads to finish
        if hasattr(self, 'combat_thread'):
            self.combat_thread.join(timeout=2.0)
        if hasattr(self, 'loot_thread'):
            self.loot_thread.join(timeout=2.0)
        if hasattr(self, 'input_monitor_thread'):
            self.input_monitor_thread.join(timeout=2.0)
        
        self.logger.info("Bot detenido correctamente")
        return True
    
    def pause(self) -> bool:
        """Pause the bot"""
        if not self.running:
            return False
        
        self.paused = True
        self.logger.info("Bot pausado")
        return True
    
    def resume(self) -> bool:
        """Resume the bot"""
        if not self.running:
            return False
        
        self.paused = False
        self.logger.info("Bot reanudado")
        return True
    
    def run(self) -> None:
        """Main run loop"""
        if not self.start():
            self.logger.error("No se pudo iniciar el bot")
            return
        
        try:
            # Start all threads
            threads = []
            
            # Monitor thread
            monitor_thread = threading.Thread(target=self._monitor_input, daemon=True)
            monitor_thread.start()
            threads.append(monitor_thread)
            
            # Combat thread (handles attack and movement)
            combat_thread = threading.Thread(target=self._combat_loop, daemon=True)
            combat_thread.start()
            threads.append(combat_thread)
            
            # Loot thread
            loot_thread = threading.Thread(target=self._loot_loop, daemon=True)
            loot_thread.start()
            threads.append(loot_thread)
            
            # Main loop
            while self.running:
                time.sleep(1)
                
                # Check if any thread died
                for thread in threads:
                    if not thread.is_alive():
                        self.logger.warning("Un hilo se detuvo inesperadamente")
                        break
                        
        except KeyboardInterrupt:
            self.logger.info("Interrupción de teclado recibida")
        except Exception as e:
            self.logger.error(f"Error en el bucle principal: {e}")
        finally:
            self.stop()

def main():
    """Main entry point"""
    print("MEJORADO TIBIA BOT - VERSION INTELIGENTE")
    print("=" * 50)
    
    try:
        bot = ImprovedBot()
        bot.run()
    except KeyboardInterrupt:
        print("\nBot detenido por el usuario")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main() 