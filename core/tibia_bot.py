"""
Main Tibia Bot
Refactored and modular Tibia bot with clean architecture
"""

import time
import signal
import sys
import logging
from typing import Optional
from utils.window_manager import WindowManager
from utils.input_manager import InputManager
from core.bot_features import BotFeatures

class TibiaBot:
    """Main Tibia bot class"""
    
    def __init__(self, log_file: str = "logs/tibia_bot.log"):
        self.logger = self._setup_logger(log_file)
        self.running = False
        
        # Initialize components
        self.window_manager = WindowManager()
        self.input_manager = InputManager(self.window_manager)
        self.features = BotFeatures(self.window_manager, self.input_manager)
        
        # Setup signal handlers
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
    
    def _setup_logger(self, log_file: str) -> logging.Logger:
        """Setup main bot logger"""
        logger = logging.getLogger('TibiaBot')
        logger.setLevel(logging.INFO)
        
        # Clear existing handlers
        for handler in logger.handlers[:]:
            logger.removeHandler(handler)
        
        # File handler
        fh = logging.FileHandler(log_file)
        fh.setLevel(logging.INFO)
        
        # Console handler
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        
        # Formatter
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)
        
        logger.addHandler(fh)
        logger.addHandler(ch)
        
        return logger
    
    def _signal_handler(self, signum, frame):
        """Handle shutdown signals"""
        self.logger.info(f"Señal recibida: {signum}")
        self.stop()
        sys.exit(0)
    
    def initialize(self) -> bool:
        """Initialize the bot"""
        try:
            self.logger.info("=== INICIANDO TIBIA BOT ===")
            
            # Setup Tibia window
            if not self.window_manager.setup_tibia_window():
                self.logger.error("No se pudo configurar la ventana de Tibia")
                return False
            
            # Test input
            if not self.input_manager.test_input():
                self.logger.error("No se pudo verificar el input")
                return False
            
            self.logger.info("Bot inicializado correctamente")
            return True
            
        except Exception as e:
            self.logger.error(f"Error inicializando bot: {e}")
            return False
    
    def start(self) -> bool:
        """Start the bot"""
        if self.running:
            self.logger.warning("Bot ya está ejecutándose")
            return False
        
        if not self.initialize():
            return False
        
        self.running = True
        self.logger.info("🚀 Iniciando funcionalidades del bot...")
        
        # Start all features
        if not self.features.start_all_features():
            self.logger.error("Error iniciando funcionalidades")
            return False
        
        self.logger.info("🎉 BOT FUNCIONANDO!")
        self.logger.info("💡 El bot está:")
        self.logger.info("   - Caminando automáticamente")
        self.logger.info("   - Looteando automáticamente")
        self.logger.info("   - Atacando cada 2 segundos")
        self.logger.info("   - Monitoreando input cada 5s")
        self.logger.info("   - Arreglando problemas automáticamente")
        self.logger.info("")
        self.logger.info("Presiona Ctrl+C para detener...")
        
        return True
    
    def stop(self) -> bool:
        """Stop the bot"""
        if not self.running:
            return False
        
        self.logger.info("🛑 Deteniendo bot...")
        self.running = False
        
        # Stop all features
        self.features.stop_all_features()
        
        self.logger.info("✅ Bot detenido correctamente")
        return True
    
    def run(self) -> None:
        """Main run loop"""
        if not self.start():
            self.logger.error("No se pudo iniciar el bot")
            return
        
        try:
            # Main loop
            while self.running:
                time.sleep(1)
                
                # Check if features are still running
                status = self.features.get_status()
                if not status['running']:
                    self.logger.warning("Funcionalidades detenidas inesperadamente")
                    break
                    
        except KeyboardInterrupt:
            self.logger.info("Interrupción de teclado recibida")
        except Exception as e:
            self.logger.error(f"Error en el bucle principal: {e}")
        finally:
            self.stop()
    
    def get_status(self) -> dict:
        """Get current bot status"""
        return {
            'running': self.running,
            'features': self.features.get_status(),
            'window_focused': self.window_manager.is_window_focused(self.window_manager.tibia_hwnd) if self.window_manager.tibia_hwnd else False
        }
    
    def test_input(self) -> bool:
        """Test if input is working"""
        return self.input_manager.test_input()
    
    def send_attack(self) -> bool:
        """Send a single attack"""
        return self.input_manager.send_attack()

def main():
    """Main entry point"""
    bot = TibiaBot()
    bot.run()

if __name__ == "__main__":
    main() 