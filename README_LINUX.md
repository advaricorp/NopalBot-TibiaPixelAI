# 🐧 PBT Bot - Ubuntu Server Edition

**Multi-Instance Bot System for Ubuntu Server with Remote Desktop Access**

By Taquito Loco 🎮

## 🚀 Quick Start

### Option 1: Direct Installation (Recommended)

```bash
# Clone or download the project
git clone <your-repo-url>
cd PBT

# Make installation script executable
chmod +x install_ubuntu.sh

# Run installation
./install_ubuntu.sh
```

### Option 2: Docker Deployment

```bash
# Build and run with Docker Compose
docker-compose up -d

# Or build single container
docker build -t pbt-bot .
docker run -d --name pbt-bot-1 pbt-bot
```

## 🎯 Features

### 🤖 Multi-Bot Support
- **Multiple Instances**: Run 1-100+ bot instances simultaneously
- **Individual Configs**: Each bot has its own configuration file
- **Screen Sessions**: Each bot runs in its own screen session
- **Independent Control**: Start/stop individual bots

### 🖥️ Remote Desktop Access
- **VNC Server**: Remote desktop access to bot instances
- **Virtual Display**: Headless operation with Xvfb
- **SSH Tunneling**: Secure remote access
- **Desktop Environment**: XFCE4 for GUI applications

### 📊 Monitoring & Management
- **Real-time Status**: Check bot status and system resources
- **Log Management**: Individual log files for each bot
- **Resource Monitoring**: CPU, memory, and disk usage
- **Health Checks**: Automatic bot health monitoring

### 🔧 Configuration Management
- **Profession Support**: Knight, Paladin, Sorcerer, Druid, Mage
- **Spell Management**: Profession-specific spells
- **Hotkey Configuration**: Customizable hotkeys
- **Feature Toggles**: Enable/disable specific features

## 📋 Prerequisites

### System Requirements
- **OS**: Ubuntu 20.04+ or Ubuntu Server 20.04+
- **RAM**: 2GB minimum (4GB+ recommended for multiple bots)
- **Storage**: 10GB+ free space
- **Network**: Internet connection for installation

### Software Requirements
- Python 3.8+
- Git
- Screen or Tmux
- Xvfb (for headless operation)
- VNC Server (for remote desktop)

## 🛠️ Installation

### 1. System Preparation

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install basic dependencies
sudo apt install -y python3 python3-pip python3-venv git screen tmux
```

### 2. Install PBT Bot

```bash
# Run installation script
./install_ubuntu.sh
```

The installation script will:
- Create PBT Bot directory at `~/pbt_bot`
- Set up Python virtual environment
- Install all dependencies
- Create management scripts
- Set up systemd service

### 3. Verify Installation

```bash
cd ~/pbt_bot
./status_bot.sh
```

## 🚀 Usage

### Single Bot Operation

```bash
# Start virtual desktop
./manage_desktop.sh start

# Start single bot
./start_bot.sh my_bot

# Check status
./status_bot.sh

# Stop bot
./stop_bot.sh my_bot
```

### Multiple Bot Operation

```bash
# Launch 5 bots
./launch_multiple_bots.sh 5 bot

# Launch 10 bots with custom prefix
./launch_multiple_bots.sh 10 farm

# Stop all bots
./stop_bot.sh all
```

### Remote Desktop Access

```bash
# Setup VNC
./setup_vnc.sh

# Start VNC server
vncserver :1

# From your desktop, create SSH tunnel
ssh -L 5901:localhost:5901 user@server_ip

# Connect VNC client to localhost:5901
```

## 📊 Monitoring

### Check Bot Status

```bash
# View all running bots
./status_bot.sh

# Check specific bot logs
tail -f logs/pbt_bot_bot1.log

# Monitor system resources
htop
```

### Screen Session Management

```bash
# List all screen sessions
screen -ls

# Attach to specific bot session
screen -r pbt_bot_bot1

# Detach from session (Ctrl+A, then D)
```

### Log Management

```bash
# View recent logs
tail -20 logs/pbt_bot_bot1.log

# Search logs
grep "ERROR" logs/pbt_bot_*.log

# Archive old logs
find logs/ -name "*.log" -mtime +7 -exec gzip {} \;
```

## 🔧 Configuration

### Individual Bot Configs

Each bot can have its own configuration file:

```bash
# Create config for bot 1
cp config/bot_config.json config/bot_config_1.json

# Edit config
nano config/bot_config_1.json

# Start bot with specific config
./start_bot.sh bot1 config/bot_config_1.json
```

### Configuration Options

```json
{
  "bot_settings": {
    "profession": "knight",
    "auto_attack": true,
    "auto_movement": true,
    "auto_loot": true,
    "spells_enabled": true,
    "emergency_spells": true
  },
  "hotkeys": {
    "attack": "space",
    "loot": "f4",
    "movement_up": "w",
    "movement_down": "s",
    "movement_left": "a",
    "movement_right": "d"
  }
}
```

## 🐳 Docker Deployment

### Single Container

```bash
# Build image
docker build -t pbt-bot .

# Run single bot
docker run -d --name pbt-bot-1 \
  -e BOT_NAME=bot1 \
  -e ENABLE_VNC=false \
  -v $(pwd)/config:/home/pbtuser/pbt_bot/config \
  -v $(pwd)/logs:/home/pbtuser/pbt_bot/logs \
  pbt-bot
```

### Multi-Container with Docker Compose

```bash
# Start all services
docker-compose up -d

# Scale to 10 bots
docker-compose up -d --scale pbt-bot-1=10

# View logs
docker-compose logs -f pbt-bot-1

# Stop all
docker-compose down
```

## 📈 Scaling

### Horizontal Scaling

```bash
# Launch 20 bots
./launch_multiple_bots.sh 20 farm

# Launch 50 bots across multiple servers
# (Copy project to multiple servers and run)
```

### Vertical Scaling

```bash
# Increase system resources
# - Add more RAM
# - Use SSD storage
# - Optimize CPU usage
```

### Load Balancing

```bash
# Distribute bots across multiple servers
# Use load balancer for VNC access
# Implement centralized logging
```

## 🔒 Security

### SSH Access

```bash
# Generate SSH key
ssh-keygen -t rsa -b 4096

# Copy to server
ssh-copy-id user@server_ip

# Disable password authentication
sudo nano /etc/ssh/sshd_config
# Set PasswordAuthentication no
```

### Firewall Configuration

```bash
# Allow SSH
sudo ufw allow ssh

# Allow VNC (if needed)
sudo ufw allow 5901

# Enable firewall
sudo ufw enable
```

## 🚨 Troubleshooting

### Common Issues

1. **Bot not starting**
   ```bash
   # Check logs
   tail -f logs/pbt_bot_bot1.log
   
   # Check virtual display
   ps aux | grep Xvfb
   
   # Restart virtual desktop
   ./manage_desktop.sh restart
   ```

2. **VNC not connecting**
   ```bash
   # Check VNC server
   ps aux | grep vnc
   
   # Restart VNC
   vncserver -kill :1
   vncserver :1
   ```

3. **High resource usage**
   ```bash
   # Check system resources
   htop
   
   # Kill specific bots
   screen -S pbt_bot_bot1 -X quit
   
   # Restart system
   sudo reboot
   ```

### Emergency Procedures

```bash
# Kill all bots
pkill -f "python.*main.py"

# Kill all screen sessions
pkill screen

# Emergency restart
sudo reboot
```

## 📚 Advanced Usage

### Custom Scripts

Create custom management scripts:

```bash
#!/bin/bash
# custom_bot_manager.sh

case "$1" in
    "start_all")
        ./launch_multiple_bots.sh 10 farm
        ;;
    "stop_all")
        ./stop_bot.sh all
        ;;
    "restart_all")
        ./stop_bot.sh all
        sleep 5
        ./launch_multiple_bots.sh 10 farm
        ;;
    *)
        echo "Usage: $0 {start_all|stop_all|restart_all}"
        ;;
esac
```

### Automation

Set up cron jobs for automatic management:

```bash
# Edit crontab
crontab -e

# Add entries
0 8 * * * cd ~/pbt_bot && ./launch_multiple_bots.sh 5 farm
0 20 * * * cd ~/pbt_bot && ./stop_bot.sh all
```

### Monitoring Dashboard

Create a simple monitoring dashboard:

```bash
#!/bin/bash
# monitor_dashboard.sh

echo "🤖 PBT Bot Dashboard"
echo "==================="
echo "⏰ $(date)"
echo

# Running bots
echo "🟢 Running Bots:"
screen -ls | grep "pbt_bot_" | wc -l

# System resources
echo "💻 System Resources:"
echo "CPU: $(top -bn1 | grep "Cpu(s)" | awk '{print $2}')"
echo "Memory: $(free -h | grep Mem | awk '{print $3"/"$2}')"

# Recent logs
echo "📋 Recent Activity:"
tail -3 logs/pbt_bot_*.log | head -10
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

- **Issues**: Create an issue on GitHub
- **Discussions**: Use GitHub Discussions
- **Documentation**: Check the docs/ directory

## 🎮 Happy Botting!

Remember to:
- ✅ Test configurations before scaling
- ✅ Monitor system resources
- ✅ Keep backups of configurations
- ✅ Update regularly
- ✅ Follow game terms of service

---

**By Taquito Loco 🎮** - *Making bot management easy and scalable!* 