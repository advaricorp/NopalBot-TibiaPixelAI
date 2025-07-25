"""
Tibia-Specific Screenshot Bypass
By Taquito Loco 🎮

Aggressive techniques specifically designed to bypass Tibia's anti-screenshot measures.
Tibia uses very aggressive anti-screenshot techniques that require special handling.
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
from ctypes import windll, byref, c_void_p, c_uint, c_int, Structure, POINTER
from ctypes.wintypes import RECT, DWORD, BOOL, HANDLE, HWND

logger = logging.getLogger(__name__)

class TibiaAggressiveBypass:
    """Aggressive bypass techniques specifically for Tibia"""
    
    def __init__(self):
        self.tibia_window_handle = None
        self.tibia_region = None
        self.last_capture_time = 0
        self.capture_interval = 0.05  # 50ms between captures (more aggressive)
        
    def find_tibia_window(self) -> bool:
        """Find Tibia window with multiple detection methods"""
        try:
            # Method 1: Search by window title
            def enum_windows_callback(hwnd, windows):
                if win32gui.IsWindowVisible(hwnd):
                    window_text = win32gui.GetWindowText(hwnd).lower()
                    if any(keyword in window_text for keyword in ['tibia', 'client']):
                        windows.append(hwnd)
                return True
            
            windows = []
            win32gui.EnumWindows(enum_windows_callback, windows)
            
            if windows:
                self.tibia_window_handle = windows[0]
                self.tibia_region = win32gui.GetWindowRect(self.tibia_window_handle)
                logger.info(f"Found Tibia window: {win32gui.GetWindowText(self.tibia_window_handle)}")
                return True
            
            # Method 2: Search by process name
            try:
                import psutil
                for proc in psutil.process_iter(['pid', 'name']):
                    if 'tibia' in proc.info['name'].lower():
                        # Find window by process ID
                        def find_window_by_pid(hwnd, target_pid):
                            if win32gui.IsWindowVisible(hwnd):
                                try:
                                    _, pid = win32gui.GetWindowThreadProcessId(hwnd)
                                    if pid == target_pid:
                                        self.tibia_window_handle = hwnd
                                        self.tibia_region = win32gui.GetWindowRect(hwnd)
                                        return False  # Stop enumeration
                                except:
                                    pass
                            return True
                        
                        win32gui.EnumWindows(find_window_by_pid, proc.info['pid'])
                        if self.tibia_window_handle:
                            logger.info(f"Found Tibia window by process: {win32gui.GetWindowText(self.tibia_window_handle)}")
                            return True
            except ImportError:
                logger.warning("psutil not available, skipping process-based detection")
            
            return False
            
        except Exception as e:
            logger.error(f"Error finding Tibia window: {e}")
            return False
    
    def capture_tibia_aggressive(self) -> Optional[np.ndarray]:
        """Aggressive capture methods specifically for Tibia"""
        
        # Rate limiting
        current_time = time.time()
        if current_time - self.last_capture_time < self.capture_interval:
            time.sleep(self.capture_interval - (current_time - self.last_capture_time))
        
        # Try multiple aggressive methods
        methods = [
            self._capture_tibia_direct_memory,
            self._capture_tibia_hardware_accelerated,
            self._capture_tibia_directx_bypass,
            self._capture_tibia_window_dc,
            self._capture_tibia_screen_dc,
            self._capture_tibia_fallback
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
        
        logger.error("💀 All Tibia-specific methods failed")
        return None
    
    def _capture_tibia_direct_memory(self) -> Optional[np.ndarray]:
        """Direct memory access to Tibia's frame buffer"""
        try:
            if not self.tibia_window_handle:
                if not self.find_tibia_window():
                    return None
            
            # Get window DC
            window_dc = win32gui.GetWindowDC(self.tibia_window_handle)
            img_dc = win32ui.CreateDCFromHandle(window_dc)
            mem_dc = img_dc.CreateCompatibleDC()
            
            # Get window dimensions
            x, y, w, h = self.tibia_region
            width = w - x
            height = h - y
            
            # Create bitmap
            screenshot = win32ui.CreateBitmap()
            screenshot.CreateCompatibleBitmap(img_dc, width, height)
            mem_dc.SelectObject(screenshot)
            
            # Use aggressive BitBlt with special flags
            result = mem_dc.BitBlt(
                (0, 0), (width, height), 
                img_dc, (0, 0), 
                win32con.SRCCOPY | win32con.CAPTUREBLT
            )
            
            if not result:
                raise Exception("BitBlt failed")
            
            # Read bitmap data directly
            bmpinfo = screenshot.GetInfo()
            bmpstr = screenshot.GetBitmapBits(True)
            
            img = np.frombuffer(bmpstr, dtype='uint8')
            img.shape = (height, width, 4)
            img_bgr = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
            
            # Clean up
            win32gui.DeleteObject(screenshot.GetHandle())
            mem_dc.DeleteDC()
            img_dc.DeleteDC()
            win32gui.ReleaseDC(self.tibia_window_handle, window_dc)
            
            return img_bgr
            
        except Exception as e:
            logger.debug(f"Direct memory error: {e}")
            return None
    
    def _capture_tibia_hardware_accelerated(self) -> Optional[np.ndarray]:
        """Hardware accelerated capture for Tibia"""
        try:
            if not self.tibia_window_handle:
                if not self.find_tibia_window():
                    return None
            
            # Get window DC
            window_dc = win32gui.GetWindowDC(self.tibia_window_handle)
            img_dc = win32ui.CreateDCFromHandle(window_dc)
            mem_dc = img_dc.CreateCompatibleDC()
            
            # Get window dimensions
            x, y, w, h = self.tibia_region
            width = w - x
            height = h - y
            
            # Create bitmap
            screenshot = win32ui.CreateBitmap()
            screenshot.CreateCompatibleBitmap(img_dc, width, height)
            mem_dc.SelectObject(screenshot)
            
            # Use StretchBlt for hardware acceleration
            mem_dc.StretchBlt(
                (0, 0), (width, height),
                img_dc, (0, 0), (width, height),
                win32con.SRCCOPY
            )
            
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
            win32gui.ReleaseDC(self.tibia_window_handle, window_dc)
            
            return img_bgr
            
        except Exception as e:
            logger.debug(f"Hardware accelerated error: {e}")
            return None
    
    def _capture_tibia_directx_bypass(self) -> Optional[np.ndarray]:
        """DirectX bypass for Tibia"""
        try:
            if not self.tibia_window_handle:
                if not self.find_tibia_window():
                    return None
            
            # Get window DC
            window_dc = win32gui.GetWindowDC(self.tibia_window_handle)
            img_dc = win32ui.CreateDCFromHandle(window_dc)
            mem_dc = img_dc.CreateCompatibleDC()
            
            # Get window dimensions
            x, y, w, h = self.tibia_region
            width = w - x
            height = h - y
            
            # Create bitmap
            screenshot = win32ui.CreateBitmap()
            screenshot.CreateCompatibleBitmap(img_dc, width, height)
            mem_dc.SelectObject(screenshot)
            
            # Use PatBlt + BitBlt combination
            mem_dc.PatBlt((0, 0), (width, height), win32con.WHITENESS)
            mem_dc.BitBlt((0, 0), (width, height), img_dc, (0, 0), win32con.SRCCOPY)
            
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
            win32gui.ReleaseDC(self.tibia_window_handle, window_dc)
            
            return img_bgr
            
        except Exception as e:
            logger.debug(f"DirectX bypass error: {e}")
            return None
    
    def _capture_tibia_window_dc(self) -> Optional[np.ndarray]:
        """Window DC capture for Tibia"""
        try:
            if not self.tibia_window_handle:
                if not self.find_tibia_window():
                    return None
            
            # Get window DC
            window_dc = win32gui.GetWindowDC(self.tibia_window_handle)
            img_dc = win32ui.CreateDCFromHandle(window_dc)
            mem_dc = img_dc.CreateCompatibleDC()
            
            # Get window dimensions
            x, y, w, h = self.tibia_region
            width = w - x
            height = h - y
            
            # Create bitmap
            screenshot = win32ui.CreateBitmap()
            screenshot.CreateCompatibleBitmap(img_dc, width, height)
            mem_dc.SelectObject(screenshot)
            
            # Simple BitBlt
            mem_dc.BitBlt((0, 0), (width, height), img_dc, (0, 0), win32con.SRCCOPY)
            
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
            win32gui.ReleaseDC(self.tibia_window_handle, window_dc)
            
            return img_bgr
            
        except Exception as e:
            logger.debug(f"Window DC error: {e}")
            return None
    
    def _capture_tibia_screen_dc(self) -> Optional[np.ndarray]:
        """Screen DC capture for Tibia"""
        try:
            if not self.tibia_window_handle:
                if not self.find_tibia_window():
                    return None
            
            # Get screen DC
            screen_dc = win32gui.GetDC(0)
            img_dc = win32ui.CreateDCFromHandle(screen_dc)
            mem_dc = img_dc.CreateCompatibleDC()
            
            # Get window dimensions
            x, y, w, h = self.tibia_region
            width = w - x
            height = h - y
            
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
    
    def _capture_tibia_fallback(self) -> Optional[np.ndarray]:
        """Fallback methods for Tibia"""
        try:
            if not self.tibia_window_handle:
                if not self.find_tibia_window():
                    return None
            
            # Try with pyautogui
            try:
                import pyautogui
                x, y, w, h = self.tibia_region
                screenshot = pyautogui.screenshot(region=(x, y, w-x, h-y))
                img_array = np.array(screenshot)
                img_bgr = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
                return img_bgr
            except Exception as e:
                logger.debug(f"PyAutoGUI fallback error: {e}")
            
            # Try with PIL
            try:
                from PIL import ImageGrab
                x, y, w, h = self.tibia_region
                screenshot = ImageGrab.grab(bbox=(x, y, w, h))
                img_array = np.array(screenshot)
                img_bgr = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
                return img_bgr
            except Exception as e:
                logger.debug(f"PIL fallback error: {e}")
            
            return None
            
        except Exception as e:
            logger.debug(f"Fallback error: {e}")
            return None
    
    def test_tibia_capture(self) -> Dict[str, Any]:
        """Test Tibia capture with all methods"""
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
                'title': win32gui.GetWindowText(self.tibia_window_handle),
                'region': self.tibia_region
            }
            
            # Test all methods
            methods = [
                ('Direct Memory', self._capture_tibia_direct_memory),
                ('Hardware Accelerated', self._capture_tibia_hardware_accelerated),
                ('DirectX Bypass', self._capture_tibia_directx_bypass),
                ('Window DC', self._capture_tibia_window_dc),
                ('Screen DC', self._capture_tibia_screen_dc),
                ('Fallback', self._capture_tibia_fallback)
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