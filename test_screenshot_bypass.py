#!/usr/bin/env python3
"""
Simple Screenshot Bypass Test
By Taquito Loco 🎮

Tests the advanced screenshot bypass techniques for Tibia bot.
"""

import sys
import os
import time
import cv2
import numpy as np
from datetime import datetime

# Add src to path
sys.path.append('src')

def test_vision_module():
    """Test the vision module with advanced screenshot bypass"""
    print("🎮 Testing Advanced Screenshot Bypass")
    print("=" * 50)
    
    try:
        from vision import ComputerVision
        print("✅ Vision module imported successfully")
        
        # Create vision system
        cv_system = ComputerVision()
        print("✅ ComputerVision instance created")
        
        # Test screenshot capture
        print("\n📸 Testing screenshot capture...")
        start_time = time.time()
        
        image = cv_system.capture_tibia_screen()
        
        end_time = time.time()
        capture_time = end_time - start_time
        
        if image is not None:
            print(f"✅ Screenshot captured successfully!")
            print(f"   Size: {image.shape[1]}x{image.shape[0]}")
            print(f"   Time: {capture_time:.3f} seconds")
            
            # Save test image
            os.makedirs("logs", exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"logs/test_screenshot_{timestamp}.png"
            cv2.imwrite(filename, image)
            print(f"   💾 Saved as: {filename}")
            
            return True
        else:
            print("❌ Screenshot capture failed")
            return False
            
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_multiple_captures(num_captures=5):
    """Test multiple screenshot captures"""
    print(f"\n🔄 Testing {num_captures} consecutive captures...")
    print("-" * 50)
    
    try:
        from vision import ComputerVision
        cv_system = ComputerVision()
        
        success_count = 0
        total_time = 0
        
        for i in range(num_captures):
            print(f"📸 Capture {i+1}/{num_captures}...")
            
            start_time = time.time()
            image = cv_system.capture_tibia_screen()
            end_time = time.time()
            
            if image is not None:
                success_count += 1
                total_time += (end_time - start_time)
                print(f"   ✅ Success ({end_time - start_time:.3f}s)")
            else:
                print(f"   ❌ Failed")
            
            time.sleep(0.5)  # Delay between captures
        
        # Calculate statistics
        success_rate = (success_count / num_captures) * 100
        avg_time = total_time / success_count if success_count > 0 else 0
        
        print(f"\n📊 Results:")
        print(f"   Success Rate: {success_rate:.1f}%")
        print(f"   Average Time: {avg_time:.3f}s")
        print(f"   Successful Captures: {success_count}/{num_captures}")
        
        return success_rate > 50  # Consider successful if >50% success rate
        
    except Exception as e:
        print(f"❌ Error in multiple capture test: {e}")
        return False

def test_advanced_bypass_module():
    """Test the advanced bypass module directly"""
    print("\n🚀 Testing Advanced Bypass Module")
    print("-" * 50)
    
    try:
        from advanced_screenshot import AdvancedScreenshotBypass
        
        bypass = AdvancedScreenshotBypass()
        print("✅ AdvancedScreenshotBypass created")
        
        # Test capture
        print("📸 Testing advanced capture...")
        start_time = time.time()
        image = bypass.capture_screen_advanced()
        end_time = time.time()
        
        if image is not None:
            print(f"✅ Advanced capture successful!")
            print(f"   Size: {image.shape[1]}x{image.shape[0]}")
            print(f"   Time: {end_time - start_time:.3f}s")
            print(f"   Best Method: {bypass.get_best_method()}")
            
            # Show performance stats
            stats = bypass.get_performance_stats()
            print(f"\n📈 Performance Stats:")
            for method, stat in stats.items():
                if stat['total'] > 0:
                    success_rate = (stat['success'] / stat['total']) * 100
                    print(f"   {method}: {success_rate:.1f}% success")
            
            return True
        else:
            print("❌ Advanced capture failed")
            return False
            
    except ImportError as e:
        print(f"❌ Advanced bypass module not available: {e}")
        return False
    except Exception as e:
        print(f"❌ Error in advanced bypass test: {e}")
        return False

def main():
    """Main test function"""
    print("🎮 Advanced Screenshot Bypass Test Suite")
    print("By Taquito Loco 🎮")
    print("=" * 60)
    
    # Test 1: Vision module
    test1_success = test_vision_module()
    
    # Test 2: Multiple captures
    test2_success = test_multiple_captures(3)
    
    # Test 3: Advanced bypass module
    test3_success = test_advanced_bypass_module()
    
    # Summary
    print("\n" + "=" * 60)
    print("📋 TEST SUMMARY")
    print("=" * 60)
    print(f"Vision Module Test: {'✅ PASS' if test1_success else '❌ FAIL'}")
    print(f"Multiple Captures Test: {'✅ PASS' if test2_success else '❌ FAIL'}")
    print(f"Advanced Bypass Test: {'✅ PASS' if test3_success else '❌ FAIL'}")
    
    total_tests = 3
    passed_tests = sum([test1_success, test2_success, test3_success])
    
    print(f"\nOverall Result: {passed_tests}/{total_tests} tests passed")
    
    if passed_tests == total_tests:
        print("🎉 All tests passed! Screenshot bypass is working correctly.")
    elif passed_tests > 0:
        print("⚠️ Some tests passed. Screenshot bypass is partially working.")
    else:
        print("❌ No tests passed. Screenshot bypass needs attention.")
    
    print("\n💡 Tips:")
    print("- Make sure Tibia is running for best results")
    print("- Check that all dependencies are installed")
    print("- Run as administrator if needed")
    print("- Check logs/ folder for saved screenshots")

if __name__ == "__main__":
    main() 