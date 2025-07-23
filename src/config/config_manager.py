"""
Configuration Manager Module for Tibia Bot

This module provides configuration management capabilities for the bot,
allowing it to load and save settings from JSON and YAML files.
"""

import json
import yaml
import os
from pathlib import Path
from typing import Dict, Any, Optional, Union
from dataclasses import dataclass, asdict
import logging


@dataclass
class HealingConfig:
    """Configuration for healing behavior."""
    health_potion_key: str = "F1"
    health_potion_percent: int = 65
    mana_potion_key: str = "F2"
    mana_potion_percent: int = 40
    spirit_potion_key: str = "F3"
    spirit_potion_percent: int = 50
    ultimate_health_key: str = "F4"
    ultimate_health_percent: int = 30
    great_mana_key: str = "F5"
    great_mana_percent: int = 25
    auto_heal_enabled: bool = True


@dataclass
class CavebotConfig:
    """Configuration for cavebot behavior."""
    script_path: str = "scripts/default.json"
    auto_navigation: bool = True
    waypoint_delay: float = 1.0
    max_waypoints: int = 100
    return_to_depot: bool = True
    depot_script: str = "scripts/depot.json"


@dataclass
class LooterConfig:
    """Configuration for looting behavior."""
    auto_loot_enabled: bool = True
    loot_delay: float = 0.5
    max_loot_weight: int = 100
    valuable_items: list = None
    ignore_items: list = None
    
    def __post_init__(self):
        if self.valuable_items is None:
            self.valuable_items = ["gold coin", "crystal coin", "platinum coin"]
        if self.ignore_items is None:
            self.ignore_items = ["rope", "shovel", "torch"]


@dataclass
class CombatConfig:
    """Configuration for combat behavior."""
    auto_attack_enabled: bool = True
    attack_spell_key: str = "1"
    attack_delay: float = 0.5
    target_priority: list = None
    avoid_creatures: list = None
    
    def __post_init__(self):
        if self.target_priority is None:
            self.target_priority = ["dragon", "demon", "orc"]
        if self.avoid_creatures is None:
            self.avoid_creatures = ["dragon lord", "demon lord"]


@dataclass
class SafetyConfig:
    """Configuration for safety and anti-detection features."""
    safe_mode: bool = True  # Prevents actual interactions
    test_mode: bool = True  # Simulates bot behavior
    max_actions_per_minute: int = 30
    random_breaks: bool = True
    break_duration_range: list = None
    emergency_stop_key: str = "F12"
    human_like_behavior: bool = True
    keyboard_delay_range: list = None
    mouse_delay_range: list = None
    
    def __post_init__(self):
        if self.break_duration_range is None:
            self.break_duration_range = [5, 15]
        if self.keyboard_delay_range is None:
            self.keyboard_delay_range = [50, 150]
        if self.mouse_delay_range is None:
            self.mouse_delay_range = [100, 300]


@dataclass
class BotConfig:
    """Main bot configuration."""
    healing: HealingConfig = None
    cavebot: CavebotConfig = None
    looter: LooterConfig = None
    combat: CombatConfig = None
    safety: SafetyConfig = None
    window_title: str = "Tibia"
    debug_mode: bool = False
    log_level: str = "INFO"
    
    def __post_init__(self):
        if self.healing is None:
            self.healing = HealingConfig()
        if self.cavebot is None:
            self.cavebot = CavebotConfig()
        if self.looter is None:
            self.looter = LooterConfig()
        if self.combat is None:
            self.combat = CombatConfig()
        if self.safety is None:
            self.safety = SafetyConfig()


class ConfigManager:
    """
    Configuration manager for the Tibia bot.
    
    This class provides methods to load and save bot configuration
    from JSON and YAML files with validation and defaults.
    """
    
    def __init__(self, config_dir: str = "config"):
        """
        Initialize the ConfigManager.
        
        Args:
            config_dir: Directory to store configuration files
        """
        self.config_dir = Path(config_dir)
        self.config_dir.mkdir(parents=True, exist_ok=True)
        
        self.config = BotConfig()
        self.config_file = self.config_dir / "bot_config.json"
        
        # Setup logging
        self._setup_logging()
    
    def _setup_logging(self):
        """Setup logging configuration."""
        log_level = getattr(logging, self.config.log_level.upper(), logging.INFO)
        logging.basicConfig(
            level=log_level,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(self.config_dir / "bot.log"),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def load_config(self, filename: Optional[str] = None) -> BotConfig:
        """
        Load configuration from file.
        
        Args:
            filename: Configuration file path (if None, uses default)
            
        Returns:
            Loaded configuration object
        """
        if filename is None:
            filename = self.config_file
        
        file_path = Path(filename)
        
        if not file_path.exists():
            self.logger.warning(f"Configuration file {filename} not found, using defaults")
            return self.config
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                if file_path.suffix.lower() in ['.yaml', '.yml']:
                    data = yaml.safe_load(f)
                else:
                    data = json.load(f)
            
            # Update configuration with loaded data
            self._update_config_from_dict(data)
            
            self.logger.info(f"Configuration loaded from {filename}")
            return self.config
            
        except Exception as e:
            self.logger.error(f"Error loading configuration from {filename}: {e}")
            return self.config
    
    def save_config(self, filename: Optional[str] = None):
        """
        Save current configuration to file.
        
        Args:
            filename: Configuration file path (if None, uses default)
        """
        if filename is None:
            filename = self.config_file
        
        file_path = Path(filename)
        
        try:
            # Convert config to dictionary
            config_dict = self._config_to_dict()
            
            with open(file_path, 'w', encoding='utf-8') as f:
                if file_path.suffix.lower() in ['.yaml', '.yml']:
                    yaml.dump(config_dict, f, default_flow_style=False, indent=2)
                else:
                    json.dump(config_dict, f, indent=2, ensure_ascii=False)
            
            self.logger.info(f"Configuration saved to {filename}")
            
        except Exception as e:
            self.logger.error(f"Error saving configuration to {filename}: {e}")
    
    def _config_to_dict(self) -> Dict[str, Any]:
        """
        Convert configuration object to dictionary.
        
        Returns:
            Configuration as dictionary
        """
        config_dict = {}
        
        # Convert each config section
        config_dict['healing'] = asdict(self.config.healing)
        config_dict['cavebot'] = asdict(self.config.cavebot)
        config_dict['looter'] = asdict(self.config.looter)
        config_dict['combat'] = asdict(self.config.combat)
        
        # Add main config fields
        config_dict['window_title'] = self.config.window_title
        config_dict['debug_mode'] = self.config.debug_mode
        config_dict['log_level'] = self.config.log_level
        
        # Add safety config
        config_dict['safety'] = asdict(self.config.safety)
        
        return config_dict
    
    def _update_config_from_dict(self, data: Dict[str, Any]):
        """
        Update configuration from dictionary data.
        
        Args:
            data: Configuration data as dictionary
        """
        # Update healing config
        if 'healing' in data:
            healing_data = data['healing']
            for key, value in healing_data.items():
                if hasattr(self.config.healing, key):
                    setattr(self.config.healing, key, value)
        
        # Update cavebot config
        if 'cavebot' in data:
            cavebot_data = data['cavebot']
            for key, value in cavebot_data.items():
                if hasattr(self.config.cavebot, key):
                    setattr(self.config.cavebot, key, value)
        
        # Update looter config
        if 'looter' in data:
            looter_data = data['looter']
            for key, value in looter_data.items():
                if hasattr(self.config.looter, key):
                    setattr(self.config.looter, key, value)
        
        # Update combat config
        if 'combat' in data:
            combat_data = data['combat']
            for key, value in combat_data.items():
                if hasattr(self.config.combat, key):
                    setattr(self.config.combat, key, value)
        
        # Update safety config
        if 'safety' in data:
            safety_data = data['safety']
            for key, value in safety_data.items():
                if hasattr(self.config.safety, key):
                    setattr(self.config.safety, key, value)
        
        # Update main config
        if 'window_title' in data:
            self.config.window_title = data['window_title']
        if 'debug_mode' in data:
            self.config.debug_mode = data['debug_mode']
        if 'log_level' in data:
            self.config.log_level = data['log_level']
            self._setup_logging()  # Re-setup logging with new level
    
    def get_healing_config(self) -> HealingConfig:
        """
        Get healing configuration.
        
        Returns:
            Healing configuration object
        """
        return self.config.healing
    
    def get_cavebot_config(self) -> CavebotConfig:
        """
        Get cavebot configuration.
        
        Returns:
            Cavebot configuration object
        """
        return self.config.cavebot
    
    def get_looter_config(self) -> LooterConfig:
        """
        Get looter configuration.
        
        Returns:
            Looter configuration object
        """
        return self.config.looter
    
    def get_combat_config(self) -> CombatConfig:
        """
        Get combat configuration.
        
        Returns:
            Combat configuration object
        """
        return self.config.combat
    
    def get_safety_config(self) -> SafetyConfig:
        """
        Get safety configuration.
        
        Returns:
            Safety configuration object
        """
        return self.config.safety
    
    def is_safe_mode(self) -> bool:
        """
        Check if bot is in safe mode (no actual interactions).
        
        Returns:
            True if safe mode is enabled
        """
        return self.config.safety.safe_mode
    
    def is_test_mode(self) -> bool:
        """
        Check if bot is in test mode (simulation only).
        
        Returns:
            True if test mode is enabled
        """
        return self.config.safety.test_mode
    
    def update_healing_config(self, **kwargs):
        """
        Update healing configuration.
        
        Args:
            **kwargs: Healing configuration parameters to update
        """
        for key, value in kwargs.items():
            if hasattr(self.config.healing, key):
                setattr(self.config.healing, key, value)
                self.logger.info(f"Updated healing config: {key} = {value}")
    
    def update_cavebot_config(self, **kwargs):
        """
        Update cavebot configuration.
        
        Args:
            **kwargs: Cavebot configuration parameters to update
        """
        for key, value in kwargs.items():
            if hasattr(self.config.cavebot, key):
                setattr(self.config.cavebot, key, value)
                self.logger.info(f"Updated cavebot config: {key} = {value}")
    
    def update_looter_config(self, **kwargs):
        """
        Update looter configuration.
        
        Args:
            **kwargs: Looter configuration parameters to update
        """
        for key, value in kwargs.items():
            if hasattr(self.config.looter, key):
                setattr(self.config.looter, key, value)
                self.logger.info(f"Updated looter config: {key} = {value}")
    
    def update_combat_config(self, **kwargs):
        """
        Update combat configuration.
        
        Args:
            **kwargs: Combat configuration parameters to update
        """
        for key, value in kwargs.items():
            if hasattr(self.config.combat, key):
                setattr(self.config.combat, key, value)
                self.logger.info(f"Updated combat config: {key} = {value}")
    
    def update_safety_config(self, **kwargs):
        """
        Update safety configuration.
        
        Args:
            **kwargs: Safety configuration parameters to update
        """
        for key, value in kwargs.items():
            if hasattr(self.config.safety, key):
                setattr(self.config.safety, key, value)
                self.logger.info(f"Updated safety config: {key} = {value}")
    
    def create_default_config(self):
        """Create a default configuration file."""
        self.save_config()
        self.logger.info("Default configuration file created")
    
    def validate_config(self) -> bool:
        """
        Validate the current configuration.
        
        Returns:
            True if configuration is valid, False otherwise
        """
        try:
            # Validate healing config
            if not (0 <= self.config.healing.health_potion_percent <= 100):
                self.logger.error("Health potion percent must be between 0 and 100")
                return False
            
            if not (0 <= self.config.healing.mana_potion_percent <= 100):
                self.logger.error("Mana potion percent must be between 0 and 100")
                return False
            
            # Validate cavebot config
            if self.config.cavebot.waypoint_delay < 0:
                self.logger.error("Waypoint delay must be positive")
                return False
            
            if self.config.cavebot.max_waypoints < 1:
                self.logger.error("Max waypoints must be at least 1")
                return False
            
            # Validate looter config
            if self.config.looter.loot_delay < 0:
                self.logger.error("Loot delay must be positive")
                return False
            
            if self.config.looter.max_loot_weight < 0:
                self.logger.error("Max loot weight must be positive")
                return False
            
            # Validate combat config
            if self.config.combat.attack_delay < 0:
                self.logger.error("Attack delay must be positive")
                return False
            
            self.logger.info("Configuration validation passed")
            return True
            
        except Exception as e:
            self.logger.error(f"Configuration validation failed: {e}")
            return False
    
    def print_config(self):
        """Print current configuration."""
        config_dict = self._config_to_dict()
        print("Current Bot Configuration:")
        print(json.dumps(config_dict, indent=2, ensure_ascii=False))
    
    def reset_to_defaults(self):
        """Reset configuration to default values."""
        self.config = BotConfig()
        self.logger.info("Configuration reset to defaults") 