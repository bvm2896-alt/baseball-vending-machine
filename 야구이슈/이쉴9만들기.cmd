rem Build 2026-09-23_issue9 (KT 2021 tiebreaker story) alone (2026-09-23 early morning).
rem Voice zip must be in ../yagu-issue/voice. When the log says "Watch started" (gamsi sijak), close this window.
@echo off
chcp 65001 >nul
cd /d "%~dp0.."
set SYS=
for /d %%D in (*) do if exist "%%D\run_daily.py" set SYS=%%D
if "%SYS%"=="" (echo run_daily.py not found & pause & exit /b)
cd /d "%SYS%"
python -X utf8 -c "import subprocess,sys;p='episodes/2026-09-23_\uc774\uc2749.json';print('=== build',p,'===');subprocess.call([sys.executable,'-X','utf8','run_daily.py','--episode',p,'--force','--no-fetch','--now','--no-shutdown'])"
pause
