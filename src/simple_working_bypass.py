"""
Simple Working Screenshot Bypass for Tibia
By Taquito Loco 🎮

Based on community research and techniques that actually work:
- Screen DC capture (most reliable)
- Window DC with special flags
- Desktop DC bypass
- Multiple fallback methods
"""

import cv2
import numpy as np
import time
import logging
from typing import Optional, Tuple, Dict, Any
import win32gui
import win32ui
import win32con
import win32api

logger = logging.getLogger(__name__)

class SimpleWorkingBypass:
    """Simple but effective bypass techniques for Tibia"""
    
    def __init__(self):
        self.tibia_window = None
        self.last_capture_time = 0
        self.capture_interval = 0.05  # 50ms between captures
        
    def find_tibia_window(self) -> bool:
        """Find Tibia window handle"""
        try:
            def enum_windows_callback(hwnd, windows):
                if win32gui.IsWindowVisible(hwnd):
                    window_text = win32gui.GetWindowText(hwnd).lower()
                    if 'tibia' in window_text:
                        windows.append(hwnd)
                return True
            
            windows = []
            win32gui.EnumWindows(enum_windows_callback, windows)
            
            if windows:
                self.tibia_window = windows[0]
                logger.info(f"Found Tibia window: {win32gui.GetWindowText(self.tibia_window)}")
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"Error finding Tibia window: {e}")
            return False
    
    def capture_simple_working(self) -> Optional[np.ndarray]:
        """Capture using simple but working methods"""
        
        # Rate limiting
        current_time = time.time()
        if current_time - self.last_capture_time < self.capture_interval:
            time.sleep(self.capture_interval - (current_time - self.last_capture_time))
        
        # Try simple working methods
        methods = [
            ('Screen DC', self._capture_screen_dc),
            ('Window DC Special', self._capture_window_dc_special),
            ('Desktop DC', self._capture_desktop_dc),
            ('Fallback Simple', self._capture_fallback_simple)
        ]
        
        for method_name, method_func in methods:
            try:
                logger.debug(f"🔄 Trying {method_name}...")
                start_time = time.time()
                result = method_func()
                if result is not None:
                    logger.info(f"✅ {method_name} successful: {result.shape[1]}x{result.shape[0]}")
                    self.last_capture_time = time.time()
                    return result
                else:
                    logger.debug(f"❌ {method_name} failed")
            except Exception as e:
                logger.debug(f"❌ {method_name} error: {e}")
        
        logger.error("💀 All simple methods failed")
        return None
    
    def _capture_screen_dc(self) -> Optional[np.ndarray]:
        """Screen DC capture - most reliable method"""
        try:
            if not self.tibia_window:
                if not self.find_tibia_window():
                    return None
            
            # Get window region
            region = win32gui.GetWindowRect(self.tibia_window)
            x, y, w, h = region
            width = w - x
            height = h - y
            
            # Get screen DC
            screen_dc = win32gui.GetDC(0)
            img_dc = win32ui.CreateDCFromHandle(screen_dc)
            mem_dc = img_dc.CreateCompatibleDC()
            
            # Create bitmap
            screenshot = win32ui.CreateBitmap()
            screenshot.CreateCompatibleBitmap(img_dc, width, height)
            mem_dc.SelectObject(screenshot)
            
            # Capture from screen coordinates
            mem_dc.BitBlt((0, 0), (width, height), img_dc, (x, y), win32con.SRCCOPY)
            
            # Read bitmap data
            bmpinfo = screenshot.GetInfo()
            bmpstr = screenshot.GetBitmapBits(True)
            
            img = np.frombuffer(bmpstr, dtype='uint8')
            img.shape = (height, width, 4)
            img_bgr = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
            
            # Clean up
            win32gui.DeleteObject(screenshot.GetHandle())
            mem_dc.DeleteDC()
            img_dc.DeleteDC()
            win32gui.ReleaseDC(0, screen_dc)
            
            return img_bgr
            
        except Exception as e:
            logger.debug(f"Screen DC error: {e}")
            return None
    
    def _capture_window_dc_special(self) -> Optional[np.ndarray]:
        """Window DC with special flags"""
        try:
            if not self.tibia_window:
                if not self.find_tibia_window():
                    return None
            
            # Get window region
            region = win32gui.GetWindowRect(self.tibia_window)
            x, y, w, h = region
            width = w - x
            height = h - y
            
            # Get window DC
            window_dc = win32gui.GetWindowDC(self.tibia_window)
            img_dc = win32ui.CreateDCFromHandle(window_dc)
            mem_dc = img_dc.CreateCompatibleDC()
            
            # Create bitmap
            screenshot = win32ui.CreateBitmap()
            screenshot.CreateCompatibleBitmap(img_dc, width, height)
            mem_dc.SelectObject(screenshot)
            
            # Use special flags
            mem_dc.BitBlt((0, 0), (width, height), img_dc, (0, 0), win32con.SRCCOPY | win32con.CAPTUREBLT)
            
            # Read bitmap data
            bmpinfo = screenshot.GetInfo()
            bmpstr = screenshot.GetBitmapBits(True)
            
            img = np.frombuffer(bmpstr, dtype='uint8')
            img.shape = (height, width, 4)
            img_bgr = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
            
            # Clean up
            win32gui.DeleteObject(screenshot.GetHandle())
            mem_dc.DeleteDC()
            img_dc.DeleteDC()
            win32gui.ReleaseDC(self.tibia_window, window_dc)
            
            return img_bgr
            
        except Exception as e:
            logger.debug(f"Window DC special error: {e}")
            return None
    
    def _capture_desktop_dc(self) -> Optional[np.ndarray]:
        """Desktop DC bypass"""
        try:
            if not self.tibia_window:
                if not self.find_tibia_window():
                    return None
            
            # Get window region
            region = win32gui.GetWindowRect(self.tibia_window)
            x, y, w, h = region
            width = w - x
            height = h - y
            
            # Get desktop DC
            desktop_dc = win32gui.GetDesktopWindow()
            desktop_dc_handle = win32gui.GetWindowDC(desktop_dc)
            img_dc = win32ui.CreateDCFromHandle(desktop_dc_handle)
            mem_dc = img_dc.CreateCompatibleDC()
            
            # Create bitmap
            screenshot = win32ui.CreateBitmap()
            screenshot.CreateCompatibleBitmap(img_dc, width, height)
            mem_dc.SelectObject(screenshot)
            
            # Capture from desktop coordinates
            mem_dc.BitBlt((0, 0), (width, height), img_dc, (x, y), win32con.SRCCOPY)
            
            # Read bitmap data
            bmpinfo = screenshot.GetInfo()
            bmpstr = screenshot.GetBitmapBits(True)
            
            img = np.frombuffer(bmpstr, dtype='uint8')
            img.shape = (height, width, 4)
            img_bgr = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
            
            # Clean up
            win32gui.DeleteObject(screenshot.GetHandle())
            mem_dc.DeleteDC()
            img_dc.DeleteDC()
            win32gui.ReleaseDC(desktop_dc, desktop_dc_handle)
            
            return img_bgr
            
        except Exception as e:
            logger.debug(f"Desktop DC error: {e}")
            return None
    
    def _capture_fallback_simple(self) -> Optional[np.ndarray]:
        """Simple fallback methods"""
        try:
            if not self.tibia_window:
                if not self.find_tibia_window():
                    return None
            
            # Get window region
            region = win32gui.GetWindowRect(self.tibia_window)
            x, y, w, h = region
            width = w - x
            height = h - y
            
            # Try multiple fallback methods
            fallback_methods = [
                # PyAutoGUI
                lambda: self._try_pyautogui(x, y, width, height),
                # PIL
                lambda: self._try_pil(x, y, w, h),
                # MSS
                lambda: self._try_mss(x, y, w, h)
            ]
            
            for method in fallback_methods:
                try:
                    result = method()
                    if result is not None:
                        return result
                except Exception as e:
                    logger.debug(f"Fallback method error: {e}")
            
            return None
            
        except Exception as e:
            logger.debug(f"Fallback simple error: {e}")
            return None
    
    def _try_pyautogui(self, x, y, width, height):
        """Try PyAutoGUI capture"""
        try:
            import pyautogui
            screenshot = pyautogui.screenshot(region=(x, y, width, height))
            img_array = np.array(screenshot)
            return cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
        except:
            return None
    
    def _try_pil(self, x, y, w, h):
        """Try PIL capture"""
        try:
            from PIL import ImageGrab
            screenshot = ImageGrab.grab(bbox=(x, y, w, h))
            img_array = np.array(screenshot)
            return cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
        except:
            return None
    
    def _try_mss(self, x, y, w, h):
        """Try MSS capture"""
        try:
            import mss
            with mss.mss() as sct:
                monitor = {"top": y, "left": x, "width": w-x, "height": h-y}
                screenshot = sct.grab(monitor)
                img_array = np.array(screenshot)
                return cv2.cvtColor(img_array, cv2.COLOR_BGRA2BGR)
        except:
            return None
    
    def test_simple_capture(self) -> Dict[str, Any]:
        """Test simple capture with all methods"""
        results = {
            'tibia_found': False,
            'methods_tested': [],
            'successful_methods': [],
            'best_method': None,
            'sample_image': None
        }
        
        # Find Tibia window
        if self.find_tibia_window():
            results['tibia_found'] = True
            results['window_info'] = {
                'title': win32gui.GetWindowText(self.tibia_window),
                'region': win32gui.GetWindowRect(self.tibia_window)
            }
            
            # Test all methods
            methods = [
                ('Screen DC', self._capture_screen_dc),
                ('Window DC Special', self._capture_window_dc_special),
                ('Desktop DC', self._capture_desktop_dc),
                ('Fallback Simple', self._capture_fallback_simple)
            ]
            
            for method_name, method_func in methods:
                results['methods_tested'].append(method_name)
                try:
                    start_time = time.time()
                    image = method_func()
                    end_time = time.time()
                    
                    if image is not None:
                        results['successful_methods'].append({
                            'name': method_name,
                            'time': end_time - start_time,
                            'size': f"{image.shape[1]}x{image.shape[0]}"
                        })
                        
                        # Save first successful image
                        if results['sample_image'] is None:
                            results['sample_image'] = image
                            results['best_method'] = method_name
                            
                except Exception as e:
                    logger.debug(f"Method {method_name} failed: {e}")
        
        return results 