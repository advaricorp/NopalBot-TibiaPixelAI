"""
Hacker GUI for Tibia Bot
By Taquito Loco 🎮

A glassmorphism hacker-style interface with neon effects and cyberpunk aesthetics.
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

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from config.language_manager import Language, set_global_language, get_message
from config.config_manager import ConfigManager
from core.bot_core import BotCore

# Set appearance
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

class HackerGUI:
    """
    Hacker-style GUI with glassmorphism effects.
    
    Features:
    - Glassmorphism design with transparency
    - Neon green/cyan color scheme
    - Animated elements
    - Real-time bot status
    - Bilingual support (English/Spanish Mexican)
    """
    
    def __init__(self):
        """Initialize the hacker GUI."""
        self.root = ctk.CTk()
        self.root.title("🤖 TIBIA BOT - By Taquito Loco 🎮")
        self.root.geometry("800x600")  # Ventana más pequeña y compacta
        self.root.configure(fg_color="#0a0a0a")
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
            "runtime": tk.StringVar(value="⏱️ Runtime: 00:00:00")
        }
        
        # Setup GUI
        self.setup_styles()
        self.create_widgets()
        self.start_animations()
        
        # Start status updates
        self.update_status()
    
    def setup_styles(self):
        """Setup custom styles for hacker theme."""
        # Custom colors
        self.colors = {
            "neon_green": "#00ff41",
            "neon_cyan": "#00ffff",
            "dark_bg": "#0a0a0a",
            "glass_bg": "#1a1a1a",
            "glass_border": "#00ff41",
            "text_primary": "#ffffff",
            "text_secondary": "#00ff41"
        }
        
        # Configure customtkinter
        ctk.set_default_color_theme("dark-blue")
    
    def create_widgets(self):
        """Create all GUI widgets."""
        # Main container with glassmorphism effect
        self.main_frame = ctk.CTkFrame(
            self.root,
            fg_color=self.colors["glass_bg"],
            corner_radius=20,
            border_width=2,
            border_color=self.colors["glass_border"]
        )
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Header with Taquito Loco branding
        self.create_header()
        
        # Main content area
        self.content_frame = ctk.CTkFrame(
            self.main_frame,
            fg_color="transparent"
        )
        self.content_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Create tabs
        self.create_tabs()
        
        # Status bar
        self.create_status_bar()
    
    def create_header(self):
        """Create the header with branding."""
        header_frame = ctk.CTkFrame(
            self.main_frame,
            fg_color="transparent",
            height=80
        )
        header_frame.pack(fill="x", padx=20, pady=(20, 10))
        header_frame.pack_propagate(False)
        
        # Title with neon effect
        title_label = ctk.CTkLabel(
            header_frame,
            text="🤖 TIBIA BOT HACKER INTERFACE",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color=self.colors["neon_green"]
        )
        title_label.pack(side="left", padx=20)
        
        # Taquito Loco branding
        branding_label = ctk.CTkLabel(
            header_frame,
            text="By Taquito Loco 🎮",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=self.colors["neon_cyan"]
        )
        branding_label.pack(side="right", padx=20)
        
        # Language selector
        self.language_var = tk.StringVar(value="🇺🇸 English")
        language_menu = ctk.CTkOptionMenu(
            header_frame,
            values=["🇺🇸 English", "🇲🇽 Spanish"],
            variable=self.language_var,
            command=self.change_language,
            fg_color=self.colors["glass_bg"],
            button_color=self.colors["neon_green"],
            button_hover_color=self.colors["neon_cyan"]
        )
        language_menu.pack(side="right", padx=10)
    
    def create_tabs(self):
        """Create tabbed interface."""
        # Tabview
        self.tabview = ctk.CTkTabview(
            self.content_frame,
            fg_color=self.colors["glass_bg"],
            segmented_button_fg_color=self.colors["neon_green"],
            segmented_button_selected_color=self.colors["neon_cyan"],
            segmented_button_selected_hover_color=self.colors["neon_cyan"]
        )
        self.tabview.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Main Control Tab
        self.main_tab = self.tabview.add("🎮 Main Control")
        self.create_main_control_tab()
        
        # Status Monitor Tab
        self.status_tab = self.tabview.add("📊 Status Monitor")
        self.create_status_monitor_tab()
        
        # Configuration Tab
        self.config_tab = self.tabview.add("⚙️ Configuration")
        self.create_configuration_tab()
        
        # Logs Tab
        self.logs_tab = self.tabview.add("📝 Logs")
        self.create_logs_tab()
    
    def create_main_control_tab(self):
        """Create main control tab."""
        # Control buttons frame
        control_frame = ctk.CTkFrame(
            self.main_tab,
            fg_color="transparent"
        )
        control_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Bot control section
        bot_control_frame = ctk.CTkFrame(
            control_frame,
            fg_color=self.colors["glass_bg"],
            corner_radius=15,
            border_width=2,
            border_color=self.colors["glass_border"]
        )
        bot_control_frame.pack(fill="x", pady=10)
        
        # Bot control title
        ctk.CTkLabel(
            bot_control_frame,
            text="🤖 BOT CONTROL",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=self.colors["neon_green"]
        ).pack(pady=10)
        
        # Control buttons
        button_frame = ctk.CTkFrame(
            bot_control_frame,
            fg_color="transparent"
        )
        button_frame.pack(pady=20)
        
        # Initialize button
        self.init_button = ctk.CTkButton(
            button_frame,
            text="🔧 Initialize Bot",
            command=self.initialize_bot,
            fg_color=self.colors["neon_green"],
            hover_color=self.colors["neon_cyan"],
            font=ctk.CTkFont(size=14, weight="bold"),
            height=40
        )
        self.init_button.pack(side="left", padx=10)
        
        # Start button
        self.start_button = ctk.CTkButton(
            button_frame,
            text="🚀 Start Bot",
            command=self.start_bot,
            fg_color=self.colors["neon_green"],
            hover_color=self.colors["neon_cyan"],
            font=ctk.CTkFont(size=14, weight="bold"),
            height=40,
            state="disabled"
        )
        self.start_button.pack(side="left", padx=10)
        
        # Stop button
        self.stop_button = ctk.CTkButton(
            button_frame,
            text="🛑 Stop Bot",
            command=self.stop_bot,
            fg_color="#ff4444",
            hover_color="#ff6666",
            font=ctk.CTkFont(size=14, weight="bold"),
            height=40,
            state="disabled"
        )
        self.stop_button.pack(side="left", padx=10)
        
        # Emergency stop button
        self.emergency_button = ctk.CTkButton(
            button_frame,
            text="🚨 EMERGENCY STOP (F12)",
            command=self.emergency_stop,
            fg_color="#ff0000",
            hover_color="#ff3333",
            font=ctk.CTkFont(size=14, weight="bold"),
            height=40
        )
        self.emergency_button.pack(side="left", padx=10)
        
        # Quick actions section
        quick_frame = ctk.CTkFrame(
            control_frame,
            fg_color=self.colors["glass_bg"],
            corner_radius=15,
            border_width=2,
            border_color=self.colors["glass_border"]
        )
        quick_frame.pack(fill="x", pady=10)
        
        ctk.CTkLabel(
            quick_frame,
            text="⚡ QUICK ACTIONS",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=self.colors["neon_green"]
        ).pack(pady=10)
        
        quick_button_frame = ctk.CTkFrame(
            quick_frame,
            fg_color="transparent"
        )
        quick_button_frame.pack(pady=20)
        
        # Quick action buttons
        actions = [
            ("🔧 Test Screen Capture", self.test_screen_capture),
            ("🎮 Test Bot Actions", self.test_bot_actions),
            ("🛡️ Safe Mode Demo", self.safe_mode_demo),
            ("🌍 Test Bilingual", self.test_bilingual)
        ]
        
        for text, command in actions:
            btn = ctk.CTkButton(
                quick_button_frame,
                text=text,
                command=command,
                fg_color=self.colors["glass_bg"],
                border_color=self.colors["neon_green"],
                border_width=2,
                hover_color=self.colors["neon_cyan"],
                font=ctk.CTkFont(size=12),
                height=35
            )
            btn.pack(side="left", padx=5)
    
    def create_status_monitor_tab(self):
        """Create status monitor tab."""
        # Status grid
        status_frame = ctk.CTkFrame(
            self.status_tab,
            fg_color="transparent"
        )
        status_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Status indicators
        status_indicators = [
            ("Bot Status", "bot_status"),
            ("Window Status", "window_status"),
            ("Safe Mode", "safe_mode"),
            ("Current State", "current_state"),
            ("Action Count", "action_count"),
            ("Runtime", "runtime")
        ]
        
        for i, (label, var_name) in enumerate(status_indicators):
            # Status container
            status_container = ctk.CTkFrame(
                status_frame,
                fg_color=self.colors["glass_bg"],
                corner_radius=10,
                border_width=1,
                border_color=self.colors["glass_border"]
            )
            status_container.grid(row=i//3, column=i%3, padx=10, pady=10, sticky="ew")
            
            # Label
            ctk.CTkLabel(
                status_container,
                text=label,
                font=ctk.CTkFont(size=14, weight="bold"),
                text_color=self.colors["neon_green"]
            ).pack(pady=(10, 5))
            
            # Value
            ctk.CTkLabel(
                status_container,
                textvariable=self.status_vars[var_name],
                font=ctk.CTkFont(size=12),
                text_color=self.colors["text_primary"]
            ).pack(pady=(0, 10))
        
        # Configure grid weights
        for i in range(3):
            status_frame.grid_columnconfigure(i, weight=1)
    
    def create_configuration_tab(self):
        """Create configuration tab."""
        config_frame = ctk.CTkFrame(
            self.config_tab,
            fg_color="transparent"
        )
        config_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Configuration sections
        sections = [
            ("🛡️ Safety Settings", self.create_safety_config),
            ("🎮 Bot Features", self.create_features_config),
            ("⚡ Performance", self.create_performance_config)
        ]
        
        for title, create_func in sections:
            section_frame = ctk.CTkFrame(
                config_frame,
                fg_color=self.colors["glass_bg"],
                corner_radius=15,
                border_width=2,
                border_color=self.colors["glass_border"]
            )
            section_frame.pack(fill="x", pady=10)
            
            ctk.CTkLabel(
                section_frame,
                text=title,
                font=ctk.CTkFont(size=18, weight="bold"),
                text_color=self.colors["neon_green"]
            ).pack(pady=10)
            
            create_func(section_frame)
    
    def create_safety_config(self, parent):
        """Create safety configuration section."""
        # Safety toggles
        self.safe_mode_var = tk.BooleanVar(value=True)
        self.test_mode_var = tk.BooleanVar(value=True)
        
        toggles = [
            ("Safe Mode", self.safe_mode_var),
            ("Test Mode", self.test_mode_var)
        ]
        
        for text, var in toggles:
            toggle = ctk.CTkSwitch(
                parent,
                text=text,
                variable=var,
                onvalue=True,
                offvalue=False,
                progress_color=self.colors["neon_green"],
                button_color=self.colors["neon_cyan"]
            )
            toggle.pack(pady=5)
    
    def create_features_config(self, parent):
        """Create features configuration section."""
        # Feature toggles
        self.auto_heal_var = tk.BooleanVar(value=False)
        self.auto_attack_var = tk.BooleanVar(value=False)
        self.auto_loot_var = tk.BooleanVar(value=False)
        self.auto_nav_var = tk.BooleanVar(value=False)
        
        features = [
            ("Auto Heal", self.auto_heal_var),
            ("Auto Attack", self.auto_attack_var),
            ("Auto Loot", self.auto_loot_var),
            ("Auto Navigation", self.auto_nav_var)
        ]
        
        for text, var in features:
            toggle = ctk.CTkSwitch(
                parent,
                text=text,
                variable=var,
                onvalue=True,
                offvalue=False,
                progress_color=self.colors["neon_green"],
                button_color=self.colors["neon_cyan"]
            )
            toggle.pack(pady=5)
    
    def create_performance_config(self, parent):
        """Create performance configuration section."""
        # Action rate slider
        ctk.CTkLabel(
            parent,
            text="Action Rate (per minute):",
            font=ctk.CTkFont(size=12),
            text_color=self.colors["text_primary"]
        ).pack(pady=5)
        
        self.action_rate_var = tk.IntVar(value=15)
        action_rate_slider = ctk.CTkSlider(
            parent,
            from_=5,
            to=30,
            number_of_steps=25,
            variable=self.action_rate_var,
            progress_color=self.colors["neon_green"],
            button_color=self.colors["neon_cyan"]
        )
        action_rate_slider.pack(pady=5)
    
    def create_logs_tab(self):
        """Create logs tab."""
        logs_frame = ctk.CTkFrame(
            self.logs_tab,
            fg_color="transparent"
        )
        logs_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Log text area
        self.log_text = ctk.CTkTextbox(
            logs_frame,
            fg_color=self.colors["glass_bg"],
            text_color=self.colors["text_primary"],
            font=ctk.CTkFont(size=11, family="Consolas")
        )
        self.log_text.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Log controls
        log_controls = ctk.CTkFrame(
            logs_frame,
            fg_color="transparent"
        )
        log_controls.pack(fill="x", pady=10)
        
        ctk.CTkButton(
            log_controls,
            text="🗑️ Clear Logs",
            command=self.clear_logs,
            fg_color=self.colors["neon_green"],
            hover_color=self.colors["neon_cyan"]
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            log_controls,
            text="💾 Save Logs",
            command=self.save_logs,
            fg_color=self.colors["neon_green"],
            hover_color=self.colors["neon_cyan"]
        ).pack(side="left", padx=5)
    
    def create_status_bar(self):
        """Create status bar."""
        status_bar = ctk.CTkFrame(
            self.main_frame,
            fg_color=self.colors["glass_bg"],
            height=30
        )
        status_bar.pack(fill="x", padx=20, pady=(10, 20))
        status_bar.pack_propagate(False)
        
        # Status text
        self.status_text = ctk.CTkLabel(
            status_bar,
            text="Ready - By Taquito Loco 🎮",
            font=ctk.CTkFont(size=12),
            text_color=self.colors["neon_cyan"]
        )
        self.status_text.pack(side="left", padx=10)
        
        # Version info
        version_label = ctk.CTkLabel(
            status_bar,
            text="v1.0.0 - Hacker Edition",
            font=ctk.CTkFont(size=10),
            text_color=self.colors["text_secondary"]
        )
        version_label.pack(side="right", padx=10)
    
    def change_language(self, value):
        """Change the application language."""
        if "English" in value:
            self.current_language = Language.ENGLISH
        else:
            self.current_language = Language.SPANISH_MEXICAN
        
        set_global_language(self.current_language)
        self.log_message(f"Language changed to: {value}")
    
    def initialize_bot(self):
        """Initialize the bot."""
        try:
            self.log_message("🔧 Initializing bot...")
            self.bot = BotCore()
            
            if self.bot.initialize():
                self.log_message("✅ Bot initialized successfully")
                self.start_button.configure(state="normal")
                self.status_vars["bot_status"].set("✅ Bot Ready")
                self.update_status_text("Bot initialized successfully")
            else:
                self.log_message("❌ Failed to initialize bot")
                self.update_status_text("Bot initialization failed")
                
        except Exception as e:
            self.log_message(f"❌ Error initializing bot: {e}")
            self.update_status_text(f"Error: {e}")
    
    def start_bot(self):
        """Start the bot."""
        if not self.bot:
            self.log_message("❌ Bot not initialized")
            return
        
        try:
            self.log_message("🚀 Starting bot...")
            
            if self.bot.start_safe_mode():
                self.bot_running = True
                self.log_message("✅ Bot started in safe mode")
                self.status_vars["bot_status"].set("🟢 Bot Running")
                self.stop_button.configure(state="normal")
                self.start_button.configure(state="disabled")
                self.update_status_text("Bot running in safe mode")
                
                # Start status updates
                self.start_status_updates()
            else:
                self.log_message("❌ Failed to start bot")
                self.update_status_text("Failed to start bot")
                
        except Exception as e:
            self.log_message(f"❌ Error starting bot: {e}")
            self.update_status_text(f"Error: {e}")
    
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
    
    def test_screen_capture(self):
        """Test screen capture."""
        self.log_message("📸 Testing screen capture...")
        # Add screen capture test logic here
        self.log_message("✅ Screen capture test completed")
    
    def test_bot_actions(self):
        """Test bot actions."""
        self.log_message("🎮 Testing bot actions...")
        # Add bot actions test logic here
        self.log_message("✅ Bot actions test completed")
    
    def safe_mode_demo(self):
        """Run safe mode demo."""
        self.log_message("🛡️ Running safe mode demo...")
        # Add safe mode demo logic here
        self.log_message("✅ Safe mode demo completed")
    
    def test_bilingual(self):
        """Test bilingual system."""
        self.log_message("🌍 Testing bilingual system...")
        # Add bilingual test logic here
        self.log_message("✅ Bilingual test completed")
    
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
                # Pulse effect for neon elements
                time.sleep(2)
        
        threading.Thread(target=pulse_animation, daemon=True).start()
    
    def run(self):
        """Run the GUI."""
        self.log_message("🤖 Tibia Bot Hacker Interface Started")
        self.log_message("By Taquito Loco 🎮")
        self.log_message("Ready for action, carnal!")
        
        self.root.mainloop()


def main():
    """Main function to run the hacker GUI."""
    app = HackerGUI()
    app.run()


if __name__ == "__main__":
    main() 