"""
Enhanced GUI for PBT Bot
Complete interface with configuration, spells, and real-time monitoring
By Taquito Loco 🎮
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

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from bot.main import PBTBot
    from config.config_manager import ConfigManager
except ImportError as e:
    print(f"[ERROR] No se pudo importar módulos: {e}")
    sys.exit(1)

# Set appearance
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class GuiLogHandler(logging.Handler):
    """Thread-safe log handler for GUI"""
    def __init__(self, log_queue: Queue):
        super().__init__()
        self.log_queue = log_queue
    
    def emit(self, record):
        msg = self.format(record)
        self.log_queue.put(msg)

class EnhancedGUI:
    """Enhanced GUI with comprehensive features"""
    
    def __init__(self):
        """Initialize the enhanced GUI"""
        self.root = ctk.CTk()
        self.root.title("🤖 PBT Bot Pro - Enhanced Edition 🎮")
        self.root.geometry("1200x800")
        self.root.configure(fg_color="#0f0f23")
        
        # Center window
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (1200 // 2)
        y = (self.root.winfo_screenheight() // 2) - (800 // 2)
        self.root.geometry(f"1200x800+{x}+{y}")
        
        # Bot and config
        self.bot: Optional[PBTBot] = None
        self.bot_running = False
        self.config = ConfigManager()
        
        # Status variables
        self.status_vars = {
            "bot_status": tk.StringVar(value="🛑 Bot Stopped"),
            "profession": tk.StringVar(value="Knight"),
            "health": tk.StringVar(value="100/100"),
            "mana": tk.StringVar(value="100/100"),
            "combat": tk.StringVar(value="❌ No Combat"),
            "movement": tk.StringVar(value="🚶 Patrol"),
            "spells": tk.StringVar(value="🔮 Enabled"),
            "loot": tk.StringVar(value="💰 Auto"),
        }
        
        # Feature switches for real-time updates
        self.feature_switches = {}
        
        # Logging
        self.log_queue = Queue()
        self._setup_logging()
        
        # Create GUI
        self.create_widgets()
        self.start_status_updates()
        self.start_log_polling()
        
        # Show splash
        self.show_splash_screen()
    
    def create_widgets(self):
        """Create all GUI widgets"""
        # Main container
        self.main_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Create sidebar and main content
        self.create_sidebar()
        self.create_main_content()
        self.create_status_bar()
    
    def create_sidebar(self):
        """Create the sidebar"""
        self.sidebar = ctk.CTkFrame(self.main_frame, width=280, fg_color="#1e1e2e")
        self.sidebar.pack(side="left", fill="y", padx=(0, 10))
        self.sidebar.pack_propagate(False)
        
        # Title
        title_label = ctk.CTkLabel(
            self.sidebar, 
            text="🤖 PBT Bot Pro", 
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="#06b6d4"
        )
        title_label.pack(pady=20)
        
        # Control buttons
        self.create_control_buttons()
        
        # Navigation
        self.create_navigation()
        
        # Spacer
        spacer = ctk.CTkFrame(self.sidebar, height=20, fg_color="transparent")
        spacer.pack(fill="x", pady=20)
        
        # Quick status
        self.create_quick_status()
    
    def create_control_buttons(self):
        """Create control buttons"""
        # Start button
        self.start_button = ctk.CTkButton(
            self.sidebar,
            text="🚀 Start Bot",
            command=self.start_bot,
            fg_color="#10b981",
            hover_color="#059669",
            font=ctk.CTkFont(size=14, weight="bold"),
            height=40
        )
        self.start_button.pack(pady=5, padx=20, fill="x")
        
        # Stop button
        self.stop_button = ctk.CTkButton(
            self.sidebar,
            text="🛑 Stop Bot",
            command=self.stop_bot,
            fg_color="#ef4444",
            hover_color="#dc2626",
            font=ctk.CTkFont(size=14, weight="bold"),
            height=40
        )
        self.stop_button.pack(pady=5, padx=20, fill="x")
        
        # Emergency button
        self.emergency_button = ctk.CTkButton(
            self.sidebar,
            text="🚨 EMERGENCY STOP",
            command=self.emergency_stop,
            fg_color="#dc2626",
            hover_color="#b91c1c",
            font=ctk.CTkFont(size=12, weight="bold"),
            height=35
        )
        self.emergency_button.pack(pady=10, padx=20, fill="x")
    
    def create_navigation(self):
        """Create navigation buttons"""
        nav_buttons = [
            ("📊 Dashboard", self.show_dashboard),
            ("⚙️ Configuration", self.show_configuration),
            ("🔮 Spells", self.show_spells),
            ("🚶 Movement", self.show_movement),
            ("📈 Status", self.show_status),
            ("📋 Logs", self.show_logs),
        ]
        
        self.nav_buttons = {}
        for text, command in nav_buttons:
            btn = ctk.CTkButton(
                self.sidebar,
                text=text,
                command=command,
                fg_color="transparent",
                hover_color="#4f46e5",
                text_color="#ffffff",
                anchor="w",
                font=ctk.CTkFont(size=12),
                height=35
            )
            btn.pack(pady=2, padx=10, fill="x")
            self.nav_buttons[text] = btn
    
    def create_quick_status(self):
        """Create quick status display"""
        status_frame = ctk.CTkFrame(self.sidebar, fg_color="#0f0f23")
        status_frame.pack(pady=10, padx=10, fill="x")
        
        status_label = ctk.CTkLabel(status_frame, text="📊 Quick Status", font=ctk.CTkFont(size=12, weight="bold"))
        status_label.pack(pady=5)
        
        # Status items
        status_items = [
            ("Bot", "bot_status"),
            ("Profession", "profession"),
            ("Health", "health"),
            ("Mana", "mana"),
            ("Combat", "combat"),
            ("Movement", "movement"),
            ("Spells", "spells"),
            ("Loot", "loot"),
        ]
        
        for label_text, var_name in status_items:
            item_frame = ctk.CTkFrame(status_frame, fg_color="transparent")
            item_frame.pack(pady=2, padx=5, fill="x")
            
            label = ctk.CTkLabel(item_frame, text=f"{label_text}:", font=ctk.CTkFont(size=10))
            label.pack(side="left")
            
            value_label = ctk.CTkLabel(
                item_frame, 
                textvariable=self.status_vars[var_name],
                font=ctk.CTkFont(size=10),
                text_color="#a1a1aa"
            )
            value_label.pack(side="right")
    
    def create_main_content(self):
        """Create main content area"""
        self.content_frame = ctk.CTkFrame(self.main_frame, fg_color="#1e1e2e")
        self.content_frame.pack(side="right", fill="both", expand=True)
        
        # Create pages
        self.create_dashboard_page()
        self.create_configuration_page()
        self.create_spells_page()
        self.create_movement_page()
        self.create_status_page()
        self.create_logs_page()
        
        # Show dashboard by default
        self.show_dashboard()
    
    def create_dashboard_page(self):
        """Create dashboard page"""
        self.dashboard_page = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        
        # Title
        title = ctk.CTkLabel(
            self.dashboard_page,
            text="📊 Dashboard",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="#06b6d4"
        )
        title.pack(pady=20)
        
        # Stats grid
        stats_frame = ctk.CTkFrame(self.dashboard_page, fg_color="#0f0f23")
        stats_frame.pack(pady=20, padx=20, fill="both", expand=True)
        
        # Stats
        stats = [
            ("Bot Status", "bot_status", "🟢"),
            ("Profession", "profession", "⚔️"),
            ("Health", "health", "❤️"),
            ("Mana", "mana", "🔮"),
            ("Combat", "combat", "⚔️"),
            ("Movement", "movement", "🚶"),
            ("Spells", "spells", "🔮"),
            ("Loot", "loot", "💰"),
        ]
        
        for i, (label_text, var_name, icon) in enumerate(stats):
            row = i // 2
            col = i % 2
            
            frame = ctk.CTkFrame(stats_frame, fg_color="transparent")
            frame.grid(row=row, column=col, padx=10, pady=5, sticky="ew")
            
            label = ctk.CTkLabel(frame, text=f"{icon} {label_text}", font=ctk.CTkFont(size=12, weight="bold"))
            label.pack(anchor="w")
            
            value_label = ctk.CTkLabel(
                frame, 
                textvariable=self.status_vars[var_name],
                font=ctk.CTkFont(size=14),
                text_color="#ffffff"
            )
            value_label.pack(anchor="w")
        
        stats_frame.grid_columnconfigure(0, weight=1)
        stats_frame.grid_columnconfigure(1, weight=1)
    
    def create_configuration_page(self):
        """Create configuration page with clear options and status"""
        self.config_page = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        
        # Title
        title = ctk.CTkLabel(
            self.config_page,
            text="⚙️ Configuration",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="#06b6d4"
        )
        title.pack(pady=20)
        
        # Configuration frame
        config_frame = ctk.CTkFrame(self.config_page, fg_color="#0f0f23")
        config_frame.pack(pady=20, padx=20, fill="both", expand=True)
        
        # Profession selection
        profession_frame = ctk.CTkFrame(config_frame, fg_color="transparent")
        profession_frame.pack(pady=10, padx=20, fill="x")
        
        profession_label = ctk.CTkLabel(profession_frame, text="🎭 Profession:", font=ctk.CTkFont(size=14, weight="bold"))
        profession_label.pack(side="left")
        
        self.profession_var = tk.StringVar(value=self.config.get_setting("bot_settings", "profession"))
        profession_menu = ctk.CTkOptionMenu(
            profession_frame,
            values=self.config.get_all_professions(),
            variable=self.profession_var,
            command=self.change_profession,
            fg_color="#4f46e5"
        )
        profession_menu.pack(side="right")
        
        # Core Features Section
        core_features_label = ctk.CTkLabel(
            config_frame, 
            text="🎯 CORE FEATURES", 
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#10b981"
        )
        core_features_label.pack(pady=(20, 10), padx=20, anchor="w")
        
        # Core features with descriptions
        core_features = [
            ("⚔️ Auto Attack", "auto_attack", "Automatically attack enemies with SPACE key"),
            ("🚶 Auto Movement", "auto_movement", "Constant WASD movement to avoid detection"),
            ("💰 Auto Loot", "auto_loot", "Automatically loot with F4 key (configured in Tibia)"),
        ]
        
        for feature_name, config_key, description in core_features:
            self.create_feature_switch(config_frame, feature_name, config_key, description)
        
        # Advanced Features Section
        advanced_features_label = ctk.CTkLabel(
            config_frame, 
            text="🔮 ADVANCED FEATURES", 
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#f59e0b"
        )
        advanced_features_label.pack(pady=(20, 10), padx=20, anchor="w")
        
        # Advanced features
        advanced_features = [
            ("🔮 Spells Enabled", "spells_enabled", "Enable spell casting based on health/mana"),
            ("🚨 Emergency Spells", "emergency_spells", "Cast emergency spells when health is low"),
        ]
        
        for feature_name, config_key, description in advanced_features:
            self.create_feature_switch(config_frame, feature_name, config_key, description)
        
        # Hotkeys Info Section
        hotkeys_label = ctk.CTkLabel(
            config_frame, 
            text="🔑 HOTKEYS CONFIGURATION", 
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#ef4444"
        )
        hotkeys_label.pack(pady=(20, 10), padx=20, anchor="w")
        
        hotkeys_frame = ctk.CTkFrame(config_frame, fg_color="transparent")
        hotkeys_frame.pack(pady=10, padx=20, fill="x")
        
        hotkeys_text = """
SPACE - Attack (Main attack key)
F4 - Auto-loot (Configured in Tibia)
WASD - Movement (Constant movement)
F1 - Pause/Resume Bot
F2 - Stop Bot
F12 - Emergency Kill (Kills all processes)

🎮 TIBIA CONFIGURATION:
• Set F4 as your auto-loot hotkey in Tibia
• The bot will press F4 to loot automatically
• Configure your loot settings in Tibia client
        """
        
        hotkeys_textbox = ctk.CTkTextbox(
            hotkeys_frame,
            fg_color="#1e1e2e",
            text_color="#ffffff",
            font=ctk.CTkFont(size=11),
            height=120
        )
        hotkeys_textbox.pack(fill="x")
        hotkeys_textbox.insert("1.0", hotkeys_text)
        hotkeys_textbox.configure(state="disabled")
        
        # Save button
        save_button = ctk.CTkButton(
            config_frame,
            text="💾 Save Configuration",
            command=self.save_configuration,
            fg_color="#10b981",
            font=ctk.CTkFont(size=12, weight="bold"),
            height=40
        )
        save_button.pack(pady=20)
    
    def create_feature_switch(self, parent, feature_name: str, config_key: str, description: str):
        """Create a feature switch with description"""
        frame = ctk.CTkFrame(parent, fg_color="transparent")
        frame.pack(pady=5, padx=20, fill="x")
        
        # Left side - Feature info
        info_frame = ctk.CTkFrame(frame, fg_color="transparent")
        info_frame.pack(side="left", fill="x", expand=True)
        
        name_label = ctk.CTkLabel(info_frame, text=feature_name, font=ctk.CTkFont(size=12, weight="bold"))
        name_label.pack(anchor="w")
        
        desc_label = ctk.CTkLabel(
            info_frame, 
            text=description, 
            font=ctk.CTkFont(size=10),
            text_color="#a1a1aa"
        )
        desc_label.pack(anchor="w")
        
        # Right side - Switch
        switch_frame = ctk.CTkFrame(frame, fg_color="transparent")
        switch_frame.pack(side="right")
        
        # Status label
        status_var = tk.StringVar(value="🟢 ENABLED" if self.config.is_feature_enabled(config_key) else "🔴 DISABLED")
        status_label = ctk.CTkLabel(
            switch_frame,
            textvariable=status_var,
            font=ctk.CTkFont(size=10, weight="bold"),
            text_color="#10b981" if self.config.is_feature_enabled(config_key) else "#ef4444"
        )
        status_label.pack(pady=2)
        
        # Switch
        switch_var = tk.BooleanVar(value=self.config.is_feature_enabled(config_key))
        switch = ctk.CTkSwitch(
            switch_frame, 
            text="",
            command=lambda key=config_key, status=status_var: self.toggle_feature(key, status),
            variable=switch_var
        )
        switch.pack()
        
        # Store references for updates
        self.feature_switches[config_key] = {
            'switch': switch,
            'status_label': status_label,
            'status_var': status_var
        }
    
    def create_spells_page(self):
        """Create spells configuration page"""
        self.spells_page = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        
        # Title
        title = ctk.CTkLabel(
            self.spells_page,
            text="🔮 Spells Configuration",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="#06b6d4"
        )
        title.pack(pady=20)
        
        # Spells frame
        spells_frame = ctk.CTkFrame(self.spells_page, fg_color="#0f0f23")
        spells_frame.pack(pady=20, padx=20, fill="both", expand=True)
        
        # Current profession spells
        profession = self.config.get_setting("bot_settings", "profession")
        spells = self.config.get_profession_spells(profession)
        
        for spell_type, spell_list in spells.items():
            type_frame = ctk.CTkFrame(spells_frame, fg_color="transparent")
            type_frame.pack(pady=10, padx=20, fill="x")
            
            # Spell type header with color
            color_map = {
                "healing": "#10b981",
                "support": "#3b82f6", 
                "emergency": "#ef4444"
            }
            
            type_label = ctk.CTkLabel(
                type_frame, 
                text=f"{spell_type.upper()} SPELLS:", 
                font=ctk.CTkFont(size=14, weight="bold"),
                text_color=color_map.get(spell_type, "#ffffff")
            )
            type_label.pack(anchor="w")
            
            for spell in spell_list:
                spell_label = ctk.CTkLabel(
                    type_frame, 
                    text=f"  • {spell}", 
                    font=ctk.CTkFont(size=12),
                    text_color="#ffffff"
                )
                spell_label.pack(anchor="w")
    
    def create_movement_page(self):
        """Create movement configuration page"""
        self.movement_page = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        
        # Title
        title = ctk.CTkLabel(
            self.movement_page,
            text="🚶 Movement Configuration",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="#06b6d4"
        )
        title.pack(pady=20)
        
        # Movement frame
        movement_frame = ctk.CTkFrame(self.movement_page, fg_color="#0f0f23")
        movement_frame.pack(pady=20, padx=20, fill="both", expand=True)
        
        # Movement type
        movement_type_frame = ctk.CTkFrame(movement_frame, fg_color="transparent")
        movement_type_frame.pack(pady=10, padx=20, fill="x")
        
        movement_label = ctk.CTkLabel(movement_type_frame, text="Movement Type:", font=ctk.CTkFont(size=14, weight="bold"))
        movement_label.pack(side="left")
        
        self.movement_var = tk.StringVar(value=self.config.get_setting("bot_settings", "movement_type"))
        movement_menu = ctk.CTkOptionMenu(
            movement_type_frame,
            values=["patrol", "random", "stair_up", "stair_down"],
            variable=self.movement_var,
            command=self.change_movement_type,
            fg_color="#4f46e5"
        )
        movement_menu.pack(side="right")
        
        # Movement info
        movement_info_text = """
🚶 MOVEMENT FEATURES:

• Constant Movement: Bot moves continuously to avoid detection
• Stair Detection: Automatically detects and handles stairs
• Anti-Stuck: Prevents getting stuck in corners or obstacles
• Patrol Mode: Systematic movement pattern
• Random Mode: Random movement for unpredictability

🎯 MOVEMENT PRIORITIES:
1. Avoid getting stuck in corners
2. Handle stairs (up/down) automatically  
3. Maintain constant movement
4. Return to safe areas if needed

⚠️ IMPORTANT:
• Make sure Tibia window is focused
• Bot will use WASD keys for movement
• Movement is designed to be human-like
        """
        
        movement_info_label = ctk.CTkLabel(
            movement_frame,
            text=movement_info_text,
            font=ctk.CTkFont(size=12),
            text_color="#ffffff",
            justify="left"
        )
        movement_info_label.pack(pady=20, padx=20)
    
    def create_status_page(self):
        """Create status monitoring page"""
        self.status_page = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        
        # Title
        title = ctk.CTkLabel(
            self.status_page,
            text="📈 Real-Time Status",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="#06b6d4"
        )
        title.pack(pady=20)
        
        # Status display
        self.status_text = ctk.CTkTextbox(
            self.status_page,
            fg_color="#0f0f23",
            text_color="#ffffff",
            font=ctk.CTkFont(size=10)
        )
        self.status_text.pack(pady=20, padx=20, fill="both", expand=True)
    
    def create_logs_page(self):
        """Create logs page"""
        self.logs_page = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        
        # Title and controls
        title_frame = ctk.CTkFrame(self.logs_page, fg_color="transparent")
        title_frame.pack(pady=20, fill="x")
        
        title = ctk.CTkLabel(
            title_frame,
            text="📋 Logs",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="#06b6d4"
        )
        title.pack(side="left")
        
        # Log controls
        clear_button = ctk.CTkButton(
            title_frame,
            text="🗑️ Clear",
            command=self.clear_logs,
            fg_color="#f59e0b",
            width=80
        )
        clear_button.pack(side="right", padx=10)
        
        save_button = ctk.CTkButton(
            title_frame,
            text="💾 Save",
            command=self.save_logs,
            fg_color="#4f46e5",
            width=80
        )
        save_button.pack(side="right")
        
        # Log display
        self.log_text = ctk.CTkTextbox(
            self.logs_page,
            fg_color="#0f0f23",
            text_color="#ffffff",
            font=ctk.CTkFont(size=10)
        )
        self.log_text.pack(pady=20, padx=20, fill="both", expand=True)
    
    def create_status_bar(self):
        """Create status bar"""
        self.status_bar = ctk.CTkFrame(self.root, height=30, fg_color="#1e1e2e")
        self.status_bar.pack(side="bottom", fill="x")
        
        self.status_label = ctk.CTkLabel(
            self.status_bar,
            text="Ready",
            font=ctk.CTkFont(size=10),
            text_color="#a1a1aa"
        )
        self.status_label.pack(side="left", padx=10, pady=5)
    
    # Navigation methods
    def show_dashboard(self):
        self.hide_all_pages()
        self.dashboard_page.pack(fill="both", expand=True)
        self.highlight_nav_button("📊 Dashboard")
    
    def show_configuration(self):
        self.hide_all_pages()
        self.config_page.pack(fill="both", expand=True)
        self.highlight_nav_button("⚙️ Configuration")
    
    def show_spells(self):
        self.hide_all_pages()
        self.spells_page.pack(fill="both", expand=True)
        self.highlight_nav_button("🔮 Spells")
    
    def show_movement(self):
        self.hide_all_pages()
        self.movement_page.pack(fill="both", expand=True)
        self.highlight_nav_button("🚶 Movement")
    
    def show_status(self):
        self.hide_all_pages()
        self.status_page.pack(fill="both", expand=True)
        self.highlight_nav_button("📈 Status")
    
    def show_logs(self):
        self.hide_all_pages()
        self.logs_page.pack(fill="both", expand=True)
        self.highlight_nav_button("📋 Logs")
    
    def hide_all_pages(self):
        for page in [self.dashboard_page, self.config_page, self.spells_page, 
                    self.movement_page, self.status_page, self.logs_page]:
            page.pack_forget()
    
    def highlight_nav_button(self, button_text):
        for text, button in self.nav_buttons.items():
            if text == button_text:
                button.configure(fg_color="#4f46e5")
            else:
                button.configure(fg_color="transparent")
    
    # Configuration methods
    def change_profession(self, value):
        self.config.set_setting("bot_settings", "profession", value)
        self.status_vars["profession"].set(value.title())
        self.log_message(f"🎭 Profession changed to: {value}")
    
    def toggle_feature(self, feature, status_var):
        current = self.config.is_feature_enabled(feature)
        new_state = not current
        self.config.set_setting("bot_settings", feature, new_state)
        
        # Update status display
        if new_state:
            status_var.set("🟢 ENABLED")
            self.feature_switches[feature]['status_label'].configure(text_color="#10b981")
            self.log_message(f"✅ Feature {feature}: ENABLED")
        else:
            status_var.set("🔴 DISABLED")
            self.feature_switches[feature]['status_label'].configure(text_color="#ef4444")
            self.log_message(f"❌ Feature {feature}: DISABLED")
    
    def change_movement_type(self, value):
        self.config.set_setting("bot_settings", "movement_type", value)
        self.status_vars["movement"].set(value.title())
        self.log_message(f"🚶 Movement type changed to: {value}")
    
    def save_configuration(self):
        if self.config.save_config():
            self.log_message("✅ Configuration saved successfully")
            messagebox.showinfo("Success", "Configuration saved successfully!")
        else:
            self.log_message("❌ Error saving configuration")
            messagebox.showerror("Error", "Failed to save configuration")
    
    # Bot control methods
    def start_bot(self):
        try:
            if self.bot_running:
                messagebox.showwarning("Warning", "Bot is already running!")
                return
            
            self.bot = PBTBot()
            self.bot_running = True
            
            # Start bot in thread
            bot_thread = threading.Thread(target=self.bot.run, daemon=True)
            bot_thread.start()
            
            # Update status
            self.status_vars["bot_status"].set("🟢 Running")
            self.status_vars["profession"].set(self.config.get_setting("bot_settings", "profession").title())
            
            self.log_message("🚀 Bot started successfully")
            self.log_message(f"🎭 Profession: {self.config.get_setting('bot_settings', 'profession')}")
            self.log_message(f"⚔️ Attack: {self.config.get_hotkey('attack')}")
            self.log_message(f"💰 Loot: {self.config.get_hotkey('loot')}")
            self.log_message(f"🚶 Movement: {self.config.get_setting('bot_settings', 'movement_type')}")
            self.log_message(f"🔮 Spells: {'ENABLED' if self.config.is_feature_enabled('spells_enabled') else 'DISABLED'}")
            self.log_message("💀 F12 for EMERGENCY KILL")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to start bot: {e}")
            self.log_message(f"❌ Error starting bot: {e}")
    
    def stop_bot(self):
        try:
            if not self.bot_running:
                messagebox.showwarning("Warning", "Bot is not running!")
                return
            
            if self.bot:
                self.bot.stop()
            
            self.bot_running = False
            self.status_vars["bot_status"].set("🛑 Stopped")
            
            self.log_message("✅ Bot stopped successfully")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to stop bot: {e}")
            self.log_message(f"❌ Error stopping bot: {e}")
    
    def emergency_stop(self):
        try:
            if self.bot:
                self.bot._emergency_kill()
            self.bot_running = False
            self.log_message("🚨 EMERGENCY STOP ACTIVATED!")
        except Exception as e:
            self.log_message(f"❌ Emergency stop error: {e}")
    
    # Log methods
    def clear_logs(self):
        self.log_text.delete("1.0", tk.END)
        self.log_message("🗑️ Logs cleared")
    
    def save_logs(self):
        try:
            logs = self.log_text.get("1.0", tk.END)
            with open("logs/gui_logs.txt", "w", encoding="utf-8") as f:
                f.write(logs)
            self.log_message("💾 Logs saved to logs/gui_logs.txt")
        except Exception as e:
            self.log_message(f"❌ Error saving logs: {e}")
    
    def log_message(self, message: str):
        timestamp = time.strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"
        self.log_text.insert(tk.END, log_entry)
        self.log_text.see(tk.END)
    
    # Status update methods
    def update_status(self):
        if self.bot_running and self.bot:
            status = self.bot.get_status()
            
            # Update status variables
            self.status_vars["bot_status"].set("🟢 Running" if status["running"] else "🛑 Stopped")
            self.status_vars["profession"].set(status["profession"].title())
            self.status_vars["health"].set(f"{status['health']}/{self.bot.max_health}")
            self.status_vars["mana"].set(f"{status['mana']}/{self.bot.max_mana}")
            self.status_vars["combat"].set("⚔️ Combat" if status["in_combat"] else "❌ No Combat")
            self.status_vars["movement"].set(self.config.get_setting("bot_settings", "movement_type").title())
            self.status_vars["spells"].set("🔮 Enabled" if status["features"]["spells_enabled"] else "🔮 Disabled")
            self.status_vars["loot"].set("💰 Auto" if status["features"]["auto_loot"] else "💰 Manual")
    
    def start_status_updates(self):
        def update_loop():
            while True:
                self.update_status()
                time.sleep(1)
        
        update_thread = threading.Thread(target=update_loop, daemon=True)
        update_thread.start()
    
    def start_log_polling(self):
        def poll_loop():
            while True:
                try:
                    while True:
                        message = self.log_queue.get_nowait()
                        self.log_message(message)
                except Empty:
                    pass
                time.sleep(0.1)
        
        poll_thread = threading.Thread(target=poll_loop, daemon=True)
        poll_thread.start()
    
    # Setup methods
    def _setup_logging(self):
        os.makedirs("logs", exist_ok=True)
        
        logger = logging.getLogger('PBTBotGUI')
        logger.setLevel(logging.INFO)
        
        gui_handler = GuiLogHandler(self.log_queue)
        gui_handler.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        gui_handler.setFormatter(formatter)
        logger.addHandler(gui_handler)
    
    def show_splash_screen(self):
        splash = ctk.CTkToplevel(self.root)
        splash.title("PBT Bot Pro - Loading...")
        splash.geometry("600x400")
        splash.configure(fg_color="#0f0f23")
        splash.attributes('-topmost', True)
        
        # Center splash
        splash.update_idletasks()
        x = (splash.winfo_screenwidth() // 2) - (600 // 2)
        y = (splash.winfo_screenheight() // 2) - (400 // 2)
        splash.geometry(f"600x400+{x}+{y}")
        
        # Loading text
        loading_label = ctk.CTkLabel(
            splash,
            text="🤖 PBT Bot Pro - Enhanced Edition 🎮",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#06b6d4"
        )
        loading_label.pack(pady=50)
        
        # Progress bar
        progress = ctk.CTkProgressBar(splash)
        progress.pack(pady=20, padx=50, fill="x")
        progress.set(0)
        
        def close_splash():
            for i in range(100):
                progress.set(i/100)
                splash.update()
                time.sleep(0.02)
            splash.destroy()
            self.root.deiconify()
        
        splash.bind('<Key>', lambda e: close_splash())
        splash.bind('<Button-1>', lambda e: close_splash())
        splash.after(2000, close_splash)
        self.root.withdraw()
    
    def run(self):
        """Run the GUI"""
        self.root.mainloop()

def main():
    """Main function"""
    app = EnhancedGUI()
    app.run()

if __name__ == "__main__":
    main() 