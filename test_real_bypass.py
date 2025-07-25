#!/usr/bin/env python3
"""
Test Real Bypass Methods
By Taquito Loco 🎮

Test different bypass methods to see which one actually works.
"""

import sys
import os
import time
import cv2
import numpy as np
from datetime import datetime

# Add src to path
sys.path.append('src')

def test_real_bypass():
    """Test different bypass methods"""
    print("🎮 Testing Real Bypass Methods")
    print("=" * 50)
    
    try:
        from simple_working_bypass import SimpleWorkingBypass
        
        bypass = SimpleWorkingBypass()
        print("✅ SimpleWorkingBypass created")
        
        # Check if Tibia is found
        if not bypass.find_tibia_window():
            print("❌ Tibia not found - make sure Tibia is running")
            return False
        
        print("✅ Tibia window found!")
        
        # Test individual methods
        print(f"\n🔬 Testing Individual Methods")
        print("=" * 35)
        
        methods = [
            ('Screen DC', bypass._capture_screen_dc),
            ('Window DC Special', bypass._capture_window_dc_special),
            ('Desktop DC', bypass._capture_desktop_dc),
            ('Fallback Simple', bypass._capture_fallback_simple)
        ]
        
        results = []
        
        for method_name, method_func in methods:
            print(f"\n📸 Testing: {method_name}")
            
            try:
                start_time = time.time()
                image = method_func()
                end_time = time.time()
                
                if image is not None:
                    # Analyze image
                    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                    mean_brightness = np.mean(gray)
                    std_brightness = np.std(gray)
                    min_brightness = np.min(gray)
                    max_brightness = np.max(gray)
                    
                    print(f"   ✅ Success ({end_time - start_time:.3f}s)")
                    print(f"   📊 Mean: {mean_brightness:.1f}, Std: {std_brightness:.1f}")
                    print(f"   📈 Range: {min_brightness} - {max_brightness}")
                    
                    # Check if image is actually black
                    if mean_brightness < 1:
                        print(f"   ⚠️ Image is essentially black")
                        quality = "BLACK"
                    elif mean_brightness < 10:
                        print(f"   ⚠️ Image is very dark")
                        quality = "DARK"
                    elif mean_brightness < 50:
                        print(f"   ⚠️ Image is dark but has content")
                        quality = "DARK_CONTENT"
                    else:
                        print(f"   ✅ Image has good content")
                        quality = "GOOD"
                    
                    results.append({
                        'name': method_name,
                        'image': image,
                        'mean': mean_brightness,
                        'std': std_brightness,
                        'min': min_brightness,
                        'max': max_brightness,
                        'quality': quality,
                        'time': end_time - start_time
                    })
                    
                    # Save image
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    filename = f"logs/test_{method_name.lower().replace(' ', '_')}_{timestamp}.png"
                    os.makedirs("logs", exist_ok=True)
                    cv2.imwrite(filename, image)
                    print(f"   💾 Saved: {filename}")
                    
                else:
                    print(f"   ❌ Failed")
                    results.append({
                        'name': method_name,
                        'image': None,
                        'quality': 'FAILED'
                    })
                
            except Exception as e:
                print(f"   ❌ Error: {e}")
                results.append({
                    'name': method_name,
                    'image': None,
                    'quality': 'ERROR'
                })
        
        # Summary
        print(f"\n📊 METHOD COMPARISON")
        print("=" * 35)
        
        successful_methods = [r for r in results if r['image'] is not None]
        
        if successful_methods:
            print(f"✅ {len(successful_methods)}/{len(methods)} methods successful")
            
            # Find best method
            best_method = max(successful_methods, key=lambda x: x['mean'])
            print(f"🎯 Best method: {best_method['name']} (brightness: {best_method['mean']:.1f})")
            
            # Create comparison
            create_method_comparison(successful_methods)
            
            # Test with different window states
            print(f"\n🔍 Testing Window States")
            print("=" * 30)
            test_window_states(bypass)
            
        else:
            print("❌ No methods successful")
        
        return len(successful_methods) > 0
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def create_method_comparison(methods):
    """Create comparison of all successful methods"""
    try:
        if len(methods) < 2:
            return
        
        # Resize all images to same size
        height, width = methods[0]['image'].shape[:2]
        target_size = (width//2, height//2)
        
        # Create grid
        grid_width = target_size[0] * 2
        grid_height = target_size[1] * ((len(methods) + 1) // 2)
        
        grid = np.zeros((grid_height, grid_width, 3), dtype=np.uint8)
        
        for i, method in enumerate(methods):
            row = i // 2
            col = i % 2
            
            y_start = row * target_size[1]
            y_end = (row + 1) * target_size[1]
            x_start = col * target_size[0]
            x_end = (col + 1) * target_size[0]
            
            resized = cv2.resize(method['image'], target_size)
            grid[y_start:y_end, x_start:x_end] = resized
            
            # Add label
            label = f"{method['name']}: {method['mean']:.1f}"
            cv2.putText(grid, label, (x_start + 10, y_start + 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        
        # Save comparison
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"logs/method_comparison_{timestamp}.png"
        cv2.imwrite(filename, grid)
        print(f"💾 Method comparison: {filename}")
        
    except Exception as e:
        print(f"❌ Error creating comparison: {e}")

def test_window_states(bypass):
    """Test different window states"""
    try:
        import win32gui
        import win32con
        
        # Get current window state
        hwnd = bypass.tibia_window
        current_state = win32gui.GetWindowPlacement(hwnd)
        
        print(f"Current window state: {current_state[1]}")
        
        # Test different states
        states = [
            (win32con.SW_SHOW, "Show"),
            (win32con.SW_RESTORE, "Restore"),
            (win32con.SW_MAXIMIZE, "Maximize")
        ]
        
        for state_id, state_name in states:
            try:
                print(f"\n🔍 Testing {state_name} state...")
                
                # Set window state
                win32gui.ShowWindow(hwnd, state_id)
                time.sleep(0.5)  # Wait for window to update
                
                # Take screenshot
                image = bypass.capture_simple_working()
                
                if image is not None:
                    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                    mean_brightness = np.mean(gray)
                    
                    print(f"   Brightness: {mean_brightness:.1f}")
                    
                    # Save if it's better
                    if mean_brightness > 10:
                        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                        filename = f"logs/tibia_{state_name.lower()}_{timestamp}.png"
                        cv2.imwrite(filename, image)
                        print(f"   💾 Saved: {filename}")
                
            except Exception as e:
                print(f"   ❌ Error: {e}")
        
        # Restore original state
        win32gui.ShowWindow(hwnd, current_state[1])
        
    except Exception as e:
        print(f"❌ Error testing window states: {e}")

def main():
    """Main function"""
    print("🎮 Real Bypass Method Testing")
    print("By Taquito Loco 🎮")
    print("=" * 50)
    
    success = test_real_bypass()
    
    print("\n" + "=" * 50)
    print("📋 TEST SUMMARY")
    print("=" * 50)
    
    if success:
        print("✅ Testing completed! Check logs/ folder for results.")
        print("💡 Look for:")
        print("   - test_*_*.png (individual method results)")
        print("   - method_comparison_*.png (all methods side by side)")
        print("   - tibia_*_*.png (window state tests)")
    else:
        print("❌ Testing failed. Tibia anti-screenshot might be too strong.")

if __name__ == "__main__":
    main() 