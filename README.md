# 🎬 YouTube Downloader Premium

Applicazione moderna con interfaccia grafica per scaricare video da YouTube in modo facile e completo.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

## ✨ Caratteristiche

- 🎨 **Interfaccia Grafica Moderna**: Design accattivante con tema scuro
- 📹 **Download Video**: Scarica video in diverse qualità (1080p, 720p, 480p, 360p)
- 🎵 **Estrazione Audio**: Converti video in MP3 ad alta qualità
- 📑 **Supporto Playlist**: Scarica intere playlist con un click
- 📝 **Sottotitoli**: Download automatico sottotitoli (IT/EN)
- 📊 **Barra Progresso**: Visualizzazione in tempo reale del download
- 📋 **Log Dettagliato**: Traccia completa delle operazioni
- 📁 **Cartella Personalizzabile**: Scegli dove salvare i tuoi file

## 🚀 Installazione

### 1. Verifica Python

Assicurati di avere Python 3.8 o superiore installato:

```bash
python --version
```

### 2. Installa FFmpeg

FFmpeg è necessario per la conversione audio/video.

**Con Scoop (Raccomandato):**
```bash
scoop install ffmpeg
```

**Oppure manualmente:**
- Scarica da: https://github.com/BtbN/FFmpeg-Builds/releases
- Estrai e aggiungi alla variabile PATH

### 3. Installa le Dipendenze Python

Apri PowerShell nella cartella del progetto e esegui:

```bash
cd Projects\Tools\YouTubeDownloader
pip install -r requirements.txt
```

## 📖 Come Usare

### Avvio dell'Applicazione

```bash
cd Projects\Tools\YouTubeDownloader
python youtube_downloader.py
```

### Interfaccia

1. **URL Video/Playlist**: Incolla l'URL del video o playlist YouTube
2. **Formato**:
   - Video + Audio: Scarica video completo
   - Solo Audio (MP3): Estrae solo l'audio in formato MP3

3. **Qualità**:
   - Migliore disponibile: Massima qualità disponibile
   - 1080p (Full HD): Video Full HD
   - 720p (HD): Video HD
   - 480p: Qualità media
   - 360p: Qualità standard

4. **Opzioni**:
   - Scarica sottotitoli: Include sottotitoli IT/EN se disponibili
   - È una playlist: Abilita per scaricare intere playlist

5. **Cartella di destinazione**: Scegli dove salvare i file (default: `Downloads\YouTube`)

6. **Premi SCARICA VIDEO**: Avvia il download

### Esempi di Uso

#### Scaricare un singolo video in 1080p:
1. Incolla URL del video
2. Seleziona "Video + Audio"
3. Seleziona "1080p (Full HD)"
4. Click su "SCARICA VIDEO"

#### Estrarre audio da un video:
1. Incolla URL del video
2. Seleziona "Solo Audio (MP3)"
3. Click su "SCARICA VIDEO"

#### Scaricare una playlist:
1. Incolla URL della playlist
2. Spunta "È una playlist"
3. Scegli formato e qualità
4. Click su "SCARICA VIDEO"

## 📦 Creare Eseguibile .exe

Puoi trasformare l'applicazione in un file eseguibile `.exe` standalone per distribuirla facilmente senza richiedere Python installato.

### Prerequisiti

1. **Installa PyInstaller**:
   ```bash
   pip install pyinstaller
   ```

2. **Verifica FFmpeg**: Assicurati che FFmpeg sia installato (sarà comunque necessario sul PC di destinazione)

### Metodo 1: Script Automatico (Raccomandato)

Esegui uno dei seguenti script dalla directory del progetto:

**PowerShell:**
```powershell
.\build_exe.ps1
```

**Batch (doppio click):**
```
build_exe.bat
```

Lo script farà automaticamente:
- Verifica delle dipendenze
- Pulizia delle directory precedenti
- Creazione dell'eseguibile con PyInstaller
- Verifica del risultato

### Metodo 2: Comando Manuale

Se preferisci creare l'eseguibile manualmente:

```bash
pyinstaller --clean --noconfirm youtube_downloader.spec
```

Oppure, senza file .spec:

```bash
pyinstaller --onefile --windowed --name "YouTubeDownloader" youtube_downloader.py
```

### Risultato

L'eseguibile sarà creato nella cartella `dist/`:
```
dist/
  └── YouTubeDownloader.exe  (circa 30-50 MB)
```

### Note Importanti

- **FFmpeg richiesto**: L'eseguibile funziona, ma FFmpeg deve comunque essere installato sul PC dove viene eseguito
- **Prima esecuzione lenta**: Il primo avvio potrebbe richiedere qualche secondo
- **Antivirus**: Alcuni antivirus potrebbero segnalare falsi positivi per gli eseguibili PyInstaller
- **Dimensione**: L'exe include Python e tutte le dipendenze, risultando in un file da 30-50 MB

### Distribuzione

Per distribuire l'applicazione:

1. Copia `YouTubeDownloader.exe` dal folder `dist/`
2. Assicurati che FFmpeg sia installato sul PC di destinazione
3. Esegui l'exe con doppio click

**Suggerimento**: Puoi creare un installer con NSIS o Inno Setup per distribuire insieme FFmpeg.

## 🎯 Scorciatoie

Per avviare l'applicazione rapidamente, crea un file batch:

**`YouTubeDownloader.bat`:**
```batch
@echo off
cd /d C:\Users\gimmy\Projects\Tools\YouTubeDownloader
python youtube_downloader.py
```

Salvalo sul Desktop per un accesso rapido!

## 🔧 Risoluzione Problemi

### Errore: "yt-dlp non è installato"
```bash
pip install yt-dlp
```

### Errore: "ffmpeg not found"
- Installa FFmpeg (vedi sezione Installazione)
- Verifica che sia nel PATH: `ffmpeg -version`

### Download lento
- Controlla la tua connessione internet
- YouTube potrebbe limitare la velocità

### Errore durante il download
- Verifica che l'URL sia corretto
- Alcuni video potrebbero avere restrizioni geografiche
- Prova con qualità inferiore

## ⚖️ Note Legali

**IMPORTANTE**: Questo strumento è fornito solo per scopi educativi e di uso personale.

- Rispetta i Terms of Service di YouTube
- Non scaricare contenuti protetti da copyright senza permesso
- Usa YouTube Premium per il download ufficiale supportato da YouTube
- Questo strumento è ideale per:
  - Scaricare i tuoi video
  - Contenuti con licenza Creative Commons
  - Backup personale di contenuti pubblici

L'autore non è responsabile per l'uso improprio di questo software.

## 🛠️ Tecnologie Utilizzate

- **Python 3**: Linguaggio di programmazione
- **tkinter**: Interfaccia grafica
- **yt-dlp**: Libreria per il download da YouTube
- **FFmpeg**: Conversione audio/video

## 📝 Changelog

### v1.0.0 (2025-12-08)
- Rilascio iniziale
- Interfaccia grafica moderna
- Supporto video e audio
- Download playlist
- Sottotitoli
- Barra progresso in tempo reale

## 👤 Autore

Creato con ❤️ da Claude Code per Gimmy

## 📄 Licenza

Questo progetto è rilasciato sotto licenza MIT.

---

**Buon download! 🎉**
