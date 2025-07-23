# AI & OCR Integration for Tibia Bot Pro
·By Taquito Loco Skunk Labs

## 1. OCR (Tesseract)
- Use Tesseract to read numbers (HP, mana, loot count) from the screen.
- Install Tesseract:
  - Windows: https://github.com/tesseract-ocr/tesseract
  - Linux: `sudo apt install tesseract-ocr`
- Python bindings:
  ```bash
  pip install pytesseract
  ```
- Example usage in Python:
  ```python
  import pytesseract
  import cv2
  img = cv2.imread('screenshot.png')
  text = pytesseract.image_to_string(img)
  print(text)
  ```
- Use for: reading HP/mana numbers, loot amounts, etc.

## 2. Deep Learning (GPU/RTX)
- Use PyTorch or TensorFlow for advanced detection (loot, bars, monsters, etc).
- Install:
  ```bash
  pip install torch torchvision
  # or
  pip install tensorflow
  ```
- Train models on screenshots (classification, segmentation, detection).
- Save models in `ai/models/` and load in your bot.
- Example: detect gold coins, rare loot, or monster types with YOLO/UNet/ResNet.
- Use your RTX 2060 for fast inference.

## 3. Folder Structure
- `ai/models/` — place your trained models here
- `ai/scripts/` — training/inference scripts
- `ai/data/` — datasets/screenshots for training

## 4. Integration
- Add hooks in bot to switch between color, OCR, or AI detection.
- Use AI for loot, powers, bars, or anything you want to automate.

## 5. Tips
- Always test new models in Safe Mode first.
- Document your templates/models for future you/others.
- Share your best models with la banda!

By Taquito Loco 🎮 