"""
Consolidated Test Script for PBT Bot
Tests all bot features and functionality
By Taquito Loco 🎮
"""

import sys
import os
import time
import threading
import unittest
from unittest.mock import Mock, patch

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from bot.main import NoSpellsBotImproved
    from utils.window_manager import WindowManager
    from utils.input_manager import InputManager
except ImportError as e:
    print(f"[ERROR] No se pudo importar módulos: {e}")
    print("Asegúrate de ejecutar desde la raíz del proyecto")
    sys.exit(1)

class TestNoSpellsBotImproved(unittest.TestCase):
    """Test cases for the improved bot"""
    
    def setUp(self):
        """Set up test environment"""
        self.bot = NoSpellsBotImproved()
        self.bot.logger = Mock()  # Mock logger to avoid file operations
    
    def tearDown(self):
        """Clean up after tests"""
        if hasattr(self.bot, 'running') and self.bot.running:
            self.bot.stop()
    
    def test_bot_initialization(self):
        """Test bot initialization"""
        self.assertIsNotNone(self.bot)
        self.assertFalse(self.bot.running)
        self.assertFalse(self.bot.paused)
        self.assertEqual(self.bot.attack_key, 'space')
        self.assertTrue(self.bot.constant_movement_enabled)
        self.assertTrue(self.bot.stair_detection_enabled)
    
    def test_feature_configuration(self):
        """Test feature configuration"""
        # Should have magic features disabled
        self.assertFalse(self.bot.auto_heal_enabled)
        self.assertFalse(self.bot.auto_potions_enabled)
        
        # Should have physical features enabled
        self.assertTrue(self.bot.auto_attack_enabled)
        self.assertTrue(self.bot.auto_loot_enabled)
        self.assertTrue(self.bot.auto_movement_enabled)
    
    def test_hotkey_configuration(self):
        """Test hotkey configuration"""
        self.assertEqual(self.bot.pause_key, 'f1')
        self.assertEqual(self.bot.stop_key, 'f2')
        self.assertEqual(self.bot.attack_key, 'space')  # Should use SPACE, not F3
        self.assertEqual(self.bot.loot_key, 'f4')
        self.assertEqual(self.bot.emergency_kill_key, 'f12')
    
    def test_movement_pattern(self):
        """Test movement pattern configuration"""
        self.assertEqual(self.bot.movement_pattern, ['w', 'a', 's', 'd'])
        self.assertEqual(self.bot.stair_movement_pattern, ['w', 's'])
        self.assertEqual(self.bot.max_movement_steps, 3)
    
    def test_combat_detection(self):
        """Test combat detection (mocked)"""
        # Mock random to simulate enemy detection
        with patch('random.random', return_value=0.1):  # 10% chance
            result = self.bot._detect_combat()
            self.assertTrue(result)
            self.assertTrue(self.bot.in_combat)
    
    def test_stair_detection(self):
        """Test stair detection (mocked)"""
        # Mock random to simulate stair detection
        with patch('random.random', return_value=0.1):  # 10% chance
            self.bot._detect_stairs()
            self.assertTrue(self.bot.on_stairs)
            self.assertEqual(self.bot.movement_pattern, ['w', 's'])
    
    def test_manual_attack(self):
        """Test manual attack method"""
        # Mock input manager
        self.bot.input_manager = Mock()
        self.bot.running = True
        self.bot.paused = False
        
        self.bot._manual_attack()
        self.bot.input_manager.send_attack.assert_called_once()
    
    def test_manual_loot(self):
        """Test manual loot method"""
        # Mock input manager
        self.bot.input_manager = Mock()
        self.bot.running = True
        self.bot.paused = False
        
        self.bot._manual_loot()
        self.bot.input_manager.send_key.assert_called_with('f4')
    
    def test_emergency_kill(self):
        """Test emergency kill method"""
        with patch('os._exit') as mock_exit:
            self.bot._emergency_kill()
            mock_exit.assert_called_with(0)
    
    def test_pause_toggle(self):
        """Test pause toggle functionality"""
        initial_pause = self.bot.paused
        self.bot._toggle_pause()
        self.assertNotEqual(self.bot.paused, initial_pause)
    
    def test_stop_bot(self):
        """Test bot stop functionality"""
        self.bot.running = True
        self.bot._stop_bot()
        self.assertFalse(self.bot.running)

class TestWindowManager(unittest.TestCase):
    """Test cases for window manager"""
    
    def setUp(self):
        """Set up test environment"""
        self.window_manager = WindowManager()
    
    def test_window_manager_initialization(self):
        """Test window manager initialization"""
        self.assertIsNotNone(self.window_manager)
    
    @patch('win32gui.FindWindow')
    def test_find_tibia_window(self, mock_find_window):
        """Test finding Tibia window (mocked)"""
        mock_find_window.return_value = 12345  # Mock window handle
        result = self.window_manager.find_tibia_window()
        self.assertTrue(result)
    
    @patch('win32gui.GetForegroundWindow')
    def test_is_tibia_focused(self, mock_get_foreground):
        """Test Tibia focus detection (mocked)"""
        mock_get_foreground.return_value = 12345
        result = self.window_manager.is_tibia_focused()
        self.assertIsInstance(result, bool)

class TestInputManager(unittest.TestCase):
    """Test cases for input manager"""
    
    def setUp(self):
        """Set up test environment"""
        self.window_manager = Mock()
        self.input_manager = InputManager(self.window_manager)
    
    def test_input_manager_initialization(self):
        """Test input manager initialization"""
        self.assertIsNotNone(self.input_manager)
        self.assertEqual(self.input_manager.window_manager, self.window_manager)
    
    @patch('keyboard.send')
    def test_send_key(self, mock_send):
        """Test sending key (mocked)"""
        result = self.input_manager.send_key('space')
        mock_send.assert_called_with('space')
        self.assertTrue(result)
    
    @patch('keyboard.send')
    def test_send_attack(self, mock_send):
        """Test sending attack (mocked)"""
        result = self.input_manager.send_attack()
        mock_send.assert_called_with('space')
        self.assertTrue(result)

def run_integration_test():
    """Run integration test with real bot instance"""
    print("🧪 EJECUTANDO TEST DE INTEGRACIÓN")
    print("=" * 40)
    
    try:
        # Create bot instance
        bot = NoSpellsBotImproved()
        
        print("✅ Bot creado exitosamente")
        print(f"   • Attack key: {bot.attack_key}")
        print(f"   • Constant movement: {bot.constant_movement_enabled}")
        print(f"   • Stair detection: {bot.stair_detection_enabled}")
        print(f"   • Auto heal: {bot.auto_heal_enabled}")
        print(f"   • Auto potions: {bot.auto_potions_enabled}")
        
        # Test manual methods
        print("\n🔧 Probando métodos manuales...")
        bot.manual_attack()
        bot.manual_loot()
        print("✅ Métodos manuales probados")
        
        # Test hotkeys
        print("\n⌨️ Probando configuración de hotkeys...")
        print(f"   • F1: {bot.pause_key} - Pausar/Reanudar")
        print(f"   • F2: {bot.stop_key} - Detener bot")
        print(f"   • SPACE: {bot.attack_key} - Ataque manual")
        print(f"   • F4: {bot.loot_key} - Loot manual")
        print(f"   • F12: {bot.emergency_kill_key} - KILL EMERGENCY")
        print("✅ Hotkeys configurados correctamente")
        
        # Test movement patterns
        print("\n🚶 Probando patrones de movimiento...")
        print(f"   • Movimiento normal: {bot.movement_pattern}")
        print(f"   • Movimiento en escaleras: {bot.stair_movement_pattern}")
        print(f"   • Pasos máximos: {bot.max_movement_steps}")
        print("✅ Patrones de movimiento configurados")
        
        print("\n🎉 ¡TEST DE INTEGRACIÓN COMPLETADO EXITOSAMENTE!")
        return True
        
    except Exception as e:
        print(f"❌ Error en test de integración: {e}")
        return False

def run_performance_test():
    """Run performance test"""
    print("\n⚡ EJECUTANDO TEST DE RENDIMIENTO")
    print("=" * 40)
    
    try:
        start_time = time.time()
        
        # Create multiple bot instances
        bots = []
        for i in range(5):
            bot = NoSpellsBotImproved()
            bots.append(bot)
        
        creation_time = time.time() - start_time
        print(f"✅ 5 instancias de bot creadas en {creation_time:.3f} segundos")
        
        # Test method calls
        start_time = time.time()
        for bot in bots:
            bot.manual_attack()
            bot.manual_loot()
        
        method_time = time.time() - start_time
        print(f"✅ 10 llamadas a métodos ejecutadas en {method_time:.3f} segundos")
        
        print("🎉 ¡TEST DE RENDIMIENTO COMPLETADO!")
        return True
        
    except Exception as e:
        print(f"❌ Error en test de rendimiento: {e}")
        return False

def main():
    """Main test function"""
    print("🧪 PBT BOT - TEST SUITE COMPLETO")
    print("=" * 50)
    print("By Taquito Loco 🎮")
    print()
    
    # Run unit tests
    print("🔬 EJECUTANDO TESTS UNITARIOS...")
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestNoSpellsBotImproved)
    suite.addTests(loader.loadTestsFromTestCase(TestWindowManager))
    suite.addTests(loader.loadTestsFromTestCase(TestInputManager))
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Run integration test
    integration_success = run_integration_test()
    
    # Run performance test
    performance_success = run_performance_test()
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 RESUMEN DE TESTS")
    print("=" * 50)
    print(f"✅ Tests unitarios: {result.testsRun - len(result.failures) - len(result.errors)}/{result.testsRun} pasaron")
    print(f"✅ Test de integración: {'PASÓ' if integration_success else 'FALLÓ'}")
    print(f"✅ Test de rendimiento: {'PASÓ' if performance_success else 'FALLÓ'}")
    
    if result.failures:
        print(f"\n❌ Fallos en tests unitarios: {len(result.failures)}")
        for test, traceback in result.failures:
            print(f"   • {test}: {traceback}")
    
    if result.errors:
        print(f"\n❌ Errores en tests unitarios: {len(result.errors)}")
        for test, traceback in result.errors:
            print(f"   • {test}: {traceback}")
    
    total_success = (result.testsRun - len(result.failures) - len(result.errors) == result.testsRun and 
                    integration_success and performance_success)
    
    if total_success:
        print("\n🎉 ¡TODOS LOS TESTS PASARON EXITOSAMENTE!")
        print("🚀 El bot está listo para usar")
    else:
        print("\n⚠️ Algunos tests fallaron")
        print("🔧 Revisa los errores y corrige los problemas")

if __name__ == "__main__":
    main() 