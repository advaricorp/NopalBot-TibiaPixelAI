#!/usr/bin/env python3
"""
Simple GUI Screenshot Bypass Test
By Taquito Loco 🎮

Simple test to verify the GUI screenshot bypass functionality.
"""

import sys
import os
import time
import cv2
import numpy as np
from datetime import datetime

# Add src to path
sys.path.append('src')

def test_gui_screenshot():
    """Test the GUI screenshot functionality"""
    print("🎮 Testing GUI Screenshot Bypass")
    print("=" * 50)
    
    try:
        from simple_working_bypass import SimpleWorkingBypass
        
        bypass = SimpleWorkingBypass()
        print("✅ SimpleWorkingBypass created")
        
        # Test Tibia window detection
        print("\n🔍 Testing Tibia window detection...")
        if bypass.find_tibia_window():
            print("✅ Tibia window found!")
            print(f"   Window: {bypass.tibia_window}")
            
            # Test single capture
            print("\n📸 Testing single capture...")
            start_time = time.time()
            image = bypass.capture_simple_working()
            end_time = time.time()
            
            if image is not None:
                print(f"✅ Single capture successful!")
                print(f"   Size: {image.shape[1]}x{image.shape[0]}")
                print(f"   Time: {end_time - start_time:.3f}s")
                
                # Check image quality
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                mean_brightness = np.mean(gray)
                print(f"   Brightness: {mean_brightness:.1f}")
                
                # Save test image
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"logs/gui_test_{timestamp}.png"
                os.makedirs("logs", exist_ok=True)
                cv2.imwrite(filename, image)
                print(f"   💾 Saved as: {filename}")
                
                # Test multiple captures
                print("\n🔄 Testing multiple captures...")
                successful_captures = 0
                total_time = 0
                
                for i in range(5):
                    try:
                        start_time = time.time()
                        image = bypass.capture_simple_working()
                        end_time = time.time()
                        
                        if image is not None:
                            successful_captures += 1
                            total_time += (end_time - start_time)
                            print(f"   ✅ Capture {i+1}: Success ({end_time - start_time:.3f}s)")
                        else:
                            print(f"   ❌ Capture {i+1}: Failed")
                        
                        time.sleep(0.1)
                        
                    except Exception as e:
                        print(f"   ❌ Capture {i+1}: Error - {e}")
                
                success_rate = (successful_captures / 5) * 100
                avg_time = total_time / successful_captures if successful_captures > 0 else 0
                
                print(f"\n📊 Results: {successful_captures}/5 successful ({success_rate:.1f}%)")
                print(f"   Average time: {avg_time:.3f}s")
                
                return True
            else:
                print("❌ Single capture failed")
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

def main():
    """Main test function"""
    print("🎮 GUI Screenshot Bypass Test")
    print("By Taquito Loco 🎮")
    print("=" * 50)
    
    success = test_gui_screenshot()
    
    print("\n" + "=" * 50)
    print("📋 TEST SUMMARY")
    print("=" * 50)
    
    if success:
        print("✅ Test passed! GUI screenshot bypass is working.")
    else:
        print("❌ Test failed. Check if Tibia is running.")
    
    print("\n💡 Next steps:")
    print("- Make sure Tibia is running")
    print("- Try the GUI test button")
    print("- Check logs/ folder for captured images")

if __name__ == "__main__":
    main() 