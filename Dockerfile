# PBT Bot - Docker Container
# By Taquito Loco 🎮

FROM ubuntu:22.04

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive
ENV DISPLAY=:99
ENV PYTHONUNBUFFERED=1

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
    && rm -rf /var/lib/apt/lists/*

# Create PBT user
RUN useradd -m -s /bin/bash pbtuser
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
RUN mkdir -p logs config

# Make scripts executable
RUN chmod +x install_ubuntu.sh start_bot.sh stop_bot.sh status_bot.sh launch_multiple_bots.sh setup_vnc.sh manage_desktop.sh

# Create startup script
RUN echo '#!/bin/bash\n\
echo "🤖 PBT Bot Docker Container Starting..."\n\
echo "========================================"\n\
\n\
# Start virtual display\n\
Xvfb :99 -screen 0 1024x768x24 &\n\
sleep 2\n\
\n\
# Start VNC server (optional)\n\
if [ "$ENABLE_VNC" = "true" ]; then\n\
    echo "🖥️ Starting VNC server..."\n\
    vncserver :1 -geometry 1024x768 -depth 24 &\n\
    sleep 2\n\
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
# Keep container running\n\
tail -f /dev/null\n\
' > /home/pbtuser/pbt_bot/start_container.sh

RUN chmod +x /home/pbtuser/pbt_bot/start_container.sh

# Expose VNC port
EXPOSE 5901

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD pgrep -f "python.*main.py" || exit 1

# Default command
CMD ["./start_container.sh"] 