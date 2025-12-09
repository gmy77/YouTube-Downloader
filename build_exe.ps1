#!/usr/bin/env pwsh
# -*- coding: utf-8 -*-

<#
.SYNOPSIS
    Script per creare l'eseguibile .exe di YouTube Downloader

.DESCRIPTION
    Questo script automatizza la creazione dell'eseguibile usando PyInstaller.
    Verifica le dipendenze, pulisce le directory di build precedenti e crea l'exe.

.EXAMPLE
    .\build_exe.ps1
    Crea l'eseguibile nella cartella dist/

.NOTES
    Author: YouTube Downloader Project
    Date: 2024
#>

[CmdletBinding()]
param()

# Configurazione
$ErrorActionPreference = "Stop"
$ProgressPreference = "SilentlyContinue"

# Colori per output
function Write-ColorOutput {
    param(
        [string]$Message,
        [ValidateSet('Success', 'Error', 'Warning', 'Info')]
        [string]$Type = 'Info'
    )

    $colors = @{
        'Success' = 'Green'
        'Error' = 'Red'
        'Warning' = 'Yellow'
        'Info' = 'Cyan'
    }

    $icons = @{
        'Success' = '[OK]'
        'Error' = '[ERRORE]'
        'Warning' = '[ATTENZIONE]'
        'Info' = '[INFO]'
    }

    Write-Host "$($icons[$Type]) $Message" -ForegroundColor $colors[$Type]
}

# Banner
Write-Host "`n========================================" -ForegroundColor Magenta
Write-Host "  YouTube Downloader - Build Script" -ForegroundColor Magenta
Write-Host "========================================`n" -ForegroundColor Magenta

# Verifica che siamo nella directory corretta
if (-not (Test-Path "youtube_downloader.py")) {
    Write-ColorOutput "Il file youtube_downloader.py non è stato trovato!" -Type Error
    Write-ColorOutput "Assicurati di eseguire questo script dalla directory del progetto." -Type Error
    exit 1
}

Write-ColorOutput "Controllo dipendenze..." -Type Info

# Verifica Python
try {
    $pythonVersion = python --version 2>&1
    Write-ColorOutput "Python trovato: $pythonVersion" -Type Success
} catch {
    Write-ColorOutput "Python non è installato o non è nel PATH!" -Type Error
    exit 1
}

# Verifica PyInstaller
try {
    $pyinstallerVersion = pyinstaller --version 2>&1
    Write-ColorOutput "PyInstaller trovato: versione $pyinstallerVersion" -Type Success
} catch {
    Write-ColorOutput "PyInstaller non è installato!" -Type Error
    Write-ColorOutput "Installalo con: pip install pyinstaller" -Type Info
    exit 1
}

# Verifica yt-dlp
try {
    python -c "import yt_dlp" 2>&1 | Out-Null
    Write-ColorOutput "yt-dlp trovato" -Type Success
} catch {
    Write-ColorOutput "yt-dlp non è installato!" -Type Error
    Write-ColorOutput "Installalo con: pip install yt-dlp" -Type Info
    exit 1
}

# Avviso FFmpeg
Write-ColorOutput "`nNOTA: FFmpeg deve essere installato nel sistema per la conversione audio/video!" -Type Warning
Write-ColorOutput "Scaricalo da: https://github.com/BtbN/FFmpeg-Builds/releases" -Type Info
Write-ColorOutput "Oppure usa Scoop: scoop install ffmpeg`n" -Type Info

# Pulizia directory precedenti
Write-ColorOutput "Pulizia directory di build precedenti..." -Type Info

$dirsToClean = @("build", "dist")
foreach ($dir in $dirsToClean) {
    if (Test-Path $dir) {
        Remove-Item -Path $dir -Recurse -Force
        Write-ColorOutput "  Rimossa directory: $dir" -Type Success
    }
}

# Rimuovi file .spec se non esiste, o usalo se esiste
$specFile = "youtube_downloader.spec"
if (-not (Test-Path $specFile)) {
    Write-ColorOutput "File .spec non trovato, verrà generato automaticamente." -Type Warning
}

# Build con PyInstaller
Write-ColorOutput "`nAvvio build dell'eseguibile..." -Type Info
Write-Host "`n--- Output PyInstaller ---" -ForegroundColor DarkGray

try {
    if (Test-Path $specFile) {
        # Usa il file .spec personalizzato
        pyinstaller --clean --noconfirm $specFile
    } else {
        # Genera automaticamente
        pyinstaller --clean --noconfirm `
            --onefile `
            --windowed `
            --name "YouTubeDownloader" `
            --add-data "requirements.txt;." `
            --hidden-import=tkinter `
            --hidden-import=yt_dlp `
            youtube_downloader.py
    }

    if ($LASTEXITCODE -ne 0) {
        throw "PyInstaller è terminato con errore (codice: $LASTEXITCODE)"
    }
} catch {
    Write-Host "`n--- Fine Output PyInstaller ---`n" -ForegroundColor DarkGray
    Write-ColorOutput "Errore durante la build!" -Type Error
    Write-ColorOutput $_.Exception.Message -Type Error
    exit 1
}

Write-Host "--- Fine Output PyInstaller ---`n" -ForegroundColor DarkGray

# Verifica che l'eseguibile sia stato creato
$exePath = "dist\YouTubeDownloader.exe"
if (Test-Path $exePath) {
    $exeSize = (Get-Item $exePath).Length / 1MB
    Write-ColorOutput "`nBUILD COMPLETATA CON SUCCESSO!" -Type Success
    Write-ColorOutput "Eseguibile creato: $exePath" -Type Success
    Write-ColorOutput "Dimensione: $($exeSize.ToString('0.00')) MB" -Type Info

    # Informazioni finali
    Write-Host "`n========================================" -ForegroundColor Magenta
    Write-Host "  Istruzioni" -ForegroundColor Magenta
    Write-Host "========================================" -ForegroundColor Magenta
    Write-ColorOutput "`n1. L'eseguibile si trova in: $exePath" -Type Info
    Write-ColorOutput "2. Puoi distribuirlo singolarmente" -Type Info
    Write-ColorOutput "3. IMPORTANTE: FFmpeg deve essere installato sul PC di destinazione!" -Type Warning
    Write-ColorOutput "4. Testa l'eseguibile prima della distribuzione" -Type Info

    # Opzione per aprire la cartella dist
    Write-Host "`n"
    $openFolder = Read-Host "Vuoi aprire la cartella dist? (S/N)"
    if ($openFolder -eq 'S' -or $openFolder -eq 's') {
        Invoke-Item "dist"
    }

} else {
    Write-ColorOutput "`nBuild fallita! L'eseguibile non è stato creato." -Type Error
    Write-ColorOutput "Controlla l'output di PyInstaller per i dettagli." -Type Error
    exit 1
}

Write-Host "`n"
