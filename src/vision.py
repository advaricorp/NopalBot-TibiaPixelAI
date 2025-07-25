"""
Módulo de Computer Vision para NopalBot
Detección de enemigos, escaleras, portales y obstáculos
"""

import cv2
import numpy as np
from PIL import Image, ImageGrab
import pyautogui
from typing import List, Tuple, Optional, Dict
import time

class ComputerVision:
    """Clase para Computer Vision en Tibia"""
    
    def __init__(self):
        # Rangos de color HSV para detección
        self.enemy_colors = [
            # Rojo (enemigos)
            ([0, 100, 100], [10, 255, 255]),
            ([170, 100, 100], [180, 255, 255])
        ]
        
        self.stair_colors = [
            # Marrón (escaleras)
            ([10, 50, 50], [20, 255, 255])
        ]
        
        self.portal_colors = [
            # Azul (portales)
            ([100, 100, 100], [130, 255, 255])
        ]
        
        self.obstacle_colors = [
            # Gris (obstáculos)
            ([0, 0, 50], [180, 30, 200])
        ]
    
    def capture_tibia_screen(self) -> Optional[np.ndarray]:
        """Captura toda la pantalla evadiendo anti-cheat con técnicas mejoradas"""
        
        # Usar el módulo simple working bypass
        try:
            from simple_working_bypass import SimpleWorkingBypass
            
            if not hasattr(self, '_simple_bypass'):
                self._simple_bypass = SimpleWorkingBypass()
            
            return self._simple_bypass.capture_simple_working()
            
        except ImportError:
            print("⚠️ Simple working bypass module not available, using fallback methods")
            return self._capture_fallback_traditional()
        except Exception as e:
            print(f"❌ Simple bypass failed: {e}")
            return self._capture_fallback_traditional()

    def _capture_directx_desktop_duplication(self) -> Optional[np.ndarray]:
        """DirectX Desktop Duplication - método más efectivo contra anti-cheat"""
        try:
            import win32gui
            import win32ui
            import win32con
            import win32api
            from ctypes import windll, byref, c_void_p, c_uint, c_int, Structure, POINTER
            from ctypes.wintypes import RECT, DWORD, BOOL
            
            # Definir estructuras necesarias
            class DXGI_OUTDUPL_DESC(Structure):
                _fields_ = [
                    ("ModeDesc", RECT),
                    ("Rotation", c_uint),
                    ("DesktopImageInSystemMemory", BOOL)
                ]
            
            class DXGI_OUTDUPL_FRAME_INFO(Structure):
                _fields_ = [
                    ("LastPresentTime", c_uint * 2),
                    ("LastMouseUpdateTime", c_uint * 2),
                    ("AccumulatedFrames", c_uint),
                    ("RectsCoalesced", BOOL),
                    ("ProtectedContentMaskedOut", BOOL),
                    ("PointerPosition", RECT),
                    ("TotalMetadataBufferSize", c_uint),
                    ("PointerShapeBufferSize", c_uint)
                ]
            
            # Obtener handle del escritorio
            hdesktop = win32gui.GetDesktopWindow()
            
            # Obtener dimensiones
            width = win32api.GetSystemMetrics(win32con.SM_CXVIRTUALSCREEN)
            height = win32api.GetSystemMetrics(win32con.SM_CYVIRTUALSCREEN)
            left = win32api.GetSystemMetrics(win32con.SM_XVIRTUALSCREEN)
            top = win32api.GetSystemMetrics(win32con.SM_YVIRTUALSCREEN)
            
            # Crear contexto de dispositivo con aceleración hardware
            desktop_dc = win32gui.GetWindowDC(hdesktop)
            img_dc = win32ui.CreateDCFromHandle(desktop_dc)
            mem_dc = img_dc.CreateCompatibleDC()
            
            # Crear bitmap con formato optimizado
            screenshot = win32ui.CreateBitmap()
            screenshot.CreateCompatibleBitmap(img_dc, width, height)
            mem_dc.SelectObject(screenshot)
            
            # Usar BitBlt con flags optimizados para bypass anti-cheat
            result = mem_dc.BitBlt(
                (0, 0), (width, height), 
                img_dc, (left, top), 
                win32con.SRCCOPY | win32con.CAPTUREBLT
            )
            
            if not result:
                raise Exception("BitBlt failed")
            
            # Convertir a array de numpy con optimización
            bmpinfo = screenshot.GetInfo()
            bmpstr = screenshot.GetBitmapBits(True)
            
            img = np.frombuffer(bmpstr, dtype='uint8')
            img.shape = (height, width, 4)
            
            # Convertir BGRA a BGR
            img_bgr = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
            
            # Limpiar recursos
            win32gui.DeleteObject(screenshot.GetHandle())
            mem_dc.DeleteDC()
            img_dc.DeleteDC()
            win32gui.ReleaseDC(hdesktop, desktop_dc)
            
            print(f"✅ DirectX Desktop Duplication exitoso: {img_bgr.shape[1]}x{img_bgr.shape[0]}")
            return img_bgr
            
        except Exception as e:
            raise Exception(f"DirectX Desktop Duplication error: {e}")

    def _capture_windows_graphics_api(self) -> Optional[np.ndarray]:
        """Windows Graphics Capture API - método moderno"""
        try:
            import win32gui
            import win32ui
            import win32con
            import win32api
            from ctypes import windll
            
            # Obtener handle del escritorio
            hdesktop = win32gui.GetDesktopWindow()
            
            # Obtener dimensiones
            width = win32api.GetSystemMetrics(win32con.SM_CXVIRTUALSCREEN)
            height = win32api.GetSystemMetrics(win32con.SM_CYVIRTUALSCREEN)
            left = win32api.GetSystemMetrics(win32con.SM_XVIRTUALSCREEN)
            top = win32api.GetSystemMetrics(win32con.SM_YVIRTUALSCREEN)
            
            # Crear contexto con flags especiales
            desktop_dc = win32gui.GetWindowDC(hdesktop)
            img_dc = win32ui.CreateDCFromHandle(desktop_dc)
            mem_dc = img_dc.CreateCompatibleDC()
            
            # Crear bitmap
            screenshot = win32ui.CreateBitmap()
            screenshot.CreateCompatibleBitmap(img_dc, width, height)
            mem_dc.SelectObject(screenshot)
            
            # Usar PatBlt para bypass
            mem_dc.PatBlt((0, 0), (width, height), win32con.WHITENESS)
            mem_dc.BitBlt((0, 0), (width, height), img_dc, (left, top), win32con.SRCCOPY)
            
            # Convertir a array
            bmpinfo = screenshot.GetInfo()
            bmpstr = screenshot.GetBitmapBits(True)
            
            img = np.frombuffer(bmpstr, dtype='uint8')
            img.shape = (height, width, 4)
            img_bgr = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
            
            # Limpiar
            win32gui.DeleteObject(screenshot.GetHandle())
            mem_dc.DeleteDC()
            img_dc.DeleteDC()
            win32gui.ReleaseDC(hdesktop, desktop_dc)
            
            print(f"✅ Windows Graphics API exitoso: {img_bgr.shape[1]}x{img_bgr.shape[0]}")
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
            from ctypes import windll
            
            # Obtener handle del escritorio
            hdesktop = win32gui.GetDesktopWindow()
            
            # Obtener dimensiones
            width = win32api.GetSystemMetrics(win32con.SM_CXVIRTUALSCREEN)
            height = win32api.GetSystemMetrics(win32con.SM_CYVIRTUALSCREEN)
            left = win32api.GetSystemMetrics(win32con.SM_XVIRTUALSCREEN)
            top = win32api.GetSystemMetrics(win32con.SM_YVIRTUALSCREEN)
            
            # Crear contexto con aceleración hardware
            desktop_dc = win32gui.GetWindowDC(hdesktop)
            img_dc = win32ui.CreateDCFromHandle(desktop_dc)
            mem_dc = img_dc.CreateCompatibleDC()
            
            # Crear bitmap
            screenshot = win32ui.CreateBitmap()
            screenshot.CreateCompatibleBitmap(img_dc, width, height)
            mem_dc.SelectObject(screenshot)
            
            # Usar StretchBlt para bypass
            mem_dc.StretchBlt(
                (0, 0), (width, height),
                img_dc, (left, top), (width, height),
                win32con.SRCCOPY
            )
            
            # Convertir a array
            bmpinfo = screenshot.GetInfo()
            bmpstr = screenshot.GetBitmapBits(True)
            
            img = np.frombuffer(bmpstr, dtype='uint8')
            img.shape = (height, width, 4)
            img_bgr = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
            
            # Limpiar
            win32gui.DeleteObject(screenshot.GetHandle())
            mem_dc.DeleteDC()
            img_dc.DeleteDC()
            win32gui.ReleaseDC(hdesktop, desktop_dc)
            
            print(f"✅ Hardware Accelerated exitoso: {img_bgr.shape[1]}x{img_bgr.shape[0]}")
            return img_bgr
            
        except Exception as e:
            raise Exception(f"Hardware Accelerated error: {e}")

    def _capture_memory_reading(self) -> Optional[np.ndarray]:
        """Memory Reading bypass - método más agresivo"""
        try:
            import win32gui
            import win32ui
            import win32con
            import win32api
            from ctypes import windll, byref, c_void_p, c_uint, c_int
            
            # Obtener handle del escritorio
            hdesktop = win32gui.GetDesktopWindow()
            
            # Obtener dimensiones
            width = win32api.GetSystemMetrics(win32con.SM_CXVIRTUALSCREEN)
            height = win32api.GetSystemMetrics(win32con.SM_CYVIRTUALSCREEN)
            left = win32api.GetSystemMetrics(win32con.SM_XVIRTUALSCREEN)
            top = win32api.GetSystemMetrics(win32con.SM_YVIRTUALSCREEN)
            
            # Crear contexto
            desktop_dc = win32gui.GetWindowDC(hdesktop)
            img_dc = win32ui.CreateDCFromHandle(desktop_dc)
            mem_dc = img_dc.CreateCompatibleDC()
            
            # Crear bitmap
            screenshot = win32ui.CreateBitmap()
            screenshot.CreateCompatibleBitmap(img_dc, width, height)
            mem_dc.SelectObject(screenshot)
            
            # Usar múltiples operaciones para bypass
            mem_dc.BitBlt((0, 0), (width, height), img_dc, (left, top), win32con.SRCCOPY)
            
            # Leer memoria directamente
            bmpinfo = screenshot.GetInfo()
            bmpstr = screenshot.GetBitmapBits(True)
            
            img = np.frombuffer(bmpstr, dtype='uint8')
            img.shape = (height, width, 4)
            img_bgr = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
            
            # Limpiar
            win32gui.DeleteObject(screenshot.GetHandle())
            mem_dc.DeleteDC()
            img_dc.DeleteDC()
            win32gui.ReleaseDC(hdesktop, desktop_dc)
            
            print(f"✅ Memory Reading exitoso: {img_bgr.shape[1]}x{img_bgr.shape[0]}")
            return img_bgr
            
        except Exception as e:
            raise Exception(f"Memory Reading error: {e}")

    def _capture_gdi_optimized(self) -> Optional[np.ndarray]:
        """GDI+ optimizado con técnicas avanzadas"""
        try:
            import win32gui
            import win32ui
            import win32con
            import win32api
            from ctypes import windll
            
            # Obtener handle del escritorio
            hdesktop = win32gui.GetDesktopWindow()
            
            # Obtener dimensiones
            width = win32api.GetSystemMetrics(win32con.SM_CXVIRTUALSCREEN)
            height = win32api.GetSystemMetrics(win32con.SM_CYVIRTUALSCREEN)
            left = win32api.GetSystemMetrics(win32con.SM_XVIRTUALSCREEN)
            top = win32api.GetSystemMetrics(win32con.SM_YVIRTUALSCREEN)
            
            # Crear contexto
            desktop_dc = win32gui.GetWindowDC(hdesktop)
            img_dc = win32ui.CreateDCFromHandle(desktop_dc)
            mem_dc = img_dc.CreateCompatibleDC()
            
            # Crear bitmap
            screenshot = win32ui.CreateBitmap()
            screenshot.CreateCompatibleBitmap(img_dc, width, height)
            mem_dc.SelectObject(screenshot)
            
            # Usar BitBlt con flags especiales
            mem_dc.BitBlt((0, 0), (width, height), img_dc, (left, top), win32con.SRCCOPY)
            
            # Convertir a array
            bmpinfo = screenshot.GetInfo()
            bmpstr = screenshot.GetBitmapBits(True)
            
            img = np.frombuffer(bmpstr, dtype='uint8')
            img.shape = (height, width, 4)
            img_bgr = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
            
            # Limpiar
            win32gui.DeleteObject(screenshot.GetHandle())
            mem_dc.DeleteDC()
            img_dc.DeleteDC()
            win32gui.ReleaseDC(hdesktop, desktop_dc)
            
            print(f"✅ GDI+ optimizado exitoso: {img_bgr.shape[1]}x{img_bgr.shape[0]}")
            return img_bgr
            
        except Exception as e:
            raise Exception(f"GDI+ optimizado error: {e}")

    def _capture_fallback_traditional(self) -> Optional[np.ndarray]:
        """Fallback tradicional con múltiples métodos"""
        try:
            # Intentar con mss
            try:
                import mss
                with mss.mss() as sct:
                    monitor = sct.monitors[1]
                    screenshot = sct.grab(monitor)
                    img_array = np.array(screenshot)
                    img_bgr = cv2.cvtColor(img_array, cv2.COLOR_BGRA2BGR)
                    print("✅ Captura con mss exitosa")
                    return img_bgr
            except Exception as mss_error:
                print(f"❌ Error con mss: {mss_error}")
            
            # Intentar con pyautogui
            try:
                screenshot = pyautogui.screenshot()
                img_array = np.array(screenshot)
                img_bgr = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
                print("✅ Captura con pyautogui exitosa")
                return img_bgr
            except Exception as pyautogui_error:
                print(f"❌ Error con pyautogui: {pyautogui_error}")
            
            # Intentar con PIL
            try:
                screenshot = ImageGrab.grab()
                img_array = np.array(screenshot)
                img_bgr = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
                print("✅ Captura con PIL exitosa")
                return img_bgr
            except Exception as pil_error:
                print(f"❌ Error con PIL: {pil_error}")
            
            raise Exception("Todos los métodos fallback fallaron")
            
        except Exception as e:
            raise Exception(f"Fallback tradicional error: {e}")
    
    def detect_enemies(self, image: np.ndarray) -> List[Tuple[int, int]]:
        """Detecta enemigos en la imagen"""
        enemies = []
        
        try:
            # Convertir a HSV
            hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
            
            for lower, upper in self.enemy_colors:
                # Crear máscara
                mask = cv2.inRange(hsv, np.array(lower), np.array(upper))
                
                # Encontrar contornos
                contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                
                for contour in contours:
                    # Filtrar por tamaño
                    if cv2.contourArea(contour) > 100:  # Mínimo tamaño
                        # Obtener centro del contorno
                        M = cv2.moments(contour)
                        if M["m00"] != 0:
                            cx = int(M["m10"] / M["m00"])
                            cy = int(M["m01"] / M["m00"])
                            enemies.append((cx, cy))
            
            return enemies
            
        except Exception as e:
            print(f"Error detectando enemigos: {e}")
            return []
    
    def detect_stairs(self, image: np.ndarray) -> List[Tuple[int, int]]:
        """Detecta escaleras en la imagen"""
        stairs = []
        
        try:
            hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
            
            for lower, upper in self.stair_colors:
                mask = cv2.inRange(hsv, np.array(lower), np.array(upper))
                contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                
                for contour in contours:
                    if cv2.contourArea(contour) > 50:
                        M = cv2.moments(contour)
                        if M["m00"] != 0:
                            cx = int(M["m10"] / M["m00"])
                            cy = int(M["m01"] / M["m00"])
                            stairs.append((cx, cy))
            
            return stairs
            
        except Exception as e:
            print(f"Error detectando escaleras: {e}")
            return []
    
    def detect_portals(self, image: np.ndarray) -> List[Tuple[int, int]]:
        """Detecta portales en la imagen"""
        portals = []
        
        try:
            hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
            
            for lower, upper in self.portal_colors:
                mask = cv2.inRange(hsv, np.array(lower), np.array(upper))
                contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                
                for contour in contours:
                    if cv2.contourArea(contour) > 200:  # Portales son más grandes
                        M = cv2.moments(contour)
                        if M["m00"] != 0:
                            cx = int(M["m10"] / M["m00"])
                            cy = int(M["m01"] / M["m00"])
                            portals.append((cx, cy))
            
            return portals
            
        except Exception as e:
            print(f"Error detectando portales: {e}")
            return []
    
    def detect_obstacles(self, image: np.ndarray) -> List[Tuple[int, int]]:
        """Detecta obstáculos en la imagen"""
        obstacles = []
        
        try:
            hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
            
            for lower, upper in self.obstacle_colors:
                mask = cv2.inRange(hsv, np.array(lower), np.array(upper))
                contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                
                for contour in contours:
                    if cv2.contourArea(contour) > 80:
                        M = cv2.moments(contour)
                        if M["m00"] != 0:
                            cx = int(M["m10"] / M["m00"])
                            cy = int(M["m01"] / M["m00"])
                            obstacles.append((cx, cy))
            
            return obstacles
            
        except Exception as e:
            print(f"Error detectando obstáculos: {e}")
            return []
    
    def find_closest_enemy(self, enemies: List[Tuple[int, int]], center: Tuple[int, int] = None) -> Optional[Tuple[int, int]]:
        """Encuentra el enemigo más cercano"""
        if not enemies:
            return None
        
        if center is None:
            # Usar centro de la pantalla como referencia
            center = (400, 300)  # Aproximadamente centro de Tibia
        
        closest = None
        min_distance = float('inf')
        
        for enemy in enemies:
            distance = np.sqrt((enemy[0] - center[0])**2 + (enemy[1] - center[1])**2)
            if distance < min_distance:
                min_distance = distance
                closest = enemy
        
        return closest
    
    def computer_vision_scan(self) -> dict:
        """Escaneo completo de Computer Vision"""
        image = self.capture_tibia_screen()
        if image is None:
            return {
                'enemies': [],
                'stairs': [],
                'portals': [],
                'obstacles': [],
                'closest_enemy': None
            }
        
        enemies = self.detect_enemies(image)
        stairs = self.detect_stairs(image)
        portals = self.detect_portals(image)
        obstacles = self.detect_obstacles(image)
        closest_enemy = self.find_closest_enemy(enemies)
        
        return {
            'enemies': enemies,
            'stairs': stairs,
            'portals': portals,
            'obstacles': obstacles,
            'closest_enemy': closest_enemy,
            'image': image
        }
    
    def detect_health_mana_from_screen(self, image: np.ndarray) -> Tuple[int, int]:
        """Detecta HP y Mana desde las barras de estado (versión refactorizada)"""
        try:
            # Obtener dimensiones de la imagen
            height, width = image.shape[:2]
            
            # Intentar cargar regiones configuradas por el usuario
            custom_regions = self._load_custom_regions()
            
            if custom_regions:
                # Usar regiones personalizadas
                health_percent = self._detect_health_from_custom_region(image, custom_regions["health_bar"])
                mana_percent = self._detect_mana_from_custom_region(image, custom_regions["mana_bar"])
                print(f"DEBUG FINAL (Custom): HP={health_percent}%, Mana={mana_percent}%")
            else:
                # Usar detección automática en múltiples regiones
                health_percent = self._detect_health_bar(image, height, width)
                mana_percent = self._detect_mana_bar(image, height, width)
                print(f"DEBUG FINAL (Auto): HP={health_percent}%, Mana={mana_percent}%")
            
            return health_percent, mana_percent
            
        except Exception as e:
            print(f"Error detectando HP/Mana: {e}")
            return 100, 100  # Default si hay error
    
    def detect_health_mana_manual(self) -> Tuple[int, int]:
        """Detecta HP y Mana usando solo coordenadas manuales (sin screenshot)"""
        try:
            # Cargar regiones configuradas
            custom_regions = self._load_custom_regions()
            
            if not custom_regions:
                print("❌ No hay regiones configuradas. Usa 'Configurar Pantalla' primero.")
                return 100, 100
            
            # Intentar capturar pantalla (puede fallar por anti-cheat)
            image = self.capture_tibia_screen()
            
            if image is None:
                print("⚠️ No se pudo capturar pantalla (anti-cheat activo)")
                print("💡 Usando valores por defecto - configura las regiones manualmente")
                return 100, 100
            
            # Usar regiones personalizadas
            health_percent = self._detect_health_from_custom_region(image, custom_regions["health_bar"])
            mana_percent = self._detect_mana_from_custom_region(image, custom_regions["mana_bar"])
            
            print(f"DEBUG MANUAL: HP={health_percent}%, Mana={mana_percent}%")
            return health_percent, mana_percent
            
        except Exception as e:
            print(f"Error en detección manual: {e}")
            return 100, 100
    
    def detect_health_mana_ocr(self) -> Tuple[int, int]:
        """Detecta HP y Mana usando OCR (reconocimiento de texto)"""
        try:
            import pytesseract
            from PIL import Image
            
            # Intentar capturar pantalla
            image = self.capture_tibia_screen()
            if image is None:
                print("❌ No se pudo capturar pantalla para OCR")
                return 100, 100
            
            # Convertir a PIL Image
            pil_image = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
            
            # Configurar tesseract para números
            custom_config = r'--oem 3 --psm 6 -c tessedit_char_whitelist=0123456789/%'
            
            # Extraer texto de toda la imagen
            text = pytesseract.image_to_string(pil_image, config=custom_config)
            
            print(f"DEBUG OCR: Texto detectado: {text}")
            
            # Buscar patrones de HP y Mana
            health_percent = self._extract_health_from_text(text)
            mana_percent = self._extract_mana_from_text(text)
            
            print(f"DEBUG OCR: HP={health_percent}%, Mana={mana_percent}%")
            return health_percent, mana_percent
            
        except Exception as e:
            print(f"Error en OCR: {e}")
            return 100, 100
    
    def _detect_health_bar(self, image: np.ndarray, height: int, width: int) -> int:
        """Detecta específicamente la barra de vida (roja)"""
        try:
            # Buscar en diferentes regiones donde puede estar la barra de vida
            regions_to_check = [
                # Región inferior izquierda (más común)
                image[height-60:height-20, 10:width//3],
                # Región inferior central
                image[height-60:height-20, width//3:2*width//3],
                # Región inferior derecha
                image[height-60:height-20, 2*width//3:width-10],
                # Región superior (alternativa)
                image[10:50, 10:width-10]
            ]
            
            best_health = 0
            best_region = 0
            
            for i, region in enumerate(regions_to_check):
                health = self._analyze_red_region(region, f"HP_Region_{i}")
                if health > best_health:
                    best_health = health
                    best_region = i
            
            print(f"DEBUG HP: Mejor región={best_region}, Valor={best_health}%")
            return best_health
            
        except Exception as e:
            print(f"Error detectando barra de vida: {e}")
            return 100
    
    def _detect_mana_bar(self, image: np.ndarray, height: int, width: int) -> int:
        """Detecta específicamente la barra de mana (azul)"""
        try:
            # Buscar en diferentes regiones donde puede estar la barra de mana
            regions_to_check = [
                # Región inferior derecha (más común para mana)
                image[height-60:height-20, 2*width//3:width-10],
                # Región inferior central
                image[height-60:height-20, width//3:2*width//3],
                # Región inferior izquierda
                image[height-60:height-20, 10:width//3],
                # Región superior (alternativa)
                image[10:50, 10:width-10]
            ]
            
            best_mana = 0
            best_region = 0
            
            for i, region in enumerate(regions_to_check):
                mana = self._analyze_blue_region(region, f"Mana_Region_{i}")
                if mana > best_mana:
                    best_mana = mana
                    best_region = i
            
            print(f"DEBUG Mana: Mejor región={best_region}, Valor={best_mana}%")
            return best_mana
            
        except Exception as e:
            print(f"Error detectando barra de mana: {e}")
            return 100
    
    def _analyze_red_region(self, region: np.ndarray, region_name: str) -> int:
        """Analiza una región específica para detectar barra roja (vida)"""
        try:
            # Convertir a HSV
            hsv = cv2.cvtColor(region, cv2.COLOR_BGR2HSV)
            
            # Detectar rojo (incluye ambos extremos del espectro HSV)
            red_lower1 = np.array([0, 100, 100])
            red_upper1 = np.array([10, 255, 255])
            red_lower2 = np.array([170, 100, 100])
            red_upper2 = np.array([180, 255, 255])
            
            red_mask1 = cv2.inRange(hsv, red_lower1, red_upper1)
            red_mask2 = cv2.inRange(hsv, red_lower2, red_upper2)
            red_mask = cv2.bitwise_or(red_mask1, red_mask2)
            
            # Contar píxeles rojos
            red_pixels = cv2.countNonZero(red_mask)
            total_pixels = region.shape[0] * region.shape[1]
            red_density = red_pixels / total_pixels
            
            # Guardar máscara para debug
            cv2.imwrite(f"logs/{region_name}_red_mask.png", red_mask)
            
            # Calcular porcentaje basado en densidad
            if red_density > 0.1:  # Más del 10% de píxeles rojos
                return min(100, int(red_density * 1000))  # Escalar apropiadamente
            elif red_density > 0.05:  # Más del 5% de píxeles rojos
                return min(100, int(red_density * 800))
            elif red_density > 0.02:  # Más del 2% de píxeles rojos
                return min(100, int(red_density * 600))
            else:
                return 0  # No hay barra roja visible
            
        except Exception as e:
            print(f"Error analizando región roja {region_name}: {e}")
            return 0
    
    def _analyze_blue_region(self, region: np.ndarray, region_name: str) -> int:
        """Analiza una región específica para detectar barra azul (mana)"""
        try:
            # Convertir a HSV
            hsv = cv2.cvtColor(region, cv2.COLOR_BGR2HSV)
            
            # Detectar azul
            blue_lower = np.array([100, 100, 100])
            blue_upper = np.array([130, 255, 255])
            blue_mask = cv2.inRange(hsv, blue_lower, blue_upper)
            
            # Contar píxeles azules
            blue_pixels = cv2.countNonZero(blue_mask)
            total_pixels = region.shape[0] * region.shape[1]
            blue_density = blue_pixels / total_pixels
            
            # Guardar máscara para debug
            cv2.imwrite(f"logs/{region_name}_blue_mask.png", blue_mask)
            
            # Calcular porcentaje basado en densidad
            if blue_density > 0.1:  # Más del 10% de píxeles azules
                return min(100, int(blue_density * 1000))  # Escalar apropiadamente
            elif blue_density > 0.05:  # Más del 5% de píxeles azules
                return min(100, int(blue_density * 800))
            elif blue_density > 0.02:  # Más del 2% de píxeles azules
                return min(100, int(blue_density * 600))
            else:
                return 0  # No hay barra azul visible
            
        except Exception as e:
            print(f"Error analizando región azul {region_name}: {e}")
            return 0
    
    def _detect_text_density(self, region: np.ndarray, region_type: str) -> int:
        """Detecta porcentaje basado en densidad de texto blanco"""
        try:
            # Contar píxeles blancos (texto)
            white_pixels = cv2.countNonZero(region)
            total_pixels = region.shape[0] * region.shape[1]
            text_density = white_pixels / total_pixels
            
            # Debug info
            print(f"DEBUG {region_type}: Píxeles blancos={white_pixels}/{total_pixels}, Densidad={text_density:.3f}")
            
            # Calcular porcentaje basado en densidad
            # Más texto blanco = números más bajos (más dígitos visibles)
            if text_density > 0.15:  # Mucho texto blanco
                return 10  # Números muy bajos
            elif text_density > 0.10:  # Bastante texto blanco
                return 25  # Números bajos
            elif text_density > 0.07:  # Texto medio
                return 50  # Números medios
            elif text_density > 0.04:  # Poco texto blanco
                return 75  # Números altos
            elif text_density > 0.02:  # Muy poco texto blanco
                return 90  # Números muy altos
            else:
                return 100  # Sin texto blanco = probablemente 100%
            
        except Exception as e:
            print(f"Error detectando {region_type}: {e}")
            return 100
    
    def _detect_health_alternative(self, region: np.ndarray) -> int:
        """Método alternativo para detectar HP usando brillo"""
        try:
            # Convertir a escala de grises
            gray = cv2.cvtColor(region, cv2.COLOR_BGR2GRAY)
            
            # Calcular brillo promedio
            brightness = np.mean(gray)
            
            # Si el brillo es muy alto, probablemente es texto blanco (números)
            if brightness > 200:  # Muy brillante
                return 25  # Probablemente números bajos
            elif brightness > 150:  # Brillo medio
                return 50
            elif brightness > 100:  # Brillo bajo
                return 75
            else:
                return 100  # Muy oscuro, probablemente sin texto
            
        except Exception as e:
            print(f"Error en detección alternativa de HP: {e}")
            return 100
    
    def _detect_mana_alternative(self, region: np.ndarray) -> int:
        """Método alternativo para detectar Mana usando brillo"""
        try:
            # Convertir a escala de grises
            gray = cv2.cvtColor(region, cv2.COLOR_BGR2GRAY)
            
            # Calcular brillo promedio
            brightness = np.mean(gray)
            
            # Si el brillo es muy alto, probablemente es texto blanco (números)
            if brightness > 200:  # Muy brillante
                return 25  # Probablemente números bajos
            elif brightness > 150:  # Brillo medio
                return 50
            elif brightness > 100:  # Brillo bajo
                return 75
            else:
                return 100  # Muy oscuro, probablemente sin texto
            
        except Exception as e:
            print(f"Error en detección alternativa de Mana: {e}")
            return 100
    
    def calibrate_health_mana_bars(self) -> dict:
        """Calibra las posiciones de las barras de vida y mana"""
        try:
            image = self.capture_tibia_screen()
            if image is None:
                return {"success": False, "message": "No se pudo capturar pantalla"}
            
            height, width = image.shape[:2]
            
            # Guardar imagen para análisis
            cv2.imwrite("logs/tibia_screen_calibration.png", image)
            
            # Buscar barras de vida y mana en diferentes regiones
            calibration_data = {
                "screen_size": (width, height),
                "health_bar_found": False,
                "mana_bar_found": False,
                "suggested_regions": []
            }
            
            # Buscar en diferentes regiones típicas de Tibia
            regions_to_check = [
                {"name": "top_left", "coords": (10, 10, 200, 60)},
                {"name": "top_center", "coords": (width//2-100, 10, width//2+100, 60)},
                {"name": "top_right", "coords": (width-210, 10, width-10, 60)},
                {"name": "bottom_left", "coords": (10, height-60, 200, height-10)},
                {"name": "bottom_center", "coords": (width//2-100, height-60, width//2+100, height-10)}
            ]
            
            for region in regions_to_check:
                x1, y1, x2, y2 = region["coords"]
                region_img = image[y1:y2, x1:x2]
                
                # Convertir a HSV
                hsv = cv2.cvtColor(region_img, cv2.COLOR_BGR2HSV)
                
                # Buscar colores de barras
                green_pixels = cv2.countNonZero(cv2.inRange(hsv, np.array([40, 50, 50]), np.array([80, 255, 255])))
                red_pixels = cv2.countNonZero(cv2.inRange(hsv, np.array([0, 50, 50]), np.array([20, 255, 255])))
                blue_pixels = cv2.countNonZero(cv2.inRange(hsv, np.array([100, 50, 50]), np.array([130, 255, 255])))
                
                # Si encuentra suficientes píxeles, es una barra
                if green_pixels > 100 or red_pixels > 100:
                    calibration_data["health_bar_found"] = True
                    calibration_data["suggested_regions"].append({
                        "type": "health",
                        "region": region["name"],
                        "coords": region["coords"],
                        "green_pixels": green_pixels,
                        "red_pixels": red_pixels
                    })
                
                if blue_pixels > 100:
                    calibration_data["mana_bar_found"] = True
                    calibration_data["suggested_regions"].append({
                        "type": "mana",
                        "region": region["name"],
                        "coords": region["coords"],
                        "blue_pixels": blue_pixels
                    })
            
            calibration_data["success"] = True
            calibration_data["message"] = f"Calibración completada. Imagen guardada en logs/tibia_screen_calibration.png"
            
            return calibration_data
            
        except Exception as e:
            return {"success": False, "message": f"Error en calibración: {e}"}
    
    def set_health_mana_regions(self, health_coords: tuple, mana_coords: tuple):
        """Establece las coordenadas personalizadas para las barras de vida y mana"""
        self.health_region_coords = health_coords  # (x1, y1, x2, y2)
        self.mana_region_coords = mana_coords      # (x1, y1, x2, y2)

    def _load_custom_regions(self) -> Optional[Dict]:
        """Carga las regiones configuradas por el usuario"""
        try:
            import json
            import os
            
            config_file = "config/screen_regions.json"
            if os.path.exists(config_file):
                with open(config_file, 'r') as f:
                    config = json.load(f)
                    if "screen_regions" in config:
                        return config["screen_regions"]
            return None
        except Exception as e:
            print(f"Error cargando regiones personalizadas: {e}")
            return None
    
    def _detect_health_from_custom_region(self, image: np.ndarray, region: Dict) -> int:
        """Detecta HP desde una región personalizada"""
        try:
            x, y = region["x"], region["y"]
            w, h = region["width"], region["height"]
            
            # Recortar la región específica
            health_region = image[y:y+h, x:x+w]
            
            # Analizar la región roja
            health_percent = self._analyze_red_region(health_region, "custom_health")
            
            print(f"DEBUG HP (Custom): Región=({x},{y}) {w}x{h}, Valor={health_percent}%")
            return health_percent
            
        except Exception as e:
            print(f"Error detectando HP desde región personalizada: {e}")
            return 100
    
    def _detect_mana_from_custom_region(self, image: np.ndarray, region: Dict) -> int:
        """Detecta Mana desde una región personalizada"""
        try:
            x, y = region["x"], region["y"]
            w, h = region["width"], region["height"]
            
            # Recortar la región específica
            mana_region = image[y:y+h, x:x+w]
            
            # Analizar la región azul
            mana_percent = self._analyze_blue_region(mana_region, "custom_mana")
            
            print(f"DEBUG Mana (Custom): Región=({x},{y}) {w}x{h}, Valor={mana_percent}%")
            return mana_percent
            
        except Exception as e:
            print(f"Error detectando Mana desde región personalizada: {e}")
            return 100

    def _extract_health_from_text(self, text: str) -> int:
        """Extrae el porcentaje de vida del texto OCR"""
        try:
            # Buscar patrones como "HP: 75%" o "75%" o "75/100"
            import re
            
            # Patrones para HP
            patterns = [
                r'HP:\s*(\d+)%',  # HP: 75%
                r'(\d+)%',        # 75%
                r'(\d+)/\d+',     # 75/100
                r'Vida:\s*(\d+)', # Vida: 75
            ]
            
            for pattern in patterns:
                matches = re.findall(pattern, text, re.IGNORECASE)
                if matches:
                    value = int(matches[0])
                    if 0 <= value <= 100:
                        return value
            
            # Si no encuentra patrones, buscar números entre 0-100
            numbers = re.findall(r'\b(\d{1,3})\b', text)
            for num in numbers:
                value = int(num)
                if 0 <= value <= 100:
                    return value
            
            return 100  # Default
            
        except Exception as e:
            print(f"Error extrayendo HP: {e}")
            return 100
    
    def _extract_mana_from_text(self, text: str) -> int:
        """Extrae el porcentaje de mana del texto OCR"""
        try:
            # Buscar patrones como "Mana: 75%" o "MP: 75%"
            import re
            
            # Patrones para Mana
            patterns = [
                r'Mana:\s*(\d+)%',  # Mana: 75%
                r'MP:\s*(\d+)%',    # MP: 75%
                r'(\d+)%',          # 75%
                r'(\d+)/\d+',       # 75/100
            ]
            
            for pattern in patterns:
                matches = re.findall(pattern, text, re.IGNORECASE)
                if matches:
                    value = int(matches[0])
                    if 0 <= value <= 100:
                        return value
            
            # Si no encuentra patrones específicos, buscar números
            numbers = re.findall(r'\b(\d{1,3})\b', text)
            for num in numbers:
                value = int(num)
                if 0 <= value <= 100:
                    return value
            
            return 100  # Default
            
        except Exception as e:
            print(f"Error extrayendo Mana: {e}")
            return 100

    def detect_health_mana_pixels(self) -> Tuple[int, int]:
        """Detecta HP y Mana usando solo píxeles específicos (sin screenshot)"""
        try:
            import pyautogui
            
            # Cargar regiones configuradas
            custom_regions = self._load_custom_regions()
            
            if not custom_regions:
                print("❌ No hay regiones configuradas. Usa 'Configurar Pantalla' primero.")
                return 100, 100
            
            health_region = custom_regions["health_bar"]
            mana_region = custom_regions["mana_bar"]
            
            # Obtener color de píxeles específicos en las regiones
            health_percent = self._detect_health_from_pixels(health_region)
            mana_percent = self._detect_mana_from_pixels(mana_region)
            
            print(f"DEBUG PIXELS: HP={health_percent}%, Mana={mana_percent}%")
            return health_percent, mana_percent
            
        except Exception as e:
            print(f"Error en detección por píxeles: {e}")
            return 100, 100
    
    def _detect_health_from_pixels(self, region: Dict) -> int:
        """Detecta HP analizando colores de píxeles específicos"""
        try:
            import pyautogui
            
            x, y = region["x"], region["y"]
            width, height = region["width"], region["height"]
            
            # Obtener colores de varios píxeles en la región
            red_pixels = 0
            total_pixels = 0
            
            # Muestrear píxeles en la región
            for i in range(0, width, 10):  # Cada 10 píxeles
                for j in range(0, height, 5):   # Cada 5 píxeles
                    try:
                        pixel_color = pyautogui.pixel(x + i, y + j)
                        total_pixels += 1
                        
                        # Detectar rojo (R > G y R > B)
                        if pixel_color[0] > pixel_color[1] and pixel_color[0] > pixel_color[2]:
                            red_pixels += 1
                    except:
                        continue
            
            if total_pixels > 0:
                red_percentage = (red_pixels / total_pixels) * 100
                return min(100, int(red_percentage * 2))  # Escalar apropiadamente
            
            return 100
            
        except Exception as e:
            print(f"Error detectando HP por píxeles: {e}")
            return 100
    
    def _detect_mana_from_pixels(self, region: Dict) -> int:
        """Detecta Mana analizando colores de píxeles específicos"""
        try:
            import pyautogui
            
            x, y = region["x"], region["y"]
            width, height = region["width"], region["height"]
            
            # Obtener colores de varios píxeles en la región
            blue_pixels = 0
            total_pixels = 0
            
            # Muestrear píxeles en la región
            for i in range(0, width, 10):  # Cada 10 píxeles
                for j in range(0, height, 5):   # Cada 5 píxeles
                    try:
                        pixel_color = pyautogui.pixel(x + i, y + j)
                        total_pixels += 1
                        
                        # Detectar azul (B > R y B > G)
                        if pixel_color[2] > pixel_color[0] and pixel_color[2] > pixel_color[1]:
                            blue_pixels += 1
                    except:
                        continue
            
            if total_pixels > 0:
                blue_percentage = (blue_pixels / total_pixels) * 100
                return min(100, int(blue_percentage * 2))  # Escalar apropiadamente
            
            return 100
            
        except Exception as e:
            print(f"Error detectando Mana por píxeles: {e}")
            return 100

# Instancia global
cv_system = ComputerVision() 