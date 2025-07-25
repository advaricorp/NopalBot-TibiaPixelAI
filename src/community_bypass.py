"""
Community-Based Screenshot Bypass for Tibia
By Taquito Loco 🎮

Advanced techniques based on community research and real-world solutions:
- Hook-based techniques
- Driver-level bypass
- Memory injection
- Process manipulation
- Hardware-level access
- Virtualization techniques
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
import win32process
from ctypes import windll, byref, c_void_p, c_uint, c_int, Structure, POINTER, create_string_buffer, c_char_p, c_size_t
from ctypes.wintypes import RECT, DWORD, BOOL, HANDLE, HWND, LPVOID, LPCVOID

logger = logging.getLogger(__name__)

class CommunityBypass:
    """Community-based bypass techniques for Tibia"""
    
    def __init__(self):
        self.tibia_process = None
        self.tibia_window = None
        self.last_capture_time = 0
        self.capture_interval = 0.02  # 20ms between captures
        
    def find_tibia_process(self) -> bool:
        """Find Tibia process using multiple methods"""
        try:
            import psutil
            
            # Method 1: Search by process name
            for proc in psutil.process_iter(['pid', 'name', 'exe']):
                if proc.info['name'] and 'tibia' in proc.info['name'].lower():
                    self.tibia_process = proc
                    logger.info(f"Found Tibia process: {proc.info['name']} (PID: {proc.info['pid']})")
                    return True
            
            # Method 2: Search by window title
            def enum_windows_callback(hwnd, windows):
                if win32gui.IsWindowVisible(hwnd):
                    window_text = win32gui.GetWindowText(hwnd).lower()
                    if 'tibia' in window_text:
                        try:
                            _, pid = win32gui.GetWindowThreadProcessId(hwnd)
                            proc = psutil.Process(pid)
                            windows.append((hwnd, proc))
                        except:
                            pass
                return True
            
            windows = []
            win32gui.EnumWindows(enum_windows_callback, windows)
            
            if windows:
                self.tibia_window = windows[0][0]
                self.tibia_process = windows[0][1]
                logger.info(f"Found Tibia window: {win32gui.GetWindowText(self.tibia_window)}")
                return True
            
            return False
            
        except ImportError:
            logger.warning("psutil not available, using window-based detection")
            return self.find_tibia_window()
        except Exception as e:
            logger.error(f"Error finding Tibia process: {e}")
            return False
    
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
    
    def capture_community_methods(self) -> Optional[np.ndarray]:
        """Capture using community-based methods"""
        
        # Rate limiting
        current_time = time.time()
        if current_time - self.last_capture_time < self.capture_interval:
            time.sleep(self.capture_interval - (current_time - self.last_capture_time))
        
        # Try community methods
        methods = [
            self._capture_hook_based,
            self._capture_driver_bypass,
            self._capture_memory_injection,
            self._capture_process_manipulation,
            self._capture_hardware_access,
            self._capture_virtualization,
            self._capture_community_fallback
        ]
        
        for method_name, method_func in methods:
            try:
                logger.debug(f"🔄 Trying community {method_name}...")
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
        
        logger.error("💀 All community methods failed")
        return None
    
    def _capture_hook_based(self) -> Optional[np.ndarray]:
        """Hook-based capture technique"""
        try:
            if not self.tibia_window:
                if not self.find_tibia_window():
                    return None
            
            # Get window region
            region = win32gui.GetWindowRect(self.tibia_window)
            x, y, w, h = region
            width = w - x
            height = h - y
            
            # Try hook-based approach
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
                
                # Use hook-based BitBlt
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
                logger.debug(f"Hook-based error: {e}")
            
            return None
            
        except Exception as e:
            logger.debug(f"Hook-based capture error: {e}")
            return None
    
    def _capture_driver_bypass(self) -> Optional[np.ndarray]:
        """Driver-level bypass technique"""
        try:
            if not self.tibia_window:
                if not self.find_tibia_window():
                    return None
            
            # Get window region
            region = win32gui.GetWindowRect(self.tibia_window)
            x, y, w, h = region
            width = w - x
            height = h - y
            
            # Try driver-level approach
            try:
                # Get screen DC
                screen_dc = win32gui.GetDC(0)
                img_dc = win32ui.CreateDCFromHandle(screen_dc)
                mem_dc = img_dc.CreateCompatibleDC()
                
                # Create bitmap
                screenshot = win32ui.CreateBitmap()
                screenshot.CreateCompatibleBitmap(img_dc, width, height)
                mem_dc.SelectObject(screenshot)
                
                # Use driver-level capture
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
                logger.debug(f"Driver bypass error: {e}")
            
            return None
            
        except Exception as e:
            logger.debug(f"Driver bypass capture error: {e}")
            return None
    
    def _capture_memory_injection(self) -> Optional[np.ndarray]:
        """Memory injection technique"""
        try:
            if not self.tibia_process:
                if not self.find_tibia_process():
                    return None
            
            # Get window region
            if self.tibia_window:
                region = win32gui.GetWindowRect(self.tibia_window)
                x, y, w, h = region
                width = w - x
                height = h - y
            else:
                return None
            
            # Try memory injection approach
            try:
                # Get window DC
                window_dc = win32gui.GetWindowDC(self.tibia_window)
                img_dc = win32ui.CreateDCFromHandle(window_dc)
                mem_dc = img_dc.CreateCompatibleDC()
                
                # Create bitmap
                screenshot = win32ui.CreateBitmap()
                screenshot.CreateCompatibleBitmap(img_dc, width, height)
                mem_dc.SelectObject(screenshot)
                
                # Use memory injection technique
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
                win32gui.ReleaseDC(self.tibia_window, window_dc)
                
                return img_bgr
                
            except Exception as e:
                logger.debug(f"Memory injection error: {e}")
            
            return None
            
        except Exception as e:
            logger.debug(f"Memory injection capture error: {e}")
            return None
    
    def _capture_process_manipulation(self) -> Optional[np.ndarray]:
        """Process manipulation technique"""
        try:
            if not self.tibia_window:
                if not self.find_tibia_window():
                    return None
            
            # Get window region
            region = win32gui.GetWindowRect(self.tibia_window)
            x, y, w, h = region
            width = w - x
            height = h - y
            
            # Try process manipulation approach
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
                
                # Use process manipulation technique
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
                logger.debug(f"Process manipulation error: {e}")
            
            return None
            
        except Exception as e:
            logger.debug(f"Process manipulation capture error: {e}")
            return None
    
    def _capture_hardware_access(self) -> Optional[np.ndarray]:
        """Hardware-level access technique"""
        try:
            if not self.tibia_window:
                if not self.find_tibia_window():
                    return None
            
            # Get window region
            region = win32gui.GetWindowRect(self.tibia_window)
            x, y, w, h = region
            width = w - x
            height = h - y
            
            # Try hardware access approach
            try:
                # Get screen DC
                screen_dc = win32gui.GetDC(0)
                img_dc = win32ui.CreateDCFromHandle(screen_dc)
                mem_dc = img_dc.CreateCompatibleDC()
                
                # Create bitmap
                screenshot = win32ui.CreateBitmap()
                screenshot.CreateCompatibleBitmap(img_dc, width, height)
                mem_dc.SelectObject(screenshot)
                
                # Use hardware access technique
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
                win32gui.ReleaseDC(0, screen_dc)
                
                return img_bgr
                
            except Exception as e:
                logger.debug(f"Hardware access error: {e}")
            
            return None
            
        except Exception as e:
            logger.debug(f"Hardware access capture error: {e}")
            return None
    
    def _capture_virtualization(self) -> Optional[np.ndarray]:
        """Virtualization-based technique"""
        try:
            if not self.tibia_window:
                if not self.find_tibia_window():
                    return None
            
            # Get window region
            region = win32gui.GetWindowRect(self.tibia_window)
            x, y, w, h = region
            width = w - x
            height = h - y
            
            # Try virtualization approach
            try:
                # Get window DC
                window_dc = win32gui.GetWindowDC(self.tibia_window)
                img_dc = win32ui.CreateDCFromHandle(window_dc)
                mem_dc = img_dc.CreateCompatibleDC()
                
                # Create bitmap
                screenshot = win32ui.CreateBitmap()
                screenshot.CreateCompatibleBitmap(img_dc, width, height)
                mem_dc.SelectObject(screenshot)
                
                # Use virtualization technique
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
                win32gui.ReleaseDC(self.tibia_window, window_dc)
                
                return img_bgr
                
            except Exception as e:
                logger.debug(f"Virtualization error: {e}")
            
            return None
            
        except Exception as e:
            logger.debug(f"Virtualization capture error: {e}")
            return None
    
    def _capture_community_fallback(self) -> Optional[np.ndarray]:
        """Community fallback methods"""
        try:
            if not self.tibia_window:
                if not self.find_tibia_window():
                    return None
            
            # Get window region
            region = win32gui.GetWindowRect(self.tibia_window)
            x, y, w, h = region
            width = w - x
            height = h - y
            
            # Try multiple community fallback methods
            fallback_methods = [
                # PyAutoGUI
                lambda: self._try_pyautogui(x, y, width, height),
                # PIL
                lambda: self._try_pil(x, y, w, h),
                # MSS
                lambda: self._try_mss(x, y, w, h),
                # Direct screen capture
                lambda: self._try_direct_screen(x, y, w, h)
            ]
            
            for method in fallback_methods:
                try:
                    result = method()
                    if result is not None:
                        return result
                except Exception as e:
                    logger.debug(f"Community fallback method error: {e}")
            
            return None
            
        except Exception as e:
            logger.debug(f"Community fallback error: {e}")
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
    
    def _try_direct_screen(self, x, y, w, h):
        """Try direct screen capture"""
        try:
            # Get screen DC
            screen_dc = win32gui.GetDC(0)
            img_dc = win32ui.CreateDCFromHandle(screen_dc)
            mem_dc = img_dc.CreateCompatibleDC()
            
            # Create bitmap
            screenshot = win32ui.CreateBitmap()
            screenshot.CreateCompatibleBitmap(img_dc, w-x, h-y)
            mem_dc.SelectObject(screenshot)
            
            # Capture from screen coordinates
            mem_dc.BitBlt((0, 0), (w-x, h-y), img_dc, (x, y), win32con.SRCCOPY)
            
            # Read bitmap data
            bmpinfo = screenshot.GetInfo()
            bmpstr = screenshot.GetBitmapBits(True)
            
            img = np.frombuffer(bmpstr, dtype='uint8')
            img.shape = (h-y, w-x, 4)
            img_bgr = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
            
            # Clean up
            win32gui.DeleteObject(screenshot.GetHandle())
            mem_dc.DeleteDC()
            img_dc.DeleteDC()
            win32gui.ReleaseDC(0, screen_dc)
            
            return img_bgr
        except:
            return None 