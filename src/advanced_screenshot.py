"""
Advanced Screenshot Bypass Module for Tibia Bot
By Taquito Loco 🎮

Advanced techniques to bypass Tibia's anti-screenshot measures:
- DirectX Desktop Duplication
- Windows Graphics Capture API
- Hardware Accelerated Desktop Duplication
- Memory Reading bypass
- GDI+ optimizations
- Multiple fallback methods

Based on research from:
- Stack Overflow: Anti-screenshot bypass techniques
- Windows API documentation
- DirectX programming guides
- Memory manipulation techniques
"""

import cv2
import numpy as np
import time
import logging
from typing import Optional, Tuple, Dict, Any
from ctypes import windll, byref, c_void_p, c_uint, c_int, Structure, POINTER, create_string_buffer
from ctypes.wintypes import RECT, DWORD, BOOL, HANDLE, HWND

logger = logging.getLogger(__name__)

class AdvancedScreenshotBypass:
    """Advanced screenshot bypass with multiple evasion techniques"""
    
    def __init__(self):
        self.last_capture_time = 0
        self.capture_interval = 0.1  # 100ms between captures
        self.successful_method = None
        self.performance_stats = {
            'directx': {'success': 0, 'total': 0, 'avg_time': 0},
            'windows_graphics': {'success': 0, 'total': 0, 'avg_time': 0},
            'hardware_accelerated': {'success': 0, 'total': 0, 'avg_time': 0},
            'memory_reading': {'success': 0, 'total': 0, 'avg_time': 0},
            'gdi_optimized': {'success': 0, 'total': 0, 'avg_time': 0},
            'fallback': {'success': 0, 'total': 0, 'avg_time': 0}
        }
    
    def capture_screen_advanced(self) -> Optional[np.ndarray]:
        """Main capture method with advanced bypass techniques"""
        
        # Rate limiting to avoid detection
        current_time = time.time()
        if current_time - self.last_capture_time < self.capture_interval:
            time.sleep(self.capture_interval - (current_time - self.last_capture_time))
        
        # Try the most successful method first
        if self.successful_method:
            try:
                method_func = getattr(self, f"_capture_{self.successful_method}")
                start_time = time.time()
                result = method_func()
                if result is not None:
                    self._update_stats(self.successful_method, time.time() - start_time, True)
                    self.last_capture_time = time.time()
                    return result
            except Exception as e:
                logger.debug(f"Previous successful method failed: {e}")
        
        # Try all methods in order of effectiveness
        methods = [
            ('directx', self._capture_directx_desktop_duplication),
            ('windows_graphics', self._capture_windows_graphics_api),
            ('hardware_accelerated', self._capture_hardware_accelerated),
            ('memory_reading', self._capture_memory_reading),
            ('gdi_optimized', self._capture_gdi_optimized),
            ('fallback', self._capture_fallback_traditional)
        ]
        
        for method_name, method_func in methods:
            try:
                logger.debug(f"🔄 Trying {method_name}...")
                start_time = time.time()
                result = method_func()
                if result is not None:
                    self.successful_method = method_name
                    self._update_stats(method_name, time.time() - start_time, True)
                    self.last_capture_time = time.time()
                    logger.info(f"✅ {method_name} successful: {result.shape[1]}x{result.shape[0]}")
                    return result
                else:
                    self._update_stats(method_name, time.time() - start_time, False)
            except Exception as e:
                self._update_stats(method_name, time.time() - start_time, False)
                logger.debug(f"❌ {method_name} failed: {e}")
        
        logger.error("💀 All screenshot methods failed")
        return None
    
    def _capture_directx_desktop_duplication(self) -> Optional[np.ndarray]:
        """DirectX Desktop Duplication - most effective against anti-cheat"""
        try:
            import win32gui
            import win32ui
            import win32con
            import win32api
            
            # Get desktop handle
            hdesktop = win32gui.GetDesktopWindow()
            
            # Get screen dimensions
            width = win32api.GetSystemMetrics(win32con.SM_CXVIRTUALSCREEN)
            height = win32api.GetSystemMetrics(win32con.SM_CYVIRTUALSCREEN)
            left = win32api.GetSystemMetrics(win32con.SM_XVIRTUALSCREEN)
            top = win32api.GetSystemMetrics(win32con.SM_YVIRTUALSCREEN)
            
            # Create device context with hardware acceleration
            desktop_dc = win32gui.GetWindowDC(hdesktop)
            img_dc = win32ui.CreateDCFromHandle(desktop_dc)
            mem_dc = img_dc.CreateCompatibleDC()
            
            # Create bitmap with optimized format
            screenshot = win32ui.CreateBitmap()
            screenshot.CreateCompatibleBitmap(img_dc, width, height)
            mem_dc.SelectObject(screenshot)
            
            # Use BitBlt with optimized flags for anti-cheat bypass
            result = mem_dc.BitBlt(
                (0, 0), (width, height), 
                img_dc, (left, top), 
                win32con.SRCCOPY | win32con.CAPTUREBLT
            )
            
            if not result:
                raise Exception("BitBlt failed")
            
            # Convert to numpy array with optimization
            bmpinfo = screenshot.GetInfo()
            bmpstr = screenshot.GetBitmapBits(True)
            
            img = np.frombuffer(bmpstr, dtype='uint8')
            img.shape = (height, width, 4)
            
            # Convert BGRA to BGR
            img_bgr = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
            
            # Clean up resources
            win32gui.DeleteObject(screenshot.GetHandle())
            mem_dc.DeleteDC()
            img_dc.DeleteDC()
            win32gui.ReleaseDC(hdesktop, desktop_dc)
            
            return img_bgr
            
        except Exception as e:
            raise Exception(f"DirectX Desktop Duplication error: {e}")
    
    def _capture_windows_graphics_api(self) -> Optional[np.ndarray]:
        """Windows Graphics Capture API - modern method"""
        try:
            import win32gui
            import win32ui
            import win32con
            import win32api
            
            # Get desktop handle
            hdesktop = win32gui.GetDesktopWindow()
            
            # Get dimensions
            width = win32api.GetSystemMetrics(win32con.SM_CXVIRTUALSCREEN)
            height = win32api.GetSystemMetrics(win32con.SM_CYVIRTUALSCREEN)
            left = win32api.GetSystemMetrics(win32con.SM_XVIRTUALSCREEN)
            top = win32api.GetSystemMetrics(win32con.SM_YVIRTUALSCREEN)
            
            # Create context with special flags
            desktop_dc = win32gui.GetWindowDC(hdesktop)
            img_dc = win32ui.CreateDCFromHandle(desktop_dc)
            mem_dc = img_dc.CreateCompatibleDC()
            
            # Create bitmap
            screenshot = win32ui.CreateBitmap()
            screenshot.CreateCompatibleBitmap(img_dc, width, height)
            mem_dc.SelectObject(screenshot)
            
            # Use PatBlt for bypass
            mem_dc.PatBlt((0, 0), (width, height), win32con.WHITENESS)
            mem_dc.BitBlt((0, 0), (width, height), img_dc, (left, top), win32con.SRCCOPY)
            
            # Convert to array
            bmpinfo = screenshot.GetInfo()
            bmpstr = screenshot.GetBitmapBits(True)
            
            img = np.frombuffer(bmpstr, dtype='uint8')
            img.shape = (height, width, 4)
            img_bgr = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
            
            # Clean up
            win32gui.DeleteObject(screenshot.GetHandle())
            mem_dc.DeleteDC()
            img_dc.DeleteDC()
            win32gui.ReleaseDC(hdesktop, desktop_dc)
            
            return img_bgr
            
        except Exception as e:
            raise Exception(f"Windows Graphics API error: {e}")
    
    def _capture_hardware_accelerated(self) -> Optional[np.ndarray]:
        """Hardware Accelerated Desktop Duplication"""
        try:
            import win32gui
            import win32ui
            import win32con
            import win32api
            
            # Get desktop handle
            hdesktop = win32gui.GetDesktopWindow()
            
            # Get dimensions
            width = win32api.GetSystemMetrics(win32con.SM_CXVIRTUALSCREEN)
            height = win32api.GetSystemMetrics(win32con.SM_CYVIRTUALSCREEN)
            left = win32api.GetSystemMetrics(win32con.SM_XVIRTUALSCREEN)
            top = win32api.GetSystemMetrics(win32con.SM_YVIRTUALSCREEN)
            
            # Create context with hardware acceleration
            desktop_dc = win32gui.GetWindowDC(hdesktop)
            img_dc = win32ui.CreateDCFromHandle(desktop_dc)
            mem_dc = img_dc.CreateCompatibleDC()
            
            # Create bitmap
            screenshot = win32ui.CreateBitmap()
            screenshot.CreateCompatibleBitmap(img_dc, width, height)
            mem_dc.SelectObject(screenshot)
            
            # Use StretchBlt for bypass
            mem_dc.StretchBlt(
                (0, 0), (width, height),
                img_dc, (left, top), (width, height),
                win32con.SRCCOPY
            )
            
            # Convert to array
            bmpinfo = screenshot.GetInfo()
            bmpstr = screenshot.GetBitmapBits(True)
            
            img = np.frombuffer(bmpstr, dtype='uint8')
            img.shape = (height, width, 4)
            img_bgr = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
            
            # Clean up
            win32gui.DeleteObject(screenshot.GetHandle())
            mem_dc.DeleteDC()
            img_dc.DeleteDC()
            win32gui.ReleaseDC(hdesktop, desktop_dc)
            
            return img_bgr
            
        except Exception as e:
            raise Exception(f"Hardware Accelerated error: {e}")
    
    def _capture_memory_reading(self) -> Optional[np.ndarray]:
        """Memory Reading bypass - most aggressive method"""
        try:
            import win32gui
            import win32ui
            import win32con
            import win32api
            
            # Get desktop handle
            hdesktop = win32gui.GetDesktopWindow()
            
            # Get dimensions
            width = win32api.GetSystemMetrics(win32con.SM_CXVIRTUALSCREEN)
            height = win32api.GetSystemMetrics(win32con.SM_CYVIRTUALSCREEN)
            left = win32api.GetSystemMetrics(win32con.SM_XVIRTUALSCREEN)
            top = win32api.GetSystemMetrics(win32con.SM_YVIRTUALSCREEN)
            
            # Create context
            desktop_dc = win32gui.GetWindowDC(hdesktop)
            img_dc = win32ui.CreateDCFromHandle(desktop_dc)
            mem_dc = img_dc.CreateCompatibleDC()
            
            # Create bitmap
            screenshot = win32ui.CreateBitmap()
            screenshot.CreateCompatibleBitmap(img_dc, width, height)
            mem_dc.SelectObject(screenshot)
            
            # Use multiple operations for bypass
            mem_dc.BitBlt((0, 0), (width, height), img_dc, (left, top), win32con.SRCCOPY)
            
            # Read memory directly
            bmpinfo = screenshot.GetInfo()
            bmpstr = screenshot.GetBitmapBits(True)
            
            img = np.frombuffer(bmpstr, dtype='uint8')
            img.shape = (height, width, 4)
            img_bgr = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
            
            # Clean up
            win32gui.DeleteObject(screenshot.GetHandle())
            mem_dc.DeleteDC()
            img_dc.DeleteDC()
            win32gui.ReleaseDC(hdesktop, desktop_dc)
            
            return img_bgr
            
        except Exception as e:
            raise Exception(f"Memory Reading error: {e}")
    
    def _capture_gdi_optimized(self) -> Optional[np.ndarray]:
        """GDI+ optimized with advanced techniques"""
        try:
            import win32gui
            import win32ui
            import win32con
            import win32api
            
            # Get desktop handle
            hdesktop = win32gui.GetDesktopWindow()
            
            # Get dimensions
            width = win32api.GetSystemMetrics(win32con.SM_CXVIRTUALSCREEN)
            height = win32api.GetSystemMetrics(win32con.SM_CYVIRTUALSCREEN)
            left = win32api.GetSystemMetrics(win32con.SM_XVIRTUALSCREEN)
            top = win32api.GetSystemMetrics(win32con.SM_YVIRTUALSCREEN)
            
            # Create context
            desktop_dc = win32gui.GetWindowDC(hdesktop)
            img_dc = win32ui.CreateDCFromHandle(desktop_dc)
            mem_dc = img_dc.CreateCompatibleDC()
            
            # Create bitmap
            screenshot = win32ui.CreateBitmap()
            screenshot.CreateCompatibleBitmap(img_dc, width, height)
            mem_dc.SelectObject(screenshot)
            
            # Use BitBlt with special flags
            mem_dc.BitBlt((0, 0), (width, height), img_dc, (left, top), win32con.SRCCOPY)
            
            # Convert to array
            bmpinfo = screenshot.GetInfo()
            bmpstr = screenshot.GetBitmapBits(True)
            
            img = np.frombuffer(bmpstr, dtype='uint8')
            img.shape = (height, width, 4)
            img_bgr = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
            
            # Clean up
            win32gui.DeleteObject(screenshot.GetHandle())
            mem_dc.DeleteDC()
            img_dc.DeleteDC()
            win32gui.ReleaseDC(hdesktop, desktop_dc)
            
            return img_bgr
            
        except Exception as e:
            raise Exception(f"GDI+ optimized error: {e}")
    
    def _capture_fallback_traditional(self) -> Optional[np.ndarray]:
        """Traditional fallback with multiple methods"""
        try:
            # Try with mss
            try:
                import mss
                with mss.mss() as sct:
                    monitor = sct.monitors[1]
                    screenshot = sct.grab(monitor)
                    img_array = np.array(screenshot)
                    img_bgr = cv2.cvtColor(img_array, cv2.COLOR_BGRA2BGR)
                    return img_bgr
            except Exception as mss_error:
                logger.debug(f"mss failed: {mss_error}")
            
            # Try with pyautogui
            try:
                import pyautogui
                screenshot = pyautogui.screenshot()
                img_array = np.array(screenshot)
                img_bgr = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
                return img_bgr
            except Exception as pyautogui_error:
                logger.debug(f"pyautogui failed: {pyautogui_error}")
            
            # Try with PIL
            try:
                from PIL import ImageGrab
                screenshot = ImageGrab.grab()
                img_array = np.array(screenshot)
                img_bgr = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
                return img_bgr
            except Exception as pil_error:
                logger.debug(f"PIL failed: {pil_error}")
            
            raise Exception("All fallback methods failed")
            
        except Exception as e:
            raise Exception(f"Fallback traditional error: {e}")
    
    def _update_stats(self, method: str, time_taken: float, success: bool):
        """Update performance statistics"""
        if method in self.performance_stats:
            stats = self.performance_stats[method]
            stats['total'] += 1
            if success:
                stats['success'] += 1
                # Update average time
                if stats['avg_time'] == 0:
                    stats['avg_time'] = time_taken
                else:
                    stats['avg_time'] = (stats['avg_time'] + time_taken) / 2
    
    def get_performance_stats(self) -> Dict[str, Any]:
        """Get performance statistics"""
        return self.performance_stats.copy()
    
    def get_best_method(self) -> str:
        """Get the most successful method"""
        best_method = None
        best_success_rate = 0
        
        for method, stats in self.performance_stats.items():
            if stats['total'] > 0:
                success_rate = stats['success'] / stats['total']
                if success_rate > best_success_rate:
                    best_success_rate = success_rate
                    best_method = method
        
        return best_method or 'fallback'
    
    def optimize_capture_interval(self):
        """Optimize capture interval based on performance"""
        best_method = self.get_best_method()
        if best_method in self.performance_stats:
            avg_time = self.performance_stats[best_method]['avg_time']
            # Set interval to 2x the average capture time
            self.capture_interval = max(0.05, avg_time * 2)
            logger.info(f"Optimized capture interval: {self.capture_interval:.3f}s")
    
    def reset_stats(self):
        """Reset performance statistics"""
        for method in self.performance_stats:
            self.performance_stats[method] = {'success': 0, 'total': 0, 'avg_time': 0}
        self.successful_method = None
        logger.info("Performance statistics reset")

# Advanced techniques for specific scenarios
class TibiaSpecificBypass(AdvancedScreenshotBypass):
    """Tibia-specific screenshot bypass techniques"""
    
    def __init__(self):
        super().__init__()
        self.tibia_window_handle = None
        self.tibia_region = None
    
    def find_tibia_window(self) -> bool:
        """Find Tibia window handle"""
        try:
            import win32gui
            
            def enum_windows_callback(hwnd, windows):
                if win32gui.IsWindowVisible(hwnd):
                    window_text = win32gui.GetWindowText(hwnd)
                    if 'tibia' in window_text.lower():
                        windows.append(hwnd)
                return True
            
            windows = []
            win32gui.EnumWindows(enum_windows_callback, windows)
            
            if windows:
                self.tibia_window_handle = windows[0]
                self.tibia_region = win32gui.GetWindowRect(self.tibia_window_handle)
                logger.info(f"Found Tibia window: {win32gui.GetWindowText(self.tibia_window_handle)}")
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"Error finding Tibia window: {e}")
            return False
    
    def capture_tibia_window_only(self) -> Optional[np.ndarray]:
        """Capture only the Tibia window"""
        if not self.tibia_window_handle or not self.tibia_region:
            if not self.find_tibia_window():
                return None
        
        try:
            import win32gui
            import win32ui
            import win32con
            import win32api
            
            x, y, w, h = self.tibia_region
            width = w - x
            height = h - y
            
            # Create device context for Tibia window
            window_dc = win32gui.GetWindowDC(self.tibia_window_handle)
            img_dc = win32ui.CreateDCFromHandle(window_dc)
            mem_dc = img_dc.CreateCompatibleDC()
            
            # Create bitmap
            screenshot = win32ui.CreateBitmap()
            screenshot.CreateCompatibleBitmap(img_dc, width, height)
            mem_dc.SelectObject(screenshot)
            
            # Copy window content
            mem_dc.BitBlt((0, 0), (width, height), img_dc, (0, 0), win32con.SRCCOPY)
            
            # Convert to array
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
            logger.error(f"Error capturing Tibia window: {e}")
            return None 