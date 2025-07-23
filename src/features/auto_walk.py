"""
Auto Walk Feature
By Taquito Loco 🎮

This module handles auto-walk functionality for automatic movement.
"""

import time
import threading
import logging
import random
from typing import List, Dict, Optional

from control.keyboard_controller import KeyboardController

logger = logging.getLogger(__name__)

class AutoWalk:
    """
    Auto-walk system for automatic movement.
    
    Features:
    - Patrol movement patterns
    - Random walking
    - Circle movement
    - Configurable patterns
    - Safe mode support
    """
    
    def __init__(self, keyboard: KeyboardController):
        """Initialize auto-walk system."""
        self.keyboard = keyboard
        self.running = False
        self.walk_thread = None
        
        # Movement settings
        self.walk_interval = 2.0  # Seconds between movements
        self.movement_duration = 0.5  # How long to hold movement keys
        
        # Movement patterns
        self.patterns = {
            "patrol": [
                {"key": "w", "duration": 1.0},  # Forward
                {"key": "a", "duration": 0.5},  # Left
                {"key": "w", "duration": 1.0},  # Forward
                {"key": "d", "duration": 0.5},  # Right
                {"key": "s", "duration": 1.0},  # Back
                {"key": "d", "duration": 0.5},  # Right
                {"key": "s", "duration": 1.0},  # Back
                {"key": "a", "duration": 0.5},  # Left
            ],
            "circle": [
                {"key": "w", "duration": 0.5},  # Forward
                {"key": "d", "duration": 0.5},  # Right
                {"key": "s", "duration": 0.5},  # Back
                {"key": "a", "duration": 0.5},  # Left
            ],
            "random": [
                {"key": "w", "duration": 0.5},
                {"key": "a", "duration": 0.5},
                {"key": "s", "duration": 0.5},
                {"key": "d", "duration": 0.5},
                {"key": "w", "duration": 1.0},
                {"key": "s", "duration": 1.0},
            ]
        }
        
        # Current settings
        self.current_pattern = "patrol"
        self.pattern_index = 0
        self.enabled = True
        
        logger.info("Auto-walk system initialized")
    
    def start(self):
        """Start auto-walk system."""
        if self.running:
            logger.warning("Auto-walk already running")
            return False
        
        self.running = True
        self.walk_thread = threading.Thread(target=self._walk_loop, daemon=True)
        self.walk_thread.start()
        
        logger.info("Auto-walk started")
        return True
    
    def stop(self):
        """Stop auto-walk system."""
        self.running = False
        if self.walk_thread:
            self.walk_thread.join(timeout=1.0)
        
        logger.info("Auto-walk stopped")
    
    def _walk_loop(self):
        """Main walking loop."""
        while self.running:
            try:
                if self.enabled:
                    self._execute_movement()
                
                time.sleep(self.walk_interval)
                
            except Exception as e:
                logger.error(f"Error in walk loop: {e}")
                time.sleep(1.0)
    
    def _execute_movement(self):
        """Execute the current movement pattern."""
        try:
            pattern = self.patterns[self.current_pattern]
            
            if self.current_pattern == "random":
                # Random movement
                movement = random.choice(pattern)
            else:
                # Sequential movement
                movement = pattern[self.pattern_index]
                self.pattern_index = (self.pattern_index + 1) % len(pattern)
            
            # Execute movement
            key = movement["key"]
            duration = movement["duration"]
            
            logger.info(f"Moving {key.upper()} for {duration}s")
            
            # Press movement key
            self.keyboard.press_key(key)
            time.sleep(duration)
            self.keyboard.release_key(key)
            
        except Exception as e:
            logger.error(f"Error executing movement: {e}")
    
    def set_pattern(self, pattern_name: str):
        """Set the movement pattern."""
        if pattern_name in self.patterns:
            self.current_pattern = pattern_name
            self.pattern_index = 0
            logger.info(f"Set movement pattern: {pattern_name}")
        else:
            logger.error(f"Unknown pattern: {pattern_name}")
    
    def add_pattern(self, name: str, movements: List[Dict]):
        """Add a new movement pattern."""
        self.patterns[name] = movements
        logger.info(f"Added movement pattern: {name}")
    
    def enable(self):
        """Enable auto-walk."""
        self.enabled = True
        logger.info("Auto-walk enabled")
    
    def disable(self):
        """Disable auto-walk."""
        self.enabled = False
        logger.info("Auto-walk disabled")
    
    def set_walk_interval(self, interval: float):
        """Set the walk interval."""
        self.walk_interval = interval
        logger.info(f"Set walk interval to {interval}s")
    
    def get_patterns(self) -> List[str]:
        """Get list of available patterns."""
        return list(self.patterns.keys())
    
    def get_status(self) -> Dict:
        """Get current status."""
        return {
            "running": self.running,
            "enabled": self.enabled,
            "current_pattern": self.current_pattern,
            "pattern_index": self.pattern_index,
            "walk_interval": self.walk_interval,
            "available_patterns": list(self.patterns.keys())
        } 