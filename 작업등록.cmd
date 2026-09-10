@echo off
chcp 65001 >nul
set HERE=%~dp0
schtasks /Delete /TN "BaseballVending" /F >nul 2>&1
schtasks /Create /SC DAILY /ST 07:30 /TN "BaseballVending" /RL HIGHEST /F /TR "cmd /c cd /d \"%HERE%\" && (if exist .git git pull -q --ff-only) && python -X utf8 run_daily.py > data\run_log.txt 2>&1"
if %errorlevel%==0 (echo OK: every day 07:30) else (echo FAILED - run as administrator)
pause
