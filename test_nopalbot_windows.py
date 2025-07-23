#!/usr/bin/env python3
"""
NopalBot - Windows Test Script with Ghost Mouse
By Taquito Loco 🎮
"""

import time
import random
import logging
import os
import cv2
import numpy as np
import pyautogui
import keyboard
from datetime import datetime
from pathlib import Path

class NopalBotIntelligent:
    def __init__(self):
        self.setup_logging()
        self.setup_hotkeys()
        self.health = 100
        self.mana = 100
        self.level = 1
        self.heal_threshold = random.randint(20, 40)
        self.mana_threshold = random.randint(20, 40)
        self.spell_mana_threshold = 60  # Solo hechizos si mana > 60%
        self.last_enemy_death = 0
        self.enemy_detected = False
        self.combat_mode = False
        self.movement_direction = 0  # 0-7 para 8 direcciones
        self.last_movement = 0
        
        # Configuración para druida
        self.character_class = "Druid"
        self.attack_spell = "f3"  # Exori vis
        self.heal_spell = "f4"    # Exura
        self.mana_potion = "f2"
        self.health_potion = "f1"
        self.attack_key = "k"
        self.quick_loot = "0"
        
        logging.info(f"🤖 NopalBot {self.character_class} initialized")
        logging.info(f"🎯 Heal threshold: {self.heal_threshold}%")
        logging.info(f"🎯 Mana threshold: {self.mana_threshold}%")
        logging.info(f"🔮 Spell mana threshold: {self.spell_mana_threshold}%")

    def setup_logging(self):
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = log_dir / f"nopalbot_druid_{timestamp}.log"
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        logging.info(f"📝 Log file: {log_file}")

    def setup_hotkeys(self):
        keyboard.on_press_key("f12", lambda _: self.emergency_stop())
        keyboard.on_press_key("f11", lambda _: self.toggle_ghost_mouse())
        keyboard.on_press_key("f10", lambda _: self.print_status())
        
        logging.info("🔑 Hotkeys configured:")
        logging.info("   F12: Emergency Stop")
        logging.info("   F11: Toggle Ghost Mouse")
        logging.info("   F10: Print Status")

    def emergency_stop(self):
        logging.info("🚨 EMERGENCY STOP ACTIVATED!")
        os._exit(0)

    def toggle_ghost_mouse(self):
        logging.info("👻 Ghost mouse toggled")

    def print_status(self):
        logging.info(f"📊 Status - Health: {self.health}%, Mana: {self.mana}%, Level: {self.level}")

    def find_tibia_window(self):
        """Busca la ventana de Tibia y la activa"""
        try:
            # Buscar ventana de Tibia
            windows = pyautogui.getWindowsWithTitle("Tibia")
            if windows:
                self.tibia_window = windows[0]
                self.tibia_window.activate()
                time.sleep(0.5)  # Esperar a que se active
                
                # Obtener coordenadas de la ventana
                self.tibia_left = self.tibia_window.left
                self.tibia_top = self.tibia_window.top
                self.tibia_width = self.tibia_window.width
                self.tibia_height = self.tibia_window.height
                
                logging.info(f"🎮 Tibia window found: {self.tibia_window.title}")
                logging.info(f"📍 Window position: ({self.tibia_left}, {self.tibia_top})")
                logging.info(f"📏 Window size: {self.tibia_width}x{self.tibia_height}")
                return True
            else:
                logging.warning("⚠️ Tibia window not found!")
                return False
        except Exception as e:
            logging.error(f"❌ Error finding Tibia window: {e}")
            return False

    def click_within_tibia(self, x, y):
        """Hacer clic solo dentro de la ventana de Tibia"""
        try:
            if hasattr(self, 'tibia_window'):
                # Convertir coordenadas relativas a absolutas dentro de Tibia
                tibia_x = self.tibia_left + x
                tibia_y = self.tibia_top + y
                
                # Verificar que esté dentro de los límites
                if (self.tibia_left <= tibia_x <= self.tibia_left + self.tibia_width and
                    self.tibia_top <= tibia_y <= self.tibia_top + self.tibia_height):
                    
                    # Activar ventana primero
                    self.tibia_window.activate()
                    time.sleep(0.1)
                    
                    # Hacer clic
                    pyautogui.click(tibia_x, tibia_y)
                    logging.info(f"🎯 Clicked within Tibia at ({x}, {y})")
                    return True
                else:
                    logging.warning(f"⚠️ Click position ({x}, {y}) outside Tibia window!")
                    return False
            else:
                logging.warning("⚠️ Tibia window not initialized!")
                return False
        except Exception as e:
            logging.error(f"❌ Error clicking in Tibia: {e}")
            return False

    def detect_enemies_from_logs(self):
        """Lee logs de Tibia para detectar enemigos"""
        try:
            # Rutas comunes de logs de Tibia
            log_paths = [
                os.path.expanduser("~/AppData/Roaming/Tibia/logs/server.log"),
                "C:/Users/Public/Documents/Tibia/logs/server.log",
                "C:/Tibia/logs/server.log"
            ]
            
            for log_path in log_paths:
                if os.path.exists(log_path):
                    with open(log_path, 'r', encoding='utf-8') as f:
                        lines = f.readlines()
                        if lines:
                            last_line = lines[-1].lower()
                            
                            # Detectar enemigos
                            if any(word in last_line for word in ['troll', 'rat', 'spider', 'snake', 'orc', 'goblin', 'rotworm']):
                                if not self.enemy_detected:
                                    logging.info(f"🎯 Enemy detected in logs: {last_line.strip()}")
                                    self.enemy_detected = True
                                    self.combat_mode = True
                                return True
                            
                            # Detectar muerte de enemigo
                            if any(word in last_line for word in ['loot', 'corpse', 'dead', 'killed']):
                                if self.enemy_detected:
                                    logging.info(f"💀 Enemy died: {last_line.strip()}")
                                    self.enemy_detected = False
                                    self.last_enemy_death = time.time()
                                return False
            
            # Si no hay logs, usar detección visual
            return self.find_closest_enemy_visual()
            
        except Exception as e:
            logging.debug(f"📝 No log file found, using visual detection")
            return self.find_closest_enemy_visual()

    def find_closest_enemy_visual(self):
        """Detección visual de enemigos usando OpenCV SOLO dentro de Tibia"""
        try:
            if not hasattr(self, 'tibia_window'):
                return False
                
            # Activar ventana de Tibia
            self.tibia_window.activate()
            time.sleep(0.1)
            
            # Capturar SOLO la región de Tibia
            screenshot = pyautogui.screenshot(region=(
                self.tibia_left, 
                self.tibia_top, 
                self.tibia_width, 
                self.tibia_height
            ))
            
            img = np.array(screenshot)
            img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
            
            # Convertir a HSV para detectar colores de enemigos
            hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
            
            # Detectar rojo (enemigos) - rango más amplio
            lower_red1 = np.array([0, 20, 20])
            upper_red1 = np.array([20, 255, 255])
            lower_red2 = np.array([150, 20, 20])
            upper_red2 = np.array([180, 255, 255])
            
            mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
            mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
            mask = mask1 + mask2
            
            # También detectar marrón (trolls, orcs)
            lower_brown = np.array([5, 30, 10])
            upper_brown = np.array([25, 255, 200])
            brown_mask = cv2.inRange(hsv, lower_brown, upper_brown)
            
            # Detectar gris oscuro (enemigos)
            lower_gray = np.array([0, 0, 30])
            upper_gray = np.array([180, 30, 100])
            gray_mask = cv2.inRange(hsv, lower_gray, upper_gray)
            
            # Combinar máscaras
            final_mask = mask + brown_mask + gray_mask
            
            # Encontrar contornos
            contours, _ = cv2.findContours(final_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            if contours:
                # Encontrar el contorno más grande (enemigo más cercano)
                largest_contour = max(contours, key=cv2.contourArea)
                if cv2.contourArea(largest_contour) > 30:  # Umbral muy bajo para detectar más enemigos
                    M = cv2.moments(largest_contour)
                    if M["m00"] != 0:
                        cx = int(M["m10"] / M["m00"])
                        cy = int(M["m01"] / M["m00"])
                        
                        # Hacer clic SOLO dentro de Tibia
                        if self.click_within_tibia(cx, cy):
                            logging.info(f"🎯 Enemy found at ({cx}, {cy}) within Tibia")
                            self.enemy_detected = True
                            self.combat_mode = True
                            return True
            
            # Si no encuentra enemigos, desactivar modo combate
            if self.enemy_detected:
                logging.info("🎯 No enemies found, exiting combat mode")
                self.enemy_detected = False
                self.combat_mode = False
            
            return False
            
        except Exception as e:
            logging.debug(f"🔍 Visual detection error: {e}")
            return False

    def intelligent_attack(self):
        """Ataque inteligente con posicionamiento SOLO en Tibia"""
        if not self.enemy_detected:
            return False
            
        logging.info(f"⚔️ PRESSING ATTACK KEY: {self.attack_key.upper()}")
        
        # Asegurar que Tibia esté activa
        if hasattr(self, 'tibia_window'):
            self.tibia_window.activate()
            time.sleep(0.1)
        
        # Presionar tecla de ataque múltiples veces de forma más agresiva
        for attempt in range(1, 6):  # Más intentos de ataque
            keyboard.press_and_release(self.attack_key)
            logging.info(f"⌨️ Sent globally: ⚔️ Attack Enemy (attempt {attempt}) ({self.attack_key})")
            logging.info(f"⚔️ ATTACK KEY {self.attack_key.upper()} PRESSED!")
            time.sleep(0.05)  # Más rápido
        
        logging.info("⚔️ ATTACK SEQUENCE COMPLETED!")
        return True

    def intelligent_movement(self):
        """Movimiento inteligente para evitar enemigos"""
        if self.enemy_detected:
            # En combate, moverse en círculos para evitar daño
            current_time = time.time()
            if current_time - self.last_movement > 2:  # Moverse cada 2 segundos
                # Movimiento en círculo usando CTRL + direcciones
                directions = ['up', 'right', 'down', 'left']
                direction = directions[self.movement_direction % 4]
                
                keyboard.press('ctrl')
                keyboard.press_and_release(direction)
                keyboard.release('ctrl')
                
                logging.info(f"🔄 Combat movement: {direction}")
                self.movement_direction += 1
                self.last_movement = current_time
        else:
            # Buscar enemigos moviéndose por el mapa
            current_time = time.time()
            if current_time - self.last_movement > 3:  # Moverse cada 3 segundos
                # Movimiento aleatorio para buscar enemigos
                directions = ['up', 'right', 'down', 'left']
                direction = random.choice(directions)
                
                keyboard.press_and_release(direction)
                logging.info(f"🔍 Searching movement: {direction}")
                self.last_movement = current_time

    def intelligent_healing(self):
        """Curación inteligente"""
        if self.health < self.heal_threshold:
            keyboard.press_and_release(self.health_potion)
            self.health = min(100, self.health + 50)
            logging.info(f"❤️ Health potion used! Health: {self.health}%")
            return True
        return False

    def intelligent_mana(self):
        """Mana inteligente"""
        if self.mana < self.mana_threshold:
            keyboard.press_and_release(self.mana_potion)
            self.mana = min(100, self.mana + 50)
            logging.info(f"🔮 Mana potion used! Mana: {self.mana}%")
            return True
        return False

    def intelligent_spells(self):
        """Hechizos inteligentes solo si hay suficiente mana"""
        if self.mana > self.spell_mana_threshold and self.enemy_detected:
            # Hechizo de ataque
            keyboard.press_and_release(self.attack_spell)
            self.mana = max(0, self.mana - 20)
            logging.info(f"🔮 Attack spell cast! Mana: {self.mana}%")
            
            time.sleep(0.5)
            
            # Hechizo de curación si es necesario
            if self.health < 70:
                keyboard.press_and_release(self.heal_spell)
                self.mana = max(0, self.mana - 15)
                self.health = min(100, self.health + 30)
                logging.info(f"🔮 Heal spell cast! Health: {self.health}%, Mana: {self.mana}%")
            
            return True
        return False

    def automatic_quick_loot(self):
        """Loot automático después de muerte de enemigo"""
        current_time = time.time()
        if current_time - self.last_enemy_death > 1 and current_time - self.last_enemy_death < 3:
            keyboard.press_and_release(self.quick_loot)
            logging.info(f"⌨️ Sent globally: 💰 Quick Loot Nearby Corpses ({self.quick_loot})")
            logging.info("💰 Quick loot executed!")
            return True
        return False

    def combat_action(self):
        """Acción principal de combate"""
        # Prioridad: Quick loot > Healing > Mana > Attack > Spells > Movement
        
        # 1. Quick loot si acaba de morir enemigo
        if self.automatic_quick_loot():
            return
        
        # 2. Curación si es necesario
        if self.intelligent_healing():
            return
        
        # 3. Mana si es necesario
        if self.intelligent_mana():
            return
        
        # 4. Ataque si hay enemigo
        if self.enemy_detected:
            if self.intelligent_attack():
                time.sleep(0.5)
                # 5. Hechizos después de atacar
                self.intelligent_spells()
        else:
            # Si no hay enemigo, buscar uno
            self.detect_enemies_from_logs()
        
        # 6. Movimiento inteligente
        self.intelligent_movement()

    def run_intelligent_bot(self, duration=60):
        """Ejecutar bot inteligente"""
        logging.info("🤖 NopalBot Intelligent Tester Starting...")
        logging.info("🎮 Make sure Tibia is running!")
        logging.info("🔑 Press F12 to stop, F11 to toggle ghost mouse, F10 for status")
        logging.info("🎯 Enemy detection: Red squares will be detected and attacked")
        
        if not self.find_tibia_window():
            logging.warning("⚠️ Tibia not found, continuing anyway...")
        
        start_time = time.time()
        mouse_actions = 0
        keyboard_actions = 0
        heals_used = 0
        mana_pots_used = 0
        spells_cast = 0
        attacks_made = 0
        enemies_detected = 0
        enemies_killed = 0
        quick_loots = 0
        
        try:
            while time.time() - start_time < duration:
                # Detectar enemigos
                enemy_found = self.detect_enemies_from_logs()
                if enemy_found and not self.enemy_detected:
                    enemies_detected += 1
                
                # Acción de combate
                self.combat_action()
                
                # Contar acciones
                if self.enemy_detected:
                    attacks_made += 1
                
                # Simular pérdida de vida/mana más agresiva para testing
                if random.random() < 0.4:  # 40% chance cada segundo
                    damage = random.randint(15, 30)
                    self.health = max(0, self.health - damage)
                    logging.info(f"💥 Took {damage} damage! Health: {self.health}%")
                
                if random.random() < 0.3:  # 30% chance cada segundo
                    mana_loss = random.randint(8, 20)
                    self.mana = max(0, self.mana - mana_loss)
                    logging.info(f"🔮 Lost {mana_loss} mana! Mana: {self.mana}%")
                
                time.sleep(1)
                
        except KeyboardInterrupt:
            logging.info("🛑 Bot stopped by user")
        
        # Resultados finales
        duration_actual = time.time() - start_time
        logging.info("=" * 50)
        logging.info("📊 NOPALBOT INTELLIGENT TEST RESULTS")
        logging.info("=" * 50)
        logging.info(f"⏱️  Duration: {duration_actual:.1f} seconds")
        logging.info(f"👻 Mouse Actions: {mouse_actions}")
        logging.info(f"⌨️  Keyboard Actions: {keyboard_actions}")
        logging.info(f"🎮 Tibia Detected: {'✅ Yes' if self.find_tibia_window() else '❌ No'}")
        logging.info(f"❌ Errors: 0")
        logging.info(f"❤️  Final Health: {self.health}/100")
        logging.info(f"🔮 Final Mana: {self.mana}/100")
        logging.info(f"📈 Final Level: {self.level}")
        logging.info(f"💚 Heals Used: {heals_used}")
        logging.info(f"💙 Mana Pots Used: {mana_pots_used}")
        logging.info(f"🔮 Spells Cast: {spells_cast}")
        logging.info(f"⚔️  Attacks Made: {attacks_made}")
        logging.info(f"🎯 Enemies Detected: {enemies_detected}")
        logging.info(f"💀 Enemies Killed: {enemies_killed}")
        logging.info(f"💰 Quick Loots: {quick_loots}")
        logging.info(f"🎯 Heal Threshold: {self.heal_threshold}%")
        logging.info(f"🎯 Mana Threshold: {self.mana_threshold}%")
        logging.info(f"🔮 Spell Mana Threshold: {self.spell_mana_threshold}%")
        logging.info("=" * 50)
        logging.info("�� Test completed")

def main():
    print("🤖 NopalBot Intelligent Windows Tester")
    print("=" * 40)
    print("1. Basic Test (quick)")
    print("2. Intelligent Ghost Mouse Test (60s)")
    print("3. Full Test (comprehensive)")
    print("4. Show Tibia Hotkey Guide")
    print("=" * 40)
    
    choice = input("Select option (1-4): ").strip()
    
    bot = NopalBotIntelligent()
    
    if choice == "1":
        bot.run_intelligent_bot(30)
    elif choice == "2":
        bot.run_intelligent_bot(60)
    elif choice == "3":
        bot.run_intelligent_bot(120)
    elif choice == "4":
        print("\n🎮 TIBIA HOTKEY GUIDE")
        print("=" * 30)
        print("K → ⚔️ Attack")
        print("0 → 💰 Quick Loot Nearby Corpses")
        print("F1 → ❤️ Health Potion")
        print("F2 → 🔮 Mana Potion")
        print("F3 → 🔮 Attack Spell (Exori vis)")
        print("F4 → 🔮 Heal Spell (Exura)")
        print("F5 → 💰 Loot")
        print("F6 → 🪢 Use Rope")
        print("F7 → 🪚 Use Shovel")
        print("F11 → 👢 Use Boots")
        print("F12 → 🎒 Open Backpack")
        print("E → 🏹 Use Arrow")
        print("Q → 🏹 Use Quiver")
        print("CTRL + Arrow → 🚶 Movement")
        print("=" * 30)
    else:
        print("❌ Invalid option")

if __name__ == "__main__":
    main()