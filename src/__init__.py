"""
NopalBot Elite Knight - Paquete principal
Bot especializado para farming automático - by Pikos Nopal
"""

__version__ = "2.0.0"
__author__ = "Pikos Nopal"
__description__ = "Bot especializado para Elite Knight en Tibia"

from .bot import NopalBotEliteKnight
from .gui import NopalBotEliteKnightGUI
from .config import config
from .utils import logger, anti_stuck, InputManager, WindowManager
from .vision import cv_system

__all__ = [
    'NopalBotEliteKnight',
    'NopalBotEliteKnightGUI', 
    'config',
    'logger',
    'anti_stuck',
    'InputManager',
    'WindowManager',
    'cv_system'
]
