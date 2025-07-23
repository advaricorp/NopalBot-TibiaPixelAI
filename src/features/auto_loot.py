"""
Auto Loot Feature
By Taquito Loco 🎮

This module handles auto-loot functionality for automatic item collection.
"""

import time
import threading
import logging
from typing import List, Dict, Optional
import cv2
import numpy as np

from vision.screen_reader import ScreenReader
from control.mouse_controller import MouseController
from control.keyboard_controller import KeyboardController

logger = logging.getLogger(__name__)

class AutoLoot:
    """
    Auto-loot system for automatic item collection.
    
    Features:
    - Loot corpses automatically
    - Template matching for items
    - Configurable loot list
    - Safe mode support
    """
    
    def __init__(self, screen_reader: ScreenReader, mouse: MouseController, keyboard: KeyboardController):
        """Initialize auto-loot system."""
        self.screen_reader = screen_reader
        self.mouse = mouse
        self.keyboard = keyboard
        self.running = False
        self.loot_thread = None
        
        # Loot settings
        self.loot_key = "ctrl"  # Key to hold while looting
        self.loot_interval = 2.0  # Check for loot every 2 seconds
        self.loot_radius = 50  # Pixels around character to loot
        
        # Items to loot (priority order)
        self.loot_items = [
            {
                "name": "Gold Coin",
                "template": "gold_coin.png",
                "enabled": True,
                "priority": 1
            },
            {
                "name": "Platinum Coin", 
                "template": "platinum_coin.png",
                "enabled": True,
                "priority": 1
            },
            {
                "name": "Crystal Coin",
                "template": "crystal_coin.png", 
                "enabled": True,
                "priority": 1
            },
            {
                "name": "Small Health Potion",
                "template": "small_health.png",
                "enabled": True,
                "priority": 2
            },
            {
                "name": "Small Mana Potion",
                "template": "small_mana.png",
                "enabled": True,
                "priority": 2
            }
        ]
        
        # Loot area (around character)
        self.loot_area = {
            "x": 400,  # Center of screen
            "y": 300,
            "width": 200,
            "height": 200
        }
        
        logger.info("Auto-loot system initialized")
    
    def start(self):
        """Start auto-loot system."""
        if self.running:
            logger.warning("Auto-loot already running")
            return False
        
        self.running = True
        self.loot_thread = threading.Thread(target=self._loot_loop, daemon=True)
        self.loot_thread.start()
        
        logger.info("Auto-loot started")
        return True
    
    def stop(self):
        """Stop auto-loot system."""
        self.running = False
        if self.loot_thread:
            self.loot_thread.join(timeout=1.0)
        
        logger.info("Auto-loot stopped")
    
    def _loot_loop(self):
        """Main loot checking loop."""
        while self.running:
            try:
                # Check for lootable items
                items_found = self._find_loot_items()
                
                if items_found:
                    logger.info(f"Found {len(items_found)} lootable items")
                    self._loot_items(items_found)
                
                time.sleep(self.loot_interval)
                
            except Exception as e:
                logger.error(f"Error in loot loop: {e}")
                time.sleep(1.0)
    
    def _find_loot_items(self) -> List[Dict]:
        """Find lootable items on screen."""
        items_found = []
        
        try:
            # Capture screen
            frame = self.screen_reader.get_current_frame()
            if frame is None:
                return items_found
            
            # Extract loot area
            x, y, w, h = (
                self.loot_area["x"],
                self.loot_area["y"], 
                self.loot_area["width"],
                self.loot_area["height"]
            )
            
            # Ensure coordinates are within frame bounds
            if x + w > frame.shape[1] or y + h > frame.shape[0]:
                logger.warning("Loot area outside screen bounds")
                return items_found
            
            loot_area = frame[y:y+h, x:x+w]
            
            # Check each enabled item
            for item in self.loot_items:
                if not item["enabled"]:
                    continue
                
                # Template matching (simplified - would need actual templates)
                if self._find_item_template(loot_area, item):
                    items_found.append({
                        "name": item["name"],
                        "priority": item["priority"],
                        "x": x + self.loot_area["x"],
                        "y": y + self.loot_area["y"]
                    })
            
            # Sort by priority
            items_found.sort(key=lambda x: x["priority"])
            
        except Exception as e:
            logger.error(f"Error finding loot items: {e}")
        
        return items_found
    
    def _find_item_template(self, image, item: Dict) -> bool:
        """Find item using template matching (simplified)."""
        try:
            # For now, use color detection as placeholder
            # In a real implementation, you'd load actual item templates
            
            # Convert to HSV
            hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
            
            # Look for gold/yellow colors (coins)
            if "coin" in item["name"].lower():
                lower_gold = np.array([20, 100, 100])
                upper_gold = np.array([40, 255, 255])
                mask = cv2.inRange(hsv, lower_gold, upper_gold)
                
                # If enough gold pixels found
                if np.sum(mask > 0) > 100:
                    return True
            
            # Look for red colors (health potions)
            elif "health" in item["name"].lower():
                lower_red1 = np.array([0, 100, 100])
                upper_red1 = np.array([10, 255, 255])
                lower_red2 = np.array([160, 100, 100])
                upper_red2 = np.array([180, 255, 255])
                
                mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
                mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
                mask = mask1 + mask2
                
                if np.sum(mask > 0) > 100:
                    return True
            
            # Look for blue colors (mana potions)
            elif "mana" in item["name"].lower():
                lower_blue = np.array([100, 100, 100])
                upper_blue = np.array([140, 255, 255])
                mask = cv2.inRange(hsv, lower_blue, upper_blue)
                
                if np.sum(mask > 0) > 100:
                    return True
            
        except Exception as e:
            logger.error(f"Error in template matching: {e}")
        
        return False
    
    def _loot_items(self, items: List[Dict]):
        """Loot the found items."""
        try:
            for item in items:
                logger.info(f"Looting {item['name']} at ({item['x']}, {item['y']})")
                
                # Hold loot key
                self.keyboard.press_key(self.loot_key)
                time.sleep(0.1)
                
                # Click on item
                self.mouse.click(item["x"], item["y"])
                time.sleep(0.2)
                
                # Release loot key
                self.keyboard.release_key(self.loot_key)
                time.sleep(0.1)
                
        except Exception as e:
            logger.error(f"Error looting items: {e}")
    
    def add_loot_item(self, name: str, template: str, priority: int = 3, enabled: bool = True):
        """Add a new item to loot list."""
        item = {
            "name": name,
            "template": template,
            "enabled": enabled,
            "priority": priority
        }
        
        self.loot_items.append(item)
        logger.info(f"Added loot item: {name} (priority {priority})")
    
    def remove_loot_item(self, name: str):
        """Remove an item from loot list."""
        self.loot_items = [i for i in self.loot_items if i["name"] != name]
        logger.info(f"Removed loot item: {name}")
    
    def enable_loot_item(self, name: str):
        """Enable looting of an item."""
        for item in self.loot_items:
            if item["name"] == name:
                item["enabled"] = True
                logger.info(f"Enabled loot item: {name}")
                break
    
    def disable_loot_item(self, name: str):
        """Disable looting of an item."""
        for item in self.loot_items:
            if item["name"] == name:
                item["enabled"] = False
                logger.info(f"Disabled loot item: {name}")
                break
    
    def set_loot_area(self, x: int, y: int, width: int, height: int):
        """Set the loot area coordinates."""
        self.loot_area = {"x": x, "y": y, "width": width, "height": height}
        logger.info(f"Set loot area: ({x}, {y}) {width}x{height}")
    
    def get_loot_items(self) -> List[Dict]:
        """Get list of all loot items."""
        return self.loot_items.copy()
    
    def get_status(self) -> Dict:
        """Get current status."""
        enabled_items = [i for i in self.loot_items if i["enabled"]]
        
        return {
            "running": self.running,
            "total_items": len(self.loot_items),
            "enabled_items": len(enabled_items),
            "loot_area": self.loot_area,
            "items": self.loot_items
        } 