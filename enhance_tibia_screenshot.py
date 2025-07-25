#!/usr/bin/env python3
"""
Enhance Tibia Screenshot
By Taquito Loco 🎮

Takes a Tibia screenshot and enhances it to make the content visible.
"""

import sys
import os
import time
import cv2
import numpy as np
from datetime import datetime

# Add src to path
sys.path.append('src')

def enhance_tibia_screenshot():
    """Take a Tibia screenshot and enhance it"""
    print("🎮 Enhancing Tibia Screenshot")
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
        
        # Basic info
        height, width = image.shape[:2]
        print(f"📏 Image size: {width}x{height}")
        
        # Convert to different formats for enhancement
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Original statistics
        original_mean = np.mean(gray)
        original_std = np.std(gray)
        print(f"📊 Original - Mean: {original_mean:.1f}, Std: {original_std:.1f}")
        
        # Create enhanced versions
        print(f"\n🔧 Creating enhanced versions...")
        
        os.makedirs("logs", exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # 1. Brightness enhancement
        enhanced_bright = enhance_brightness(image, 2.0)
        bright_filename = f"logs/tibia_enhanced_bright_{timestamp}.png"
        cv2.imwrite(bright_filename, enhanced_bright)
        print(f"💡 Brightness enhanced: {bright_filename}")
        
        # 2. Contrast enhancement
        enhanced_contrast = enhance_contrast(image, 2.0)
        contrast_filename = f"logs/tibia_enhanced_contrast_{timestamp}.png"
        cv2.imwrite(contrast_filename, enhanced_contrast)
        print(f"🎨 Contrast enhanced: {contrast_filename}")
        
        # 3. Histogram equalization
        enhanced_hist = enhance_histogram(image)
        hist_filename = f"logs/tibia_enhanced_hist_{timestamp}.png"
        cv2.imwrite(hist_filename, enhanced_hist)
        print(f"📊 Histogram equalized: {hist_filename}")
        
        # 4. CLAHE (Contrast Limited Adaptive Histogram Equalization)
        enhanced_clahe = enhance_clahe(image)
        clahe_filename = f"logs/tibia_enhanced_clahe_{timestamp}.png"
        cv2.imwrite(clahe_filename, enhanced_clahe)
        print(f"🔬 CLAHE enhanced: {clahe_filename}")
        
        # 5. Gamma correction
        enhanced_gamma = enhance_gamma(image, 0.5)
        gamma_filename = f"logs/tibia_enhanced_gamma_{timestamp}.png"
        cv2.imwrite(gamma_filename, enhanced_gamma)
        print(f"📈 Gamma corrected: {gamma_filename}")
        
        # 6. Combined enhancement
        enhanced_combined = enhance_combined(image)
        combined_filename = f"logs/tibia_enhanced_combined_{timestamp}.png"
        cv2.imwrite(combined_filename, enhanced_combined)
        print(f"🚀 Combined enhancement: {combined_filename}")
        
        # Save original for comparison
        original_filename = f"logs/tibia_original_{timestamp}.png"
        cv2.imwrite(original_filename, image)
        print(f"📸 Original: {original_filename}")
        
        # Create comparison grid
        comparison_filename = f"logs/tibia_comparison_{timestamp}.png"
        create_comparison_grid(image, enhanced_bright, enhanced_contrast, 
                             enhanced_hist, enhanced_clahe, enhanced_gamma, 
                             enhanced_combined, comparison_filename)
        print(f"🖼️ Comparison grid: {comparison_filename}")
        
        # Analyze enhanced versions
        print(f"\n📊 ENHANCED VERSION ANALYSIS")
        print("=" * 35)
        
        analyze_enhanced_versions(image, enhanced_bright, enhanced_contrast, 
                                enhanced_hist, enhanced_clahe, enhanced_gamma, 
                                enhanced_combined)
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def enhance_brightness(image, factor):
    """Enhance brightness"""
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    hsv[:, :, 2] = np.clip(hsv[:, :, 2] * factor, 0, 255)
    return cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

def enhance_contrast(image, factor):
    """Enhance contrast"""
    lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
    lab[:, :, 0] = np.clip(lab[:, :, 0] * factor, 0, 255)
    return cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)

def enhance_histogram(image):
    """Histogram equalization"""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    enhanced_gray = cv2.equalizeHist(gray)
    return cv2.cvtColor(enhanced_gray, cv2.COLOR_GRAY2BGR)

def enhance_clahe(image):
    """CLAHE enhancement"""
    lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    lab[:, :, 0] = clahe.apply(lab[:, :, 0])
    return cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)

def enhance_gamma(image, gamma):
    """Gamma correction"""
    inv_gamma = 1.0 / gamma
    table = np.array([((i / 255.0) ** inv_gamma) * 255 for i in np.arange(0, 256)]).astype("uint8")
    return cv2.LUT(image, table)

def enhance_combined(image):
    """Combined enhancement"""
    # Apply multiple enhancements
    enhanced = enhance_brightness(image, 1.5)
    enhanced = enhance_contrast(enhanced, 1.3)
    enhanced = enhance_gamma(enhanced, 0.7)
    return enhanced

def create_comparison_grid(original, bright, contrast, hist, clahe, gamma, combined, filename):
    """Create a comparison grid of all versions"""
    try:
        # Resize all images to same size for comparison
        height, width = original.shape[:2]
        target_size = (width//2, height//2)  # Half size for grid
        
        # Resize all images
        original_resized = cv2.resize(original, target_size)
        bright_resized = cv2.resize(bright, target_size)
        contrast_resized = cv2.resize(contrast, target_size)
        hist_resized = cv2.resize(hist, target_size)
        clahe_resized = cv2.resize(clahe, target_size)
        gamma_resized = cv2.resize(gamma, target_size)
        combined_resized = cv2.resize(combined, target_size)
        
        # Create grid (3 rows, 3 columns)
        grid_height = target_size[1] * 3
        grid_width = target_size[0] * 3
        
        # Create blank grid
        grid = np.zeros((grid_height, grid_width, 3), dtype=np.uint8)
        
        # Place images in grid
        images = [
            (original_resized, "Original"),
            (bright_resized, "Bright"),
            (contrast_resized, "Contrast"),
            (hist_resized, "Histogram"),
            (clahe_resized, "CLAHE"),
            (gamma_resized, "Gamma"),
            (combined_resized, "Combined"),
            (np.zeros_like(original_resized), ""),  # Empty space
            (np.zeros_like(original_resized), "")   # Empty space
        ]
        
        for i, (img, label) in enumerate(images):
            row = i // 3
            col = i % 3
            
            y_start = row * target_size[1]
            y_end = (row + 1) * target_size[1]
            x_start = col * target_size[0]
            x_end = (col + 1) * target_size[0]
            
            grid[y_start:y_end, x_start:x_end] = img
            
            # Add label
            if label:
                cv2.putText(grid, label, (x_start + 10, y_start + 30), 
                           cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        
        cv2.imwrite(filename, grid)
        
    except Exception as e:
        print(f"   ❌ Error creating comparison grid: {e}")

def analyze_enhanced_versions(original, bright, contrast, hist, clahe, gamma, combined):
    """Analyze all enhanced versions"""
    versions = [
        ("Original", original),
        ("Bright", bright),
        ("Contrast", contrast),
        ("Histogram", hist),
        ("CLAHE", clahe),
        ("Gamma", gamma),
        ("Combined", combined)
    ]
    
    print(f"{'Version':<12} {'Mean':<8} {'Std':<8} {'Min':<8} {'Max':<8}")
    print("-" * 50)
    
    for name, img in versions:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        mean_val = np.mean(gray)
        std_val = np.std(gray)
        min_val = np.min(gray)
        max_val = np.max(gray)
        
        print(f"{name:<12} {mean_val:<8.1f} {std_val:<8.1f} {min_val:<8.0f} {max_val:<8.0f}")

def main():
    """Main function"""
    print("🎮 Tibia Screenshot Enhancement")
    print("By Taquito Loco 🎮")
    print("=" * 50)
    
    success = enhance_tibia_screenshot()
    
    print("\n" + "=" * 50)
    print("📋 ENHANCEMENT SUMMARY")
    print("=" * 50)
    
    if success:
        print("✅ Enhancement completed! Check logs/ folder for enhanced images.")
        print("💡 Look for:")
        print("   - tibia_enhanced_*_*.png (different enhancement methods)")
        print("   - tibia_comparison_*.png (all versions side by side)")
        print("   - tibia_original_*.png (original for comparison)")
    else:
        print("❌ Enhancement failed. Check if Tibia is running.")

if __name__ == "__main__":
    main() 