"""
Language Manager for Bilingual Logging

This module provides bilingual logging capabilities for the Tibia Bot,
supporting both English and Mexican Spanish.
"""

import logging
from typing import Dict, Any, Optional
from enum import Enum


class Language(Enum):
    """Supported languages."""
    ENGLISH = "en"
    SPANISH_MEXICAN = "es_mx"


class LanguageManager:
    """
    Manages bilingual logging and messages for the Tibia Bot.
    
    Supports English and Mexican Spanish with authentic Mexican expressions.
    """
    
    def __init__(self, language: Language = Language.ENGLISH):
        """
        Initialize the LanguageManager.
        
        Args:
            language: Default language for messages
        """
        self.language = language
        self.logger = logging.getLogger(__name__)
        
        # Bilingual message dictionaries
        self.messages = {
            Language.ENGLISH: {
                # Bot status messages
                "bot_initialized": "Bot initialized successfully",
                "bot_started": "Bot started successfully",
                "bot_stopped": "Bot stopped",
                "bot_paused": "Bot paused",
                "bot_resumed": "Bot resumed",
                
                # Safety messages
                "safe_mode_enabled": "Safe mode enabled",
                "test_mode_enabled": "Test mode enabled",
                "emergency_stop": "Emergency stop activated",
                "action_rate_limit": "Action rate limit reached",
                
                # Window detection
                "window_found": "Tibia window found",
                "window_not_found": "Tibia window not found",
                "window_lost": "Tibia window lost",
                
                # State transitions
                "state_idle": "Entering IDLE state",
                "state_healing": "Entering HEALING state",
                "state_combat": "Entering COMBAT state",
                "state_looting": "Entering LOOTING state",
                "state_navigating": "Entering NAVIGATING state",
                "state_error": "Entering ERROR state",
                
                # Actions
                "auto_heal_triggered": "Auto-heal triggered",
                "auto_attack_triggered": "Auto-attack triggered",
                "auto_loot_triggered": "Auto-loot triggered",
                "navigation_started": "Navigation started",
                
                # Errors
                "capture_error": "Screen capture error",
                "config_error": "Configuration error",
                "initialization_error": "Initialization error",
                "safety_violation": "Safety violation detected",
                
                # Performance
                "performance_warning": "Performance warning",
                "memory_usage": "Memory usage",
                "cpu_usage": "CPU usage",
                
                # User messages
                "welcome": "Welcome to Tibia Bot!",
                "ready": "Bot is ready to use",
                "testing": "Running in test mode",
                "monitoring": "Monitoring active"
            },
            
            Language.SPANISH_MEXICAN: {
                # Bot status messages
                "bot_initialized": "¡Órale! El bot ya está listo, carnal",
                "bot_started": "¡Ya arrancó el bot, compa!",
                "bot_stopped": "Ya paré el bot, wey",
                "bot_paused": "El bot está en pausa, carnal",
                "bot_resumed": "¡Ya siguió el bot, compa!",
                
                # Safety messages
                "safe_mode_enabled": "¡Modo seguro activado, no te preocupes!",
                "test_mode_enabled": "Modo de prueba activado, todo chido",
                "emergency_stop": "¡ALTO! Parada de emergencia activada",
                "action_rate_limit": "Ya llegaste al límite de acciones, espérate tantito",
                
                # Window detection
                "window_found": "¡Órale! Ya encontré la ventana de Tibia",
                "window_not_found": "No encuentro la ventana de Tibia, carnal",
                "window_lost": "Se perdió la ventana de Tibia, wey",
                
                # State transitions
                "state_idle": "Estoy en modo relax, carnal",
                "state_healing": "¡Me estoy curando, compa!",
                "state_combat": "¡A la guerra, carnal!",
                "state_looting": "¡A recoger el botín, wey!",
                "state_navigating": "¡Voy para allá, compa!",
                "state_error": "¡Ups! Algo salió mal, carnal",
                
                # Actions
                "auto_heal_triggered": "¡Me curé automáticamente, compa!",
                "auto_attack_triggered": "¡Le di al monstruo, carnal!",
                "auto_loot_triggered": "¡Ya recogí el loot, wey!",
                "navigation_started": "¡Ya empecé a navegar, compa!",
                
                # Errors
                "capture_error": "No pude capturar la pantalla, carnal",
                "config_error": "Hay un problema con la configuración, wey",
                "initialization_error": "No pude inicializar el bot, compa",
                "safety_violation": "¡Cuidado! Violación de seguridad detectada",
                
                # Performance
                "performance_warning": "¡Ojo! Advertencia de rendimiento",
                "memory_usage": "Uso de memoria",
                "cpu_usage": "Uso de CPU",
                
                # User messages
                "welcome": "¡Órale! Bienvenido al Bot de Tibia",
                "ready": "¡El bot ya está listo, carnal!",
                "testing": "Estoy en modo de prueba, todo chido",
                "monitoring": "¡Estoy monitoreando, compa!"
            }
        }
    
    def get_message(self, key: str, **kwargs) -> str:
        """
        Get a message in the current language.
        
        Args:
            key: Message key
            **kwargs: Format parameters
            
        Returns:
            Formatted message in current language
        """
        if self.language not in self.messages:
            self.language = Language.ENGLISH
        
        if key not in self.messages[self.language]:
            # Fallback to English if message not found
            if key in self.messages[Language.ENGLISH]:
                return self.messages[Language.ENGLISH][key].format(**kwargs)
            return f"Message not found: {key}"
        
        return self.messages[self.language][key].format(**kwargs)
    
    def set_language(self, language: Language):
        """Set the current language."""
        self.language = language
        self.logger.info(f"Language changed to: {language.value}")
    
    def log_info(self, key: str, **kwargs):
        """Log an info message in the current language."""
        message = self.get_message(key, **kwargs)
        self.logger.info(message)
    
    def log_warning(self, key: str, **kwargs):
        """Log a warning message in the current language."""
        message = self.get_message(key, **kwargs)
        self.logger.warning(message)
    
    def log_error(self, key: str, **kwargs):
        """Log an error message in the current language."""
        message = self.get_message(key, **kwargs)
        self.logger.error(message)
    
    def log_debug(self, key: str, **kwargs):
        """Log a debug message in the current language."""
        message = self.get_message(key, **kwargs)
        self.logger.debug(message)
    
    def get_bilingual_message(self, key: str, **kwargs) -> Dict[str, str]:
        """
        Get a message in both languages.
        
        Args:
            key: Message key
            **kwargs: Format parameters
            
        Returns:
            Dictionary with messages in both languages
        """
        return {
            "english": self.messages[Language.ENGLISH].get(key, f"Message not found: {key}").format(**kwargs),
            "spanish": self.messages[Language.SPANISH_MEXICAN].get(key, f"Mensaje no encontrado: {key}").format(**kwargs)
        }


# Global language manager instance
language_manager = LanguageManager(Language.ENGLISH)


def set_global_language(language: Language):
    """Set the global language for the entire application."""
    global language_manager
    language_manager.set_language(language)


def get_message(key: str, **kwargs) -> str:
    """Get a message using the global language manager."""
    return language_manager.get_message(key, **kwargs)


def log_info(key: str, **kwargs):
    """Log info using the global language manager."""
    language_manager.log_info(key, **kwargs)


def log_warning(key: str, **kwargs):
    """Log warning using the global language manager."""
    language_manager.log_warning(key, **kwargs)


def log_error(key: str, **kwargs):
    """Log error using the global language manager."""
    language_manager.log_error(key, **kwargs)


def log_debug(key: str, **kwargs):
    """Log debug using the global language manager."""
    language_manager.log_debug(key, **kwargs) 