#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
YouTube Downloader GUI
Applicazione moderna per scaricare video da YouTube con interfaccia grafica
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import os
import sys
import threading
from pathlib import Path
import json
from datetime import datetime

try:
    import yt_dlp
except ImportError:
    print("ERRORE: yt-dlp non è installato. Esegui: pip install yt-dlp")
    sys.exit(1)


class YouTubeDownloaderGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🎬 YouTube Downloader Premium")
        self.root.geometry("900x700")
        self.root.resizable(True, True)

        # Colori tema moderno
        self.bg_color = "#1e1e2e"
        self.fg_color = "#cdd6f4"
        self.accent_color = "#89b4fa"
        self.button_color = "#74c7ec"
        self.error_color = "#f38ba8"
        self.success_color = "#a6e3a1"
        self.frame_color = "#313244"

        # Configura stile
        self.setup_styles()

        # Variabili
        self.download_path = tk.StringVar(value=str(Path.home() / "Downloads" / "YouTube"))
        self.url_var = tk.StringVar()
        self.quality_var = tk.StringVar(value="best")
        self.format_var = tk.StringVar(value="video")
        self.subtitles_var = tk.BooleanVar(value=False)
        self.playlist_var = tk.BooleanVar(value=False)
        self.is_downloading = False

        # Crea UI
        self.create_widgets()

        # Crea directory di default se non esiste
        os.makedirs(self.download_path.get(), exist_ok=True)

    def setup_styles(self):
        """Configura gli stili ttk"""
        style = ttk.Style()
        style.theme_use('clam')

        # Configura colori generali
        self.root.configure(bg=self.bg_color)

        # Frame style
        style.configure('Custom.TFrame', background=self.bg_color)
        style.configure('Card.TFrame', background=self.frame_color, relief='raised')

        # Label style
        style.configure('Title.TLabel',
                       background=self.bg_color,
                       foreground=self.accent_color,
                       font=('Segoe UI', 20, 'bold'))
        style.configure('Custom.TLabel',
                       background=self.bg_color,
                       foreground=self.fg_color,
                       font=('Segoe UI', 10))
        style.configure('Card.TLabel',
                       background=self.frame_color,
                       foreground=self.fg_color,
                       font=('Segoe UI', 10))

        # Button style
        style.configure('Accent.TButton',
                       background=self.button_color,
                       foreground='#1e1e2e',
                       font=('Segoe UI', 10, 'bold'),
                       borderwidth=0,
                       focuscolor='none')
        style.map('Accent.TButton',
                 background=[('active', self.accent_color)])

        # Radiobutton style
        style.configure('Custom.TRadiobutton',
                       background=self.frame_color,
                       foreground=self.fg_color,
                       font=('Segoe UI', 9))

        # Checkbutton style
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

    def create_widgets(self):
        """Crea tutti i widget dell'interfaccia"""

        # Container principale
        main_container = ttk.Frame(self.root, style='Custom.TFrame', padding="20")
        main_container.pack(fill=tk.BOTH, expand=True)

        # Titolo
        title_label = ttk.Label(main_container,
                               text="🎬 YouTube Downloader Premium",
                               style='Title.TLabel')
        title_label.pack(pady=(0, 20))

        # Frame URL
        url_frame = ttk.Frame(main_container, style='Card.TFrame', padding="15")
        url_frame.pack(fill=tk.X, pady=(0, 15))

        ttk.Label(url_frame, text="📎 URL Video/Playlist:", style='Card.TLabel').pack(anchor=tk.W)
        url_entry = tk.Entry(url_frame, textvariable=self.url_var,
                            font=('Segoe UI', 10),
                            bg=self.bg_color, fg=self.fg_color,
                            insertbackground=self.fg_color,
                            relief=tk.FLAT, bd=5)
        url_entry.pack(fill=tk.X, pady=(5, 0), ipady=8)

        # Frame Impostazioni
        settings_frame = ttk.Frame(main_container, style='Card.TFrame', padding="15")
        settings_frame.pack(fill=tk.X, pady=(0, 15))

        # Griglia per impostazioni
        settings_grid = ttk.Frame(settings_frame, style='Card.TFrame')
        settings_grid.pack(fill=tk.X)

        # Colonna 1: Formato
        format_frame = ttk.Frame(settings_grid, style='Card.TFrame')
        format_frame.grid(row=0, column=0, sticky='nw', padx=(0, 20))

        ttk.Label(format_frame, text="📹 Formato:", style='Card.TLabel',
                 font=('Segoe UI', 10, 'bold')).pack(anchor=tk.W, pady=(0, 5))

        ttk.Radiobutton(format_frame, text="Video + Audio", variable=self.format_var,
                       value="video", style='Custom.TRadiobutton').pack(anchor=tk.W)
        ttk.Radiobutton(format_frame, text="Solo Audio (MP3)", variable=self.format_var,
                       value="audio", style='Custom.TRadiobutton').pack(anchor=tk.W)

        # Colonna 2: Qualità
        quality_frame = ttk.Frame(settings_grid, style='Card.TFrame')
        quality_frame.grid(row=0, column=1, sticky='nw', padx=(0, 20))

        ttk.Label(quality_frame, text="⚡ Qualità:", style='Card.TLabel',
                 font=('Segoe UI', 10, 'bold')).pack(anchor=tk.W, pady=(0, 5))

        qualities = [
            ("Migliore disponibile", "best"),
            ("1080p (Full HD)", "1080"),
            ("720p (HD)", "720"),
            ("480p", "480"),
            ("360p", "360")
        ]

        for text, value in qualities:
            ttk.Radiobutton(quality_frame, text=text, variable=self.quality_var,
                           value=value, style='Custom.TRadiobutton').pack(anchor=tk.W)

        # Colonna 3: Opzioni
        options_frame = ttk.Frame(settings_grid, style='Card.TFrame')
        options_frame.grid(row=0, column=2, sticky='nw')

        ttk.Label(options_frame, text="⚙️ Opzioni:", style='Card.TLabel',
                 font=('Segoe UI', 10, 'bold')).pack(anchor=tk.W, pady=(0, 5))

        ttk.Checkbutton(options_frame, text="Scarica sottotitoli",
                       variable=self.subtitles_var,
                       style='Custom.TCheckbutton').pack(anchor=tk.W)
        ttk.Checkbutton(options_frame, text="È una playlist",
                       variable=self.playlist_var,
                       style='Custom.TCheckbutton').pack(anchor=tk.W)

        # Frame Directory
        dir_frame = ttk.Frame(main_container, style='Card.TFrame', padding="15")
        dir_frame.pack(fill=tk.X, pady=(0, 15))

        ttk.Label(dir_frame, text="📁 Cartella di destinazione:", style='Card.TLabel').pack(anchor=tk.W)

        dir_input_frame = ttk.Frame(dir_frame, style='Card.TFrame')
        dir_input_frame.pack(fill=tk.X, pady=(5, 0))

        dir_entry = tk.Entry(dir_input_frame, textvariable=self.download_path,
                            font=('Segoe UI', 9),
                            bg=self.bg_color, fg=self.fg_color,
                            insertbackground=self.fg_color,
                            relief=tk.FLAT, bd=5, state='readonly')
        dir_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=5)

        browse_btn = tk.Button(dir_input_frame, text="📂 Sfoglia",
                              command=self.browse_directory,
                              bg=self.frame_color, fg=self.fg_color,
                              font=('Segoe UI', 9, 'bold'),
                              relief=tk.FLAT, bd=0, padx=15, pady=5,
                              cursor='hand2')
        browse_btn.pack(side=tk.LEFT, padx=(10, 0))

        # Pulsante Download
        self.download_btn = tk.Button(main_container, text="⬇️ SCARICA VIDEO",
                                     command=self.start_download,
                                     bg=self.button_color, fg='#1e1e2e',
                                     font=('Segoe UI', 12, 'bold'),
                                     relief=tk.FLAT, bd=0, pady=12,
                                     cursor='hand2')
        self.download_btn.pack(fill=tk.X, pady=(0, 15))

        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress = ttk.Progressbar(main_container, variable=self.progress_var,
                                       style='Custom.Horizontal.TProgressbar',
                                       mode='determinate', maximum=100)
        self.progress.pack(fill=tk.X, pady=(0, 5))

        # Status label
        self.status_label = ttk.Label(main_container, text="Pronto per il download",
                                     style='Custom.TLabel', font=('Segoe UI', 9))
        self.status_label.pack(anchor=tk.W, pady=(0, 10))

        # Frame Log
        log_frame = ttk.Frame(main_container, style='Card.TFrame', padding="15")
        log_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(log_frame, text="📋 Log:", style='Card.TLabel',
                 font=('Segoe UI', 10, 'bold')).pack(anchor=tk.W, pady=(0, 5))

        # Text widget per log
        self.log_text = scrolledtext.ScrolledText(log_frame, height=10,
                                                  bg=self.bg_color, fg=self.fg_color,
                                                  font=('Consolas', 9),
                                                  relief=tk.FLAT, bd=5,
                                                  insertbackground=self.fg_color)
        self.log_text.pack(fill=tk.BOTH, expand=True)

        # Tag per colorare il log
        self.log_text.tag_config('info', foreground=self.accent_color)
        self.log_text.tag_config('success', foreground=self.success_color)
        self.log_text.tag_config('error', foreground=self.error_color)

        self.log("✨ Applicazione avviata con successo!", 'success')
        self.log(f"📁 Directory di default: {self.download_path.get()}", 'info')

    def browse_directory(self):
        """Apri dialog per selezionare directory"""
        directory = filedialog.askdirectory(initialdir=self.download_path.get())
        if directory:
            self.download_path.set(directory)
            self.log(f"📁 Directory cambiata: {directory}", 'info')

    def log(self, message, tag='info'):
        """Aggiungi messaggio al log"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_text.insert(tk.END, f"[{timestamp}] {message}\n", tag)
        self.log_text.see(tk.END)
        self.root.update_idletasks()

    def progress_hook(self, d):
        """Hook per aggiornare la progress bar"""
        if d['status'] == 'downloading':
            try:
                # Rimuovi colori ANSI e caratteri speciali
                percent_str = d.get('_percent_str', '0%').strip()
                percent_str = percent_str.replace('\x1b[0;94m', '').replace('\x1b[0m', '')
                percent = float(percent_str.replace('%', ''))

                self.progress_var.set(percent)

                downloaded = d.get('_downloaded_bytes_str', 'N/A')
                total = d.get('_total_bytes_str', 'N/A')
                speed = d.get('_speed_str', 'N/A')
                eta = d.get('_eta_str', 'N/A')

                status = f"⬇️ Download: {percent:.1f}% - {downloaded}/{total} - Velocità: {speed} - ETA: {eta}"
                self.status_label.config(text=status)
            except:
                pass
        elif d['status'] == 'finished':
            self.progress_var.set(100)
            self.status_label.config(text="✅ Download completato, elaborazione in corso...")

    def download_video(self):
        """Funzione per scaricare il video"""
        url = self.url_var.get().strip()

        if not url:
            self.log("❌ ERRORE: Inserisci un URL valido!", 'error')
            messagebox.showerror("Errore", "Inserisci un URL di YouTube valido!")
            self.is_downloading = False
            self.download_btn.config(state=tk.NORMAL, text="⬇️ SCARICA VIDEO")
            return

        output_path = self.download_path.get()
        os.makedirs(output_path, exist_ok=True)

        # Opzioni base
        ydl_opts = {
            'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
            'progress_hooks': [self.progress_hook],
            'quiet': False,
            'no_warnings': False,
        }

        # Formato
        if self.format_var.get() == 'audio':
            ydl_opts.update({
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
            })
            self.log("🎵 Modalità: Solo Audio (MP3)", 'info')
        else:
            # Qualità video
            quality = self.quality_var.get()
            if quality == 'best':
                format_string = 'bestvideo+bestaudio/best'
            else:
                format_string = f'bestvideo[height<={quality}]+bestaudio/best[height<={quality}]'

            ydl_opts['format'] = format_string
            ydl_opts['merge_output_format'] = 'mp4'
            self.log(f"🎬 Modalità: Video - Qualità: {quality}", 'info')

        # Sottotitoli
        if self.subtitles_var.get():
            ydl_opts.update({
                'writesubtitles': True,
                'writeautomaticsub': True,
                'subtitleslangs': ['it', 'en'],
            })
            self.log("📝 Sottotitoli: Abilitati (IT, EN)", 'info')

        # Playlist
        if self.playlist_var.get():
            ydl_opts['noplaylist'] = False
            self.log("📑 Modalità Playlist: Attiva", 'info')
        else:
            ydl_opts['noplaylist'] = True

        try:
            self.log(f"🔗 URL: {url}", 'info')
            self.log("🚀 Inizio download...", 'info')

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                # Ottieni info
                info = ydl.extract_info(url, download=False)

                if 'entries' in info:
                    # È una playlist
                    video_count = len(info['entries'])
                    self.log(f"📑 Playlist rilevata: {video_count} video", 'info')
                    self.log(f"📺 Titolo playlist: {info.get('title', 'N/A')}", 'info')
                else:
                    # Video singolo
                    self.log(f"📺 Titolo: {info.get('title', 'N/A')}", 'info')
                    self.log(f"⏱️ Durata: {info.get('duration', 0) // 60} minuti", 'info')

                # Download
                ydl.download([url])

            self.log("✅ DOWNLOAD COMPLETATO CON SUCCESSO!", 'success')
            self.log(f"📁 File salvato in: {output_path}", 'success')
            self.status_label.config(text="✅ Download completato con successo!")
            self.progress_var.set(100)

            messagebox.showinfo("Successo", f"Download completato!\n\nFile salvato in:\n{output_path}")

        except Exception as e:
            error_msg = str(e)
            self.log(f"❌ ERRORE: {error_msg}", 'error')
            self.status_label.config(text="❌ Errore durante il download")
            self.progress_var.set(0)
            messagebox.showerror("Errore", f"Errore durante il download:\n\n{error_msg}")

        finally:
            self.is_downloading = False
            self.download_btn.config(state=tk.NORMAL, text="⬇️ SCARICA VIDEO")

    def start_download(self):
        """Avvia il download in un thread separato"""
        if self.is_downloading:
            return

        self.is_downloading = True
        self.download_btn.config(state=tk.DISABLED, text="⏳ Download in corso...")
        self.progress_var.set(0)

        # Avvia download in thread separato
        thread = threading.Thread(target=self.download_video, daemon=True)
        thread.start()


def main():
    """Funzione principale"""
    root = tk.Tk()
    app = YouTubeDownloaderGUI(root)

    # Centra finestra
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')

    root.mainloop()


if __name__ == "__main__":
    main()
