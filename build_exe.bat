@echo off
REM Script batch per eseguire il build dell'eseguibile
REM Semplicemente chiama lo script PowerShell

echo ========================================
echo   YouTube Downloader - Build Script
echo ========================================
echo.

powershell -ExecutionPolicy Bypass -File "%~dp0build_exe.ps1"

if %errorlevel% neq 0 (
    echo.
    echo Errore durante la build!
    pause
    exit /b %errorlevel%
)

pause
