#!/bin/bash

# PBT Bot - WSL Quick Setup Script
# By Taquito Loco 🎮
# Optimized for Ubuntu 22.04 in WSL2

set -e

echo "🚀 PBT Bot - WSL Quick Setup"
echo "============================="
echo "🐧 Optimized for Ubuntu 22.04 + WSL2"
echo "⏰ Started at: $(date)"
echo

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️ $1${NC}"
}

print_header() {
    echo -e "${BLUE}🔧 $1${NC}"
}

# Check if running in WSL
print_header "Checking WSL environment..."
if grep -qi microsoft /proc/version; then
    print_success "Running in WSL environment"
    WSL_VERSION=$(grep -o "WSL[0-9]*" /proc/version | head -1)
    print_info "WSL Version: $WSL_VERSION"
else
    print_warning "Not running in WSL environment"
fi

# Check Ubuntu version
UBUNTU_VERSION=$(lsb_release -rs)
print_info "Ubuntu Version: $UBUNTU_VERSION"

if [[ "$UBUNTU_VERSION" != "22.04" && "$UBUNTU_VERSION" != "20.04" ]]; then
    print_warning "This script is optimized for Ubuntu 22.04. You're running $UBUNTU_VERSION"
fi

# Update system
print_header "Updating system packages..."
sudo apt update && sudo apt upgrade -y

# Install essential packages for WSL
print_header "Installing essential packages for WSL..."
sudo apt install -y \
    python3 \
    python3-pip \
    python3-venv \
    python3-tk \
    tk-dev \
    git \
    screen \
    tmux \
    xvfb \
    x11vnc \
    tightvncserver \
    curl \
    wget \
    nano \
    htop \
    net-tools \
    iputils-ping \
    build-essential \
    libssl-dev \
    libffi-dev \
    python3-dev \
    libjpeg-dev \
    libpng-dev \
    libtiff-dev \
    libavcodec-dev \
    libavformat-dev \
    libswscale-dev \
    libv4l-dev \
    libxvidcore-dev \
    libx264-dev \
    libgtk-3-dev \
    libatlas-base-dev \
    gfortran \
    libhdf5-dev \
    libhdf5-serial-dev \
    libhdf5-103 \
    libqtgui4 \
    libqtwebkit4 \
    libqt4-test \
    python3-pyqt5 \
    libgstreamer1.0-0 \
    gstreamer1.0-plugins-base \
    gstreamer1.0-plugins-good \
    gstreamer1.0-plugins-bad \
    gstreamer1.0-plugins-ugly \
    gstreamer1.0-libav \
    gstreamer1.0-tools \
    gstreamer1.0-x \
    gstreamer1.0-alsa \
    gstreamer1.0-gl \
    gstreamer1.0-gtk3 \
    gstreamer1.0-qt5 \
    gstreamer1.0-pulseaudio \
    x11-apps \
    xauth \
    x11-utils \
    x11-xserver-utils

# Create PBT directory
PBT_DIR="$HOME/pbt_bot"
print_header "Setting up PBT Bot directory..."
mkdir -p "$PBT_DIR"
cd "$PBT_DIR"

# Create virtual environment
print_header "Creating Python virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install Python dependencies
print_header "Installing Python dependencies..."
pip install -r requirements_linux.txt

# Install additional WSL-specific packages
pip install python-xlib pynput

# Create WSL-specific configuration
print_header "Creating WSL-specific configurations..."

# Create .bashrc additions for WSL
cat >> ~/.bashrc << 'EOF'

# PBT Bot WSL Configuration
export DISPLAY=:99
export DISPLAY_WSL=localhost:0.0

# PBT Bot aliases
alias pbt-status='cd ~/pbt_bot && ./status_bot.sh'
alias pbt-start='cd ~/pbt_bot && ./start_bot.sh'
alias pbt-stop='cd ~/pbt_bot && ./stop_bot.sh'
alias pbt-logs='cd ~/pbt_bot && tail -f logs/pbt_bot.log'
alias pbt-test='cd ~/pbt_bot && ./test_wsl.sh'

# WSL performance optimizations
export PYTHONUNBUFFERED=1
export PYTHONDONTWRITEBYTECODE=1
EOF

# Create WSL performance configuration
print_header "Creating WSL performance configuration..."

# Create .wslconfig instructions
cat > WSL_CONFIG_INSTRUCTIONS.txt << 'EOF'
WSL Performance Configuration Instructions
==========================================

1. Create .wslconfig file in your Windows user directory:
   C:\Users\YourUsername\.wslconfig

2. Add the following content:
[wsl2]
memory=8GB
processors=4
swap=2GB
localhostForwarding=true
nestedVirtualization=true

3. Restart WSL:
   wsl --shutdown
   wsl

4. Verify configuration:
   cat /proc/meminfo | grep MemTotal
   nproc
EOF

# Create quick start script for WSL
cat > quick_start_wsl.sh << 'EOF'
#!/bin/bash

# PBT Bot - WSL Quick Start
# By Taquito Loco 🎮

echo "🚀 PBT Bot - WSL Quick Start"
echo "============================"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found. Run setup first."
    exit 1
fi

# Activate virtual environment
source venv/bin/activate

# Start virtual desktop
echo "🖥️ Starting virtual desktop..."
Xvfb :99 -screen 0 1024x768x24 &
sleep 3

# Start a test bot
echo "🤖 Starting test bot..."
screen -dmS pbt_test_bot bash -c "
    echo 'Starting PBT Bot in WSL...'
    export DISPLAY=:99
    python3 main_linux.py --config config/bot_config.json --name test_bot --headless
"

echo "✅ PBT Bot started in WSL!"
echo "📋 To view logs: screen -r pbt_test_bot"
echo "🛑 To stop: screen -S pbt_test_bot -X quit"
EOF

chmod +x quick_start_wsl.sh

# Create WSL optimization script
cat > optimize_wsl.sh << 'EOF'
#!/bin/bash

# WSL Optimization Script
# By Taquito Loco 🎮

echo "🔧 Optimizing WSL for PBT Bot..."

# Update system
sudo apt update && sudo apt upgrade -y

# Install performance tools
sudo apt install -y htop iotop nethogs

# Optimize Python
pip install --upgrade pip
pip install psutil

# Create swap if needed
if [ ! -f /swapfile ]; then
    echo "Creating swap file..."
    sudo fallocate -l 2G /swapfile
    sudo chmod 600 /swapfile
    sudo mkswap /swapfile
    sudo swapon /swapfile
    echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
fi

# Optimize file system
echo "Optimizing file system..."
sudo sysctl vm.swappiness=10

echo "✅ WSL optimization complete!"
EOF

chmod +x optimize_wsl.sh

# Create WSL troubleshooting script
cat > troubleshoot_wsl.sh << 'EOF'
#!/bin/bash

# WSL Troubleshooting Script
# By Taquito Loco 🎮

echo "🔍 WSL Troubleshooting"
echo "======================"

echo "1. WSL Information:"
echo "   Version: $(grep -o 'WSL[0-9]*' /proc/version | head -1)"
echo "   Ubuntu: $(lsb_release -rs)"
echo "   Kernel: $(uname -r)"

echo -e "\n2. System Resources:"
echo "   Memory: $(free -h | grep Mem | awk '{print $2}')"
echo "   CPU Cores: $(nproc)"
echo "   Disk: $(df -h / | awk 'NR==2 {print $4}') available"

echo -e "\n3. Network:"
ping -c 1 8.8.8.8 > /dev/null && echo "   ✅ Internet: OK" || echo "   ❌ Internet: FAILED"

echo -e "\n4. Display:"
if [ -n "$DISPLAY" ]; then
    echo "   ✅ DISPLAY: $DISPLAY"
else
    echo "   ❌ DISPLAY: Not set"
fi

echo -e "\n5. Python:"
if command -v python3 &> /dev/null; then
    echo "   ✅ Python3: $(python3 --version)"
else
    echo "   ❌ Python3: Not found"
fi

echo -e "\n6. Virtual Environment:"
if [ -d "venv" ]; then
    echo "   ✅ Virtual environment: Found"
else
    echo "   ❌ Virtual environment: Not found"
fi

echo -e "\n7. PBT Bot Files:"
if [ -f "main_linux.py" ]; then
    echo "   ✅ Main script: Found"
else
    echo "   ❌ Main script: Not found"
fi

if [ -f "config/bot_config.json" ]; then
    echo "   ✅ Config: Found"
else
    echo "   ❌ Config: Not found"
fi

echo -e "\n8. Common Solutions:"
echo "   - Restart WSL: wsl --shutdown && wsl"
echo "   - Reinstall: ./install_ubuntu.sh"
echo "   - Optimize: ./optimize_wsl.sh"
echo "   - Test: ./test_wsl.sh"
EOF

chmod +x troubleshoot_wsl.sh

# Create WSL-specific README
cat > README_WSL_QUICK.md << 'EOF'
# 🐧 PBT Bot - WSL Quick Guide

## 🚀 Quick Start (WSL)

1. **Setup WSL:**
   ```bash
   ./setup_wsl_quick.sh
   ```

2. **Quick Start:**
   ```bash
   ./quick_start_wsl.sh
   ```

3. **Check Status:**
   ```bash
   ./status_bot.sh
   ```

4. **Troubleshoot:**
   ```bash
   ./troubleshoot_wsl.sh
   ```

## 🔧 WSL Optimizations

1. **Performance:**
   ```bash
   ./optimize_wsl.sh
   ```

2. **Windows Configuration:**
   - Create `C:\Users\YourUsername\.wslconfig`
   - Add memory and CPU allocations

3. **Display Setup:**
   - Install VcXsrv on Windows
   - Set `export DISPLAY=localhost:0.0` in WSL

## 📊 Monitoring

- **System:** `htop`
- **Bots:** `./status_bot.sh`
- **Logs:** `tail -f logs/pbt_bot.log`
- **Network:** `nethogs`

## 🚨 Common Issues

1. **Display Issues:** Use `export DISPLAY=:99`
2. **Performance:** Run `./optimize_wsl.sh`
3. **Memory:** Increase WSL memory in `.wslconfig`
4. **Network:** Restart WSL with `wsl --shutdown`

## 🎯 WSL Advantages

- ✅ **Better Performance** than Windows
- ✅ **Linux Tools** available
- ✅ **Multi-bot Support** (1-100+ instances)
- ✅ **Headless Operation** optimized
- ✅ **Docker Support** native
- ✅ **Easy Scaling** horizontal/vertical

Happy botting in WSL! 🎮
EOF

print_header "WSL Quick Setup Complete! 🎉"
echo
echo "📁 PBT Bot installed at: $PBT_DIR"
echo "🚀 Quick start: ./quick_start_wsl.sh"
echo "🔧 Optimize: ./optimize_wsl.sh"
echo "🔍 Troubleshoot: ./troubleshoot_wsl.sh"
echo
echo "📖 Read: cat README_WSL_QUICK.md"
echo "📋 Read: cat WSL_CONFIG_INSTRUCTIONS.txt"
echo
echo "🔄 Restart WSL for best performance:"
echo "   wsl --shutdown"
echo "   wsl"
echo
echo "✅ WSL quick setup completed successfully!" 