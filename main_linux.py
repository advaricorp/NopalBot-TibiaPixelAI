#!/usr/bin/env python3
"""
NopalBot - Linux Server Version
By Taquito Loco 🎮
Optimized for Ubuntu 22.04 and WSL
"""

import sys
import os
import argparse
import logging
import signal
import time
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from bot.main import NopalBot
from config.config_manager import ConfigManager

class LinuxNopalBot:
    """Linux-compatible NopalBot with command line support"""
    
    def __init__(self, config_file="config/bot_config.json", bot_name="nopal_bot", headless=True):
        self.config_file = config_file
        self.bot_name = bot_name
        self.headless = headless
        self.bot = None
        self.running = False
        
        # Setup logging
        self.setup_logging()
        
        # Setup signal handlers
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
        
        self.logger.info(f"🤖 Linux NopalBot '{bot_name}' initialized")
        
    def setup_logging(self):
        """Setup logging configuration"""
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
        
    def signal_handler(self, signum, frame):
        """Handle shutdown signals gracefully"""
        self.logger.info(f"Received signal {signum}, shutting down gracefully...")
        self.stop()
        
    def load_config(self):
        """Load bot configuration"""
        try:
            config_manager = ConfigManager(self.config_file)
            config = config_manager.load_config()
            self.logger.info(f"Configuration loaded from {self.config_file}")
            return config
        except Exception as e:
            self.logger.error(f"Error loading configuration: {e}")
            return None
            
    def start(self):
        """Start the bot"""
        try:
            self.logger.info(f"🚀 Starting NopalBot '{self.bot_name}'...")
            
            # Load configuration
            config = self.load_config()
            if not config:
                self.logger.error("Failed to load configuration")
                return False
                
            # Initialize bot
            self.bot = NopalBot(config, bot_name=self.bot_name)
            
            # Set headless mode
            if self.headless:
                self.logger.info("Running in headless mode")
                os.environ['DISPLAY'] = ':99'
                
            # Start bot
            self.running = True
            self.bot.start()
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error starting bot: {e}")
            return False
            
    def stop(self):
        """Stop the bot"""
        if self.running:
            self.logger.info("Stopping bot...")
            self.running = False
            if self.bot:
                self.bot.stop()
            self.logger.info("Bot stopped")
            
    def run(self):
        """Main run loop"""
        if self.start():
            try:
                while self.running:
                    time.sleep(1)
            except KeyboardInterrupt:
                self.logger.info("Bot interrupted by user")
            finally:
                self.stop()
        else:
            self.logger.error("Failed to start bot")
            return False

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="NopalBot - Linux Server Version",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main_linux.py
  python main_linux.py --config config/bot_config.json --name my_bot
  python main_linux.py --headless --name warrior_bot
        """
    )
    
    parser.add_argument(
        '--config', 
        default='config/bot_config.json',
        help='Configuration file path (default: config/bot_config.json)'
    )
    
    parser.add_argument(
        '--name', 
        default='nopal_bot',
        help='Bot name (default: nopal_bot)'
    )
    
    parser.add_argument(
        '--headless', 
        action='store_true',
        help='Run in headless mode (default: True)'
    )
    
    parser.add_argument(
        '--log-level', 
        default='INFO',
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'],
        help='Logging level (default: INFO)'
    )
    
    args = parser.parse_args()
    
    # Set log level
    logging.getLogger().setLevel(getattr(logging, args.log_level.upper()))
    
    # Create and run bot
    bot = LinuxNopalBot(
        config_file=args.config,
        bot_name=args.name,
        headless=args.headless
    )
    
    return bot.run()

if __name__ == "__main__":
    sys.exit(0 if main() else 1) 