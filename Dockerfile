# PBT Bot - Docker Container for Ubuntu 22.04 & WSL
# By Taquito Loco 🎮

FROM ubuntu:22.04

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive
ENV DISPLAY=:99
ENV PYTHONUNBUFFERED=1
ENV TZ=UTC

# Install system dependencies
RUN apt-get update && apt-get install -y \
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
    xfce4 \
    xfce4-goodies \
    xfce4-terminal \
    firefox \
    curl \
    wget \
    nano \
    htop \
    net-tools \
    iputils-ping \
    openssh-client \
    && rm -rf /var/lib/apt/lists/*

# Create PBT user
RUN useradd -m -s /bin/bash pbtuser && \
    echo "pbtuser ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

USER pbtuser
WORKDIR /home/pbtuser

# Create PBT directory
RUN mkdir -p /home/pbtuser/pbt_bot
WORKDIR /home/pbtuser/pbt_bot

# Copy requirements first for better caching
COPY requirements_linux.txt .

# Create virtual environment
RUN python3 -m venv venv
ENV PATH="/home/pbtuser/pbt_bot/venv/bin:$PATH"

# Install Python dependencies
RUN pip install --upgrade pip && \
    pip install -r requirements_linux.txt

# Copy application files
COPY --chown=pbtuser:pbtuser . .

# Create necessary directories
RUN mkdir -p logs config data

# Make scripts executable
RUN chmod +x install_ubuntu.sh start_bot.sh stop_bot.sh status_bot.sh launch_multiple_bots.sh setup_vnc.sh manage_desktop.sh

# Create VNC startup script
RUN mkdir -p ~/.vnc && \
    echo '#!/bin/bash' > ~/.vnc/xstartup && \
    echo 'xrdb $HOME/.Xresources' >> ~/.vnc/xstartup && \
    echo 'startxfce4 &' >> ~/.vnc/xstartup && \
    chmod +x ~/.vnc/xstartup

# Create startup script
RUN echo '#!/bin/bash\n\
echo "🤖 PBT Bot Docker Container Starting..."\n\
echo "========================================"\n\
echo "🐧 Ubuntu 22.04 + WSL Compatible"\n\
echo "⏰ Started at: $(date)"\n\
echo\n\
\n\
# Start virtual display\n\
echo "🖥️ Starting virtual display..."\n\
Xvfb :99 -screen 0 1024x768x24 &\n\
sleep 3\n\
echo "✅ Virtual display started on :99"\n\
\n\
# Start VNC server (optional)\n\
if [ "$ENABLE_VNC" = "true" ]; then\n\
    echo "🖥️ Starting VNC server..."\n\
    vncserver :1 -geometry 1024x768 -depth 24 &\n\
    sleep 3\n\
    echo "✅ VNC server started on :1"\n\
fi\n\
\n\
# Start bot(s)\n\
if [ "$BOT_COUNT" -gt 1 ]; then\n\
    echo "🚀 Starting $BOT_COUNT bots..."\n\
    ./launch_multiple_bots.sh $BOT_COUNT $BOT_PREFIX\n\
else\n\
    echo "🚀 Starting single bot..."\n\
    ./start_bot.sh $BOT_NAME\n\
fi\n\
\n\
echo "✅ All services started successfully!"\n\
echo "📊 Check status: ./status_bot.sh"\n\
echo "🖥️ VNC access: localhost:5901"\n\
echo\n\
\n\
# Keep container running\n\
tail -f /dev/null\n\
' > /home/pbtuser/pbt_bot/start_container.sh

RUN chmod +x /home/pbtuser/pbt_bot/start_container.sh

# Create health check script
RUN echo '#!/bin/bash\n\
# Health check for PBT Bot\n\
if pgrep -f "python.*main.py" > /dev/null; then\n\
    echo "✅ Bot is running"\n\
    exit 0\n\
else\n\
    echo "❌ Bot is not running"\n\
    exit 1\n\
fi\n\
' > /home/pbtuser/pbt_bot/health_check.sh

RUN chmod +x /home/pbtuser/pbt_bot/health_check.sh

# Expose ports
EXPOSE 5901 8080

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD /home/pbtuser/pbt_bot/health_check.sh

# Default command
CMD ["./start_container.sh"] 