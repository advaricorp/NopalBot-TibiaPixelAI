# 🚀 OBS + Matrix Hybrid Bypass
# Combinando técnicas de TibiaAuto12 y PyTibia

import cv2
import numpy as np
import time
import threading
from typing import Optional, Tuple
import win32gui
import win32ui
import win32con
import win32api
import mss
import mss.tools
from concurrent.futures import ThreadPoolExecutor
import logging

class OBSMatrixBypass:
    """
    Hybrid bypass combining OBS Game Capture (TibiaAuto12) 
    with Matrix-based processing (PyTibia)
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.executor = ThreadPoolExecutor(max_workers=4)
        self.capture_cache = {}
        self.last_capture_time = 0
        self.capture_interval = 0.016  # 60 FPS
        
        # Matrix processing parameters
        self.matrix_size = (1920, 1080)
        self.parallel_captures = 4
        
        # OBS integration
        self.obs_window = None
        self.game_window = None
        
    def find_obs_window(self) -> Optional[int]:
        """Find OBS Studio window for game capture"""
        def enum_windows_callback(hwnd, windows):
            if win32gui.IsWindowVisible(hwnd):
                window_text = win32gui.GetWindowText(hwnd)
                if "OBS Studio" in window_text and "Game Capture" in window_text:
                    windows.append(hwnd)
            return True
        
        windows = []
        win32gui.EnumWindows(enum_windows_callback, windows)
        return windows[0] if windows else None
    
    def find_tibia_window(self) -> Optional[int]:
        """Find Tibia client window"""
        def enum_windows_callback(hwnd, windows):
            if win32gui.IsWindowVisible(hwnd):
                window_text = win32gui.GetWindowText(hwnd)
                if "Tibia" in window_text:
                    windows.append(hwnd)
            return True
        
        windows = []
        win32gui.EnumWindows(enum_windows_callback, windows)
        return windows[0] if windows else None
    
    def setup_obs_capture(self) -> bool:
        """Setup OBS Game Capture for Tibia"""
        try:
            self.obs_window = self.find_obs_window()
            self.game_window = self.find_tibia_window()
            
            if not self.obs_window or not self.game_window:
                self.logger.error("❌ OBS or Tibia window not found")
                return False
            
            self.logger.info(f"✅ OBS Window: {self.obs_window}")
            self.logger.info(f"✅ Tibia Window: {self.game_window}")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ OBS setup failed: {e}")
            return False
    
    def capture_matrix_parallel(self) -> Optional[np.ndarray]:
        """Matrix-based parallel capture (PyTibia style)"""
        try:
            # Rate limiting
            current_time = time.time()
            if current_time - self.last_capture_time < self.capture_interval:
                time.sleep(self.capture_interval - (current_time - self.last_capture_time))
            
            # Parallel capture methods
            capture_methods = [
                self._capture_matrix_direct,
                self._capture_matrix_obs,
                self._capture_matrix_mss,
                self._capture_matrix_win32
            ]
            
            # Execute captures in parallel
            futures = []
            for method in capture_methods:
                future = self.executor.submit(method)
                futures.append(future)
            
            # Get first successful result
            for future in futures:
                try:
                    result = future.result(timeout=0.1)
                    if result is not None:
                        self.last_capture_time = time.time()
                        return result
                except Exception as e:
                    self.logger.debug(f"Capture method failed: {e}")
                    continue
            
            return None
            
        except Exception as e:
            self.logger.error(f"❌ Matrix capture failed: {e}")
            return None
    
    def _capture_matrix_direct(self) -> Optional[np.ndarray]:
        """Direct matrix capture (PyTibia approach)"""
        try:
            if not self.game_window:
                return None
            
            # Get window dimensions
            rect = win32gui.GetWindowRect(self.game_window)
            x, y, w, h = rect[0], rect[1], rect[2] - rect[0], rect[3] - rect[1]
            
            # Create device context
            hwndDC = win32gui.GetWindowDC(self.game_window)
            mfcDC = win32ui.CreateDCFromHandle(hwndDC)
            saveDC = mfcDC.CreateCompatibleDC()
            
            # Create bitmap
            saveBitMap = win32ui.CreateBitmap()
            saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)
            saveDC.SelectObject(saveBitMap)
            
            # Copy window content
            result = saveDC.BitBlt((0, 0), (w, h), mfcDC, (0, 0), win32con.SRCCOPY)
            
            if result:
                # Convert to numpy array
                bmpinfo = saveBitMap.GetInfo()
                bmpstr = saveBitMap.GetBitmapBits(True)
                
                # Create matrix directly
                img = np.frombuffer(bmpstr, dtype='uint8')
                img.shape = (h, w, 4)
                
                # Convert BGRA to BGR
                img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
                
                # Cleanup
                win32gui.DeleteObject(saveBitMap.GetHandle())
                saveDC.DeleteDC()
                mfcDC.DeleteDC()
                win32gui.ReleaseDC(self.game_window, hwndDC)
                
                return img
            
            return None
            
        except Exception as e:
            self.logger.debug(f"Direct matrix capture failed: {e}")
            return None
    
    def _capture_matrix_obs(self) -> Optional[np.ndarray]:
        """OBS Game Capture method (TibiaAuto12 approach)"""
        try:
            if not self.obs_window:
                return None
            
            # Capture OBS window (which contains Tibia)
            with mss.mss() as sct:
                # Get OBS window position
                rect = win32gui.GetWindowRect(self.obs_window)
                
                # Capture OBS region
                monitor = {
                    "top": rect[1],
                    "left": rect[0],
                    "width": rect[2] - rect[0],
                    "height": rect[3] - rect[1]
                }
                
                screenshot = sct.grab(monitor)
                
                # Convert to numpy array
                img = np.array(screenshot)
                img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
                
                return img
                
        except Exception as e:
            self.logger.debug(f"OBS capture failed: {e}")
            return None
    
    def _capture_matrix_mss(self) -> Optional[np.ndarray]:
        """MSS-based matrix capture"""
        try:
            if not self.game_window:
                return None
            
            with mss.mss() as sct:
                # Get Tibia window position
                rect = win32gui.GetWindowRect(self.game_window)
                
                monitor = {
                    "top": rect[1],
                    "left": rect[0],
                    "width": rect[2] - rect[0],
                    "height": rect[3] - rect[1]
                }
                
                screenshot = sct.grab(monitor)
                img = np.array(screenshot)
                img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
                
                return img
                
        except Exception as e:
            self.logger.debug(f"MSS capture failed: {e}")
            return None
    
    def _capture_matrix_win32(self) -> Optional[np.ndarray]:
        """Win32-based matrix capture"""
        try:
            if not self.game_window:
                return None
            
            # Get window DC
            hwndDC = win32gui.GetWindowDC(self.game_window)
            mfcDC = win32ui.CreateDCFromHandle(hwndDC)
            saveDC = mfcDC.CreateCompatibleDC()
            
            # Get window size
            rect = win32gui.GetWindowRect(self.game_window)
            w, h = rect[2] - rect[0], rect[3] - rect[1]
            
            # Create bitmap
            saveBitMap = win32ui.CreateBitmap()
            saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)
            saveDC.SelectObject(saveBitMap)
            
            # Copy window
            saveDC.BitBlt((0, 0), (w, h), mfcDC, (0, 0), win32con.SRCCOPY)
            
            # Get bitmap data
            bmpinfo = saveBitMap.GetInfo()
            bmpstr = saveBitMap.GetBitmapBits(True)
            
            # Convert to matrix
            img = np.frombuffer(bmpstr, dtype='uint8')
            img.shape = (h, w, 4)
            img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
            
            # Cleanup
            win32gui.DeleteObject(saveBitMap.GetHandle())
            saveDC.DeleteDC()
            mfcDC.DeleteDC()
            win32gui.ReleaseDC(self.game_window, hwndDC)
            
            return img
            
        except Exception as e:
            self.logger.debug(f"Win32 capture failed: {e}")
            return None
    
    def preprocess_matrix(self, img: np.ndarray) -> np.ndarray:
        """Pre-process matrix for optimal performance (PyTibia style)"""
        try:
            # Resize to standard matrix size
            if img.shape[:2] != self.matrix_size[::-1]:
                img = cv2.resize(img, self.matrix_size)
            
            # Optimize matrix operations
            img = img.astype(np.float32) / 255.0
            
            # Apply matrix optimizations
            # - Normalize
            # - Apply filters if needed
            # - Optimize for matrix calculations
            
            return img
            
        except Exception as e:
            self.logger.error(f"❌ Matrix preprocessing failed: {e}")
            return img
    
    def analyze_matrix_performance(self, img: np.ndarray) -> dict:
        """Analyze matrix performance metrics (PyTibia style)"""
        try:
            start_time = time.time()
            
            # Matrix calculations
            mean_brightness = np.mean(img)
            std_dev = np.std(img)
            edge_density = np.sum(cv2.Canny(img, 50, 150)) / (img.shape[0] * img.shape[1])
            
            processing_time = time.time() - start_time
            
            return {
                'mean_brightness': mean_brightness,
                'std_dev': std_dev,
                'edge_density': edge_density,
                'processing_time': processing_time,
                'matrix_size': img.shape,
                'fps': 1.0 / processing_time if processing_time > 0 else 0
            }
            
        except Exception as e:
            self.logger.error(f"❌ Matrix analysis failed: {e}")
            return {}
    
    def capture_with_analysis(self) -> Tuple[Optional[np.ndarray], dict]:
        """Capture with performance analysis"""
        try:
            # Capture matrix
            img = self.capture_matrix_parallel()
            
            if img is not None:
                # Preprocess
                processed_img = self.preprocess_matrix(img)
                
                # Analyze performance
                analysis = self.analyze_matrix_performance(processed_img)
                
                return processed_img, analysis
            else:
                return None, {}
                
        except Exception as e:
            self.logger.error(f"❌ Capture with analysis failed: {e}")
            return None, {}

# Usage example
def test_obs_matrix_bypass():
    """Test the hybrid bypass system"""
    bypass = OBSMatrixBypass()
    
    # Setup OBS capture
    if bypass.setup_obs_capture():
        print("✅ OBS Matrix Bypass setup successful")
        
        # Test capture
        for i in range(5):
            img, analysis = bypass.capture_with_analysis()
            
            if img is not None:
                print(f"✅ Capture {i+1} successful")
                print(f"📊 Analysis: {analysis}")
                
                # Save test image
                cv2.imwrite(f"test_capture_{i+1}.png", img)
            else:
                print(f"❌ Capture {i+1} failed")
            
            time.sleep(0.1)
    else:
        print("❌ OBS Matrix Bypass setup failed")

if __name__ == "__main__":
    test_obs_matrix_bypass() 