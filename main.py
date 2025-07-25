#!/usr/bin/env python3
"""
NopalBot Elite Knight - Main Entry Point
Bot especializado para farming automático - by Pikos Nopal
"""

import sys
import os

# Agregar el directorio src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def main():
    """Función principal"""
    try:
        # Importar y ejecutar GUI
        from src.gui import NopalBotEliteKnightGUI
        
        print("🚀 Iniciando NopalBot Elite Knight...")
        print("📋 Cargando configuración...")
        
        # Crear y ejecutar GUI
        gui = NopalBotEliteKnightGUI()
        gui.run()
        
    except ImportError as e:
        print(f"❌ Error importando módulos: {e}")
        print("💡 Asegúrate de tener todas las dependencias instaladas:")
        print("   pip install -r requirements.txt")
        
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        print("💡 Verifica que Tibia esté ejecutándose")

if __name__ == "__main__":
    main() 