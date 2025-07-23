"""
Auto Attack Feature for Classic Controls
By Taquito Loco 🎮

This module handles auto-attack functionality for Tibia classic controls.
It will attack the current target and automatically click the next target in the battle list.
"""

import time
import threading
import logging
from typing import Optional, Tuple
import cv2
import numpy as np

from vision.screen_reader import ScreenReader
from control.keyboard_controller import KeyboardController
from control.mouse_controller import MouseController
from core.state_machine import BotState

logger = logging.getLogger(__name__)

class AutoAttack:
    """
    Auto-attack system for classic controls.
    
    Features:
    - Attack current target
    - Click next target in battle list
    - Handle classic controls
    - Safe mode support
    """
    
    def __init__(self, screen_reader: ScreenReader, keyboard: KeyboardController, mouse: MouseController):
        """Initialize auto-attack system."""
        self.screen_reader = screen_reader
        self.keyboard = keyboard
        self.mouse = mouse
        self.running = False
        self.attack_thread = None
        
        # Attack settings
        self.attack_key = "space"  # Default attack key for classic controls (space bar)
        self.next_target_key = "u"  # Next target key
        self.attack_interval = 1.0  # Seconds between attacks
        self.target_check_interval = 0.5  # Check for new targets
        
        # Battle list coordinates (approximate - will be calibrated)
        self.battle_list_region = {
            "x": 1600,  # Right side of screen
            "y": 200,   # Below top bar
            "width": 200,
            "height": 400
        }
        
        # Target detection
        self.current_target = None
        self.targets_found = []
        
        logger.info("Auto-attack system initialized")
    
    def start(self):
        """Start auto-attack system."""
        if self.running:
            logger.warning("Auto-attack already running")
            return False
        
        self.running = True
        self.attack_thread = threading.Thread(target=self._attack_loop, daemon=True)
        self.attack_thread.start()
        
        logger.info("Auto-attack started")
        return True
    
    def stop(self):
        """Stop auto-attack system."""
        self.running = False
        if self.attack_thread:
            self.attack_thread.join(timeout=1.0)
        
        logger.info("Auto-attack stopped")
    
    def _attack_loop(self):
        """Main attack loop."""
        while self.running:
            try:
                # Check for targets
                self._find_targets()
                
                # Attack current target
                if self.current_target:
                    self._attack_current_target()
                
                # Look for next target
                self._find_next_target()
                
                time.sleep(self.target_check_interval)
                
            except Exception as e:
                logger.error(f"Error in attack loop: {e}")
                time.sleep(1.0)
    
    def _find_targets(self):
        """Find targets in battle list."""
        try:
            # Capture battle list area
            frame = self.screen_reader.capture_single_frame()
            if frame is None:
                return
            
            # Extract battle list region
            x, y, w, h = (
                self.battle_list_region["x"],
                self.battle_list_region["y"],
                self.battle_list_region["width"],
                self.battle_list_region["height"]
            )
            
            # Ensure coordinates are within frame bounds
            if x + w > frame.shape[1] or y + h > frame.shape[0]:
                logger.warning("Battle list region outside screen bounds")
                return
            
            battle_list = frame[y:y+h, x:x+w]
            
            # Find targets (red health bars or creature names)
            targets = self._detect_targets(battle_list)
            
            if targets:
                self.targets_found = targets
                logger.debug(f"Found {len(targets)} targets")
            
        except Exception as e:
            logger.error(f"Error finding targets: {e}")
    
    def _detect_targets(self, battle_list_image):
        """Detect targets in battle list image."""
        targets = []
        
        try:
            # Convert to HSV for better color detection
            hsv = cv2.cvtColor(battle_list_image, cv2.COLOR_BGR2HSV)
            
            # Look for red health bars (low health)
            lower_red1 = np.array([0, 100, 100])
            upper_red1 = np.array([10, 255, 255])
            lower_red2 = np.array([160, 100, 100])
            upper_red2 = np.array([180, 255, 255])
            
            mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
            mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
            red_mask = mask1 + mask2
            
            # Find contours of red areas
            contours, _ = cv2.findContours(red_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            for contour in contours:
                if cv2.contourArea(contour) > 50:  # Minimum size
                    x, y, w, h = cv2.boundingRect(contour)
                    targets.append({
                        "x": x + self.battle_list_region["x"],
                        "y": y + self.battle_list_region["y"],
                        "width": w,
                        "height": h,
                        "area": cv2.contourArea(contour)
                    })
            
            # Sort by area (larger = more important target)
            targets.sort(key=lambda t: t["area"], reverse=True)
            
        except Exception as e:
            logger.error(f"Error detecting targets: {e}")
        
        return targets
    
    def _attack_current_target(self):
        """Attack the current target."""
        try:
            # Press attack key
            self.keyboard.press_key(self.attack_key)
            time.sleep(0.1)
            self.keyboard.release_key(self.attack_key)
            
            logger.debug(f"Attacked with key: {self.attack_key}")
            
            # Wait for attack animation
            time.sleep(self.attack_interval)
            
        except Exception as e:
            logger.error(f"Error attacking current target: {e}")
    
    def _find_next_target(self):
        """Find and click next target."""
        try:
            if not self.targets_found:
                # No targets found, try next target key
                self.keyboard.press_key(self.next_target_key)
                time.sleep(0.1)
                self.keyboard.release_key(self.next_target_key)
                logger.debug("No targets found, pressed next target key")
                return
            
            # Click on the first target in battle list
            target = self.targets_found[0]
            click_x = target["x"] + target["width"] // 2
            click_y = target["y"] + target["height"] // 2
            
            # Click on target
            self.mouse.click(click_x, click_y)
            logger.debug(f"Clicked target at ({click_x}, {click_y})")
            
            # Update current target
            self.current_target = target
            
            time.sleep(0.5)  # Wait for target selection
            
        except Exception as e:
            logger.error(f"Error finding next target: {e}")
    
    def set_attack_key(self, key: str):
        """Set the attack key."""
        self.attack_key = key
        logger.info(f"Attack key set to: {key}")
    
    def set_next_target_key(self, key: str):
        """Set the next target key."""
        self.next_target_key = key
        logger.info(f"Next target key set to: {key}")
    
    def set_attack_interval(self, interval: float):
        """Set attack interval in seconds."""
        self.attack_interval = interval
        logger.info(f"Attack interval set to: {interval}s")
    
    def calibrate_battle_list(self, x: int, y: int, width: int, height: int):
        """Calibrate battle list position."""
        self.battle_list_region = {
            "x": x,
            "y": y,
            "width": width,
            "height": height
        }
        logger.info(f"Battle list calibrated: ({x}, {y}, {width}, {height})")
    
    def get_status(self):
        """Get auto-attack status."""
        return {
            "running": self.running,
            "current_target": self.current_target,
            "targets_found": len(self.targets_found),
            "attack_key": self.attack_key,
            "next_target_key": self.next_target_key,
            "attack_interval": self.attack_interval
        } 