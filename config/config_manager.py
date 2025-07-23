"""
Configuration Manager for PBT Bot
Handles all bot settings and configuration
By Taquito Loco 🎮
"""

import json
import os
from typing import Dict, Any, List
from pathlib import Path

class ConfigManager:
    """Manages bot configuration and settings"""
    
    def __init__(self, config_file: str = "config/bot_config.json"):
        self.config_file = config_file
        self.config = self._load_config()
        self._ensure_config_directory()
    
    def _ensure_config_directory(self):
        """Ensure config directory exists"""
        config_dir = Path(self.config_file).parent
        config_dir.mkdir(parents=True, exist_ok=True)
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from file"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                return self._get_default_config()
        except Exception as e:
            print(f"Error loading config: {e}")
            return self._get_default_config()
    
    def _get_default_config(self) -> Dict[str, Any]:
        """Get default configuration"""
        return {
            "bot_settings": {
                "profession": "knight",
                "auto_attack": True,
                "auto_movement": True,
                "auto_loot": True,
                "spells_enabled": True,
                "emergency_spells": True,
                "movement_type": "patrol",
                "attack_range": "melee",
                "loot_priority": "gold_only"
            },
            "hotkeys": {
                "attack": "space",
                "loot": "f4",
                "movement_up": "w",
                "movement_down": "s",
                "movement_left": "a",
                "movement_right": "d",
                "emergency_kill": "f12",
                "pause": "f1",
                "stop": "f2"
            },
            "spells": {
                "knight": {
                    "healing": ["exura", "exura gran", "exura ico"],
                    "support": ["utani hur", "utani gran hur"],
                    "emergency": ["exura vita", "exura gran ico"]
                },
                "paladin": {
                    "healing": ["exura", "exura san"],
                    "support": ["utani hur", "utani gran hur"],
                    "emergency": ["exura vita", "exura gran san"]
                },
                "sorcerer": {
                    "healing": ["exura", "exura gran"],
                    "support": ["utani hur", "utani gran hur"],
                    "emergency": ["exura vita", "exura gran"]
                },
                "druid": {
                    "healing": ["exura", "exura gran"],
                    "support": ["utani hur", "utani gran hur"],
                    "emergency": ["exura vita", "exura gran"]
                },
                "mage": {
                    "healing": ["exura", "exura gran"],
                    "support": ["utani hur", "utani gran hur"],
                    "emergency": ["exura vita", "exura gran"]
                }
            },
            "movement_patterns": {
                "patrol": ["w", "a", "s", "d"],
                "stair_up": ["w"],
                "stair_down": ["s"],
                "random": ["w", "a", "s", "d"]
            },
            "thresholds": {
                "health_low": 30,
                "health_medium": 50,
                "mana_low": 20,
                "mana_medium": 40
            },
            "timing": {
                "attack_cooldown": 1.0,
                "movement_cooldown": 0.5,
                "loot_cooldown": 2.0,
                "spell_cooldown": 3.0
            }
        }
    
    def save_config(self):
        """Save configuration to file"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error saving config: {e}")
            return False
    
    def get_setting(self, section: str, key: str, default: Any = None) -> Any:
        """Get a specific setting"""
        try:
            return self.config[section][key]
        except KeyError:
            return default
    
    def set_setting(self, section: str, key: str, value: Any) -> bool:
        """Set a specific setting"""
        try:
            if section not in self.config:
                self.config[section] = {}
            self.config[section][key] = value
            return self.save_config()
        except Exception as e:
            print(f"Error setting config: {e}")
            return False
    
    def get_profession_spells(self, profession: str = None) -> Dict[str, List[str]]:
        """Get spells for a specific profession"""
        if profession is None:
            profession = self.get_setting("bot_settings", "profession", "knight")
        return self.config["spells"].get(profession, {})
    
    def get_hotkey(self, action: str) -> str:
        """Get hotkey for a specific action"""
        return self.get_setting("hotkeys", action, "")
    
    def get_movement_pattern(self, pattern_type: str = None) -> List[str]:
        """Get movement pattern"""
        if pattern_type is None:
            pattern_type = self.get_setting("bot_settings", "movement_type", "patrol")
        return self.config["movement_patterns"].get(pattern_type, ["w", "a", "s", "d"])
    
    def get_threshold(self, threshold_type: str) -> int:
        """Get threshold value"""
        return self.get_setting("thresholds", threshold_type, 50)
    
    def get_timing(self, timing_type: str) -> float:
        """Get timing value"""
        return self.get_setting("timing", timing_type, 1.0)
    
    def is_feature_enabled(self, feature: str) -> bool:
        """Check if a feature is enabled"""
        return self.get_setting("bot_settings", feature, False)
    
    def get_all_professions(self) -> List[str]:
        """Get all available professions"""
        return list(self.config["spells"].keys())
    
    def get_all_spell_types(self) -> List[str]:
        """Get all spell types"""
        return ["healing", "support", "emergency"] 