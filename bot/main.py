"""
NopalBot - Main Bot Logic
By Taquito Loco 🎮
Enhanced version with spells, movement, and configuration
"""

import time
import threading
import logging
import json
import os
from datetime import datetime

class NopalBot:
    """Enhanced NopalBot with spells, movement, and configuration"""
    
    def __init__(self, config, bot_name="nopal_bot"):
        self.config = config
        self.bot_name = bot_name
        self.running = False
        self.threads = []
        
        # Setup logging
        self.setup_logging()
        
        # Bot state
        self.health = 100
        self.mana = 100
        self.level = 1
        self.experience = 0
        
        # Features
        self.auto_attack = config.get('auto_attack', True)
        self.auto_movement = config.get('auto_movement', True)
        self.auto_loot = config.get('auto_loot', True)
        self.spell_casting = config.get('spell_casting', True)
        
        # Hotkeys
        self.hotkeys = config.get('hotkeys', {
            'attack': 'space',
            'heal': 'f1',
            'spell1': 'f2',
            'spell2': 'f3',
            'loot': 'f4',
            'emergency': 'f12'
        })
        
        self.logger.info("NopalBot inicializado con configuración completa")
        
    def setup_logging(self):
        """Setup logging for the bot"""
        # Create logs directory if it doesn't exist
        os.makedirs("logs", exist_ok=True)
        
        # Configure logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(f'logs/{self.bot_name}.log'),
                logging.StreamHandler()
            ]
        )
        
        self.logger = logging.getLogger(self.bot_name)
        
    def start(self):
        """Start the bot"""
        self.logger.info(f"🚀 Iniciando NopalBot '{self.bot_name}'...")
        self.running = True
        
        # Start feature threads
        if self.auto_attack:
            self.start_attack_thread()
            
        if self.auto_movement:
            self.start_movement_thread()
            
        if self.auto_loot:
            self.start_loot_thread()
            
        if self.spell_casting:
            self.start_spell_thread()
            
        self.logger.info("✅ NopalBot iniciado exitosamente")
        
    def stop(self):
        """Stop the bot"""
        self.logger.info("🛑 Deteniendo NopalBot...")
        self.running = False
        
        # Wait for threads to finish
        for thread in self.threads:
            if thread.is_alive():
                thread.join(timeout=2)
                
        self.logger.info("✅ NopalBot detenido")
        
    def start_attack_thread(self):
        """Start attack thread"""
        thread = threading.Thread(target=self.attack_loop, daemon=True)
        thread.start()
        self.threads.append(thread)
        self.logger.info("⚔️ Thread de ataque iniciado")
        
    def start_movement_thread(self):
        """Start movement thread"""
        thread = threading.Thread(target=self.movement_loop, daemon=True)
        thread.start()
        self.threads.append(thread)
        self.logger.info("🚶 Thread de movimiento iniciado")
        
    def start_loot_thread(self):
        """Start loot thread"""
        thread = threading.Thread(target=self.loot_loop, daemon=True)
        thread.start()
        self.threads.append(thread)
        self.logger.info("💰 Thread de loot iniciado")
        
    def start_spell_thread(self):
        """Start spell casting thread"""
        thread = threading.Thread(target=self.spell_loop, daemon=True)
        thread.start()
        self.threads.append(thread)
        self.logger.info("🔮 Thread de hechizos iniciado")
        
    def attack_loop(self):
        """Attack loop"""
        while self.running:
            try:
                # Simulate attack
                self.logger.debug("⚔️ Atacando...")
                time.sleep(2)
            except Exception as e:
                self.logger.error(f"Error en ataque: {e}")
                
    def movement_loop(self):
        """Movement loop with stair detection"""
        while self.running:
            try:
                # Simulate movement with stair detection
                self.logger.debug("🚶 Moviéndose...")
                
                # Anti-stuck mechanism
                if self.detect_stuck():
                    self.logger.info("🪜 Detectado escalera, moviendo verticalmente")
                    
                time.sleep(1)
            except Exception as e:
                self.logger.error(f"Error en movimiento: {e}")
                
    def loot_loop(self):
        """Loot loop"""
        while self.running:
            try:
                # Simulate loot collection
                self.logger.debug("💰 Recolectando loot...")
                time.sleep(5)
            except Exception as e:
                self.logger.error(f"Error en loot: {e}")
                
    def spell_loop(self):
        """Spell casting loop"""
        while self.running:
            try:
                # Simulate spell casting
                if self.mana > 20:
                    self.logger.debug("🔮 Lanzando hechizo...")
                    self.mana -= 10
                time.sleep(3)
            except Exception as e:
                self.logger.error(f"Error en hechizos: {e}")
                
    def detect_stuck(self):
        """Detect if bot is stuck (simulated)"""
        # Simulate stuck detection
        return False
        
    def get_status(self):
        """Get bot status"""
        return {
            "running": self.running,
            "bot_name": self.bot_name,
            "health": self.health,
            "mana": self.mana,
            "level": self.level,
            "experience": self.experience,
            "features": {
                "auto_attack": self.auto_attack,
                "auto_movement": self.auto_movement,
                "auto_loot": self.auto_loot,
                "spell_casting": self.spell_casting
            }
        } 