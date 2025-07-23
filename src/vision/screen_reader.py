"""
Screen Reader Module for Tibia Bot

This module provides efficient screen capturing capabilities for reading
the Tibia client window and extracting game information.
"""

import cv2
import numpy as np
import mss
import mss.tools
from typing import Optional, Tuple, Dict, Any
import time
import threading
from dataclasses import dataclass


@dataclass
class WindowInfo:
    """Information about a window including its position and size."""
    x: int
    y: int
    width: int
    height: int
    title: str


class ScreenReader:
    """
    Efficient screen reader for capturing Tibia client window.
    
    This class provides methods to capture the Tibia window and extract
    game information using computer vision techniques.
    """
    
    def __init__(self, window_title: str = "Tibia"):
        """
        Initialize the ScreenReader.
        
        Args:
            window_title: Title of the window to capture (default: "Tibia")
        """
        self.window_title = window_title
        self.window_info: Optional[WindowInfo] = None
        self._capture_thread: Optional[threading.Thread] = None
        self._stop_capture = False
        self._current_frame: Optional[np.ndarray] = None
        self._frame_lock = threading.Lock()
        
    def find_window(self) -> bool:
        """
        Find the Tibia window and store its information.
        
        Returns:
            True if window is found, False otherwise
        """
        try:
            import win32gui
            import win32con
            
            def enum_windows_callback(hwnd, windows):
                if win32gui.IsWindowVisible(hwnd):
                    window_text = win32gui.GetWindowText(hwnd)
                    if self.window_title.lower() in window_text.lower():
                        rect = win32gui.GetWindowRect(hwnd)
                        x, y, right, bottom = rect
                        width = right - x
                        height = bottom - y
                        windows.append(WindowInfo(x, y, width, height, window_text))
                return True
            
            windows = []
            win32gui.EnumWindows(enum_windows_callback, windows)
            
            if windows:
                self.window_info = windows[0]
                print(f"Found Tibia window: {self.window_info.title}")
                print(f"Position: ({self.window_info.x}, {self.window_info.y})")
                print(f"Size: {self.window_info.width}x{self.window_info.height}")
                return True
            else:
                print(f"Tibia window with title '{self.window_title}' not found")
                return False
                
        except ImportError:
            print("win32gui not available. Please install pywin32: pip install pywin32")
            return False
    
    def start_capture(self) -> bool:
        """
        Start continuous screen capture in a separate thread.
        
        Returns:
            True if capture started successfully, False otherwise
        """
        if not self.window_info:
            if not self.find_window():
                return False
        
        if self._capture_thread and self._capture_thread.is_alive():
            print("Capture thread already running")
            return True
        
        self._stop_capture = False
        self._capture_thread = threading.Thread(target=self._capture_loop, daemon=True)
        self._capture_thread.start()
        print("Screen capture started")
        return True
    
    def stop_capture(self):
        """Stop the continuous screen capture."""
        self._stop_capture = True
        if self._capture_thread:
            self._capture_thread.join(timeout=2.0)
        print("Screen capture stopped")
    
    def _capture_loop(self):
        """Internal method for continuous screen capture."""
        while not self._stop_capture:
            try:
                frame = self._capture_frame()
                if frame is not None:
                    with self._frame_lock:
                        self._current_frame = frame
                time.sleep(0.016)  # ~60 FPS
            except Exception as e:
                print(f"Error in capture loop: {e}")
                time.sleep(0.1)
    
    def _capture_frame(self) -> Optional[np.ndarray]:
        """
        Capture a single frame from the Tibia window.
        
        Returns:
            Captured frame as numpy array, or None if failed
        """
        if not self.window_info:
            return None
        
        # Try multiple capture methods
        methods = [
            self._capture_with_mss,
            self._capture_with_win32api,
            self._capture_with_pil
        ]
        
        for method in methods:
            try:
                frame = method()
                if frame is not None:
                    return frame
            except Exception as e:
                print(f"Capture method {method.__name__} failed: {e}")
                continue
        
        return None
    
    def _capture_with_mss(self) -> Optional[np.ndarray]:
        """Capture using MSS (primary method)."""
        try:
            # Create a new MSS instance for each capture to avoid threading issues
            with mss.mss() as sct:
                # Define the region to capture
                monitor = {
                    "top": self.window_info.y,
                    "left": self.window_info.x,
                    "width": self.window_info.width,
                    "height": self.window_info.height
                }
                
                # Capture the screen
                screenshot = sct.grab(monitor)
                
                # Convert to numpy array
                frame = np.array(screenshot)
                
                # Convert from BGRA to BGR (OpenCV format)
                frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)
                
                return frame
            
        except Exception as e:
            print(f"Error capturing frame with MSS: {e}")
            return None
    
    def _capture_with_win32api(self) -> Optional[np.ndarray]:
        """Capture using Win32API (fallback method)."""
        try:
            import win32gui
            import win32ui
            import win32con
            import win32api
            
            # Find the window
            hwnd = win32gui.FindWindow(None, self.window_info.title)
            if not hwnd:
                return None
            
            # Get window DC
            wDC = win32gui.GetWindowDC(hwnd)
            dcObj = win32ui.CreateDCFromHandle(wDC)
            cDC = dcObj.CreateCompatibleDC()
            
            # Create bitmap
            dataBitMap = win32ui.CreateBitmap()
            dataBitMap.CreateCompatibleBitmap(dcObj, self.window_info.width, self.window_info.height)
            cDC.SelectObject(dataBitMap)
            
            # Copy screen to bitmap
            cDC.BitBlt((0, 0), (self.window_info.width, self.window_info.height), 
                      dcObj, (0, 0), win32con.SRCCOPY)
            
            # Convert to numpy array
            bmpinfo = dataBitMap.GetInfo()
            bmpstr = dataBitMap.GetBitmapBits(True)
            
            # Convert to numpy array
            frame = np.frombuffer(bmpstr, dtype='uint8')
            frame.shape = (self.window_info.height, self.window_info.width, 4)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)
            
            # Cleanup
            dcObj.DeleteDC()
            cDC.DeleteDC()
            win32gui.ReleaseDC(hwnd, wDC)
            win32gui.DeleteObject(dataBitMap.GetHandle())
            
            return frame
            
        except Exception as e:
            print(f"Error capturing frame with Win32API: {e}")
            return None
    
    def _capture_with_pil(self) -> Optional[np.ndarray]:
        """Capture using PIL (alternative method)."""
        try:
            from PIL import ImageGrab
            
            # Capture the specific region
            bbox = (self.window_info.x, self.window_info.y, 
                   self.window_info.x + self.window_info.width, 
                   self.window_info.y + self.window_info.height)
            
            screenshot = ImageGrab.grab(bbox=bbox)
            
            # Convert to numpy array
            frame = np.array(screenshot)
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            
            return frame
            
        except Exception as e:
            print(f"Error capturing frame with PIL: {e}")
            return None
    
    def get_current_frame(self) -> Optional[np.ndarray]:
        """
        Get the most recently captured frame.
        
        Returns:
            Current frame as numpy array, or None if not available
        """
        with self._frame_lock:
            return self._current_frame.copy() if self._current_frame is not None else None
    
    def capture_single_frame(self) -> Optional[np.ndarray]:
        """
        Capture a single frame immediately.
        
        Returns:
            Captured frame as numpy array, or None if failed
        """
        return self._capture_frame()
    
    def get_window_info(self) -> Optional[WindowInfo]:
        """
        Get information about the captured window.
        
        Returns:
            WindowInfo object or None if window not found
        """
        return self.window_info
    
    def is_window_active(self) -> bool:
        """
        Check if the Tibia window is still active and visible.
        
        Returns:
            True if window is active, False otherwise
        """
        if not self.window_info:
            return False
        
        try:
            import win32gui
            hwnd = win32gui.FindWindow(None, self.window_info.title)
            if hwnd == 0:
                return False
            
            return win32gui.IsWindowVisible(hwnd)
            
        except ImportError:
            # Fallback: assume window is active if we can capture frames
            return self.capture_single_frame() is not None
    
    def test_capture_methods(self) -> Dict[str, bool]:
        """
        Test all available capture methods and return which ones work.
        
        Returns:
            Dictionary mapping method names to success status
        """
        if not self.window_info:
            print("No window found, cannot test capture methods")
            return {}
        
        methods = {
            "MSS": self._capture_with_mss,
            "Win32API": self._capture_with_win32api,
            "PIL": self._capture_with_pil
        }
        
        results = {}
        
        print("Testing capture methods...")
        for name, method in methods.items():
            try:
                frame = method()
                if frame is not None:
                    results[name] = True
                    print(f"✓ {name}: Success ({frame.shape})")
                else:
                    results[name] = False
                    print(f"✗ {name}: Failed (returned None)")
            except Exception as e:
                results[name] = False
                print(f"✗ {name}: Failed ({e})")
        
        return results
    
    def get_best_capture_method(self) -> str:
        """
        Get the best working capture method.
        
        Returns:
            Name of the best working method
        """
        results = self.test_capture_methods()
        
        # Priority order
        priority = ["MSS", "Win32API", "PIL"]
        
        for method in priority:
            if results.get(method, False):
                return method
        
        return "None"
    
    def __del__(self):
        """Cleanup when the object is destroyed."""
        self.stop_capture() 