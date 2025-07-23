#!/usr/bin/env python3
"""
NopalBot - Main Entry Point
By Taquito Loco 🎮
"""

import sys
import os
import logging
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from gui.main import start_gui
from cli.main import start_cli
from bot.main import start_bot

def main():
    """Main entry point for NopalBot"""
    
    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('logs/nopal_bot.log'),
            logging.StreamHandler()
        ]
    )
    
    logger = logging.getLogger(__name__)
    
    print("🤖 NopalBot - By Taquito Loco 🎮")
    print("=" * 40)
    print("1. GUI Mode (Graphical Interface)")
    print("2. CLI Mode (Command Line Interface)")
    print("3. Bot Mode (Direct Bot Execution)")
    print("4. Exit")
    print("=" * 40)
    
    try:
        choice = input("Select mode (1-4): ").strip()
        
        if choice == "1":
            logger.info("Starting GUI mode")
            start_gui()
        elif choice == "2":
            logger.info("Starting CLI mode")
            start_cli()
        elif choice == "3":
            logger.info("Starting bot mode")
            start_bot()
        elif choice == "4":
            logger.info("Exiting NopalBot")
            print("👋 Goodbye!")
            sys.exit(0)
        else:
            print("❌ Invalid choice. Please select 1-4.")
            sys.exit(1)
            
    except KeyboardInterrupt:
        logger.info("Bot interrupted by user")
        print("\n👋 Bot stopped by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Error in main: {e}")
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 