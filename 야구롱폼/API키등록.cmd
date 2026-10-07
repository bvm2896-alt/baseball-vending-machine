@echo off
chcp 65001 >nul
rem Register the Typecast API key as Windows user environment variables (company PC: settings file gets encrypted by DRM).
rem Run once. Paste the values from the home PC settings file. Never paste the key into chat.
cd /d "%~dp0.."
set SYS=
for /d %%D in (*) do if exist "%%D\run_daily.py" set SYS=%%D
if "%SYS%"=="" (echo run_daily.py not found ^& pause ^& exit /b)
cd /d "%SYS%"
python -X utf8 tools\register_api_key.py
pause
