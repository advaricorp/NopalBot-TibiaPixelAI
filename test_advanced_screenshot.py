#!/usr/bin/env python3
"""
Advanced Screenshot Bypass Test Script
By Taquito Loco 🎮

This script tests all the advanced screenshot bypass techniques
to evade Tibia's anti-screenshot measures.

Usage:
    python test_advanced_screenshot.py

Features:
- Tests all bypass methods
- Performance benchmarking
- Success rate analysis
- Real-time testing
- Tibia window detection
"""

import sys
import os
import time
import cv2
import numpy as np
from datetime import datetime

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

try:
    from advanced_screenshot import AdvancedScreenshotBypass, TibiaSpecificBypass
    from vision import ComputerVision
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("💡 Make sure you're running from the project root directory")
    sys.exit(1)

class ScreenshotBypassTester:
    """Test suite for advanced screenshot bypass techniques"""
    
    def __init__(self):
        self.advanced_bypass = AdvancedScreenshotBypass()
        self.tibia_bypass = TibiaSpecificBypass()
        self.cv_system = ComputerVision()
        self.test_results = {}
        
    def test_all_methods(self, num_tests=5):
        """Test all screenshot methods"""
        print("🚀 Testing Advanced Screenshot Bypass Methods")
        print("=" * 60)
        
        methods = [
            ('DirectX Desktop Duplication', self.advanced_bypass._capture_directx_desktop_duplication),
            ('Windows Graphics API', self.advanced_bypass._capture_windows_graphics_api),
            ('Hardware Accelerated', self.advanced_bypass._capture_hardware_accelerated),
            ('Memory Reading', self.advanced_bypass._capture_memory_reading),
            ('GDI+ Optimized', self.advanced_bypass._capture_gdi_optimized),
            ('Fallback Traditional', self.advanced_bypass._capture_fallback_traditional)
        ]
        
        for method_name, method_func in methods:
            print(f"\n🔬 Testing: {method_name}")
            print("-" * 40)
            
            success_count = 0
            total_time = 0
            images = []
            
            for i in range(num_tests):
                try:
                    start_time = time.time()
                    image = method_func()
                    end_time = time.time()
                    
                    if image is not None:
                        success_count += 1
                        total_time += (end_time - start_time)
                        images.append(image)
                        print(f"  ✅ Test {i+1}: Success ({end_time - start_time:.3f}s)")
                    else:
                        print(f"  ❌ Test {i+1}: Failed")
                        
                except Exception as e:
                    print(f"  ❌ Test {i+1}: Error - {e}")
                
                time.sleep(0.1)  # Small delay between tests
            
            # Calculate statistics
            success_rate = (success_count / num_tests) * 100
            avg_time = total_time / success_count if success_count > 0 else 0
            
            self.test_results[method_name] = {
                'success_rate': success_rate,
                'avg_time': avg_time,
                'success_count': success_count,
                'total_tests': num_tests,
                'images': images
            }
            
            print(f"  📊 Results: {success_rate:.1f}% success rate, {avg_time:.3f}s avg time")
        
        return self.test_results
    
    def test_tibia_specific(self):
        """Test Tibia-specific bypass methods"""
        print("\n🎮 Testing Tibia-Specific Bypass Methods")
        print("=" * 60)
        
        # Test Tibia window detection
        print("🔍 Testing Tibia window detection...")
        if self.tibia_bypass.find_tibia_window():
            print("✅ Tibia window found!")
            
            # Test Tibia window capture
            print("📸 Testing Tibia window capture...")
            try:
                start_time = time.time()
                image = self.tibia_bypass.capture_tibia_window_only()
                end_time = time.time()
                
                if image is not None:
                    print(f"✅ Tibia window capture successful ({end_time - start_time:.3f}s)")
                    print(f"   Image size: {image.shape[1]}x{image.shape[0]}")
                    
                    # Save test image
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    filename = f"logs/tibia_window_capture_{timestamp}.png"
                    os.makedirs("logs", exist_ok=True)
                    cv2.imwrite(filename, image)
                    print(f"   💾 Saved as: {filename}")
                    
                    return image
                else:
                    print("❌ Tibia window capture failed")
                    
            except Exception as e:
                print(f"❌ Tibia window capture error: {e}")
        else:
            print("❌ Tibia window not found")
            print("💡 Make sure Tibia is running")
        
        return None
    
    def test_advanced_capture(self, num_tests=10):
        """Test the advanced capture method with automatic method selection"""
        print("\n🚀 Testing Advanced Capture with Auto-Selection")
        print("=" * 60)
        
        success_count = 0
        total_time = 0
        images = []
        
        for i in range(num_tests):
            try:
                start_time = time.time()
                image = self.advanced_bypass.capture_screen_advanced()
                end_time = time.time()
                
                if image is not None:
                    success_count += 1
                    total_time += (end_time - start_time)
                    images.append(image)
                    print(f"✅ Test {i+1}: Success ({end_time - start_time:.3f}s)")
                else:
                    print(f"❌ Test {i+1}: Failed")
                    
            except Exception as e:
                print(f"❌ Test {i+1}: Error - {e}")
            
            time.sleep(0.1)
        
        # Calculate statistics
        success_rate = (success_count / num_tests) * 100
        avg_time = total_time / success_count if success_count > 0 else 0
        
        print(f"\n📊 Advanced Capture Results:")
        print(f"   Success Rate: {success_rate:.1f}%")
        print(f"   Average Time: {avg_time:.3f}s")
        print(f"   Best Method: {self.advanced_bypass.get_best_method()}")
        
        # Show performance stats
        stats = self.advanced_bypass.get_performance_stats()
        print(f"\n📈 Performance Statistics:")
        for method, stat in stats.items():
            if stat['total'] > 0:
                success_rate = (stat['success'] / stat['total']) * 100
                print(f"   {method}: {success_rate:.1f}% success, {stat['avg_time']:.3f}s avg")
        
        return images
    
    def benchmark_performance(self, duration=30):
        """Benchmark performance over time"""
        print(f"\n⏱️ Performance Benchmark ({duration}s)")
        print("=" * 60)
        
        start_time = time.time()
        capture_count = 0
        successful_captures = 0
        total_capture_time = 0
        
        print("🔄 Running benchmark...")
        
        while time.time() - start_time < duration:
            try:
                capture_start = time.time()
                image = self.advanced_bypass.capture_screen_advanced()
                capture_end = time.time()
                
                capture_count += 1
                if image is not None:
                    successful_captures += 1
                    total_capture_time += (capture_end - capture_start)
                
                # Progress indicator
                elapsed = time.time() - start_time
                if capture_count % 10 == 0:
                    progress = (elapsed / duration) * 100
                    print(f"   Progress: {progress:.1f}% ({capture_count} captures)")
                
            except Exception as e:
                print(f"   ❌ Capture error: {e}")
        
        # Calculate final statistics
        total_time = time.time() - start_time
        success_rate = (successful_captures / capture_count) * 100 if capture_count > 0 else 0
        avg_capture_time = total_capture_time / successful_captures if successful_captures > 0 else 0
        captures_per_second = capture_count / total_time
        
        print(f"\n📊 Benchmark Results:")
        print(f"   Total Time: {total_time:.1f}s")
        print(f"   Total Captures: {capture_count}")
        print(f"   Successful Captures: {successful_captures}")
        print(f"   Success Rate: {success_rate:.1f}%")
        print(f"   Average Capture Time: {avg_capture_time:.3f}s")
        print(f"   Captures per Second: {captures_per_second:.1f}")
        
        return {
            'total_time': total_time,
            'total_captures': capture_count,
            'successful_captures': successful_captures,
            'success_rate': success_rate,
            'avg_capture_time': avg_capture_time,
            'captures_per_second': captures_per_second
        }
    
    def save_test_images(self, images, prefix="test_capture"):
        """Save test images for analysis"""
        if not images:
            print("❌ No images to save")
            return
        
        os.makedirs("logs", exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        for i, image in enumerate(images):
            filename = f"logs/{prefix}_{timestamp}_{i+1}.png"
            cv2.imwrite(filename, image)
            print(f"💾 Saved: {filename}")
    
    def generate_report(self):
        """Generate a comprehensive test report"""
        print("\n📋 Generating Test Report")
        print("=" * 60)
        
        report = {
            'timestamp': datetime.now().isoformat(),
            'test_results': self.test_results,
            'best_method': self.advanced_bypass.get_best_method(),
            'performance_stats': self.advanced_bypass.get_performance_stats()
        }
        
        # Save report
        import json
        os.makedirs("logs", exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_filename = f"logs/screenshot_test_report_{timestamp}.json"
        
        with open(report_filename, 'w') as f:
            json.dump(report, f, indent=2, default=str)
        
        print(f"💾 Report saved: {report_filename}")
        
        # Print summary
        print(f"\n📊 Test Summary:")
        print(f"   Best Method: {report['best_method']}")
        
        if self.test_results:
            best_result = max(self.test_results.items(), 
                            key=lambda x: x[1]['success_rate'])
            print(f"   Highest Success Rate: {best_result[0]} ({best_result[1]['success_rate']:.1f}%)")
        
        return report

def main():
    """Main test function"""
    print("🎮 Advanced Screenshot Bypass Test Suite")
    print("By Taquito Loco 🎮")
    print("=" * 60)
    
    # Create tester
    tester = ScreenshotBypassTester()
    
    try:
        # Test all individual methods
        test_results = tester.test_all_methods(num_tests=3)
        
        # Test Tibia-specific methods
        tibia_image = tester.test_tibia_specific()
        
        # Test advanced capture with auto-selection
        advanced_images = tester.test_advanced_capture(num_tests=5)
        
        # Save some test images
        if advanced_images:
            tester.save_test_images(advanced_images[:3], "advanced_capture")
        
        # Run performance benchmark
        benchmark_results = tester.benchmark_performance(duration=10)
        
        # Generate report
        report = tester.generate_report()
        
        print("\n🎉 Test Suite Completed Successfully!")
        print("=" * 60)
        
        # Final recommendations
        best_method = tester.advanced_bypass.get_best_method()
        print(f"💡 Recommendation: Use '{best_method}' method for best results")
        
        if benchmark_results['success_rate'] > 80:
            print("✅ Anti-screenshot bypass is working well!")
        elif benchmark_results['success_rate'] > 50:
            print("⚠️ Anti-screenshot bypass is partially working")
        else:
            print("❌ Anti-screenshot bypass needs improvement")
        
    except KeyboardInterrupt:
        print("\n⏹️ Test interrupted by user")
    except Exception as e:
        print(f"\n❌ Test error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 