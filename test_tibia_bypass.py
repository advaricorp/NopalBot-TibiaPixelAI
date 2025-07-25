#!/usr/bin/env python3
"""
Tibia-Specific Screenshot Bypass Test
By Taquito Loco 🎮

Tests aggressive bypass techniques specifically designed for Tibia's anti-screenshot measures.
"""

import sys
import os
import time
import cv2
import numpy as np
from datetime import datetime

# Add src to path
sys.path.append('src')

def test_tibia_bypass():
    """Test Tibia-specific bypass techniques"""
    print("🎮 Testing Tibia-Specific Screenshot Bypass")
    print("=" * 60)
    
    try:
        from tibia_specific_bypass import TibiaAggressiveBypass
        
        bypass = TibiaAggressiveBypass()
        print("✅ TibiaAggressiveBypass created")
        
        # Test Tibia window detection
        print("\n🔍 Testing Tibia window detection...")
        if bypass.find_tibia_window():
            print("✅ Tibia window found!")
            print(f"   Window: {win32gui.GetWindowText(bypass.tibia_window_handle)}")
            print(f"   Region: {bypass.tibia_region}")
            
            # Test capture
            print("\n📸 Testing Tibia capture...")
            start_time = time.time()
            image = bypass.capture_tibia_aggressive()
            end_time = time.time()
            
            if image is not None:
                print(f"✅ Tibia capture successful!")
                print(f"   Size: {image.shape[1]}x{image.shape[0]}")
                print(f"   Time: {end_time - start_time:.3f}s")
                
                # Save test image
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"logs/tibia_capture_{timestamp}.png"
                os.makedirs("logs", exist_ok=True)
                cv2.imwrite(filename, image)
                print(f"   💾 Saved as: {filename}")
                
                # Check if image is mostly black
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                mean_brightness = np.mean(gray)
                print(f"   Brightness: {mean_brightness:.1f} (0=black, 255=white)")
                
                if mean_brightness < 10:
                    print("   ⚠️ Image appears to be black - anti-screenshot active")
                elif mean_brightness < 50:
                    print("   ⚠️ Image appears very dark - partial bypass")
                else:
                    print("   ✅ Image appears normal - bypass successful!")
                
                return True
            else:
                print("❌ Tibia capture failed")
                return False
        else:
            print("❌ Tibia window not found")
            print("💡 Make sure Tibia is running")
            return False
            
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_all_tibia_methods():
    """Test all Tibia-specific methods individually"""
    print("\n🔬 Testing All Tibia Methods")
    print("=" * 40)
    
    try:
        from tibia_specific_bypass import TibiaAggressiveBypass
        
        bypass = TibiaAggressiveBypass()
        
        if not bypass.find_tibia_window():
            print("❌ Tibia window not found")
            return False
        
        methods = [
            ('Direct Memory', bypass._capture_tibia_direct_memory),
            ('Hardware Accelerated', bypass._capture_tibia_hardware_accelerated),
            ('DirectX Bypass', bypass._capture_tibia_directx_bypass),
            ('Window DC', bypass._capture_tibia_window_dc),
            ('Screen DC', bypass._capture_tibia_screen_dc),
            ('Fallback', bypass._capture_tibia_fallback)
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
                    
                    print(f"   ✅ Success ({end_time - start_time:.3f}s)")
                    print(f"   Size: {image.shape[1]}x{image.shape[0]}")
                    print(f"   Brightness: {mean_brightness:.1f}")
                    
                    successful_methods.append({
                        'name': method_name,
                        'time': end_time - start_time,
                        'brightness': mean_brightness,
                        'image': image
                    })
                    
                    # Save best image
                    if mean_brightness > 50:  # Not too dark
                        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                        filename = f"logs/tibia_{method_name.lower().replace(' ', '_')}_{timestamp}.png"
                        cv2.imwrite(filename, image)
                        print(f"   💾 Saved: {filename}")
                else:
                    print(f"   ❌ Failed")
                    
            except Exception as e:
                print(f"   ❌ Error: {e}")
        
        # Summary
        print(f"\n📊 Results: {len(successful_methods)}/{len(methods)} methods successful")
        
        if successful_methods:
            # Find best method
            best_method = max(successful_methods, key=lambda x: x['brightness'])
            print(f"🎯 Best method: {best_method['name']} (brightness: {best_method['brightness']:.1f})")
            
            return True
        else:
            print("❌ No methods successful")
            return False
            
    except Exception as e:
        print(f"❌ Error in method testing: {e}")
        return False

def test_tibia_capture_test():
    """Test the comprehensive capture test"""
    print("\n🧪 Testing Comprehensive Capture Test")
    print("=" * 50)
    
    try:
        from tibia_specific_bypass import TibiaAggressiveBypass
        
        bypass = TibiaAggressiveBypass()
        results = bypass.test_tibia_capture()
        
        print(f"Tibia Found: {'✅' if results['tibia_found'] else '❌'}")
        
        if results['tibia_found']:
            print(f"Window: {results['window_info']['title']}")
            print(f"Region: {results['window_info']['region']}")
            
            print(f"\nMethods Tested: {len(results['methods_tested'])}")
            for method in results['methods_tested']:
                print(f"   - {method}")
            
            print(f"\nSuccessful Methods: {len(results['successful_methods'])}")
            for method in results['successful_methods']:
                print(f"   ✅ {method['name']}: {method['time']:.3f}s, {method['size']}")
            
            if results['best_method']:
                print(f"\n🎯 Best Method: {results['best_method']}")
                
                # Save sample image
                if results['sample_image'] is not None:
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    filename = f"logs/tibia_best_method_{timestamp}.png"
                    cv2.imwrite(filename, results['sample_image'])
                    print(f"💾 Sample image saved: {filename}")
                
                return True
            else:
                print("❌ No successful methods")
                return False
        else:
            print("❌ Tibia not found")
            return False
            
    except Exception as e:
        print(f"❌ Error in comprehensive test: {e}")
        return False

def main():
    """Main test function"""
    print("🎮 Tibia-Specific Screenshot Bypass Test")
    print("By Taquito Loco 🎮")
    print("=" * 60)
    
    # Test 1: Basic Tibia bypass
    test1_success = test_tibia_bypass()
    
    # Test 2: All methods individually
    test2_success = test_all_tibia_methods()
    
    # Test 3: Comprehensive test
    test3_success = test_tibia_capture_test()
    
    # Summary
    print("\n" + "=" * 60)
    print("📋 TEST SUMMARY")
    print("=" * 60)
    print(f"Basic Tibia Bypass: {'✅ PASS' if test1_success else '❌ FAIL'}")
    print(f"All Methods Test: {'✅ PASS' if test2_success else '❌ FAIL'}")
    print(f"Comprehensive Test: {'✅ PASS' if test3_success else '❌ FAIL'}")
    
    total_tests = 3
    passed_tests = sum([test1_success, test2_success, test3_success])
    
    print(f"\nOverall Result: {passed_tests}/{total_tests} tests passed")
    
    if passed_tests == total_tests:
        print("🎉 All tests passed! Tibia bypass is working.")
    elif passed_tests > 0:
        print("⚠️ Some tests passed. Tibia bypass is partially working.")
    else:
        print("❌ No tests passed. Tibia's anti-screenshot is too strong.")
    
    print("\n💡 Tips for Tibia:")
    print("- Make sure Tibia is running and visible")
    print("- Try running as administrator")
    print("- Check if Tibia is in fullscreen mode")
    print("- Some anti-screenshot measures cannot be bypassed")
    print("- Check logs/ folder for captured images")

if __name__ == "__main__":
    main() 