"""
Status Detector for Tibia Bot
By Taquito Loco 🎮

- Detects health and mana percentage from the screen using color detection (OpenCV)
- Fast and efficient (no OCR required)
- Easy to adjust color ranges for different clients/themes
"""
import cv2
import numpy as np
import logging

logger = logging.getLogger(__name__)

class StatusDetector:
    def __init__(self, screen_reader):
        self.screen_reader = screen_reader
        # Default regions for health/mana bars (adjust as needed)
        self.health_bar_region = (50, 40, 200, 10)  # (x, y, w, h)
        self.mana_bar_region = (50, 55, 200, 10)
        # Color ranges (BGR) for health (red) and mana (blue)
        self.health_color = ([0, 0, 180], [80, 80, 255])  # Lower, Upper
        self.mana_color = ([180, 0, 0], [255, 80, 80])

    def get_health_percent(self) -> float:
        return self._get_bar_percent(self.health_bar_region, self.health_color, 'health')

    def get_mana_percent(self) -> float:
        return self._get_bar_percent(self.mana_bar_region, self.mana_color, 'mana')

    def _get_bar_percent(self, region, color_range, label) -> float:
        frame = self.screen_reader.capture_single_frame()
        if frame is None:
            logger.error(f"StatusDetector: No frame for {label} bar detection")
            return 0.0
        x, y, w, h = region
        bar_img = frame[y:y+h, x:x+w]
        lower = np.array(color_range[0], dtype=np.uint8)
        upper = np.array(color_range[1], dtype=np.uint8)
        mask = cv2.inRange(bar_img, lower, upper)
        bar_pixels = np.count_nonzero(mask)
        percent = bar_pixels / (w * h)
        percent = min(max(percent, 0.0), 1.0)
        logger.info(f"StatusDetector: {label} bar {percent*100:.1f}%")
        return percent

# Example usage:
# detector = StatusDetector(screen_reader)
# hp = detector.get_health_percent()
# mp = detector.get_mana_percent() 