"""
Bot Core Module for Tibia Bot

This module provides the main bot functionality by orchestrating
all the different modules (vision, control, features, etc.).
"""

import time
import threading
from typing import Optional, Dict, Any
from pathlib import Path

# Import our modules
from vision.screen_reader import ScreenReader
from vision.template_matcher import TemplateMatcher
from control.keyboard_controller import KeyboardController
from control.mouse_controller import MouseController
from core.state_machine import StateMachine, BotState
from config.config_manager import ConfigManager
from features.auto_attack import AutoAttack
from features.auto_loot import AutoLoot
from features.auto_walk import AutoWalk


class BotCore:
    """
    Main bot core that orchestrates all modules.
    
    This class provides the main bot functionality by coordinating
    the vision, control, state management, and feature modules.
    """
    
    def __init__(self, config_dir: str = "config"):
        """
        Initialize the BotCore.
        
        Args:
            config_dir: Directory for configuration files
        """
        # Initialize configuration
        self.config_manager = ConfigManager(config_dir)
        self.config = self.config_manager.load_config()
        
        # Initialize core modules
        self.screen_reader = ScreenReader(self.config.window_title)
        self.template_matcher = TemplateMatcher()
        self.keyboard_controller = KeyboardController(self.config.window_title)
        self.mouse_controller = MouseController(self.config.window_title)
        self.state_machine = StateMachine()
        
        # Bot state
        self.is_running = False
        self.is_paused = False
        self._main_thread: Optional[threading.Thread] = None
        self._vision_thread: Optional[threading.Thread] = None
        
        # Initialize features
        self.auto_attack = AutoAttack(self.screen_reader, self.keyboard_controller, self.mouse_controller)
        self.auto_loot = AutoLoot(self.screen_reader, self.mouse_controller)
        self.auto_walk = AutoWalk(self.keyboard_controller, self)
        self.enable_auto_loot = True  # Set to True to enable auto-loot by default
        self.enable_auto_walk = True  # Set to True to enable auto-walk by default
        self.auto_walk_paused = False
        
        # Setup state handlers
        self._setup_state_handlers()
        
        # Setup logging
        self.logger = self.config_manager.logger
    
    def _setup_state_handlers(self):
        """Setup handlers for different bot states."""
        self.state_machine.set_state_handler(BotState.IDLE, self._handle_idle_state)
        self.state_machine.set_state_handler(BotState.HEALING, self._handle_healing_state)
        self.state_machine.set_state_handler(BotState.COMBAT, self._handle_combat_state)
        self.state_machine.set_state_handler(BotState.LOOTING, self._handle_looting_state)
        self.state_machine.set_state_handler(BotState.NAVIGATING, self._handle_navigating_state)
        self.state_machine.set_state_handler(BotState.ERROR, self._handle_error_state)
    
    def start(self) -> bool:
        """
        Start the bot.
        
        Returns:
            True if bot started successfully, False otherwise
        """
        if self.is_running:
            self.logger.warning("Bot is already running")
            return True
        
        try:
            # Validate configuration
            if not self.config_manager.validate_config():
                self.logger.error("Configuration validation failed")
                return False
            
            # Find Tibia window
            if not self.screen_reader.find_window():
                self.logger.error("Tibia window not found")
                return False
            
            # Start all modules
            self.screen_reader.start_capture()
            self.keyboard_controller.start()
            self.mouse_controller.start()
            self.state_machine.start()
            
            # Start main bot loop
            self.is_running = True
            self.is_paused = False
            self._main_thread = threading.Thread(target=self._main_loop, daemon=True)
            self._main_thread.start()
            
            # Start vision processing thread
            self._vision_thread = threading.Thread(target=self._vision_loop, daemon=True)
            self._vision_thread.start()
            
            if self.enable_auto_loot:
                threading.Thread(target=self.auto_loot.start, daemon=True).start()
            
            if self.enable_auto_walk:
                threading.Thread(target=self.auto_walk.start, daemon=True).start()
            
            self.logger.info("Bot started successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Error starting bot: {e}")
            return False
    
    def stop(self):
        """Stop the bot."""
        if not self.is_running:
            return
        
        self.logger.info("Stopping bot...")
        self.is_running = False
        
        # Stop all modules
        self.screen_reader.stop_capture()
        self.keyboard_controller.stop()
        self.mouse_controller.stop()
        self.state_machine.stop()
        self.auto_loot.stop()
        self.auto_walk.stop()
        
        # Wait for threads to finish
        if self._main_thread:
            self._main_thread.join(timeout=5.0)
        if self._vision_thread:
            self._vision_thread.join(timeout=5.0)
        
        self.logger.info("Bot stopped")
    
    def pause(self):
        """Pause the bot."""
        if not self.is_running:
            return
        
        self.is_paused = True
        self.logger.info("Bot paused")
    
    def resume(self):
        """Resume the bot."""
        if not self.is_running:
            return
        
        self.is_paused = False
        self.logger.info("Bot resumed")
    
    def start_safe_mode(self) -> bool:
        """
        Start the bot in safe mode (simulation only).
        
        Returns:
            True if bot started successfully, False otherwise
        """
        if self.is_running:
            self.logger.warning("Bot is already running")
            return True
        
        try:
            # Enable safe mode
            self.config_manager.update_safety_config(safe_mode=True, test_mode=True)
            
            # Validate configuration
            if not self.config_manager.validate_config():
                self.logger.error("Configuration validation failed")
                return False
            
            # Start all modules in safe mode
            self.screen_reader.start_capture()
            self.keyboard_controller.start()
            self.mouse_controller.start()
            self.state_machine.start()
            
            # Start main bot loop
            self.is_running = True
            self.is_paused = False
            self._main_thread = threading.Thread(target=self._main_loop, daemon=True)
            self._main_thread.start()
            
            # Start vision processing thread
            self._vision_thread = threading.Thread(target=self._vision_loop, daemon=True)
            self._vision_thread.start()
            
            if self.enable_auto_loot:
                threading.Thread(target=self.auto_loot.start, daemon=True).start()
            
            if self.enable_auto_walk:
                threading.Thread(target=self.auto_walk.start, daemon=True).start()
            
            self.logger.info("Bot started in SAFE MODE - no actual interactions")
            return True
            
        except Exception as e:
            self.logger.error(f"Error starting bot in safe mode: {e}")
            return False
    
    def initialize(self) -> bool:
        """
        Initialize the bot without starting it.
        
        Returns:
            True if initialization successful, False otherwise
        """
        try:
            # Validate configuration
            if not self.config_manager.validate_config():
                self.logger.error("Configuration validation failed")
                return False
            
            # Initialize modules
            self.screen_reader.start_capture()
            self.keyboard_controller.start()
            self.mouse_controller.start()
            self.state_machine.start()
            
            self.logger.info("Bot initialized successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Error initializing bot: {e}")
            return False
    
    def _main_loop(self):
        """Main bot loop."""
        while self.is_running:
            try:
                if not self.is_paused:
                    # Get current state
                    current_state = self.state_machine.get_current_state()
                    
                    # Execute state-specific logic
                    if current_state == BotState.IDLE:
                        self._execute_idle_logic()
                    elif current_state == BotState.HEALING:
                        self._execute_healing_logic()
                    elif current_state == BotState.COMBAT:
                        self._execute_combat_logic()
                    elif current_state == BotState.LOOTING:
                        self._execute_looting_logic()
                    elif current_state == BotState.NAVIGATING:
                        self._execute_navigation_logic()
                    elif current_state == BotState.ERROR:
                        self._execute_error_logic()
                
                time.sleep(0.1)  # 10 FPS
                
            except Exception as e:
                self.logger.error(f"Error in main loop: {e}")
                self.state_machine.set_state_data('error_occurred', True)
                time.sleep(1.0)
    
    def _vision_loop(self):
        """Vision processing loop."""
        while self.is_running:
            try:
                if not self.is_paused:
                    # Get current frame
                    frame = self.screen_reader.get_current_frame()
                    if frame is not None:
                        # Process vision data
                        self._process_vision_data(frame)
                
                time.sleep(0.05)  # 20 FPS for vision processing
                
            except Exception as e:
                self.logger.error(f"Error in vision loop: {e}")
                time.sleep(0.5)
    
    def _process_vision_data(self, frame):
        """
        Process vision data from the current frame.
        
        Args:
            frame: Current screen frame
        """
        try:
            # Detect health and mana
            health_info = self.template_matcher.detect_health_bar(frame)
            mana_info = self.template_matcher.detect_mana_bar(frame)
            
            if health_info:
                health_percent = health_info['percentage']
                self.state_machine.set_state_data('health_percent', health_percent)
                self.state_machine.set_state_data('health_low', health_percent <= self.config.healing.health_potion_percent)
                self.state_machine.set_state_data('health_critical', health_percent <= self.config.healing.ultimate_health_percent)
            
            if mana_info:
                mana_percent = mana_info['percentage']
                self.state_machine.set_state_data('mana_percent', mana_percent)
                self.state_machine.set_state_data('mana_low', mana_percent <= self.config.healing.mana_potion_percent)
            
            # Detect status effects
            status_icons = self.template_matcher.detect_status_icons(frame)
            self.state_machine.set_state_data('status_effects', status_icons)
            
            # Detect equipment
            equipment_slots = self.template_matcher.detect_equipment_slots(frame)
            self.state_machine.set_state_data('equipment', equipment_slots)
            
        except Exception as e:
            self.logger.error(f"Error processing vision data: {e}")
    
    def _execute_idle_logic(self):
        """Execute logic for IDLE state."""
        # Check if we need to heal
        if self.state_machine.get_state_data('health_low', False):
            return  # State machine will handle transition
        
        # Check if we have waypoints to follow
        if self.config.cavebot.auto_navigation:
            # This would be implemented in the cavebot feature
            pass
        
        # Small delay to prevent excessive CPU usage
        time.sleep(0.5)
    
    def _execute_healing_logic(self):
        """Execute logic for HEALING state."""
        try:
            health_percent = self.state_machine.get_state_data('health_percent', 100)
            mana_percent = self.state_machine.get_state_data('mana_percent', 100)
            
            # Use health potion if needed
            if health_percent <= self.config.healing.health_potion_percent:
                if self.keyboard_controller.is_key_ready(self.config.healing.health_potion_key):
                    self.keyboard_controller.press_key(self.config.healing.health_potion_key)
            
            # Use ultimate health potion if critical
            if health_percent <= self.config.healing.ultimate_health_percent:
                if self.keyboard_controller.is_key_ready(self.config.healing.ultimate_health_key):
                    self.keyboard_controller.press_key(self.config.healing.ultimate_health_key)
            
            # Use mana potion if needed
            if mana_percent <= self.config.healing.mana_potion_percent:
                if self.keyboard_controller.is_key_ready(self.config.healing.mana_potion_key):
                    self.keyboard_controller.press_key(self.config.healing.mana_potion_key)
            
            # Use spirit potion if needed
            if mana_percent <= self.config.healing.spirit_potion_percent:
                if self.keyboard_controller.is_key_ready(self.config.healing.spirit_potion_key):
                    self.keyboard_controller.press_key(self.config.healing.spirit_potion_key)
            
            time.sleep(0.2)  # Small delay between healing checks
            
        except Exception as e:
            self.logger.error(f"Error in healing logic: {e}")
    
    def _execute_combat_logic(self):
        """Execute logic for COMBAT state."""
        try:
            if self.config.combat.auto_attack_enabled:
                # This would be implemented in the combat feature
                # For now, just press the attack spell key
                if self.keyboard_controller.is_key_ready(self.config.combat.attack_spell_key):
                    self.keyboard_controller.press_key(self.config.combat.attack_spell_key)
                    time.sleep(self.config.combat.attack_delay)
            
        except Exception as e:
            self.logger.error(f"Error in combat logic: {e}")
    
    def _execute_looting_logic(self):
        """Execute logic for LOOTING state."""
        try:
            if self.config.looter.auto_loot_enabled:
                # This would be implemented in the looter feature
                # For now, just mark looting as finished
                time.sleep(self.config.looter.loot_delay)
                self.state_machine.set_state_data('looting_finished', True)
            
        except Exception as e:
            self.logger.error(f"Error in looting logic: {e}")
    
    def _execute_navigation_logic(self):
        """Execute logic for NAVIGATING state."""
        try:
            if self.config.cavebot.auto_navigation:
                # This would be implemented in the cavebot feature
                # For now, just mark navigation as finished
                time.sleep(self.config.cavebot.waypoint_delay)
                self.state_machine.set_state_data('waypoint_available', False)
            
        except Exception as e:
            self.logger.error(f"Error in navigation logic: {e}")
    
    def _execute_error_logic(self):
        """Execute logic for ERROR state."""
        try:
            # Try to resolve the error
            self.logger.warning("Bot is in ERROR state, attempting to resolve...")
            
            # Clear error flag after some time
            time.sleep(5.0)
            self.state_machine.set_state_data('error_occurred', False)
            
        except Exception as e:
            self.logger.error(f"Error in error handling logic: {e}")
    
    def _handle_idle_state(self):
        """Handler for entering IDLE state."""
        self.logger.info("Entering IDLE state")
    
    def _handle_healing_state(self):
        """Handler for entering HEALING state."""
        self.logger.info("Entering HEALING state")
    
    def _handle_combat_state(self):
        """Handler for entering COMBAT state."""
        self.logger.info("Entering COMBAT state")
    
    def _handle_looting_state(self):
        """Handler for entering LOOTING state."""
        self.logger.info("Entering LOOTING state")
        # Clear looting finished flag
        self.state_machine.set_state_data('looting_finished', False)
    
    def _handle_navigating_state(self):
        """Handler for entering NAVIGATING state."""
        self.logger.info("Entering NAVIGATING state")
        # Clear waypoint available flag
        self.state_machine.set_state_data('waypoint_available', False)
    
    def _handle_error_state(self):
        """Handler for entering ERROR state."""
        self.logger.error("Entering ERROR state")
    
    def get_status(self) -> Dict[str, Any]:
        """
        Get current bot status.
        
        Returns:
            Dictionary with bot status information
        """
        return {
            'is_running': self.is_running,
            'is_paused': self.is_paused,
            'state_info': self.state_machine.get_state_info(),
            'window_found': self.screen_reader.window_info is not None,
            'config': self.config_manager._config_to_dict()
        }
    
    def print_status(self):
        """Print current bot status."""
        status = self.get_status()
        print("Bot Status:")
        print(f"Running: {status['is_running']}")
        print(f"Paused: {status['is_paused']}")
        print(f"Window Found: {status['window_found']}")
        print(f"Current State: {status['state_info']['current_state']}")
        print(f"State Duration: {status['state_info']['state_duration']:.2f} seconds")
    
    def save_config(self):
        """Save current configuration."""
        self.config_manager.save_config()
    
    def load_config(self):
        """Load configuration from file."""
        self.config = self.config_manager.load_config()
        self.logger.info("Configuration reloaded")
    
    def start_auto_attack(self):
        """Start auto-attack feature."""
        if not self.is_running:
            self.logger.warning("Bot must be running to start auto-attack")
            return False
        
        success = self.auto_attack.start()
        if success:
            self.logger.info("Auto-attack started")
            self.state_machine.force_state(BotState.COMBAT)
        else:
            self.logger.error("Failed to start auto-attack")
        
        return success
    
    def stop_auto_attack(self):
        """Stop auto-attack feature."""
        self.auto_attack.stop()
        self.logger.info("Auto-attack stopped")
        self.state_machine.force_state(BotState.IDLE)
    
    def set_attack_key(self, key: str):
        """Set the attack key for auto-attack."""
        self.auto_attack.set_attack_key(key)
    
    def set_next_target_key(self, key: str):
        """Set the next target key for auto-attack."""
        self.auto_attack.set_next_target_key(key)
    
    def get_auto_attack_status(self):
        """Get auto-attack status."""
        return self.auto_attack.get_status()
    
    @property
    def is_attacking(self):
        # Returns True if bot is in COMBAT state
        return self.state_machine.current_state.name == "COMBAT"
    
    def pause_auto_walk(self):
        self.auto_walk_paused = True
        self.logger.info("Auto-walk paused by user")
    def resume_auto_walk(self):
        self.auto_walk_paused = False
        self.logger.info("Auto-walk resumed by user")
    def is_auto_walk_paused(self):
        return self.auto_walk_paused
    
    def __del__(self):
        """Cleanup when the object is destroyed."""
        self.stop() 