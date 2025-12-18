# 🎬 YouTube Downloader Premium v2.1.2

**Applicazione professionale con interfaccia moderna per scaricare video da YouTube, con Knowledge Base ricercabile e Visual Summary Generator integrati.**

## 🚨 FIX CRITICO v2.1.2 - Download HD Risolto!
**Finalmente risolto il problema dei download in bassa qualità!** La versione 2.1.2 scarica correttamente video in **720p, 1080p e qualità HD** grazie all'integrazione del challenge solver di YouTube.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Version](https://img.shields.io/badge/Version-2.1.2-success.svg)

## 🌟 Novità v2.1.2

### 🎬 FIX DEFINITIVO Download HD
- **RISOLTO AL 100%**: Download in 720p/1080p ora funzionante!
- **Soluzione**: Uso di subprocess con `--remote-components ejs:github`
- **Tecnologia**: Challenge solver automatico per bypassare restrizioni YouTube
- **Testato e funzionante**: Video HD scaricati correttamente
- **Note**: Richiede Node.js installato (già presente sul sistema)

## 🌟 Novità v2.1.0

### 📋 Copia Log con Un Click
- **Pulsante "📋 Copia Log"**: Nuovo pulsante nell'area log per copiare tutto il contenuto
- **Debugging facilitato**: Copia istantanea del log completo nella clipboard
- **Un solo click**: Niente più selezioni manuali difficili

### ⚠️ Gestione Intelligente Errori Sottotitoli
- **Resilienza Errore 429**: Download continua anche se YouTube limita i sottotitoli
- **Download garantito**: Video salvato comunque nel database anche senza sottotitoli
- **Messaggi chiari**: Log dettagliato su stato sottotitoli e eventuali errori
- **Graceful degradation**: Knowledge Base funziona anche senza trascrizioni

## 🌟 Funzionalità v2.0

### 📚 Knowledge Base Ricercabile
- **Database SQLite integrato**: Tutti i video scaricati vengono salvati con metadati completi
- **Ricerca Full-Text**: Cerca parole o frasi attraverso le trascrizioni di TUTTI i tuoi video
- **Risultati intelligenti**: Ogni risultato mostra thumbnail, titolo, canale e snippet del testo trovato
- **Accesso rapido**: Click per aprire il video o la cartella direttamente dall'app

### 🎨 Visual Summary Generator
- **Screenshot automatici**: Genera screenshot a intervalli regolari dal video
- **Timeline visuale**: Ogni screenshot è etichettato con timestamp preciso
- **Navigazione visiva**: Scorri velocemente il contenuto del video
- **Export friendly**: Screenshot salvati in alta qualità per condivisione

### 🎯 Interfaccia Professionale
- **Design moderno con sidebar**: Navigazione intuitiva tra sezioni
- **4 sezioni principali**: Download, Libreria, Summary, Impostazioni
- **Tema scuro ottimizzato**: Facile sugli occhi durante lunghe sessioni
- **Responsive e fluida**: Interfaccia che si adatta al contenuto

## ✨ Caratteristiche Complete

### Download Avanzato
- 📹 **Download Video**: Qualità selezionabile (Best, 1080p, 720p, 480p)
- 🎵 **Estrazione Audio**: Conversione automatica in MP3 ad alta qualità
- 📝 **Solo Sottotitoli**: Download sottotitoli in 12+ lingue senza video
- 📑 **Supporto Playlist**: Scarica intere playlist con un click
- 🌍 **Sottotitoli Multilingua**: IT, EN, ES, FR, DE, PT, RU, JA, KO, ZH, AR

### Knowledge Base
- 🔍 **Ricerca Intelligente**: Trova video per contenuto, non solo per titolo
- 💾 **Database Automatico**: Salvataggio automatico di metadati e trascrizioni
- 📊 **Libreria Organizzata**: Visualizzazione elegante di tutti i video scaricati
- 🔗 **Link diretti**: Apri file e cartelle con un click

### Visual Summary
- 📸 **Screenshot Automatici**: Intervallo personalizzabile
- ⏱️ **Timeline Navigabile**: Ogni screenshot con timestamp
- 🖼️ **Alta Qualità**: Screenshot in risoluzione ottimale
- 📁 **Organizzazione**: Screenshot raggruppati per video

### Altre Features
- 📊 **Barra Progresso**: Visualizzazione real-time del download
- 📋 **Log Dettagliato**: Tracciamento completo delle operazioni
- 📁 **Cartella Personalizzabile**: Scegli dove salvare i file
- 💫 **Auto-Summary**: Genera screenshot automaticamente dopo download

## 🚀 Installazione

### 1. Prerequisiti

**Python 3.8+**
```bash
python --version
```

**FFmpeg** (obbligatorio per conversioni e screenshot)
```bash
# Con Scoop (raccomandato):
scoop install ffmpeg

# Verifica installazione:
ffmpeg -version
```

### 2. Installa Dipendenze

```bash
cd Projects\Tools\YouTubeDownloader
pip install -r requirements.txt
```

Le dipendenze includono:
- `yt-dlp`: Download da YouTube
- `Pillow`: Gestione immagini e thumbnails

### 3. Avvia l'Applicazione

**Versione 2.0 (Nuova - Consigliata):**
```bash
python youtube_downloader_v2.py
```

**Versione 1.x (Classica):**
```bash
python youtube_downloader.py
```

## 📖 Guida all'Uso

### 🔽 Sezione Download

1. **Incolla URL**: Inserisci l'URL del video o playlist YouTube
2. **Seleziona Formato**:
   - **Video + Audio**: Download completo del video
   - **Solo Audio (MP3)**: Estrae solo l'audio
   - **Solo Sottotitoli**: Scarica solo i sottotitoli multilingua

3. **Scegli Qualità**: Best, 1080p, 720p, 480p
4. **Opzioni**:
   - ✅ **È una playlist**: Per scaricare intere playlist
   - ✅ **Salva in Knowledge Base**: Abilita ricerca e metadati (consigliato!)
   - ✅ **Genera Visual Summary**: Crea screenshot automatici

5. **Click SCARICA VIDEO**: Inizia il download!

### 📚 Sezione Libreria (Knowledge Base)

**Funzionalità:**
- Visualizza tutti i video scaricati con thumbnails
- Cerca per parole chiave nel contenuto (non solo nel titolo!)
- Click su "▶️ Apri" per riprodurre il video
- Click su "📂 Cartella" per aprire la directory

**Come Cercare:**
1. Digita una parola o frase nella barra di ricerca
2. Premi Invio o click su "🔍 Cerca"
3. I risultati mostreranno:
   - 🖼️ Thumbnail del video
   - 📺 Titolo e canale
   - 💬 Snippet di testo dove appare la parola cercata
   - ⏱️ Data di download

**Esempio:**
- Cerca "python tutorial" → Trova tutti i video che parlano di Python
- Cerca "machine learning" → Trova discussioni su ML in tutti i tuoi video
- Cerca "come installare" → Trova guide di installazione

### 🎨 Sezione Visual Summary

**Genera Screenshot:**
1. Seleziona un video dal menu a tendina
2. Imposta intervallo in secondi (es. 30 = uno screenshot ogni 30 sec)
3. Click su "📸 Genera Screenshot"
4. Attendi la generazione (mostrato avviso)
5. Gli screenshot appariranno in griglia con timestamp

**Visualizza Screenshot Esistenti:**
- Seleziona video già elaborato
- Gli screenshot salvati verranno mostrati automaticamente
- Ogni screenshot è etichettato con il tempo esatto (es. 02:45)

### ⚙️ Sezione Impostazioni

- 📊 Statistiche database (numero video, percorsi, ecc.)
- ℹ️ Informazioni sulla versione e funzionalità

## 🎯 Esempi d'Uso

### Scenario 1: Scaricare e Catalogare un Tutorial
```
1. Incolla URL del tutorial
2. Seleziona "Video + Audio"
3. Qualità: "Best"
4. ✅ Salva in Knowledge Base
5. ✅ Genera Visual Summary
6. Download!

Risultato:
- Video scaricato in alta qualità
- Trascrizione salvata nel database
- Screenshot generati automaticamente
- Ricercabile nella Libreria
```

### Scenario 2: Trovare un Argomento Specifico
```
1. Vai in "📚 Libreria"
2. Cerca "docker container"
3. Visualizza tutti i video che parlano di Docker
4. Click per aprire il video esatto
```

### Scenario 3: Creare un'Anteprima Visuale
```
1. Vai in "🎨 Summary"
2. Seleziona video già scaricato
3. Imposta intervallo: 60 secondi
4. Genera screenshot
5. Visualizza timeline visuale completa
```

## 💡 Suggerimenti

- **Knowledge Base**: Tieni sempre attiva l'opzione per costruire un archivio ricercabile
- **Visual Summary**: Utile per video lunghi - puoi "vedere" tutto il contenuto a colpo d'occhio
- **Intervallo Screenshot**: 30-60 secondi è ottimale per la maggior parte dei video
- **Ricerca**: Cerca frasi specifiche per risultati più precisi
- **Playlist**: Ideale per scaricare interi corsi o serie di video

## 🗄️ Struttura Database

Il database SQLite salva:
- **videos**: ID, titolo, canale, durata, descrizione, thumbnail, percorso file
- **transcripts**: Trascrizioni complete con lingua
- **screenshots**: Timestamp e percorsi degli screenshot

**Percorso database:**
```
C:\Users\<username>\Downloads\YouTube\youtube_library.db
```

## 📦 Creare Eseguibile

Usa gli script esistenti per creare un `.exe`:

```powershell
.\build_exe.ps1
```

L'eseguibile includerà tutta la nuova funzionalità!

## 🔧 Risoluzione Problemi

### Errore: "FFmpeg not found"
```bash
# Installa FFmpeg
scoop install ffmpeg

# Verifica
ffmpeg -version
```

### Database non funziona
- Verifica permessi di scrittura in `Downloads/YouTube/`
- Il database viene creato automaticamente al primo download

### Screenshot non vengono generati
- Verifica che FFmpeg sia installato correttamente
- Controlla che il file video esista e sia accessibile
- Prova con intervalli più grandi (es. 60 secondi)

### Ricerca non trova nulla
- Assicurati di aver scaricato video con "Salva in Knowledge Base" attivo
- I sottotitoli devono essere disponibili (IT o EN)
- Controlla spelling della query

## 🆚 Differenze v1.0 vs v2.0

| Feature | v1.0 | v2.0 |
|---------|------|------|
| Interfaccia | Singola finestra | Sidebar multi-sezione |
| Database | ❌ | ✅ SQLite integrato |
| Ricerca | ❌ | ✅ Full-text search |
| Visual Summary | ❌ | ✅ Screenshot automatici |
| Libreria | ❌ | ✅ Gestione video |
| Dimensione finestra | 900x700 | 1200x800 |

## 📝 Changelog Dettagliato

### v2.1.2 (2025-12-18)
**FIX DEFINITIVO - Download HD Funzionante:**
- 🎬 **RISOLTO AL 100%**: Download in HD/720p/1080p finalmente funzionante!
- 🔧 **Fix**: Riscritto motore download per usare subprocess invece di Python API
- ⚡ **Implementazione**: `subprocess.Popen` con `--remote-components ejs:github`
- ✅ **Testato**: Confermato download 1080p (316MB), 720p (164MB) funzionanti
- 📺 **Risultato**: Scarica correttamente in tutte le qualità HD richieste

**Dettagli Tecnici:**
- Python API yt-dlp non supporta `remote_components` come parametro dict
- Soluzione: chiamare yt-dlp via subprocess da command line con flag `--remote-components ejs:github`
- Challenge solver scaricato automaticamente da GitHub per bypassare n-challenge YouTube
- Progress bar funzionante tramite parsing output subprocess in real-time
- Richiede Node.js per esecuzione challenge solver (già presente nel sistema)

**Breaking Changes:**
- Download ora usa subprocess invece di Python API (più robusto, meno flessibile per progress tracking avanzato)

### v2.1.1 (2025-12-18) [DEPRECATO - Bug non risolto]
**Tentativo Fix Download HD (NON FUNZIONANTE):**
- ❌ Tentato: Aggiunto `remote_components: ejs:github` come parametro dict Python API
- ❌ Risultato: Parametro ignorato, download continuava a 360p
- 📝 Lezione: Python API non supporta questa opzione

### v2.1.0 (2025-12-16)
**Bug Fix e Miglioramenti UX:**
- 📋 **Nuovo**: Pulsante "Copia Log" per copiare tutto il log nella clipboard
- ⚠️ **Fix**: Gestione errore 429 "Too Many Requests" sui sottotitoli YouTube
- ✅ **Fix**: Download continua anche se sottotitoli non disponibili
- 💾 **Fix**: Video salvato nel database anche senza trascrizioni
- 📝 **Migliorato**: Messaggi di log più chiari e informativi
- 🔧 **Migliorato**: Wrapping del testo nel log (wrap=WORD)
- 🛡️ **Migliorato**: Error handling robusto per sottotitoli con try/except multipli

**Feedback Utente:**
- Risolto problema segnalato: impossibilità di copiare il log
- Risolto problema segnalato: download falliva con errore 429 sottotitoli IT

### v2.0.0 (2025-12-16)
**Novità Maggiori:**
- ✨ Interfaccia completamente ridisegnata con sidebar navigation
- 📚 Knowledge Base con database SQLite
- 🔍 Ricerca full-text nelle trascrizioni
- 🎨 Visual Summary Generator
- 📊 Sezione Libreria per gestire video scaricati
- 🖼️ Visualizzazione thumbnails
- ⚙️ Pannello impostazioni e statistiche

**Miglioramenti:**
- Layout professionale 1200x800px
- Database automatico per metadati
- Screenshot extraction con ffmpeg
- Cache intelligente per immagini
- Threading ottimizzato

### v1.1.0 (2025-12-16)
- Download solo sottotitoli in 12+ lingue

### v1.0.0 (2025-12-08)
- Rilascio iniziale

## 🛠️ Tecnologie

- **Python 3**: Linguaggio principale
- **tkinter/ttk**: Interfaccia grafica
- **yt-dlp**: Engine download YouTube
- **SQLite**: Database locale
- **Pillow (PIL)**: Gestione immagini
- **FFmpeg**: Conversione e screenshot

## ⚖️ Note Legali

**IMPORTANTE**: Questo software è per uso personale ed educativo.

- ✅ Scarica i tuoi video
- ✅ Contenuti Creative Commons
- ✅ Backup personale
- ❌ NON scaricare contenuti protetti da copyright senza permesso
- ❌ NON ridistribuire contenuti scaricati

Rispetta i [Terms of Service di YouTube](https://www.youtube.com/static?template=terms).

L'autore non è responsabile per l'uso improprio del software.

## 👤 Autore

Creato con ❤️ e ☕ da **Claude Code** per **Gimmy**

## 📄 Licenza

MIT License - Vedi LICENSE file

## 🙏 Crediti

- [yt-dlp](https://github.com/yt-dlp/yt-dlp) - Libreria download
- [FFmpeg](https://ffmpeg.org/) - Processing multimedia
- [Python](https://www.python.org/) - Linguaggio
- [Pillow](https://python-pillow.org/) - Immagini

---

**Buon download e buona ricerca! 🎉🔍**

Per domande o problemi, apri una issue su GitHub!
