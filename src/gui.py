"""
Módulo de GUI para NopalBot
Interfaz gráfica moderna y funcional
"""

import customtkinter as ctk
import tkinter as tk
from datetime import datetime
from typing import Optional, Callable
from .config import config
import time

# Configurar tema
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class Tooltip:
    """Clase para mostrar tooltips informativos"""
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip = None
        self.widget.bind("<Enter>", self.show_tooltip)
        self.widget.bind("<Leave>", self.hide_tooltip)
    
    def show_tooltip(self, event=None):
        x, y, _, _ = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 20
        
        self.tooltip = tk.Toplevel(self.widget)
        self.tooltip.wm_overrideredirect(True)
        self.tooltip.wm_geometry(f"+{x}+{y}")
        
        label = tk.Label(self.tooltip, text=self.text, 
                        justify=tk.LEFT,
                        background="#ffffe0", 
                        relief=tk.SOLID, 
                        borderwidth=1,
                        font=("Arial", "8", "normal"))
        label.pack()
    
    def hide_tooltip(self, event=None):
        if self.tooltip:
            self.tooltip.destroy()
            self.tooltip = None

class TransparentOverlay:
    """Overlay transparente para logs en tiempo real"""
    def __init__(self, parent):
        self.parent = parent
        self.is_visible = False
        self.create_overlay()
        
    def create_overlay(self):
        """Crea la ventana overlay transparente"""
        self.overlay_window = tk.Toplevel(self.parent)
        self.overlay_window.title("NopalBot Logs")
        
        # Hacer más pequeño y más a la derecha
        screen_width = self.overlay_window.winfo_screenwidth()
        screen_height = self.overlay_window.winfo_screenheight()
        
        # Tamaño 25% más grande que antes
        overlay_width = 220  # Era 175, ahora 220 (25% más)
        overlay_height = 156  # Era 125, ahora 156 (25% más)
        
        # Posición a la IZQUIERDA
        x = 20  # 20px del borde izquierdo
        y = 50  # 50px desde arriba
        
        self.overlay_window.geometry(f"{overlay_width}x{overlay_height}+{x}+{y}")
        self.overlay_window.overrideredirect(True)  # Sin bordes de ventana
        self.overlay_window.attributes('-topmost', True)  # Siempre arriba
        self.overlay_window.attributes('-alpha', 0.9)  # Transparencia
        
        # Configurar fondo negro
        self.overlay_window.configure(bg='black')
        
        # Frame principal
        main_frame = tk.Frame(self.overlay_window, bg='black')
        main_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Título
        title_label = tk.Label(main_frame, text="NopalBot Logs", 
                              font=('Consolas', 11, 'bold'),
                              fg='yellow', bg='black')
        title_label.pack(pady=2)
        
        # Texto de logs
        self.log_text = tk.Text(main_frame, 
                               width=25, height=6,  # Un poco más grande
                               font=('Consolas', 9),  # Fuente un poco más grande
                               fg='yellow', bg='black',
                               insertbackground='yellow',
                               selectbackground='darkgreen',
                               relief='flat', bd=0)
        self.log_text.pack(fill='both', expand=True, padx=2, pady=2)
        
        # Scrollbar
        scrollbar = tk.Scrollbar(main_frame, orient='vertical', command=self.log_text.yview)
        scrollbar.pack(side='right', fill='y')
        self.log_text.configure(yscrollcommand=scrollbar.set)
        
        # Botones en una fila
        buttons_frame = tk.Frame(main_frame, bg='black')
        buttons_frame.pack(fill='x', pady=2)
        
        # Botón limpiar
        clear_btn = tk.Button(buttons_frame, text="Limpiar", 
                             command=self.clear_logs,
                             font=('Consolas', 8),
                             fg='white', bg='darkred',
                             relief='flat', bd=1)
        clear_btn.pack(side='left', padx=1, expand=True)
        
        # Botón copiar
        copy_btn = tk.Button(buttons_frame, text="Copiar", 
                            command=self.copy_logs,
                            font=('Consolas', 8),
                            fg='white', bg='darkblue',
                            relief='flat', bd=1)
        copy_btn.pack(side='left', padx=1, expand=True)
        
        # Ocultar inicialmente
        self.overlay_window.withdraw()
        self.is_visible = False
        
    def show(self):
        self.overlay_window.deiconify()
        self.is_visible = True
        
    def hide(self):
        self.overlay_window.withdraw()
        self.is_visible = False
        
    def add_log(self, message: str):
        """Agrega un mensaje al log del overlay"""
        try:
            timestamp = time.strftime("%H:%M:%S")
            log_entry = f"[{timestamp}] {message}\n"
            
            self.log_text.insert("end", log_entry)
            self.log_text.see("end")
            
            # Limitar líneas para evitar que crezca demasiado
            lines = self.log_text.get("1.0", "end").split('\n')
            if len(lines) > 20:  # Máximo 20 líneas
                self.log_text.delete("1.0", "2.0")
                
        except Exception as e:
            print(f"Error agregando log al overlay: {e}")
    
    def clear_logs(self):
        """Limpia los logs del overlay"""
        try:
            self.log_text.delete("1.0", "end")
            self.add_log("Logs limpiados")
        except Exception as e:
            print(f"Error limpiando logs: {e}")
    
    def copy_logs(self):
        """Copia los logs al portapapeles"""
        try:
            logs = self.log_text.get("1.0", "end")
            self.overlay_window.clipboard_clear()
            self.overlay_window.clipboard_append(logs)
            self.add_log("Logs copiados al portapapeles")
        except Exception as e:
            print(f"Error copiando logs: {e}")
    
    def save_logs(self):
        """Guarda los logs en un archivo"""
        try:
            from datetime import datetime
            logs = self.log_text.get("1.0", "end")
            filename = f"logs/nopalbot_overlay_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            
            # Crear directorio logs si no existe
            import os
            os.makedirs("logs", exist_ok=True)
            
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(logs)
            
            self.add_log(f"Logs guardados en: {filename}")
        except Exception as e:
            self.add_log(f"Error guardando logs: {e}")
    
    def refresh_status(self):
        """Actualiza la información del bot en tiempo real"""
        try:
            if hasattr(self.parent, 'bot_instance') and self.parent.bot_instance:
                status = self.parent.bot_instance.get_status()
                status_text = f"Estado: {'Ejecutando' if status['running'] else 'Detenido'} | "
                status_text += f"HP: 100% | Mana: 100% | "  # Simulado por ahora
                status_text += f"Potiones: {status['health_potions']}/{status['mana_potions']} | "
                status_text += f"Comida: {status['food_count']}"
            else:
                status_text = "Estado: Detenido | HP: 100% | Mana: 100% | Potiones: 100/100"
            
            self.status_label.configure(text=status_text)
            self.add_log("Estado actualizado")
        except Exception as e:
            self.add_log(f"Error actualizando estado: {e}")
    
    def toggle_size(self):
        """Alterna entre tamaño grande y pequeño"""
        if self.is_large:
            # Cambiar a tamaño pequeño
            self.overlay.geometry("400x300+1300+100")
            self.size_btn.configure(text="📏 Pequeño")
            self.is_large = False
            self.add_log("Overlay cambiado a tamaño pequeño")
        else:
            # Cambiar a tamaño grande
            self.overlay.geometry("700x500+1100+50")
            self.size_btn.configure(text="📏 Grande")
            self.is_large = True
            self.add_log("Overlay cambiado a tamaño grande")

class NopalBotEliteKnightGUI:
    """GUI principal para NopalBot Elite Knight"""
    
    def __init__(self):
        self.root = ctk.CTk()
        self.bot_instance = None
        self.overlay = None
        self.setup_gui()
        
    def setup_gui(self):
        """Configura la interfaz gráfica"""
        self.root.title("NopalBot Elite Knight - Pikos Nopal")
        self.root.geometry("800x600")  # Ventana más pequeña
        self.root.resizable(True, True)
        
        # Crear scrollable frame principal
        main_container = ctk.CTkScrollableFrame(self.root, width=780, height=580)
        main_container.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Frame principal dentro del scroll
        main_frame = ctk.CTkFrame(main_container)
        main_frame.pack(fill='x', padx=5, pady=5)
        
        # Título principal
        title_label = ctk.CTkLabel(main_frame, text="⚔️ NopalBot Elite Knight ⚔️", 
                                  font=ctk.CTkFont(size=20, weight="bold"))
        title_label.pack(pady=10)
        
        # Frame de información del personaje (más compacto)
        char_frame = ctk.CTkFrame(main_frame)
        char_frame.pack(fill='x', padx=10, pady=5)
        
        ctk.CTkLabel(char_frame, text="👤 Información del Personaje", 
                    font=ctk.CTkFont(size=14, weight="bold")).pack(pady=2)
        
        char_info_frame = ctk.CTkFrame(char_frame)
        char_info_frame.pack(fill='x', padx=10, pady=2)
        
        # Información en una sola fila
        self.char_name_label = ctk.CTkLabel(char_info_frame, text="Nombre: [No detectado]", 
                                           font=ctk.CTkFont(size=12))
        self.char_name_label.pack(side='left', padx=5, pady=2)
        
        self.char_vocation_label = ctk.CTkLabel(char_info_frame, text="Vocation: Elite Knight", 
                                               font=ctk.CTkFont(size=12))
        self.char_vocation_label.pack(side='left', padx=5, pady=2)
        
        self.char_level_label = ctk.CTkLabel(char_info_frame, text="Level: [No detectado]", 
                                            font=ctk.CTkFont(size=12))
        self.char_level_label.pack(side='left', padx=5, pady=2)
        
        # Frame de controles principales (más compacto)
        controls_frame = ctk.CTkFrame(main_frame)
        controls_frame.pack(fill='x', padx=10, pady=5)
        
        ctk.CTkLabel(controls_frame, text="🎮 Controles Principales", 
                    font=ctk.CTkFont(size=14, weight="bold")).pack(pady=2)
        
        # Grid de botones principales (2 filas de 3)
        main_buttons_frame = ctk.CTkFrame(controls_frame)
        main_buttons_frame.pack(fill='x', padx=10, pady=2)
        
        # Primera fila
        row1 = ctk.CTkFrame(main_buttons_frame)
        row1.pack(fill='x', pady=1)
        
        self.auto_attack_btn = ctk.CTkButton(row1, text="⚔️ Auto Attack", 
                                            command=self.toggle_auto_attack,
                                            fg_color="#4B0082", hover_color="#6A0DAD",
                                            height=30)
        self.auto_attack_btn.pack(side='left', padx=2, pady=2, expand=True)
        
        self.auto_walk_btn = ctk.CTkButton(row1, text="🚶 Auto Walk", 
                                          command=self.toggle_auto_walk,
                                          fg_color="#4B0082", hover_color="#6A0DAD",
                                          height=30)
        self.auto_walk_btn.pack(side='left', padx=2, pady=2, expand=True)
        
        self.auto_heal_btn = ctk.CTkButton(row1, text="💚 Auto Heal", 
                                          command=self.toggle_auto_heal,
                                          fg_color="#4B0082", hover_color="#6A0DAD",
                                          height=30)
        self.auto_heal_btn.pack(side='left', padx=2, pady=2, expand=True)
        
        # Segunda fila
        row2 = ctk.CTkFrame(main_buttons_frame)
        row2.pack(fill='x', pady=1)
        
        self.auto_mana_btn = ctk.CTkButton(row2, text="🔵 Auto Mana", 
                                          command=self.toggle_auto_mana,
                                          fg_color="#4B0082", hover_color="#6A0DAD",
                                          height=30)
        self.auto_mana_btn.pack(side='left', padx=2, pady=2, expand=True)
        
        self.auto_food_btn = ctk.CTkButton(row2, text="🍖 Auto Food", 
                                          command=self.toggle_auto_food,
                                          fg_color="#4B0082", hover_color="#6A0DAD",
                                          height=30)
        self.auto_food_btn.pack(side='left', padx=2, pady=2, expand=True)
        
        self.auto_loot_btn = ctk.CTkButton(row2, text="💰 Auto Loot", 
                                          command=self.toggle_auto_loot,
                                          fg_color="#4B0082", hover_color="#6A0DAD",
                                          height=30)
        self.auto_loot_btn.pack(side='left', padx=2, pady=2, expand=True)
        
        # Tercera fila
        row3 = ctk.CTkFrame(main_buttons_frame)
        row3.pack(fill='x', pady=1)
        
        self.auto_spells_btn = ctk.CTkButton(row3, text="🔮 Auto Spells", 
                                            command=self.toggle_auto_spells,
                                            fg_color="#4B0082", hover_color="#6A0DAD",
                                            height=30)
        self.auto_spells_btn.pack(side='left', padx=2, pady=2, expand=True)
        
        self.auto_runes_btn = ctk.CTkButton(row3, text="💥 Auto Runes", 
                                           command=self.toggle_auto_runes,
                                           fg_color="#4B0082", hover_color="#6A0DAD",
                                           height=30)
        self.auto_runes_btn.pack(side='left', padx=2, pady=2, expand=True)
        
        self.overlay_btn = ctk.CTkButton(row3, text="📊 Overlay", 
                                        command=self.toggle_overlay,
                                        fg_color="#4B0082", hover_color="#6A0DAD",
                                        height=30)
        self.overlay_btn.pack(side='left', padx=2, pady=2, expand=True)
        
        # Frame de thresholds (más compacto)
        thresholds_frame = ctk.CTkFrame(main_frame)
        thresholds_frame.pack(fill='x', padx=10, pady=5)
        
        ctk.CTkLabel(thresholds_frame, text="⚙️ Configuración de Thresholds", 
                    font=ctk.CTkFont(size=14, weight="bold")).pack(pady=2)
        
        # Sliders en una sola columna más compacta
        # Heal Threshold
        heal_frame = ctk.CTkFrame(thresholds_frame)
        heal_frame.pack(fill='x', padx=10, pady=2)
        
        ctk.CTkLabel(heal_frame, text="💚 Heal:", 
                    font=ctk.CTkFont(size=11)).pack(side='left', padx=5)
        
        self.heal_slider = ctk.CTkSlider(heal_frame, from_=10, to=90, 
                                        command=self.update_heal_threshold,
                                        number_of_steps=80, height=15)
        self.heal_slider.pack(side='left', padx=10, fill='x', expand=True)
        self.heal_slider.set(config.get_threshold("heal"))
        
        self.heal_label = ctk.CTkLabel(heal_frame, text=f"{config.get_threshold('heal')}%", 
                                      font=ctk.CTkFont(size=11))
        self.heal_label.pack(side='right', padx=5)
        
        # Mana Threshold
        mana_frame = ctk.CTkFrame(thresholds_frame)
        mana_frame.pack(fill='x', padx=10, pady=2)
        
        ctk.CTkLabel(mana_frame, text="🔵 Mana:", 
                    font=ctk.CTkFont(size=11)).pack(side='left', padx=5)
        
        self.mana_slider = ctk.CTkSlider(mana_frame, from_=10, to=90, 
                                        command=self.update_mana_threshold,
                                        number_of_steps=80, height=15)
        self.mana_slider.pack(side='left', padx=10, fill='x', expand=True)
        self.mana_slider.set(config.get_threshold("mana"))
        
        self.mana_label = ctk.CTkLabel(mana_frame, text=f"{config.get_threshold('mana')}%", 
                                      font=ctk.CTkFont(size=11))
        self.mana_label.pack(side='right', padx=5)
        
        # Food Threshold
        food_frame = ctk.CTkFrame(thresholds_frame)
        food_frame.pack(fill='x', padx=10, pady=2)
        
        ctk.CTkLabel(food_frame, text="🍖 Food:", 
                    font=ctk.CTkFont(size=11)).pack(side='left', padx=5)
        
        self.food_slider = ctk.CTkSlider(food_frame, from_=10, to=90, 
                                        command=self.update_food_threshold,
                                        number_of_steps=80, height=15)
        self.food_slider.pack(side='left', padx=10, fill='x', expand=True)
        self.food_slider.set(config.get_threshold("food"))
        
        self.food_label = ctk.CTkLabel(food_frame, text=f"{config.get_threshold('food')}%", 
                                      font=ctk.CTkFont(size=11))
        self.food_label.pack(side='right', padx=5)
        
        # Frame de hechizos (más compacto)
        spells_frame = ctk.CTkFrame(main_frame)
        spells_frame.pack(fill='x', padx=10, pady=5)
        
        ctk.CTkLabel(spells_frame, text="🔮 Hechizos Elite Knight", 
                    font=ctk.CTkFont(size=14, weight="bold")).pack(pady=2)
        
        spells_buttons_frame = ctk.CTkFrame(spells_frame)
        spells_buttons_frame.pack(fill='x', padx=10, pady=2)
        
        # Hechizos en una sola fila
        self.utani_hur_btn = ctk.CTkButton(spells_buttons_frame, text="Utani Hur (F8)", 
                                          command=self.toggle_utani_hur,
                                          fg_color="#8B0000", hover_color="#A52A2A",
                                          height=25)
        self.utani_hur_btn.pack(side='left', padx=2, pady=2, expand=True)
        
        self.exori_btn = ctk.CTkButton(spells_buttons_frame, text="Exori (F5)", 
                                      command=self.toggle_exori,
                                      fg_color="#8B0000", hover_color="#A52A2A",
                                      height=25)
        self.exori_btn.pack(side='left', padx=2, pady=2, expand=True)
        
        self.exori_ico_btn = ctk.CTkButton(spells_buttons_frame, text="Exori Ico (F6)", 
                                          command=self.toggle_exori_ico,
                                          fg_color="#8B0000", hover_color="#A52A2A",
                                          height=25)
        self.exori_ico_btn.pack(side='left', padx=2, pady=2, expand=True)
        
        self.exori_gran_btn = ctk.CTkButton(spells_buttons_frame, text="Exori Gran (F7)", 
                                           command=self.toggle_exori_gran,
                                           fg_color="#8B0000", hover_color="#A52A2A",
                                           height=25)
        self.exori_gran_btn.pack(side='left', padx=2, pady=2, expand=True)
        
        self.utito_tempo_btn = ctk.CTkButton(spells_buttons_frame, text="Utito Tempo (F9)", 
                                            command=self.toggle_utito_tempo,
                                            fg_color="#8B0000", hover_color="#A52A2A",
                                            height=25)
        self.utito_tempo_btn.pack(side='left', padx=2, pady=2, expand=True)
        
        # Frame de controles de bot (más compacto)
        bot_controls_frame = ctk.CTkFrame(main_frame)
        bot_controls_frame.pack(fill='x', padx=10, pady=5)
        
        # Botones de control del bot
        self.start_btn = ctk.CTkButton(bot_controls_frame, text="🚀 Iniciar Bot", 
                                      command=self.start_bot,
                                      fg_color="#228B22", hover_color="#32CD32",
                                      font=ctk.CTkFont(size=14, weight="bold"),
                                      height=35)
        self.start_btn.pack(side='left', padx=5, pady=5, expand=True)
        
        self.stop_btn = ctk.CTkButton(bot_controls_frame, text="🛑 Detener Bot", 
                                     command=self.stop_bot,
                                     fg_color="#DC143C", hover_color="#FF0000",
                                     font=ctk.CTkFont(size=14, weight="bold"),
                                     height=35)
        self.stop_btn.pack(side='left', padx=5, pady=5, expand=True)
        
        self.save_btn = ctk.CTkButton(bot_controls_frame, text="💾 Guardar Config", 
                                     command=self.save_configuration,
                                     fg_color="#4169E1", hover_color="#1E90FF",
                                     font=ctk.CTkFont(size=12),
                                     height=35)
        self.save_btn.pack(side='left', padx=5, pady=5, expand=True)
        
        # Frame de mapas y coordenadas (más compacto)
        map_frame = ctk.CTkFrame(main_frame)
        map_frame.pack(fill='x', padx=10, pady=5)
        
        ctk.CTkLabel(map_frame, text="🗺️ Mapas y Coordenadas", 
                    font=ctk.CTkFont(size=14, weight="bold")).pack(pady=2)
        
        map_buttons_frame = ctk.CTkFrame(map_frame)
        map_buttons_frame.pack(fill='x', padx=10, pady=2)
        
        # Botones de mapas en una fila
        self.save_map_btn = ctk.CTkButton(map_buttons_frame, text="🗺️ Guardar Mapa", 
                                         command=self.save_map,
                                         fg_color="#228B22", hover_color="#32CD32",
                                         height=25)
        self.save_map_btn.pack(side='left', padx=2, pady=2, expand=True)
        
        self.load_map_btn = ctk.CTkButton(map_buttons_frame, text="📂 Cargar Mapa", 
                                         command=self.load_map,
                                         fg_color="#FF8C00", hover_color="#FFA500",
                                         height=25)
        self.load_map_btn.pack(side='left', padx=2, pady=2, expand=True)
        
        self.export_coords_btn = ctk.CTkButton(map_buttons_frame, text="📤 Exportar Coordenadas", 
                                              command=self.export_coordinates,
                                              fg_color="#8B008B", hover_color="#9932CC",
                                              height=25)
        self.export_coords_btn.pack(side='left', padx=2, pady=2, expand=True)
        
        # Frame de calibración
        calibration_frame = ctk.CTkFrame(main_frame)
        calibration_frame.pack(fill='x', padx=10, pady=5)
        
        ctk.CTkLabel(calibration_frame, text="🔧 Calibración", 
                    font=ctk.CTkFont(size=14, weight="bold")).pack(pady=2)
        
        calibration_buttons_frame = ctk.CTkFrame(calibration_frame)
        calibration_buttons_frame.pack(fill='x', padx=10, pady=2)
        
        # Botón para testear screenshot bypass
        self.config_screen_btn = ctk.CTkButton(calibration_buttons_frame, text="📸 Test Screenshot Bypass", 
                                              command=self.test_screenshot_bypass,
                                              fg_color="#FF8C00", hover_color="#FFA500",
                                              height=25)
        self.config_screen_btn.pack(side='left', padx=2, pady=2, expand=True)
        
        # Botón de calibración
        self.calibrate_btn = ctk.CTkButton(calibration_buttons_frame, text="🎯 Calibrar Barras HP/Mana", 
                                          command=self.calibrate_bars,
                                          fg_color="#FF4500", hover_color="#FF6347",
                                          height=25)
        self.calibrate_btn.pack(side='left', padx=2, pady=2, expand=True)
        
        self.test_detection_btn = ctk.CTkButton(calibration_buttons_frame, text="👁️ Probar Detección", 
                                               command=self.test_detection,
                                               fg_color="#4169E1", hover_color="#1E90FF",
                                               height=25)
        self.test_detection_btn.pack(side='left', padx=2, pady=2, expand=True)
        
        # Frame de logs (más pequeño)
        logs_frame = ctk.CTkFrame(main_frame)
        logs_frame.pack(fill='x', padx=10, pady=5)
        
        ctk.CTkLabel(logs_frame, text="📋 Logs del Bot", 
                    font=ctk.CTkFont(size=14, weight="bold")).pack(pady=2)
        
        self.log_text = ctk.CTkTextbox(logs_frame, height=100)  # Más pequeño
        self.log_text.pack(fill='x', padx=10, pady=2)
        
        # Configurar cierre de ventana
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Inicializar overlay (ARREGLADO)
        self.overlay = TransparentOverlay(self.root)
        
        # Actualizar estados de botones
        self.update_button_states()
        
        # Log inicial
        self.log_to_gui("🎮 NopalBot Elite Knight GUI iniciado")
        self.log_to_gui("💡 Todos los botones inician desactivados por defecto")
    
    def update_button_states(self):
        """Actualiza el estado visual de los botones"""
        # Configurar colores según estado
        active_color = "#228B22"  # Verde cuando está activo
        inactive_color = "#4B0082"  # Morado cuando está inactivo
        
        # Botones principales - usar las secciones correctas del JSON
        self.auto_attack_btn.configure(fg_color=active_color if config.get_feature("auto_attack") else inactive_color)
        self.auto_walk_btn.configure(fg_color=active_color if config.get_feature("auto_walk") else inactive_color)
        self.auto_heal_btn.configure(fg_color=active_color if config.get_feature("auto_heal") else inactive_color)
        self.auto_mana_btn.configure(fg_color=active_color if config.get_feature("auto_mana") else inactive_color)
        self.auto_food_btn.configure(fg_color=active_color if config.get_feature("auto_food") else inactive_color)
        self.auto_spells_btn.configure(fg_color=active_color if config.get_feature("auto_spells") else inactive_color)
        self.auto_runes_btn.configure(fg_color=active_color if config.get_feature("auto_runes") else inactive_color)
        self.auto_loot_btn.configure(fg_color=active_color if config.get_feature("auto_loot") else inactive_color)
    
    def log_to_gui(self, message: str):
        """Agrega mensaje al log de la GUI"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"
        self.log_text.insert("end", log_entry)
        self.log_text.see("end")
        
        # También agregar al overlay si está visible
        if self.overlay and self.overlay.is_visible:
            self.overlay.add_log(message)
    
    def toggle_auto_attack(self):
        """Alterna auto attack"""
        current = config.get_feature("auto_attack")
        config.update_config("combat", "auto_attack", not current)
        
        # Actualizar variable del bot si está ejecutándose
        if hasattr(self, 'bot_instance') and self.bot_instance:
            self.bot_instance.auto_attack_enabled = not current
        
        self.update_button_states()
        self.log_to_gui("⚔️ Auto Attack: " + ("Activado" if not current else "Desactivado"))
    
    def toggle_auto_walk(self):
        """Alterna auto walk"""
        current = config.get_feature("auto_walk")
        config.update_config("features", "auto_walk", not current)
        
        # Actualizar variable del bot si está ejecutándose
        if hasattr(self, 'bot_instance') and self.bot_instance:
            self.bot_instance.auto_walk_enabled = not current
        
        self.update_button_states()
        self.log_to_gui("🚶 Auto Walk: " + ("Activado" if not current else "Desactivado"))
    
    def toggle_auto_heal(self):
        """Alterna auto heal"""
        current = config.get_feature("auto_heal")
        config.update_config("features", "auto_heal", not current)
        
        # Actualizar variable del bot si está ejecutándose
        if hasattr(self, 'bot_instance') and self.bot_instance:
            self.bot_instance.auto_heal_enabled = not current
        
        self.update_button_states()
        self.log_to_gui("💚 Auto Heal: " + ("Activado" if not current else "Desactivado"))
    
    def toggle_auto_mana(self):
        """Alterna auto mana"""
        current = config.get_feature("auto_mana")
        config.update_config("features", "auto_mana", not current)
        
        # Actualizar variable del bot si está ejecutándose
        if hasattr(self, 'bot_instance') and self.bot_instance:
            self.bot_instance.auto_mana_enabled = not current
        
        self.update_button_states()
        self.log_to_gui("🔵 Auto Mana: " + ("Activado" if not current else "Desactivado"))
    
    def toggle_auto_food(self):
        """Alterna auto food"""
        current = config.get_feature("auto_food")
        config.update_config("features", "auto_food", not current)
        
        # Actualizar variable del bot si está ejecutándose
        if hasattr(self, 'bot_instance') and self.bot_instance:
            self.bot_instance.auto_food_enabled = not current
        
        self.update_button_states()
        self.log_to_gui("🍖 Auto Food: " + ("Activado" if not current else "Desactivado"))
    
    def toggle_auto_spells(self):
        """Alterna auto spells"""
        current = config.get_feature("auto_spells")
        config.update_config("combat", "auto_spells", not current)
        
        # Actualizar variable del bot si está ejecutándose
        if hasattr(self, 'bot_instance') and self.bot_instance:
            self.bot_instance.auto_spells_enabled = not current
        
        self.update_button_states()
        self.log_to_gui("🔮 Auto Spells: " + ("Activado" if not current else "Desactivado"))
    
    def toggle_auto_runes(self):
        """Alterna auto runes"""
        current = config.get_feature("auto_runes")
        config.update_config("combat", "auto_runes", not current)
        
        # Actualizar variable del bot si está ejecutándose
        if hasattr(self, 'bot_instance') and self.bot_instance:
            self.bot_instance.auto_runes_enabled = not current
        
        self.update_button_states()
        self.log_to_gui("💥 Auto Runes: " + ("Activado" if not current else "Desactivado"))
    
    def toggle_auto_loot(self):
        """Alterna auto loot"""
        current = config.get_feature("auto_loot")
        config.update_config("features", "auto_loot", not current)
        
        # Actualizar variable del bot si está ejecutándose
        if hasattr(self, 'bot_instance') and self.bot_instance:
            self.bot_instance.auto_loot_enabled = not current
        
        self.update_button_states()
        self.log_to_gui("💰 Auto Loot: " + ("Activado" if not current else "Desactivado"))
    
    def update_heal_threshold(self, value):
        """Actualiza el threshold de heal desde el slider"""
        threshold = int(value)
        config.update_config("thresholds", "heal", threshold)
        self.heal_label.configure(text=f"{threshold}%")
        self.log_to_gui(f"💚 Heal threshold actualizado: {threshold}%")
    
    def update_mana_threshold(self, value):
        """Actualiza el threshold de mana desde el slider"""
        threshold = int(value)
        config.update_config("thresholds", "mana", threshold)
        self.mana_label.configure(text=f"{threshold}%")
        self.log_to_gui(f"🔵 Mana threshold actualizado: {threshold}%")
    
    def update_food_threshold(self, value):
        """Actualiza el threshold de food desde el slider"""
        threshold = int(value)
        config.update_config("thresholds", "food", threshold)
        self.food_label.configure(text=f"{threshold}%")
        self.log_to_gui(f"🍖 Food threshold actualizado: {threshold}%")
    
    def toggle_utani_hur(self):
        """Alterna Utani Hur"""
        self.log_to_gui("🔮 Utani Hur configurado (F8)")
    
    def toggle_exori(self):
        """Alterna Exori"""
        self.log_to_gui("🔮 Exori configurado (F5)")
    
    def toggle_exori_ico(self):
        """Alterna Exori Ico"""
        self.log_to_gui("🔮 Exori Ico configurado (F6)")
    
    def toggle_exori_gran(self):
        """Alterna Exori Gran"""
        self.log_to_gui("🔮 Exori Gran configurado (F7)")
    
    def toggle_utito_tempo(self):
        """Alterna Utito Tempo"""
        self.log_to_gui("🔮 Utito Tempo configurado (F9)")
    
    def toggle_overlay(self):
        """Alterna overlay"""
        if self.overlay.is_visible:
            self.overlay.hide()
            self.log_to_gui("👁️ Overlay oculto")
        else:
            self.overlay.show()
            self.log_to_gui("👁️ Overlay visible")
    
    def start_bot(self):
        """Inicia el bot"""
        try:
            from .bot import NopalBotEliteKnight
            self.bot_instance = NopalBotEliteKnight(self.log_to_gui)
            self.bot_instance.start()
            self.log_to_gui("🚀 Bot iniciado correctamente")
            self.start_btn.configure(state="disabled")
            self.stop_btn.configure(state="normal")
        except Exception as e:
            self.log_to_gui(f"❌ Error iniciando bot: {e}")
    
    def stop_bot(self):
        """Detiene el bot"""
        if self.bot_instance:
            self.bot_instance.stop_bot()
            self.bot_instance = None
            self.log_to_gui("🛑 Bot detenido")
            self.start_btn.configure(state="normal")
            self.stop_btn.configure(state="disabled")
    
    def save_configuration(self):
        """Guarda la configuración actual"""
        if config.save_config():
            self.log_to_gui("✅ Configuración guardada")
        else:
            self.log_to_gui("❌ Error guardando configuración")
    
    def save_map(self):
        """Guarda el mapa actual"""
        if hasattr(self, 'bot_instance') and self.bot_instance:
            filename = self.bot_instance.save_map_data()
            if filename:
                self.log_to_gui(f"🗺️ Mapa guardado exitosamente: {filename}")
            else:
                self.log_to_gui("❌ Error guardando mapa")
        else:
            self.log_to_gui("❌ Bot no iniciado - no hay mapa para guardar")
    
    def load_map(self):
        """Carga un mapa desde archivo"""
        try:
            from tkinter import filedialog
            filename = filedialog.askopenfilename(
                title="Seleccionar archivo de mapa",
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
                initialdir="logs"
            )
            
            if filename and hasattr(self, 'bot_instance') and self.bot_instance:
                if self.bot_instance.load_map_data(filename):
                    self.log_to_gui(f"🗺️ Mapa cargado exitosamente: {filename}")
                else:
                    self.log_to_gui("❌ Error cargando mapa")
            elif filename:
                self.log_to_gui("❌ Bot no iniciado - inicia el bot primero")
                
        except Exception as e:
            self.log_to_gui(f"❌ Error seleccionando archivo: {e}")
    
    def export_coordinates(self):
        """Exporta coordenadas para compartir"""
        if hasattr(self, 'bot_instance') and self.bot_instance:
            filename = self.bot_instance.export_coordinates_for_sharing()
            if filename:
                self.log_to_gui(f"📤 Coordenadas exportadas: {filename}")
                self.log_to_gui("💡 Comparte este archivo con otros jugadores")
            else:
                self.log_to_gui("❌ Error exportando coordenadas")
        else:
            self.log_to_gui("❌ Bot no iniciado - no hay coordenadas para exportar")
    
    def calibrate_bars(self):
        """Calibra las barras de vida y mana"""
        try:
            from .vision import cv_system
            
            self.log_to_gui("🎯 Iniciando calibración de barras HP/Mana...")
            self.log_to_gui("💡 Asegúrate de que Tibia esté visible y las barras sean visibles")
            
            result = cv_system.calibrate_health_mana_bars()
            
            if result["success"]:
                self.log_to_gui(f"✅ {result['message']}")
                self.log_to_gui(f"📊 Tamaño de pantalla: {result['screen_size']}")
                
                if result["health_bar_found"]:
                    self.log_to_gui("💚 Barra de vida detectada")
                else:
                    self.log_to_gui("⚠️ Barra de vida NO detectada")
                
                if result["mana_bar_found"]:
                    self.log_to_gui("🔵 Barra de mana detectada")
                else:
                    self.log_to_gui("⚠️ Barra de mana NO detectada")
                
                if result["suggested_regions"]:
                    self.log_to_gui("📍 Regiones sugeridas:")
                    for region in result["suggested_regions"]:
                        self.log_to_gui(f"   - {region['type']}: {region['region']} {region['coords']}")
                
                self.log_to_gui("📸 Imagen guardada en logs/tibia_screen_calibration.png")
            else:
                self.log_to_gui(f"❌ Error en calibración: {result['message']}")
                
        except Exception as e:
            self.log_to_gui(f"❌ Error en calibración: {e}")
    
    def test_screenshot_bypass(self):
        """Test the improved simple working screenshot bypass functionality"""
        try:
            import tkinter as tk
            from tkinter import messagebox
            import cv2
            import numpy as np
            import time
            from PIL import Image, ImageTk
            from datetime import datetime
            import os
            
            self.log_to_gui("📸 Testing Improved Screenshot Bypass...")
            self.log_to_gui("💡 Using new simple working bypass methods")
            
            # Create test window
            test_window = tk.Toplevel(self.root)
            test_window.title("🎮 Improved Screenshot Bypass Test - NopalBot")
            test_window.geometry("900x700")
            test_window.resizable(True, True)
            
            # Main frame
            main_frame = tk.Frame(test_window)
            main_frame.pack(fill='both', expand=True, padx=10, pady=10)
            
            # Title
            title_label = tk.Label(main_frame, text="🎮 Improved Screenshot Bypass Test", 
                                 font=("Arial", 16, "bold"), fg="#4169E1")
            title_label.pack(pady=10)
            
            # Status label
            status_label = tk.Label(main_frame, text="Ready to test improved screenshot bypass", 
                                  font=("Arial", 12), fg="#228B22")
            status_label.pack(pady=5)
            
            # Image canvas
            canvas_frame = tk.Frame(main_frame)
            canvas_frame.pack(fill='both', expand=True, pady=10)
            
            image_canvas = tk.Canvas(canvas_frame, bg="white", relief="sunken", bd=2)
            image_canvas.pack(fill='both', expand=True)
            
            # Scrollbars
            v_scrollbar = tk.Scrollbar(canvas_frame, orient="vertical", command=image_canvas.yview)
            h_scrollbar = tk.Scrollbar(canvas_frame, orient="horizontal", command=image_canvas.xview)
            image_canvas.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
            
            v_scrollbar.pack(side="right", fill="y")
            h_scrollbar.pack(side="bottom", fill="x")
            
            # Buttons frame
            buttons_frame = tk.Frame(main_frame)
            buttons_frame.pack(fill='x', pady=10)
            
            def take_screenshot():
                """Take a screenshot using improved bypass methods"""
                try:
                    status_label.config(text="📸 Capturing screenshot with improved bypass...", fg="#FF8C00")
                    test_window.update()
                    
                    # Import improved bypass system
                    from .simple_working_bypass import SimpleWorkingBypass
                    
                    # Create bypass instance
                    bypass = SimpleWorkingBypass()
                    
                    # Check if Tibia is found first
                    if not bypass.find_tibia_window():
                        status_label.config(text="❌ Tibia not found - make sure Tibia is running", fg="#FF4500")
                        self.log_to_gui("❌ Tibia not found - make sure Tibia is running")
                        return
                    
                    # Capture screenshot
                    start_time = time.time()
                    image = bypass.capture_simple_working()
                    end_time = time.time()
                    
                    if image is None:
                        status_label.config(text="❌ Screenshot capture failed", fg="#FF4500")
                        self.log_to_gui("❌ Screenshot capture failed")
                        return
                    
                    capture_time = end_time - start_time
                    
                    # Convert BGR to RGB for tkinter
                    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                    
                    # Resize if too large
                    height, width = image_rgb.shape[:2]
                    scale = min(800/width, 500/height, 1.0)
                    new_width = int(width * scale)
                    new_height = int(height * scale)
                    
                    if scale < 1.0:
                        image_resized = cv2.resize(image_rgb, (new_width, new_height))
                    else:
                        image_resized = image_rgb
                    
                    # Convert to PIL and then to PhotoImage
                    pil_image = Image.fromarray(image_resized)
                    photo = ImageTk.PhotoImage(pil_image)
                    
                    # Update canvas
                    image_canvas.delete("all")
                    image_canvas.create_image(0, 0, anchor=tk.NW, image=photo)
                    image_canvas.image = photo  # Keep reference
                    
                    # Check image quality
                    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                    mean_brightness = np.mean(gray)
                    
                    # Update status with quality info
                    if mean_brightness < 10:
                        quality_status = "⚠️ Very dark (anti-screenshot active)"
                        status_color = "#FF8C00"
                    elif mean_brightness < 50:
                        quality_status = "⚠️ Dark (partial bypass)"
                        status_color = "#FFA500"
                    else:
                        quality_status = "✅ Good quality"
                        status_color = "#228B22"
                    
                    status_label.config(text=f"✅ Screenshot captured! ({capture_time:.3f}s) - Size: {width}x{height} - {quality_status}", fg=status_color)
                    
                    # Save screenshot
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    filename = f"logs/gui_screenshot_{timestamp}.png"
                    os.makedirs("logs", exist_ok=True)
                    cv2.imwrite(filename, image)
                    self.log_to_gui(f"💾 Screenshot saved: {filename}")
                    
                except Exception as e:
                    status_label.config(text=f"❌ Error: {str(e)}", fg="#FF4500")
                    self.log_to_gui(f"❌ Screenshot error: {e}")
            
            def take_multiple_screenshots():
                """Take multiple screenshots to test consistency"""
                try:
                    status_label.config(text="📸 Taking multiple screenshots...", fg="#FF8C00")
                    test_window.update()
                    
                    from .simple_working_bypass import SimpleWorkingBypass
                    bypass = SimpleWorkingBypass()
                    
                    # Check if Tibia is found first
                    if not bypass.find_tibia_window():
                        status_label.config(text="❌ Tibia not found - make sure Tibia is running", fg="#FF4500")
                        self.log_to_gui("❌ Tibia not found - make sure Tibia is running")
                        return
                    
                    successful_captures = 0
                    total_time = 0
                    brightness_values = []
                    
                    for i in range(5):
                        try:
                            status_label.config(text=f"📸 Taking screenshot {i+1}/5...", fg="#FF8C00")
                            test_window.update()
                            
                            start_time = time.time()
                            image = bypass.capture_simple_working()
                            end_time = time.time()
                            
                            if image is not None:
                                successful_captures += 1
                                total_time += (end_time - start_time)
                                
                                # Check brightness
                                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                                mean_brightness = np.mean(gray)
                                brightness_values.append(mean_brightness)
                                
                                self.log_to_gui(f"   ✅ Capture {i+1}: {mean_brightness:.1f} brightness ({end_time - start_time:.3f}s)")
                            else:
                                self.log_to_gui(f"   ❌ Capture {i+1}: Failed")
                            
                            time.sleep(0.1)  # Small delay
                            
                        except Exception as e:
                            self.log_to_gui(f"   ❌ Capture {i+1}: Error - {e}")
                    
                    # Results
                    success_rate = (successful_captures / 5) * 100
                    avg_time = total_time / successful_captures if successful_captures > 0 else 0
                    avg_brightness = np.mean(brightness_values) if brightness_values else 0
                    
                    status_label.config(text=f"📊 Results: {successful_captures}/5 successful, {avg_brightness:.1f} avg brightness", fg="#228B22")
                    self.log_to_gui(f"📊 Multiple captures: {success_rate:.1f}% success, {avg_time:.3f}s avg time")
                    
                except Exception as e:
                    status_label.config(text=f"❌ Error: {str(e)}", fg="#FF4500")
                    self.log_to_gui(f"❌ Multiple screenshots error: {e}")
            
            def show_bypass_info():
                """Show information about the bypass methods"""
                try:
                    from .simple_working_bypass import SimpleWorkingBypass
                    bypass = SimpleWorkingBypass()
                    
                    # Test all methods
                    results = bypass.test_simple_capture()
                    
                    info_msg = "🚀 Improved Screenshot Bypass Methods:\n\n"
                    
                    if results['tibia_found']:
                        info_msg += f"✅ Tibia Found: {results['window_info']['title']}\n\n"
                        
                        info_msg += "Methods Tested:\n"
                        for method in results['methods_tested']:
                            info_msg += f"   - {method}\n"
                        
                        info_msg += f"\nSuccessful Methods: {len(results['successful_methods'])}/{len(results['methods_tested'])}\n"
                        for method in results['successful_methods']:
                            info_msg += f"   ✅ {method['name']}: {method['time']:.3f}s, {method['size']}\n"
                        
                        if results['best_method']:
                            info_msg += f"\n🎯 Best Method: {results['best_method']}"
                    else:
                        info_msg += "❌ Tibia not found - make sure Tibia is running"
                    
                    messagebox.showinfo("ℹ️ Improved Bypass Info", info_msg)
                    
                except Exception as e:
                    messagebox.showerror("Error", f"Error getting bypass info: {e}")
            
            # Create buttons
            tk.Button(buttons_frame, text="📸 Take Screenshot", command=take_screenshot,
                     bg="#228B22", fg="white", font=("Arial", 10, "bold")).pack(side='left', padx=5)
            
            tk.Button(buttons_frame, text="🔄 Multiple Screenshots", command=take_multiple_screenshots,
                     bg="#4169E1", fg="white", font=("Arial", 10, "bold")).pack(side='left', padx=5)
            
            tk.Button(buttons_frame, text="ℹ️ Bypass Info", command=show_bypass_info,
                     bg="#FF8C00", fg="white", font=("Arial", 10, "bold")).pack(side='left', padx=5)
            
            tk.Button(buttons_frame, text="❌ Close", command=test_window.destroy,
                     bg="#DC143C", fg="white", font=("Arial", 10, "bold")).pack(side='right', padx=5)
            
        except Exception as e:
            self.log_to_gui(f"❌ Error creating screenshot test window: {e}")
            messagebox.showerror("Error", f"Error creating screenshot test window: {e}")
    
    def test_detection(self):
        """Prueba la detección actual de HP/Mana"""
        try:
            from .vision import cv_system
            
            self.log_to_gui("👁️ Probando detección de HP/Mana...")
            
            # Intentar primero con detección por píxeles (sin screenshot)
            self.log_to_gui("🔍 Intentando detección por píxeles...")
            health_percent, mana_percent = cv_system.detect_health_mana_pixels()
            
            if health_percent == 100 and mana_percent == 100:
                # Si falla, intentar con OCR
                self.log_to_gui("🔄 Píxeles falló, intentando OCR...")
                health_percent, mana_percent = cv_system.detect_health_mana_ocr()
                
                if health_percent == 100 and mana_percent == 100:
                    # Si OCR falla, intentar con detección manual
                    self.log_to_gui("🔄 OCR falló, intentando detección manual...")
                    health_percent, mana_percent = cv_system.detect_health_mana_manual()
            
            self.log_to_gui(f"💚 HP detectado: {health_percent}%")
            self.log_to_gui(f"🔵 Mana detectado: {mana_percent}%")
            
            # Mostrar información de debug
            self.log_to_gui("📸 Imágenes de debug guardadas en logs/")
            self.log_to_gui("   - HP_Region_0_red_mask.png (HP región 0)")
            self.log_to_gui("   - HP_Region_1_red_mask.png (HP región 1)")
            self.log_to_gui("   - HP_Region_2_red_mask.png (HP región 2)")
            self.log_to_gui("   - HP_Region_3_red_mask.png (HP región 3)")
            self.log_to_gui("   - Mana_Region_0_blue_mask.png (Mana región 0)")
            self.log_to_gui("   - Mana_Region_1_blue_mask.png (Mana región 1)")
            self.log_to_gui("   - Mana_Region_2_blue_mask.png (Mana región 2)")
            self.log_to_gui("   - Mana_Region_3_blue_mask.png (Mana región 3)")
            
            # Mostrar recomendaciones
            if health_percent == 100:
                self.log_to_gui("✅ HP al 100% - No necesita curación")
            elif health_percent < 40:
                self.log_to_gui("⚠️ HP bajo - Necesita curación urgente")
            else:
                self.log_to_gui("🟡 HP medio - Monitorear")
            
            if mana_percent == 100:
                self.log_to_gui("✅ Mana al 100% - No necesita potiones")
            elif mana_percent < 40:
                self.log_to_gui("⚠️ Mana bajo - Necesita potiones")
            else:
                self.log_to_gui("🟡 Mana medio - Monitorear")
            
            # Mostrar configuración actual
            heal_threshold = config.get_threshold("heal")
            mana_threshold = config.get_threshold("mana")
            self.log_to_gui(f"⚙️ Thresholds actuales: Heal {heal_threshold}%, Mana {mana_threshold}%")
            
            # Mostrar si se activaría la curación
            if health_percent < heal_threshold:
                self.log_to_gui(f"🔴 Se activaría Auto Heal (HP {health_percent}% < {heal_threshold}%)")
            else:
                self.log_to_gui(f"🟢 No se activaría Auto Heal (HP {health_percent}% >= {heal_threshold}%)")
            
            if mana_percent < mana_threshold:
                self.log_to_gui(f"🔴 Se activaría Auto Mana (Mana {mana_percent}% < {mana_threshold}%)")
            else:
                self.log_to_gui(f"🟢 No se activaría Auto Mana (Mana {mana_percent}% >= {mana_threshold}%)")
                
        except Exception as e:
            self.log_to_gui(f"❌ Error en prueba de detección: {e}")
    
    def run(self):
        """Ejecuta la GUI"""
        self.log_to_gui("🎯 NopalBot Elite Knight GUI iniciado")
        self.log_to_gui("📋 Configuración cargada desde config/bot_config.json")
        self.log_to_gui("💡 Todos los botones empiezan DESACTIVADOS - activa los que necesites")
        
        # Configurar evento de cierre para guardar configuración
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        self.root.mainloop()
    
    def on_closing(self):
        """Maneja el cierre de la ventana"""
        try:
            # Detener el bot si está ejecutándose
            if hasattr(self, 'bot_instance') and self.bot_instance:
                self.bot_instance.stop_bot()
            
            # Guardar configuración
            self.save_configuration()
            
            # Cerrar overlay si está abierto
            if self.overlay and self.overlay.is_visible:
                self.overlay.hide()
            
            self.log_to_gui("👋 Cerrando NopalBot - configuración guardada")
            
        except Exception as e:
            print(f"Error cerrando aplicación: {e}")
        
        finally:
            self.root.destroy()