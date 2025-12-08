# YouTube Downloader - Script di Installazione Automatica
# Questo script installa automaticamente tutte le dipendenze necessarie

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  YouTube Downloader Premium" -ForegroundColor Cyan
Write-Host "  Script di Installazione" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Verifica Python
Write-Host "[1/3] Verifica Python..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "  OK: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "  ERRORE: Python non trovato!" -ForegroundColor Red
    Write-Host "  Installa Python da: https://www.python.org/downloads/" -ForegroundColor Red
    pause
    exit 1
}

# Verifica FFmpeg
Write-Host ""
Write-Host "[2/3] Verifica FFmpeg..." -ForegroundColor Yellow
try {
    $ffmpegVersion = ffmpeg -version 2>&1 | Select-Object -First 1
    Write-Host "  OK: FFmpeg installato" -ForegroundColor Green
} catch {
    Write-Host "  ATTENZIONE: FFmpeg non trovato!" -ForegroundColor Yellow
    Write-Host "  FFmpeg e' necessario per la conversione audio/video." -ForegroundColor Yellow
    Write-Host ""
    $installFFmpeg = Read-Host "  Vuoi installare FFmpeg tramite Scoop? (s/n)"

    if ($installFFmpeg -eq 's' -or $installFFmpeg -eq 'S') {
        # Verifica se Scoop e' installato
        try {
            scoop --version | Out-Null
            Write-Host "  Installazione FFmpeg in corso..." -ForegroundColor Yellow
            scoop install ffmpeg
            Write-Host "  OK: FFmpeg installato con successo!" -ForegroundColor Green
        } catch {
            Write-Host "  ERRORE: Scoop non e' installato!" -ForegroundColor Red
            Write-Host "  Installa Scoop da: https://scoop.sh/" -ForegroundColor Yellow
            Write-Host "  Oppure scarica FFmpeg manualmente da:" -ForegroundColor Yellow
            Write-Host "  https://github.com/BtbN/FFmpeg-Builds/releases" -ForegroundColor Yellow
        }
    } else {
        Write-Host "  Scarica FFmpeg manualmente da:" -ForegroundColor Yellow
        Write-Host "  https://github.com/BtbN/FFmpeg-Builds/releases" -ForegroundColor Yellow
    }
}

# Installa dipendenze Python
Write-Host ""
Write-Host "[3/3] Installazione dipendenze Python..." -ForegroundColor Yellow
Write-Host "  Installazione di yt-dlp..." -ForegroundColor Yellow

try {
    pip install -r requirements.txt
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  OK: Dipendenze installate con successo!" -ForegroundColor Green
    } else {
        throw "Errore durante l'installazione"
    }
} catch {
    Write-Host "  ERRORE: Impossibile installare le dipendenze!" -ForegroundColor Red
    Write-Host "  Prova manualmente: pip install yt-dlp" -ForegroundColor Red
    pause
    exit 1
}

# Verifica installazione
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Verifica Installazione" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

try {
    python -c "import yt_dlp; print('  OK: yt-dlp versione', yt_dlp.version.__version__)" 2>$null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "yt-dlp installato correttamente" -ForegroundColor Green
    }
} catch {
    Write-Host "  ATTENZIONE: Verifica yt-dlp fallita" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Installazione Completata!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Per avviare l'applicazione:" -ForegroundColor Yellow
Write-Host "  1. Doppio click su YouTubeDownloader.bat" -ForegroundColor White
Write-Host "  2. Oppure esegui: python youtube_downloader.py" -ForegroundColor White
Write-Host ""

$avvio = Read-Host "Vuoi avviare l'applicazione ora? (s/n)"
if ($avvio -eq 's' -or $avvio -eq 'S') {
    Write-Host ""
    Write-Host "Avvio in corso..." -ForegroundColor Yellow
    python youtube_downloader.py
}

Write-Host ""
Write-Host "Premi un tasto per uscire..." -ForegroundColor Gray
pause
