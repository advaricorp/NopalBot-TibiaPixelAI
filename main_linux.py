#!/usr/bin/env python3
"""
PBT Bot - Linux Server Version
Enhanced version for headless operation and multiple instances
By Taquito Loco 🎮
"""

import os
import sys
import time
import argparse
import signal
import logging
from pathlib import Path

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from bot.main import PBTBot
    from config.config_manager import ConfigManager
except ImportError as e:
    print(f"[ERROR] No se pudo importar módulos: {e}")
    sys.exit(1)

class LinuxPBTBot:
    """Linux-compatible PBT Bot with command line support"""
    
    def __init__(self, config_file: str = "config/bot_config.json", bot_name: str = "default"):
        self.config_file = config_file
        self.bot_name = bot_name
        self.bot = None
        self.running = False
        
        # Setup signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
        
        # Setup logging
        self._setup_logging()
        
        # Load configuration
        self.config = ConfigManager(config_file)
        
        self.logger.info(f"🤖 Linux PBT Bot '{bot_name}' initialized")
        self.logger.info(f"📁 Config: {config_file}")
    
    def _setup_logging(self):
        """Setup logging for Linux environment"""
        # Ensure logs directory exists
        os.makedirs("logs", exist_ok=True)
        
        # Create logger
        self.logger = logging.getLogger(f'PBTBot_{self.bot_name}')
        self.logger.setLevel(logging.INFO)
        
        # Clear existing handlers
        for handler in self.logger.handlers[:]:
            self.logger.removeHandler(handler)
        
        # File handler
        log_file = f"logs/pbt_bot_{self.bot_name}.log"
        fh = logging.FileHandler(log_file, encoding='utf-8')
        fh.setLevel(logging.INFO)
        
        # Console handler
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        
        # Formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)
        
        self.logger.addHandler(fh)
        self.logger.addHandler(ch)
    
    def _signal_handler(self, signum, frame):
        """Handle shutdown signals"""
        self.logger.info(f"📡 Received signal {signum}, shutting down gracefully...")
        self.stop()
    
    def start(self):
        """Start the bot"""
        try:
            self.logger.info(f"🚀 Starting PBT Bot '{self.bot_name}'...")
            
            # Create bot instance
            self.bot = PBTBot(f"logs/pbt_bot_{self.bot_name}.log")
            
            # Override config file if specified
            if self.config_file != "config/bot_config.json":
                self.bot.config = ConfigManager(self.config_file)
            
            # Start bot
            if self.bot.start():
                self.running = True
                self.logger.info(f"✅ Bot '{self.bot_name}' started successfully")
                
                # Keep running
                while self.running:
                    time.sleep(1)
                    
            else:
                self.logger.error(f"❌ Failed to start bot '{self.bot_name}'")
                return False
                
        except Exception as e:
            self.logger.error(f"❌ Error starting bot: {e}")
            return False
    
    def stop(self):
        """Stop the bot"""
        try:
            if self.bot:
                self.bot.stop()
            
            self.running = False
            self.logger.info(f"✅ Bot '{self.bot_name}' stopped")
            
        except Exception as e:
            self.logger.error(f"❌ Error stopping bot: {e}")
    
    def get_status(self):
        """Get bot status"""
        if self.bot:
            return self.bot.get_status()
        return {"running": False, "bot_name": self.bot_name}

def main():
    """Main function with command line argument support"""
    parser = argparse.ArgumentParser(
        description="PBT Bot - Linux Server Version",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 main_linux.py                           # Use default config
  python3 main_linux.py --config config/bot_config_1.json --name bot1
  python3 main_linux.py --config config/bot_config_2.json --name bot2
  python3 main_linux.py --headless --name headless_bot
        """
    )
    
    parser.add_argument(
        '--config', 
        default='config/bot_config.json',
        help='Configuration file path (default: config/bot_config.json)'
    )
    
    parser.add_argument(
        '--name', 
        default='default',
        help='Bot instance name (default: default)'
    )
    
    parser.add_argument(
        '--headless', 
        action='store_true',
        help='Run in headless mode (no GUI)'
    )
    
    parser.add_argument(
        '--log-level', 
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'],
        default='INFO',
        help='Logging level (default: INFO)'
    )
    
    args = parser.parse_args()
    
    # Set display for headless mode
    if args.headless:
        os.environ['DISPLAY'] = ':99'
        print("🖥️ Running in headless mode (DISPLAY=:99)")
    
    # Create and start bot
    bot = LinuxPBTBot(args.config, args.name)
    
    try:
        bot.start()
    except KeyboardInterrupt:
        print("\n🛑 Interrupted by user")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
    finally:
        bot.stop()

if __name__ == "__main__":
    main() 