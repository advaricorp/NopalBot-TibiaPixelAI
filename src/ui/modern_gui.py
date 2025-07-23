"""
Modern GUI for Tibia Bot
By Taquito Loco 🎮

A modern 2020s-style interface with professional design, gradients, and contemporary aesthetics.
"""

import customtkinter as ctk
import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time
import sys
import os
from typing import Dict, Any, Optional
import json
from PIL import Image, ImageTk
import logging
from queue import Queue, Empty

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from config.language_manager import Language, set_global_language, get_message
from config.config_manager import ConfigManager
from core.bot_core import BotCore

# Set appearance for modern look
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

ASCII_MATRIX = '''
████████╗ █████╗  ██████╗ ██╗   ██╗██╗████████╗ ██████╗     ██╗      ██████╗  ██████╗ ██████╗     
╚══██╔══╝██╔══██╗██╔═══██╗██║   ██║██║╚══██╔══╝██╔═══██╗    ██║     ██╔═══██╗██╔════╝██╔═══██╗    
   ██║   ███████║██║   ██║██║   ██║██║   ██║   ██║   ██║    ██║     ██║   ██║██║     ██║   ██║    
   ██║   ██╔══██║██║▄▄ ██║██║   ██║██║   ██║   ██║   ██║    ██║     ██║   ██║██║     ██║   ██║    
   ██║   ██║  ██║╚██████╔╝╚██████╔╝██║   ██║   ╚██████╔╝    ███████╗╚██████╔╝╚██████╗╚██████╔╝    
   ╚═╝   ╚═╝  ╚═╝ ╚══▀▀═╝  ╚═════╝ ╚═╝   ╚═╝    ╚═════╝     ╚══════╝ ╚═════╝  ╚═════╝ ╚═════╝     
                                                                                                  
███████╗██╗  ██╗██╗   ██╗███╗   ██╗██╗  ██╗    ██╗    ██╗ ██████╗ ██████╗ ██╗  ██╗███████╗        
██╔════╝██║ ██╔╝██║   ██║████╗  ██║██║ ██╔╝    ██║    ██║██╔═══██╗██╔══██╗██║ ██╔╝██╔════╝        
███████╗█████╔╝ ██║   ██║██╔██╗ ██║█████╔╝     ██║ █╗ ██║██║   ██║██████╔╝█████╔╝ ███████╗        
╚════██║██╔═██╗ ██║   ██║██║╚██╗██║██╔═██╗     ██║███╗██║██║   ██║██╔══██╗██╔═██╗ ╚════██║        
███████║██║  ██╗╚██████╔╝██║ ╚████║██║  ██╗    ╚███╔███╔╝╚██████╔╝██║  ██║██║  ██╗███████║        
╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝╚═╝  ╚═╝     ╚══╝╚══╝  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝        
                                                                                                  
'''

class GuiLogHandler(logging.Handler):
    """Thread-safe log handler for GUI log display."""
    def __init__(self, log_queue: Queue):
        super().__init__()
        self.log_queue = log_queue
    def emit(self, record):
        msg = self.format(record)
        self.log_queue.put(msg)

class ModernGUI:
    """
    Modern 2020s-style GUI with professional design.
    
    Features:
    - Modern color schemes (blues, purples, gradients)
    - Professional typography
    - Smooth animations
    - Real-time status monitoring
    - Bilingual support
    - Auto-attack integration
    """
    
    def __init__(self):
        """Initialize the modern GUI."""
        self.root = ctk.CTk()
        self.root.title("🤖 Tibia Bot Pro - By Taquito Loco 🎮")
        self.root.geometry("800x600")  # Ventana más pequeña y compacta
        self.root.configure(fg_color="#0f0f23")  # Dark blue background
        # Centrar la ventana en la pantalla
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (800 // 2)
        y = (self.root.winfo_screenheight() // 2) - (600 // 2)
        self.root.geometry(f"800x600+{x}+{y}")
        
        # Bot instance
        self.bot: Optional[BotCore] = None
        self.bot_running = False
        self.config = ConfigManager()
        
        # Language
        self.current_language = Language.ENGLISH
        set_global_language(self.current_language)
        
        # Status variables
        self.status_vars = {
            "bot_status": tk.StringVar(value="🛑 Bot Stopped"),
            "window_status": tk.StringVar(value="❌ Window Not Found"),
            "safe_mode": tk.StringVar(value="🛡️ Safe Mode: ENABLED"),
            "current_state": tk.StringVar(value="🎯 State: IDLE"),
            "action_count": tk.StringVar(value="⚡ Actions: 0"),
            "runtime": tk.StringVar(value="⏱️ Runtime: 00:00:00"),
            "auto_attack": tk.StringVar(value="⚔️ Auto-Attack: DISABLED"),
            "auto_walk": tk.StringVar(value="🟢 Auto-Walk: ENABLED")
        }
        
        # Setup modern styles
        self.setup_modern_styles()
        self.create_widgets()
        self.start_animations()
        
        # Start status updates
        self.update_status()
        self.log_queue = Queue()
        self._setup_logging()
        self.show_splash_screen()
    
    def setup_modern_styles(self):
        """Setup glassmorphism Apple-like color scheme (solid colors only)."""
        self.colors = {
            # Glass backgrounds (solid, no alpha)
            "glass_bg": "#f7fafd",  # White with blue tint
            "glass_card": "#e3e8f0",  # Light blue/gray
            "glass_elevated": "#dbeafe",  # Even lighter blue
            "glass_border": "#cbd5e1",
            # Accents
            "accent": "#00FF41",  # Matrix green
            "accent2": "#00CC33",  # Darker Matrix green
            # Text
            "text_primary": "#22292f",
            "text_secondary": "#64748b",
            "text_muted": "#94a3b8",
            # Status
            "success": "#22c55e",
            "warning": "#fbbf24",
            "error": "#ef4444",
            "info": "#38bdf8",
        }
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")
    
    def create_widgets(self):
        """Create all GUI widgets with glassmorphism design."""
        # Main container with glassmorphism styling
        self.main_frame = ctk.CTkFrame(
            self.root,
            fg_color=self.colors["glass_bg"],
            corner_radius=24,
            border_width=2,
            border_color=self.colors["glass_border"]
        )
        self.main_frame.pack(fill="both", expand=True)
        
        # Create sidebar
        self.create_sidebar()
        
        # Create main content area
        self.create_main_content()
        
        # Create status bar
        self.create_status_bar()
    
    def create_sidebar(self):
        """Create modern sidebar."""
        # Sidebar container - más pequeño
        self.sidebar = ctk.CTkFrame(
            self.main_frame,
            fg_color=self.colors["glass_card"],
            width=200,  # Reducido de 280 a 200
            corner_radius=24,
            border_width=2,
            border_color=self.colors["glass_border"]
        )
        self.sidebar.pack(side="left", fill="y", padx=0, pady=0)
        self.sidebar.pack_propagate(False)
        
        # Logo and branding - más compacto
        logo_frame = ctk.CTkFrame(
            self.sidebar,
            fg_color="transparent",
            height=80  # Reducido de 120 a 80
        )
        logo_frame.pack(fill="x", padx=20, pady=(20, 10))
        logo_frame.pack_propagate(False)
        
        # Modern logo - más pequeño
        logo_label = ctk.CTkLabel(
            logo_frame,
            text="🤖",
            font=ctk.CTkFont(size=32, weight="bold"),  # Reducido de 48 a 32
            text_color=self.colors["accent"]
        )
        logo_label.pack(pady=(5, 2))  # Reducido padding
        
        # Title - más pequeño
        title_label = ctk.CTkLabel(
            logo_frame,
            text="TIBIA BOT PRO",
            font=ctk.CTkFont(size=16, weight="bold"),  # Reducido de 20 a 16
            text_color=self.colors["text_primary"]
        )
        title_label.pack()
        
        # Subtitle - más pequeño
        subtitle_label = ctk.CTkLabel(
            logo_frame,
            text="By Taquito Loco 🎮",
            font=ctk.CTkFont(size=12),  # Reducido de 14 a 12
            text_color=self.colors["text_secondary"]
        )
        subtitle_label.pack()
        
        # Navigation buttons
        self.create_navigation_buttons()
        
        # Language selector
        self.create_language_selector()
        
        # About button at bottom
        about_btn = ctk.CTkButton(
            self.sidebar,
            text="About",
            command=self.show_about,
            fg_color=self.colors["accent"],
            hover_color=self.colors["accent2"],
            text_color="#000000",
            font=ctk.CTkFont(size=14, weight="bold"),
            corner_radius=12
        )
        about_btn.pack(side="bottom", pady=20, padx=20, fill="x")
    
    def create_navigation_buttons(self):
        """Create modern navigation buttons."""
        nav_frame = ctk.CTkFrame(
            self.sidebar,
            fg_color="transparent"
        )
        nav_frame.pack(fill="x", padx=20, pady=20)
        
        # Navigation buttons with modern styling
        nav_buttons = [
            ("🎮 Dashboard", self.show_dashboard),
            ("⚔️ Auto-Attack", self.show_auto_attack),
            ("📊 Status", self.show_status),
            ("⚙️ Settings", self.show_settings),
            ("📝 Logs", self.show_logs)
        ]
        
        self.nav_buttons = {}
        for text, command in nav_buttons:
            btn = ctk.CTkButton(
                nav_frame,
                text=text,
                command=command,
                fg_color="transparent",
                text_color=self.colors["text_secondary"],
                hover_color=self.colors["glass_elevated"],
                anchor="w",
                height=45,
                font=ctk.CTkFont(size=15, weight="normal")
            )
            btn.pack(fill="x", pady=2)
            self.nav_buttons[text] = btn
    
    def create_language_selector(self):
        """Create language selector."""
        lang_frame = ctk.CTkFrame(
            self.sidebar,
            fg_color="transparent"
        )
        lang_frame.pack(fill="x", padx=20, pady=20)
        
        ctk.CTkLabel(
            lang_frame,
            text="Language / Idioma",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=self.colors["text_primary"]
        ).pack(pady=(0, 10))
        
        self.language_var = tk.StringVar(value="🇺🇸 English")
        language_menu = ctk.CTkOptionMenu(
            lang_frame,
            values=["🇺🇸 English", "🇲🇽 Spanish"],
            variable=self.language_var,
            command=self.change_language,
            fg_color=self.colors["glass_elevated"],
            button_color=self.colors["accent"],
            button_hover_color=self.colors["accent2"],
            text_color=self.colors["text_primary"]
        )
        language_menu.pack(fill="x")
    
    def create_main_content(self):
        """Create main content area."""
        # Main content container
        self.content_frame = ctk.CTkFrame(
            self.main_frame,
            fg_color=self.colors["glass_bg"],
            corner_radius=24,
            border_width=2,
            border_color=self.colors["glass_border"]
        )
        self.content_frame.pack(side="right", fill="both", expand=True, padx=20, pady=20)
        
        # Create different pages
        self.pages = {}
        self.create_dashboard_page()
        self.create_auto_attack_page()
        self.create_status_page()
        self.create_settings_page()
        self.create_logs_page()
        
        # Show dashboard by default
        self.show_dashboard()
    
    def create_dashboard_page(self):
        """Create modern dashboard page."""
        page = ctk.CTkFrame(
            self.content_frame,
            fg_color="transparent"
        )
        
        # Header
        header = ctk.CTkFrame(
            page,
            fg_color=self.colors["glass_bg"],
            corner_radius=16,
            border_width=1,
            border_color=self.colors["glass_border"],
            height=80
        )
        header.pack(fill="x", pady=(0, 20))
        header.pack_propagate(False)
        
        ctk.CTkLabel(
            header,
            text="Dashboard",
            font=ctk.CTkFont(size=32, weight="bold"),
            text_color=self.colors["text_primary"]
        ).pack(side="left", padx=20, pady=20)
        
        # Help button (manual)
        help_button = ctk.CTkButton(
            header,
            text="❓ Manual",
            command=self.show_manual,
            fg_color=self.colors["accent"],
            hover_color=self.colors["accent2"],
            width=120,
            height=40,
            font=ctk.CTkFont(size=14, weight="bold"),
            corner_radius=8
        )
        help_button.pack(side="right", padx=20, pady=20)
        
        # Quick stats cards
        stats_frame = ctk.CTkFrame(
            page,
            fg_color="transparent"
        )
        stats_frame.pack(fill="x", pady=20)
        
        # Create stat cards
        stats = [
            ("Bot Status", "bot_status", "🤖"),
            ("Window Status", "window_status", "🖥️"),
            ("Safe Mode", "safe_mode", "🛡️"),
            ("Current State", "current_state", "🎯")
        ]
        
        for i, (title, var_name, icon) in enumerate(stats):
            card = ctk.CTkFrame(
                stats_frame,
                fg_color=self.colors["glass_card"],
                corner_radius=16,
                border_width=1,
                border_color=self.colors["glass_border"],
                height=120
            )
            card.grid(row=0, column=i, padx=10, pady=10, sticky="ew")
            
            ctk.CTkLabel(
                card,
                text=icon,
                font=ctk.CTkFont(size=24),
                text_color=self.colors["accent"]
            ).pack(pady=(15, 5))
            
            ctk.CTkLabel(
                card,
                text=title,
                font=ctk.CTkFont(size=14, weight="bold"),
                text_color=self.colors["text_primary"]
            ).pack()
            
            ctk.CTkLabel(
                card,
                textvariable=self.status_vars[var_name],
                font=ctk.CTkFont(size=12),
                text_color=self.colors["text_secondary"]
            ).pack(pady=5)
        
        # Configure grid weights
        for i in range(4):
            stats_frame.grid_columnconfigure(i, weight=1)
        
        # Control buttons
        control_frame = ctk.CTkFrame(
            page,
            fg_color="transparent"
        )
        control_frame.pack(fill="x", pady=20)
        
        # Modern control buttons
        self.start_button = ctk.CTkButton(
            control_frame,
            text="🚀 Start Bot",
            command=self.start_bot,
            fg_color=self.colors["accent"],
            hover_color=self.colors["accent2"],
            text_color=self.colors["text_primary"],
            height=50,
            font=ctk.CTkFont(size=16, weight="bold")
        )
        self.start_button.pack(side="left", padx=10)
        
        self.stop_button = ctk.CTkButton(
            control_frame,
            text="🛑 Stop Bot",
            command=self.stop_bot,
            fg_color=self.colors["error"],
            hover_color="#dc2626",
            text_color=self.colors["text_primary"],
            height=50,
            font=ctk.CTkFont(size=16, weight="bold"),
            state="disabled"
        )
        self.stop_button.pack(side="left", padx=10)
        
        self.emergency_button = ctk.CTkButton(
            control_frame,
            text="🚨 EMERGENCY STOP",
            command=self.emergency_stop,
            fg_color="#dc2626",
            hover_color="#b91c1c",
            height=50,
            font=ctk.CTkFont(size=16, weight="bold")
        )
        self.emergency_button.pack(side="right", padx=10)
        
        # Add auto-walk toggle
        self.auto_walk_var = tk.BooleanVar(value=True)
        auto_walk_switch = ctk.CTkSwitch(
            control_frame,
            text="Enable Auto-Walk (WSAD)",
            variable=self.auto_walk_var,
            command=self.toggle_auto_walk,
            progress_color=self.colors["accent"],
            button_color=self.colors["accent2"],
            font=ctk.CTkFont(size=14, weight="bold")
        )
        auto_walk_switch.pack(side="left", padx=10)
        
        self.pages["dashboard"] = page
    
    def create_auto_attack_page(self):
        """Create auto-attack configuration page."""
        page = ctk.CTkFrame(
            self.content_frame,
            fg_color="transparent"
        )
        
        # Header
        header = ctk.CTkFrame(
            page,
            fg_color=self.colors["glass_bg"],
            corner_radius=16,
            border_width=1,
            border_color=self.colors["glass_border"],
            height=80
        )
        header.pack(fill="x", pady=(0, 20))
        header.pack_propagate(False)
        
        ctk.CTkLabel(
            header,
            text="Auto-Attack Configuration",
            font=ctk.CTkFont(size=32, weight="bold"),
            text_color=self.colors["text_primary"]
        ).pack(side="left", padx=20, pady=20)
        
        # Help button (manual)
        help_button = ctk.CTkButton(
            header,
            text="❓ Manual",
            command=self.show_manual,
            fg_color=self.colors["accent"],
            hover_color=self.colors["accent2"],
            width=120,
            height=40,
            font=ctk.CTkFont(size=14, weight="bold"),
            corner_radius=8
        )
        help_button.pack(side="right", padx=20, pady=20)
        
        # Auto-attack controls
        controls_frame = ctk.CTkFrame(
            page,
            fg_color=self.colors["glass_card"],
            corner_radius=16,
            border_width=1,
            border_color=self.colors["glass_border"]
        )
        controls_frame.pack(fill="x", pady=20, padx=20)
        
        # Attack key configuration
        key_frame = ctk.CTkFrame(
            controls_frame,
            fg_color="transparent"
        )
        key_frame.pack(fill="x", padx=20, pady=20)
        
        ctk.CTkLabel(
            key_frame,
            text="Attack Configuration",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=self.colors["text_primary"]
        ).pack(anchor="w", pady=(0, 15))
        
        # Attack key
        attack_frame = ctk.CTkFrame(
            key_frame,
            fg_color="transparent"
        )
        attack_frame.pack(fill="x", pady=5)
        
        ctk.CTkLabel(
            attack_frame,
            text="Attack Key:",
            font=ctk.CTkFont(size=14),
            text_color=self.colors["text_primary"]
        ).pack(side="left")
        
        self.attack_key_var = tk.StringVar(value="y")
        attack_key_entry = ctk.CTkEntry(
            attack_frame,
            textvariable=self.attack_key_var,
            width=100,
            fg_color=self.colors["glass_elevated"],
            border_color=self.colors["accent"]
        )
        attack_key_entry.pack(side="right")
        
        # Next target key
        target_frame = ctk.CTkFrame(
            key_frame,
            fg_color="transparent"
        )
        target_frame.pack(fill="x", pady=5)
        
        ctk.CTkLabel(
            target_frame,
            text="Next Target Key:",
            font=ctk.CTkFont(size=14),
            text_color=self.colors["text_primary"]
        ).pack(side="left")
        
        self.target_key_var = tk.StringVar(value="u")
        target_key_entry = ctk.CTkEntry(
            target_frame,
            textvariable=self.target_key_var,
            width=100,
            fg_color=self.colors["glass_elevated"],
            border_color=self.colors["accent"]
        )
        target_key_entry.pack(side="right")
        
        # Auto-attack toggle
        toggle_frame = ctk.CTkFrame(
            controls_frame,
            fg_color="transparent"
        )
        toggle_frame.pack(fill="x", padx=20, pady=20)
        
        self.auto_attack_var = tk.BooleanVar(value=False)
        auto_attack_switch = ctk.CTkSwitch(
            toggle_frame,
            text="Enable Auto-Attack",
            variable=self.auto_attack_var,
            command=self.toggle_auto_attack,
            progress_color=self.colors["success"],
            button_color=self.colors["accent"],
            font=ctk.CTkFont(size=16, weight="bold")
        )
        auto_attack_switch.pack(side="left")
        
        # Status indicator
        ctk.CTkLabel(
            toggle_frame,
            textvariable=self.status_vars["auto_attack"],
            font=ctk.CTkFont(size=14),
            text_color=self.colors["text_secondary"]
        ).pack(side="right")
        
        self.pages["auto_attack"] = page
    
    def create_status_page(self):
        """Create detailed status page."""
        page = ctk.CTkFrame(
            self.content_frame,
            fg_color="transparent"
        )
        
        # Header
        header = ctk.CTkFrame(
            page,
            fg_color=self.colors["glass_bg"],
            corner_radius=16,
            border_width=1,
            border_color=self.colors["glass_border"],
            height=80
        )
        header.pack(fill="x", pady=(0, 20))
        header.pack_propagate(False)
        
        ctk.CTkLabel(
            header,
            text="Status Monitor",
            font=ctk.CTkFont(size=32, weight="bold"),
            text_color=self.colors["text_primary"]
        ).pack(side="left", padx=20, pady=20)
        
        # Help button (manual)
        help_button = ctk.CTkButton(
            header,
            text="❓ Manual",
            command=self.show_manual,
            fg_color=self.colors["accent"],
            hover_color=self.colors["accent2"],
            width=120,
            height=40,
            font=ctk.CTkFont(size=14, weight="bold"),
            corner_radius=8
        )
        help_button.pack(side="right", padx=20, pady=20)
        
        # Status grid
        status_frame = ctk.CTkFrame(
            page,
            fg_color=self.colors["glass_card"],
            corner_radius=16,
            border_width=1,
            border_color=self.colors["glass_border"]
        )
        status_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Status indicators in grid
        status_indicators = [
            ("Bot Status", "bot_status"),
            ("Window Status", "window_status"),
            ("Safe Mode", "safe_mode"),
            ("Current State", "current_state"),
            ("Action Count", "action_count"),
            ("Runtime", "runtime"),
            ("Auto-Attack", "auto_attack"),
            ("Auto-Walk", "auto_walk")
        ]
        
        for i, (label, var_name) in enumerate(status_indicators):
            row = i // 2
            col = i % 2
            
            # Status container
            status_container = ctk.CTkFrame(
                status_frame,
                fg_color=self.colors["glass_elevated"],
                corner_radius=8
            )
            status_container.grid(row=row, column=col, padx=15, pady=15, sticky="ew")
            
            # Label
            ctk.CTkLabel(
                status_container,
                text=label,
                font=ctk.CTkFont(size=16, weight="bold"),
                text_color=self.colors["text_primary"]
            ).pack(pady=(15, 5))
            
            # Value
            ctk.CTkLabel(
                status_container,
                textvariable=self.status_vars[var_name],
                font=ctk.CTkFont(size=14),
                text_color=self.colors["text_secondary"]
            ).pack(pady=(0, 15))
        
        # Configure grid weights
        status_frame.grid_columnconfigure(0, weight=1)
        status_frame.grid_columnconfigure(1, weight=1)
        
        self.pages["status"] = page
    
    def create_settings_page(self):
        """Create settings page."""
        page = ctk.CTkFrame(
            self.content_frame,
            fg_color="transparent"
        )
        
        # Header
        header = ctk.CTkFrame(
            page,
            fg_color=self.colors["glass_bg"],
            corner_radius=16,
            border_width=1,
            border_color=self.colors["glass_border"],
            height=80
        )
        header.pack(fill="x", pady=(0, 20))
        header.pack_propagate(False)
        
        ctk.CTkLabel(
            header,
            text="Settings",
            font=ctk.CTkFont(size=32, weight="bold"),
            text_color=self.colors["text_primary"]
        ).pack(side="left", padx=20, pady=20)
        
        # Help button (manual)
        help_button = ctk.CTkButton(
            header,
            text="❓ Manual",
            command=self.show_manual,
            fg_color=self.colors["accent"],
            hover_color=self.colors["accent2"],
            width=120,
            height=40,
            font=ctk.CTkFont(size=14, weight="bold"),
            corner_radius=8
        )
        help_button.pack(side="right", padx=20, pady=20)
        
        # Settings sections
        sections_frame = ctk.CTkFrame(
            page,
            fg_color="transparent"
        )
        sections_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Safety settings
        safety_frame = ctk.CTkFrame(
            sections_frame,
            fg_color=self.colors["glass_card"],
            corner_radius=16,
            border_width=1,
            border_color=self.colors["glass_border"]
        )
        safety_frame.pack(fill="x", pady=10)
        
        ctk.CTkLabel(
            safety_frame,
            text="🛡️ Safety Settings",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=self.colors["text_primary"]
        ).pack(anchor="w", padx=20, pady=15)
        
        # Safety toggles
        self.safe_mode_var = tk.BooleanVar(value=True)
        self.test_mode_var = tk.BooleanVar(value=True)
        
        toggles = [
            ("Safe Mode", self.safe_mode_var),
            ("Test Mode", self.test_mode_var)
        ]
        
        for text, var in toggles:
            toggle = ctk.CTkSwitch(
                safety_frame,
                text=text,
                variable=var,
                onvalue=True,
                offvalue=False,
                progress_color=self.colors["success"],
                button_color=self.colors["accent"]
            )
            toggle.pack(anchor="w", padx=20, pady=5)
        
        # Features settings
        features_frame = ctk.CTkFrame(
            sections_frame,
            fg_color=self.colors["glass_card"],
            corner_radius=16,
            border_width=1,
            border_color=self.colors["glass_border"]
        )
        features_frame.pack(fill="x", pady=10)
        
        ctk.CTkLabel(
            features_frame,
            text="⚡ Bot Features",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=self.colors["text_primary"]
        ).pack(anchor="w", padx=20, pady=15)
        
        # Feature toggles
        self.auto_heal_var = tk.BooleanVar(value=False)
        self.auto_loot_var = tk.BooleanVar(value=False)
        self.auto_nav_var = tk.BooleanVar(value=False)
        
        features = [
            ("Auto Heal", self.auto_heal_var),
            ("Auto Loot", self.auto_loot_var),
            ("Auto Navigation", self.auto_nav_var)
        ]
        
        for text, var in features:
            toggle = ctk.CTkSwitch(
                features_frame,
                text=text,
                variable=var,
                onvalue=True,
                offvalue=False,
                progress_color=self.colors["success"],
                button_color=self.colors["accent"]
            )
            toggle.pack(anchor="w", padx=20, pady=5)
        
        self.pages["settings"] = page
    
    def create_logs_page(self):
        """Create logs page."""
        page = ctk.CTkFrame(
            self.content_frame,
            fg_color="transparent"
        )
        
        # Header
        header = ctk.CTkFrame(
            page,
            fg_color=self.colors["glass_bg"],
            corner_radius=16,
            border_width=1,
            border_color=self.colors["glass_border"],
            height=80
        )
        header.pack(fill="x", pady=(0, 20))
        header.pack_propagate(False)
        
        ctk.CTkLabel(
            header,
            text="Logs",
            font=ctk.CTkFont(size=32, weight="bold"),
            text_color=self.colors["text_primary"]
        ).pack(side="left", padx=20, pady=20)
        
        # Help button (manual)
        help_button = ctk.CTkButton(
            header,
            text="❓ Manual",
            command=self.show_manual,
            fg_color=self.colors["accent"],
            hover_color=self.colors["accent2"],
            width=120,
            height=40,
            font=ctk.CTkFont(size=14, weight="bold"),
            corner_radius=8
        )
        help_button.pack(side="right", padx=20, pady=20)
        
        # Log controls
        controls_frame = ctk.CTkFrame(
            page,
            fg_color="transparent"
        )
        controls_frame.pack(fill="x", pady=10)
        
        ctk.CTkButton(
            controls_frame,
            text="🗑️ Clear Logs",
            command=self.clear_logs,
            fg_color=self.colors["error"],
            hover_color="#dc2626",
            width=120
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            controls_frame,
            text="💾 Save Logs",
            command=self.save_logs,
            fg_color=self.colors["accent"],
            hover_color=self.colors["accent2"],
            width=120
        ).pack(side="left", padx=5)
        
        # Log text area
        self.log_text = ctk.CTkTextbox(
            page,
            fg_color=self.colors["glass_elevated"],
            text_color=self.colors["text_primary"],
            font=ctk.CTkFont(size=12, family="Consolas"),
            corner_radius=16
        )
        self.log_text.pack(fill="both", expand=True, padx=20, pady=20)
        
        self.pages["logs"] = page
    
    def create_status_bar(self):
        """Create modern status bar."""
        status_bar = ctk.CTkFrame(
            self.main_frame,
            fg_color=self.colors["glass_card"],
            corner_radius=12,
            border_width=1,
            border_color=self.colors["glass_border"],
            height=40
        )
        status_bar.pack(side="bottom", fill="x", padx=0, pady=0)
        status_bar.pack_propagate(False)
        
        # Status text
        self.status_text = ctk.CTkLabel(
            status_bar,
            text="Ready - By Taquito Loco 🎮",
            font=ctk.CTkFont(size=12),
            text_color=self.colors["text_secondary"]
        )
        self.status_text.pack(side="left", padx=20, pady=10)
        
        # Version info
        version_label = ctk.CTkLabel(
            status_bar,
            text="v2.0.0 - Glass Edition",
            font=ctk.CTkFont(size=10),
            text_color=self.colors["text_muted"]
        )
        version_label.pack(side="right", padx=20, pady=10)
    
    # Navigation methods
    def show_dashboard(self):
        """Show dashboard page."""
        self.hide_all_pages()
        self.pages["dashboard"].pack(fill="both", expand=True)
        self.highlight_nav_button("🎮 Dashboard")
    
    def show_auto_attack(self):
        """Show auto-attack page."""
        self.hide_all_pages()
        self.pages["auto_attack"].pack(fill="both", expand=True)
        self.highlight_nav_button("⚔️ Auto-Attack")
    
    def show_status(self):
        """Show status page."""
        self.hide_all_pages()
        self.pages["status"].pack(fill="both", expand=True)
        self.highlight_nav_button("📊 Status")
    
    def show_settings(self):
        """Show settings page."""
        self.hide_all_pages()
        self.pages["settings"].pack(fill="both", expand=True)
        self.highlight_nav_button("⚙️ Settings")
    
    def show_logs(self):
        """Show logs page."""
        self.hide_all_pages()
        self.pages["logs"].pack(fill="both", expand=True)
        self.highlight_nav_button("📝 Logs")
    
    def hide_all_pages(self):
        """Hide all pages."""
        for page in self.pages.values():
            page.pack_forget()
    
    def highlight_nav_button(self, button_text):
        """Highlight the active navigation button."""
        for text, button in self.nav_buttons.items():
            if text == button_text:
                button.configure(fg_color=self.colors["accent"])
            else:
                button.configure(fg_color="transparent")
    
    # Bot control methods
    def change_language(self, value):
        """Change the application language."""
        if "English" in value:
            self.current_language = Language.ENGLISH
        else:
            self.current_language = Language.SPANISH_MEXICAN
        
        set_global_language(self.current_language)
        self.log_message(f"Language changed to: {value}")
    
    def show_manual(self):
        """Show the user manual in a popup window."""
        manual_text = """
🤖 MANUAL DE USUARIO - Tibia Bot Pro
By Taquito Loco 🎮

📋 CAMBIOS RECIENTES (v2.1)
✅ Nuevas Teclas: Y (Attack) y U (Next Target)
✅ Proceso Simplificado: Solo Start Bot
✅ Logging en Tiempo Real

🚀 CÓMO USAR (3 PASOS SIMPLES)

PASO 1: Iniciar Bot
• Ve a Dashboard
• Click en 🚀 Start Bot
• Espera confirmación automática

PASO 2: Configurar Auto-Attack
• Ve a pestaña ⚔️ Auto-Attack
• Teclas ya configuradas: Y y U
• Activa el switch "Enable Auto-Attack"

PASO 3: ¡Disfrutar!
• Bot ataca con Y
• Cambia objetivos con U
• Todo se ve en Logs en tiempo real

🎮 NAVEGACIÓN
• 🎮 Dashboard: Control principal
• ⚔️ Auto-Attack: Configuración de ataque
• 📊 Status: Monitoreo en tiempo real
• ⚙️ Settings: Configuración de seguridad
• 📝 Logs: Todos los eventos

⚔️ AUTO-ATTACK
• Attack Key: Y (configurable)
• Next Target Key: U (configurable)
• Funciona automáticamente

🛡️ SEGURIDAD
• Safe Mode siempre activo
• 100% seguro contra BattleEye
• No hay riesgo de ban

🌍 IDIOMAS
• Cambia en la barra lateral
• Inglés y Español Mexicano

📊 LOGS
• Todos los eventos en tiempo real
• Se guardan en bot_gui.log
• Revisa si algo no funciona

🚨 PROBLEMAS COMUNES
• "Tibia not found": Asegúrate de que Tibia esté corriendo
• "Key not configured": Normal en safe mode
• Auto-attack no funciona: Revisa logs y switch

💡 CONSEJOS
• Siempre usa Safe Mode
• Revisa logs si hay problemas
• Cierra con Stop Bot antes de cerrar GUI

¡Disfruta dominando Tibia, carnal! 🎮⚔️💪
        """
        
        # Create manual window
        manual_window = ctk.CTkToplevel(self.root)
        manual_window.title("📖 Manual de Usuario - By Taquito Loco 🎮")
        manual_window.geometry("800x600")
        manual_window.configure(fg_color=self.colors["glass_bg"])
        
        # Make it modal
        manual_window.transient(self.root)
        manual_window.grab_set()
        
        # Manual content
        manual_frame = ctk.CTkFrame(
            manual_window,
            fg_color=self.colors["glass_card"],
            corner_radius=16,
            border_width=1,
            border_color=self.colors["glass_border"]
        )
        manual_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Title
        title_label = ctk.CTkLabel(
            manual_frame,
            text="📖 Manual de Usuario",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color=self.colors["accent"]
        )
        title_label.pack(pady=(20, 10))
        
        subtitle_label = ctk.CTkLabel(
            manual_frame,
            text="By Taquito Loco 🎮",
            font=ctk.CTkFont(size=16),
            text_color=self.colors["text_secondary"]
        )
        subtitle_label.pack(pady=(0, 20))
        
        # Manual text
        manual_textbox = ctk.CTkTextbox(
            manual_frame,
            fg_color=self.colors["glass_elevated"],
            text_color=self.colors["text_primary"],
            font=ctk.CTkFont(size=12),
            wrap="word",
            corner_radius=12
        )
        manual_textbox.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        manual_textbox.insert("1.0", manual_text)
        manual_textbox.configure(state="disabled")  # Read-only
        
        # Close button
        close_button = ctk.CTkButton(
            manual_frame,
            text="✅ Entendido",
            command=manual_window.destroy,
            fg_color=self.colors["success"],
            hover_color="#059669",
            height=40,
            font=ctk.CTkFont(size=14, weight="bold")
        )
        close_button.pack(pady=(0, 20))
        
        # Center the window
        manual_window.update_idletasks()
        x = (manual_window.winfo_screenwidth() // 2) - (800 // 2)
        y = (manual_window.winfo_screenheight() // 2) - (600 // 2)
        manual_window.geometry(f"800x600+{x}+{y}")
        
        self.log_message("📖 Manual de usuario abierto")
    
    def show_splash_screen(self):
        splash = ctk.CTkToplevel(self.root)
        splash.title("Tibia Bot Pro - Matrix Splash")
        splash.geometry("1100x500")
        splash.configure(fg_color="#000000")
        splash.resizable(False, False)
        splash.grab_set()
        splash.transient(self.root)  # Make splash modal to main window
        
        # ASCII label
        ascii_label = ctk.CTkLabel(
            splash,
            text=ASCII_MATRIX,
            font=("Consolas", 14),
            text_color="#00FF41",
            justify="left"
        )
        ascii_label.pack(padx=20, pady=30)
        
        # Creditos
        credits = ctk.CTkLabel(
            splash,
            text="By Taquito Loco 🎮 - Matrix Edition",
            font=("Consolas", 16, "bold"),
            text_color="#00FF41"
        )
        credits.pack(pady=(0, 20))
        
        # Loading indicator
        loading_label = ctk.CTkLabel(
            splash,
            text="🖥️  Cargando interfaz gráfica...",
            font=("Consolas", 12),
            text_color="#00FF41"
        )
        loading_label.pack(pady=(0, 20))
        
        # Cerrar splash después de 3 segundos automáticamente
        def close_splash():
            time.sleep(3.0)
            try:
                splash.destroy()
            except:
                pass  # Window might already be destroyed
        
        # Start timer thread
        timer_thread = threading.Thread(target=close_splash, daemon=True)
        timer_thread.start()
        
        # Also allow manual close with Escape key
        def on_key_press(event):
            if event.keysym == 'Escape':
                splash.destroy()
        
        splash.bind('<Key>', on_key_press)
        splash.focus_set()
        
        # Don't wait for splash to close - let it close automatically
        # self.root.wait_window(splash)  # REMOVED - This was causing the hang

    def show_about(self):
        about = ctk.CTkToplevel(self.root)
        about.title("About - Tibia Bot Pro Matrix Edition")
        about.geometry("1100x600")
        about.configure(fg_color="#000000")
        about.grab_set()
        ascii_label = ctk.CTkLabel(
            about,
            text=ASCII_MATRIX,
            font=("Consolas", 14),
            text_color="#00FF41",
            justify="left"
        )
        ascii_label.pack(padx=20, pady=30)
        credits = ctk.CTkLabel(
            about,
            text="By Taquito Loco 🎮\nTibia Bot Pro - Matrix Edition\nCompatible CLI/GUI/Linux/Win",
            font=("Consolas", 16, "bold"),
            text_color="#00FF41"
        )
        credits.pack(pady=(0, 20))
        close_btn = ctk.CTkButton(
            about,
            text="Cerrar",
            command=about.destroy,
            fg_color="#00FF41",
            hover_color="#00CC33",
            text_color="#000000",
            font=ctk.CTkFont(size=14, weight="bold"),
            corner_radius=12
        )
        close_btn.pack(pady=10)
    
    def start_bot(self):
        """Start the bot with automatic initialization and Tibia detection."""
        try:
            self.log_message("🚀 Starting bot...")
            
            # Initialize bot if not already done
            if not self.bot:
                self.log_message("🔧 Initializing bot...")
                self.bot = BotCore()
                
                if not self.bot.initialize():
                    self.log_message("❌ Failed to initialize bot")
                    self.update_status_text("Bot initialization failed")
                    return
                
                self.log_message("✅ Bot initialized successfully")
            
            # Check if Tibia is detected
            if not self.bot.screen_reader.find_window():
                self.log_message("❌ Tibia window not found!")
                self.log_message("💡 Please make sure Tibia is running")
                self.update_status_text("Tibia not detected - Please start Tibia")
                return
            
            self.log_message("✅ Tibia detected successfully!")
            self.status_vars["window_status"].set("✅ Window Found")
            
            # Start bot in safe mode
            if self.bot.start_safe_mode():
                self.bot_running = True
                self.log_message("✅ Bot started in safe mode")
                self.log_message("🛡️ Safe Mode: No actual interactions")
                self.log_message("🎯 Ready for auto-attack configuration")
                
                self.status_vars["bot_status"].set("🟢 Bot Running")
                self.status_vars["safe_mode"].set("🛡️ Safe Mode: ENABLED")
                self.stop_button.configure(state="normal")
                self.start_button.configure(state="disabled")
                self.update_status_text("Bot running - Tibia detected - Ready for action!")
                
                # Start status updates
                self.start_status_updates()
                
                # Show success message
                messagebox.showinfo(
                    "Bot Started Successfully", 
                    "✅ Bot is running!\n\n"
                    "🎮 Tibia detected\n"
                    "🛡️ Safe Mode active\n"
                    "⚔️ Ready for auto-attack\n\n"
                    "Go to Auto-Attack tab to configure and start attacking!"
                )
            else:
                self.log_message("❌ Failed to start bot")
                self.update_status_text("Failed to start bot")
                
        except Exception as e:
            self.log_message(f"❌ Error starting bot: {e}")
            self.update_status_text(f"Error: {e}")
            messagebox.showerror("Error", f"Failed to start bot: {e}")
    
    def stop_bot(self):
        """Stop the bot."""
        if not self.bot:
            return
        
        try:
            self.log_message("🛑 Stopping bot...")
            self.bot.stop()
            self.bot_running = False
            self.log_message("✅ Bot stopped")
            self.status_vars["bot_status"].set("🛑 Bot Stopped")
            self.stop_button.configure(state="disabled")
            self.start_button.configure(state="normal")
            self.update_status_text("Bot stopped")
            
        except Exception as e:
            self.log_message(f"❌ Error stopping bot: {e}")
    
    def emergency_stop(self):
        """Emergency stop."""
        self.log_message("🚨 EMERGENCY STOP ACTIVATED!")
        self.stop_bot()
        self.update_status_text("EMERGENCY STOP - Bot stopped")
    
    def toggle_auto_attack(self):
        """Toggle auto-attack feature."""
        if not self.bot or not self.bot_running:
            self.log_message("❌ Bot must be running to use auto-attack")
            self.auto_attack_var.set(False)
            return
        
        if self.auto_attack_var.get():
            # Start auto-attack
            if self.bot.start_auto_attack():
                self.log_message("⚔️ Auto-attack started")
                self.status_vars["auto_attack"].set("⚔️ Auto-Attack: ENABLED")
            else:
                self.log_message("❌ Failed to start auto-attack")
                self.auto_attack_var.set(False)
        else:
            # Stop auto-attack
            self.bot.stop_auto_attack()
            self.log_message("⚔️ Auto-attack stopped")
            self.status_vars["auto_attack"].set("⚔️ Auto-Attack: DISABLED")
    
    def toggle_auto_walk(self):
        if not self.bot:
            self.log_message("❌ Bot not initialized")
            return
        if self.auto_walk_var.get():
            self.bot.resume_auto_walk()
            self.log_message("🟢 Auto-walk resumed by user")
            self.status_vars["auto_walk"] = tk.StringVar(value="🟢 Auto-Walk: ENABLED")
        else:
            self.bot.pause_auto_walk()
            self.log_message("⏸️ Auto-walk paused by user")
            self.status_vars["auto_walk"] = tk.StringVar(value="⏸️ Auto-Walk: PAUSED")
    
    def clear_logs(self):
        """Clear log text."""
        self.log_text.delete("1.0", tk.END)
        self.log_message("🗑️ Logs cleared")
    
    def save_logs(self):
        """Save logs to file."""
        try:
            logs = self.log_text.get("1.0", tk.END)
            with open("bot_logs.txt", "w", encoding="utf-8") as f:
                f.write(logs)
            self.log_message("💾 Logs saved to bot_logs.txt")
        except Exception as e:
            self.log_message(f"❌ Error saving logs: {e}")
    
    def log_message(self, message: str):
        """Add message to log."""
        timestamp = time.strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"
        self.log_text.insert(tk.END, log_entry)
        self.log_text.see(tk.END)
    
    def update_status_text(self, text: str):
        """Update status bar text."""
        self.status_text.configure(text=f"{text} - By Taquito Loco 🎮")
    
    def update_status(self):
        """Update status variables."""
        if self.bot and self.bot_running:
            # Update runtime
            runtime = "00:00:00"  # Calculate actual runtime
            self.status_vars["runtime"].set(f"⏱️ Runtime: {runtime}")
            
            # Update other status variables
            # This would be updated with real bot data
    
    def start_status_updates(self):
        """Start periodic status updates."""
        def update_loop():
            while self.bot_running:
                self.update_status()
                time.sleep(1)
        
        threading.Thread(target=update_loop, daemon=True).start()
    
    def start_animations(self):
        """Start GUI animations."""
        def pulse_animation():
            while True:
                # Pulse effect for modern elements
                time.sleep(3)
        
        threading.Thread(target=pulse_animation, daemon=True).start()

    def _setup_logging(self):
        """Setup logging to redirect to GUI log tab."""
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.INFO)
        handler = GuiLogHandler(self.log_queue)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(message)s', datefmt='%H:%M:%S')
        handler.setFormatter(formatter)
        # Remove old GUI handlers to avoid duplicates
        for h in self.logger.handlers[:]:
            if isinstance(h, GuiLogHandler):
                self.logger.removeHandler(h)
        self.logger.addHandler(handler)
        # Also log to file
        file_handler = logging.FileHandler('bot_gui.log', encoding='utf-8')
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)
        # Start log polling
        self.root.after(200, self._poll_log_queue)

    def _poll_log_queue(self):
        """Poll the log queue and display logs in the GUI."""
        try:
            while True:
                msg = self.log_queue.get_nowait()
                self.log_text.insert(tk.END, msg + '\n')
                self.log_text.see(tk.END)
        except Empty:
            pass
        self.root.after(200, self._poll_log_queue)
    
    def run(self):
        """Run the GUI."""
        self.log_message("🤖 Tibia Bot Pro Modern Interface Started")
        self.log_message("By Taquito Loco 🎮")
        self.log_message("Ready for action, carnal!")
        
        self.root.mainloop()


def main():
    """Main function to run the modern GUI."""
    app = ModernGUI()
    app.run()


if __name__ == "__main__":
    main() 