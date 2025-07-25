"""
Módulo principal del bot NopalBot
Lógica core para Elite Knight - NopalBot by Pikos Nopal
"""

import time
import threading
import keyboard
from typing import Optional, Callable, Tuple
from .config import config
from .utils import logger, anti_stuck, InputManager, WindowManager
from .vision import cv_system

class NopalBotEliteKnight:
    """Bot especializado para Elite Knight - NopalBot by Pikos Nopal"""
    
    def __init__(self, gui_callback: Optional[Callable] = None):
        self.gui_callback = gui_callback
        self.running = False
        self.paused = False
        self.tibia_window = None
        
        # Configuración del bot
        self.auto_attack_enabled = config.get_feature("auto_attack")
        self.auto_walk_enabled = config.get_feature("auto_walk")
        self.auto_heal_enabled = config.get_feature("auto_heal")
        self.auto_mana_enabled = config.get_feature("auto_mana")
        self.auto_food_enabled = config.get_feature("auto_food")
        self.auto_spells_enabled = config.get_feature("auto_spells")
        self.auto_runes_enabled = config.get_feature("auto_runes")
        self.auto_loot_enabled = config.get_feature("auto_loot")
        self.computer_vision_enabled = config.get_feature("computer_vision")
        self.mapping_enabled = config.get_feature("mapping")
        
        # Contadores y estado
        self.health_potions = 100
        self.mana_potions = 100
        self.food_count = 50
        self.last_heal_time = 0
        self.last_mana_time = 0
        self.last_food_time = 0
        self.last_spell_time = 0
        self.last_rune_time = 0
        
        # SISTEMA DE COORDENADAS Y MOVIMIENTO (RESTAURADO)
        self.current_position = (0, 0)
        self.last_position = (0, 0)
        self.position_history = []
        self.movement_attempts = 0
        self.stuck_counter = 0
        self.max_stuck_attempts = 5
        self.visited_positions = set()
        self.movement_state = "forward"
        self.current_direction = "w"
        self.direction_change_time = time.time()
        self.direction_change_interval = config.get_timing("movement_delay")
        
        # Thread principal
        self.bot_thread = None
        
        # Configurar hotkeys
        self.setup_hotkeys()
    
    def log_to_gui(self, message: str):
        """Envía log a la GUI"""
        if self.gui_callback:
            self.gui_callback(message)
        logger.log(message)
    
    def setup_hotkeys(self):
        """Configura hotkeys globales"""
        try:
            keyboard.add_hotkey(config.get_hotkey("stop"), self.stop_bot)
            keyboard.add_hotkey(config.get_hotkey("pause"), self.toggle_pause)
            self.log_to_gui("✅ Hotkeys configurados")
        except Exception as e:
            self.log_to_gui(f"❌ Error configurando hotkeys: {e}")
    
    def simple_attack(self):
        """Ataque simple con verificación y click en enemigo"""
        if not self.auto_attack_enabled:
            return
        
        try:
            # Activar ventana de Tibia
            if not WindowManager.activate_tibia_window():
                return
            
            # Si Computer Vision está habilitado, buscar enemigo más cercano
            if self.computer_vision_enabled:
                cv_data = cv_system.computer_vision_scan()
                if cv_data['enemies']:
                    closest_enemy = cv_system.find_closest_enemy(cv_data['enemies'])
                    if closest_enemy:
                        # Click en el enemigo
                        if InputManager.send_mouse_click(closest_enemy[0], closest_enemy[1]):
                            self.log_to_gui(f"🎯 Click en enemigo en ({closest_enemy[0]}, {closest_enemy[1]})")
                            time.sleep(0.1)
            
            # Enviar ataque con triple verificación
            attack_key = config.get_hotkey("attack")
            if InputManager.triple_check_tibia_input(attack_key):
                self.log_to_gui("⚔️ Ataque enviado")
                time.sleep(config.get_timing("attack_delay"))
                
                # Enviar next target también
                next_target_key = config.get_hotkey("next_target")
                if InputManager.send_keyboard_input(next_target_key):
                    self.log_to_gui("🎯 Next target enviado")
            else:
                self.log_to_gui("❌ Error enviando ataque")
                
        except Exception as e:
            self.log_to_gui(f"❌ Error en ataque: {e}")
    
    def intelligent_attack(self):
        """Ataque inteligente con detección de enemigos"""
        if not self.auto_attack_enabled:
            return
        
        try:
            # Verificar si hay enemigos
            if self.computer_vision_enabled:
                cv_data = cv_system.computer_vision_scan()
                if not cv_data['enemies']:
                    return  # No hay enemigos, no atacar
            
            # Realizar ataque
            self.simple_attack()
            
            # Loot automático después del ataque
            time.sleep(1)  # Esperar 1 segundo
            self.auto_loot()
            
        except Exception as e:
            self.log_to_gui(f"❌ Error en ataque inteligente: {e}")
    
    def auto_heal(self):
        """Curación automática"""
        if not self.auto_heal_enabled:
            return
        
        current_time = time.time()
        if current_time - self.last_heal_time < config.get_timing("heal_delay"):
            return
        
        try:
            # Detectar HP actual (simulado)
            image = cv_system.capture_tibia_screen()
            if image is not None:
                health_percent, _ = cv_system.detect_health_mana_from_screen(image)
            else:
                health_percent = 100  # Default si no se puede detectar
            
            # Verificar si necesita curación
            heal_threshold = config.get_threshold("heal")
            if health_percent < heal_threshold and self.health_potions > 0:
                # Usar poción de curación con la tecla correcta
                heal_key = config.get_hotkey("health_potion")
                if InputManager.send_keyboard_input(heal_key):
                    self.health_potions -= 1
                    self.last_heal_time = current_time
                    self.log_to_gui(f"💚 Curación automática (HP: {health_percent}% < {heal_threshold}%)")
                    
        except Exception as e:
            self.log_to_gui(f"❌ Error en curación: {e}")
    
    def auto_mana(self):
        """Mana automático"""
        if not self.auto_mana_enabled:
            return
        
        current_time = time.time()
        if current_time - self.last_mana_time < config.get_timing("mana_delay"):
            return
        
        try:
            # Detectar Mana actual (simulado)
            image = cv_system.capture_tibia_screen()
            if image is not None:
                _, mana_percent = cv_system.detect_health_mana_from_screen(image)
            else:
                mana_percent = 100  # Default
            
            # Verificar si necesita mana
            mana_threshold = config.get_threshold("mana")
            if mana_percent < mana_threshold and self.mana_potions > 0:
                mana_key = config.get_hotkey("mana_potion")
                if InputManager.send_keyboard_input(mana_key):
                    self.mana_potions -= 1
                    self.last_mana_time = current_time
                    self.log_to_gui(f"🔵 Mana automático (Mana: {mana_percent}% < {mana_threshold}%)")
                    
        except Exception as e:
            self.log_to_gui(f"❌ Error en mana: {e}")
    
    def auto_food(self):
        """Comida automática"""
        if not self.auto_food_enabled:
            return
        
        current_time = time.time()
        if current_time - self.last_food_time < config.get_timing("food_delay"):
            return
        
        try:
            if self.food_count > 0:
                food_key = config.get_hotkey("food")
                if InputManager.send_keyboard_input(food_key):
                    self.food_count -= 1
                    self.last_food_time = current_time
                    self.log_to_gui(f"🍖 Comida automática ({self.food_count} restantes)")
                    
        except Exception as e:
            self.log_to_gui(f"❌ Error en comida: {e}")
    
    def cast_spell(self, spell_name: str, hotkey: str):
        """Lanza un hechizo específico"""
        if not self.auto_spells_enabled:
            return
        
        current_time = time.time()
        if current_time - self.last_spell_time < config.get_timing("spell_delay"):
            return
        
        try:
            if InputManager.send_keyboard_input(hotkey):
                self.last_spell_time = current_time
                self.log_to_gui(f"🔮 {spell_name} lanzado")
                time.sleep(config.get_timing("spell_delay"))
                
        except Exception as e:
            self.log_to_gui(f"❌ Error lanzando {spell_name}: {e}")
    
    def cast_utani_hur(self):
        """Lanza Utani Hur"""
        self.cast_spell("Utani Hur", config.get_hotkey("utani_hur"))
    
    def cast_exori(self):
        """Lanza Exori"""
        self.cast_spell("Exori", config.get_hotkey("exori"))
    
    def cast_exori_ico(self):
        """Lanza Exori Ico"""
        self.cast_spell("Exori Ico", config.get_hotkey("exori_ico"))
    
    def cast_exori_gran(self):
        """Lanza Exori Gran"""
        self.cast_spell("Exori Gran", config.get_hotkey("exori_gran"))
    
    def cast_utito_tempo(self):
        """Lanza Utito Tempo"""
        self.cast_spell("Utito Tempo", config.get_hotkey("utito_tempo"))
    
    def cast_rune(self):
        """Lanza runa"""
        if not self.auto_runes_enabled:
            return
        
        current_time = time.time()
        if current_time - self.last_rune_time < config.get_timing("spell_delay"):
            return
        
        try:
            rune_key = config.get_hotkey("rune")
            if InputManager.send_keyboard_input(rune_key):
                self.last_rune_time = current_time
                self.log_to_gui("💥 Runa lanzada")
                
        except Exception as e:
            self.log_to_gui(f"❌ Error lanzando runa: {e}")
    
    def smart_walk(self):
        """Movimiento inteligente con anti-stuck y evasión de obstáculos"""
        if not self.auto_walk_enabled:
            return
        
        try:
            # Cambiar dirección periódicamente para evitar patrones predecibles
            current_time = time.time()
            if current_time - self.direction_change_time > self.direction_change_interval:
                directions = ['w', 'a', 's', 'd']
                self.current_direction = directions[int(current_time) % len(directions)]
                self.direction_change_time = current_time
                self.log_to_gui(f"�� Cambiando dirección a: {self.current_direction}")
            
            # Verificar Computer Vision si está habilitado
            if self.computer_vision_enabled:
                cv_data = cv_system.computer_vision_scan()
                
                # Si hay enemigos, detener movimiento y atacar
                if cv_data['enemies']:
                    self.log_to_gui("⚔️ Enemigos detectados - deteniendo movimiento para atacar")
                    return
                
                # Evitar escaleras, portales y obstáculos
                if self.avoid_stairs(cv_data) or self.avoid_portals(cv_data) or self.avoid_obstacles(cv_data):
                    return
            
            # Verificar si está atascado ANTES de intentar moverse
            if self.is_stuck():
                self.log_to_gui("🚫 Personaje atascado - probando otras teclas")
                self.current_direction = self.try_all_movement_keys()
                self.reset_stuck_counter()
                return
            
            # Obtener posición actual antes del movimiento
            old_position = self.get_character_position()
            
            # Enviar movimiento
            if InputManager.send_keyboard_input(self.current_direction):
                time.sleep(0.2)  # Esperar a que el movimiento se procese
                
                # Obtener nueva posición después del movimiento
                new_position = self.get_character_position()
                
                # Verificar si la posición cambió
                if self.check_position_change(new_position):
                    self.log_to_gui(f"✅ Movimiento exitoso: {self.current_direction} - ({old_position[0]},{old_position[1]}) → ({new_position[0]},{new_position[1]})")
                    self.reset_stuck_counter()
                    
                    # Actualizar posición en el bot
                    self.update_position()
                else:
                    self.log_to_gui(f"⚠️ Posición no cambió con {self.current_direction} - ({old_position[0]},{old_position[1]})")
                    self.stuck_counter += 1
                    
                    # Si se está atascando, probar otra tecla
                    if self.stuck_counter >= 3:
                        self.log_to_gui("🔄 Probando otra tecla de movimiento")
                        self.current_direction = self.try_all_movement_keys()
                        self.reset_stuck_counter()
                    
        except Exception as e:
            self.log_to_gui(f"❌ Error en movimiento: {e}")
    
    def get_character_position(self) -> Tuple[int, int]:
        """Obtiene la posición real del personaje en Tibia"""
        try:
            # En una implementación real, esto obtendría las coordenadas de Tibia
            # Por ahora, simulamos con valores que cambian cuando se mueve
            
            # Si no hay historial, empezar en posición inicial
            if not self.position_history:
                return (100, 100)
            
            # Obtener la última posición conocida
            last_pos = self.position_history[-1]
            
            # Simular movimiento basado en la dirección actual
            if self.current_direction == "w":
                new_pos = (last_pos[0], last_pos[1] - 1)
            elif self.current_direction == "s":
                new_pos = (last_pos[0], last_pos[1] + 1)
            elif self.current_direction == "a":
                new_pos = (last_pos[0] - 1, last_pos[1])
            elif self.current_direction == "d":
                new_pos = (last_pos[0] + 1, last_pos[1])
            else:
                new_pos = last_pos
            
            return new_pos
            
        except Exception as e:
            self.log_to_gui(f"❌ Error obteniendo posición: {e}")
            return (0, 0)
    
    def update_position(self):
        """Actualiza la posición actual del personaje"""
        try:
            # Obtener posición real (o simulada)
            new_pos = self.get_character_position()
            
            # Actualizar historial de posiciones
            self.position_history.append(new_pos)
            if len(self.position_history) > 10:
                self.position_history.pop(0)
            
            # Guardar posición anterior
            self.last_position = self.current_position
            self.current_position = new_pos
            
            # Agregar a posiciones visitadas si mapping está habilitado
            if self.mapping_enabled:
                self.visited_positions.add(new_pos)
            
            self.log_to_gui(f"📍 Posición actualizada: ({new_pos[0]}, {new_pos[1]})")
            
        except Exception as e:
            self.log_to_gui(f"❌ Error actualizando posición: {e}")
    
    def check_position_change(self, new_position: Tuple[int, int]) -> bool:
        """Verifica si la posición cambió"""
        if self.last_position == (0, 0):
            self.last_position = new_position
            return True
        
        # Calcular distancia
        dx = abs(new_position[0] - self.last_position[0])
        dy = abs(new_position[1] - self.last_position[1])
        
        # Si la posición cambió significativamente
        if dx > 0 or dy > 0:  # Cualquier cambio cuenta
            self.stuck_counter = 0
            self.last_position = new_position
            return True
        
        self.stuck_counter += 1
        return False
    
    def is_stuck(self) -> bool:
        """Determina si el personaje está atascado"""
        return self.stuck_counter >= self.max_stuck_attempts
    
    def try_all_movement_keys(self) -> str:
        """Intenta todas las teclas de movimiento hasta encontrar una que funcione"""
        keys = ['w', 'a', 's', 'd']
        random.shuffle(keys)  # Orden aleatorio
        
        for key in keys:
            self.log_to_gui(f"🔄 Probando tecla: {key}")
            
            if InputManager.send_keyboard_input(key):
                time.sleep(0.3)  # Esperar más tiempo
                
                # Obtener nueva posición
                new_pos = self.get_character_position()
                
                if self.check_position_change(new_pos):
                    self.log_to_gui(f"✅ Movimiento exitoso con tecla: {key}")
                    return key
                else:
                    self.log_to_gui(f"❌ Tecla {key} no funcionó")
        
        self.log_to_gui("⚠️ Ninguna tecla funcionó, usando 'w' por defecto")
        return 'w'
    
    def reset_stuck_counter(self):
        """Resetea el contador de stuck"""
        self.stuck_counter = 0
        self.log_to_gui("🔄 Contador de stuck reseteado")
    
    def avoid_stairs(self, cv_data: dict) -> bool:
        """Evita escaleras si están detectadas"""
        if cv_data.get('stairs') and config.get_feature("avoid_stairs"):
            self.log_to_gui("⚠️ Escaleras detectadas - evitando")
            return True
        return False
    
    def avoid_portals(self, cv_data: dict) -> bool:
        """Evita portales si están detectados"""
        if cv_data.get('portals'):
            self.log_to_gui("⚠️ Portales detectados - evitando")
            return True
        return False
    
    def avoid_obstacles(self, cv_data: dict) -> bool:
        """Evita obstáculos si están detectados"""
        if cv_data.get('obstacles'):
            self.log_to_gui("⚠️ Obstáculos detectados - evitando")
            return True
        return False
    
    def auto_loot(self):
        """Loot automático"""
        if not self.auto_loot_enabled:
            return
        
        try:
            loot_key = config.get_hotkey("quick_loot")
            if InputManager.send_keyboard_input(loot_key):
                self.log_to_gui("💰 Loot automático")
                time.sleep(1)  # Esperar 1 segundo después del loot
                
        except Exception as e:
            self.log_to_gui(f"❌ Error en loot: {e}")
    
    def toggle_pause(self):
        """Alterna pausa del bot"""
        self.paused = not self.paused
        status = "⏸️ PAUSADO" if self.paused else "▶️ REANUDADO"
        self.log_to_gui(f"{status}")
    
    def stop_bot(self):
        """Detiene el bot"""
        self.running = False
        self.log_to_gui("🛑 Bot detenido")
    
    def run_bot(self):
        """Función principal del bot"""
        self.running = True
        self.log_to_gui("🚀 NopalBot Elite Knight iniciado")
        
        while self.running:
            try:
                if self.paused:
                    time.sleep(1)
                    continue
                
                # Activar ventana de Tibia
                if not WindowManager.activate_tibia_window():
                    self.log_to_gui("❌ Ventana de Tibia no encontrada")
                    time.sleep(5)
                    continue
                
                # Ejecutar funciones del bot en orden de prioridad
                
                # 1. Curación y mana (prioridad alta)
                self.auto_heal()
                self.auto_mana()
                self.auto_food()
                
                # 2. Verificar enemigos y atacar
                cv_data = {'enemies': []}  # Inicializar por defecto
                
                if self.computer_vision_enabled:
                    cv_data = cv_system.computer_vision_scan()
                    if cv_data['enemies']:
                        # Hay enemigos - atacar
                        self.log_to_gui("⚔️ Enemigos detectados - iniciando combate")
                        self.intelligent_attack()
                        
                        # Lanzar hechizos si están habilitados
                        if self.auto_spells_enabled:
                            self.cast_exori()
                            time.sleep(0.5)
                            self.cast_rune()
                    else:
                        # No hay enemigos - moverse
                        self.smart_walk()
                else:
                    # Computer Vision deshabilitado - atacar siempre si está habilitado
                    if self.auto_attack_enabled:
                        self.log_to_gui("⚔️ Auto Attack activado - atacando")
                        self.simple_attack()
                        
                        # Lanzar hechizos si están habilitados
                        if self.auto_spells_enabled:
                            self.cast_exori()
                            time.sleep(0.5)
                            self.cast_rune()
                    
                    # Moverse si está habilitado
                    if self.auto_walk_enabled:
                        self.smart_walk()
                
                # 3. Loot automático si no hay enemigos
                if not self.computer_vision_enabled or not cv_data.get('enemies'):
                    self.auto_loot()
                
                # Esperar antes del siguiente ciclo
                time.sleep(0.5)
                
            except Exception as e:
                self.log_to_gui(f"❌ Error en ciclo principal: {e}")
                time.sleep(1)
        
        self.log_to_gui("👋 NopalBot finalizado")
    
    def start(self):
        """Inicia el bot en un thread separado"""
        if not self.running:
            self.bot_thread = threading.Thread(target=self.run_bot, daemon=True)
            self.bot_thread.start()
            self.log_to_gui("🎯 Bot iniciado en thread separado")
    
    def get_status(self) -> dict:
        """Retorna el estado actual del bot"""
        return {
            'running': self.running,
            'paused': self.paused,
            'health_potions': self.health_potions,
            'mana_potions': self.mana_potions,
            'food_count': self.food_count,
            'current_position': self.current_position,
            'visited_positions': len(self.visited_positions)
        } 

    def save_map_data(self):
        """Guarda las coordenadas visitadas en un archivo JSON"""
        try:
            import json
            from datetime import datetime
            
            map_data = {
                "timestamp": datetime.now().isoformat(),
                "vocation": config.get_feature("vocation"),
                "visited_positions": list(self.visited_positions),
                "position_history": self.position_history,
                "total_positions": len(self.visited_positions),
                "description": "Coordenadas visitadas por NopalBot"
            }
            
            filename = f"logs/map_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            
            # Crear directorio logs si no existe
            import os
            os.makedirs("logs", exist_ok=True)
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(map_data, f, indent=2, ensure_ascii=False)
            
            self.log_to_gui(f"🗺️ Mapa guardado: {filename} ({len(self.visited_positions)} posiciones)")
            return filename
            
        except Exception as e:
            self.log_to_gui(f"❌ Error guardando mapa: {e}")
            return None
    
    def load_map_data(self, filename: str):
        """Carga coordenadas desde un archivo JSON"""
        try:
            import json
            
            with open(filename, 'r', encoding='utf-8') as f:
                map_data = json.load(f)
            
            # Cargar posiciones visitadas
            if 'visited_positions' in map_data:
                self.visited_positions = set(map_data['visited_positions'])
                self.log_to_gui(f"🗺️ Mapa cargado: {len(self.visited_positions)} posiciones")
            
            # Cargar historial de posiciones
            if 'position_history' in map_data:
                self.position_history = map_data['position_history']
                if self.position_history:
                    self.current_position = self.position_history[-1]
                    self.log_to_gui(f"📍 Posición actual: {self.current_position}")
            
            return True
            
        except Exception as e:
            self.log_to_gui(f"❌ Error cargando mapa: {e}")
            return False
    
    def export_coordinates_for_sharing(self):
        """Exporta coordenadas en formato para compartir"""
        try:
            import json
            from datetime import datetime
            
            # Crear archivo de coordenadas para compartir
            share_data = {
                "nopalbot_coordinates": {
                    "version": "1.0",
                    "created": datetime.now().isoformat(),
                    "author": "NopalBot by Pikos Nopal",
                    "description": "Coordenadas de farming para Elite Knight",
                    "positions": list(self.visited_positions),
                    "total_positions": len(self.visited_positions),
                    "usage": "Copiar este archivo a la carpeta logs/ y usar 'Cargar Mapa'"
                }
            }
            
            filename = f"logs/coordenadas_compartir_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            
            # Crear directorio logs si no existe
            import os
            os.makedirs("logs", exist_ok=True)
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(share_data, f, indent=2, ensure_ascii=False)
            
            self.log_to_gui(f"📤 Coordenadas exportadas para compartir: {filename}")
            self.log_to_gui(f"💡 Comparte este archivo con otros jugadores para que no tengan que explorar desde cero")
            return filename
            
        except Exception as e:
            self.log_to_gui(f"❌ Error exportando coordenadas: {e}")
            return None 