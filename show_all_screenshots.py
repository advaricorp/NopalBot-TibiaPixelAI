#!/usr/bin/env python3
"""
Show All Screenshots Test
By Taquito Loco 🎮

Takes 5 screenshots and displays them all to check quality.
"""

import sys
import os
import time
import cv2
import numpy as np
from datetime import datetime

# Add src to path
sys.path.append('src')

def show_all_screenshots():
    """Take 5 screenshots and show them all"""
    print("🎮 Taking 5 Screenshots to Check Quality")
    print("=" * 60)
    
    try:
        from simple_working_bypass import SimpleWorkingBypass
        
        bypass = SimpleWorkingBypass()
        print("✅ SimpleWorkingBypass created")
        
        # Check if Tibia is found
        if not bypass.find_tibia_window():
            print("❌ Tibia not found - make sure Tibia is running")
            return False
        
        print("✅ Tibia window found!")
        
        # Take 5 screenshots
        screenshots = []
        brightness_values = []
        
        for i in range(5):
            print(f"\n📸 Taking screenshot {i+1}/5...")
            
            try:
                start_time = time.time()
                image = bypass.capture_simple_working()
                end_time = time.time()
                
                if image is not None:
                    # Check brightness
                    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                    mean_brightness = np.mean(gray)
                    std_brightness = np.std(gray)
                    
                    brightness_values.append(mean_brightness)
                    screenshots.append({
                        'image': image,
                        'brightness': mean_brightness,
                        'contrast': std_brightness,
                        'time': end_time - start_time,
                        'size': f"{image.shape[1]}x{image.shape[0]}"
                    })
                    
                    print(f"   ✅ Success: {mean_brightness:.1f} brightness, {std_brightness:.1f} contrast ({end_time - start_time:.3f}s)")
                else:
                    print(f"   ❌ Failed")
                    screenshots.append(None)
                
                time.sleep(0.1)  # Small delay
                
            except Exception as e:
                print(f"   ❌ Error: {e}")
                screenshots.append(None)
        
        # Save all screenshots
        print(f"\n💾 Saving all screenshots...")
        os.makedirs("logs", exist_ok=True)
        
        successful_screenshots = [s for s in screenshots if s is not None]
        
        if successful_screenshots:
            print(f"✅ {len(successful_screenshots)}/5 screenshots successful")
            
            # Save individual screenshots
            for i, screenshot in enumerate(screenshots):
                if screenshot is not None:
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    filename = f"logs/screenshot_{i+1}_{timestamp}.png"
                    cv2.imwrite(filename, screenshot['image'])
                    print(f"   💾 Screenshot {i+1}: {filename}")
            
            # Create comparison image
            print(f"\n🖼️ Creating comparison image...")
            create_comparison_image(successful_screenshots)
            
            # Show statistics
            show_statistics(successful_screenshots)
            
            return True
        else:
            print("❌ No screenshots successful")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def create_comparison_image(screenshots):
    """Create a comparison image showing all screenshots"""
    try:
        if not screenshots:
            return
        
        # Get dimensions
        height, width = screenshots[0]['image'].shape[:2]
        
        # Create comparison image (2 rows, 3 columns)
        comparison_height = height * 2
        comparison_width = width * 3
        
        # Create blank image
        comparison = np.zeros((comparison_height, comparison_width, 3), dtype=np.uint8)
        
        # Place screenshots
        positions = [
            (0, 0), (0, width), (0, width*2),
            (height, 0), (height, width)
        ]
        
        for i, screenshot in enumerate(screenshots[:5]):
            if i < len(positions):
                y, x = positions[i]
                comparison[y:y+height, x:x+width] = screenshot['image']
                
                # Add text label
                label = f"S{i+1}: {screenshot['brightness']:.1f}"
                cv2.putText(comparison, label, (x+10, y+30), 
                           cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        
        # Save comparison
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"logs/comparison_{timestamp}.png"
        cv2.imwrite(filename, comparison)
        print(f"   💾 Comparison image: {filename}")
        
    except Exception as e:
        print(f"   ❌ Error creating comparison: {e}")

def show_statistics(screenshots):
    """Show detailed statistics"""
    print(f"\n📊 DETAILED STATISTICS")
    print("=" * 40)
    
    if not screenshots:
        print("❌ No screenshots to analyze")
        return
    
    # Calculate statistics
    brightness_values = [s['brightness'] for s in screenshots]
    contrast_values = [s['contrast'] for s in screenshots]
    time_values = [s['time'] for s in screenshots]
    
    avg_brightness = np.mean(brightness_values)
    avg_contrast = np.mean(contrast_values)
    avg_time = np.mean(time_values)
    
    min_brightness = np.min(brightness_values)
    max_brightness = np.max(brightness_values)
    
    print(f"📸 Screenshots analyzed: {len(screenshots)}")
    print(f"⏱️ Average time: {avg_time:.3f}s")
    print(f"💡 Average brightness: {avg_brightness:.1f}")
    print(f"🎨 Average contrast: {avg_contrast:.1f}")
    print(f"📈 Brightness range: {min_brightness:.1f} - {max_brightness:.1f}")
    
    # Quality assessment
    print(f"\n🔍 QUALITY ASSESSMENT")
    print("=" * 30)
    
    if avg_brightness < 10:
        print("❌ Very dark - Anti-screenshot active")
    elif avg_brightness < 30:
        print("⚠️ Dark - Partial bypass")
    elif avg_brightness < 50:
        print("⚠️ Moderate - Some bypass")
    else:
        print("✅ Good - Bypass working")
    
    if avg_contrast < 10:
        print("❌ Low contrast - Poor image quality")
    elif avg_contrast < 30:
        print("⚠️ Moderate contrast")
    else:
        print("✅ Good contrast")
    
    # Individual analysis
    print(f"\n📋 INDIVIDUAL ANALYSIS")
    print("=" * 30)
    
    for i, screenshot in enumerate(screenshots):
        quality = "❌" if screenshot['brightness'] < 10 else "⚠️" if screenshot['brightness'] < 30 else "✅"
        print(f"{quality} Screenshot {i+1}: {screenshot['brightness']:.1f} brightness, {screenshot['contrast']:.1f} contrast")

def main():
    """Main function"""
    print("🎮 Show All Screenshots Test")
    print("By Taquito Loco 🎮")
    print("=" * 60)
    
    success = show_all_screenshots()
    
    print("\n" + "=" * 60)
    print("📋 TEST SUMMARY")
    print("=" * 60)
    
    if success:
        print("✅ Test completed! Check logs/ folder for images.")
        print("💡 Look for:")
        print("   - screenshot_1_*.png to screenshot_5_*.png")
        print("   - comparison_*.png (all screenshots side by side)")
    else:
        print("❌ Test failed. Check if Tibia is running.")

if __name__ == "__main__":
    main() 