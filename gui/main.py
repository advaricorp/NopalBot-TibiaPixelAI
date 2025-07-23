"""
Enhanced GUI for NopalBot
By Taquito Loco 🎮
"""

import customtkinter as ctk
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
import time
import json
import os
from datetime import datetime

# Set appearance mode and color theme
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class NopalBotGUI:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.geometry("1200x800")
        self.root.title("🤖 NopalBot Pro - Enhanced Edition 🎮")
        
        # Bot state
        self.bot_running = False
        self.bot_thread = None
        
        # Setup GUI
        self.setup_gui()
        
    def setup_gui(self):
        """Setup the main GUI"""
        # Main frame
        main_frame = ctk.CTkFrame(self.root)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Title
        title_label = ctk.CTkLabel(
            main_frame, 
            text="🤖 NopalBot Pro",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.pack(pady=10)
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Create tabs
        self.create_control_tab()
        self.create_config_tab()
        self.create_logs_tab()
        self.create_status_tab()
        
    def create_control_tab(self):
        """Create the main control tab"""
        control_frame = ctk.CTkFrame(self.notebook)
        self.notebook.add(control_frame, text="🎮 Control")
        
        # Control buttons frame
        button_frame = ctk.CTkFrame(control_frame)
        button_frame.pack(fill="x", padx=20, pady=20)
        
        # Start/Stop button
        self.start_button = ctk.CTkButton(
            button_frame,
            text="🚀 Start Bot",
            command=self.start_bot,
            height=50,
            font=ctk.CTkFont(size=16, weight="bold")
        )
        self.start_button.pack(side="left", padx=10, pady=10)
        
        # Emergency stop button
        self.emergency_button = ctk.CTkButton(
            button_frame,
            text="🛑 Emergency Stop",
            command=self.emergency_stop,
            height=50,
            fg_color="red",
            hover_color="darkred",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        self.emergency_button.pack(side="left", padx=10, pady=10)
        
        # Feature toggles frame
        features_frame = ctk.CTkFrame(control_frame)
        features_frame.pack(fill="x", padx=20, pady=20)
        
        # Feature toggles
        self.create_feature_toggles(features_frame)
        
    def create_feature_toggles(self, parent):
        """Create feature toggle switches"""
        # Title
        title_label = ctk.CTkLabel(
            parent,
            text="🎯 Bot Features",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        title_label.pack(pady=10)
        
        # Features grid
        features_grid = ctk.CTkFrame(parent)
        features_grid.pack(fill="x", padx=20, pady=10)
        
        # Auto Attack
        self.auto_attack_var = tk.BooleanVar(value=True)
        auto_attack_switch = ctk.CTkSwitch(
            features_grid,
            text="⚔️ Auto Attack",
            variable=self.auto_attack_var,
            command=self.update_config
        )
        auto_attack_switch.grid(row=0, column=0, padx=20, pady=10, sticky="w")
        
        # Status label for auto attack
        self.auto_attack_status = ctk.CTkLabel(
            features_grid,
            text="✅ Enabled",
            text_color="green"
        )
        self.auto_attack_status.grid(row=0, column=1, padx=20, pady=10)
        
        # Auto Movement
        self.auto_movement_var = tk.BooleanVar(value=True)
        auto_movement_switch = ctk.CTkSwitch(
            features_grid,
            text="🚶 Auto Movement",
            variable=self.auto_movement_var,
            command=self.update_config
        )
        auto_movement_switch.grid(row=1, column=0, padx=20, pady=10, sticky="w")
        
        self.auto_movement_status = ctk.CTkLabel(
            features_grid,
            text="✅ Enabled",
            text_color="green"
        )
        self.auto_movement_status.grid(row=1, column=1, padx=20, pady=10)
        
        # Auto Loot
        self.auto_loot_var = tk.BooleanVar(value=True)
        auto_loot_switch = ctk.CTkSwitch(
            features_grid,
            text="💰 Auto Loot",
            variable=self.auto_loot_var,
            command=self.update_config
        )
        auto_loot_switch.grid(row=2, column=0, padx=20, pady=10, sticky="w")
        
        self.auto_loot_status = ctk.CTkLabel(
            features_grid,
            text="✅ Enabled",
            text_color="green"
        )
        self.auto_loot_status.grid(row=2, column=1, padx=20, pady=10)
        
        # Spell Casting
        self.spell_casting_var = tk.BooleanVar(value=True)
        spell_casting_switch = ctk.CTkSwitch(
            features_grid,
            text="🔮 Spell Casting",
            variable=self.spell_casting_var,
            command=self.update_config
        )
        spell_casting_switch.grid(row=3, column=0, padx=20, pady=10, sticky="w")
        
        self.spell_casting_status = ctk.CTkLabel(
            features_grid,
            text="✅ Enabled",
            text_color="green"
        )
        self.spell_casting_status.grid(row=3, column=1, padx=20, pady=10)
        
    def create_config_tab(self):
        """Create the configuration tab"""
        config_frame = ctk.CTkFrame(self.notebook)
        self.notebook.add(config_frame, text="⚙️ Configuration")
        
        # Config title
        title_label = ctk.CTkLabel(
            config_frame,
            text="⚙️ Bot Configuration",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        title_label.pack(pady=10)
        
        # Hotkeys frame
        hotkeys_frame = ctk.CTkFrame(config_frame)
        hotkeys_frame.pack(fill="x", padx=20, pady=20)
        
        hotkeys_label = ctk.CTkLabel(
            hotkeys_frame,
            text="🔑 Hotkeys",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        hotkeys_label.pack(pady=10)
        
        # Hotkeys grid
        hotkeys_grid = ctk.CTkFrame(hotkeys_frame)
        hotkeys_grid.pack(fill="x", padx=20, pady=10)
        
        # Attack key
        ctk.CTkLabel(hotkeys_grid, text="⚔️ Attack:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.attack_key = ctk.CTkEntry(hotkeys_grid, placeholder_text="space")
        self.attack_key.grid(row=0, column=1, padx=10, pady=5)
        self.attack_key.insert(0, "space")
        
        # Heal key
        ctk.CTkLabel(hotkeys_grid, text="❤️ Heal:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.heal_key = ctk.CTkEntry(hotkeys_grid, placeholder_text="f1")
        self.heal_key.grid(row=1, column=1, padx=10, pady=5)
        self.heal_key.insert(0, "f1")
        
        # Spell 1 key
        ctk.CTkLabel(hotkeys_grid, text="🔮 Spell 1:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.spell1_key = ctk.CTkEntry(hotkeys_grid, placeholder_text="f2")
        self.spell1_key.grid(row=2, column=1, padx=10, pady=5)
        self.spell1_key.insert(0, "f2")
        
        # Spell 2 key
        ctk.CTkLabel(hotkeys_grid, text="🔮 Spell 2:").grid(row=3, column=0, padx=10, pady=5, sticky="w")
        self.spell2_key = ctk.CTkEntry(hotkeys_grid, placeholder_text="f3")
        self.spell2_key.grid(row=3, column=1, padx=10, pady=5)
        self.spell2_key.insert(0, "f3")
        
        # Loot key
        ctk.CTkLabel(hotkeys_grid, text="💰 Loot:").grid(row=4, column=0, padx=10, pady=5, sticky="w")
        self.loot_key = ctk.CTkEntry(hotkeys_grid, placeholder_text="f4")
        self.loot_key.grid(row=4, column=1, padx=10, pady=5)
        self.loot_key.insert(0, "f4")
        
        # Emergency key
        ctk.CTkLabel(hotkeys_grid, text="🚨 Emergency:").grid(row=5, column=0, padx=10, pady=5, sticky="w")
        self.emergency_key = ctk.CTkEntry(hotkeys_grid, placeholder_text="f12")
        self.emergency_key.grid(row=5, column=1, padx=10, pady=5)
        self.emergency_key.insert(0, "f12")
        
        # Save config button
        save_button = ctk.CTkButton(
            config_frame,
            text="💾 Save Configuration",
            command=self.save_config
        )
        save_button.pack(pady=20)
        
    def create_logs_tab(self):
        """Create the logs tab"""
        logs_frame = ctk.CTkFrame(self.notebook)
        self.notebook.add(logs_frame, text="📋 Logs")
        
        # Logs title
        title_label = ctk.CTkLabel(
            logs_frame,
            text="📋 Bot Logs",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        title_label.pack(pady=10)
        
        # Logs text area
        self.logs_text = scrolledtext.ScrolledText(
            logs_frame,
            height=20,
            width=80,
            bg="black",
            fg="white",
            font=("Consolas", 10)
        )
        self.logs_text.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Clear logs button
        clear_button = ctk.CTkButton(
            logs_frame,
            text="🗑️ Clear Logs",
            command=self.clear_logs
        )
        clear_button.pack(pady=10)
        
    def create_status_tab(self):
        """Create the status tab"""
        status_frame = ctk.CTkFrame(self.notebook)
        self.notebook.add(status_frame, text="📊 Status")
        
        # Status title
        title_label = ctk.CTkLabel(
            status_frame,
            text="📊 Bot Status",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        title_label.pack(pady=10)
        
        # Status info frame
        self.status_frame = ctk.CTkFrame(status_frame)
        self.status_frame.pack(fill="x", padx=20, pady=20)
        
        # Status labels
        self.status_labels = {}
        
        status_items = [
            ("Bot Status", "🛑 Stopped"),
            ("Health", "100/100"),
            ("Mana", "100/100"),
            ("Level", "1"),
            ("Experience", "0"),
            ("Uptime", "00:00:00")
        ]
        
        for i, (label, value) in enumerate(status_items):
            ctk.CTkLabel(self.status_frame, text=f"{label}:", font=ctk.CTkFont(weight="bold")).grid(
                row=i, column=0, padx=10, pady=5, sticky="w"
            )
            self.status_labels[label] = ctk.CTkLabel(self.status_frame, text=value)
            self.status_labels[label].grid(row=i, column=1, padx=10, pady=5, sticky="w")
        
        # Refresh status button
        refresh_button = ctk.CTkButton(
            status_frame,
            text="🔄 Refresh Status",
            command=self.refresh_status
        )
        refresh_button.pack(pady=20)
        
    def start_bot(self):
        """Start the bot"""
        if not self.bot_running:
            self.bot_running = True
            self.start_button.configure(text="🛑 Stop Bot")
            
            # Start bot in separate thread
            self.bot_thread = threading.Thread(target=self.run_bot, daemon=True)
            self.bot_thread.start()
            
            self.log_message("🚀 Bot started")
            self.update_status("Bot Status", "🟢 Running")
            
    def stop_bot(self):
        """Stop the bot"""
        if self.bot_running:
            self.bot_running = False
            self.start_button.configure(text="🚀 Start Bot")
            
            self.log_message("🛑 Bot stopped")
            self.update_status("Bot Status", "🛑 Stopped")
            
    def emergency_stop(self):
        """Emergency stop"""
        self.stop_bot()
        self.log_message("🚨 EMERGENCY STOP ACTIVATED!")
        messagebox.showwarning("Emergency Stop", "Bot has been emergency stopped!")
        
    def run_bot(self):
        """Run the bot (simulated)"""
        start_time = time.time()
        
        while self.bot_running:
            try:
                # Simulate bot activity
                current_time = time.time()
                uptime = current_time - start_time
                
                # Update uptime
                hours = int(uptime // 3600)
                minutes = int((uptime % 3600) // 60)
                seconds = int(uptime % 60)
                uptime_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
                
                self.update_status("Uptime", uptime_str)
                
                # Simulate health/mana changes
                if self.bot_running:
                    # Simulate combat
                    if hasattr(self, 'health') and self.health > 0:
                        self.health = max(0, self.health - 1)
                        self.update_status("Health", f"{self.health}/100")
                    
                    if hasattr(self, 'mana') and self.mana > 0:
                        self.mana = max(0, self.mana - 0.5)
                        self.update_status("Mana", f"{int(self.mana)}/100")
                
                time.sleep(1)
                
            except Exception as e:
                self.log_message(f"❌ Error: {e}")
                break
                
    def update_config(self):
        """Update configuration based on toggles"""
        # Update status labels
        self.auto_attack_status.configure(
            text="✅ Enabled" if self.auto_attack_var.get() else "❌ Disabled",
            text_color="green" if self.auto_attack_var.get() else "red"
        )
        
        self.auto_movement_status.configure(
            text="✅ Enabled" if self.auto_movement_var.get() else "❌ Disabled",
            text_color="green" if self.auto_movement_var.get() else "red"
        )
        
        self.auto_loot_status.configure(
            text="✅ Enabled" if self.auto_loot_var.get() else "❌ Disabled",
            text_color="green" if self.auto_loot_var.get() else "red"
        )
        
        self.spell_casting_status.configure(
            text="✅ Enabled" if self.spell_casting_var.get() else "❌ Disabled",
            text_color="green" if self.spell_casting_var.get() else "red"
        )
        
    def save_config(self):
        """Save configuration to file"""
        config = {
            "auto_attack": self.auto_attack_var.get(),
            "auto_movement": self.auto_movement_var.get(),
            "auto_loot": self.auto_loot_var.get(),
            "spell_casting": self.spell_casting_var.get(),
            "hotkeys": {
                "attack": self.attack_key.get(),
                "heal": self.heal_key.get(),
                "spell1": self.spell1_key.get(),
                "spell2": self.spell2_key.get(),
                "loot": self.loot_key.get(),
                "emergency": self.emergency_key.get()
            }
        }
        
        try:
            os.makedirs("config", exist_ok=True)
            with open("config/bot_config.json", "w") as f:
                json.dump(config, f, indent=2)
            
            self.log_message("💾 Configuration saved")
            messagebox.showinfo("Success", "Configuration saved successfully!")
            
        except Exception as e:
            self.log_message(f"❌ Error saving config: {e}")
            messagebox.showerror("Error", f"Failed to save configuration: {e}")
            
    def log_message(self, message):
        """Add message to logs"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"
        
        self.logs_text.insert(tk.END, log_entry)
        self.logs_text.see(tk.END)
        
    def clear_logs(self):
        """Clear logs"""
        self.logs_text.delete(1.0, tk.END)
        self.log_message("🗑️ Logs cleared")
        
    def update_status(self, label, value):
        """Update status label"""
        if label in self.status_labels:
            self.status_labels[label].configure(text=value)
            
    def refresh_status(self):
        """Refresh status information"""
        self.log_message("🔄 Status refreshed")
        
    def run(self):
        """Run the GUI"""
        self.root.mainloop()

def start_gui():
    """Start the GUI"""
    # Create splash screen
    splash = ctk.CTkToplevel()
    splash.title("NopalBot Pro - Loading...")
    splash.geometry("400x200")
    splash.resizable(False, False)
    
    # Center splash screen
    splash.update_idletasks()
    x = (splash.winfo_screenwidth() // 2) - (400 // 2)
    y = (splash.winfo_screenheight() // 2) - (200 // 2)
    splash.geometry(f"400x200+{x}+{y}")
    
    # Splash content
    splash_label = ctk.CTkLabel(
        splash,
        text="🤖 NopalBot Pro - Enhanced Edition 🎮",
        font=ctk.CTkFont(size=18, weight="bold")
    )
    splash_label.pack(pady=20)
    
    loading_label = ctk.CTkLabel(splash, text="Loading...")
    loading_label.pack(pady=10)
    
    progress = ctk.CTkProgressBar(splash)
    progress.pack(pady=10)
    progress.set(0)
    
    # Simulate loading
    for i in range(101):
        progress.set(i/100)
        splash.update()
        time.sleep(0.02)
    
    # Close splash and show main window
    splash.destroy()
    
    # Start main GUI
    app = NopalBotGUI()
    app.run()

if __name__ == "__main__":
    start_gui() 