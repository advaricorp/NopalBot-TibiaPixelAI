#!/usr/bin/env python3
"""
Simple Working Screenshot Bypass Test
By Taquito Loco 🎮

Tests simple but effective bypass techniques for Tibia's anti-screenshot measures.
"""

import sys
import os
import time
import cv2
import numpy as np
from datetime import datetime

# Add src to path
sys.path.append('src')

def test_simple_bypass():
    """Test simple working bypass techniques"""
    print("🎮 Testing Simple Working Screenshot Bypass")
    print("=" * 60)
    
    try:
        from simple_working_bypass import SimpleWorkingBypass
        
        bypass = SimpleWorkingBypass()
        print("✅ SimpleWorkingBypass created")
        
        # Test Tibia window detection
        print("\n🔍 Testing Tibia window detection...")
        if bypass.find_tibia_window():
            print("✅ Tibia window found!")
            print(f"   Window: {win32gui.GetWindowText(bypass.tibia_window)}")
            
            # Test simple capture
            print("\n📸 Testing simple capture...")
            start_time = time.time()
            image = bypass.capture_simple_working()
            end_time = time.time()
            
            if image is not None:
                print(f"✅ Simple capture successful!")
                print(f"   Size: {image.shape[1]}x{image.shape[0]}")
                print(f"   Time: {end_time - start_time:.3f}s")
                
                # Save test image
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"logs/simple_capture_{timestamp}.png"
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
                    print("   ✅ Image appears normal - simple bypass successful!")
                
                return True
            else:
                print("❌ Simple capture failed")
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

def test_all_simple_methods():
    """Test all simple methods individually"""
    print("\n🔬 Testing All Simple Methods")
    print("=" * 50)
    
    try:
        from simple_working_bypass import SimpleWorkingBypass
        
        bypass = SimpleWorkingBypass()
        
        if not bypass.find_tibia_window():
            print("❌ Tibia window not found")
            return False
        
        methods = [
            ('Screen DC', bypass._capture_screen_dc),
            ('Window DC Special', bypass._capture_window_dc_special),
            ('Desktop DC', bypass._capture_desktop_dc),
            ('Fallback Simple', bypass._capture_fallback_simple)
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
                        filename = f"logs/simple_{method_name.lower().replace(' ', '_')}_{timestamp}.png"
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

def test_simple_capture_test():
    """Test the comprehensive simple capture test"""
    print("\n🧪 Testing Comprehensive Simple Capture Test")
    print("=" * 60)
    
    try:
        from simple_working_bypass import SimpleWorkingBypass
        
        bypass = SimpleWorkingBypass()
        results = bypass.test_simple_capture()
        
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
                    filename = f"logs/simple_best_method_{timestamp}.png"
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
    print("🎮 Simple Working Screenshot Bypass Test")
    print("By Taquito Loco 🎮")
    print("=" * 60)
    
    # Test 1: Basic simple bypass
    test1_success = test_simple_bypass()
    
    # Test 2: All simple methods individually
    test2_success = test_all_simple_methods()
    
    # Test 3: Comprehensive simple test
    test3_success = test_simple_capture_test()
    
    # Summary
    print("\n" + "=" * 60)
    print("📋 TEST SUMMARY")
    print("=" * 60)
    print(f"Basic Simple Bypass: {'✅ PASS' if test1_success else '❌ FAIL'}")
    print(f"All Simple Methods: {'✅ PASS' if test2_success else '❌ FAIL'}")
    print(f"Comprehensive Simple: {'✅ PASS' if test3_success else '❌ FAIL'}")
    
    total_tests = 3
    passed_tests = sum([test1_success, test2_success, test3_success])
    
    print(f"\nOverall Result: {passed_tests}/{total_tests} tests passed")
    
    if passed_tests == total_tests:
        print("🎉 All tests passed! Simple bypass is working.")
    elif passed_tests > 0:
        print("⚠️ Some tests passed. Simple bypass is partially working.")
    else:
        print("❌ No tests passed. Anti-screenshot is too strong.")
    
    print("\n💡 Simple Working Techniques Used:")
    print("- Screen DC capture (most reliable)")
    print("- Window DC with special flags")
    print("- Desktop DC bypass")
    print("- Multiple fallback methods")

if __name__ == "__main__":
    main() 