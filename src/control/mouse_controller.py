"""
Mouse Controller Module for Tibia Bot

This module provides mouse input capabilities for controlling
the Tibia client with human-like curved movements and behavior patterns.
"""

import pyautogui
import mouse
import time
import random
import math
import numpy as np
from typing import Optional, Tuple, List, Dict, Any
from dataclasses import dataclass
import json


@dataclass
class MouseConfig:
    """Configuration for mouse behavior."""
    movement_speed: float = 0.5  # Seconds for movement
    click_delay: float = 0.1  # Delay between click and release
    human_like: bool = True  # Enable human-like behavior
    curve_intensity: float = 0.3  # Intensity of curved movements (0.0 to 1.0)


class MouseController:
    """
    Mouse controller for sending inputs to the Tibia client.
    
    This class provides methods to send mouse inputs with human-like
    curved movements and behavior patterns to avoid detection.
    """
    
    def __init__(self, window_title: str = "Tibia"):
        """
        Initialize the MouseController.
        
        Args:
            window_title: Title of the window to send inputs to
        """
        self.window_title = window_title
        self.config = MouseConfig()
        self.is_active = False
        self._last_position: Optional[Tuple[int, int]] = None
        
        # Configure PyAutoGUI
        pyautogui.FAILSAFE = True
        pyautogui.PAUSE = 0.1
    
    def set_config(self, config: MouseConfig):
        """
        Set mouse configuration.
        
        Args:
            config: Mouse configuration object
        """
        self.config = config
    
    def get_current_position(self) -> Tuple[int, int]:
        """
        Get current mouse position.
        
        Returns:
            Current mouse position as (x, y) tuple
        """
        return pyautogui.position()
    
    def move_to(self, x: int, y: int, duration: Optional[float] = None, safe_mode: bool = False) -> bool:
        """
        Move mouse to specified position with human-like curved movement.
        
        Args:
            x: Target X coordinate
            y: Target Y coordinate
            duration: Movement duration in seconds (if None, uses config)
            safe_mode: If True, only simulate the action without actually moving
            
        Returns:
            True if movement was successful, False otherwise
        """
        if not self.is_active and not safe_mode:
            return False
        
        if duration is None:
            duration = self.config.movement_speed
        
        try:
            if safe_mode:
                # Simulate mouse movement without actually moving
                print(f"[SAFE MODE] Simulated mouse move to ({x}, {y})")
                time.sleep(duration)
                self._last_position = (x, y)
                return True
            else:
                if self.config.human_like:
                    self._move_with_curve(x, y, duration)
                else:
                    pyautogui.moveTo(x, y, duration=duration)
                
                self._last_position = (x, y)
                return True
            
        except Exception as e:
            print(f"Error moving mouse to ({x}, {y}): {e}")
            return False
    
    def _move_with_curve(self, target_x: int, target_y: int, duration: float):
        """
        Move mouse with curved path for human-like behavior.
        
        Args:
            target_x: Target X coordinate
            target_y: Target Y coordinate
            duration: Movement duration in seconds
        """
        start_x, start_y = pyautogui.position()
        
        # Calculate distance
        distance = math.sqrt((target_x - start_x) ** 2 + (target_y - start_y) ** 2)
        
        # Determine number of steps based on distance and duration
        steps = max(10, int(distance / 10))
        step_duration = duration / steps
        
        # Generate curved path using Bezier curve
        control_points = self._generate_control_points(start_x, start_y, target_x, target_y)
        
        for i in range(steps + 1):
            t = i / steps
            x, y = self._bezier_curve(control_points, t)
            
            # Add small random variation
            if self.config.human_like:
                x += random.uniform(-2, 2)
                y += random.uniform(-2, 2)
            
            pyautogui.moveTo(int(x), int(y))
            time.sleep(step_duration)
    
    def _generate_control_points(self, start_x: int, start_y: int, end_x: int, end_y: int) -> List[Tuple[float, float]]:
        """
        Generate control points for Bezier curve.
        
        Args:
            start_x: Starting X coordinate
            start_y: Starting Y coordinate
            end_x: Ending X coordinate
            end_y: Ending Y coordinate
            
        Returns:
            List of control points for Bezier curve
        """
        # Calculate midpoint
        mid_x = (start_x + end_x) / 2
        mid_y = (start_y + end_y) / 2
        
        # Calculate distance
        distance = math.sqrt((end_x - start_x) ** 2 + (end_y - start_y) ** 2)
        
        # Generate random offset for curve
        offset_x = random.uniform(-distance * self.config.curve_intensity, distance * self.config.curve_intensity)
        offset_y = random.uniform(-distance * self.config.curve_intensity, distance * self.config.curve_intensity)
        
        # Control points for quadratic Bezier curve
        control_x = mid_x + offset_x
        control_y = mid_y + offset_y
        
        return [(start_x, start_y), (control_x, control_y), (end_x, end_y)]
    
    def _bezier_curve(self, control_points: List[Tuple[float, float]], t: float) -> Tuple[float, float]:
        """
        Calculate point on Bezier curve.
        
        Args:
            control_points: Control points for the curve
            t: Parameter t (0.0 to 1.0)
            
        Returns:
            Point on the curve as (x, y) tuple
        """
        n = len(control_points) - 1
        x = 0
        y = 0
        
        for i, (px, py) in enumerate(control_points):
            coefficient = math.comb(n, i) * (1 - t) ** (n - i) * t ** i
            x += coefficient * px
            y += coefficient * py
        
        return x, y
    
    def click(self, x: Optional[int] = None, y: Optional[int] = None, button: str = "left", safe_mode: bool = False) -> bool:
        """
        Click at specified position or current position.
        
        Args:
            x: X coordinate (if None, uses current position)
            y: Y coordinate (if None, uses current position)
            button: Mouse button ("left", "right", "middle")
            safe_mode: If True, only simulate the action without actually clicking
            
        Returns:
            True if click was successful, False otherwise
        """
        if not self.is_active and not safe_mode:
            return False
        
        try:
            if safe_mode:
                # Simulate click without actually clicking
                if x is not None and y is not None:
                    print(f"[SAFE MODE] Simulated mouse move to ({x}, {y})")
                    time.sleep(0.1)
                
                print(f"[SAFE MODE] Simulated {button} click at ({x or 'current'}, {y or 'current'})")
                time.sleep(0.1)
                return True
            else:
                if x is not None and y is not None:
                    self.move_to(x, y)
                
                # Add random delay before click
                if self.config.human_like:
                    time.sleep(random.uniform(0.05, 0.15))
                
                pyautogui.click(button=button)
                
                # Add random delay after click
                if self.config.human_like:
                    time.sleep(random.uniform(0.05, 0.15))
                
                print(f"Clicked at {pyautogui.position()} with {button} button")
                return True
            
        except Exception as e:
            print(f"Error clicking: {e}")
            return False
    
    def double_click(self, x: Optional[int] = None, y: Optional[int] = None, button: str = "left") -> bool:
        """
        Double click at specified position or current position.
        
        Args:
            x: X coordinate (if None, uses current position)
            y: Y coordinate (if None, uses current position)
            button: Mouse button ("left", "right", "middle")
            
        Returns:
            True if double click was successful, False otherwise
        """
        if not self.is_active:
            return False
        
        try:
            if x is not None and y is not None:
                self.move_to(x, y)
            
            pyautogui.doubleClick(button=button)
            
            print(f"Double clicked at {pyautogui.position()} with {button} button")
            return True
            
        except Exception as e:
            print(f"Error double clicking: {e}")
            return False
    
    def right_click(self, x: Optional[int] = None, y: Optional[int] = None) -> bool:
        """
        Right click at specified position or current position.
        
        Args:
            x: X coordinate (if None, uses current position)
            y: Y coordinate (if None, uses current position)
            
        Returns:
            True if right click was successful, False otherwise
        """
        return self.click(x, y, button="right")
    
    def drag(self, start_x: int, start_y: int, end_x: int, end_y: int, duration: Optional[float] = None) -> bool:
        """
        Drag from start position to end position.
        
        Args:
            start_x: Starting X coordinate
            start_y: Starting Y coordinate
            end_x: Ending X coordinate
            end_y: Ending Y coordinate
            duration: Drag duration in seconds (if None, uses config)
            
        Returns:
            True if drag was successful, False otherwise
        """
        if not self.is_active:
            return False
        
        if duration is None:
            duration = self.config.movement_speed
        
        try:
            # Move to start position
            self.move_to(start_x, start_y)
            
            # Press and hold
            pyautogui.mouseDown(button="left")
            
            # Move to end position
            self.move_to(end_x, end_y, duration=duration)
            
            # Release
            pyautogui.mouseUp(button="left")
            
            print(f"Dragged from ({start_x}, {start_y}) to ({end_x}, {end_y})")
            return True
            
        except Exception as e:
            print(f"Error dragging: {e}")
            return False
    
    def scroll(self, clicks: int, x: Optional[int] = None, y: Optional[int] = None) -> bool:
        """
        Scroll at specified position or current position.
        
        Args:
            clicks: Number of scroll clicks (positive for up, negative for down)
            x: X coordinate (if None, uses current position)
            y: Y coordinate (if None, uses current position)
            
        Returns:
            True if scroll was successful, False otherwise
        """
        if not self.is_active:
            return False
        
        try:
            if x is not None and y is not None:
                self.move_to(x, y)
            
            pyautogui.scroll(clicks)
            
            print(f"Scrolled {clicks} clicks at {pyautogui.position()}")
            return True
            
        except Exception as e:
            print(f"Error scrolling: {e}")
            return False
    
    def click_on_image(self, image_path: str, confidence: float = 0.8) -> bool:
        """
        Click on an image found on screen.
        
        Args:
            image_path: Path to the image to find
            confidence: Confidence level for image matching (0.0 to 1.0)
            
        Returns:
            True if image was found and clicked, False otherwise
        """
        if not self.is_active:
            return False
        
        try:
            location = pyautogui.locateOnScreen(image_path, confidence=confidence)
            if location:
                center = pyautogui.center(location)
                return self.click(center.x, center.y)
            else:
                print(f"Image {image_path} not found on screen")
                return False
                
        except Exception as e:
            print(f"Error clicking on image: {e}")
            return False
    
    def wait_for_image(self, image_path: str, timeout: float = 10.0, confidence: float = 0.8) -> Optional[Tuple[int, int]]:
        """
        Wait for an image to appear on screen.
        
        Args:
            image_path: Path to the image to wait for
            timeout: Maximum time to wait in seconds
            confidence: Confidence level for image matching (0.0 to 1.0)
            
        Returns:
            Center coordinates of the image if found, None if timeout
        """
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            try:
                location = pyautogui.locateOnScreen(image_path, confidence=confidence)
                if location:
                    center = pyautogui.center(location)
                    print(f"Image {image_path} found at {center}")
                    return (center.x, center.y)
            except Exception as e:
                print(f"Error waiting for image: {e}")
            
            time.sleep(0.1)
        
        print(f"Timeout waiting for image {image_path}")
        return None
    
    def start(self):
        """Start the mouse controller."""
        if self.is_active:
            print("Mouse controller already active")
            return
        
        self.is_active = True
        print("Mouse controller started")
    
    def stop(self):
        """Stop the mouse controller."""
        self.is_active = False
        print("Mouse controller stopped")
    
    def load_config(self, config_file: str):
        """
        Load mouse configuration from a JSON file.
        
        Args:
            config_file: Path to the configuration file
        """
        try:
            with open(config_file, 'r') as f:
                config_data = json.load(f)
            
            self.config = MouseConfig(
                movement_speed=config_data.get('movement_speed', 0.5),
                click_delay=config_data.get('click_delay', 0.1),
                human_like=config_data.get('human_like', True),
                curve_intensity=config_data.get('curve_intensity', 0.3)
            )
            
            print(f"Loaded mouse configuration from {config_file}")
            
        except Exception as e:
            print(f"Error loading mouse configuration: {e}")
    
    def save_config(self, config_file: str):
        """
        Save mouse configuration to a JSON file.
        
        Args:
            config_file: Path to the configuration file
        """
        try:
            config_data = {
                'movement_speed': self.config.movement_speed,
                'click_delay': self.config.click_delay,
                'human_like': self.config.human_like,
                'curve_intensity': self.config.curve_intensity
            }
            
            with open(config_file, 'w') as f:
                json.dump(config_data, f, indent=2)
            
            print(f"Saved mouse configuration to {config_file}")
            
        except Exception as e:
            print(f"Error saving mouse configuration: {e}") 