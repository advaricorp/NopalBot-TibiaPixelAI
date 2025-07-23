"""
Template Matcher Module for Tibia Bot

This module provides template matching capabilities for detecting
UI elements, status bars, and other game elements in the Tibia client.
"""

import cv2
import numpy as np
from typing import Optional, Tuple, List, Dict, Any
import os
from pathlib import Path
import json


class TemplateMatcher:
    """
    Template matcher for detecting UI elements in the Tibia client.
    
    This class provides methods to detect various game elements using
    template matching techniques with OpenCV.
    """
    
    def __init__(self, templates_dir: str = "resources/templates"):
        """
        Initialize the TemplateMatcher.
        
        Args:
            templates_dir: Directory containing template images
        """
        self.templates_dir = Path(templates_dir)
        self.templates_dir.mkdir(parents=True, exist_ok=True)
        self.templates_cache: Dict[str, np.ndarray] = {}
        self.threshold = 0.8  # Default matching threshold
        
    def load_template(self, template_name: str) -> Optional[np.ndarray]:
        """
        Load a template image from the templates directory.
        
        Args:
            template_name: Name of the template file (with or without extension)
            
        Returns:
            Template image as numpy array, or None if not found
        """
        if template_name in self.templates_cache:
            return self.templates_cache[template_name]
        
        # Try different extensions
        extensions = ['.png', '.jpg', '.jpeg', '.bmp']
        template_path = None
        
        for ext in extensions:
            if template_name.endswith(ext):
                template_path = self.templates_dir / template_name
                break
            else:
                template_path = self.templates_dir / f"{template_name}{ext}"
            
            if template_path.exists():
                break
        
        if template_path and template_path.exists():
            try:
                template = cv2.imread(str(template_path))
                if template is not None:
                    self.templates_cache[template_name] = template
                    return template
            except Exception as e:
                print(f"Error loading template {template_name}: {e}")
        
        return None
    
    def find_template(self, 
                     image: np.ndarray, 
                     template_name: str, 
                     threshold: Optional[float] = None) -> Optional[Tuple[int, int, int, int]]:
        """
        Find a template in the given image.
        
        Args:
            image: Image to search in
            template_name: Name of the template to find
            threshold: Matching threshold (0.0 to 1.0)
            
        Returns:
            Tuple of (x, y, width, height) of the found template, or None if not found
        """
        template = self.load_template(template_name)
        if template is None:
            return None
        
        return self.find_template_in_image(image, template, threshold)
    
    def find_template_in_image(self, 
                              image: np.ndarray, 
                              template: np.ndarray, 
                              threshold: Optional[float] = None) -> Optional[Tuple[int, int, int, int]]:
        """
        Find a template image within another image.
        
        Args:
            image: Image to search in
            template: Template image to find
            threshold: Matching threshold (0.0 to 1.0)
            
        Returns:
            Tuple of (x, y, width, height) of the found template, or None if not found
        """
        if threshold is None:
            threshold = self.threshold
        
        # Perform template matching
        result = cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        
        if max_val >= threshold:
            x, y = max_loc
            w, h = template.shape[1], template.shape[0]
            return (x, y, w, h)
        
        return None
    
    def find_all_templates(self, 
                          image: np.ndarray, 
                          template_name: str, 
                          threshold: Optional[float] = None) -> List[Tuple[int, int, int, int]]:
        """
        Find all occurrences of a template in the given image.
        
        Args:
            image: Image to search in
            template_name: Name of the template to find
            threshold: Matching threshold (0.0 to 1.0)
            
        Returns:
            List of tuples (x, y, width, height) for all found templates
        """
        template = self.load_template(template_name)
        if template is None:
            return []
        
        return self.find_all_templates_in_image(image, template, threshold)
    
    def find_all_templates_in_image(self, 
                                   image: np.ndarray, 
                                   template: np.ndarray, 
                                   threshold: Optional[float] = None) -> List[Tuple[int, int, int, int]]:
        """
        Find all occurrences of a template image within another image.
        
        Args:
            image: Image to search in
            template: Template image to find
            threshold: Matching threshold (0.0 to 1.0)
            
        Returns:
            List of tuples (x, y, width, height) for all found templates
        """
        if threshold is None:
            threshold = self.threshold
        
        # Perform template matching
        result = cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)
        
        # Find all locations where the result exceeds the threshold
        locations = np.where(result >= threshold)
        matches = []
        
        for pt in zip(*locations[::-1]):  # Switch columns and rows
            x, y = pt
            w, h = template.shape[1], template.shape[0]
            matches.append((x, y, w, h))
        
        return matches
    
    def detect_health_bar(self, image: np.ndarray) -> Optional[Dict[str, Any]]:
        """
        Detect the health bar and extract health percentage.
        
        Args:
            image: Image containing the health bar
            
        Returns:
            Dictionary with health information, or None if not found
        """
        # Try to find health bar template
        health_bar_rect = self.find_template(image, "health_bar")
        if health_bar_rect is None:
            return None
        
        x, y, w, h = health_bar_rect
        
        # Extract the health bar region
        health_bar_region = image[y:y+h, x:x+w]
        
        # Calculate health percentage based on green pixels
        # This is a simplified approach - you might need to adjust based on actual UI
        hsv = cv2.cvtColor(health_bar_region, cv2.COLOR_BGR2HSV)
        
        # Define green color range for health
        lower_green = np.array([40, 40, 40])
        upper_green = np.array([80, 255, 255])
        
        # Create mask for green pixels
        green_mask = cv2.inRange(hsv, lower_green, upper_green)
        
        # Calculate percentage of green pixels
        total_pixels = green_mask.shape[0] * green_mask.shape[1]
        green_pixels = cv2.countNonZero(green_mask)
        health_percentage = (green_pixels / total_pixels) * 100 if total_pixels > 0 else 0
        
        return {
            "percentage": int(health_percentage),
            "position": health_bar_rect,
            "region": health_bar_region
        }
    
    def detect_mana_bar(self, image: np.ndarray) -> Optional[Dict[str, Any]]:
        """
        Detect the mana bar and extract mana percentage.
        
        Args:
            image: Image containing the mana bar
            
        Returns:
            Dictionary with mana information, or None if not found
        """
        # Try to find mana bar template
        mana_bar_rect = self.find_template(image, "mana_bar")
        if mana_bar_rect is None:
            return None
        
        x, y, w, h = mana_bar_rect
        
        # Extract the mana bar region
        mana_bar_region = image[y:y+h, x:x+w]
        
        # Calculate mana percentage based on blue pixels
        hsv = cv2.cvtColor(mana_bar_region, cv2.COLOR_BGR2HSV)
        
        # Define blue color range for mana
        lower_blue = np.array([100, 40, 40])
        upper_blue = np.array([140, 255, 255])
        
        # Create mask for blue pixels
        blue_mask = cv2.inRange(hsv, lower_blue, upper_blue)
        
        # Calculate percentage of blue pixels
        total_pixels = blue_mask.shape[0] * blue_mask.shape[1]
        blue_pixels = cv2.countNonZero(blue_mask)
        mana_percentage = (blue_pixels / total_pixels) * 100 if total_pixels > 0 else 0
        
        return {
            "percentage": int(mana_percentage),
            "position": mana_bar_rect,
            "region": mana_bar_region
        }
    
    def detect_status_icons(self, image: np.ndarray) -> Dict[str, bool]:
        """
        Detect various status icons in the game.
        
        Args:
            image: Image to search for status icons
            
        Returns:
            Dictionary mapping status names to boolean values
        """
        status_icons = {
            "poisoned": "poison_icon",
            "burning": "fire_icon", 
            "paralyzed": "paralyze_icon",
            "exhausted": "exhaust_icon",
            "invisible": "invisible_icon",
            "hasted": "haste_icon",
            "shielded": "shield_icon"
        }
        
        detected_status = {}
        
        for status_name, template_name in status_icons.items():
            detected_status[status_name] = self.find_template(image, template_name) is not None
        
        return detected_status
    
    def detect_equipment_slots(self, image: np.ndarray) -> Dict[str, Optional[Tuple[int, int, int, int]]]:
        """
        Detect equipment slots in the character window.
        
        Args:
            image: Image containing the character window
            
        Returns:
            Dictionary mapping equipment slot names to their positions
        """
        equipment_slots = {
            "head": "head_slot",
            "neck": "neck_slot",
            "back": "back_slot",
            "body": "body_slot",
            "right_hand": "right_hand_slot",
            "left_hand": "left_hand_slot",
            "legs": "legs_slot",
            "feet": "feet_slot",
            "finger": "finger_slot",
            "shield": "shield_slot"
        }
        
        detected_slots = {}
        
        for slot_name, template_name in equipment_slots.items():
            detected_slots[slot_name] = self.find_template(image, template_name)
        
        return detected_slots
    
    def set_threshold(self, threshold: float):
        """
        Set the default matching threshold.
        
        Args:
            threshold: Threshold value between 0.0 and 1.0
        """
        if 0.0 <= threshold <= 1.0:
            self.threshold = threshold
        else:
            raise ValueError("Threshold must be between 0.0 and 1.0")
    
    def clear_cache(self):
        """Clear the template cache."""
        self.templates_cache.clear()
    
    def save_template(self, image: np.ndarray, template_name: str):
        """
        Save a template image to the templates directory.
        
        Args:
            image: Image to save as template
            template_name: Name for the template file
        """
        template_path = self.templates_dir / f"{template_name}.png"
        cv2.imwrite(str(template_path), image)
        print(f"Template saved: {template_path}") 