"""
Keyboard Controller Module for Tibia Bot

This module provides keyboard input capabilities for controlling
the Tibia client with human-like behavior patterns.
"""

import keyboard
import time
import random
import threading
from typing import Optional, List, Dict, Any
from dataclasses import dataclass
import json


@dataclass
class KeyConfig:
    """Configuration for a keyboard key."""
    key: str
    description: str
    cooldown: float = 0.1  # Minimum time between presses
    last_pressed: float = 0.0


class KeyboardController:
    """
    Keyboard controller for sending inputs to the Tibia client.
    
    This class provides methods to send keyboard inputs with human-like
    timing and behavior patterns to avoid detection.
    """
    
    def __init__(self, window_title: str = "Tibia"):
        """
        Initialize the KeyboardController.
        
        Args:
            window_title: Title of the window to send inputs to
        """
        self.window_title = window_title
        self.key_configs: Dict[str, KeyConfig] = {}
        self.is_active = False
        self._input_thread: Optional[threading.Thread] = None
        self._input_queue: List[Dict[str, Any]] = []
        self._queue_lock = threading.Lock()
        
        # Initialize default key configurations
        self._init_default_keys()
    
    def _init_default_keys(self):
        """Initialize default key configurations for common Tibia actions."""
        default_keys = {
            "F1": KeyConfig("F1", "Health Potion", cooldown=1.0),
            "F2": KeyConfig("F2", "Mana Potion", cooldown=1.0),
            "F3": KeyConfig("F3", "Spirit Potion", cooldown=1.0),
            "F4": KeyConfig("F4", "Ultimate Health Potion", cooldown=2.0),
            "F5": KeyConfig("F5", "Great Mana Potion", cooldown=2.0),
            "F6": KeyConfig("F6", "Great Spirit Potion", cooldown=2.0),
            "F7": KeyConfig("F7", "Supreme Health Potion", cooldown=3.0),
            "F8": KeyConfig("F8", "Supreme Mana Potion", cooldown=3.0),
            "F9": KeyConfig("F9", "Ultimate Spirit Potion", cooldown=3.0),
            "F10": KeyConfig("F10", "Great Health Potion", cooldown=2.0),
            "F11": KeyConfig("F11", "Ultimate Mana Potion", cooldown=3.0),
            "F12": KeyConfig("F12", "Ultimate Spirit Potion", cooldown=3.0),
            "1": KeyConfig("1", "Spell 1", cooldown=0.5),
            "2": KeyConfig("2", "Spell 2", cooldown=0.5),
            "3": KeyConfig("3", "Spell 3", cooldown=0.5),
            "4": KeyConfig("4", "Spell 4", cooldown=0.5),
            "5": KeyConfig("5", "Spell 5", cooldown=0.5),
            "6": KeyConfig("6", "Spell 6", cooldown=0.5),
            "7": KeyConfig("7", "Spell 7", cooldown=0.5),
            "8": KeyConfig("8", "Spell 8", cooldown=0.5),
            "9": KeyConfig("9", "Spell 9", cooldown=0.5),
            "0": KeyConfig("0", "Spell 10", cooldown=0.5),
        }
        
        self.key_configs.update(default_keys)
    
    def add_key_config(self, key: str, description: str, cooldown: float = 0.1):
        """
        Add a new key configuration.
        
        Args:
            key: The key to configure
            description: Description of what the key does
            cooldown: Minimum time between presses in seconds
        """
        self.key_configs[key] = KeyConfig(key, description, cooldown)
    
    def press_key(self, key: str, delay: Optional[float] = None, safe_mode: bool = False) -> bool:
        """
        Press a key with human-like timing.
        
        Args:
            key: The key to press
            delay: Optional delay before pressing (if None, uses random delay)
            safe_mode: If True, only simulate the action without actually pressing
            
        Returns:
            True if key was pressed successfully, False otherwise
        """
        if not self.is_active and not safe_mode:
            return False
        
        # Check if key is configured, if not, add it automatically
        if key not in self.key_configs:
            self.add_key_config(key, f"Key {key}", 0.1)
        
        config = self.key_configs[key]
        current_time = time.time()
        
        # Check cooldown
        if current_time - config.last_pressed < config.cooldown:
            return False
        
        # Add random delay for human-like behavior
        if delay is None:
            delay = random.uniform(0.05, 0.15)
        
        time.sleep(delay)
        
        try:
            if safe_mode:
                # Simulate key press without actually pressing
                print(f"[SAFE MODE] Simulated key press: {key} ({config.description})")
                config.last_pressed = current_time
                return True
            else:
                # Press and release the key
                keyboard.press_and_release(key)
                config.last_pressed = current_time
                
                print(f"Pressed key: {key} ({config.description})")
                return True
            
        except Exception as e:
            print(f"Error pressing key {key}: {e}")
            return False
    
    def press_key_sequence(self, keys: List[str], delays: Optional[List[float]] = None) -> bool:
        """
        Press a sequence of keys with human-like timing.
        
        Args:
            keys: List of keys to press in sequence
            delays: Optional list of delays between key presses
            
        Returns:
            True if all keys were pressed successfully, False otherwise
        """
        if not self.is_active:
            return False
        
        success = True
        
        for i, key in enumerate(keys):
            if not self.press_key(key):
                success = False
                break
            
            # Add delay between keys if specified
            if delays and i < len(delays):
                time.sleep(delays[i])
            else:
                # Default random delay between keys
                time.sleep(random.uniform(0.1, 0.3))
        
        return success
    
    def hold_key(self, key: str, duration: float, safe_mode: bool = False) -> bool:
        """
        Hold a key for a specified duration.
        
        Args:
            key: The key to hold
            duration: How long to hold the key in seconds
            safe_mode: If True, only simulate the action without actually pressing
            
        Returns:
            True if key was held successfully, False otherwise
        """
        if not self.is_active and not safe_mode:
            return False
        
        try:
            if safe_mode:
                # Simulate key hold without actually pressing
                print(f"[SAFE MODE] Simulated key hold: {key} for {duration:.2f} seconds")
                time.sleep(duration)
                return True
            else:
                keyboard.press(key)
                time.sleep(duration)
                keyboard.release(key)
                
                print(f"Held key: {key} for {duration:.2f} seconds")
                return True
            
        except Exception as e:
            print(f"Error holding key {key}: {e}")
            return False
    
    def release_key(self, key: str, safe_mode: bool = False) -> bool:
        """
        Release a key.
        
        Args:
            key: The key to release
            safe_mode: If True, only simulate the action without actually releasing
            
        Returns:
            True if key was released successfully, False otherwise
        """
        if not self.is_active and not safe_mode:
            return False
        
        # Check if key is configured, if not, add it automatically
        if key not in self.key_configs:
            self.add_key_config(key, f"Key {key}", 0.1)
        
        try:
            if safe_mode:
                # Simulate key release without actually releasing
                print(f"[SAFE MODE] Simulated key release: {key}")
                return True
            else:
                keyboard.release(key)
                print(f"Released key: {key}")
                return True
            
        except Exception as e:
            print(f"Error releasing key {key}: {e}")
            return False
    
    def type_text(self, text: str, typing_speed: float = 0.1) -> bool:
        """
        Type text with human-like timing.
        
        Args:
            text: Text to type
            typing_speed: Average time between characters in seconds
            
        Returns:
            True if text was typed successfully, False otherwise
        """
        if not self.is_active:
            return False
        
        try:
            for char in text:
                keyboard.press_and_release(char)
                # Random delay between characters
                time.sleep(random.uniform(typing_speed * 0.5, typing_speed * 1.5))
            
            print(f"Typed text: {text}")
            return True
            
        except Exception as e:
            print(f"Error typing text: {e}")
            return False
    
    def start(self):
        """Start the keyboard controller."""
        if self.is_active:
            print("Keyboard controller already active")
            return
        
        self.is_active = True
        print("Keyboard controller started")
    
    def stop(self):
        """Stop the keyboard controller."""
        self.is_active = False
        print("Keyboard controller stopped")
    
    def load_config(self, config_file: str):
        """
        Load key configurations from a JSON file.
        
        Args:
            config_file: Path to the configuration file
        """
        try:
            with open(config_file, 'r') as f:
                config_data = json.load(f)
            
            for key_data in config_data.get('keys', []):
                key = key_data['key']
                description = key_data.get('description', '')
                cooldown = key_data.get('cooldown', 0.1)
                
                self.add_key_config(key, description, cooldown)
            
            print(f"Loaded keyboard configuration from {config_file}")
            
        except Exception as e:
            print(f"Error loading keyboard configuration: {e}")
    
    def save_config(self, config_file: str):
        """
        Save key configurations to a JSON file.
        
        Args:
            config_file: Path to the configuration file
        """
        try:
            config_data = {
                'keys': [
                    {
                        'key': config.key,
                        'description': config.description,
                        'cooldown': config.cooldown
                    }
                    for config in self.key_configs.values()
                ]
            }
            
            with open(config_file, 'w') as f:
                json.dump(config_data, f, indent=2)
            
            print(f"Saved keyboard configuration to {config_file}")
            
        except Exception as e:
            print(f"Error saving keyboard configuration: {e}")
    
    def get_key_config(self, key: str) -> Optional[KeyConfig]:
        """
        Get configuration for a specific key.
        
        Args:
            key: The key to get configuration for
            
        Returns:
            KeyConfig object or None if key not found
        """
        return self.key_configs.get(key)
    
    def list_configured_keys(self) -> List[str]:
        """
        Get a list of all configured keys.
        
        Returns:
            List of configured key names
        """
        return list(self.key_configs.keys())
    
    def is_key_ready(self, key: str) -> bool:
        """
        Check if a key is ready to be pressed (cooldown expired).
        
        Args:
            key: The key to check
            
        Returns:
            True if key is ready, False otherwise
        """
        if key not in self.key_configs:
            return False
        
        config = self.key_configs[key]
        current_time = time.time()
        return current_time - config.last_pressed >= config.cooldown 