#!/bin/bash

# PBT Bot - Ubuntu Server Installation Script
# By Taquito Loco 🎮
# For running multiple bot instances on Ubuntu Server

set -e

echo "🤖 PBT Bot - Ubuntu Server Installation"
echo "========================================"
echo "Installing PBT Bot for headless operation..."
echo

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_header() {
    echo -e "${BLUE}[HEADER]${NC} $1"
}

# Check if running as root
if [[ $EUID -eq 0 ]]; then
   print_error "This script should not be run as root"
   exit 1
fi

# Update system
print_header "Updating system packages..."
sudo apt update && sudo apt upgrade -y

# Install required packages
print_header "Installing required packages..."
sudo apt install -y python3 python3-pip python3-venv git screen tmux xvfb x11vnc

# Install additional dependencies for GUI support (if needed)
sudo apt install -y python3-tk tk-dev

# Create PBT directory
PBT_DIR="$HOME/pbt_bot"
print_header "Creating PBT Bot directory at $PBT_DIR..."
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
pip install -r requirements.txt

# Install additional Linux-specific packages
pip install python-xlib pynput

# Create bot management scripts
print_header "Creating management scripts..."

# Create start script
cat > start_bot.sh << 'EOF'
#!/bin/bash

# PBT Bot Start Script for Ubuntu Server
# By Taquito Loco 🎮

BOT_DIR="$HOME/pbt_bot"
BOT_NAME="${1:-default}"
BOT_CONFIG="${2:-config/bot_config.json}"

cd "$BOT_DIR"

# Activate virtual environment
source venv/bin/activate

# Start bot in screen session
screen -dmS "pbt_bot_$BOT_NAME" bash -c "
    echo '🤖 Starting PBT Bot: $BOT_NAME'
    echo '📁 Config: $BOT_CONFIG'
    echo '⏰ Started at: $(date)'
    echo '========================================'
    
    # Set display for headless operation
    export DISPLAY=:99
    
    # Start Xvfb if not running
    if ! pgrep -x 'Xvfb' > /dev/null; then
        echo '🖥️ Starting virtual display...'
        Xvfb :99 -screen 0 1024x768x24 &
        sleep 2
    fi
    
    # Start bot
    python3 main.py --config $BOT_CONFIG --name $BOT_NAME
    
    echo '🛑 Bot stopped at: $(date)'
"

echo "✅ Bot '$BOT_NAME' started in screen session: pbt_bot_$BOT_NAME"
echo "📋 To view logs: screen -r pbt_bot_$BOT_NAME"
echo "🛑 To stop: screen -S pbt_bot_$BOT_NAME -X quit"
EOF

# Create stop script
cat > stop_bot.sh << 'EOF'
#!/bin/bash

# PBT Bot Stop Script for Ubuntu Server
# By Taquito Loco 🎮

BOT_NAME="${1:-all}"

if [ "$BOT_NAME" = "all" ]; then
    echo "🛑 Stopping all PBT bots..."
    screen -ls | grep "pbt_bot_" | cut -d. -f1 | xargs -I {} screen -S {} -X quit
    echo "✅ All bots stopped"
else
    echo "🛑 Stopping bot: $BOT_NAME"
    screen -S "pbt_bot_$BOT_NAME" -X quit
    echo "✅ Bot '$BOT_NAME' stopped"
fi
EOF

# Create status script
cat > status_bot.sh << 'EOF'
#!/bin/bash

# PBT Bot Status Script for Ubuntu Server
# By Taquito Loco 🎮

echo "🤖 PBT Bot Status Report"
echo "========================"
echo "⏰ Generated at: $(date)"
echo

# Check running bots
echo "🟢 Running Bots:"
screen -ls | grep "pbt_bot_" | while read line; do
    if [[ $line =~ pbt_bot_([a-zA-Z0-9_]+) ]]; then
        BOT_NAME="${BASH_REMATCH[1]}"
        echo "  • $BOT_NAME"
    fi
done

echo

# Check system resources
echo "💻 System Resources:"
echo "  • CPU Usage: $(top -bn1 | grep "Cpu(s)" | awk '{print $2}' | cut -d'%' -f1)%"
echo "  • Memory Usage: $(free | grep Mem | awk '{printf("%.1f%%", $3/$2 * 100.0)}')"
echo "  • Disk Usage: $(df -h / | awk 'NR==2 {print $5}')"

echo

# Check logs
echo "📋 Recent Logs:"
if [ -f "logs/pbt_bot.log" ]; then
    echo "  • Last 5 log entries:"
    tail -5 logs/pbt_bot.log | sed 's/^/    /'
else
    echo "  • No log file found"
fi
EOF

# Create multi-bot launcher
cat > launch_multiple_bots.sh << 'EOF'
#!/bin/bash

# PBT Bot Multi-Instance Launcher for Ubuntu Server
# By Taquito Loco 🎮

BOT_COUNT="${1:-3}"
BOT_PREFIX="${2:-bot}"

echo "🚀 Launching $BOT_COUNT PBT Bot instances..."
echo "📝 Bot prefix: $BOT_PREFIX"
echo

for i in $(seq 1 $BOT_COUNT); do
    BOT_NAME="${BOT_PREFIX}_$i"
    CONFIG_FILE="config/bot_config_$i.json"
    
    # Create individual config if it doesn't exist
    if [ ! -f "$CONFIG_FILE" ]; then
        cp config/bot_config.json "$CONFIG_FILE"
        echo "📄 Created config: $CONFIG_FILE"
    fi
    
    echo "🤖 Starting bot $i/$BOT_COUNT: $BOT_NAME"
    ./start_bot.sh "$BOT_NAME" "$CONFIG_FILE"
    sleep 2
done

echo
echo "✅ All $BOT_COUNT bots launched!"
echo "📋 Check status with: ./status_bot.sh"
echo "🛑 Stop all with: ./stop_bot.sh all"
EOF

# Create VNC setup script
cat > setup_vnc.sh << 'EOF'
#!/bin/bash

# VNC Setup Script for Remote Desktop Access
# By Taquito Loco 🎮

echo "🖥️ Setting up VNC for remote desktop access..."

# Install VNC server
sudo apt install -y tightvncserver

# Create VNC password
echo "🔐 Setting up VNC password..."
vncpasswd

# Create VNC startup script
cat > ~/.vnc/xstartup << 'VNCSTARTUP'
#!/bin/bash
xrdb $HOME/.Xresources
startxfce4 &
VNCSTARTUP

chmod +x ~/.vnc/xstartup

echo "✅ VNC setup complete!"
echo "🚀 Start VNC server: vncserver :1"
echo "📱 Connect from desktop: ssh -L 5901:localhost:5901 user@server_ip"
echo "🖥️ Then connect VNC client to localhost:5901"
EOF

# Make scripts executable
chmod +x start_bot.sh stop_bot.sh status_bot.sh launch_multiple_bots.sh setup_vnc.sh

# Create systemd service for auto-start
print_header "Creating systemd service for auto-start..."

sudo tee /etc/systemd/system/pbt-bot.service > /dev/null << EOF
[Unit]
Description=PBT Bot Service
After=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=$PBT_DIR
ExecStart=$PBT_DIR/venv/bin/python $PBT_DIR/main.py
Restart=always
RestartSec=10
Environment=DISPLAY=:99

[Install]
WantedBy=multi-user.target
EOF

# Create desktop management script
cat > manage_desktop.sh << 'EOF'
#!/bin/bash

# Desktop Management Script for Ubuntu Server
# By Taquito Loco 🎮

case "$1" in
    "start")
        echo "🖥️ Starting virtual desktop..."
        Xvfb :99 -screen 0 1024x768x24 &
        sleep 2
        echo "✅ Virtual desktop started on :99"
        ;;
    "stop")
        echo "🛑 Stopping virtual desktop..."
        pkill Xvfb
        echo "✅ Virtual desktop stopped"
        ;;
    "restart")
        echo "🔄 Restarting virtual desktop..."
        pkill Xvfb
        sleep 2
        Xvfb :99 -screen 0 1024x768x24 &
        echo "✅ Virtual desktop restarted"
        ;;
    *)
        echo "Usage: $0 {start|stop|restart}"
        exit 1
        ;;
esac
EOF

chmod +x manage_desktop.sh

# Create quick start guide
cat > QUICK_START_UBUNTU.md << 'EOF'
# 🐧 PBT Bot - Ubuntu Server Quick Start Guide

## 🚀 Quick Start

1. **Start virtual desktop:**
   ```bash
   ./manage_desktop.sh start
   ```

2. **Launch single bot:**
   ```bash
   ./start_bot.sh my_bot
   ```

3. **Launch multiple bots:**
   ```bash
   ./launch_multiple_bots.sh 5 bot
   ```

4. **Check status:**
   ```bash
   ./status_bot.sh
   ```

5. **Stop bots:**
   ```bash
   ./stop_bot.sh all
   ```

## 🖥️ Remote Desktop Access

1. **Setup VNC:**
   ```bash
   ./setup_vnc.sh
   ```

2. **Start VNC server:**
   ```bash
   vncserver :1
   ```

3. **Connect from desktop:**
   ```bash
   ssh -L 5901:localhost:5901 user@server_ip
   ```

4. **Use VNC client to connect to localhost:5901**

## 📊 Monitoring

- **View bot logs:** `tail -f logs/pbt_bot.log`
- **Check screen sessions:** `screen -ls`
- **Attach to bot session:** `screen -r pbt_bot_botname`
- **System resources:** `htop`

## 🔧 Configuration

- **Individual bot configs:** `config/bot_config_1.json`, `config/bot_config_2.json`, etc.
- **Main config:** `config/bot_config.json`
- **Logs:** `logs/` directory

## 🚨 Emergency

- **Kill all bots:** `pkill -f "python.*main.py"`
- **Kill all screens:** `pkill screen`
- **Restart system:** `sudo reboot`

## 📈 Scaling

To run more bots, simply increase the number in `launch_multiple_bots.sh`:
```bash
./launch_multiple_bots.sh 10 bot  # Launch 10 bots
```

Each bot runs in its own screen session and can be managed independently.
EOF

print_header "Installation Complete! 🎉"
echo
echo "📁 PBT Bot installed at: $PBT_DIR"
echo "🚀 Quick start: cd $PBT_DIR && ./start_bot.sh my_bot"
echo "📖 Read: cat QUICK_START_UBUNTU.md"
echo
echo "🖥️ For remote desktop access:"
echo "   ./setup_vnc.sh"
echo "   vncserver :1"
echo
echo "📊 For multiple bots:"
echo "   ./launch_multiple_bots.sh 5 bot"
echo
echo "✅ Installation completed successfully!" 