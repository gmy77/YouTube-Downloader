@echo off
REM YouTube Downloader - Avvio Rapido
REM Questo file batch avvia l'applicazione YouTube Downloader

echo.
echo ========================================
echo   YouTube Downloader Premium
echo ========================================
echo.
echo Avvio dell'applicazione...
echo.

cd /d "%~dp0"
python youtube_downloader.py

if errorlevel 1 (
    echo.
    echo ERRORE: Si e' verificato un problema durante l'avvio.
    echo.
    echo Possibili soluzioni:
    echo 1. Verifica che Python sia installato: python --version
    echo 2. Installa le dipendenze: pip install -r requirements.txt
    echo 3. Controlla che FFmpeg sia installato: ffmpeg -version
    echo.
    pause
)
