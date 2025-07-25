"""
Módulo de configuración para NopalBot
Maneja la carga y gestión de configuraciones desde JSON
"""

import json
import os
from typing import Dict, Any

class BotConfig:
    """Clase para manejar la configuración del bot"""
    
    def __init__(self, config_path: str = "config/bot_config.json"):
        self.config_path = config_path
        self.config = self.load_config()
    
    def load_config(self) -> Dict[str, Any]:
        """Carga la configuración desde el archivo JSON"""
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                # Configuración por defecto si no existe el archivo
                return self.get_default_config()
        except Exception as e:
            print(f"Error cargando configuración: {e}")
            return self.get_default_config()
    
    def save_config(self) -> bool:
        """Guarda la configuración actual en el archivo JSON"""
        try:
            os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error guardando configuración: {e}")
            return False
    
    def get_default_config(self) -> Dict[str, Any]:
        """Retorna la configuración por defecto"""
        return {
            "vocation": "elite_knight",
            "hotkeys": {
                "attack": "ctrl+space",
                "next_target": "space",
                "exori": "f5",
                "exori_ico": "f6",
                "exori_gran": "f7",
                "utani_hur": "f8",
                "utito_tempo": "f9",
                "food": "f12",
                "mana_potion": "f11",
                "rune": "r",
                "quick_loot": "0",
                "stop": "f10",
                "pause": "f11"
            },
            "thresholds": {
                "heal": 50,
                "mana": 40,
                "food": 80
            },
            "timing": {
                "attack_delay": 0.5,
                "spell_delay": 1.0,
                "movement_delay": 0.3,
                "heal_delay": 2.0,
                "mana_delay": 3.0,
                "food_delay": 10.0
            },
            "movement": {
                "auto_exploration": True,
                "avoid_stairs": True,
                "anti_stuck_enabled": True,
                "direction_change_interval": 15
            },
            "combat": {
                "auto_attack": True,
                "auto_spells": True,
                "auto_runes": False,
                "target_priority": "closest"
            },
            "features": {
                "computer_vision": True,
                "mapping": True,
                "overlay": True,
                "auto_loot": True
            }
        }
    
    def get_hotkey(self, action: str) -> str:
        """Obtiene un hotkey específico"""
        return self.config.get("hotkeys", {}).get(action, "")
    
    def get_threshold(self, type_: str) -> int:
        """Obtiene un threshold específico"""
        return self.config.get("thresholds", {}).get(type_, 50)
    
    def get_timing(self, action: str) -> float:
        """Obtiene un timing específico"""
        return self.config.get("timing", {}).get(action, 1.0)
    
    def get_feature(self, feature: str) -> bool:
        """Obtiene el estado de una feature desde cualquier sección"""
        # Buscar en features primero
        if feature in self.config.get("features", {}):
            return self.config["features"][feature]
        
        # Buscar en combat
        if feature in self.config.get("combat", {}):
            return self.config["combat"][feature]
        
        # Buscar en movement
        if feature in self.config.get("movement", {}):
            return self.config["movement"][feature]
        
        # Si no se encuentra, retornar False
        return False
    
    def update_config(self, section: str, key: str, value: Any) -> bool:
        """Actualiza una configuración específica"""
        try:
            if section not in self.config:
                self.config[section] = {}
            self.config[section][key] = value
            return self.save_config()
        except Exception as e:
            print(f"Error actualizando configuración: {e}")
            return False

# Instancia global de configuración
config = BotConfig() 