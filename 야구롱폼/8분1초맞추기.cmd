@echo off
chcp 65001 >nul
rem 10/15: extend the finished longform (2026-10-15) to totalSec 8:01 by appending the end screen. No re-render (under 1 minute).
cd /d "%~dp0.."
set SYS=
for /d %%D in (*) do if exist "%%D\run_daily.py" set SYS=%%D
if "%SYS%"=="" (echo run_daily.py not found ^& pause ^& exit /b)
cd /d "%SYS%"
python -X utf8 tools\extend_tail_1015.py
pause
