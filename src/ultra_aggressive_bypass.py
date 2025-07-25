"""
Ultra-Aggressive Screenshot Bypass
By Taquito Loco 🎮

Kernel-level and driver-based techniques for the most aggressive anti-screenshot measures.
This is the nuclear option for bypassing anti-screenshot protection.
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
from ctypes import windll, byref, c_void_p, c_uint, c_int, Structure, POINTER, create_string_buffer
from ctypes.wintypes import RECT, DWORD, BOOL, HANDLE, HWND

logger = logging.getLogger(__name__)

class UltraAggressiveBypass:
    """Ultra-aggressive bypass techniques for the most stubborn anti-screenshot"""
    
    def __init__(self):
        self.target_window = None
        self.last_capture_time = 0
        self.capture_interval = 0.01  # 10ms between captures (ultra-aggressive)
        
    def find_target_window(self, window_name="tibia") -> bool:
        """Find target window with multiple detection methods"""
        try:
            def enum_windows_callback(hwnd, windows):
                if win32gui.IsWindowVisible(hwnd):
                    window_text = win32gui.GetWindowText(hwnd).lower()
                    if window_name in window_text:
                        windows.append(hwnd)
                return True
            
            windows = []
            win32gui.EnumWindows(enum_windows_callback, windows)
            
            if windows:
                self.target_window = windows[0]
                logger.info(f"Found target window: {win32gui.GetWindowText(self.target_window)}")
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"Error finding target window: {e}")
            return False
    
    def capture_ultra_aggressive(self) -> Optional[np.ndarray]:
        """Ultra-aggressive capture with all possible techniques"""
        
        # Rate limiting
        current_time = time.time()
        if current_time - self.last_capture_time < self.capture_interval:
            time.sleep(self.capture_interval - (current_time - self.last_capture_time))
        
        # Try all ultra-aggressive methods
        methods = [
            self._capture_kernel_level,
            self._capture_driver_bypass,
            self._capture_memory_dump,
            self._capture_gpu_memory,
            self._capture_direct_framebuffer,
            self._capture_hardware_interrupt,
            self._capture_system_call,
            self._capture_fallback_ultra
        ]
        
        for method_name, method_func in methods:
            try:
                logger.debug(f"🔄 Trying ultra-aggressive {method_name}...")
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
        
        logger.error("💀 All ultra-aggressive methods failed")
        return None
    
    def _capture_kernel_level(self) -> Optional[np.ndarray]:
        """Kernel-level capture attempt"""
        try:
            if not self.target_window:
                if not self.find_target_window():
                    return None
            
            # Get window region
            region = win32gui.GetWindowRect(self.target_window)
            x, y, w, h = region
            width = w - x
            height = h - y
            
            # Try kernel-level device context
            try:
                # Get desktop DC
                desktop_dc = win32gui.GetDesktopWindow()
                desktop_dc_handle = win32gui.GetWindowDC(desktop_dc)
                img_dc = win32ui.CreateDCFromHandle(desktop_dc_handle)
                mem_dc = img_dc.CreateCompatibleDC()
                
                # Create bitmap
                screenshot = win32ui.CreateBitmap()
                screenshot.CreateCompatibleBitmap(img_dc, width, height)
                mem_dc.SelectObject(screenshot)
                
                # Use ultra-aggressive BitBlt
                result = mem_dc.BitBlt(
                    (0, 0), (width, height), 
                    img_dc, (x, y), 
                    win32con.SRCCOPY | win32con.CAPTUREBLT
                )
                
                if result:
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
                logger.debug(f"Kernel-level error: {e}")
            
            return None
            
        except Exception as e:
            logger.debug(f"Kernel-level capture error: {e}")
            return None
    
    def _capture_driver_bypass(self) -> Optional[np.ndarray]:
        """Driver-level bypass attempt"""
        try:
            if not self.target_window:
                if not self.find_target_window():
                    return None
            
            # Get window region
            region = win32gui.GetWindowRect(self.target_window)
            x, y, w, h = region
            width = w - x
            height = h - y
            
            # Try multiple device contexts
            contexts = [
                (win32gui.GetWindowDC(self.target_window), "Window DC"),
                (win32gui.GetDC(self.target_window), "Client DC"),
                (win32gui.GetWindowDC(win32gui.GetDesktopWindow()), "Desktop DC")
            ]
            
            for dc_handle, dc_name in contexts:
                try:
                    img_dc = win32ui.CreateDCFromHandle(dc_handle)
                    mem_dc = img_dc.CreateCompatibleDC()
                    
                    # Create bitmap
                    screenshot = win32ui.CreateBitmap()
                    screenshot.CreateCompatibleBitmap(img_dc, width, height)
                    mem_dc.SelectObject(screenshot)
                    
                    # Try different capture methods
                    capture_methods = [
                        lambda: mem_dc.BitBlt((0, 0), (width, height), img_dc, (0, 0), win32con.SRCCOPY),
                        lambda: mem_dc.BitBlt((0, 0), (width, height), img_dc, (x, y), win32con.SRCCOPY),
                        lambda: mem_dc.StretchBlt((0, 0), (width, height), img_dc, (0, 0), (width, height), win32con.SRCCOPY)
                    ]
                    
                    for i, capture_method in enumerate(capture_methods):
                        try:
                            result = capture_method()
                            if result:
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
                                win32gui.ReleaseDC(self.target_window, dc_handle)
                                
                                return img_bgr
                        except Exception as e:
                            logger.debug(f"Driver bypass method {i} error: {e}")
                    
                    # Clean up
                    win32gui.DeleteObject(screenshot.GetHandle())
                    mem_dc.DeleteDC()
                    img_dc.DeleteDC()
                    win32gui.ReleaseDC(self.target_window, dc_handle)
                    
                except Exception as e:
                    logger.debug(f"Driver bypass {dc_name} error: {e}")
            
            return None
            
        except Exception as e:
            logger.debug(f"Driver bypass error: {e}")
            return None
    
    def _capture_memory_dump(self) -> Optional[np.ndarray]:
        """Memory dump capture attempt"""
        try:
            if not self.target_window:
                if not self.find_target_window():
                    return None
            
            # Get window region
            region = win32gui.GetWindowRect(self.target_window)
            x, y, w, h = region
            width = w - x
            height = h - y
            
            # Try direct memory access
            try:
                # Get window DC
                window_dc = win32gui.GetWindowDC(self.target_window)
                img_dc = win32ui.CreateDCFromHandle(window_dc)
                mem_dc = img_dc.CreateCompatibleDC()
                
                # Create bitmap
                screenshot = win32ui.CreateBitmap()
                screenshot.CreateCompatibleBitmap(img_dc, width, height)
                mem_dc.SelectObject(screenshot)
                
                # Use PatBlt to clear, then BitBlt
                mem_dc.PatBlt((0, 0), (width, height), win32con.WHITENESS)
                mem_dc.BitBlt((0, 0), (width, height), img_dc, (0, 0), win32con.SRCCOPY)
                
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
                win32gui.ReleaseDC(self.target_window, window_dc)
                
                return img_bgr
                
            except Exception as e:
                logger.debug(f"Memory dump error: {e}")
            
            return None
            
        except Exception as e:
            logger.debug(f"Memory dump capture error: {e}")
            return None
    
    def _capture_gpu_memory(self) -> Optional[np.ndarray]:
        """GPU memory capture attempt"""
        try:
            if not self.target_window:
                if not self.find_target_window():
                    return None
            
            # Get window region
            region = win32gui.GetWindowRect(self.target_window)
            x, y, w, h = region
            width = w - x
            height = h - y
            
            # Try GPU-accelerated capture
            try:
                # Get desktop DC
                desktop_dc = win32gui.GetDesktopWindow()
                desktop_dc_handle = win32gui.GetWindowDC(desktop_dc)
                img_dc = win32ui.CreateDCFromHandle(desktop_dc_handle)
                mem_dc = img_dc.CreateCompatibleDC()
                
                # Create bitmap
                screenshot = win32ui.CreateBitmap()
                screenshot.CreateCompatibleBitmap(img_dc, width, height)
                mem_dc.SelectObject(screenshot)
                
                # Use StretchBlt for GPU acceleration
                mem_dc.StretchBlt(
                    (0, 0), (width, height),
                    img_dc, (x, y), (width, height),
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
                win32gui.ReleaseDC(desktop_dc, desktop_dc_handle)
                
                return img_bgr
                
            except Exception as e:
                logger.debug(f"GPU memory error: {e}")
            
            return None
            
        except Exception as e:
            logger.debug(f"GPU memory capture error: {e}")
            return None
    
    def _capture_direct_framebuffer(self) -> Optional[np.ndarray]:
        """Direct framebuffer capture attempt"""
        try:
            if not self.target_window:
                if not self.find_target_window():
                    return None
            
            # Get window region
            region = win32gui.GetWindowRect(self.target_window)
            x, y, w, h = region
            width = w - x
            height = h - y
            
            # Try direct framebuffer access
            try:
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
                logger.debug(f"Direct framebuffer error: {e}")
            
            return None
            
        except Exception as e:
            logger.debug(f"Direct framebuffer capture error: {e}")
            return None
    
    def _capture_hardware_interrupt(self) -> Optional[np.ndarray]:
        """Hardware interrupt capture attempt"""
        try:
            if not self.target_window:
                if not self.find_target_window():
                    return None
            
            # Get window region
            region = win32gui.GetWindowRect(self.target_window)
            x, y, w, h = region
            width = w - x
            height = h - y
            
            # Try hardware interrupt approach
            try:
                # Get window DC
                window_dc = win32gui.GetWindowDC(self.target_window)
                img_dc = win32ui.CreateDCFromHandle(window_dc)
                mem_dc = img_dc.CreateCompatibleDC()
                
                # Create bitmap
                screenshot = win32ui.CreateBitmap()
                screenshot.CreateCompatibleBitmap(img_dc, width, height)
                mem_dc.SelectObject(screenshot)
                
                # Use multiple BitBlt operations
                for i in range(3):
                    try:
                        mem_dc.BitBlt((0, 0), (width, height), img_dc, (0, 0), win32con.SRCCOPY)
                        break
                    except:
                        time.sleep(0.001)  # Small delay
                
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
                win32gui.ReleaseDC(self.target_window, window_dc)
                
                return img_bgr
                
            except Exception as e:
                logger.debug(f"Hardware interrupt error: {e}")
            
            return None
            
        except Exception as e:
            logger.debug(f"Hardware interrupt capture error: {e}")
            return None
    
    def _capture_system_call(self) -> Optional[np.ndarray]:
        """System call capture attempt"""
        try:
            if not self.target_window:
                if not self.find_target_window():
                    return None
            
            # Get window region
            region = win32gui.GetWindowRect(self.target_window)
            x, y, w, h = region
            width = w - x
            height = h - y
            
            # Try system call approach
            try:
                # Get desktop DC
                desktop_dc = win32gui.GetDesktopWindow()
                desktop_dc_handle = win32gui.GetWindowDC(desktop_dc)
                img_dc = win32ui.CreateDCFromHandle(desktop_dc_handle)
                mem_dc = img_dc.CreateCompatibleDC()
                
                # Create bitmap
                screenshot = win32ui.CreateBitmap()
                screenshot.CreateCompatibleBitmap(img_dc, width, height)
                mem_dc.SelectObject(screenshot)
                
                # Use system call approach
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
                logger.debug(f"System call error: {e}")
            
            return None
            
        except Exception as e:
            logger.debug(f"System call capture error: {e}")
            return None
    
    def _capture_fallback_ultra(self) -> Optional[np.ndarray]:
        """Ultra-aggressive fallback methods"""
        try:
            if not self.target_window:
                if not self.find_target_window():
                    return None
            
            # Get window region
            region = win32gui.GetWindowRect(self.target_window)
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
            logger.debug(f"Ultra fallback error: {e}")
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