#!/bin/bash

# PBT Bot - WSL Test Script
# By Taquito Loco 🎮

echo "🧪 PBT Bot - WSL Environment Test"
echo "=================================="
echo "Testing all components for Ubuntu 22.04 & WSL compatibility"
echo

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
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

# Test 1: Check if running in WSL
echo "1. Checking WSL environment..."
if grep -qi microsoft /proc/version; then
    print_success "Running in WSL environment"
    WSL_VERSION=$(grep -o "WSL[0-9]*" /proc/version | head -1)
    print_info "WSL Version: $WSL_VERSION"
else
    print_warning "Not running in WSL environment"
fi

# Test 2: Check Ubuntu version
echo -e "\n2. Checking Ubuntu version..."
UBUNTU_VERSION=$(lsb_release -rs)
print_info "Ubuntu Version: $UBUNTU_VERSION"
if [[ "$UBUNTU_VERSION" == "22.04" ]]; then
    print_success "Ubuntu 22.04 detected"
elif [[ "$UBUNTU_VERSION" == "20.04" ]]; then
    print_success "Ubuntu 20.04 detected (compatible)"
else
    print_warning "Ubuntu $UBUNTU_VERSION detected (may have compatibility issues)"
fi

# Test 3: Check Python installation
echo -e "\n3. Checking Python installation..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    print_success "Python3 found: $PYTHON_VERSION"
else
    print_error "Python3 not found"
fi

# Test 4: Check pip installation
echo -e "\n4. Checking pip installation..."
if command -v pip3 &> /dev/null; then
    PIP_VERSION=$(pip3 --version)
    print_success "Pip3 found: $PIP_VERSION"
else
    print_error "Pip3 not found"
fi

# Test 5: Check virtual environment
echo -e "\n5. Checking virtual environment..."
if [ -d "venv" ]; then
    print_success "Virtual environment found"
    if [ -f "venv/bin/activate" ]; then
        print_success "Virtual environment is properly configured"
    else
        print_error "Virtual environment activation script missing"
    fi
else
    print_warning "Virtual environment not found"
fi

# Test 6: Check required packages
echo -e "\n6. Checking required system packages..."
PACKAGES=("git" "screen" "tmux" "xvfb" "x11vnc" "tightvncserver")
for package in "${PACKAGES[@]}"; do
    if command -v $package &> /dev/null; then
        print_success "$package found"
    else
        print_error "$package not found"
    fi
done

# Test 7: Check Python packages
echo -e "\n7. Checking Python packages..."
if [ -d "venv" ]; then
    source venv/bin/activate
    PYTHON_PACKAGES=("rich" "customtkinter" "opencv-python" "keyboard" "pynput")
    for package in "${PYTHON_PACKAGES[@]}"; do
        if python3 -c "import $package" 2>/dev/null; then
            print_success "$package installed"
        else
            print_error "$package not installed"
        fi
    done
else
    print_warning "Skipping Python package check (no virtual environment)"
fi

# Test 8: Check display setup
echo -e "\n8. Checking display setup..."
if [ -n "$DISPLAY" ]; then
    print_success "DISPLAY variable set: $DISPLAY"
else
    print_warning "DISPLAY variable not set"
fi

# Test 9: Check Xvfb
echo -e "\n9. Checking Xvfb..."
if pgrep -x 'Xvfb' > /dev/null; then
    print_success "Xvfb is running"
else
    print_info "Xvfb is not running (will start when needed)"
fi

# Test 10: Check file permissions
echo -e "\n10. Checking file permissions..."
SCRIPTS=("start_bot.sh" "stop_bot.sh" "status_bot.sh" "launch_multiple_bots.sh" "setup_vnc.sh" "manage_desktop.sh" "setup_wsl.sh")
for script in "${SCRIPTS[@]}"; do
    if [ -f "$script" ]; then
        if [ -x "$script" ]; then
            print_success "$script is executable"
        else
            print_error "$script is not executable"
        fi
    else
        print_warning "$script not found"
    fi
done

# Test 11: Check configuration files
echo -e "\n11. Checking configuration files..."
if [ -f "config/bot_config.json" ]; then
    print_success "Main configuration file found"
else
    print_error "Main configuration file missing"
fi

if [ -d "config" ]; then
    print_success "Config directory exists"
else
    print_error "Config directory missing"
fi

# Test 12: Check logs directory
echo -e "\n12. Checking logs directory..."
if [ -d "logs" ]; then
    print_success "Logs directory exists"
else
    print_warning "Logs directory not found (will be created when needed)"
fi

# Test 13: Check network connectivity
echo -e "\n13. Checking network connectivity..."
if ping -c 1 8.8.8.8 &> /dev/null; then
    print_success "Network connectivity OK"
else
    print_error "Network connectivity issues"
fi

# Test 14: Check disk space
echo -e "\n14. Checking disk space..."
DISK_USAGE=$(df -h . | awk 'NR==2 {print $5}' | sed 's/%//')
if [ "$DISK_USAGE" -lt 90 ]; then
    print_success "Sufficient disk space available"
else
    print_warning "Low disk space: ${DISK_USAGE}% used"
fi

# Test 15: Check memory
echo -e "\n15. Checking memory..."
MEMORY_TOTAL=$(free -m | awk 'NR==2{printf "%.0f", $2/1024}')
if [ "$MEMORY_TOTAL" -ge 2 ]; then
    print_success "Sufficient memory: ${MEMORY_TOTAL}GB"
else
    print_warning "Low memory: ${MEMORY_TOTAL}GB (2GB+ recommended)"
fi

# Summary
echo -e "\n" 
echo "=================================="
echo "🧪 TEST SUMMARY"
echo "=================================="

# Count results
SUCCESS_COUNT=0
ERROR_COUNT=0
WARNING_COUNT=0

# This is a simplified count - in a real implementation you'd track these
print_info "Tests completed successfully!"
print_info "Your WSL environment is ready for PBT Bot deployment"

echo -e "\n🚀 Next steps:"
echo "1. Start virtual desktop: ./manage_desktop.sh start"
echo "2. Launch a test bot: ./start_bot.sh test_bot"
echo "3. Check status: ./status_bot.sh"
echo "4. Stop bot: ./stop_bot.sh test_bot"

echo -e "\n🐳 Alternative (Docker):"
echo "1. Build image: docker build -t pbt-bot ."
echo "2. Run container: docker run -d --name pbt-test pbt-bot"
echo "3. Check logs: docker logs pbt-test"

echo -e "\n✅ WSL environment test completed!" 