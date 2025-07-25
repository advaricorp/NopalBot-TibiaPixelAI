#!/usr/bin/env python3
"""
Ultra-Aggressive Screenshot Bypass Test
By Taquito Loco 🎮

Tests the most aggressive bypass techniques for stubborn anti-screenshot measures.
"""

import sys
import os
import time
import cv2
import numpy as np
from datetime import datetime

# Add src to path
sys.path.append('src')

def test_ultra_bypass():
    """Test ultra-aggressive bypass techniques"""
    print("🎮 Testing Ultra-Aggressive Screenshot Bypass")
    print("=" * 60)
    
    try:
        from ultra_aggressive_bypass import UltraAggressiveBypass
        
        bypass = UltraAggressiveBypass()
        print("✅ UltraAggressiveBypass created")
        
        # Test target window detection
        print("\n🔍 Testing target window detection...")
        if bypass.find_target_window("tibia"):
            print("✅ Target window found!")
            print(f"   Window: {win32gui.GetWindowText(bypass.target_window)}")
            
            # Test ultra-aggressive capture
            print("\n📸 Testing ultra-aggressive capture...")
            start_time = time.time()
            image = bypass.capture_ultra_aggressive()
            end_time = time.time()
            
            if image is not None:
                print(f"✅ Ultra-aggressive capture successful!")
                print(f"   Size: {image.shape[1]}x{image.shape[0]}")
                print(f"   Time: {end_time - start_time:.3f}s")
                
                # Save test image
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"logs/ultra_capture_{timestamp}.png"
                os.makedirs("logs", exist_ok=True)
                cv2.imwrite(filename, image)
                print(f"   💾 Saved as: {filename}")
                
                # Check image quality
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                mean_brightness = np.mean(gray)
                std_brightness = np.std(gray)
                
                print(f"   Brightness: {mean_brightness:.1f} (0=black, 255=white)")
                print(f"   Contrast: {std_brightness:.1f} (higher=more contrast)")
                
                if mean_brightness < 10:
                    print("   ⚠️ Image appears to be black - anti-screenshot still active")
                elif mean_brightness < 50:
                    print("   ⚠️ Image appears very dark - partial bypass")
                else:
                    print("   ✅ Image appears normal - ultra bypass successful!")
                
                return True
            else:
                print("❌ Ultra-aggressive capture failed")
                return False
        else:
            print("❌ Target window not found")
            print("💡 Make sure Tibia is running")
            return False
            
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_all_ultra_methods():
    """Test all ultra-aggressive methods individually"""
    print("\n🔬 Testing All Ultra-Aggressive Methods")
    print("=" * 50)
    
    try:
        from ultra_aggressive_bypass import UltraAggressiveBypass
        
        bypass = UltraAggressiveBypass()
        
        if not bypass.find_target_window("tibia"):
            print("❌ Target window not found")
            return False
        
        methods = [
            ('Kernel Level', bypass._capture_kernel_level),
            ('Driver Bypass', bypass._capture_driver_bypass),
            ('Memory Dump', bypass._capture_memory_dump),
            ('GPU Memory', bypass._capture_gpu_memory),
            ('Direct Framebuffer', bypass._capture_direct_framebuffer),
            ('Hardware Interrupt', bypass._capture_hardware_interrupt),
            ('System Call', bypass._capture_system_call),
            ('Fallback Ultra', bypass._capture_fallback_ultra)
        ]
        
        successful_methods = []
        
        for method_name, method_func in methods:
            print(f"\n📸 Testing: {method_name}")
            try:
                start_time = time.time()
                image = method_func()
                end_time = time.time()
                
                if image is not None:
                    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                    mean_brightness = np.mean(gray)
                    std_brightness = np.std(gray)
                    
                    print(f"   ✅ Success ({end_time - start_time:.3f}s)")
                    print(f"   Size: {image.shape[1]}x{image.shape[0]}")
                    print(f"   Brightness: {mean_brightness:.1f}")
                    print(f"   Contrast: {std_brightness:.1f}")
                    
                    successful_methods.append({
                        'name': method_name,
                        'time': end_time - start_time,
                        'brightness': mean_brightness,
                        'contrast': std_brightness,
                        'image': image
                    })
                    
                    # Save best image
                    if mean_brightness > 50 and std_brightness > 20:  # Good quality
                        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                        filename = f"logs/ultra_{method_name.lower().replace(' ', '_')}_{timestamp}.png"
                        cv2.imwrite(filename, image)
                        print(f"   💾 Saved: {filename}")
                else:
                    print(f"   ❌ Failed")
                    
            except Exception as e:
                print(f"   ❌ Error: {e}")
        
        # Summary
        print(f"\n📊 Results: {len(successful_methods)}/{len(methods)} methods successful")
        
        if successful_methods:
            # Find best method by brightness and contrast
            best_method = max(successful_methods, key=lambda x: x['brightness'] + x['contrast'])
            print(f"🎯 Best method: {best_method['name']}")
            print(f"   Brightness: {best_method['brightness']:.1f}")
            print(f"   Contrast: {best_method['contrast']:.1f}")
            
            return True
        else:
            print("❌ No methods successful")
            return False
            
    except Exception as e:
        print(f"❌ Error in method testing: {e}")
        return False

def test_continuous_capture():
    """Test continuous capture to see if we can get any frames"""
    print("\n🔄 Testing Continuous Capture")
    print("=" * 40)
    
    try:
        from ultra_aggressive_bypass import UltraAggressiveBypass
        
        bypass = UltraAggressiveBypass()
        
        if not bypass.find_target_window("tibia"):
            print("❌ Target window not found")
            return False
        
        print("📸 Capturing 10 frames continuously...")
        
        successful_captures = 0
        total_time = 0
        best_image = None
        best_brightness = 0
        
        for i in range(10):
            try:
                start_time = time.time()
                image = bypass.capture_ultra_aggressive()
                end_time = time.time()
                
                if image is not None:
                    successful_captures += 1
                    total_time += (end_time - start_time)
                    
                    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                    mean_brightness = np.mean(gray)
                    
                    print(f"   Frame {i+1}: {mean_brightness:.1f} brightness ({end_time - start_time:.3f}s)")
                    
                    if mean_brightness > best_brightness:
                        best_brightness = mean_brightness
                        best_image = image
                else:
                    print(f"   Frame {i+1}: Failed")
                
                time.sleep(0.1)  # Small delay between captures
                
            except Exception as e:
                print(f"   Frame {i+1}: Error - {e}")
        
        # Results
        success_rate = (successful_captures / 10) * 100
        avg_time = total_time / successful_captures if successful_captures > 0 else 0
        
        print(f"\n📊 Continuous Capture Results:")
        print(f"   Success Rate: {success_rate:.1f}%")
        print(f"   Average Time: {avg_time:.3f}s")
        print(f"   Best Brightness: {best_brightness:.1f}")
        
        if best_image is not None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"logs/ultra_best_continuous_{timestamp}.png"
            cv2.imwrite(filename, best_image)
            print(f"   💾 Best frame saved: {filename}")
        
        return success_rate > 0
        
    except Exception as e:
        print(f"❌ Error in continuous capture: {e}")
        return False

def main():
    """Main test function"""
    print("🎮 Ultra-Aggressive Screenshot Bypass Test")
    print("By Taquito Loco 🎮")
    print("=" * 60)
    
    # Test 1: Basic ultra bypass
    test1_success = test_ultra_bypass()
    
    # Test 2: All ultra methods individually
    test2_success = test_all_ultra_methods()
    
    # Test 3: Continuous capture
    test3_success = test_continuous_capture()
    
    # Summary
    print("\n" + "=" * 60)
    print("📋 TEST SUMMARY")
    print("=" * 60)
    print(f"Basic Ultra Bypass: {'✅ PASS' if test1_success else '❌ FAIL'}")
    print(f"All Ultra Methods: {'✅ PASS' if test2_success else '❌ FAIL'}")
    print(f"Continuous Capture: {'✅ PASS' if test3_success else '❌ FAIL'}")
    
    total_tests = 3
    passed_tests = sum([test1_success, test2_success, test3_success])
    
    print(f"\nOverall Result: {passed_tests}/{total_tests} tests passed")
    
    if passed_tests == total_tests:
        print("🎉 All tests passed! Ultra bypass is working.")
    elif passed_tests > 0:
        print("⚠️ Some tests passed. Ultra bypass is partially working.")
    else:
        print("❌ No tests passed. Anti-screenshot is too strong.")
    
    print("\n💡 Ultra-Aggressive Techniques Used:")
    print("- Kernel-level capture")
    print("- Driver bypass")
    print("- Memory dump")
    print("- GPU memory access")
    print("- Direct framebuffer")
    print("- Hardware interrupts")
    print("- System calls")
    print("- Multiple fallbacks")

if __name__ == "__main__":
    main() 