"""
Auto Spell Feature
By Taquito Loco 🎮

This module handles auto-spell functionality for automatic spell casting.
"""

import time
import threading
import logging
from typing import List, Dict, Optional

from control.keyboard_controller import KeyboardController
from core.state_machine import BotState

logger = logging.getLogger(__name__)

class AutoSpell:
    """
    Auto-spell system for automatic spell casting.
    
    Features:
    - Cast spells at regular intervals
    - Multiple spell slots
    - Configurable intervals
    - Safe mode support
    """
    
    def __init__(self, keyboard: KeyboardController):
        """Initialize auto-spell system."""
        self.keyboard = keyboard
        self.running = False
        self.spell_thread = None
        
        # Spell settings
        self.spells = [
            {
                "name": "Exura",
                "key": "f1",
                "interval": 5.0,  # Cast every 5 seconds
                "enabled": True
            },
            {
                "name": "Exura Gran",
                "key": "f2", 
                "interval": 10.0,  # Cast every 10 seconds
                "enabled": True
            },
            {
                "name": "Exura Vita",
                "key": "f3",
                "interval": 15.0,  # Cast every 15 seconds
                "enabled": True
            },
            {
                "name": "Utani Hur",
                "key": "f4",
                "interval": 20.0,  # Cast every 20 seconds
                "enabled": False
            }
        ]
        
        # Timing tracking
        self.last_cast_times = {}
        for spell in self.spells:
            self.last_cast_times[spell["name"]] = 0
        
        logger.info("Auto-spell system initialized")
    
    def start(self):
        """Start auto-spell system."""
        if self.running:
            logger.warning("Auto-spell already running")
            return False
        
        self.running = True
        self.spell_thread = threading.Thread(target=self._spell_loop, daemon=True)
        self.spell_thread.start()
        
        logger.info("Auto-spell started")
        return True
    
    def stop(self):
        """Stop auto-spell system."""
        self.running = False
        if self.spell_thread:
            self.spell_thread.join(timeout=1.0)
        
        logger.info("Auto-spell stopped")
    
    def _spell_loop(self):
        """Main spell casting loop."""
        while self.running:
            try:
                current_time = time.time()
                
                # Check each spell
                for spell in self.spells:
                    if not spell["enabled"]:
                        continue
                    
                    last_cast = self.last_cast_times[spell["name"]]
                    if current_time - last_cast >= spell["interval"]:
                        self._cast_spell(spell)
                        self.last_cast_times[spell["name"]] = current_time
                
                time.sleep(0.5)  # Check every 0.5 seconds
                
            except Exception as e:
                logger.error(f"Error in spell loop: {e}")
                time.sleep(1.0)
    
    def _cast_spell(self, spell: Dict):
        """Cast a specific spell."""
        try:
            logger.info(f"Casting spell: {spell['name']} ({spell['key']})")
            
            # Press spell key
            self.keyboard.press_key(spell["key"])
            time.sleep(0.1)
            self.keyboard.release_key(spell["key"])
            
        except Exception as e:
            logger.error(f"Error casting spell {spell['name']}: {e}")
    
    def add_spell(self, name: str, key: str, interval: float, enabled: bool = True):
        """Add a new spell to the list."""
        spell = {
            "name": name,
            "key": key,
            "interval": interval,
            "enabled": enabled
        }
        
        self.spells.append(spell)
        self.last_cast_times[name] = 0
        
        logger.info(f"Added spell: {name} ({key}) every {interval}s")
    
    def remove_spell(self, name: str):
        """Remove a spell from the list."""
        self.spells = [s for s in self.spells if s["name"] != name]
        if name in self.last_cast_times:
            del self.last_cast_times[name]
        
        logger.info(f"Removed spell: {name}")
    
    def enable_spell(self, name: str):
        """Enable a spell."""
        for spell in self.spells:
            if spell["name"] == name:
                spell["enabled"] = True
                logger.info(f"Enabled spell: {name}")
                break
    
    def disable_spell(self, name: str):
        """Disable a spell."""
        for spell in self.spells:
            if spell["name"] == name:
                spell["enabled"] = False
                logger.info(f"Disabled spell: {name}")
                break
    
    def set_spell_interval(self, name: str, interval: float):
        """Set the interval for a spell."""
        for spell in self.spells:
            if spell["name"] == name:
                spell["interval"] = interval
                logger.info(f"Set {name} interval to {interval}s")
                break
    
    def get_spells(self) -> List[Dict]:
        """Get list of all spells."""
        return self.spells.copy()
    
    def get_status(self) -> Dict:
        """Get current status."""
        enabled_spells = [s for s in self.spells if s["enabled"]]
        
        return {
            "running": self.running,
            "total_spells": len(self.spells),
            "enabled_spells": len(enabled_spells),
            "spells": self.spells
        } 