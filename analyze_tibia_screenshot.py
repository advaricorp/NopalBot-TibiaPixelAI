#!/usr/bin/env python3
"""
Analyze Tibia Screenshot Content
By Taquito Loco 🎮

Takes a screenshot of Tibia and analyzes the content to verify if we're actually capturing the game.
"""

import sys
import os
import time
import cv2
import numpy as np
from datetime import datetime

# Add src to path
sys.path.append('src')

def analyze_tibia_screenshot():
    """Take a screenshot of Tibia and analyze its content"""
    print("🎮 Analyzing Tibia Screenshot Content")
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
        
        # Take screenshot
        print("\n📸 Taking screenshot...")
        start_time = time.time()
        image = bypass.capture_simple_working()
        end_time = time.time()
        
        if image is None:
            print("❌ Screenshot failed")
            return False
        
        capture_time = end_time - start_time
        print(f"✅ Screenshot taken in {capture_time:.3f}s")
        
        # Basic image info
        height, width = image.shape[:2]
        print(f"📏 Image size: {width}x{height}")
        
        # Convert to different color spaces for analysis
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        
        # Basic statistics
        mean_brightness = np.mean(gray)
        std_brightness = np.std(gray)
        min_brightness = np.min(gray)
        max_brightness = np.max(gray)
        
        print(f"\n📊 BASIC STATISTICS")
        print("=" * 30)
        print(f"💡 Mean brightness: {mean_brightness:.1f}")
        print(f"📈 Brightness range: {min_brightness} - {max_brightness}")
        print(f"🎨 Standard deviation: {std_brightness:.1f}")
        
        # Analyze color distribution
        print(f"\n🎨 COLOR ANALYSIS")
        print("=" * 25)
        
        # BGR channels
        b_mean = np.mean(image[:, :, 0])
        g_mean = np.mean(image[:, :, 1])
        r_mean = np.mean(image[:, :, 2])
        
        print(f"🔵 Blue channel: {b_mean:.1f}")
        print(f"🟢 Green channel: {g_mean:.1f}")
        print(f"🔴 Red channel: {r_mean:.1f}")
        
        # HSV analysis
        h_mean = np.mean(hsv[:, :, 0])
        s_mean = np.mean(hsv[:, :, 1])
        v_mean = np.mean(hsv[:, :, 2])
        
        print(f"🌈 Hue: {h_mean:.1f}")
        print(f"💎 Saturation: {s_mean:.1f}")
        print(f"💡 Value: {v_mean:.1f}")
        
        # Detect if image is mostly black/empty
        print(f"\n🔍 CONTENT ANALYSIS")
        print("=" * 25)
        
        # Count very dark pixels
        dark_pixels = np.sum(gray < 10)
        total_pixels = gray.size
        dark_percentage = (dark_pixels / total_pixels) * 100
        
        print(f"⚫ Very dark pixels (<10): {dark_pixels:,} ({dark_percentage:.1f}%)")
        
        # Count very bright pixels
        bright_pixels = np.sum(gray > 200)
        bright_percentage = (bright_pixels / total_pixels) * 100
        
        print(f"⚪ Very bright pixels (>200): {bright_pixels:,} ({bright_percentage:.1f}%)")
        
        # Count medium brightness pixels
        medium_pixels = np.sum((gray >= 50) & (gray <= 150))
        medium_percentage = (medium_pixels / total_pixels) * 100
        
        print(f"🟡 Medium pixels (50-150): {medium_pixels:,} ({medium_percentage:.1f}%)")
        
        # Edge detection to see if there's any structure
        print(f"\n🔍 EDGE DETECTION")
        print("=" * 20)
        
        edges = cv2.Canny(gray, 50, 150)
        edge_pixels = np.sum(edges > 0)
        edge_percentage = (edge_pixels / total_pixels) * 100
        
        print(f"📐 Edge pixels: {edge_pixels:,} ({edge_percentage:.1f}%)")
        
        # Save images for visual inspection
        print(f"\n💾 SAVING ANALYSIS IMAGES")
        print("=" * 30)
        
        os.makedirs("logs", exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Save original
        original_filename = f"logs/tibia_original_{timestamp}.png"
        cv2.imwrite(original_filename, image)
        print(f"📸 Original: {original_filename}")
        
        # Save grayscale
        gray_filename = f"logs/tibia_gray_{timestamp}.png"
        cv2.imwrite(gray_filename, gray)
        print(f"⚫ Grayscale: {gray_filename}")
        
        # Save edges
        edges_filename = f"logs/tibia_edges_{timestamp}.png"
        cv2.imwrite(edges_filename, edges)
        print(f"📐 Edges: {edges_filename}")
        
        # Save histogram
        hist_filename = f"logs/tibia_histogram_{timestamp}.png"
        create_histogram(gray, hist_filename)
        print(f"📊 Histogram: {hist_filename}")
        
        # Content assessment
        print(f"\n🎯 CONTENT ASSESSMENT")
        print("=" * 25)
        
        if dark_percentage > 80:
            print("❌ Image is mostly black - likely anti-screenshot active")
            assessment = "BLACK_SCREEN"
        elif edge_percentage < 1:
            print("❌ Very few edges - likely blank or uniform content")
            assessment = "BLANK_CONTENT"
        elif medium_percentage > 30:
            print("✅ Good content distribution - likely real game content")
            assessment = "GOOD_CONTENT"
        elif bright_percentage > 20:
            print("⚠️ High brightness - might be overexposed or wrong window")
            assessment = "BRIGHT_CONTENT"
        else:
            print("⚠️ Mixed content - needs further analysis")
            assessment = "MIXED_CONTENT"
        
        # Try to detect Tibia-specific content
        print(f"\n🎮 TIBIA CONTENT DETECTION")
        print("=" * 30)
        
        tibia_detected = detect_tibia_content(image, gray, hsv)
        
        if tibia_detected:
            print("✅ Tibia content detected!")
        else:
            print("❌ No clear Tibia content detected")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def create_histogram(gray_image, filename):
    """Create and save histogram of grayscale image"""
    try:
        import matplotlib.pyplot as plt
        
        plt.figure(figsize=(10, 6))
        plt.hist(gray_image.ravel(), bins=256, range=[0, 256], alpha=0.7, color='blue')
        plt.title('Grayscale Histogram')
        plt.xlabel('Pixel Value')
        plt.ylabel('Frequency')
        plt.grid(True, alpha=0.3)
        plt.savefig(filename, dpi=150, bbox_inches='tight')
        plt.close()
        
    except ImportError:
        print("   ⚠️ matplotlib not available, skipping histogram")
    except Exception as e:
        print(f"   ❌ Error creating histogram: {e}")

def detect_tibia_content(image, gray, hsv):
    """Try to detect Tibia-specific content"""
    try:
        # Look for common Tibia colors
        tibia_detected = False
        
        # Green colors (grass, trees)
        green_mask = cv2.inRange(hsv, (40, 40, 40), (80, 255, 255))
        green_pixels = np.sum(green_mask > 0)
        green_percentage = (green_pixels / green_mask.size) * 100
        
        if green_percentage > 5:
            print(f"   🌲 Green content detected: {green_percentage:.1f}%")
            tibia_detected = True
        
        # Brown colors (dirt, walls)
        brown_mask = cv2.inRange(hsv, (10, 50, 50), (20, 255, 255))
        brown_pixels = np.sum(brown_mask > 0)
        brown_percentage = (brown_pixels / brown_mask.size) * 100
        
        if brown_percentage > 5:
            print(f"   🟫 Brown content detected: {brown_percentage:.1f}%")
            tibia_detected = True
        
        # Blue colors (water, sky)
        blue_mask = cv2.inRange(hsv, (100, 50, 50), (130, 255, 255))
        blue_pixels = np.sum(blue_mask > 0)
        blue_percentage = (blue_pixels / blue_mask.size) * 100
        
        if blue_percentage > 5:
            print(f"   💙 Blue content detected: {blue_percentage:.1f}%")
            tibia_detected = True
        
        # Red colors (health bars, enemies)
        red_mask1 = cv2.inRange(hsv, (0, 50, 50), (10, 255, 255))
        red_mask2 = cv2.inRange(hsv, (170, 50, 50), (180, 255, 255))
        red_mask = cv2.bitwise_or(red_mask1, red_mask2)
        red_pixels = np.sum(red_mask > 0)
        red_percentage = (red_pixels / red_mask.size) * 100
        
        if red_percentage > 2:
            print(f"   🔴 Red content detected: {red_percentage:.1f}%")
            tibia_detected = True
        
        # Check for text-like patterns (high contrast areas)
        high_contrast = cv2.Laplacian(gray, cv2.CV_64F).var()
        if high_contrast > 100:
            print(f"   📝 High contrast detected: {high_contrast:.1f}")
            tibia_detected = True
        
        return tibia_detected
        
    except Exception as e:
        print(f"   ❌ Error in Tibia detection: {e}")
        return False

def main():
    """Main function"""
    print("🎮 Tibia Screenshot Content Analysis")
    print("By Taquito Loco 🎮")
    print("=" * 60)
    
    success = analyze_tibia_screenshot()
    
    print("\n" + "=" * 60)
    print("📋 ANALYSIS SUMMARY")
    print("=" * 60)
    
    if success:
        print("✅ Analysis completed! Check logs/ folder for detailed images.")
        print("💡 Look for:")
        print("   - tibia_original_*.png (original screenshot)")
        print("   - tibia_gray_*.png (grayscale version)")
        print("   - tibia_edges_*.png (edge detection)")
        print("   - tibia_histogram_*.png (brightness distribution)")
    else:
        print("❌ Analysis failed. Check if Tibia is running.")

if __name__ == "__main__":
    main() 