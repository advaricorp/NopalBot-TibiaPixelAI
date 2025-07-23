"""
PBT Bot - Main Bot Logic
Enhanced version with spells, movement, and configuration
By Taquito Loco 🎮
"""

import os
import time
import logging
import threading
import random
import keyboard
from typing import Optional, Dict, Any, List
from queue import Queue

# Import utils and config
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.window_manager import WindowManager
from utils.input_manager import InputManager
from config.config_manager import ConfigManager

class PBTBot:
    """Enhanced PBT Bot with spells, movement, and configuration"""
    
    def __init__(self, log_file: str = "logs/pbt_bot.log"):
        # Ensure logs directory exists
        os.makedirs("logs", exist_ok=True)
        
        # Setup logger
        self.logger = self._setup_logger(log_file)
        
        # Load configuration
        self.config = ConfigManager()
        
        # Bot state
        self.running = False
        self.paused = False
        
        # Setup managers
        self.window_manager = WindowManager()
        self.input_manager = InputManager(self.window_manager)
        
        # Combat state
        self.in_combat = False
        self.last_combat_time = 0
        self.last_attack_time = 0
        self.last_spell_time = 0
        self.last_loot_time = 0
        self.last_movement_time = 0
        
        # Health and mana tracking (simulated)
        self.current_health = 100
        self.current_mana = 100
        self.max_health = 100
        self.max_mana = 100
        
        # Movement state - Enhanced for better stair handling
        self.current_direction_index = 0
        self.movement_steps = 0
        self.on_stairs = False
        self.stuck_counter = 0
        self.last_position = None
        self.movement_pattern = self.config.get_movement_pattern()
        
        # Enhanced movement patterns for different scenarios
        self.movement_patterns = {
            "patrol": ["w", "a", "s", "d"],
            "random": ["w", "a", "s", "d"],
            "stair_up": ["w"],
            "stair_down": ["s"],
            "unstuck": ["w", "a", "s", "d", "w", "a", "s", "d"],  # Extended pattern for unstucking
            "corner_escape": ["a", "w", "d", "s", "a", "w", "d", "s"]  # Pattern to escape corners
        }
        
        # Setup hotkeys
        self._setup_hotkeys()
        
        self.logger.info("PBT Bot inicializado con configuración completa")
        self.logger.info(f"Profesión: {self.config.get_setting('bot_settings', 'profession')}")
        self.logger.info(f"Hechizos habilitados: {self.config.is_feature_enabled('spells_enabled')}")
        self.logger.info("🎯 Core features: Attack (SPACE), Movement (WASD), Loot (F4)")
    
    def _setup_logger(self, log_file: str) -> logging.Logger:
        """Setup logging"""
        logger = logging.getLogger('PBTBot')
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
        pause_key = self.config.get_hotkey('pause')
        stop_key = self.config.get_hotkey('stop')
        emergency_key = self.config.get_hotkey('emergency_kill')
        
        # Setup hotkey listeners
        keyboard.add_hotkey(pause_key, self._toggle_pause, suppress=True)
        keyboard.add_hotkey(stop_key, self._stop_bot, suppress=True)
        keyboard.add_hotkey(emergency_key, self._emergency_kill, suppress=True)
        
        # Manual control hotkeys
        attack_key = self.config.get_hotkey('attack')
        loot_key = self.config.get_hotkey('loot')
        
        keyboard.add_hotkey(attack_key, self._manual_attack, suppress=True)
        keyboard.add_hotkey(loot_key, self._manual_loot, suppress=True)
        
        self.logger.info(f"🔑 Hotkeys configurados: Pause={pause_key}, Stop={stop_key}, Emergency={emergency_key}")
        self.logger.info(f"⚔️ Attack={attack_key}, 💰 Loot={loot_key}")
    
    def _toggle_pause(self):
        """Toggle bot pause state"""
        self.paused = not self.paused
        status = "PAUSED" if self.paused else "RESUMED"
        self.logger.info(f"⏸️ Bot {status}")
    
    def _stop_bot(self):
        """Stop the bot"""
        self.running = False
        self.logger.info("🛑 Bot stopped by hotkey")
    
    def _emergency_kill(self):
        """Emergency kill - stops all processes"""
        self.running = False
        self.logger.warning("🚨 EMERGENCY KILL ACTIVATED!")
        # Additional emergency cleanup can be added here
        os._exit(0)
    
    def _manual_attack(self):
        """Manual attack trigger"""
        if self.running and not self.paused:
            self._perform_attack()
            self.logger.info("⚔️ Manual attack triggered")
    
    def _manual_loot(self):
        """Manual loot trigger"""
        if self.running and not self.paused:
            self._perform_loot()
            self.logger.info("💰 Manual loot triggered")
    
    def _perform_attack(self):
        """Perform attack action"""
        if not self.config.is_feature_enabled('auto_attack'):
            return
        
        current_time = time.time()
        cooldown = self.config.get_timing('attack_cooldown')
        
        if current_time - self.last_attack_time >= cooldown:
            attack_key = self.config.get_hotkey('attack')
            self.input_manager.press_key(attack_key)
            self.last_attack_time = current_time
            self.in_combat = True
            self.last_combat_time = current_time
            
            # Simulate health/mana changes during combat
            self._simulate_combat_effects()
    
    def _perform_loot(self):
        """Perform loot action"""
        if not self.config.is_feature_enabled('auto_loot'):
            return
        
        current_time = time.time()
        cooldown = self.config.get_timing('loot_cooldown')
        
        if current_time - self.last_loot_time >= cooldown:
            loot_key = self.config.get_hotkey('loot')
            self.input_manager.press_key(loot_key)
            self.last_loot_time = current_time
            self.logger.debug("💰 Loot action performed")
    
    def _perform_movement(self):
        """Enhanced movement with stair detection and anti-stuck"""
        if not self.config.is_feature_enabled('auto_movement'):
            return
        
        current_time = time.time()
        cooldown = self.config.get_timing('movement_cooldown')
        
        if current_time - self.last_movement_time >= cooldown:
            movement_type = self.config.get_setting('bot_settings', 'movement_type')
            
            # Enhanced movement logic
            if self._detect_stairs():
                # Handle stairs
                if movement_type == "stair_up":
                    self._handle_stair_movement("up")
                elif movement_type == "stair_down":
                    self._handle_stair_movement("down")
                else:
                    # Auto-detect stair direction and handle
                    self._handle_stair_movement("auto")
            else:
                # Normal movement with anti-stuck
                self._handle_normal_movement(movement_type)
            
            self.last_movement_time = current_time
    
    def _handle_stair_movement(self, direction: str):
        """Handle stair movement"""
        if direction == "up":
            key = self.config.get_hotkey('movement_up')
            self.input_manager.press_key(key)
            self.logger.debug("🪜 Moving up stairs")
        elif direction == "down":
            key = self.config.get_hotkey('movement_down')
            self.input_manager.press_key(key)
            self.logger.debug("🪜 Moving down stairs")
        else:
            # Auto-detect: try up first, then down
            up_key = self.config.get_hotkey('movement_up')
            down_key = self.config.get_hotkey('movement_down')
            
            # Try up first
            self.input_manager.press_key(up_key)
            time.sleep(0.1)
            # If still on stairs, try down
            if self._detect_stairs():
                self.input_manager.press_key(down_key)
                self.logger.debug("🪜 Auto stair movement (down)")
            else:
                self.logger.debug("🪜 Auto stair movement (up)")
        
        self.on_stairs = True
        self.stuck_counter = 0  # Reset stuck counter on stairs
    
    def _handle_normal_movement(self, movement_type: str):
        """Handle normal movement with anti-stuck logic"""
        # Get movement pattern
        if movement_type == "random":
            # Random movement
            movement_keys = ["w", "a", "s", "d"]
            key = random.choice(movement_keys)
            self.input_manager.press_key(key)
            self.logger.debug(f"🚶 Random movement: {key}")
        else:
            # Pattern-based movement
            pattern = self.movement_patterns.get(movement_type, self.movement_patterns["patrol"])
            
            # Check if stuck
            if self._is_stuck():
                # Use unstuck pattern
                pattern = self.movement_patterns["unstuck"]
                self.logger.debug("🚧 Detected stuck, using unstuck pattern")
            
            # Get next direction
            key = pattern[self.current_direction_index % len(pattern)]
            self.input_manager.press_key(key)
            
            # Update direction index
            self.current_direction_index = (self.current_direction_index + 1) % len(pattern)
            self.movement_steps += 1
            
            self.logger.debug(f"🚶 Movement: {key} (step {self.movement_steps})")
        
        # Reset stuck counter on successful movement
        self.stuck_counter = max(0, self.stuck_counter - 1)
    
    def _detect_stairs(self) -> bool:
        """Enhanced stair detection"""
        # This is a simplified detection - in a real implementation,
        # you would use image recognition to detect stair tiles
        # For now, we'll simulate stair detection based on movement patterns
        
        # Simulate stair detection (every 10-15 movements)
        if self.movement_steps > 0 and self.movement_steps % random.randint(10, 15) == 0:
            self.logger.debug("🪜 Stair detection triggered")
            return True
        
        return False
    
    def _is_stuck(self) -> bool:
        """Detect if bot is stuck"""
        # Simulate stuck detection
        # In a real implementation, you would compare current position with previous positions
        
        # For now, simulate getting stuck occasionally
        if random.random() < 0.05:  # 5% chance of getting stuck
            self.stuck_counter += 1
            if self.stuck_counter > 3:
                self.logger.warning("🚧 Bot appears to be stuck!")
                return True
        
        return False
    
    def _simulate_combat_effects(self):
        """Simulate health and mana changes during combat"""
        # Simulate health loss during combat
        if self.in_combat:
            health_loss = random.randint(5, 15)
            self.current_health = max(0, self.current_health - health_loss)
            
            # Simulate mana usage
            mana_loss = random.randint(2, 8)
            self.current_mana = max(0, self.current_mana - mana_loss)
            
            self.logger.debug(f"❤️ Health: {self.current_health}/{self.max_health}, 🔮 Mana: {self.current_mana}/{self.max_mana}")
    
    def _check_health_and_mana(self):
        """Check health and mana levels and cast spells if needed"""
        if not self.config.is_feature_enabled('spells_enabled'):
            return
        
        current_time = time.time()
        cooldown = self.config.get_timing('spell_cooldown')
        
        if current_time - self.last_spell_time >= cooldown:
            spell_info = self._should_cast_spell()
            if spell_info:
                spell_type, spell_name = spell_info
                self._cast_spell(spell_type, spell_name)
                self.last_spell_time = current_time
    
    def _cast_spell(self, spell_type: str, spell_name: str):
        """Cast a spell"""
        try:
            # In a real implementation, you would send the spell text to Tibia
            # For now, we'll simulate spell casting
            self.logger.info(f"🔮 Casting {spell_type} spell: {spell_name}")
            
            # Simulate spell effects
            if spell_type == "healing":
                heal_amount = random.randint(20, 40)
                self.current_health = min(self.max_health, self.current_health + heal_amount)
                self.logger.info(f"❤️ Healed for {heal_amount} HP")
            elif spell_type == "emergency":
                heal_amount = random.randint(40, 60)
                self.current_health = min(self.max_health, self.current_health + heal_amount)
                self.logger.info(f"🚨 Emergency heal for {heal_amount} HP")
            
            # Simulate mana cost
            mana_cost = random.randint(5, 15)
            self.current_mana = max(0, self.current_mana - mana_cost)
            
        except Exception as e:
            self.logger.error(f"❌ Error casting spell: {e}")
    
    def _should_cast_spell(self) -> Optional[tuple]:
        """Determine if and which spell should be cast"""
        profession = self.config.get_setting('bot_settings', 'profession')
        spells = self.config.get_profession_spells(profession)
        
        health_low = self.config.get_threshold('health_low')
        health_medium = self.config.get_threshold('health_medium')
        mana_low = self.config.get_threshold('mana_low')
        
        # Emergency spells (very low health)
        if self.current_health <= health_low and self.config.is_feature_enabled('emergency_spells'):
            emergency_spells = spells.get('emergency', [])
            if emergency_spells and self.current_mana > mana_low:
                return ('emergency', random.choice(emergency_spells))
        
        # Healing spells (low health)
        elif self.current_health <= health_medium:
            healing_spells = spells.get('healing', [])
            if healing_spells and self.current_mana > mana_low:
                return ('healing', random.choice(healing_spells))
        
        # Support spells (when not in immediate danger)
        elif self.current_health > health_medium and self.current_mana > mana_low:
            support_spells = spells.get('support', [])
            if support_spells and random.random() < 0.3:  # 30% chance
                return ('support', random.choice(support_spells))
        
        return None
    
    def _combat_loop(self):
        """Combat loop - handles attacking and spell casting"""
        while self.running:
            try:
                if not self.paused:
                    # Perform attack
                    self._perform_attack()
                    
                    # Check health and cast spells
                    self._check_health_and_mana()
                    
                    # Simulate combat state changes
                    current_time = time.time()
                    if current_time - self.last_combat_time > 5:  # 5 seconds without combat
                        self.in_combat = False
                
                time.sleep(0.1)  # 100ms loop
                
            except Exception as e:
                self.logger.error(f"❌ Error in combat loop: {e}")
                time.sleep(1)
    
    def _movement_loop(self):
        """Movement loop - handles movement and stair detection"""
        while self.running:
            try:
                if not self.paused:
                    self._perform_movement()
                
                time.sleep(0.5)  # 500ms loop for movement
                
            except Exception as e:
                self.logger.error(f"❌ Error in movement loop: {e}")
                time.sleep(1)
    
    def _loot_loop(self):
        """Loot loop - handles automatic looting"""
        while self.running:
            try:
                if not self.paused:
                    self._perform_loot()
                
                time.sleep(2)  # 2 second loop for looting
                
            except Exception as e:
                self.logger.error(f"❌ Error in loot loop: {e}")
                time.sleep(1)
    
    def _detect_enemies(self):
        """Detect enemies (simulated)"""
        # In a real implementation, you would use image recognition
        # to detect enemies on screen
        # For now, we'll simulate enemy detection
        if random.random() < 0.1:  # 10% chance of detecting enemy
            self.in_combat = True
            self.last_combat_time = time.time()
            self.logger.debug("👹 Enemy detected")
    
    def _detection_loop(self):
        """Detection loop - handles enemy detection"""
        while self.running:
            try:
                if not self.paused:
                    self._detect_enemies()
                
                time.sleep(1)  # 1 second loop for detection
                
            except Exception as e:
                self.logger.error(f"❌ Error in detection loop: {e}")
                time.sleep(1)
    
    def start(self) -> bool:
        """Start the bot"""
        try:
            if self.running:
                self.logger.warning("Bot is already running")
                return False
            
            self.running = True
            self.paused = False
            
            # Start all loops in separate threads
            combat_thread = threading.Thread(target=self._combat_loop, daemon=True)
            movement_thread = threading.Thread(target=self._movement_loop, daemon=True)
            loot_thread = threading.Thread(target=self._loot_loop, daemon=True)
            detection_thread = threading.Thread(target=self._detection_loop, daemon=True)
            
            combat_thread.start()
            movement_thread.start()
            loot_thread.start()
            detection_thread.start()
            
            self.logger.info("🚀 Bot started successfully")
            self.logger.info(f"🎭 Profession: {self.config.get_setting('bot_settings', 'profession')}")
            self.logger.info(f"⚔️ Auto Attack: {'ENABLED' if self.config.is_feature_enabled('auto_attack') else 'DISABLED'}")
            self.logger.info(f"🚶 Auto Movement: {'ENABLED' if self.config.is_feature_enabled('auto_movement') else 'DISABLED'}")
            self.logger.info(f"💰 Auto Loot: {'ENABLED' if self.config.is_feature_enabled('auto_loot') else 'DISABLED'}")
            self.logger.info(f"🔮 Spells: {'ENABLED' if self.config.is_feature_enabled('spells_enabled') else 'DISABLED'}")
            self.logger.info("💀 F12 for EMERGENCY KILL")
            
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Error starting bot: {e}")
            return False
    
    def stop(self) -> bool:
        """Stop the bot"""
        try:
            if not self.running:
                self.logger.warning("Bot is not running")
                return False
            
            self.running = False
            self.paused = False
            
            # Clean up hotkeys
            keyboard.unhook_all()
            
            self.logger.info("✅ Bot stopped successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Error stopping bot: {e}")
            return False
    
    def get_status(self) -> Dict[str, Any]:
        """Get current bot status"""
        return {
            "running": self.running,
            "paused": self.paused,
            "profession": self.config.get_setting("bot_settings", "profession"),
            "health": self.current_health,
            "mana": self.current_mana,
            "in_combat": self.in_combat,
            "on_stairs": self.on_stairs,
            "movement_steps": self.movement_steps,
            "stuck_counter": self.stuck_counter,
            "features": {
                "auto_attack": self.config.is_feature_enabled("auto_attack"),
                "auto_movement": self.config.is_feature_enabled("auto_movement"),
                "auto_loot": self.config.is_feature_enabled("auto_loot"),
                "spells_enabled": self.config.is_feature_enabled("spells_enabled"),
                "emergency_spells": self.config.is_feature_enabled("emergency_spells"),
            },
            "hotkeys": {
                "attack": self.config.get_hotkey("attack"),
                "loot": self.config.get_hotkey("loot"),
                "movement_type": self.config.get_setting("bot_settings", "movement_type"),
            }
        }
    
    def run(self) -> None:
        """Main run method"""
        if self.start():
            try:
                # Keep main thread alive
                while self.running:
                    time.sleep(1)
            except KeyboardInterrupt:
                self.logger.info("🛑 Bot interrupted by user")
            finally:
                self.stop()

def main():
    """Main function"""
    bot = PBTBot()
    bot.run()

if __name__ == "__main__":
    main() 