#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
YouTube Downloader Premium v2.1.2
Applicazione avanzata con Knowledge Base ricercabile e Visual Summary
FIX CRITICO: Download HD funzionante con subprocess + remote_components
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import os
import sys
import threading
import sqlite3
from pathlib import Path
import json
from datetime import datetime
import re
from PIL import Image, ImageTk
import subprocess

try:
    import yt_dlp
except ImportError:
    print("ERRORE: yt-dlp non è installato. Esegui: pip install yt-dlp")
    sys.exit(1)


class DatabaseManager:
    """Gestisce il database SQLite per metadati e trascrizioni"""

    def __init__(self, db_path):
        self.db_path = db_path
        self.init_database()

    def init_database(self):
        """Inizializza il database con le tabelle necessarie"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Tabella video
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS videos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                video_id TEXT UNIQUE NOT NULL,
                title TEXT NOT NULL,
                channel TEXT,
                duration INTEGER,
                upload_date TEXT,
                description TEXT,
                thumbnail_path TEXT,
                file_path TEXT,
                download_date TEXT,
                file_size INTEGER,
                format TEXT
            )
        ''')

        # Tabella trascrizioni
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS transcripts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                video_id TEXT NOT NULL,
                language TEXT,
                transcript_text TEXT,
                FOREIGN KEY (video_id) REFERENCES videos(video_id)
            )
        ''')

        # Tabella screenshot
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS screenshots (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                video_id TEXT NOT NULL,
                timestamp REAL,
                screenshot_path TEXT,
                FOREIGN KEY (video_id) REFERENCES videos(video_id)
            )
        ''')

        # Indice per ricerca full-text
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_transcript_search
            ON transcripts(transcript_text)
        ''')

        conn.commit()
        conn.close()

    def add_video(self, video_data):
        """Aggiunge un video al database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        try:
            cursor.execute('''
                INSERT OR REPLACE INTO videos
                (video_id, title, channel, duration, upload_date, description,
                 thumbnail_path, file_path, download_date, file_size, format)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                video_data.get('id'),
                video_data.get('title'),
                video_data.get('uploader'),
                video_data.get('duration'),
                video_data.get('upload_date'),
                video_data.get('description'),
                video_data.get('thumbnail_path'),
                video_data.get('file_path'),
                datetime.now().isoformat(),
                video_data.get('file_size'),
                video_data.get('format')
            ))
            conn.commit()
            return True
        except Exception as e:
            print(f"Errore inserimento video: {e}")
            return False
        finally:
            conn.close()

    def add_transcript(self, video_id, language, text):
        """Aggiunge una trascrizione"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        try:
            cursor.execute('''
                INSERT INTO transcripts (video_id, language, transcript_text)
                VALUES (?, ?, ?)
            ''', (video_id, language, text))
            conn.commit()
            return True
        except Exception as e:
            print(f"Errore inserimento trascrizione: {e}")
            return False
        finally:
            conn.close()

    def add_screenshot(self, video_id, timestamp, path):
        """Aggiunge uno screenshot"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        try:
            cursor.execute('''
                INSERT INTO screenshots (video_id, timestamp, screenshot_path)
                VALUES (?, ?, ?)
            ''', (video_id, timestamp, path))
            conn.commit()
            return True
        except Exception as e:
            print(f"Errore inserimento screenshot: {e}")
            return False
        finally:
            conn.close()

    def search_transcripts(self, query):
        """Ricerca nelle trascrizioni"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        try:
            cursor.execute('''
                SELECT DISTINCT v.video_id, v.title, v.channel, v.thumbnail_path,
                       v.file_path, t.transcript_text, t.language
                FROM videos v
                JOIN transcripts t ON v.video_id = t.video_id
                WHERE t.transcript_text LIKE ?
                ORDER BY v.download_date DESC
            ''', (f'%{query}%',))

            results = cursor.fetchall()
            return results
        except Exception as e:
            print(f"Errore ricerca: {e}")
            return []
        finally:
            conn.close()

    def get_all_videos(self):
        """Ottiene tutti i video"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        try:
            cursor.execute('''
                SELECT video_id, title, channel, thumbnail_path, file_path,
                       download_date, format
                FROM videos
                ORDER BY download_date DESC
            ''')
            return cursor.fetchall()
        except Exception as e:
            print(f"Errore recupero video: {e}")
            return []
        finally:
            conn.close()

    def get_video_screenshots(self, video_id):
        """Ottiene gli screenshot di un video"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        try:
            cursor.execute('''
                SELECT timestamp, screenshot_path
                FROM screenshots
                WHERE video_id = ?
                ORDER BY timestamp
            ''', (video_id,))
            return cursor.fetchall()
        except Exception as e:
            print(f"Errore recupero screenshot: {e}")
            return []
        finally:
            conn.close()


class YouTubeDownloaderGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🎬 YouTube Downloader Premium v2.1.2")
        self.root.geometry("1200x800")
        self.root.resizable(True, True)

        # Colori tema moderno
        self.bg_color = "#1e1e2e"
        self.fg_color = "#cdd6f4"
        self.accent_color = "#89b4fa"
        self.button_color = "#74c7ec"
        self.error_color = "#f38ba8"
        self.success_color = "#a6e3a1"
        self.frame_color = "#313244"
        self.sidebar_color = "#181825"
        self.card_hover = "#45475a"

        # Database
        db_path = Path.home() / "Downloads" / "YouTube" / "youtube_library.db"
        db_path.parent.mkdir(parents=True, exist_ok=True)
        self.db = DatabaseManager(str(db_path))

        # Variabili
        self.download_path = tk.StringVar(value=str(Path.home() / "Downloads" / "YouTube"))
        self.url_var = tk.StringVar()
        self.quality_var = tk.StringVar(value="best")
        self.format_var = tk.StringVar(value="video")
        self.subtitles_var = tk.BooleanVar(value=True)  # Sempre attivi per Knowledge Base
        self.playlist_var = tk.BooleanVar(value=False)
        self.auto_summary_var = tk.BooleanVar(value=True)
        self.is_downloading = False
        self.current_section = "download"

        # Cache per immagini
        self.image_cache = {}

        # Configura stile
        self.setup_styles()

        # Crea UI principale
        self.create_main_layout()

        # Crea directory di default
        os.makedirs(self.download_path.get(), exist_ok=True)

    def setup_styles(self):
        """Configura gli stili ttk"""
        style = ttk.Style()
        style.theme_use('clam')
        self.root.configure(bg=self.bg_color)

        # Frame styles
        style.configure('Sidebar.TFrame', background=self.sidebar_color)
        style.configure('Custom.TFrame', background=self.bg_color)
        style.configure('Card.TFrame', background=self.frame_color)

        # Label styles
        style.configure('Title.TLabel',
                       background=self.bg_color,
                       foreground=self.accent_color,
                       font=('Segoe UI', 24, 'bold'))
        style.configure('SectionTitle.TLabel',
                       background=self.bg_color,
                       foreground=self.accent_color,
                       font=('Segoe UI', 18, 'bold'))
        style.configure('Custom.TLabel',
                       background=self.bg_color,
                       foreground=self.fg_color,
                       font=('Segoe UI', 10))
        style.configure('Card.TLabel',
                       background=self.frame_color,
                       foreground=self.fg_color,
                       font=('Segoe UI', 10))
        style.configure('Sidebar.TLabel',
                       background=self.sidebar_color,
                       foreground=self.fg_color,
                       font=('Segoe UI', 11))

        # Button styles
        style.configure('Accent.TButton',
                       background=self.button_color,
                       foreground='#1e1e2e',
                       font=('Segoe UI', 10, 'bold'),
                       borderwidth=0)
        style.configure('Sidebar.TButton',
                       background=self.sidebar_color,
                       foreground=self.fg_color,
                       font=('Segoe UI', 11, 'bold'),
                       borderwidth=0,
                       padding=15)

        # Radiobutton & Checkbutton styles
        style.configure('Custom.TRadiobutton',
                       background=self.frame_color,
                       foreground=self.fg_color,
                       font=('Segoe UI', 9))
        style.configure('Custom.TCheckbutton',
                       background=self.frame_color,
                       foreground=self.fg_color,
                       font=('Segoe UI', 9))

        # Progressbar style
        style.configure('Custom.Horizontal.TProgressbar',
                       background=self.accent_color,
                       troughcolor=self.frame_color,
                       borderwidth=0,
                       thickness=20)

    def create_main_layout(self):
        """Crea il layout principale con sidebar"""
        # Container principale
        main_container = tk.Frame(self.root, bg=self.bg_color)
        main_container.pack(fill=tk.BOTH, expand=True)

        # Sidebar
        self.create_sidebar(main_container)

        # Area contenuto
        self.content_area = tk.Frame(main_container, bg=self.bg_color)
        self.content_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Mostra sezione download di default
        self.show_download_section()

    def create_sidebar(self, parent):
        """Crea la sidebar di navigazione"""
        sidebar = tk.Frame(parent, bg=self.sidebar_color, width=200)
        sidebar.pack(side=tk.LEFT, fill=tk.Y)
        sidebar.pack_propagate(False)

        # Logo/Titolo
        logo_frame = tk.Frame(sidebar, bg=self.sidebar_color, height=100)
        logo_frame.pack(fill=tk.X, pady=(20, 40))

        tk.Label(logo_frame, text="🎬",
                font=('Segoe UI', 32),
                bg=self.sidebar_color,
                fg=self.accent_color).pack()

        tk.Label(logo_frame, text="YT Premium",
                font=('Segoe UI', 12, 'bold'),
                bg=self.sidebar_color,
                fg=self.fg_color).pack()

        # Menu items
        menu_items = [
            ("⬇️", "Download", "download"),
            ("📚", "Libreria", "library"),
            ("🎨", "Summary", "summary"),
            ("⚙️", "Impostazioni", "settings")
        ]

        for icon, text, section in menu_items:
            btn = self.create_sidebar_button(sidebar, icon, text, section)
            btn.pack(fill=tk.X, padx=10, pady=5)

        # Footer
        footer = tk.Frame(sidebar, bg=self.sidebar_color)
        footer.pack(side=tk.BOTTOM, fill=tk.X, pady=20)

        tk.Label(footer, text="v2.1.2",
                font=('Segoe UI', 8),
                bg=self.sidebar_color,
                fg=self.fg_color).pack()

    def create_sidebar_button(self, parent, icon, text, section):
        """Crea un pulsante della sidebar"""
        btn_frame = tk.Frame(parent, bg=self.sidebar_color)

        btn = tk.Button(btn_frame,
                       text=f"{icon}  {text}",
                       bg=self.sidebar_color,
                       fg=self.fg_color,
                       font=('Segoe UI', 11, 'bold'),
                       relief=tk.FLAT,
                       bd=0,
                       padx=20,
                       pady=15,
                       cursor='hand2',
                       anchor='w',
                       command=lambda: self.switch_section(section))
        btn.pack(fill=tk.BOTH)

        # Hover effect
        btn.bind('<Enter>', lambda e: btn.config(bg=self.card_hover))
        btn.bind('<Leave>', lambda e: btn.config(bg=self.sidebar_color))

        return btn_frame

    def switch_section(self, section):
        """Cambia la sezione visualizzata"""
        self.current_section = section

        # Pulisci area contenuto
        for widget in self.content_area.winfo_children():
            widget.destroy()

        # Mostra sezione appropriata
        if section == "download":
            self.show_download_section()
        elif section == "library":
            self.show_library_section()
        elif section == "summary":
            self.show_summary_section()
        elif section == "settings":
            self.show_settings_section()

    def show_download_section(self):
        """Mostra la sezione download (UI originale migliorata)"""
        # Titolo
        title = ttk.Label(self.content_area,
                         text="📥 Download Video",
                         style='SectionTitle.TLabel')
        title.pack(pady=(0, 20))

        # Frame URL
        url_frame = ttk.Frame(self.content_area, style='Card.TFrame', padding="15")
        url_frame.pack(fill=tk.X, pady=(0, 15))

        ttk.Label(url_frame, text="📎 URL Video/Playlist:", style='Card.TLabel').pack(anchor=tk.W)
        url_entry = tk.Entry(url_frame, textvariable=self.url_var,
                            font=('Segoe UI', 10),
                            bg=self.bg_color, fg=self.fg_color,
                            insertbackground=self.fg_color,
                            relief=tk.FLAT, bd=5)
        url_entry.pack(fill=tk.X, pady=(5, 0), ipady=8)

        # Frame Impostazioni (2 colonne)
        settings_frame = ttk.Frame(self.content_area, style='Card.TFrame', padding="15")
        settings_frame.pack(fill=tk.X, pady=(0, 15))

        # Colonna sinistra
        left_col = ttk.Frame(settings_frame, style='Card.TFrame')
        left_col.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

        # Formato
        ttk.Label(left_col, text="📹 Formato:", style='Card.TLabel',
                 font=('Segoe UI', 10, 'bold')).pack(anchor=tk.W, pady=(0, 5))

        formats = [
            ("Video + Audio", "video"),
            ("Solo Audio (MP3)", "audio"),
            ("Solo Sottotitoli", "subtitles")
        ]
        for text, value in formats:
            ttk.Radiobutton(left_col, text=text, variable=self.format_var,
                           value=value, style='Custom.TRadiobutton').pack(anchor=tk.W)

        # Qualità
        ttk.Label(left_col, text="⚡ Qualità:", style='Card.TLabel',
                 font=('Segoe UI', 10, 'bold')).pack(anchor=tk.W, pady=(15, 5))

        qualities = [
            ("Migliore", "best"),
            ("1080p", "1080"),
            ("720p", "720"),
            ("480p", "480")
        ]
        for text, value in qualities:
            ttk.Radiobutton(left_col, text=text, variable=self.quality_var,
                           value=value, style='Custom.TRadiobutton').pack(anchor=tk.W)

        # Colonna destra
        right_col = ttk.Frame(settings_frame, style='Card.TFrame')
        right_col.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        ttk.Label(right_col, text="⚙️ Opzioni:", style='Card.TLabel',
                 font=('Segoe UI', 10, 'bold')).pack(anchor=tk.W, pady=(0, 5))

        ttk.Checkbutton(right_col, text="📑 È una playlist",
                       variable=self.playlist_var,
                       style='Custom.TCheckbutton').pack(anchor=tk.W, pady=2)
        ttk.Checkbutton(right_col, text="🧠 Salva in Knowledge Base",
                       variable=self.subtitles_var,
                       style='Custom.TCheckbutton').pack(anchor=tk.W, pady=2)
        ttk.Checkbutton(right_col, text="📸 Genera Visual Summary",
                       variable=self.auto_summary_var,
                       style='Custom.TCheckbutton').pack(anchor=tk.W, pady=2)

        # Directory
        dir_frame = ttk.Frame(self.content_area, style='Card.TFrame', padding="15")
        dir_frame.pack(fill=tk.X, pady=(0, 15))

        ttk.Label(dir_frame, text="📁 Cartella destinazione:", style='Card.TLabel').pack(anchor=tk.W)

        dir_input = ttk.Frame(dir_frame, style='Card.TFrame')
        dir_input.pack(fill=tk.X, pady=(5, 0))

        dir_entry = tk.Entry(dir_input, textvariable=self.download_path,
                            font=('Segoe UI', 9),
                            bg=self.bg_color, fg=self.fg_color,
                            insertbackground=self.fg_color,
                            relief=tk.FLAT, bd=5, state='readonly')
        dir_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=5)

        browse_btn = tk.Button(dir_input, text="📂 Sfoglia",
                              command=self.browse_directory,
                              bg=self.frame_color, fg=self.fg_color,
                              font=('Segoe UI', 9, 'bold'),
                              relief=tk.FLAT, bd=0, padx=15, pady=5,
                              cursor='hand2')
        browse_btn.pack(side=tk.LEFT, padx=(10, 0))

        # Pulsante Download
        self.download_btn = tk.Button(self.content_area, text="⬇️ SCARICA VIDEO",
                                     command=self.start_download,
                                     bg=self.button_color, fg='#1e1e2e',
                                     font=('Segoe UI', 12, 'bold'),
                                     relief=tk.FLAT, bd=0, pady=12,
                                     cursor='hand2')
        self.download_btn.pack(fill=tk.X, pady=(0, 15))

        # Progress
        self.progress_var = tk.DoubleVar()
        self.progress = ttk.Progressbar(self.content_area, variable=self.progress_var,
                                       style='Custom.Horizontal.TProgressbar',
                                       mode='determinate', maximum=100)
        self.progress.pack(fill=tk.X, pady=(0, 5))

        self.status_label = ttk.Label(self.content_area, text="Pronto per il download",
                                     style='Custom.TLabel', font=('Segoe UI', 9))
        self.status_label.pack(anchor=tk.W, pady=(0, 10))

        # Log
        log_frame = ttk.Frame(self.content_area, style='Card.TFrame', padding="15")
        log_frame.pack(fill=tk.BOTH, expand=True)

        # Header log con pulsante copia
        log_header = tk.Frame(log_frame, bg=self.frame_color)
        log_header.pack(fill=tk.X, pady=(0, 5))

        ttk.Label(log_header, text="📋 Log:", style='Card.TLabel',
                 font=('Segoe UI', 10, 'bold')).pack(side=tk.LEFT)

        copy_log_btn = tk.Button(log_header, text="📋 Copia Log",
                                command=self.copy_log_to_clipboard,
                                bg=self.frame_color, fg=self.accent_color,
                                font=('Segoe UI', 8, 'bold'),
                                relief=tk.FLAT, bd=0, padx=10, pady=2,
                                cursor='hand2')
        copy_log_btn.pack(side=tk.RIGHT)

        self.log_text = scrolledtext.ScrolledText(log_frame, height=10,
                                                  bg=self.bg_color, fg=self.fg_color,
                                                  font=('Consolas', 9),
                                                  relief=tk.FLAT, bd=5,
                                                  insertbackground=self.fg_color,
                                                  wrap=tk.WORD)
        self.log_text.pack(fill=tk.BOTH, expand=True)

        self.log_text.tag_config('info', foreground=self.accent_color)
        self.log_text.tag_config('success', foreground=self.success_color)
        self.log_text.tag_config('error', foreground=self.error_color)

        self.log("✨ YouTube Downloader Premium v2.1.2 pronto!", 'success')
        self.log("🎬 FIX: Download HD/720p/1080p ora funzionante!", 'info')

    def show_library_section(self):
        """Mostra la sezione libreria con ricerca"""
        # Titolo
        title = ttk.Label(self.content_area,
                         text="📚 Knowledge Base",
                         style='SectionTitle.TLabel')
        title.pack(pady=(0, 20))

        # Frame ricerca
        search_frame = ttk.Frame(self.content_area, style='Card.TFrame', padding="15")
        search_frame.pack(fill=tk.X, pady=(0, 15))

        ttk.Label(search_frame, text="🔍 Ricerca nei video:", style='Card.TLabel',
                 font=('Segoe UI', 11, 'bold')).pack(anchor=tk.W, pady=(0, 10))

        search_input = ttk.Frame(search_frame, style='Card.TFrame')
        search_input.pack(fill=tk.X)

        self.search_var = tk.StringVar()
        search_entry = tk.Entry(search_input, textvariable=self.search_var,
                               font=('Segoe UI', 11),
                               bg=self.bg_color, fg=self.fg_color,
                               insertbackground=self.fg_color,
                               relief=tk.FLAT, bd=5)
        search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=8)
        search_entry.bind('<Return>', lambda e: self.perform_search())

        search_btn = tk.Button(search_input, text="🔍 Cerca",
                              command=self.perform_search,
                              bg=self.button_color, fg='#1e1e2e',
                              font=('Segoe UI', 10, 'bold'),
                              relief=tk.FLAT, bd=0, padx=20, pady=8,
                              cursor='hand2')
        search_btn.pack(side=tk.LEFT, padx=(10, 0))

        # Frame risultati (scrollable)
        results_frame = ttk.Frame(self.content_area, style='Custom.TFrame')
        results_frame.pack(fill=tk.BOTH, expand=True)

        # Canvas per scroll
        canvas = tk.Canvas(results_frame, bg=self.bg_color, highlightthickness=0)
        scrollbar = ttk.Scrollbar(results_frame, orient="vertical", command=canvas.yview)
        self.results_container = ttk.Frame(canvas, style='Custom.TFrame')

        self.results_container.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=self.results_container, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Mostra tutti i video inizialmente
        self.display_all_videos()

    def display_all_videos(self):
        """Mostra tutti i video nel database"""
        for widget in self.results_container.winfo_children():
            widget.destroy()

        videos = self.db.get_all_videos()

        if not videos:
            no_videos = ttk.Label(self.results_container,
                                 text="📭 Nessun video nel database.\nScarica video con 'Salva in Knowledge Base' attivo!",
                                 style='Custom.TLabel',
                                 font=('Segoe UI', 12),
                                 justify=tk.CENTER)
            no_videos.pack(pady=50)
            return

        for video in videos:
            self.create_video_card(video)

    def create_video_card(self, video_data):
        """Crea una card per un video"""
        video_id, title, channel, thumb_path, file_path, download_date, format_type = video_data

        card = tk.Frame(self.results_container, bg=self.frame_color, relief=tk.RAISED, bd=1)
        card.pack(fill=tk.X, padx=10, pady=5)

        # Hover effect
        def on_enter(e):
            card.config(bg=self.card_hover)
        def on_leave(e):
            card.config(bg=self.frame_color)

        card.bind('<Enter>', on_enter)
        card.bind('<Leave>', on_leave)

        inner = tk.Frame(card, bg=self.frame_color)
        inner.pack(fill=tk.BOTH, padx=15, pady=15)

        # Thumbnail (se esiste)
        if thumb_path and os.path.exists(thumb_path):
            try:
                img = Image.open(thumb_path)
                img = img.resize((120, 90), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(img)
                self.image_cache[video_id] = photo  # Mantieni riferimento

                thumb_label = tk.Label(inner, image=photo, bg=self.frame_color)
                thumb_label.pack(side=tk.LEFT, padx=(0, 15))
            except:
                pass

        # Info
        info_frame = tk.Frame(inner, bg=self.frame_color)
        info_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        title_label = tk.Label(info_frame, text=title[:80] + ("..." if len(title) > 80 else ""),
                              bg=self.frame_color, fg=self.accent_color,
                              font=('Segoe UI', 11, 'bold'), anchor='w')
        title_label.pack(fill=tk.X)

        channel_label = tk.Label(info_frame, text=f"📺 {channel or 'N/A'}",
                                bg=self.frame_color, fg=self.fg_color,
                                font=('Segoe UI', 9), anchor='w')
        channel_label.pack(fill=tk.X, pady=(2, 0))

        date_label = tk.Label(info_frame, text=f"📅 Scaricato: {download_date[:10] if download_date else 'N/A'}",
                             bg=self.frame_color, fg=self.fg_color,
                             font=('Segoe UI', 8), anchor='w')
        date_label.pack(fill=tk.X, pady=(2, 0))

        format_label = tk.Label(info_frame, text=f"📄 {format_type or 'N/A'}",
                               bg=self.frame_color, fg=self.fg_color,
                               font=('Segoe UI', 8), anchor='w')
        format_label.pack(fill=tk.X, pady=(2, 0))

        # Bottoni azioni
        actions_frame = tk.Frame(inner, bg=self.frame_color)
        actions_frame.pack(side=tk.RIGHT)

        if file_path and os.path.exists(file_path):
            open_btn = tk.Button(actions_frame, text="▶️ Apri",
                                command=lambda: self.open_file(file_path),
                                bg=self.button_color, fg='#1e1e2e',
                                font=('Segoe UI', 8, 'bold'),
                                relief=tk.FLAT, padx=10, pady=5,
                                cursor='hand2')
            open_btn.pack(pady=2)

        folder_btn = tk.Button(actions_frame, text="📂 Cartella",
                              command=lambda: self.open_folder(file_path),
                              bg=self.frame_color, fg=self.fg_color,
                              font=('Segoe UI', 8, 'bold'),
                              relief=tk.FLAT, padx=10, pady=5,
                              cursor='hand2')
        folder_btn.pack(pady=2)

    def perform_search(self):
        """Esegue la ricerca nel database"""
        query = self.search_var.get().strip()

        for widget in self.results_container.winfo_children():
            widget.destroy()

        if not query:
            self.display_all_videos()
            return

        results = self.db.search_transcripts(query)

        if not results:
            no_results = ttk.Label(self.results_container,
                                  text=f"🔍 Nessun risultato per: '{query}'",
                                  style='Custom.TLabel',
                                  font=('Segoe UI', 12))
            no_results.pack(pady=50)
            return

        for result in results:
            video_id, title, channel, thumb_path, file_path, transcript_text, language = result
            self.create_search_result_card(
                (video_id, title, channel, thumb_path, file_path, None, None),
                query, transcript_text
            )

    def create_search_result_card(self, video_data, query, transcript_snippet):
        """Crea una card per risultato di ricerca"""
        video_id, title, channel, thumb_path, file_path, _, _ = video_data

        card = tk.Frame(self.results_container, bg=self.frame_color, relief=tk.RAISED, bd=1)
        card.pack(fill=tk.X, padx=10, pady=5)

        inner = tk.Frame(card, bg=self.frame_color)
        inner.pack(fill=tk.BOTH, padx=15, pady=15)

        # Thumbnail
        if thumb_path and os.path.exists(thumb_path):
            try:
                img = Image.open(thumb_path)
                img = img.resize((120, 90), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(img)
                self.image_cache[f"{video_id}_search"] = photo

                thumb_label = tk.Label(inner, image=photo, bg=self.frame_color)
                thumb_label.pack(side=tk.LEFT, padx=(0, 15))
            except:
                pass

        # Info
        info_frame = tk.Frame(inner, bg=self.frame_color)
        info_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        title_label = tk.Label(info_frame, text=title[:80] + ("..." if len(title) > 80 else ""),
                              bg=self.frame_color, fg=self.accent_color,
                              font=('Segoe UI', 11, 'bold'), anchor='w')
        title_label.pack(fill=tk.X)

        channel_label = tk.Label(info_frame, text=f"📺 {channel or 'N/A'}",
                                bg=self.frame_color, fg=self.fg_color,
                                font=('Segoe UI', 9), anchor='w')
        channel_label.pack(fill=tk.X, pady=(2, 0))

        # Snippet con query evidenziata
        snippet = self.create_snippet(transcript_snippet, query)
        snippet_label = tk.Label(info_frame, text=f"💬 ...{snippet}...",
                                bg=self.frame_color, fg=self.success_color,
                                font=('Segoe UI', 9, 'italic'), anchor='w',
                                wraplength=500, justify=tk.LEFT)
        snippet_label.pack(fill=tk.X, pady=(5, 0))

        # Bottoni
        actions_frame = tk.Frame(inner, bg=self.frame_color)
        actions_frame.pack(side=tk.RIGHT)

        if file_path and os.path.exists(file_path):
            open_btn = tk.Button(actions_frame, text="▶️ Apri",
                                command=lambda: self.open_file(file_path),
                                bg=self.button_color, fg='#1e1e2e',
                                font=('Segoe UI', 8, 'bold'),
                                relief=tk.FLAT, padx=10, pady=5,
                                cursor='hand2')
            open_btn.pack(pady=2)

    def create_snippet(self, text, query, context_chars=100):
        """Crea uno snippet di testo con la query evidenziata"""
        query_lower = query.lower()
        text_lower = text.lower()

        pos = text_lower.find(query_lower)
        if pos == -1:
            return text[:context_chars]

        start = max(0, pos - context_chars // 2)
        end = min(len(text), pos + len(query) + context_chars // 2)

        return text[start:end]

    def show_summary_section(self):
        """Mostra la sezione Visual Summary"""
        # Titolo
        title = ttk.Label(self.content_area,
                         text="🎨 Visual Summary Generator",
                         style='SectionTitle.TLabel')
        title.pack(pady=(0, 20))

        # Selezione video
        select_frame = ttk.Frame(self.content_area, style='Card.TFrame', padding="15")
        select_frame.pack(fill=tk.X, pady=(0, 15))

        ttk.Label(select_frame, text="📺 Seleziona video:", style='Card.TLabel',
                 font=('Segoe UI', 11, 'bold')).pack(anchor=tk.W, pady=(0, 10))

        # Dropdown con video
        videos = self.db.get_all_videos()
        if not videos:
            ttk.Label(select_frame, text="Nessun video disponibile",
                     style='Card.TLabel').pack()
            return

        self.selected_video_var = tk.StringVar()
        video_options = [f"{v[1][:50]}... ({v[0]})" for v in videos]

        video_dropdown = ttk.Combobox(select_frame, textvariable=self.selected_video_var,
                                     values=video_options, state='readonly',
                                     font=('Segoe UI', 10), width=60)
        video_dropdown.pack(fill=tk.X, pady=(0, 10))
        if video_options:
            video_dropdown.current(0)

        # Opzioni
        options_frame = tk.Frame(select_frame, bg=self.frame_color)
        options_frame.pack(fill=tk.X)

        tk.Label(options_frame, text="Intervallo (secondi):",
                bg=self.frame_color, fg=self.fg_color,
                font=('Segoe UI', 9)).pack(side=tk.LEFT, padx=(0, 10))

        self.interval_var = tk.StringVar(value="30")
        interval_entry = tk.Entry(options_frame, textvariable=self.interval_var,
                                 width=10, font=('Segoe UI', 9),
                                 bg=self.bg_color, fg=self.fg_color,
                                 relief=tk.FLAT, bd=2)
        interval_entry.pack(side=tk.LEFT, padx=(0, 20))

        generate_btn = tk.Button(options_frame, text="📸 Genera Screenshot",
                                command=self.generate_visual_summary,
                                bg=self.button_color, fg='#1e1e2e',
                                font=('Segoe UI', 10, 'bold'),
                                relief=tk.FLAT, bd=0, padx=20, pady=8,
                                cursor='hand2')
        generate_btn.pack(side=tk.LEFT)

        # Area screenshots
        screenshots_frame = ttk.Frame(self.content_area, style='Custom.TFrame')
        screenshots_frame.pack(fill=tk.BOTH, expand=True)

        canvas = tk.Canvas(screenshots_frame, bg=self.bg_color, highlightthickness=0)
        scrollbar = ttk.Scrollbar(screenshots_frame, orient="vertical", command=canvas.yview)
        self.screenshots_container = ttk.Frame(canvas, style='Custom.TFrame')

        self.screenshots_container.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=self.screenshots_container, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Carica screenshot esistenti se disponibili
        if video_options:
            selected = video_dropdown.get()
            video_id = selected.split('(')[-1].strip(')')
            self.display_existing_screenshots(video_id)

    def display_existing_screenshots(self, video_id):
        """Mostra screenshot esistenti per un video"""
        for widget in self.screenshots_container.winfo_children():
            widget.destroy()

        screenshots = self.db.get_video_screenshots(video_id)

        if not screenshots:
            no_screenshots = ttk.Label(self.screenshots_container,
                                      text="📭 Nessuno screenshot disponibile.\nGenera screenshot per questo video!",
                                      style='Custom.TLabel',
                                      font=('Segoe UI', 11),
                                      justify=tk.CENTER)
            no_screenshots.pack(pady=50)
            return

        # Griglia screenshot
        row_frame = None
        for idx, (timestamp, path) in enumerate(screenshots):
            if idx % 3 == 0:
                row_frame = tk.Frame(self.screenshots_container, bg=self.bg_color)
                row_frame.pack(fill=tk.X, pady=10)

            if os.path.exists(path):
                self.create_screenshot_card(row_frame, timestamp, path)

    def create_screenshot_card(self, parent, timestamp, path):
        """Crea una card per uno screenshot"""
        card = tk.Frame(parent, bg=self.frame_color, relief=tk.RAISED, bd=1)
        card.pack(side=tk.LEFT, padx=10)

        try:
            img = Image.open(path)
            img = img.resize((300, 200), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(img)
            self.image_cache[path] = photo

            img_label = tk.Label(card, image=photo, bg=self.frame_color)
            img_label.pack(padx=5, pady=5)

            # Timestamp
            minutes = int(timestamp // 60)
            seconds = int(timestamp % 60)
            time_label = tk.Label(card, text=f"⏱️ {minutes:02d}:{seconds:02d}",
                                 bg=self.frame_color, fg=self.accent_color,
                                 font=('Segoe UI', 9, 'bold'))
            time_label.pack(pady=(0, 5))
        except:
            pass

    def generate_visual_summary(self):
        """Genera screenshot per il video selezionato"""
        selected = self.selected_video_var.get()
        if not selected:
            messagebox.showwarning("Attenzione", "Seleziona un video!")
            return

        video_id = selected.split('(')[-1].strip(')')
        videos = self.db.get_all_videos()
        video_data = next((v for v in videos if v[0] == video_id), None)

        if not video_data or not video_data[4]:
            messagebox.showerror("Errore", "File video non trovato!")
            return

        file_path = video_data[4]
        interval = int(self.interval_var.get())

        # Genera in thread separato
        thread = threading.Thread(
            target=self.extract_screenshots_thread,
            args=(video_id, file_path, interval),
            daemon=True
        )
        thread.start()

        messagebox.showinfo("Avviato", "Generazione screenshot avviata!\nAttendere...")

    def extract_screenshots_thread(self, video_id, video_path, interval):
        """Estrae screenshot dal video usando ffmpeg"""
        try:
            # Directory per screenshot
            screenshots_dir = Path(self.download_path.get()) / "screenshots" / video_id
            screenshots_dir.mkdir(parents=True, exist_ok=True)

            # Ottieni durata video
            probe_cmd = [
                'ffprobe', '-v', 'error', '-show_entries',
                'format=duration', '-of',
                'default=noprint_wrappers=1:nokey=1',
                video_path
            ]

            duration_output = subprocess.check_output(probe_cmd, stderr=subprocess.STDOUT)
            duration = float(duration_output.strip())

            # Genera screenshot
            timestamps = []
            current = 0
            while current < duration:
                timestamp = current
                output_path = screenshots_dir / f"screenshot_{int(timestamp)}.jpg"

                # Estrai frame
                cmd = [
                    'ffmpeg', '-ss', str(timestamp), '-i', video_path,
                    '-vframes', '1', '-q:v', '2',
                    str(output_path), '-y'
                ]

                subprocess.run(cmd, capture_output=True, check=True)

                # Salva nel database
                self.db.add_screenshot(video_id, timestamp, str(output_path))
                timestamps.append((timestamp, str(output_path)))

                current += interval

            # Aggiorna UI
            self.root.after(0, lambda: self.display_existing_screenshots(video_id))
            self.root.after(0, lambda: messagebox.showinfo(
                "Completato",
                f"Generati {len(timestamps)} screenshot!"
            ))

        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror(
                "Errore",
                f"Errore generazione screenshot:\n{str(e)}"
            ))

    def show_settings_section(self):
        """Mostra la sezione impostazioni"""
        title = ttk.Label(self.content_area,
                         text="⚙️ Impostazioni",
                         style='SectionTitle.TLabel')
        title.pack(pady=(0, 20))

        # Info database
        info_frame = ttk.Frame(self.content_area, style='Card.TFrame', padding="20")
        info_frame.pack(fill=tk.X, pady=(0, 15))

        ttk.Label(info_frame, text="📊 Statistiche Database",
                 style='Card.TLabel',
                 font=('Segoe UI', 12, 'bold')).pack(anchor=tk.W, pady=(0, 15))

        videos = self.db.get_all_videos()
        stats_text = f"""
        📹 Video nel database: {len(videos)}
        📁 Percorso database: {Path.home() / 'Downloads' / 'YouTube' / 'youtube_library.db'}
        💾 Directory download: {self.download_path.get()}
        """

        stats_label = tk.Label(info_frame, text=stats_text,
                              bg=self.frame_color, fg=self.fg_color,
                              font=('Segoe UI', 10), justify=tk.LEFT)
        stats_label.pack(anchor=tk.W)

        # About
        about_frame = ttk.Frame(self.content_area, style='Card.TFrame', padding="20")
        about_frame.pack(fill=tk.X)

        ttk.Label(about_frame, text="ℹ️ Informazioni",
                 style='Card.TLabel',
                 font=('Segoe UI', 12, 'bold')).pack(anchor=tk.W, pady=(0, 15))

        about_text = """
        YouTube Downloader Premium v2.1.2

        Funzionalità:
        • Download video, audio e sottotitoli
        • Knowledge Base con ricerca full-text
        • Visual Summary Generator
        • Database SQLite integrato
        • Fix HD: Download in 720p/1080p funzionante

        Creato con ❤️ da Claude Code per Gimmy
        """

        about_label = tk.Label(about_frame, text=about_text,
                              bg=self.frame_color, fg=self.fg_color,
                              font=('Segoe UI', 10), justify=tk.LEFT)
        about_label.pack(anchor=tk.W)

    # Metodi helper e download (mantengono logica originale)

    def browse_directory(self):
        """Apri dialog per selezionare directory"""
        directory = filedialog.askdirectory(initialdir=self.download_path.get())
        if directory:
            self.download_path.set(directory)
            self.log(f"📁 Directory cambiata: {directory}", 'info')

    def log(self, message, tag='info'):
        """Aggiungi messaggio al log"""
        if hasattr(self, 'log_text'):
            timestamp = datetime.now().strftime("%H:%M:%S")
            self.log_text.insert(tk.END, f"[{timestamp}] {message}\n", tag)
            self.log_text.see(tk.END)
            self.root.update_idletasks()

    def copy_log_to_clipboard(self):
        """Copia tutto il contenuto del log nella clipboard"""
        if hasattr(self, 'log_text'):
            log_content = self.log_text.get("1.0", tk.END)
            self.root.clipboard_clear()
            self.root.clipboard_append(log_content)
            self.root.update()
            messagebox.showinfo("Copiato", "Log copiato nella clipboard!")

    def strip_ansi_codes(self, text):
        """Rimuove tutti i codici ANSI di escape dal testo"""
        ansi_escape = re.compile(r'\x1b\[[0-9;]*m')
        return ansi_escape.sub('', text)

    def progress_hook(self, d):
        """Hook per aggiornare la progress bar"""
        if d['status'] == 'downloading':
            try:
                percent_str = self.strip_ansi_codes(d.get('_percent_str', '0%').strip())
                percent = float(percent_str.replace('%', ''))

                self.progress_var.set(percent)

                downloaded = self.strip_ansi_codes(d.get('_downloaded_bytes_str', 'N/A'))
                total = self.strip_ansi_codes(d.get('_total_bytes_str', 'N/A'))
                speed = self.strip_ansi_codes(d.get('_speed_str', 'N/A'))
                eta = self.strip_ansi_codes(d.get('_eta_str', 'N/A'))

                status = f"⬇️ {percent:.1f}% - {downloaded}/{total} - {speed} - ETA: {eta}"
                self.status_label.config(text=status)
            except:
                pass
        elif d['status'] == 'finished':
            self.progress_var.set(100)
            self.status_label.config(text="✅ Download completato!")

    def download_video(self):
        """Funzione per scaricare il video - USA SUBPROCESS per supporto HD"""
        url = self.url_var.get().strip()

        if not url:
            self.log("❌ ERRORE: Inserisci un URL valido!", 'error')
            messagebox.showerror("Errore", "Inserisci un URL valido!")
            self.is_downloading = False
            self.download_btn.config(state=tk.NORMAL, text="⬇️ SCARICA VIDEO")
            return

        output_path = self.download_path.get()
        os.makedirs(output_path, exist_ok=True)

        # Costruiamo il comando yt-dlp con --remote-components per HD
        # Questo è l'UNICO modo per ottenere formati HD con YouTube moderno
        cmd = [
            'yt-dlp',
            '--remote-components', 'ejs:github',  # Challenge solver per HD
            '--newline',  # Progress su righe separate
            '-o', os.path.join(output_path, '%(title)s.%(ext)s'),
            '--write-thumbnail',  # Download thumbnail
        ]

        # Formato
        if self.format_var.get() == 'audio':
            cmd.extend(['-f', 'bestaudio/best'])
            cmd.extend(['-x', '--audio-format', 'mp3', '--audio-quality', '192K'])
            self.log("🎵 Modalità: Solo Audio (MP3)", 'info')
        elif self.format_var.get() == 'subtitles':
            cmd.extend(['--skip-download', '--write-subs', '--write-auto-subs'])
            cmd.extend(['--sub-langs', 'it,en,es,fr,de,pt,ru,ja,ko,zh-Hans,zh-Hant,ar'])
            cmd.extend(['--sub-format', 'srt/vtt/best'])
            self.log("📝 Modalità: Solo Sottotitoli", 'info')
        else:
            quality = self.quality_var.get()
            if quality == 'best':
                format_string = 'bestvideo+bestaudio/best'
            else:
                format_string = f'bestvideo[height<={quality}]+bestaudio/bestvideo+bestaudio/best'

            cmd.extend(['-f', format_string])
            cmd.extend(['--merge-output-format', 'mp4'])
            self.log(f"🎬 Modalità: Video - Qualità: {quality}", 'info')

        # Sottotitoli per Knowledge Base
        if self.subtitles_var.get() and self.format_var.get() != 'subtitles':
            cmd.extend(['--write-subs', '--write-auto-subs', '--sub-langs', 'it,en'])
            cmd.append('--ignore-errors')  # Continua se sottotitoli falliscono
            self.log("🧠 Knowledge Base: Abilitato (sottotitoli opzionali)", 'info')

        # Playlist
        if self.playlist_var.get():
            cmd.append('--yes-playlist')
            self.log("📑 Modalità Playlist: Attiva", 'info')
        else:
            cmd.append('--no-playlist')

        # Aggiungi URL
        cmd.append(url)

        try:
            self.log(f"🔗 URL: {url}", 'info')
            self.log("🚀 Inizio download con challenge solver HD...", 'info')
            self.log(f"🔧 Comando: yt-dlp --remote-components ejs:github ...", 'info')

            # Esegui yt-dlp come subprocess
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
                encoding='utf-8',
                errors='replace'
            )

            # Leggi output per progress
            for line in process.stdout:
                line = line.strip()
                if line:
                    self.log(line, 'info')

                    # Parse progress
                    if '[download]' in line and '%' in line:
                        try:
                            # Cerca pattern "X.X%"
                            match = re.search(r'(\d+\.?\d*)%', line)
                            if match:
                                percent = float(match.group(1))
                                self.progress_var.set(percent)
                                self.status_label.config(text=f"⬇️ Download: {percent:.1f}%")
                                self.root.update_idletasks()
                        except:
                            pass

            process.wait()

            if process.returncode == 0:
                self.log("✅ DOWNLOAD COMPLETATO!", 'success')
                self.status_label.config(text="✅ Download completato!")
                self.progress_var.set(100)

                # Salva nel database se richiesto
                if self.subtitles_var.get():
                    self.log("💾 Salvataggio nel database...", 'info')
                    # Usa yt-dlp API solo per ottenere info (senza download)
                    try:
                        with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
                            info = ydl.extract_info(url, download=False)
                            if info:
                                if 'entries' in info:
                                    for video_info in info['entries']:
                                        if video_info:
                                            self.save_to_database(video_info, output_path)
                                else:
                                    self.save_to_database(info, output_path)
                    except Exception as e:
                        self.log(f"⚠️ Errore salvataggio database: {e}", 'error')

                messagebox.showinfo("Successo", f"Download completato!\n\nFile in: {output_path}")
            else:
                raise Exception(f"yt-dlp terminato con errore (code {process.returncode})")

        except Exception as e:
            error_msg = str(e)
            self.log(f"❌ ERRORE: {error_msg}", 'error')
            self.status_label.config(text="❌ Errore durante il download")
            self.progress_var.set(0)
            messagebox.showerror("Errore", f"Errore:\n\n{error_msg}")

        finally:
            self.is_downloading = False
            self.download_btn.config(state=tk.NORMAL, text="⬇️ SCARICA VIDEO")

    def save_to_database(self, video_info, output_path):
        """Salva video e trascrizioni nel database"""
        try:
            video_id = video_info.get('id')

            # Trova file scaricato
            file_path = None
            for ext in ['mp4', 'webm', 'mkv', 'mp3']:
                potential_path = os.path.join(output_path, f"{video_info.get('title')}.{ext}")
                if os.path.exists(potential_path):
                    file_path = potential_path
                    break

            # Trova thumbnail
            thumb_path = None
            for ext in ['jpg', 'png', 'webp']:
                potential_thumb = os.path.join(output_path, f"{video_info.get('title')}.{ext}")
                if os.path.exists(potential_thumb):
                    thumb_path = potential_thumb
                    break

            # File size
            file_size = os.path.getsize(file_path) if file_path and os.path.exists(file_path) else 0

            # Salva video
            video_data = {
                'id': video_id,
                'title': video_info.get('title'),
                'uploader': video_info.get('uploader'),
                'duration': video_info.get('duration'),
                'upload_date': video_info.get('upload_date'),
                'description': video_info.get('description', '')[:500],  # Primi 500 char
                'thumbnail_path': thumb_path,
                'file_path': file_path,
                'file_size': file_size,
                'format': self.format_var.get()
            }

            self.db.add_video(video_data)
            self.log(f"💾 Video salvato nel database: {video_id}", 'success')

            # Trova e salva sottotitoli (opzionale - può fallire)
            subtitles_found = False
            try:
                for lang in ['it', 'en']:
                    for ext in ['srt', 'vtt']:
                        sub_path = os.path.join(output_path, f"{video_info.get('title')}.{lang}.{ext}")
                        if os.path.exists(sub_path):
                            try:
                                with open(sub_path, 'r', encoding='utf-8') as f:
                                    sub_text = f.read()
                                    # Rimuovi timestamp e formattazione
                                    clean_text = re.sub(r'\d{2}:\d{2}:\d{2}[.,]\d{3}\s*-->\s*\d{2}:\d{2}:\d{2}[.,]\d{3}', '', sub_text)
                                    clean_text = re.sub(r'\d+\n', '', clean_text)
                                    clean_text = ' '.join(clean_text.split())

                                    self.db.add_transcript(video_id, lang, clean_text)
                                    self.log(f"📝 Trascrizione salvata: {lang}", 'success')
                                    subtitles_found = True
                            except Exception as e:
                                self.log(f"⚠️ Errore lettura sottotitolo {lang}: {e}", 'error')

                if not subtitles_found and self.subtitles_var.get():
                    self.log("⚠️ Nessun sottotitolo trovato (possibile errore 429 o non disponibili)", 'error')
                    self.log("💡 Video salvato comunque - ricerca Knowledge Base limitata", 'info')
            except Exception as e:
                self.log(f"⚠️ Errore processing sottotitoli: {e}", 'error')

            # Genera Visual Summary se richiesto
            if self.auto_summary_var.get() and file_path and self.format_var.get() == 'video':
                self.log("📸 Generazione Visual Summary in background...", 'info')
                thread = threading.Thread(
                    target=self.extract_screenshots_thread,
                    args=(video_id, file_path, 30),
                    daemon=True
                )
                thread.start()

        except Exception as e:
            self.log(f"⚠️ Errore salvataggio database: {e}", 'error')

    def start_download(self):
        """Avvia il download in un thread separato"""
        if self.is_downloading:
            return

        self.is_downloading = True
        self.download_btn.config(state=tk.DISABLED, text="⏳ Download...")
        self.progress_var.set(0)

        thread = threading.Thread(target=self.download_video, daemon=True)
        thread.start()

    def open_file(self, file_path):
        """Apri file con applicazione predefinita"""
        try:
            if sys.platform == 'win32':
                os.startfile(file_path)
            elif sys.platform == 'darwin':
                subprocess.run(['open', file_path])
            else:
                subprocess.run(['xdg-open', file_path])
        except Exception as e:
            messagebox.showerror("Errore", f"Impossibile aprire il file:\n{e}")

    def open_folder(self, file_path):
        """Apri la cartella contenente il file"""
        try:
            if file_path and os.path.exists(file_path):
                folder = os.path.dirname(file_path)
            else:
                folder = self.download_path.get()

            if sys.platform == 'win32':
                os.startfile(folder)
            elif sys.platform == 'darwin':
                subprocess.run(['open', folder])
            else:
                subprocess.run(['xdg-open', folder])
        except Exception as e:
            messagebox.showerror("Errore", f"Impossibile aprire la cartella:\n{e}")


def main():
    """Funzione principale"""
    root = tk.Tk()
    app = YouTubeDownloaderGUI(root)

    # Centra finestra
    root.update_idletasks()
    width = 1200
    height = 800
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')

    root.mainloop()


if __name__ == "__main__":
    main()
