# 🐧 PBT Bot - WSL (Windows Subsystem for Linux) Guide

## 🎮 Complete PBT Bot Setup for Ubuntu 22.04 in WSL

**By Taquito Loco** 🎯

---

## 📋 Table of Contents

1. [Prerequisites](#prerequisites)
2. [WSL Installation](#wsl-installation)
3. [PBT Bot Installation](#pbt-bot-installation)
4. [Quick Start](#quick-start)
5. [Multi-Bot Deployment](#multi-bot-deployment)
6. [Docker Alternative](#docker-alternative)
7. [Troubleshooting](#troubleshooting)
8. [Advanced Usage](#advanced-usage)

---

## 🔧 Prerequisites

### Windows Requirements
- Windows 10/11 (Build 19041 or higher)
- WSL2 enabled
- Docker Desktop (optional, for containerized deployment)

### WSL Requirements
- Ubuntu 22.04 LTS
- At least 4GB RAM
- 10GB free disk space

---

## 🚀 WSL Installation

### 1. Enable WSL2
```powershell
# Run as Administrator in PowerShell
dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart
dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart
```

### 2. Install Ubuntu 22.04
```powershell
# Install from Microsoft Store or use:
wsl --install -d Ubuntu-22.04
```

### 3. Set WSL2 as Default
```powershell
wsl --set-default-version 2
```

### 4. Update Ubuntu
```bash
sudo apt update && sudo apt upgrade -y
```

---

## 🤖 PBT Bot Installation

### 1. Clone Repository
```bash
git clone https://github.com/your-username/pbt-bot-complete.git
cd pbt-bot-complete
```

### 2. Run Installation Script
```bash
chmod +x install_ubuntu.sh
./install_ubuntu.sh
```

### 3. Test Installation
```bash
chmod +x test_wsl.sh
./test_wsl.sh
```

---

## ⚡ Quick Start

### 1. Start Virtual Desktop
```bash
./manage_desktop.sh start
```

### 2. Launch Single Bot
```bash
./start_bot.sh my_bot
```

### 3. Check Status
```bash
./status_bot.sh
```

### 4. Stop Bot
```bash
./stop_bot.sh my_bot
```

---

## 🚀 Multi-Bot Deployment

### Launch Multiple Bots
```bash
# Launch 5 bots with prefix "bot"
./launch_multiple_bots.sh 5 bot

# Launch 10 bots with prefix "warrior"
./launch_multiple_bots.sh 10 warrior
```

### Monitor All Bots
```bash
# Check status of all bots
./status_bot.sh

# View specific bot logs
screen -r pbt_bot_bot_1

# Stop all bots
./stop_bot.sh all
```

### Individual Bot Management
```bash
# Start specific bot
./start_bot.sh warrior_1

# Stop specific bot
./stop_bot.sh warrior_1

# View bot logs
screen -r pbt_bot_warrior_1
```

---

## 🐳 Docker Alternative

### 1. Build Docker Image
```bash
docker build -t pbt-bot .
```

### 2. Run Single Container
```bash
docker run -d --name pbt-single pbt-bot
```

### 3. Run Multiple Containers
```bash
docker-compose up -d
```

### 4. Monitor Containers
```bash
# Check container status
docker ps

# View logs
docker logs pbt-single

# Stop containers
docker-compose down
```

---

## 🔧 Configuration

### Bot Configuration Files
```
config/
├── bot_config.json          # Main configuration
├── bot_config_1.json        # Bot 1 configuration
├── bot_config_2.json        # Bot 2 configuration
└── ...
```

### Key Configuration Options
```json
{
  "bot_name": "my_bot",
  "headless_mode": true,
  "auto_attack": true,
  "auto_movement": true,
  "auto_loot": true,
  "spell_casting": true,
  "hotkeys": {
    "attack": "f1",
    "heal": "f2",
    "spell1": "f3",
    "spell2": "f4"
  }
}
```

---

## 🖥️ Remote Desktop Access

### 1. Setup VNC
```bash
./setup_vnc.sh
```

### 2. Start VNC Server
```bash
vncserver :1
```

### 3. Connect from Windows
```bash
# In WSL
export DISPLAY=localhost:0.0

# Install VNC client on Windows (TightVNC, RealVNC, etc.)
# Connect to localhost:5901
```

### 4. Alternative: X11 Forwarding
```bash
# Install VcXsrv on Windows
# In WSL
export DISPLAY=localhost:0.0
```

---

## 🚨 Troubleshooting

### Common Issues

#### 1. Display Issues
```bash
# Check if Xvfb is running
pgrep Xvfb

# Restart virtual desktop
./manage_desktop.sh restart

# Set display manually
export DISPLAY=:99
```

#### 2. Permission Issues
```bash
# Fix script permissions
chmod +x *.sh

# Fix directory permissions
chmod -R 755 .
```

#### 3. Python Package Issues
```bash
# Reinstall virtual environment
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements_linux.txt
```

#### 4. Memory Issues
```bash
# Check memory usage
free -h

# Kill unnecessary processes
pkill -f "python.*main.py"
```

#### 5. Network Issues
```bash
# Check network connectivity
ping 8.8.8.8

# Restart WSL
wsl --shutdown
wsl
```

### WSL-Specific Issues

#### 1. WSL Performance
```bash
# Create .wslconfig in Windows user directory
# C:\Users\YourUsername\.wslconfig
[wsl2]
memory=8GB
processors=4
swap=2GB
```

#### 2. File System Performance
```bash
# Access files from WSL, not Windows
# Use /home/username/ instead of /mnt/c/
```

#### 3. GUI Applications
```bash
# Install VcXsrv on Windows
# Set DISPLAY in WSL
export DISPLAY=localhost:0.0
```

---

## 📊 Monitoring & Logs

### View Logs
```bash
# Real-time logs
tail -f logs/pbt_bot.log

# Last 100 lines
tail -100 logs/pbt_bot.log

# Search logs
grep "ERROR" logs/pbt_bot.log
```

### System Monitoring
```bash
# Check system resources
htop

# Check disk usage
df -h

# Check memory usage
free -h
```

### Bot Monitoring
```bash
# List running bots
screen -ls

# Attach to bot session
screen -r pbt_bot_botname

# Detach from session (Ctrl+A, D)
```

---

## 🔄 Advanced Usage

### Custom Bot Configurations
```bash
# Create custom config for specific bot
cp config/bot_config.json config/bot_config_warrior.json

# Edit configuration
nano config/bot_config_warrior.json

# Launch with custom config
./start_bot.sh warrior config/bot_config_warrior.json
```

### Automated Startup
```bash
# Enable systemd service
sudo systemctl enable pbt-bot.service

# Start service
sudo systemctl start pbt-bot.service

# Check service status
sudo systemctl status pbt-bot.service
```

### Backup & Restore
```bash
# Backup configurations
tar -czf pbt_backup_$(date +%Y%m%d).tar.gz config/ logs/

# Restore configurations
tar -xzf pbt_backup_20231201.tar.gz
```

### Scaling Strategies
```bash
# Horizontal scaling (more bots)
./launch_multiple_bots.sh 20 bot

# Vertical scaling (more resources per bot)
# Edit config files to increase resource allocation

# Load balancing
# Use different configurations for different bot types
```

---

## 📈 Performance Optimization

### WSL Performance
1. **Memory Allocation**: Allocate 8GB+ RAM to WSL
2. **CPU Cores**: Allocate 4+ CPU cores
3. **File System**: Use WSL file system, not Windows
4. **Swap Space**: Configure appropriate swap

### Bot Performance
1. **Headless Mode**: Always use headless mode in WSL
2. **Resource Limits**: Set appropriate resource limits per bot
3. **Logging**: Use appropriate log levels
4. **Monitoring**: Regular health checks

---

## 🔐 Security Considerations

### WSL Security
1. **Updates**: Keep WSL and Ubuntu updated
2. **Firewall**: Configure Windows firewall appropriately
3. **Access Control**: Limit access to WSL environment
4. **Backups**: Regular backups of configurations

### Bot Security
1. **Credentials**: Never store credentials in plain text
2. **Network**: Use secure connections
3. **Logs**: Secure log files
4. **Updates**: Keep bot software updated

---

## 📞 Support

### Getting Help
1. **Check Logs**: Always check logs first
2. **Test Script**: Run `./test_wsl.sh` for diagnostics
3. **Documentation**: Check this README and other docs
4. **Community**: Check GitHub issues

### Useful Commands
```bash
# Quick health check
./test_wsl.sh

# System information
uname -a
lsb_release -a

# WSL information
cat /proc/version

# Resource usage
top
htop
```

---

## 🎯 Conclusion

This guide provides everything you need to run PBT Bot in WSL with Ubuntu 22.04. The setup is optimized for:

- ✅ **Multi-bot deployment** (1-100+ instances)
- ✅ **Headless operation** (no GUI required)
- ✅ **Remote management** (VNC, SSH)
- ✅ **Docker support** (containerized deployment)
- ✅ **WSL optimization** (performance tuned)
- ✅ **Easy scaling** (horizontal and vertical)

**Happy botting! 🎮**

---

*Last updated: December 2024*
*Compatible with: Ubuntu 22.04 LTS, WSL2, Windows 10/11* 